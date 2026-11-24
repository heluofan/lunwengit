import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
RUNDIR = "/data/heluofan/picai"
LOCAL = r"C:\lunwen\dl_picai_v2.py"

log = []

def main():
    t = paramiko.Transport((HOST, PORT))
    t.connect(username=USER, password=PW)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(LOCAL, RUNDIR + "/dl_picai_v2.py")
    log.append("uploaded %d bytes" % sftp.stat(RUNDIR + "/dl_picai_v2.py").st_size)
    sftp.close()

    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    steps = [
        ("kill", "pkill -f dl_picai.py; sleep 2; echo KILLED; ps -ef | grep -c '[d]l_picai'"),
        ("launch", "cd %s && mv -f dl.log dl_v1.log; (setsid nohup python3 dl_picai_v2.py >> dl_v2.log 2>&1 < /dev/null &) ; sleep 3; echo LAUNCHED" % RUNDIR),
    ]
    for tag, c in steps:
        try:
            _, o, e = cli.exec_command(c, timeout=30)
            o.channel.settimeout(30)
            log.append(tag + ": " + o.read().decode("utf-8", "replace").strip().replace("\n", " | "))
        except Exception as ex:
            log.append(tag + " [EXC] " + repr(ex)[:150])
    cli.close()
    with open(r"C:\lunwen\_v2_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("DONE")

main()
