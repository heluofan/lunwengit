import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

DIRS = ["seg_work", "models", "image", "der_data"]

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    for d in DIRS:
        out.append("######## " + d)
        c = "du -sh --max-depth=1 /data/heluofan/%s/* 2>/dev/null | sort -hr | head -18" % d
        try:
            _, o, e = cli.exec_command(c, timeout=105)
            o.channel.settimeout(105)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[TIMEOUT/EXC] " + repr(ex)[:120])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_du2.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
