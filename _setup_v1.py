import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
PY=/data/heluofan/envs/ms/bin/python
VENV=/data/heluofan/picai/venv_v1
SRC=/data/heluofan/picai/repos/nnUNet_v1/nnUNet-1.7.0
echo "=== venv ==="
$PY -m venv --system-site-packages $VENV 2>&1 | tail -3
echo "venv_rc=$?"
ls $VENV/bin/python 2>&1
echo "=== medpy ==="
$VENV/bin/python -m pip install -q medpy 2>&1 | tail -4
$VENV/bin/python -c "import medpy; print('medpy OK')" 2>&1 | tail -2
echo "=== nnunet install ==="
cd $SRC && $VENV/bin/python -m pip install -q --no-deps -e . 2>&1 | tail -6
echo "=== which ==="
ls $VENV/bin | grep -i nnunet | head
echo "=== sitecustomize ==="
cat > $VENV/lib/python3.10/site-packages/sitecustomize.py <<'EOF'
try:
    import functools, torch
    _o = torch.load
    if not getattr(_o, "_picai_patched", False):
        @functools.wraps(_o)
        def _load(*a, **kw):
            kw.setdefault("weights_only", False)
            return _o(*a, **kw)
        _load._picai_patched = True
        torch.load = _load
except Exception:
    pass
EOF
echo "sitecustomize written"
echo "=== verify ==="
$VENV/bin/python -c "import torch, torch.load as _x" 2>/dev/null
$VENV/bin/python - <<'EOF'
import torch, numpy
print("patched torch.load:", getattr(torch.load, "_picai_patched", False))
print("numpy", numpy.__version__)
mods = [
 "nnunet.training.network_training.nnUNetTrainerV2",
 "nnunet.training.network_training.nnUNetTrainer",
 "nnunet.experiment_planning.experiment_planner_baseline_3DUNet_v21",
 "nnunet.inference.predict",
 "nnunet.preprocessing.preprocessing",
]
for m in mods:
    try:
        __import__(m); print("IMPORT OK  ", m)
    except Exception as e:
        print("IMPORT FAIL", m, "->", type(e).__name__, str(e)[:160])
EOF
echo "ENV_DONE"
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_setup_v1.sh && bash /tmp/_setup_v1.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=900)
        o.channel.settimeout(900)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_setupv1.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
