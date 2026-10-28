"""Download NSE financial-results filings (announcement timestamps + XBRL links) month by month.

Usage: python3 -I download_results_filings.py RAW_DIR START_YEAR END_YEAR
Writes RAW/results/{period}_{YYYYMM}.json for period in Quarterly, Annual. Re-running skips months already saved.
"""
import calendar, json, os, sys, time, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
HDR = {"User-Agent": UA, "Accept": "application/json",
       "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-financial-results"}


def main(raw, y0, y1):
    os.makedirs(os.path.join(raw, "results"), exist_ok=True)
    for y in range(int(y0), int(y1) + 1):
        for m in range(1, 13):
            for period in ["Quarterly", "Annual"]:
                path = os.path.join(raw, "results", f"{period}_{y}{m:02d}.json")
                if os.path.exists(path) and os.path.getsize(path) > 2:
                    continue
                last = calendar.monthrange(y, m)[1]
                url = (f"https://www.nseindia.com/api/corporates-financial-results?index=equities&period={period}"
                       f"&from_date=01-{m:02d}-{y}&to_date={last}-{m:02d}-{y}")
                for k in range(4):
                    try:
                        data = urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=90).read()
                        json.loads(data)
                        open(path, "wb").write(data)
                        break
                    except Exception:
                        time.sleep(4 * (k + 1))
                time.sleep(1.0)


def integrated(raw, y0, y1):
    """From the quarter ended March 2025 results are filed as 'Integrated Filing - Financials' (NSE/CML/2025/20).
    The endpoint is paginated; request one large page and check it against totalCount."""
    hdr = dict(HDR, Referer="https://www.nseindia.com/companies-listing/corporate-integrated-filing")
    for y in range(int(y0), int(y1) + 1):
        for m in range(1, 13):
            path = os.path.join(raw, "results", f"Integrated_{y}{m:02d}.json")
            if os.path.exists(path) and os.path.getsize(path) > 2:
                continue
            last = calendar.monthrange(y, m)[1]
            url = (f"https://www.nseindia.com/api/integrated-filing-results?index=equities&from_date=01-{m:02d}-{y}"
                   f"&to_date={last}-{m:02d}-{y}&type=Integrated%20Filing-%20Financials&size=20000")
            for k in range(4):
                try:
                    d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120).read())
                    if len(d.get("data", [])) != d.get("totalCount", -1):
                        print(f"WARNING {y}{m:02d}: got {len(d.get('data', []))} of {d.get('totalCount')}")
                    json.dump(d["data"], open(path, "w"))
                    break
                except Exception:
                    time.sleep(4 * (k + 1))
            time.sleep(1.0)


if __name__ == "__main__":
    if len(sys.argv) > 4 and sys.argv[4] == "integrated":
        integrated(*sys.argv[1:4])
    else:
        main(*sys.argv[1:4])
