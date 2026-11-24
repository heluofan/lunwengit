import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
SRC = "/data/heluofan/picai/repos/nnUNet_v1/nnUNet-1.7.0"

CMDS = [
    ("np-aliases", "grep -rn --include='*.py' -E 'np\\.(float|int|bool|object|str)\\b' %s | grep -v 'np.float32\\|np.float64\\|np.int32\\|np.int64\\|np.bool_\\|np.object_' | head -15 || echo NONE" % SRC),
    ("amp", "grep -rn --include='*.py' 'GradScaler\\|torch.cuda.amp' %s | head -8" % SRC),
    ("dl", "tail -2 /data/heluofan/picai/dl_v2.log; du -sh /data/heluofan/picai/downloads"),
    ("gpu-free", "nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader"),
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
            _, o, e = cli.exec_command(c, timeout=120)
            o.channel.settimeout(120)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_compat.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
