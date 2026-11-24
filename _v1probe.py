import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

PY = "/data/heluofan/envs/ms/bin/python"
SRC = "/data/heluofan/picai/repos/nnUNet_v1"

PROBE = r'''
import sys, os, warnings
warnings.filterwarnings("ignore")
print("python", sys.version.split()[0])
import numpy; print("numpy", numpy.__version__)
import torch; print("torch", torch.__version__, "cuda", torch.version.cuda)
print("cap", torch.cuda.get_device_capability(0), "dev", torch.cuda.get_device_name(0))

# 1) torch.load 默认行为
import torch as T
p = "/tmp/_probe.pt"
T.save({"a": 1}, p)
try:
    T.load(p); print("LOAD default: OK(weights_only=True 放过了纯 dict)")
except Exception as e:
    print("LOAD default: FAIL", type(e).__name__, str(e)[:110])
try:
    T.load(p, weights_only=False); print("LOAD w_only=False: OK")
except Exception as e:
    print("LOAD w_only=False: FAIL", str(e)[:110])

# 2) 带自定义类的 pickle（模拟 nnU-Net plans.pkl）
class Dummy:
    def __init__(self): self.x = 1
T.save({"obj": Dummy()}, p)
try:
    T.load(p); print("LOAD obj default: OK")
except Exception as e:
    print("LOAD obj default: FAIL", type(e).__name__)
try:
    T.load(p, weights_only=False); print("LOAD obj w_only=False: OK")
except Exception as e:
    print("LOAD obj w_only=False: FAIL", str(e)[:110])

# 3) import nnU-Net v1
sys.path.insert(0, os.environ.get("NNUNET_SRC", ""))
mods = [
    "nnunet.training.network_training.nnUNetTrainerV2",
    "nnunet.training.network_training.nnUNetTrainer",
    "nnunet.preprocessing.preprocessing",
    "nnunet.experiment_planning.experiment_planner_baseline_3DUNet_v21",
    "nnunet.inference.predict",
]
for m in mods:
    try:
        __import__(m); print("IMPORT OK  ", m)
    except Exception as e:
        print("IMPORT FAIL", m, "->", type(e).__name__, str(e)[:140])

# 4) 前向是否能在 sm_120 上算
try:
    import torch.nn as nn
    net = nn.Sequential(nn.Conv3d(4, 8, 3, padding=1), nn.InstanceNorm3d(8), nn.LeakyReLU()).cuda()
    x = torch.randn(1, 4, 32, 64, 64, device="cuda")
    y = net(x)
    loss = y.mean(); loss.backward()
    print("SM120 FORWARD+BACKWARD: OK", tuple(y.shape))
except Exception as e:
    print("SM120 FORWARD: FAIL", type(e).__name__, str(e)[:160])
'''

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)

    b64 = base64.b64encode(PROBE.encode()).decode()
    cmd = ("mkdir -p %s && cd /data/heluofan/picai/repos && python3 -m zipfile -e nnUNet_v1.zip %s/ && "
           "ls -d %s/* && "
           "echo %s | base64 -d > /tmp/_probe.py && NNUNET_SRC=%s/nnUNet-1.7.0 %s /tmp/_probe.py 2>&1"
           % (SRC, SRC, SRC, b64, SRC, PY))
    try:
        _, o, e = cli.exec_command(cmd, timeout=240)
        o.channel.settimeout(240)
        out.append(o.read().decode("utf-8", "replace"))
        err = e.read().decode("utf-8", "replace").strip()
        if err:
            out.append("[stderr] " + err[-800:])
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:200])
    cli.close()
    with open(r"C:\lunwen\_v1probe.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
