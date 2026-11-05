"""Audit: does combineoi OI on date t equal bhavcopy gross OI (stock futures + stock options) on t, t-1 or t+1?
Bhavcopy OI on an expiry day still includes the expiring contracts, combineoi does not -> expiry days are excluded."""
import glob, os, sys
import pandas as pd
RAW = sys.argv[1]
def load(sub, cols):
    fs = sorted(glob.glob(os.path.join(RAW, "prices", sub, "*.csv")))
    return pd.concat([pd.read_csv(f, usecols=lambda c: c in cols) for f in fs if os.path.getsize(f) > 0], ignore_index=True)
fut = load("fut", {"date", "inst", "symbol", "oi", "expiry"}); fut = fut[fut.inst.isin(["STF", "FUTSTK"])]
expd = set(pd.to_datetime(fut.expiry.unique()))
opt = load("optsum", {"inst", "symbol", "oi", "date"}); opt = opt[opt.inst.isin(["STO", "OPTSTK"])]
bh = fut.groupby(["date", "symbol"]).oi.sum().add(opt.groupby(["date", "symbol"]).oi.sum(), fill_value=0).rename("bhav").reset_index()
bh["date"] = pd.to_datetime(bh.date)
days = sorted(bh.date.unique()); idx = {d: i for i, d in enumerate(days)}
bh["i"] = bh.date.map(idx)
pan = pd.read_csv("data/processed/mwpl_oi_panel.csv.gz", usecols=["date", "symbol", "oi"], parse_dates=["date"])
pan = pan[pan.date.isin(idx)]; pan["i"] = pan.date.map(idx)
out = []
for k in (-1, 0, 1):
    b = bh[["i", "symbol", "bhav"]].copy(); b["i"] = b.i - k      # bhav of day i+k aligned to panel day i
    m = pan.merge(b, on=["i", "symbol"])
    m["ok"] = (m.oi / m.bhav - 1).abs() <= 0.01
    out.append(m.groupby("date").ok.mean().rename(f"match_t{k:+d}"))
res = pd.concat(out, axis=1)
res = res[~res.index.isin(expd)]
best = res.idxmax(axis=1)
res["best"] = best
bad = res[(res["match_t+0"] < 0.9)]
print(f"non-expiry days {len(res)}; days with <90% match at t: {len(bad)}")
print(bad.round(3).to_string())
