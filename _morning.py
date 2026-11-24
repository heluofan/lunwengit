import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("proc", "ps -ef | grep '[d]l_picai' | wc -l; echo '---log tail---'; tail -20 /data/heluofan/picai/dl_v2.log"),
    ("files", "ls -la /data/heluofan/picai/downloads/*.zip 2>/dev/null; echo '---parts---'; ls /data/heluofan/picai/downloads | grep -c '.tmp$'"),
    ("du", "du -sh /data/heluofan/picai/downloads; df -h /data | tail -1"),
    ("gpu", "nvidia-smi --query-gpu=index,memory.used --format=csv,noheader"),
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
    with open(r"C:\lunwen\_morning.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
