import os, sys, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("sys", "hostname; uname -r; nproc; free -g | head -2"),
    ("disk", "df -h | head -25"),
    ("data", "ls -la /data/ 2>&1 | head -20; echo ---; ls -la /data/heluofan 2>&1 | head -40"),
    ("mount", "mount | grep -Ei 'data|nvme|sd' | head -20"),
    ("tools", "for t in aria2c axel curl wget python3 p7zip unzip tmux screen nohup setsid; do printf '%-10s ' $t; command -v $t || echo MISSING; done"),
    ("py", "python3 -V 2>&1; echo ---; ls /data/heluofan/envs 2>&1 | head"),
]

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    for tag, c in CMDS:
        out.append("=" * 20 + " " + tag)
        out.append("$ " + c)
        try:
            _, o, e = cli.exec_command(c, timeout=90)
            out.append(o.read().decode("utf-8", "replace").rstrip())
            err = e.read().decode("utf-8", "replace").rstrip()
            if err:
                out.append("[stderr] " + err)
        except Exception as ex:
            out.append("[FAIL] " + repr(ex))
    cli.close()
    with open(r"C:\lunwen\_ssh_health.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
