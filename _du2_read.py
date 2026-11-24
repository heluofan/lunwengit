import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

def main():
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    out = []
    try:
        _, o, e = cli.exec_command("cat /data/heluofan/_du_scan2.txt 2>/dev/null", timeout=60)
        o.channel.settimeout(60)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:150])
    cli.close()
    with open(r"C:\lunwen\_du_scan2_local.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("LEN=%d" % len(out[0]))

main()
