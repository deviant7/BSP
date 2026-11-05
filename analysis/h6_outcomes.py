"""Outcomes for H6 (PAP §3 O5, O6; §11.3 C6 d-e). Outcome construction only: nothing here uses F&O status.

Outputs (data/processed/cache/):
  delay_panel.pkl   symbol x calendar year: D1 price delay (Hou-Moskowitz), VR(5), weeks used, log mcap, log traded value,
                    daily volatility (the covariates of C6 c)
  event_outcomes.pkl  results announcements: EAR[-1,+1], BHAR[+2,+64] against the stock's size-decile EW portfolio,
                    bad-news indicator (bottom tercile of EAR within the calendar quarter)
Report: analysis/output/h6_outcomes_report.txt
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import PROC, CACHE, ROOT

OUT = os.path.join(ROOT, "analysis", "output")


def wide():
    R = pd.read_csv(os.path.join(PROC, "returns_daily.csv.gz"), usecols=["date", "symbol", "ret", "value_rs", "close"], parse_dates=["date"])
    M = pd.read_csv(os.path.join(PROC, "mcap_daily.csv.gz"), usecols=["date", "symbol", "mcap_cr"], parse_dates=["date"])
    days = pd.DatetimeIndex(sorted(R["date"].unique())); syms = pd.Index(sorted(R["symbol"].unique()))
    di = days.get_indexer(R["date"]); si = syms.get_indexer(R["symbol"])
    ret = np.full((len(days), len(syms)), np.nan, dtype="float64"); ret[di, si] = R["ret"].values
    val = np.full_like(ret, np.nan); val[di, si] = R["value_rs"].values
    px = np.full_like(ret, np.nan); px[di, si] = R["close"].values
    mc = np.full_like(ret, np.nan)
    dm = days.get_indexer(M["date"]); sm = syms.get_indexer(M["symbol"]); ok = (dm >= 0) & (sm >= 0)
    mc[dm[ok], sm[ok]] = M["mcap_cr"].values[ok]
    return days, syms, ret, val, mc, px


def main():
    os.makedirs(CACHE, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    rep = []
    days, syms, ret, val, mc, px = wide()
    T, N = ret.shape
    rep.append(f"wide panel: {T} days x {N} stocks; valid returns {np.isfinite(ret).mean():.3f}; market cap {np.isfinite(mc).mean():.3f}")
    # value-weighted market (weights = previous day's market cap)
    w = np.vstack([np.full((1, N), np.nan), mc[:-1]])
    okm = np.isfinite(w) & np.isfinite(ret)
    mkt = np.where(okm, w * ret, 0).sum(1) / np.where(okm, w, 0).sum(1)
    # size deciles each month on the previous month-end market cap; equal-weighted daily decile returns
    month = days.to_period("M")
    dec = np.full((T, N), -1, dtype=np.int8)
    mends = pd.Series(np.arange(T), index=days).groupby(month).max()
    for j, m in enumerate(mends.index):
        if j == 0:
            continue
        cap = mc[mends.iloc[j - 1]]
        okc = np.isfinite(cap)
        if okc.sum() < 100:
            continue
        q = np.full(N, -1, dtype=np.int8)
        q[okc] = np.minimum((pd.Series(cap[okc]).rank(pct=True).values * 10).astype(int), 9)
        rows = np.where(month == m)[0]
        dec[rows] = q
    port = np.full((T, 10), np.nan)
    for k in range(10):
        msk = (dec == k) & np.isfinite(ret)
        port[:, k] = np.where(msk, ret, 0).sum(1) / np.maximum(msk.sum(1), 1)
        port[msk.sum(1) == 0, k] = np.nan
    bench = np.full((T, N), np.nan)
    for k in range(10):
        bench = np.where(dec == k, port[:, [k]], bench)

    # ---- O6: delay and VR(5) per stock-year
    wk = days.to_period("W-FRI")
    wks = pd.Index(sorted(set(wk)))
    wi = wks.get_indexer(wk)
    lr = np.log1p(ret)
    W = len(wks)
    wret = np.full((W, N), np.nan); wcnt = np.zeros((W, N))
    for j in range(W):
        rows = np.where(wi == j)[0]
        x = lr[rows]
        c = np.isfinite(x).sum(0)
        wret[j] = np.where(c >= 3, np.expm1(np.nansum(x, 0)), np.nan); wcnt[j] = c
    wm = np.array([np.expm1(np.nansum(np.log1p(mkt[wi == j]))) for j in range(W)])
    L = np.column_stack([np.roll(wm, l) for l in range(5)]); L[:4] = np.nan
    wyear = np.array([p.end_time.year for p in wks])
    rows = []
    for y in range(2015, 2026):
        jj = np.where(wyear == y)[0]
        X1 = np.column_stack([np.ones(len(jj)), L[jj, 0]]); X5 = np.column_stack([np.ones(len(jj)), L[jj]])
        dy = np.where(days.year == y)[0]
        for i in range(N):
            yv = wret[jj, i]
            ok = np.isfinite(yv) & np.isfinite(L[jj]).all(1)
            if ok.sum() < 40:
                continue
            yy = yv[ok]; tss = ((yy - yy.mean()) ** 2).sum()
            if tss <= 0:
                continue
            r1 = 1 - ((yy - X1[ok] @ np.linalg.lstsq(X1[ok], yy, rcond=None)[0]) ** 2).sum() / tss
            r5 = 1 - ((yy - X5[ok] @ np.linalg.lstsq(X5[ok], yy, rcond=None)[0]) ** 2).sum() / tss
            d1 = 1 - r1 / r5 if r5 > 0 else np.nan
            x = lr[dy, i]; x = x[np.isfinite(x)]
            vr = np.nan
            if len(x) >= 150:
                s5 = np.convolve(x, np.ones(5), "valid")
                vr = s5.var() / (5 * x.var()) if x.var() > 0 else np.nan
            rows.append((syms[i], y, d1, vr, int(ok.sum()), np.log(np.nanmean(mc[dy, i])) if np.isfinite(mc[dy, i]).any() else np.nan,
                         np.log(np.nanmean(val[dy, i])) if np.isfinite(val[dy, i]).any() else np.nan, np.nanstd(ret[dy, i]),
                         np.nanmean(px[dy, i])))
    D = pd.DataFrame(rows, columns=["symbol", "year", "delay", "vr5", "weeks", "log_mcap", "log_value", "vol", "avg_price"])
    n0 = len(D); D = D[D["avg_price"] >= 5]
    rep.append(f"stock-years with average price below Rs 5 dropped: {n0 - len(D)}")
    D.to_pickle(os.path.join(CACHE, "delay_panel.pkl"))
    rep.append(f"delay panel: {len(D)} stock-years, {D['symbol'].nunique()} stocks; delay median {D['delay'].median():.3f} "
               f"(p10 {D['delay'].quantile(.1):.3f}, p90 {D['delay'].quantile(.9):.3f}); VR5 median {D['vr5'].median():.3f}")
    rep.append("  delay by log-mcap quintile (outcome on its own): " +
               D.groupby(pd.qcut(D["log_mcap"], 5, labels=False))["delay"].median().round(3).to_dict().__repr__())

    # ---- O5: EAR and BHAR around results announcements
    A = pd.read_csv(os.path.join(PROC, "announcements.csv.gz"), usecols=["symbol", "period_end", "event_day", "timing_known"],
                    parse_dates=["event_day"])
    A = A[A["event_day"].between(days[1], days[-1])]
    A["si"] = syms.get_indexer(A["symbol"]); A["ti"] = days.get_indexer(A["event_day"])
    A = A[(A["si"] >= 0) & (A["ti"] >= 1)]
    n0 = len(A); A = A.drop_duplicates(["symbol", "event_day"])
    A["px0"] = px[A["ti"].values, A["si"].values]
    rep.append(f"duplicate (stock, event day) dropped: {n0 - len(A)}; events with day-0 price below Rs 5 dropped: {int((A['px0'] < 5).sum())} "
               f"(no price: {int(A['px0'].isna().sum())})")
    A = A[A["px0"] >= 5]
    ex = ret - bench
    out = []
    for si, ti in zip(A["si"].values, A["ti"].values):
        a, b = ti - 1, ti + 2
        x, p = ret[a:b, si], bench[a:b, si]
        ok = np.isfinite(x) & np.isfinite(p)
        ear = np.prod(1 + x[ok]) - np.prod(1 + p[ok]) if ok.sum() >= 2 else np.nan
        a2, b2 = ti + 2, ti + 65
        if b2 > T:
            out.append((ear, np.nan, 0)); continue
        x, p = ret[a2:b2, si], bench[a2:b2, si]
        ok = np.isfinite(x) & np.isfinite(p)
        bh = np.prod(1 + x[ok]) - np.prod(1 + p[ok]) if ok.sum() >= 50 else np.nan
        out.append((ear, bh, int(ok.sum())))
    A[["ear", "bhar", "n_days"]] = np.array(out)
    A["year"] = A["event_day"].dt.year
    for c in ("ear", "bhar"):
        lo, hi = A.groupby("year")[c].transform(lambda x: x.quantile(0.01)), A.groupby("year")[c].transform(lambda x: x.quantile(0.99))
        A[c + "_w"] = A[c].clip(lo, hi)
    A["q"] = A["event_day"].dt.to_period("Q")
    A["ear_terc"] = A.groupby("q")["ear"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False) if s.notna().sum() >= 30 else np.nan)
    A["bad"] = A["ear_terc"] == 0
    A["good"] = A["ear_terc"] == 2
    A.to_pickle(os.path.join(CACHE, "event_outcomes.pkl"))
    rep.append(f"events with EAR: {A['ear'].notna().sum()} of {len(A)}; with BHAR: {A['bhar'].notna().sum()}")
    rep.append(f"  winsorised mean BHAR after bad news {A.loc[A['bad'],'bhar_w'].mean():.4f}, after good news {A.loc[A['good'],'bhar_w'].mean():.4f}, "
               f"middle {A.loc[A['ear_terc']==1,'bhar_w'].mean():.4f}; medians {A.loc[A['bad'],'bhar'].median():.4f} / "
               f"{A.loc[A['good'],'bhar'].median():.4f} / {A.loc[A['ear_terc']==1,'bhar'].median():.4f} (drift exists if bad < good)")
    open(os.path.join(OUT, "h6_outcomes_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
