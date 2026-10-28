"""Download NSE daily MWPL / open-interest files (combineoi) and securities-in-ban lists (fo_secban).

These are treatment-side files only (MWPL, open interest, ban status). No price/mispricing outcome is downloaded here.
Usage: python3 -I download_nse_mwpl.py RAW_DIR START(YYYY-MM-DD) END(YYYY-MM-DD)
Weekends are skipped; holidays return 404 and are logged. Re-running skips files already present.
"""
import datetime as dt, os, sys, threading, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
BASE = "https://nsearchives.nseindia.com/archives/"
KINDS = {"combineoi": "nsccl/mwpl/combineoi_{d}.zip", "secban": "fo/sec_ban/fo_secban_{d}.csv"}


def fetch(url, path, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
            return 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404
            time.sleep(2 ** (k + 1))
        except Exception:
            time.sleep(2 ** (k + 1))
    return -1


def main(raw, start, end, workers=6):
    for kind in KINDS:
        os.makedirs(os.path.join(raw, kind), exist_ok=True)
    log = open(os.path.join(raw, "download_log.tsv"), "a")
    lock = threading.Lock()
    jobs = []
    d, end = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    while d <= end:
        if d.weekday() < 5:
            ds = d.strftime("%d%m%Y")
            for kind, pat in KINDS.items():
                rel = pat.format(d=ds)
                path = os.path.join(raw, kind, os.path.basename(rel))
                if not (os.path.exists(path) and os.path.getsize(path) > 0):
                    jobs.append((d, kind, rel, path))
        d += dt.timedelta(days=1)

    def run(job):
        d, kind, rel, path = job
        code = fetch(BASE + rel, path)
        with lock:
            log.write(f"{d}\t{kind}\t{code}\n"); log.flush()
        time.sleep(0.2)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(run, jobs))
    log.close()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
