#!/usr/bin/env python3
"""Launch the corrected-label PET/CT nnU-Net five-fold baseline remotely."""

import os
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: launch_corrected_petct_baseline.py RUN_ROOT")

    run_root = Path(sys.argv[1])
    if run_root.exists() and any(run_root.iterdir()):
        raise SystemExit(f"refusing to use non-empty output directory: {run_root}")
    run_root.mkdir(parents=True, exist_ok=True)

    data_root = Path("/data/heluofan/seg_work/datasets")
    binary = Path("/data/heluofan/envs/ms/bin/nnUNetv2_train")
    if not binary.is_file():
        raise SystemExit(f"nnU-Net entry point missing: {binary}")

    folds = [(0, 1), (1, 2), (2, 3), (3, 5), (4, 6)]
    env_base = os.environ.copy()
    env_base.update(
        {
            "nnUNet_raw": str(data_root / "nnUNet_raw"),
            "nnUNet_preprocessed": str(data_root / "nnUNet_preprocessed"),
            "nnUNet_results": str(run_root),
            "nnUNet_n_proc_DA": "6",
        }
    )

    processes = []
    for fold, gpu in folds:
        env = env_base.copy()
        env["CUDA_VISIBLE_DEVICES"] = str(gpu)
        log_path = run_root / f"fold_{fold}.log"
        log_handle = log_path.open("w", encoding="utf-8")
        process = subprocess.Popen(
            [str(binary), "701", "3d_fullres", str(fold)],
            cwd=str(data_root),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            close_fds=True,
        )
        log_handle.close()
        processes.append((fold, gpu, process.pid))

    for fold, gpu, pid in processes:
        print(f"fold={fold} gpu={gpu} pid={pid} log={run_root}/fold_{fold}.log")


if __name__ == "__main__":
    main()
