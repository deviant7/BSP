"""Download (1) monthly Indian interest-rate series from FRED (OECD MEI) and (2) NSE corporate actions (dividends,
splits, bonuses) month by month from the NSE corporate-actions API.

Usage: python3 -I download_rates_corpactions.py RAW_DIR START_YEAR END_YEAR
"""
import calendar, json, os, sys, time, urllib.request, http.cookiejar

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
FRED = {"INDIR3TIB01STM": "India 3-month interbank rate (OECD MEI, monthly, % p.a.)",
        "IRSTCI01INM156N": "India call money / interbank immediate rate (OECD MEI, monthly, % p.a.)"}


def main(raw, y0, y1):
    os.makedirs(os.path.join(raw, "rates"), exist_ok=True)
    os.makedirs(os.path.join(raw, "corpactions"), exist_ok=True)
    for sid in FRED:  # FRED sometimes drops Python connections; fall back to curl
        path = os.path.join(raw, "rates", f"{sid}.csv")
        if os.path.exists(path) and os.path.getsize(path) > 100:
            continue
        os.system(f'curl -sS -L --max-time 60 -o "{path}" "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"')
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    hdr = {"User-Agent": UA, "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-actions",
           "Accept": "application/json"}
    try:
        op.open(urllib.request.Request("https://www.nseindia.com/", headers={"User-Agent": UA}), timeout=30)
    except Exception:
        pass  # home page may refuse; the API has worked without its cookies
    for y in range(int(y0), int(y1) + 1):
        for m in range(1, 13):
            path = os.path.join(raw, "corpactions", f"ca_{y}{m:02d}.json")
            if os.path.exists(path) and os.path.getsize(path) > 2:
                continue
            last = calendar.monthrange(y, m)[1]
            url = (f"https://www.nseindia.com/api/corporates-corporateActions?index=equities"
                   f"&from_date=01-{m:02d}-{y}&to_date={last}-{m:02d}-{y}")
            for k in range(4):
                try:
                    data = op.open(urllib.request.Request(url, headers=hdr), timeout=60).read()
                    json.loads(data)
                    open(path, "wb").write(data)
                    break
                except Exception:
                    time.sleep(3 * (k + 1))
            time.sleep(1.0)


if __name__ == "__main__":
    main(*sys.argv[1:4])
