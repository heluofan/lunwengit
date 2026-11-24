#!/usr/bin/env python3
"""PI-CAI 全监督预处理：把 resampled(1295) + Pooch25(205) 合并成 1500 例，转 nnU-Net raw 格式"""
import json, csv, os, sys, time
from pathlib import Path
import SimpleITK as sitk
from picai_prep import MHA2nnUNetConverter
from picai_prep.examples.mha2nnunet.picai_archive import generate_mha2nnunet_settings

ROOT = Path("/data/heluofan/picai")
IMG = ROOT / "images"
LABELS_ROOT = ROOT / "repos/picai_labels/picai_labels-main"
HE = LABELS_ROOT / "csPCa_lesion_delineations/human_expert"
ANN = HE / "merged1500"
WORK = ROOT / "workdir"
TASK = "Task2201_picai_baseline"

def preprocess_picai_annotation(lbl):
    arr = sitk.GetArrayFromImage(lbl)
    arr = (arr >= 1).astype("uint8")
    out = sitk.GetImageFromArray(arr)
    out.CopyInformation(lbl)
    return out

def main():
    t0 = time.time()
    # 1) 合并标注目录（软链）
    ANN.mkdir(parents=True, exist_ok=True)
    n = 0
    for sub in ("resampled", "Pooch25"):
        for f in sorted((HE / sub).glob("*.nii.gz")):
            dst = ANN / f.name
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            os.symlink(str(f), str(dst))
            n += 1
    real = len(list(ANN.glob("*.nii.gz")))
    print("merged annotations: links=%d, visible=%d" % (n, real), flush=True)

    settings_path = WORK / "mha2nnunet_settings" / ("%s.json" % TASK)
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    # 2) 生成转换计划
    if not settings_path.exists():
        generate_mha2nnunet_settings(
            archive_dir=IMG, annotations_dir=ANN,
            output_path=settings_path, task=TASK)
        print("settings written:", settings_path, flush=True)
    s = json.load(open(settings_path))
    print("settings: preprocessing=%s" % json.dumps(s.get("preprocessing", {})), flush=True)
    print("settings: #cases=%d" % len(s.get("archive", s.get("scans", []))) if isinstance(s.get("archive", s.get("scans", [])), list) else "settings: keys=%s" % list(s.keys()), flush=True)

    raw = WORK / "nnUNet_raw_data"
    task_dir = raw / TASK

    # 3) 转换
    if not (task_dir / "dataset.json").exists():
        s.setdefault("options", {})
        s["options"]["annotation_preprocess_func"] = preprocess_picai_annotation
        conv = MHA2nnUNetConverter(
            output_dir=raw, scans_dir=IMG,
            annotations_dir=ANN, mha2nnunet_settings=s)
        conv.convert()
        conv.create_dataset_json()
        print("converted.", flush=True)
    else:
        print("dataset.json exists, skip convert", flush=True)

    # 4) splits（沿用 case_manifest 的 fold，205 例已患者隔离补入）
    rows = list(csv.DictReader(open(ROOT / "case_manifest.csv")))
    splits = []
    for fo in range(5):
        tr = sorted(r["case_id"] for r in rows if int(r["fold"]) != fo)
        va = sorted(r["case_id"] for r in rows if int(r["fold"]) == fo)
        splits.append({"train": tr, "val": va})
    with open(task_dir / "splits.json", "w") as fp:
        json.dump(splits, fp)
    print("splits: " + ", ".join("f%d tr=%d va=%d" % (i, len(x["train"]), len(x["val"])) for i, x in enumerate(splits)), flush=True)

    # 5) 计数
    imgs = list((task_dir / "imagesTr").glob("*.nii.gz"))
    lbls = list((task_dir / "labelsTr").glob("*.nii.gz"))
    print("imagesTr=%d labelsTr=%d elapsed=%.1f min" % (len(imgs), len(lbls), (time.time() - t0) / 60), flush=True)
    print("PREP_ALL_DONE", flush=True)

main()
