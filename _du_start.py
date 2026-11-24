import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
OUT=/data/heluofan/_du_scan.txt
: > $OUT
for d in seg_work models image der_data eegfnirs brats_work thyroid_tta qwen3-embed venvs wheels; do
  echo "######## $d" >> $OUT
  du -sh /data/heluofan/$d/* 2>/dev/null | sort -hr | head -14 >> $OUT
  echo "" >> $OUT
done
echo "__SCAN_DONE__" >> $OUT
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c = ("echo %s | base64 -d > /tmp/_du.sh && chmod +x /tmp/_du.sh && "
         "(setsid nohup bash /tmp/_du.sh > /dev/null 2>&1 < /dev/null &) ; sleep 2; echo LAUNCHED") % b64
    out = []
    try:
        _, o, e = cli.exec_command(c, timeout=30)
        o.channel.settimeout(30)
        out.append(o.read().decode("utf-8", "replace").strip())
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:150])
    cli.close()
    with open(r"C:\lunwen\_du_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
