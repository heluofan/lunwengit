import os, time, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
LOCAL = r"C:\lunwen\dl_picai.py"
RUNDIR = "/data/heluofan/picai"
REMOTE = RUNDIR + "/dl_picai.py"

log = []

def main():
    t = paramiko.Transport((HOST, PORT))
    t.connect(username=USER, password=PW)
    sftp = paramiko.SFTPClient.from_transport(t)

    for d in [RUNDIR, RUNDIR + "/downloads"]:
        try:
            sftp.stat(d)
        except IOError:
            sftp.mkdir(d)
            log.append("mkdir " + d)

    sftp.put(LOCAL, REMOTE)
    log.append("uploaded dl_picai.py -> %s (%d bytes)" % (REMOTE, sftp.stat(REMOTE).st_size))
    sftp.close()

    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = ("cd %s && setsid nohup python3 dl_picai.py >> dl.log 2>&1 < /dev/null & "
           "sleep 3; echo PID_LIST:; pgrep -af dl_picai.py | head -3; echo LOGHEAD:; head -6 dl.log") % RUNDIR
    _, o, e = cli.exec_command(cmd, timeout=60)
    log.append(o.read().decode("utf-8", "replace"))
    err = e.read().decode("utf-8", "replace").strip()
    if err:
        log.append("[stderr] " + err)
    cli.close()

    with open(r"C:\lunwen\_dl_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("DONE")

main()
