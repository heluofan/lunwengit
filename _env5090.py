import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

CMDS = [
    ("gpu", "nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader"),
    ("dl", "tail -3 /data/heluofan/picai/dl_v2.log; echo '--- nnunet ---'; cat /data/heluofan/picai/nnunet_dl.log 2>/dev/null | tail -3"),
    ("envs", "ls -d ~/miniforge3/envs/* /data/heluofan/envs/* 2>/dev/null"),
    ("torch", "for p in ~/miniforge3/envs/*/bin/python /data/heluofan/envs/*/bin/python; do [ -x $p ] || continue; echo -n \"$p : \"; $p -c \"import torch;print(torch.__version__, torch.version.cuda, torch.cuda.get_device_capability(0) if torch.cuda.is_available() else 'no-cuda')\" 2>&1 | head -1; done"),
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
            _, o, e = cli.exec_command(c, timeout=180)
            o.channel.settimeout(180)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_env5090.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
