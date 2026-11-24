import os, sys, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

def run(cli, cmd, out, timeout=45):
    try:
        _, o, e = cli.exec_command(cmd, timeout=timeout)
        o.channel.settimeout(timeout)
        txt = o.read().decode("utf-8", "replace")
        err = e.read().decode("utf-8", "replace")
        out.append("$ " + cmd)
        out.append(txt.rstrip())
        if err.strip():
            out.append("[stderr] " + err.strip())
    except Exception as ex:
        out.append("$ " + cmd)
        out.append("[EXC] " + repr(ex))
    out.append("")

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    run(cli, "ls -la /data/heluofan/picai/ 2>&1", out)
    run(cli, "ls -la /data/heluofan/picai/downloads/ 2>&1 | head -5; echo COUNT=$(ls /data/heluofan/picai/downloads/ 2>/dev/null | wc -l)", out)
    run(cli, "ps -ef | grep -c '[d]l_picai.py'; echo '---'; tail -8 /data/heluofan/picai/dl.log 2>&1", out)
    cli.close()
    with open(r"C:\lunwen\_dl_stat.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
