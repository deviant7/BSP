"""Audit: day-by-day coverage of every raw source against the NSE trading calendar."""
import glob, os, re, sys
import pandas as pd

RAW = sys.argv[1]
def days_from(pattern, rx, fmt):
    out = set()
    for f in glob.glob(os.path.join(RAW, pattern)):
        if os.path.getsize(f) == 0:
            continue
        m = re.search(rx, os.path.basename(f))
        if m:
            out.add(pd.to_datetime(m.group(1), format=fmt))
    return out

oi = days_from("combineoi/*.zip", r"(\d{8})", "%d%m%Y")
sb = days_from("secban/*.csv", r"(\d{8})", "%d%m%Y")
fut = days_from("prices/fut/*.csv", r"(\d{8})", "%Y%m%d")
cash = days_from("prices/cash/*.csv", r"(\d{8})", "%Y%m%d")
dl = days_from("prices/deliv/*.csv", r"(\d{8})", "%Y%m%d")
opt = days_from("prices/optsum/*.csv", r"(\d{8})", "%Y%m%d")
nifty = set(pd.to_datetime(pd.read_csv(os.path.join(RAW, "indices/nifty50_daily.csv"))["date"]))

# trading calendar: cash days (2015+) U OI days (any date) ; check weekends
cal = sorted(cash | oi)
cal15 = [d for d in cal if d >= pd.Timestamp("2015-01-01")]
print(f"calendar days: all {len(cal)} ({min(cal).date()}..{max(cal).date()}), 2015+ {len(cal15)}")
print("weekend trading days:", [d.date() for d in cal if d.weekday() >= 5])
for name, s, start in [("combineoi", oi, "2010-02-01"), ("secban", sb, "2010-02-01"), ("futures", fut, "2015-01-01"),
                       ("cash", cash, "2015-01-01"), ("delivery", dl, "2015-01-01"), ("options summary", opt, "2015-01-01"),
                       ("nifty", nifty, "2015-01-01")]:
    c = [d for d in cal if d >= pd.Timestamp(start)]
    miss = sorted(set(c) - s)
    extra = sorted(d for d in s - set(cal) if d >= pd.Timestamp(start))
    print(f"{name:16s} expected {len(c):5d}  missing {len(miss):3d} {[d.date() for d in miss][:12]}  "
          f"on non-calendar days {len(extra)} {[d.date() for d in extra][:6]}")
