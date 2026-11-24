import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("recent", "for d in seg_work picai der_data eegfnirs brats_work thyroid_tta models image qwen3-embed bench; do printf '%-14s ' $d; stat -c '%y' /data/heluofan/$d 2>/dev/null | cut -d. -f1; done"),
    ("segwork_newest", "find /data/heluofan/seg_work -type f -newermt '2026-11-15' 2>/dev/null | head -12; echo '--- count ---'; find /data/heluofan/seg_work -type f -newermt '2026-11-15' 2>/dev/null | wc -l"),
    ("segwork_cfg", "ls -lt /data/heluofan/seg_work/*.py /data/heluofan/seg_work/*.sh /data/heluofan/seg_work/datasets/*.csv 2>/dev/null | head -8"),
    ("mos", "head -3 /data/heluofan/seg_work/datasets/all_fdg.json 2>/dev/null | cut -c1-300; echo '---'; head -2 /data/heluofan/seg_work/datasets/cases_all.csv 2>/dev/null; wc -l /data/heluofan/seg_work/datasets/cases_all.csv 2>/dev/null"),
]

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    for tag, c in CMDS:
        out.append("==== " + tag)
        try:
            _, o, e = cli.exec_command(c, timeout=100)
            o.channel.settimeout(100)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_mtime.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
