import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
LOCAL = r"C:\lunwen\research_audit\picai_sop_20261123\case_manifest.csv"
RUNDIR = "/data/heluofan/picai"

SH = r'''#!/bin/bash
VENV=/data/heluofan/picai/venv_v1
$VENV/bin/python - <<'EOF'
import csv, collections
from picai_baseline.splits.picai_nnunet import nnunet_splits

official = {}
for i, f in enumerate(nnunet_splits):
    for c in f['val']:
        official[c] = i

rows = list(csv.DictReader(open('/data/heluofan/picai/case_manifest.csv')))
print("rows:", len(rows), "cols:", list(rows[0].keys()))
in_off = [r for r in rows if r['case_id'] in official]
extra = [r for r in rows if r['case_id'] not in official]
print("in official splits:", len(in_off), " extra:", len(extra))

mis = [(r['case_id'], r['fold'], official[r['case_id']]) for r in in_off if int(r['fold']) != official[r['case_id']]]
print("fold mismatch vs official:", len(mis), mis[:5])

print("extra fold dist:", dict(collections.Counter(r['fold'] for r in extra)))
print("extra label dist:", dict(collections.Counter(r['has_lesion'] for r in extra)))

# 患者是否跨折
byp = collections.defaultdict(set)
for r in rows:
    byp[r['patient_id']].add(r['fold'])
multi = {p: v for p, v in byp.items() if len(v) > 1}
print("patients spanning >1 fold:", len(multi), list(multi.items())[:5])

# 每折统计
for fo in sorted(set(r['fold'] for r in rows)):
    sub = [r for r in rows if r['fold'] == fo]
    print("fold %s: n=%d pos=%d pats=%d" % (fo, len(sub), sum(1 for r in sub if r['has_lesion'] == 'True'), len(set(r['patient_id'] for r in sub))))
EOF
echo SPLIT_CHECK_DONE
'''

def main():
    t = paramiko.Transport((HOST, PORT))
    t.connect(username=USER, password=PW)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(LOCAL, RUNDIR + "/case_manifest.csv")
    ok = sftp.stat(RUNDIR + "/case_manifest.csv").st_size
    sftp.close()

    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_sc.sh && bash /tmp/_sc.sh 2>&1" % b64
    out = ["manifest uploaded: %d bytes" % ok]
    try:
        _, o, e = cli.exec_command(cmd, timeout=300)
        o.channel.settimeout(300)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_splitcheck.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
