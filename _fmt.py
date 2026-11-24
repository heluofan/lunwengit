import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
TD = "/data/heluofan/picai/workdir/nnUNet_raw_data/Task2201_picai_baseline"

CMDS = [
    ("proc", "pgrep -f prepare_1500.py | wc -l; echo '--- log ---'; tail -3 /data/heluofan/picai/prepare.log"),
    ("count", "echo -n 'imagesTr='; ls %s/imagesTr/*.nii.gz 2>/dev/null | wc -l; echo -n 'labelsTr='; ls %s/labelsTr/*.nii.gz 2>/dev/null | wc -l" % (TD, TD)),
    ("names", "ls %s/imagesTr 2>/dev/null | head -5; echo '--labels--'; ls %s/labelsTr 2>/dev/null | head -3" % (TD, TD)),
    ("dsjson", "cat %s/dataset.json 2>/dev/null" % TD),
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
    with open(r"C:\lunwen\_fmt.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
