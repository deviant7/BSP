"""Download NSE Securities Lending and Borrowing (SLBS) daily bhavcopies.

Source: https://nsearchives.nseindia.com/archives/slbs/bhavcopy/SLBM_BC_DDMMYYYY.DAT (no cookies needed; send a browser
User-Agent and a Referer). One file per trading day; days come from the MWPL panel calendar.
File layout (comma-separated, padded, no header): company name, symbol, series (tenure code), expiry date (DD-MON-YYYY),
flag, previous close fee, open, high, low, close (lending fee in Rs per share), blank, quantity (shares), value (Rs),
upper band, lower band, trade date, number of trades.

Usage: python3 -I data_pipeline/download_slb.py data/raw/slb [threads]
"""
import os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
URL = "https://nsearchives.nseindia.com/archives/slbs/bhavcopy/SLBM_BC_{}.DAT"


def get(day, out):
    fn = os.path.join(out, day.strftime("%Y%m%d") + ".dat")
    if os.path.exists(fn) and os.path.getsize(fn) > 0:
        return day, "have"
    url = URL.format(day.strftime("%d%m%Y"))
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.nseindia.com/all-reports"})
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
            if data[:15].lower().startswith(b"<!doctype") or data[:5].lower() == b"<html":
                open(fn + ".missing", "w").close()
                return day, "missing"
            open(fn, "wb").write(data)
            return day, "ok"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                open(fn + ".missing", "w").close()
                return day, "404"
            time.sleep(2 ** k)
        except Exception:
            time.sleep(2 ** k)
    return day, "fail"


def main(out, threads=4):
    os.makedirs(out, exist_ok=True)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    d = pd.read_csv(os.path.join(root, "data", "processed", "mwpl_oi_panel.csv.gz"), usecols=["date"])["date"].unique()
    days = sorted(pd.to_datetime(d))
    days = [x for x in days if x >= pd.Timestamp("2015-01-01")]
    res = {}
    with ThreadPoolExecutor(threads) as ex:
        for day, st in ex.map(lambda x: get(x, out), days):
            res[st] = res.get(st, 0) + 1
    print(res)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4)
