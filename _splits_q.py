import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
VENV=/data/heluofan/picai/venv_v1
BASE=/data/heluofan/picai/repos/picai_baseline/picai_baseline-main
echo "=== splits 覆盖范围 ==="
$VENV/bin/python - <<'EOF'
from picai_baseline.splits.picai_nnunet import nnunet_splits as s
alld=set()
for f in s:
    tr=set(f['train']); va=set(f['val'])
    print('fold', f.get('fold'), 'train', len(tr), 'val', len(va))
    alld |= tr|va
print('UNION cases =', len(alld))
import picai_baseline.splits.picai as p
print('picai_pub splits folds =', len(p.nnunet_splits))
EOF
echo "=== README Data Preprocessing ==="
sed -n '100,148p' $BASE/README.md
echo "=== unzip 进度 ==="
tail -6 /data/heluofan/picai/unzip.log
find /data/heluofan/picai/images -name '*.mha' | wc -l
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_q.sh && bash /tmp/_q.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=300)
        o.channel.settimeout(300)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_splits_q.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
