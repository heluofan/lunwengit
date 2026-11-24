import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
cd /data/heluofan || exit 1
LOG=/data/heluofan/_cleanup.log
echo "=== start $(date) ===" > $LOG

M=/data/heluofan/_deleted_manifest_20261124
rm -rf $M
mkdir -p $M

echo "== 逐目录清点 ==" > $M/tree.txt
for d in seg_work picai eegfnirs der_data brats_work thyroid_tta; do
  {
    echo "--- $d ---"
    echo "size: $(du -sh "$d" 2>/dev/null | cut -f1)"
    echo "files: $(find "$d" -type f 2>/dev/null | wc -l)"
    echo "tree:"
    find "$d" -maxdepth 2 -type d 2>/dev/null | head -120
    echo ""
  } >> $M/tree.txt
done
echo "manifest tree done" >> $LOG

for d in seg_work picai eegfnirs der_data brats_work thyroid_tta; do
  find "$d" -maxdepth 3 -type f \( -name '*.csv' -o -name '*.json' -o -name '*.py' -o -name '*.sh' -o -name '*.md' -o -name '*.yaml' \) -size -1M 2>/dev/null \
  | head -400 \
  | while read -r f; do
      mkdir -p "$M/files/$(dirname "$f")"
      cp -a "$f" "$M/files/$f" 2>/dev/null
    done
done
echo "manifest small-files done" >> $LOG

tar czf $M.tar.gz -C /data/heluofan _deleted_manifest_20261124 2>/dev/null
echo "manifest tar: $(du -sh $M.tar.gz 2>/dev/null | cut -f1)  files: $(find $M/files -type f 2>/dev/null | wc -l)" >> $LOG
rm -rf $M

used_before=$(df --output=used /data | tail -1)
echo "used_before_kb=$used_before" >> $LOG

for d in seg_work picai eegfnirs der_data brats_work thyroid_tta; do
  sz=$(du -sh "$d" 2>/dev/null | cut -f1)
  echo ">>> deleting $d ($sz) at $(date +%H:%M:%S)" >> $LOG
  rm -rf "/data/heluofan/$d"
  echo "<<< done $d  remaining_exists=$([ -e "$d" ] && echo YES || echo NO)" >> $LOG
done

used_after=$(df --output=used /data | tail -1)
echo "used_after_kb=$used_after" >> $LOG
echo "freed_gb=$(( (used_before - used_after) / 1024 / 1024 ))" >> $LOG
echo "=== CLEANUP_DONE $(date) ===" >> $LOG
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    c = ("echo %s | base64 -d > /tmp/_clean.sh && chmod +x /tmp/_clean.sh && "
         "(setsid nohup bash /tmp/_clean.sh > /tmp/_clean.out 2>&1 < /dev/null &) ; sleep 3; echo LAUNCHED") % b64
    out = []
    try:
        _, o, e = cli.exec_command(c, timeout=30)
        o.channel.settimeout(30)
        out.append(o.read().decode("utf-8", "replace").strip())
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:150])
    cli.close()
    with open(r"C:\lunwen\_clean_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
