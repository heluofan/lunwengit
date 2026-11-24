import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
echo "== 清理分块 =="
before=$(du -sm downloads | cut -f1)
rm -f downloads/*.p[0-9][0-9][0-9][0-9][0-9]
rm -f downloads/*.tmp
after=$(du -sm downloads | cut -f1)
echo "downloads: ${before}MB -> ${after}MB"
echo "== 解压 =="
mkdir -p images
for f in downloads/*.zip; do
  echo "--- $f"
  python3 -m zipfile -e "$f" images/ 2>&1 | tail -2
  echo "rc=$? $(du -sh images | cut -f1)"
done
echo "== 结构 =="
find images -maxdepth 2 -type d | head -12
echo "== 计数 =="
for ext in mha nii.gz; do echo -n "$ext="; find images -name "*.$ext" | wc -l; done
echo "UNZIP_DONE"
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c1 = "echo %s | base64 -d > /data/heluofan/picai/unzip.sh && chmod +x /data/heluofan/picai/unzip.sh && echo WROTE" % b64
    c2 = "cd /data/heluofan/picai && (setsid nohup bash unzip.sh >> unzip.log 2>&1 < /dev/null &) ; sleep 2; echo LAUNCHED"
    out = []
    for c in (c1, c2):
        try:
            _, o, e = cli.exec_command(c, timeout=25)
            o.channel.settimeout(25)
            out.append(o.read().decode("utf-8", "replace").strip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:120])
    cli.close()
    with open(r"C:\lunwen\_unzip_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
