import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("left", "du -sh --max-depth=0 /data/heluofan/* 2>/dev/null | sort -hr | head -20"),
    ("total", "du -sh /data/heluofan 2>/dev/null; df -h /data | tail -1"),
    ("bk", "ls -lh /data/heluofan/_seg_metrics_20261124.tar.gz 2>/dev/null; tar tzf /data/heluofan/_seg_metrics_20261124.tar.gz 2>/dev/null | head -20"),
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
    with open(r"C:\lunwen\_final.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
