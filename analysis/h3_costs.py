"""H3 (primary): costs set the band edges. Specification: PAP §5 and §11 C4.
Event windows of 40 trading days before / from each STT increase; stock-level change in the 80th (and 20th, 50th)
percentile of the winsorised basis. Outputs analysis/output/h3_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, ROOT
from inference import feols, coef_table
from setar import fit_setar3

OUT = os.path.join(ROOT, "analysis", "output")
BP = 1e4
EVENTS = {"2023": ("2023-04-01", 0.25), "2024": ("2024-10-01", 0.75), "2026": ("2026-04-01", 3.0)}  # STT change in bp


def window_stats(S, i0, W=40, min_n=20):
    pre = S[(S["i"] >= i0 - W) & (S["i"] <= i0 - 1)]
    post = S[(S["i"] >= i0) & (S["i"] <= i0 + W - 1)]
    out = []
    for q in (0.8, 0.2, 0.5):
        a = pre.groupby("symbol")["m"].agg(["size", lambda s, q=q: s.quantile(q)])
        b = post.groupby("symbol")["m"].agg(["size", lambda s, q=q: s.quantile(q)])
        a.columns = b.columns = ["n", "v"]
        j = a.join(b, lsuffix="_pre", rsuffix="_post", how="inner")
        j = j[(j["n_pre"] >= min_n) & (j["n_post"] >= min_n)]
        out.append(((j["v_post"] - j["v_pre"]) * BP).rename(f"d{int(q*100)}"))
    return pd.concat(out, axis=1).dropna()


def pooled_setar(S, i0, W=40):
    res = {}
    win = S[(S["i"] >= i0 - W) & (S["i"] <= i0 + W - 1)].dropna(subset=["m_lag", "dm"]).copy()
    mu = win.groupby("symbol")["m"].mean()
    win["x"] = (win["m_lag"] - win["symbol"].map(mu)) * BP
    win["d"] = win["dm"] * BP
    for lab, msk in (("pre", win["i"] < i0), ("post", win["i"] >= i0)):
        f = fit_setar3(win.loc[msk, "x"].values, win.loc[msk, "d"].values)
        res[lab] = (f["gL"], f["gU"]) if f else (np.nan, np.nan)
    return res


def main():
    S = basis_sample()
    days, pos = calendar()
    r = ["H3: costs set the band edges (PAP §5, §11 C4). Changes in stock-level percentiles of the basis (bp), post minus pre,",
         "40 trading days each side. Prediction: the 80th percentile (upper edge) rises; size ordered 2026 > 2024 > 2023.", ""]
    ev_idx, rows = {}, []
    for k, (d, dc) in EVENTS.items():
        i0 = int(days.searchsorted(pd.Timestamp(d)))
        ev_idx[k] = i0
        w = window_stats(S, i0)
        w["event"] = k
        rows.append(w.reset_index())
        st = pooled_setar(S, i0)
        r.append(f"{k} (event day {days[i0].date()}, futures STT +{dc} bp per sale): stocks {len(w)}; "
                 f"mean d80 {w['d80'].mean():+.2f} (se {w['d80'].std()/np.sqrt(len(w)):.2f}), median {w['d80'].median():+.2f}; "
                 f"mean d20 {w['d20'].mean():+.2f}; mean d50 {w['d50'].mean():+.2f}; "
                 f"pooled threshold model upper edge pre {st['pre'][1]:+.1f} -> post {st['post'][1]:+.1f}, "
                 f"lower {st['pre'][0]:+.1f} -> {st['post'][0]:+.1f}")
    P = pd.concat(rows, ignore_index=True)
    fam = P[P["event"].isin(["2024", "2026"])].copy()
    t = coef_table(feols(fam, "d80 ~ 1", cluster="symbol"))
    G = fam["symbol"].nunique() - 1
    b, se = t.loc["Intercept", "b"], t.loc["Intercept", "se"]
    p = float(stats.t.sf(b / se, G))
    r += ["", f"Family test statistic (C4 d): mean d80 over {len(fam)} stock-events (2024, 2026) = {b:+.3f} bp (se {se:.3f}, "
              f"clustered by stock); one-sided p_H3 = {p:.3g}"]
    m = P.groupby("event")["d80"].mean()
    order = list(m.sort_values(ascending=False).index)
    r.append(f"Ordering of mean d80: {', '.join(f'{e} {m[e]:+.2f}' for e in order)} -> predicted 2026 > 2024 > 2023: "
             f"{'YES' if order == ['2026', '2024', '2023'] else 'NO'}")
    # placebo distribution (C4 f)
    first = int(S["i"].min()) + 40
    last = int(S["i"].max()) - 39
    true_i = list(ev_idx.values())
    pl = []
    for i0 in range(first, last + 1, 80):
        if any(abs(i0 - j) < 80 for j in true_i):
            continue
        w = window_stats(S, i0)
        if len(w) >= 50:
            pl.append((days[i0].date(), w["d80"].mean()))
    pv = np.array([v for _, v in pl])
    r += ["", f"Placebo (C4 f): {len(pv)} pseudo-events every 80 trading days, windows not overlapping true dates; "
              f"mean d80 across placebos: mean {pv.mean():+.2f}, sd {pv.std():.2f}, min {pv.min():+.2f}, max {pv.max():+.2f}"]
    for k in EVENTS:
        r.append(f"  {k}: mean d80 {m[k]:+.2f}; share of placebos with a value at least as large: {(pv >= m[k]).mean():.3f}")
    txt = "\n".join(r)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "h3_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
