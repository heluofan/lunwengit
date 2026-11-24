import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
IMG = "/data/heluofan/picai/images"

CMDS = [
    ("one", "ls -la %s/11073" % IMG),
    ("npat", "ls %s | wc -l" % IMG),
    ("percase", "for d in %s/*/; do echo $(ls \"$d\" | wc -l); done | sort | uniq -c" % IMG),
    ("seqs", "ls %s/*/*.mha | sed 's/.*_//' | sort | uniq -c" % IMG),
    ("nocase", "find %s -maxdepth 1 -name '*.mha' | head -3" % IMG),
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
            _, o, e = cli.exec_command(c, timeout=120)
            o.channel.settimeout(120)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_imgstruct.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
