import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

def main():
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    out = []
    for c in ("cat /data/heluofan/_cleanup2.log 2>/dev/null",
              "pgrep -f _clean2.sh | wc -l"):
        try:
            _, o, e = cli.exec_command(c, timeout=60)
            o.channel.settimeout(60)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:120])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_c2log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
