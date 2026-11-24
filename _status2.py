import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    "ps -ef | grep '[d]l_picai' | awk '{print $2, $8, $9, $10}'; echo PROCS=$(ps -ef | grep -c '[d]l_picai')",
    "tail -5 /data/heluofan/picai/dl_v2.log 2>/dev/null || echo NO_V2LOG",
    "du -sh /data/heluofan/picai/downloads; ls /data/heluofan/picai/downloads | grep -c '.tmp$'",
    "df -h /data | tail -1",
]

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    for c in CMDS:
        try:
            _, o, e = cli.exec_command(c, timeout=40)
            o.channel.settimeout(40)
            out.append("$ " + c)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("$ " + c)
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_status2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
