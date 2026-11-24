import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
R = "/data/heluofan/picai"

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
VENV=/data/heluofan/picai/venv_v1
TASK=Task2201_picai_baseline
RAW=/data/heluofan/picai/workdir/nnUNet_raw_data
TD=$RAW/$TASK

echo "===== 等待转换结束 ====="
for i in $(seq 1 180); do
  if ! pgrep -f prepare_1500.py > /dev/null; then echo "converter finished (waited ${i}0s)"; break; fi
  sleep 10
done
tail -4 /data/heluofan/picai/prepare.log

echo "===== 格式核对 ====="
echo -n "imagesTr="; ls $TD/imagesTr/*.nii.gz 2>/dev/null | wc -l
echo -n "labelsTr="; ls $TD/labelsTr/*.nii.gz 2>/dev/null | wc -l
echo "--- imagesTr 命名样例 ---"; ls $TD/imagesTr | head -6
echo "--- labelsTr 命名样例 ---"; ls $TD/labelsTr | head -3
echo "--- 某例完整文件 ---"; ls $TD/imagesTr/10000_1000000* 2>/dev/null
echo "--- dataset.json ---"; cat $TD/dataset.json
echo "--- splits.json 摘要 ---"; $VENV/bin/python -c "
import json;s=json.load(open('$TD/splits.json'))
print('folds',len(s));
[print(' fold',i,'train',len(x['train']),'val',len(x['val'])) for i,x in enumerate(s)]
print(' sample val', s[0]['val'][:3])
"

echo "===== 启动 plan_and_preprocess (仅 3d_fullres) ====="
export nnUNet_raw_data_base=/data/heluofan/picai/workdir/nnUNet_raw_data
export nnUNet_preprocessed=/data/heluofan/picai/workdir/nnUNet_preprocessed
export RESULTS_FOLDER=/data/heluofan/picai/workdir/results
mkdir -p $nnUNet_preprocessed $RESULTS_FOLDER
(setsid nohup $VENV/bin/nnUNet_plan_and_preprocess -t 2201 -pl2d None -pl3d ExperimentPlanner3D_v21 --verify_dataset_integrity -tl 16 -tf 16 > /data/heluofan/picai/plan.log 2>&1 < /dev/null &)
echo "plan launched"
sleep 25
echo "--- plan.log head ---"
tail -20 /data/heluofan/picai/plan.log
echo PLAN_STAGE_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_cont.sh && bash /tmp/_cont.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=1800)
        o.channel.settimeout(1800)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_cont.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
