import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
R = "/data/heluofan/picai"

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
VENV=/data/heluofan/picai/venv_v1
TD=/data/heluofan/picai/workdir/nnUNet_raw_data/Task2201_picai_baseline

echo "imagesTr=$(ls $TD/imagesTr/*.nii.gz 2>/dev/null | wc -l) labelsTr=$(ls $TD/labelsTr/*.nii.gz 2>/dev/null | wc -l)"
if [ -f $TD/dataset.json ]; then echo "=== dataset.json ==="; cat $TD/dataset.json; else echo "NO dataset.json yet"; fi
echo "=== log tail ==="
tail -3 /data/heluofan/picai/prepare.log

if [ ! -f $TD/dataset.json ]; then echo "SKIP_LAUNCH"; exit 0; fi

export nnUNet_raw_data_base=/data/heluofan/picai/workdir/nnUNet_raw_data
export nnUNet_preprocessed=/data/heluofan/picai/workdir/nnUNet_preprocessed
export RESULTS_FOLDER=/data/heluofan/picai/workdir/results
mkdir -p $nnUNet_preprocessed $RESULTS_FOLDER
echo "=== 启动 plan_and_preprocess ==="
(setsid nohup $VENV/bin/nnUNet_plan_and_preprocess -t 2201 -pl2d None -pl3d ExperimentPlanner3D_v21 --verify_dataset_integrity -tl 16 -tf 16 > /data/heluofan/picai/plan.log 2>&1 < /dev/null &)
sleep 20
echo "--- plan.log ---"
tail -25 /data/heluofan/picai/plan.log
echo LAUNCH_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_pl.sh && bash /tmp/_pl.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=100)
        o.channel.settimeout(100)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_pl.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
