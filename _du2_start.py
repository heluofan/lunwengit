import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
OUT=/data/heluofan/_du_scan2.txt
: > $OUT
echo "######## seg_work/datasets (deep)" >> $OUT
du -sh /data/heluofan/seg_work/datasets/* 2>/dev/null | sort -hr | head -20 >> $OUT
echo "" >> $OUT
echo "######## der_data 深入" >> $OUT
du -sh /data/heluofan/der_data/raw/* /data/heluofan/der_data/tta_dataset/* 2>/dev/null | sort -hr | head -12 >> $OUT
echo "" >> $OUT
echo "######## seg_work 目录名一览" >> $OUT
ls -1 /data/heluofan/seg_work/datasets 2>/dev/null | head -30 >> $OUT
echo "" >> $OUT
echo "######## 各数据集里的样本文件名" >> $OUT
for p in /data/heluofan/seg_work/datasets /data/heluofan/der_data/raw /data/heluofan/der_data/tta_dataset /data/heluofan/brats_work/data; do
  echo "--- $p" >> $OUT
  find $p -maxdepth 3 -type f 2>/dev/null | head -6 >> $OUT
  echo "" >> $OUT
done
echo "__SCAN2_DONE__" >> $OUT
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c = ("echo %s | base64 -d > /tmp/_du2.sh && chmod +x /tmp/_du2.sh && "
         "(setsid nohup bash /tmp/_du2.sh > /dev/null 2>&1 < /dev/null &) ; sleep 2; echo LAUNCHED") % b64
    out = []
    try:
        _, o, e = cli.exec_command(c, timeout=30)
        o.channel.settimeout(30)
        out.append(o.read().decode("utf-8", "replace").strip())
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:150])
    cli.close()
    with open(r"C:\lunwen\_du2_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
