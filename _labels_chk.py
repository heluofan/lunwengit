import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
L = "/data/heluofan/picai/repos/picai_labels"

CMDS = [
    "tail -3 /data/heluofan/picai/dl_v2.log",
    "ls %s" % L,
    "ls %s/csPCa_lesion_delineations/human_expert" % L,
    "for d in original resampled Pooch25; do echo -n \"$d: \"; ls %s/csPCa_lesion_delineations/human_expert/$d/*.nii.gz 2>/dev/null | wc -l; done" % L,
    "ls %s/csPCa_lesion_delineations/ " % L,
    "du -sh %s; du -sh %s/*" % (L, L),
    "head -3 %s/csPCa_lesion_delineations/human_expert/Pooch25/*.nii.gz 2>/dev/null | head -1" % L,
]

def main():
    out = []
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    for c in CMDS:
        try:
            _, o, e = cli.exec_command(c, timeout=60)
            o.channel.settimeout(60)
            out.append("$ " + c)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("$ " + c)
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_labels_chk.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
