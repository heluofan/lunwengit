"""STU-Net for Dataset501_Flare22 on nnU-Net 2.8.1.

ADAPT-1  nnU-Net 2.2 -> 2.8 removed `unpack_dataset` from nnUNetTrainer.__init__.
         STU-Net's official v2 trainer still passes it -> we override __init__.
         NOTE: nnUNetTrainer.__init__ reflects on locals(), so every subclass
         __init__ MUST use explicit parameter names (no *args/**kwargs).
ADAPT-2  Official STUNet.forward() concatenates without size reconciliation;
         patch dims must be divisible by 2**n_pool (=32). nnU-Net plans give
         [40,224,192] -> handled at plans level (patch -> [32,224,192]).
ADAPT-3  Totalsegmentator ckpt has 105 output channels; FLARE22 has 14.
         Load only shape-matching tensors (120/130); reinit seg_outputs.
"""
import os
import torch
from STUNetTrainer import STUNet, STUNetTrainer_small

PRETRAINED = "/data/heluofan/seg_work/baselines/stu-net/stu-net-s-small_ep4k.model"


class _Base(STUNetTrainer_small):
    def __init__(self, plans: dict, configuration: str, fold: int,
                 dataset_json: dict, device: torch.device = torch.device("cuda")):
        # ADAPT-1: drop unpack_dataset (removed in nnU-Net 2.8)
        nnUNetTrainer_small_mro = STUNetTrainer_small.__mro__
        base_init = nnUNetTrainer_small_mro[2].__init__   # nnUNetTrainer.__init__
        base_init(self, plans, configuration, fold, dataset_json, device)
        self.num_epochs = 1000
        self.initial_lr = 1e-3

    @staticmethod
    def build_network_architecture(plans_manager, configuration_manager,
                                   num_input_channels, num_output_channels,
                                   enable_deep_supervision=True):
        strides = configuration_manager.pool_op_kernel_sizes[1:][:5]
        while len(strides) < 5:
            strides.append([1, 1, 1])
        return STUNet(
            num_input_channels, num_output_channels,
            depth=[1] * 6,
            dims=[16 * x for x in [1, 2, 4, 8, 16, 16]],
            pool_op_kernel_sizes=strides,
            conv_kernel_sizes=[[3, 3, 3]] * 6,
            enable_deep_supervision=enable_deep_supervision,
        )

    def _load_pretrained(self):
        if os.environ.get("STU_PRETRAIN", "0") != "1":
            print("STU_PRETRAIN=0 -> from scratch")
            return
        ck = torch.load(PRETRAINED, map_location="cpu", weights_only=False)
        sd = ck["state_dict"] if "state_dict" in ck else ck
        nsd = self.network.state_dict()
        loadable = {k: v for k, v in sd.items()
                    if k in nsd and tuple(nsd[k].shape) == tuple(v.shape)}
        dropped = [k for k in sd if k not in loadable]
        missing, _ = self.network.load_state_dict(loadable, strict=False)
        print("STU_PRETRAIN=1 loaded %d/%d; dropped_by_shape=%d; reinit=%d"
              % (len(loadable), len(nsd), len(dropped), len(missing)))
        print("  dropped:", dropped[:4])

    def initialize(self):
        super().initialize()
        self._load_pretrained()


class STUNetFlareTrainer(_Base):
    """Full 1000-epoch STU-Net-small baseline for FLARE22."""
    pass


class STUNetFlareTrainer_1ep(_Base):
    """SMOKE ONLY - 2 epochs. Metrics are NOT results."""
    def __init__(self, plans: dict, configuration: str, fold: int,
                 dataset_json: dict, device: torch.device = torch.device("cuda")):
        super().__init__(plans, configuration, fold, dataset_json, device)
        self.num_epochs = 2
        self.num_val_batches_per_epoch = 1
        self.save_every = 1
