import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
RUNDIR = "/data/heluofan/picai"

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
mkdir -p repos
for t in v1.7.0 v1.7.1 v1; do
  if curl -fsSL --max-time 900 -o repos/nnUNet_v1.zip "https://codeload.github.com/MIC-DKFZ/nnUNet/zip/refs/tags/$t"; then
    echo "NNUNET_V1 tag=$t bytes=$(stat -c%s repos/nnUNet_v1.zip)"; break
  fi
  if curl -fsSL --max-time 900 -o repos/nnUNet_v1.zip "https://codeload.github.com/MIC-DKFZ/nnUNet/zip/refs/heads/$t"; then
    echo "NNUNET_V1 branch=$t bytes=$(stat -c%s repos/nnUNet_v1.zip)"; break
  fi
done
echo DONE_NNUNET
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c1 = "echo %s | base64 -d > %s/nnunet_dl.sh && chmod +x %s/nnunet_dl.sh && echo WROTE" % (b64, RUNDIR, RUNDIR)
    c2 = "cd %s && (setsid bash nnunet_dl.sh >> nnunet_dl.log 2>&1 < /dev/null &) ; sleep 2; echo LAUNCHED" % RUNDIR
    out = []
    for c in (c1, c2):
        try:
            _, o, e = cli.exec_command(c, timeout=25)
            o.channel.settimeout(25)
            out.append(o.read().decode("utf-8", "replace").strip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:120])
    cli.close()
    with open(r"C:\lunwen\_nn_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
