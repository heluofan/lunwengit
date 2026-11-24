import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
me=$$
P1="_cle""an.sh"
P2="rm -rf /data/heluofan/"
echo "=== 立即停止 ==="
for p in $(pgrep -f "$P1"); do [ "$p" = "$me" ] || { kill -9 $p 2>/dev/null; echo "killed $p ($P1)"; }; done
for p in $(pgrep -f "$P2"); do [ "$p" = "$me" ] || { kill -9 $p 2>/dev/null; echo "killed $p (rm)"; }; done
sleep 1
echo "=== 剩余进程 ==="
ps -eo pid,args | grep -E "$P1|rm -rf /data/heluofan" | grep -v grep | head -5
echo "procs=$(pgrep -f "$P1" | wc -l)"
echo "=== 清理日志 ==="
cat /data/heluofan/_cleanup.log 2>/dev/null
echo "=== 目录现状 ==="
for d in seg_work picai eegfnirs der_data brats_work thyroid_tta; do
  if [ -e "/data/heluofan/$d" ]; then printf '%-14s %s\n' "$d" "$(du -sh /data/heluofan/$d 2>/dev/null | cut -f1)"; else printf '%-14s %s\n' "$d" "GONE"; fi
done
echo "=== manifest ==="
ls -lh /data/heluofan/_deleted_manifest_20261124.tar.gz 2>/dev/null || echo "no manifest"
echo "=== disk ==="
df -h /data | tail -1
echo ABORT_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    out = []
    try:
        _, o, e = cli.exec_command("echo %s | base64 -d > /tmp/_abort.sh && bash /tmp/_abort.sh 2>&1" % b64, timeout=100)
        o.channel.settimeout(100)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_abort.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
