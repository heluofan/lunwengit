#!/usr/bin/env python3
# PI-CAI 五个官方影像包多线程分段下载（断点续传 + md5 校验）
import os, time, hashlib, threading, urllib.request, ssl

BASE = "https://zenodo.org/api/records/6624726/files"
DEST = "/data/heluofan/picai/downloads"
CHUNK = 64 * 1024 * 1024
WORKERS = 32
RETRY = 8

FILES = [
    ("picai_public_images_fold0.zip", 5368893021, "b0cdd8f5fb7733ca585dca3541586a34"),
    ("picai_public_images_fold1.zip", 5164062415, "d7c8cd0efc0e7f264df8d5acf860662f"),
    ("picai_public_images_fold2.zip", 5270275720, "5ac0caf27cfe94dfc04bb408a971b351"),
    ("picai_public_images_fold3.zip", 5502916242, "6602bce3d0882d7b9c2153d880c97e96"),
    ("picai_public_images_fold4.zip", 5562839222, "8941720d8a8ee66571691cfb10dbee66"),
]

TOTAL = sum(f[1] for f in FILES)
lock = threading.Lock()
done = [0]
t_start = time.time()
last = [0, time.time()]
STOP = [False]

ctx = ssl.create_default_context()
try:
    urllib.request.urlopen(BASE + "/picai_public_images_fold0.zip/content",
                           timeout=20, context=ctx).close()
except Exception as e:
    print("TLS check warn: %r" % (e,), flush=True)
    ctx = ssl._create_unverified_context()
    print("-> fallback to unverified TLS", flush=True)


def fetch(args):
    name, s, e, p, exp, total = args
    url = "%s/%s/content" % (BASE, name)
    for att in range(RETRY):
        tmp = p + ".tmp"
        try:
            req = urllib.request.Request(url, headers={
                "Range": "bytes=%d-%d" % (s, e),
                "User-Agent": "picai-dl/1.0",
            })
            got = 0
            with urllib.request.urlopen(req, timeout=180, context=ctx) as r, open(tmp, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
                    got += len(b)
            if got != exp:
                raise IOError("short %d/%d" % (got, exp))
            os.replace(tmp, p)
            with lock:
                done[0] += exp
            return True
        except Exception as ex:
            if att == RETRY - 1:
                print("FAIL %s %d-%d : %r" % (name, s, e, ex), flush=True)
            time.sleep(min(2 ** att, 20))
    return False


def monitor():
    while not STOP[0]:
        time.sleep(15)
        with lock:
            d = done[0]
        now = time.time()
        inst = (d - last[0]) / max(now - last[1], 1e-6) / 1048576
        avg = d / max(now - t_start, 1e-6) / 1048576
        last[0], last[1] = d, now
        eta = (TOTAL - d) / max(avg * 1048576, 1.0) / 60
        print("[%5.0fs] %6.2f/%6.2f GB %5.1f%%  inst=%5.2f MB/s avg=%5.2f MB/s ETA=%4.0f min"
              % (now - t_start, d / 2**30, TOTAL / 2**30, 100.0 * d / TOTAL, inst, avg, eta),
              flush=True)


def main():
    os.makedirs(DEST, exist_ok=True)
    print("TOTAL=%.2f GB  CHUNK=%dMB  WORKERS=%d" % (TOTAL / 2**30, CHUNK >> 20, WORKERS), flush=True)
    tasks, skipped = [], 0
    for name, total, md5 in FILES:
        n = (total + CHUNK - 1) // CHUNK
        for i in range(n):
            s = i * CHUNK
            e = min(s + CHUNK, total) - 1
            p = os.path.join(DEST, "%s.p%05d" % (name, i))
            exp = e - s + 1
            if os.path.exists(p) and os.path.getsize(p) == exp:
                done[0] += exp
                skipped += 1
            else:
                tasks.append((name, s, e, p, exp, total))
    last[0] = done[0]
    print("resume: %d parts done, %d to fetch" % (skipped, len(tasks)), flush=True)

    th = threading.Thread(target=monitor, daemon=True)
    th.start()

    import concurrent.futures as cf
    ok = 0
    with cf.ThreadPoolExecutor(WORKERS) as ex:
        for r in ex.map(fetch, tasks):
            ok += 1 if r else 0
    STOP[0] = True
    print("DOWNLOAD DONE ok=%d/%d elapsed=%.0f min" % (ok, len(tasks), (time.time() - t_start) / 60), flush=True)

    # 拼接 + md5
    for name, total, md5 in FILES:
        outp = os.path.join(DEST, name)
        if os.path.exists(outp) and os.path.getsize(outp) == total:
            print("ASSEMBLE skip %s (exists)" % name, flush=True)
            continue
        n = (total + CHUNK - 1) // CHUNK
        h = hashlib.md5()
        with open(outp, "wb") as fo:
            for i in range(n):
                p = os.path.join(DEST, "%s.p%05d" % (name, i))
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


main()
