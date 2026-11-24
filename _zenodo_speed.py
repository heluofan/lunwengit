import os, base64, paramiko

HOST, PORT, USER = "112.27.96.69", 11079, "heluofan"
PW = os.environ["PICAI_PW"]

REMOTE = r'''
import time, urllib.request, concurrent.futures, sys
U = "https://zenodo.org/api/records/6624726/files/picai_public_images_fold0.zip/content"
CH = 8 * 1024 * 1024

def get(rng):
    req = urllib.request.Request(U, headers={"Range": "bytes=%d-%d" % rng})
    t = time.time(); n = 0; code = 0
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            code = r.getcode()
            while True:
                b = r.read(65536)
                if not b:
                    break
                n += len(b)
    except Exception as e:
        return (rng[0], "ERR " + repr(e)[:120], 0, time.time() - t)
    return (rng[0], code, n, time.time() - t)

print("== single 8MB ==")
r = get((0, CH - 1))
print("start=%s code=%s bytes=%d time=%.2fs speed=%.2fMB/s" % (r[0], r[1], r[2], r[3], r[2] / 1048576 / max(r[3], 1e-6)))

print("== 8 parallel x 8MB ==")
t0 = time.time()
with concurrent.futures.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(get, [(i * CH, i * CH + CH - 1) for i in range(8)]))
wall = time.time() - t0
tot = sum(x[2] for x in res if isinstance(x[2], int))
print("wall=%.2fs total=%.1fMB aggregate=%.2fMB/s" % (wall, tot / 1048576, (tot / 1048576) / max(wall, 1e-6)))
for x in res:
    print("  start=%s code=%s bytes=%s time=%.1fs" % (x[0], x[1], x[2], x[3]))
'''

def main():
    b64 = base64.b64encode(REMOTE.encode()).decode()
    cmd = "echo %s | base64 -d | python3 - 2>&1" % b64
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(HOST, port=PORT, username=USER, password=PW, timeout=30,
                look_for_keys=False, allow_agent=False)
    _, o, e = cli.exec_command(cmd, timeout=300)
    out = o.read().decode("utf-8", "replace")
    err = e.read().decode("utf-8", "replace")
    cli.close()
    with open(r"C:\lunwen\_zenodo_speed.txt", "w", encoding="utf-8") as f:
        f.write(out)
        if err.strip():
            f.write("\n[stderr]\n" + err)
    print("DONE")

main()
