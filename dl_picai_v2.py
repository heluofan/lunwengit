#!/usr/bin/env python3
# PI-CAI 五个官方影像包下载 v2：低并发 + .tmp 断点续传 + 目录级实时进度 + md5 校验
import os, time, hashlib, threading, urllib.request, ssl

BASE = "https://zenodo.org/api/records/6624726/files"
DEST = "/data/heluofan/picai/downloads"
CHUNK = 64 * 1024 * 1024
WORKERS = int(os.environ.get("PICAI_WORKERS", "10"))
RETRY = 10

FILES = [
    ("picai_public_images_fold0.zip", 5368893021, "b0cdd8f5fb7733ca585dca3541586a34"),
    ("picai_public_images_fold1.zip", 5164062415, "d7c8cd0efc0e7f264df8d5acf860662f"),
    ("picai_public_images_fold2.zip", 5270275720, "5ac0caf27cfe94dfc04bb408a971b351"),
    ("picai_public_images_fold3.zip", 5502916242, "6602bce3d0882d7b9c2153d880c97e96"),
    ("picai_public_images_fold4.zip", 5562839222, "8941720d8a8ee66571691cfb10dbee66"),
]
TOTAL = sum(f[1] for f in FILES)
STOP = [False]
lock = threading.Lock()
fails = []

ctx = ssl.create_default_context()


def disk_bytes():
    n = 0
    try:
        for ent in os.scandir(DEST):
            try:
                if ent.is_file() and (".p0" in ent.name):
                    n += ent.stat().st_size
            except OSError:
                pass
    except OSError:
        pass
    return n


def fetch(args):
    name, s, e, p, exp, total = args
    url = "%s/%s/content" % (BASE, name)
    tmp = p + ".tmp"
    for att in range(RETRY):
        try:
            cur = os.path.getsize(tmp) if os.path.exists(tmp) else 0
            if cur == exp:
                os.replace(tmp, p)
                return True
            if cur > exp:
                os.remove(tmp)
                cur = 0
            req = urllib.request.Request(url, headers={
                "Range": "bytes=%d-%d" % (s + cur, e),
                "User-Agent": "picai-dl/2.0",
            })
            with urllib.request.urlopen(req, timeout=180, context=ctx) as r, open(tmp, "ab") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
            if os.path.getsize(tmp) != exp:
                raise IOError("short %d/%d" % (os.path.getsize(tmp), exp))
            os.replace(tmp, p)
            return True
        except Exception as ex:
            if att == RETRY - 1:
                with lock:
                    fails.append((name, s, repr(ex)[:120]))
            time.sleep(min(2 ** att, 30))
    return False


def monitor():
    t0 = time.time()
    prev, pt = 0, t0
    while not STOP[0]:
        time.sleep(15)
        d = disk_bytes()
        now = time.time()
        inst = (d - prev) / max(now - pt, 1e-6) / 1048576
        prev, pt = d, now
        avg = d / max(now - t0, 1e-6) / 1048576
        eta = (TOTAL - d) / max(avg * 1048576, 1.0) / 60 if avg > 0 else -1
        print("[%5.0fs] %6.2f/%.2f GB %5.1f%%  inst=%.2f avg=%.2f MB/s ETA=%.0f min"
              % (now - t0, d / 2**30, TOTAL / 2**30, 100.0 * d / TOTAL, inst, avg, eta), flush=True)


def main():
    os.makedirs(DEST, exist_ok=True)
    print("v2 TOTAL=%.2fGB CHUNK=%dMB WORKERS=%d" % (TOTAL / 2**30, CHUNK >> 20, WORKERS), flush=True)
    tasks, skipped = [], 0
    for name, total, md5 in FILES:
        n = (total + CHUNK - 1) // CHUNK
        for i in range(n):
            s = i * CHUNK
            e = min(s + CHUNK, total) - 1
            p = os.path.join(DEST, "%s.p%05d" % (name, i))
            if os.path.exists(p) and os.path.getsize(p) == e - s + 1:
                skipped += 1
            else:
                tasks.append((name, s, e, p, e - s + 1, total))
    print("resume: %d parts done, %d to fetch, on-disk=%.2fGB"
          % (skipped, len(tasks), disk_bytes() / 2**30), flush=True)

    threading.Thread(target=monitor, daemon=True).start()

    import concurrent.futures as cf
    ok = 0
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for r in ex.map(fetch, tasks):
            ok += 1 if r else 0
    STOP[0] = True
    print("DOWNLOAD DONE ok=%d/%d fails=%d" % (ok, len(tasks), len(fails)), flush=True)
    for f in fails[:10]:
        print("  FAIL", f, flush=True)

    for name, total, md5 in FILES:
        outp = os.path.join(DEST, name)
        if os.path.exists(outp) and os.path.getsize(outp) == total:
            print("ASSEMBLE skip %s (exists %d)" % (name, total), flush=True)
            continue
        n = (total + CHUNK - 1) // CHUNK
        parts = [os.path.join(DEST, "%s.p%05d" % (name, i)) for i in range(n)]
        if not all(os.path.exists(p) for p in parts):
            print("ASSEMBLE ABORT %s (missing parts)" % name, flush=True)
            continue
        h = hashlib.md5()
        with open(outp, "wb") as fo:
            for p in parts:
                with open(p, "rb") as fi:
                    while True:
                        b = fi.read(1 << 22)
                        if not b:
                            break
                        fo.write(b)
                        h.update(b)
        got = h.hexdigest()
        print("ASSEMBLE %s size=%d md5=%s expect=%s %s"
              % (name, os.path.getsize(outp), got, md5, "OK" if got == md5 else "MISMATCH"), flush=True)
    print("ALLDONE", flush=True)


main()
