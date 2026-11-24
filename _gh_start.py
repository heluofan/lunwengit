import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
RUNDIR = "/data/heluofan/picai"

SH = r'''#!/bin/bash
cd /data/heluofan/picai || exit 1
mkdir -p repos
for r in picai_labels picai_baseline picai_eval Report-Guided-Annotation; do
  if [ -s "repos/$r/.DONE" ]; then echo "SKIP $r"; continue; fi
  ok=1
  for br in main master; do
    if curl -fsSL --max-time 3600 -o "repos/$r.zip" "https://codeload.github.com/DIAGNijmegen/$r/zip/refs/heads/$br"; then
      ok=0; echo "GET $r ($br) bytes=$(stat -c%s repos/$r.zip)"; break
    fi
  done
  if [ $ok -eq 0 ]; then
    rm -rf "repos/$r"; mkdir -p "repos/$r"
    python3 -m zipfile -e "repos/$r.zip" "repos/$r/" && touch "repos/$r/.DONE" && echo "EXTRACT $r ok"
  else
    echo "FAIL $r"
  fi
done
echo ALLDONE
'''

log = []

def main():
    b64 = base64.b64encode(SH.encode()).decode()
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)

    cmds = [
        "echo %s | base64 -d > %s/repos_dl.sh && chmod +x %s/repos_dl.sh && echo WROTE" % (b64, RUNDIR, RUNDIR),
        "cd %s && (setsid bash repos_dl.sh >> repos_dl.log 2>&1 < /dev/null &) ; sleep 2; echo LAUNCHED" % RUNDIR,
    ]
    for c in cmds:
        try:
            _, o, e = cli.exec_command(c, timeout=25)
            o.channel.settimeout(25)
            log.append("$ " + c[:80])
            log.append(o.read().decode("utf-8", "replace").strip())
        except Exception as ex:
            log.append("[EXC] " + repr(ex)[:200])
    cli.close()
    with open(r"C:\lunwen\_gh_start.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print("DONE")

main()
