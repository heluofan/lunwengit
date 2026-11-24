import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
VENV=/data/heluofan/picai/venv_v1
W=/data/heluofan/picai/workdir
TD=$W/nnUNet_raw_data/Task2201_picai_baseline

echo "===== 1. 修 dataset.json modality ====="
$VENV/bin/python - <<'EOF'
import json
p="/data/heluofan/picai/workdir/nnUNet_raw_data/Task2201_picai_baseline/dataset.json"
d=json.load(open(p))
print("before:", d["modality"])
d["modality"]={"0":"T2W","1":"ADC","2":"HBV"}
d["description"]="bpMRI (T2W+ADC+HBV) from PI-CAI public dataset, 1500 cases (1295 expert + 205 Pooch25)"
json.dump(d,open(p,"w"),indent=4)
print("after :", json.load(open(p))["modality"])
EOF

echo "===== 2. 对齐 nnU-Net v1 目录层级 ====="
ln -sfn $W/nnUNet_raw_data $W/nnUNet_raw
ls -ld $W/nnUNet_raw
ls $W/nnUNet_raw/Task2201_picai_baseline/ | head -6

echo "===== 3. 启动 plan_and_preprocess ====="
export nnUNet_raw_data_base=$W
export nnUNet_preprocessed=$W/nnUNet_preprocessed
export RESULTS_FOLDER=$W/results
mkdir -p $nnUNet_preprocessed $RESULTS_FOLDER $W/nnUNet_cropped_data
(setsid nohup $VENV/bin/nnUNet_plan_and_preprocess -t 2201 -pl2d None -pl3d ExperimentPlanner3D_v21 --verify_dataset_integrity -tl 16 -tf 16 > /data/heluofan/picai/plan.log 2>&1 < /dev/null &)
sleep 30
echo "procs=$(pgrep -f nnUNet_plan_and_preprocess | wc -l)"
echo "--- plan.log ---"
tail -30 /data/heluofan/picai/plan.log
echo PLAN_RESTART_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_fx.sh && bash /tmp/_fx.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=110)
        o.channel.settimeout(110)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_fix.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
