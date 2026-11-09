"""Half-yearly average market capitalisation of every listed company (AMFI lists for SEBI's large/mid/small-cap
categorisation), July-December 2017 to January-June 2026.

Usage: python3 -I build_amfi_mcap.py RAW_DIR OUT_DIR
Downloads the AMFI PDFs into RAW/amfi_mcap/ (skips files present), parses them with pdftotext, writes
OUT/amfi_mcap.csv.gz: period_end, isin, nse_symbol (as printed, may be blank), name, avg_mcap_cr (average of all
exchanges, Rs crore), rank, category; and OUT/amfi_mcap_report.txt.
Notes: one row per company and half-year; the average-of-exchanges figure is used (it is the last number on each row,
which avoids ambiguity about which exchange column a number belongs to); BSE-only companies are included.
"""
import os, re, subprocess, sys, time, urllib.parse, urllib.request
import pandas as pd

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
B = "https://www.amfiindia.com/Themes/Theme1/downloads/"
FILES = {
    "2017-12-31": B + "Avg. Market Capitalization of listed companies during -Jul-Dec 2017.pdf",
    "2018-06-30": B + "Avg. Market Capitalization of listed companies during -Jan-June 2018.pdf",
    "2018-12-31": B + "Avg. Market Capitalization of listed companies during Jul-Dec 2018.pdf",
    "2019-06-30": B + "Avg. Market Capitalization of listed companies during -Jan-June 2019.pdf",
    "2019-12-31": B + "Avg. Market Capitalization of listed companies during Jul-Dec 2019.pdf",
    "2020-06-30": B + "Average Market Capitalization of Listed Companies during Jan - Jun 2020_Final.pdf",
    "2020-12-31": B + "Average Market Capitalization of Listed Companies during Jul - Dec_2020_Final.pdf",
    "2021-06-30": B + "Average Market Capitalization of List Companies during Jan-June 2021.pdf",
    "2021-12-31": B + "Average Market Capitalisation of Listed Companies during Jul - Dec 2021.pdf",
    "2022-06-30": B + "AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended30June2022.pdf",
    "2022-12-31": B + "AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended31Dec2022.pdf",
    "2023-06-30": B + "AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended30Jun2023.pdf",
    "2023-12-31": B + "AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended31Dec2023.pdf",
    "2024-06-30": B + "AverageMarketCapitalization30Jun2024.pdf",
    "2024-12-31": B + "AverageMarketCapitalizationoflistedcompaniesduringthesixmonthsended31Dec2024.pdf",
    "2025-06-30": B + "AverageMarketCapitalization30Jun2025.pdf",
    "2025-12-31": B + "AverageMarketCapitalization31Dec2025.pdf",
    "2026-06-30": "https://portal.amfiindia.com/spages/AverageMarketCapitalization30Jun2026.pdf",
}
ISIN = re.compile(r"(IN[EF][A-Z0-9]{4}[0-9]{2}[A-Z0-9]{2}[0-9])(?![A-Z0-9])")   # may be glued to the name
NUM = re.compile(r"^-?[0-9][0-9,]*\.?[0-9]*$")


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 100000:
        return True
    p = urllib.parse.urlsplit(url)
    u = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(urllib.parse.unquote(p.path)), "", ""))
    for k in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120).read()
            if data[:4] == b"%PDF":
                open(path, "wb").write(data)
                return True
        except Exception:
            time.sleep(4 * (k + 1))
    return False


def parse(path, period):
    """A record starts on a line that begins with its rank (Sr. No.) and continues on the following lines until the next
    rank line; some files wrap the ISIN and the numbers onto a continuation line."""
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    recs, cur = [], None
    for ln in txt.splitlines():
        if re.search(r"Average Market Cap|Sr\.? ?No|Page \d|Categorizat|Circular|Exchanges|Total Market", ln, re.I) and not ISIN.search(ln):
            continue
        m = re.match(r"\s*([0-9]{1,5})\s{2,}(\S.*)$", ln) or re.match(r"\s*([0-9]{1,5})\s+([A-Za-z].*)$", ln)
        if m and not NUM.match(m.group(2).split()[0]):
            if cur:
                recs.append(cur)
            cur = [int(m.group(1)), m.group(2)]
        elif cur and ln.strip():
            cur[1] += " " + ln.strip()
    if cur:
        recs.append(cur)
    rows = []
    for rank, body in recs:
        m = ISIN.search(body)
        if not m:
            continue
        name, tail = body[:m.start()].strip(), body[m.end():]
        cat = None
        for c in ("Large Cap", "Mid Cap", "Small Cap"):
            if c in tail:
                cat = c
                tail = tail[:tail.index(c)]
        toks = tail.split()
        nums = [t for t in toks if NUM.match(t) and ("," in t or "." in t)]
        if not nums:
            continue
        syms = [t for t in toks if not NUM.match(t)]
        rows.append((period, m.group(1), name, rank, float(nums[-1].replace(",", "")), cat, " ".join(syms)))
    return pd.DataFrame(rows, columns=["period_end", "isin", "name", "rank", "avg_mcap_cr", "category", "symbols"])


def main(raw, out):
    d = os.path.join(raw, "amfi_mcap"); os.makedirs(d, exist_ok=True)
    rep, frames = [], []
    for per, url in FILES.items():
        path = os.path.join(d, f"amfi_mcap_{per}.pdf")
        if not fetch(url, path):
            rep.append(f"{per}: DOWNLOAD FAILED ({url})"); continue
        df = parse(path, per)
        frames.append(df)
        rep.append(f"{per}: companies {len(df)}, max rank {df['rank'].max()}, rank gaps {df['rank'].max() - len(df)}, "
                   f"categorised {df['category'].notna().mean():.3f}, total avg mcap Rs {df['avg_mcap_cr'].sum()/1e5:.1f} lakh crore")
    A = pd.concat(frames, ignore_index=True)
    A = A.drop_duplicates(["period_end", "isin"])
    A.to_csv(os.path.join(out, "amfi_mcap.csv.gz"), index=False, compression="gzip")
    open(os.path.join(out, "amfi_mcap_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
