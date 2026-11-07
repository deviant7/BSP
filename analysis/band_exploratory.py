"""EXPLORATORY additions to the band chapter (added 7 Nov 2026 AFTER the C16 estimates were seen; logged in PAP §11.2).

(1) Period-specific demeaning: the full-sample stock median does not remove level shifts (H3 found a rise of about 7 bp
    around 2024/2026), which makes the 2026 thresholds collapse; re-estimate with x demeaned by the stock's median within
    each STT period.
(2) Measurement noise: the middle regime shows strong reversion (half-life about 1 day), unlike a textbook band. Classical
    noise in daily VWAP prices biases the slope of Delta m_t on m_(t-1) toward -1. Check: instrument x_(t-1) with x_(t-2)
    (same stock, previous valid day) in the linear model and by regime of x_(t-2); compare with OLS.
Outputs analysis/output/band_exploratory.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from band_estimation import load, SortedData, setar_fit, fmt_setar, QGRID, STT, BP
from samples import ROOT

OUT = os.path.join(ROOT, "analysis", "output")


def main():
    S = load()
    r = ["EXPLORATORY band checks (not pre-specified; PAP §11.2). Units bp.", ""]
    # (1) period-specific demeaning
    S["per"] = "p0"
    for k, (lab, a, b) in enumerate(STT):
        msk = pd.Series(True, index=S.index)
        if a: msk &= S["date"] >= a
        if b: msk &= S["date"] < b
        S.loc[msk, "per"] = lab
    med = S.groupby(["symbol", "per"])["m_lag"].transform("median")
    S["xp"] = (S["m_lag"] - med) * BP
    r.append("(1) Threshold model with x demeaned by the stock's median within each STT period:")
    for lab, g in S.groupby("per", sort=False):
        x, d = g["xp"].values, g["d"].values
        o = setar_fit(SortedData(x, np.unique(np.quantile(x, QGRID))), d)
        r.append(fmt_setar(o, f"STT period {lab}"))
    for yv, g in S.groupby(S["date"].dt.year):
        if yv not in (2020, 2025, 2026):
            continue
        x, d = g["xp"].values, g["d"].values
        o = setar_fit(SortedData(x, np.unique(np.quantile(x, QGRID))), d)
        r.append(fmt_setar(o, f"year {yv} (period-demeaned)"))
    # (2) noise check: IV with the second lag
    S = S.sort_values(["symbol", "i"])
    L = S[["symbol", "i", "x"]].copy(); L["i"] += 1
    S = S.merge(L.rename(columns={"x": "x2"}), on=["symbol", "i"], how="left")
    d = S.dropna(subset=["x2"])
    def ols(y, x):
        X = np.c_[np.ones_like(x), x]; return np.linalg.lstsq(X, y, rcond=None)[0][1]
    def iv(y, x, z):
        Z = np.c_[np.ones_like(z), z]; X = np.c_[np.ones_like(x), x]
        b = np.linalg.solve(Z.T @ X, Z.T @ y); return b[1]
    r += ["", f"(2) Noise check (linear, pooled, n {len(d)}): OLS slope of Delta m_t on x_(t-1) {ols(d['d'].values, d['x'].values):+.3f}; "
              f"IV with x_(t-2) {iv(d['d'].values, d['x'].values, d['x2'].values):+.3f}; "
              f"first-order autocorrelation of x {np.corrcoef(d['x'], d['x2'])[0, 1]:.3f}"]
    lo, hi = np.percentile(d["x2"], [12, 88])
    for nm, msk in [("x_(t-2) below its 12th pct", d["x2"] < lo), ("middle", (d["x2"] >= lo) & (d["x2"] <= hi)),
                    ("x_(t-2) above its 88th pct", d["x2"] > hi)]:
        g = d[msk]
        r.append(f"    regime by x_(t-2), {nm:28s}: OLS {ols(g['d'].values, g['x'].values):+.3f}; "
                 f"IV {iv(g['d'].values, g['x'].values, g['x2'].values):+.3f}; n {len(g)}")
    r.append("  Reading: with classical noise in m, OLS slopes are biased toward -1 and IV slopes are not; IV slopes much "
             "closer to 0 mean that much of the day-to-day reversion is noise.")
    txt = "\n".join(r)
    open(os.path.join(OUT, "band_exploratory.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
