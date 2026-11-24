import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
VENV=/data/heluofan/picai/venv_v1
$VENV/bin/python - <<'EOF'
import SimpleITK as sitk, glob, os, collections
ROOT = "/data/heluofan/picai"
IMG = ROOT + "/images"
HE = ROOT + "/repos/picai_labels/picai_labels-main/csPCa_lesion_delineations/human_expert"

def check(group, limit=None):
    files = sorted(glob.glob(os.path.join(HE, group, "*.nii.gz")))
    if limit: files = files[:limit]
    stat = collections.Counter()
    bad = []
    for f in files:
        case = os.path.basename(f)[:-7]
        pid = case.split("_")[0]
        t2 = os.path.join(IMG, pid, case + "_t2w.mha")
        if not os.path.exists(t2):
            stat["no_t2w"] += 1; bad.append((case, "no_t2w")); continue
        try:
            a = sitk.ReadImage(f); b = sitk.ReadImage(t2)
        except Exception as e:
            stat["read_err"] += 1; bad.append((case, repr(e)[:60])); continue
        sz = a.GetSize() == b.GetSize()
        sp = all(abs(x-y) < 1e-3 for x, y in zip(a.GetSpacing(), b.GetSpacing()))
        og = all(abs(x-y) < 1e-3 for x, y in zip(a.GetOrigin(), b.GetOrigin()))
        grid = sz and sp
        stat["grid_same" if grid else "grid_diff"] += 1
        stat["origin_same" if og else "origin_diff"] += 1
        if not grid and len(bad) < 6:
            bad.append((case, "mask%s vs img%s  sp%s/%s" % (a.GetSize(), b.GetSize(), tuple(round(v,2) for v in a.GetSpacing()), tuple(round(v,2) for v in b.GetSpacing()))))
    print("### %s : %d files" % (group, len(files)))
    for k, v in sorted(stat.items()): print("   %-12s %d" % (k, v))
    for b in bad[:6]: print("   e.g.", b)

check("resampled", limit=30)
check("Pooch25")
EOF
echo GRID_CHECK_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_grid.sh && bash /tmp/_grid.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=900)
        o.channel.settimeout(900)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_grid.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
