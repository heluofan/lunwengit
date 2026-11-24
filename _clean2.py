import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
LOG=/data/heluofan/_cleanup2.log
echo "=== start $(date) ===" > $LOG

T1=/data/heluofan/seg_work
T2=/data/heluofan/picai
T3=/data/heluofan/eegfnirs
T4=/data/heluofan/der_data
T5=/data/heluofan/brats_work
T6=/data/heluofan/thyroid_tta

echo "== 删除前清单 ==" >> $LOG
for t in $T1 $T2 $T3 $T4 $T5 $T6; do
  if [ -e "$t" ]; then printf '%-40s %s\n' "$t" "$(du -sh "$t" 2>/dev/null | cut -f1)" >> $LOG
  else printf '%-40s %s\n' "$t" "NOT_EXIST" >> $LOG; fi
done
echo "" >> $LOG

# 仅备份 seg_work 的小体积结果文件（csv/md/json，<2M）
BK=/data/heluofan/_seg_metrics_20261124.tar.gz
if [ -d "$T1" ]; then
  cd "$T1" || exit 1
  find . -maxdepth 3 -type f \( -name '*.csv' -o -name '*.md' -o -name '*.json' \) -size -2M 2>/dev/null | head -300 > /tmp/_bklist.txt
  echo "backup candidates: $(wc -l < /tmp/_bklist.txt)" >> $LOG
  if [ -s /tmp/_bklist.txt ]; then
    tar czf "$BK" -T /tmp/_bklist.txt 2>/dev/null
    echo "backup: $(du -sh "$BK" 2>/dev/null | cut -f1)" >> $LOG
  fi
  cd /data/heluofan || exit 1
fi

before=$(df --output=used /data | tail -1)
echo "used_before_kb=$before" >> $LOG

for t in $T1 $T2 $T3 $T4 $T5 $T6; do
  [ -e "$t" ] || { echo "skip (absent) $t" >> $LOG; continue; }
  echo ">>> rm -rf $t" >> $LOG
  rm -rf "$t"
  echo "<<< done, exists=$([ -e "$t" ] && echo YES || echo NO)" >> $LOG
done

after=$(df --output=used /data | tail -1)
echo "used_after_kb=$after" >> $LOG
echo "freed_gb=$(( (before - after) / 1024 / 1024 ))" >> $LOG
echo "== 剩余 ==" >> $LOG
du -sh /data/heluofan 2>/dev/null >> $LOG
df -h /data | tail -1 >> $LOG
echo "=== DONE $(date) ===" >> $LOG
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c = ("echo %s | base64 -d > /tmp/_clean2.sh && chmod +x /tmp/_clean2.sh && "
         "(setsid nohup bash /tmp/_clean2.sh > /tmp/_clean2.out 2>&1 < /dev/null &) ; sleep 3; "
         "echo LAUNCHED; head -12 /data/heluofan/_cleanup2.log") % b64
    out = []
    try:
        _, o, e = cli.exec_command(c, timeout=40)
        o.channel.settimeout(40)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:200])
    cli.close()
    with open(r"C:\lunwen\_clean2_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
