import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
VENV=/data/heluofan/picai/venv_v1
TD=/data/heluofan/picai/workdir/nnUNet_raw_data/Task2201_picai_baseline
echo "===== 通道顺序验证（数值域比对）====="
$VENV/bin/python - <<'EOF'
import SimpleITK as sitk, numpy as np, os
TD="/data/heluofan/picai/workdir/nnUNet_raw_data/Task2201_picai_baseline"
IMG="/data/heluofan/picai/images"
case="10000_1000000"; pid="10000"
for ch in range(3):
    a=sitk.GetArrayFromImage(sitk.ReadImage(os.path.join(TD,"imagesTr","%s_%04d.nii.gz"%(case,ch))))
    print("nnUNet ch%d  shape=%s  min=%.1f max=%.1f mean=%.1f" % (ch, a.shape, a.min(), a.max(), a.mean()))
print("--- 原始 mha ---")
for seq in ("t2w","adc","hbv"):
    b=sitk.GetArrayFromImage(sitk.ReadImage(os.path.join(IMG,pid,"%s_%s.mha"%(case,seq))))
    print("%-4s        shape=%s  min=%.1f max=%.1f mean=%.1f" % (seq, b.shape, b.min(), b.max(), b.mean()))
EOF

echo "===== splits.json ====="
if [ -f $TD/splits.json ]; then
  $VENV/bin/python -c "
import json;s=json.load(open('$TD/splits.json'))
print('folds',len(s))
[print(' fold',i,'train',len(x['train']),'val',len(x['val'])) for i,x in enumerate(s)]
import itertools
# 患者隔离复查
p=lambda c:c.split('_')[0]
bad=0
for i,x in enumerate(s):
    vt=set(p(c) for c in x['val']); tt=set(p(c) for c in x['train'])
    bad+=len(vt&tt)
print('val/train 患者交集总数 =',bad)
"
else echo "NO splits.json"; fi

echo "===== plan 进程/日志 ====="
echo "procs=$(pgrep -f nnUNet_plan_and_preprocess | wc -l)"
tail -20 /data/heluofan/picai/plan.log 2>/dev/null || echo NO_PLAN_LOG
echo "===== 磁盘 ====="
du -sh /data/heluofan/picai/workdir; df -h /data | tail -1
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_ch.sh && bash /tmp/_ch.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=110)
        o.channel.settimeout(110)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_chan.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
