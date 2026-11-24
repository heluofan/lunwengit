import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

SH = r'''#!/bin/bash
PAT="nnUNet_plan""_and_preprocess"
me=$$
echo "=== 停止前进程 ==="
ps -eo pid,args | grep -v grep | grep "$PAT" | head -5
n=0
for p in $(pgrep -f "$PAT"); do
  [ "$p" = "$me" ] && continue
  kill -TERM $p 2>/dev/null && n=$((n+1))
done
echo "TERM sent to $n"
sleep 4
for p in $(pgrep -f "$PAT"); do
  [ "$p" = "$me" ] && continue
  kill -KILL $p 2>/dev/null
done
sleep 1
echo "=== 停止后剩余 ==="
echo "procs=$(pgrep -f "$PAT" | wc -l)"
echo "=== 空间占用 ==="
du -sh /data/heluofan/picai/downloads /data/heluofan/picai/images /data/heluofan/picai/workdir 2>/dev/null
du -sh /data/heluofan/picai 2>/dev/null
df -h /data | tail -1
echo STOP_DONE
'''

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    cmd = "echo %s | base64 -d > /tmp/_stop.sh && bash /tmp/_stop.sh 2>&1" % b64
    out = []
    try:
        _, o, e = cli.exec_command(cmd, timeout=90)
        o.channel.settimeout(90)
        out.append(o.read().decode("utf-8", "replace"))
    except Exception as ex:
        out.append("[EXC] " + repr(ex)[:300])
    cli.close()
    with open(r"C:\lunwen\_stop.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
