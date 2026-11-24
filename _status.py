import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    "tail -4 /data/heluofan/picai/dl.log",
    "du -sh /data/heluofan/picai/downloads 2>/dev/null; ls /data/heluofan/picai/downloads | wc -l",
    "tail -6 /data/heluofan/picai/repos_dl.log 2>/dev/null; echo '--repos--'; du -sh /data/heluofan/picai/repos 2>/dev/null",
    "ps -ef | grep -c '[d]l_picai.py'; ps -ef | grep -c '[r]epos_dl.sh'",
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
            err = e.read().decode("utf-8", "replace").strip()
            if err:
                out.append("[err] " + err)
        except Exception as ex:
            out.append("$ " + c)
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_status.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
