import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("owner", "ls -ld /data/heluofan /data/heluofan/seg_work /data/heluofan/picai 2>/dev/null"),
    ("data", "ls -ld /data/* 2>/dev/null"),
    ("size", "du -sh /data/heluofan 2>/dev/null; df -h /data | tail -1"),
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
    with open(r"C:\lunwen\_owner.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
