import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
W = "/data/heluofan/picai/workdir"

CMDS = [
    ("proc", "pgrep -f nnUNet_plan_and_preprocess | wc -l; echo '---'; ps -ef | grep '[n]nUNet_plan' | head -2"),
    ("log", "wc -l /data/heluofan/picai/plan.log 2>/dev/null; tail -25 /data/heluofan/picai/plan.log 2>/dev/null"),
    ("dirs", "du -sh %s/nnUNet_preprocessed %s/nnUNet_cropped_data 2>/dev/null; ls %s/nnUNet_preprocessed 2>/dev/null" % (W, W, W)),
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
            _, o, e = cli.exec_command(c, timeout=60)
            o.channel.settimeout(60)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_plstat.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
