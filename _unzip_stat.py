import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("unzip", "tail -14 /data/heluofan/picai/unzip.log 2>/dev/null || echo NO_LOG"),
    ("img", "du -sh /data/heluofan/picai/images 2>/dev/null; find /data/heluofan/picai/images -name '*.mha' 2>/dev/null | wc -l"),
    ("proc", "ps -ef | grep -c '[u]nzip.sh'"),
    ("du", "du -sh /data/heluofan/picai/downloads /data/heluofan/picai/images 2>/dev/null; df -h /data | tail -1"),
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
            _, o, e = cli.exec_command(c, timeout=90)
            o.channel.settimeout(90)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_unzip_stat.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
