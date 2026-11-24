import os, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]
PY = "/data/heluofan/envs/ms/bin/python"

CMDS = [
    ("pkgs", "%s -m pip list 2>/dev/null | grep -Ei '^(medpy|SimpleITK|batchgenerators|scikit-|scipy|nibabel|pandas|numpy|torch|fbm|connected-components|dicom2nifti|blosc|tqdm)' " % PY),
    ("disk", "df -h /data | tail -1"),
    ("dl", "tail -2 /data/heluofan/picai/dl_v2.log"),
    ("pip", "%s -m pip config list 2>/dev/null; echo '---'; %s -m pip download medpy -d /tmp/_t --no-deps -q 2>&1 | tail -3" % (PY, PY)),
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
            _, o, e = cli.exec_command(c, timeout=180)
            o.channel.settimeout(180)
            out.append(o.read().decode("utf-8", "replace").rstrip())
        except Exception as ex:
            out.append("[EXC] " + repr(ex)[:150])
        out.append("")
    cli.close()
    with open(r"C:\lunwen\_pkgs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("DONE")

main()
