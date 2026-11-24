import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
VENV=/data/heluofan/picai/venv_v1
BASE=/data/heluofan/picai/repos/picai_baseline/picai_baseline-main
echo "=== pip install picai_prep ==="
$VENV/bin/python -m pip install -q picai_prep 2>&1 | tail -4
$VENV/bin/python -c "import picai_prep; print('picai_prep OK', picai_prep.__file__)" 2>&1 | tail -2
echo "=== pip install picai_baseline ==="
cd $BASE && $VENV/bin/python -m pip install -q --no-deps -e . 2>&1 | tail -4
$VENV/bin/python -c "from picai_baseline.splits.picai_nnunet import nnunet_splits; print('splits OK, folds=', len(nnunet_splits))" 2>&1 | tail -3
echo "=== README: preprocessing 段落 ==="
grep -n -A6 -i "prepare data\|preprocessing_kwargs\|prepare_data.py" $BASE/README.md 2>/dev/null | head -40
echo "PREP_DONE"
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_prep.sh && bash /tmp/_prep.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=600)
        o.channel.settimeout(600)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_prep_env.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
