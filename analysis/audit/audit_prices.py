"""Audit: duplicates, legacy->UDiFF continuity, combineoi OI vs bhavcopy OI, rate coverage. Outcome-free (no ban info used)."""
import glob, os, sys
import pandas as pd
RAW = sys.argv[1]
def load(sub, cols):
    fs = sorted(glob.glob(os.path.join(RAW, "prices", sub, "*.csv")))
    return pd.concat([pd.read_csv(f, usecols=lambda c: c in cols) for f in fs if os.path.getsize(f) > 0], ignore_index=True)
fut = load("fut", {"date","inst","symbol","expiry","contracts","oi","value_rs","src"})
fut = fut[fut.inst == "STF"]
print("STF rows", len(fut), "dup (date,symbol,expiry):", fut.duplicated(["date","symbol","expiry"]).sum())
print("src by year:", fut.groupby([fut.date.str[:4], "src"]).size().unstack().fillna(0).astype(int).tail(4).to_dict())
fut["d"] = pd.to_datetime(fut.date)
w = fut[(fut.d >= "2024-06-10") & (fut.d <= "2024-08-05")]
print(w.groupby(["date","src"]).agg(n=("symbol","nunique"), contracts=("contracts","sum"), oi=("oi","sum")).to_string())
cash = load("cash", {"date","symbol","series"})
print("cash rows", len(cash), "dup (date,symbol,series):", cash.duplicated(["date","symbol","series"]).sum())
opt = load("optsum", {"inst","symbol","oi","date"})
# combineoi (gross OI in shares, fut+opt) vs bhavcopy: sum STF OI + STO OI per stock-day
oi_f = fut.groupby(["date","symbol"]).oi.sum()
oi_o = opt[opt.inst == "STO"].groupby(["date","symbol"]).oi.sum()
bh = oi_f.add(oi_o, fill_value=0).rename("bhav").reset_index()
bh["date"] = pd.to_datetime(bh.date)
pan = pd.read_csv("data/processed/mwpl_oi_panel.csv.gz", usecols=["date","symbol","oi","futeq_oi"], parse_dates=["date"])
m = pan.merge(bh, on=["date","symbol"], how="inner")
m["r"] = m.oi / m.bhav
m["era"] = pd.cut(m.date, [pd.Timestamp("2014-12-31"), pd.Timestamp("2024-07-05"), pd.Timestamp("2025-09-30"), pd.Timestamp("2030-01-01")],
                  labels=["legacy", "udiff_pre_reform", "post_reform"])
print("matched stock-days", len(m), "of panel 2015+", (pan.date >= "2015-01-01").sum())
print(m.groupby("era", observed=True).r.describe(percentiles=[.01,.5,.99]).to_string())
print("share |r-1|>1%:", m.groupby("era", observed=True).r.apply(lambda s: ((s-1).abs() > .01).mean()).round(4).to_dict())
bad = m[(m.r - 1).abs() > .01]
print("worst:", bad.assign(a=(bad.r-1).abs()).sort_values("a").tail(8)[["date","symbol","oi","bhav","r"]].to_string())
ra = pd.read_csv(os.path.join(RAW, "rates", "INDIR3TIB01STM.csv"))
print("rate file tail:\n", ra.tail(3).to_string())
