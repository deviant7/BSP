"""Download NSE daily all-index closing files and keep the Nifty 50 row (close, P/E, P/B, trailing dividend yield).
Usage: python3 -I download_index_close.py OUT_CSV START END"""
import csv, datetime as dt, io, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}


def get(d):
    url = f"https://nsearchives.nseindia.com/content/indices/ind_close_all_{d:%d%m%Y}.csv"
    for k in range(3):
        try:
            txt = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8", "ignore")
            for row in csv.reader(io.StringIO(txt)):
                if row and row[0].strip().lower() in ("nifty 50", "cnx nifty", "s&p cnx nifty"):
                    return [d.isoformat()] + row
            return None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 * (k + 1))
        except Exception:
            time.sleep(2 * (k + 1))
    return None


def main(out, start, end):
    days, d = [], dt.date.fromisoformat(start)
    while d <= dt.date.fromisoformat(end):
        if d.weekday() < 5:
            days.append(d)
        d += dt.timedelta(days=1)
    with ThreadPoolExecutor(max_workers=4) as ex:
        rows = [r for r in ex.map(get, days) if r]
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "index", "index_date", "open", "high", "low", "close", "chg", "chg_pct", "volume", "turnover_cr", "pe", "pb", "div_yield"])
        w.writerows(rows)
    print(len(rows), "rows")


if __name__ == "__main__":
    main(*sys.argv[1:4])
