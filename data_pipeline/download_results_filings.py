"""Download NSE financial-results filings (announcement timestamps + XBRL links) month by month.

Usage: python3 -I download_results_filings.py RAW_DIR START_YEAR END_YEAR
Writes RAW/results/{period}_{YYYYMM}.json for period in Quarterly, Annual. Re-running skips months already saved.
       python3 -I download_results_filings.py RAW_DIR 2025 2026 integrated     (Integrated Filing, from Mar-2025 quarter)
       python3 -I download_results_filings.py RAW_DIR 2014 2026 boardmeetings  (board-meeting calendar)
       python3 -I download_results_filings.py RAW_DIR 2014 2026 resultupdates  (first-release time of every result)
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


def boardmeetings(raw, y0, y1):
    """Board-meeting calendar (date and purpose). The legacy results API misses some filings (audit of 5 Nov 2026:
    e.g. no June-2022-quarter filing for 52 of 198 F&O stocks); a board meeting whose purpose is financial results
    dates those events. Half-month windows, so that no single response is large."""
    hdr = dict(HDR, Referer="https://www.nseindia.com/companies-listing/corporate-filings-board-meetings")
    os.makedirs(os.path.join(raw, "boardmeetings"), exist_ok=True)
    for y in range(int(y0), int(y1) + 1):
        for m in range(1, 13):
            last = calendar.monthrange(y, m)[1]
            for a, b, tag in [(1, 15, "a"), (16, last, "b")]:
                path = os.path.join(raw, "boardmeetings", f"bm_{y}{m:02d}{tag}.json")
                if os.path.exists(path) and os.path.getsize(path) > 1:
                    continue
                url = (f"https://www.nseindia.com/api/corporate-board-meetings?index=equities"
                       f"&from_date={a:02d}-{m:02d}-{y}&to_date={b:02d}-{m:02d}-{y}")
                for k in range(4):
                    try:
                        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120).read())
                        d = d if isinstance(d, list) else d.get("data", [])
                        json.dump(d, open(path, "w"))
                        break
                    except Exception:
                        time.sleep(4 * (k + 1))
                time.sleep(0.7)


def resultupdates(raw, y0, y1):
    """Corporate announcements in the category 'Financial Result Updates': the exchange's dissemination time of each
    results filing (the first public release). Audit of 5 Nov 2026: the results-filings feed above often carries a later
    re-filing time (in 2017-2018 most timestamps are days or weeks after the board meeting), while this category carries
    the release on the meeting day. Four-day windows keep each response small."""
    import datetime as dt
    hdr = dict(HDR, Referer="https://www.nseindia.com/companies-listing/corporate-filings-announcements")
    os.makedirs(os.path.join(raw, "resultupdates"), exist_ok=True)
    from concurrent.futures import ThreadPoolExecutor
    d, end = dt.date(int(y0), 1, 1), min(dt.date(int(y1), 12, 31), dt.date.today())
    windows = []
    while d <= end:
        windows.append((d, min(d + dt.timedelta(days=3), end)))
        d = windows[-1][1] + dt.timedelta(days=1)

    def fetch(w):
        d, e = w
        path = os.path.join(raw, "resultupdates", f"ru_{d:%Y%m%d}.json")
        if os.path.exists(path) and os.path.getsize(path) > 1:
            return
        url = (f"https://www.nseindia.com/api/corporate-announcements?index=equities&from_date={d:%d-%m-%Y}"
               f"&to_date={e:%d-%m-%Y}&subject=Financial%20Result%20Updates")
        for k in range(5):
            try:
                r = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120).read())
                r = r if isinstance(r, list) else r.get("data", [])
                json.dump(r, open(path, "w"))
                return
            except Exception:
                time.sleep(4 * (k + 1))
        print("FAILED", d)

    with ThreadPoolExecutor(4) as ex:
        list(ex.map(fetch, windows))

if __name__ == "__main__":
    if len(sys.argv) > 4 and sys.argv[4] == "resultupdates":
        resultupdates(*sys.argv[1:4])
        sys.exit()
    if len(sys.argv) > 4 and sys.argv[4] == "boardmeetings":
        boardmeetings(*sys.argv[1:4])
        sys.exit()
    if len(sys.argv) > 4 and sys.argv[4] == "integrated":
        integrated(*sys.argv[1:4])
    else:
        main(*sys.argv[1:4])
