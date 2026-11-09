"""Secondary (supporting) test: density of utilisation at the 95% trigger. Specification: PAP §11.5 C8.
Treatment side only (utilisation; no outcome). Outputs analysis/output/density_test.txt and reports/figs/density_95.pdf.
"""
import os, sys, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import calendar, PROC, ROOT

warnings.filterwarnings("ignore")
OUT = os.path.join(ROOT, "analysis", "output")
FIG = os.path.join(ROOT, "reports", "figs")
REFORM = pd.Timestamp("2025-10-01")
INTRADAY = pd.Timestamp("2020-03-23")
C = 0.95
rng = np.random.default_rng(95)


def panel():
    days, pos = calendar()
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl", "util", "util_futeq"],
                    parse_dates=["date"])
    P["omega"] = np.where(P["date"] >= REFORM, P["util_futeq"], P["util"])
    P["i"] = P["date"].map(pos)
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["ban"] = True
    P = P.merge(B[["date", "symbol", "ban"]], on=["date", "symbol"], how="left")
    P["ban"] = P["ban"].fillna(False).astype(bool)
    L = P[["symbol", "i", "omega", "ban", "mwpl"]].copy()
    L["i"] += 1
    L = L.rename(columns={"omega": "omega_prev", "ban": "ban_prev", "mwpl": "mwpl_prev"})
    P = P.merge(L, on=["symbol", "i"], how="left")
    P["mwpl_change"] = P["mwpl"] != P["mwpl_prev"]
    return P


def cjm(x, **kw):
    from rddensity import rddensity
    r = rddensity(X=np.asarray(x, float), c=C, **kw)
    t, p = r.test["t_jk"], r.test["p_jk"]
    return dict(t=t, p=p, fl=r.hat["left"], fr=r.hat["right"], hl=r.h["left"], hr=r.h["right"],
                nl=int(np.sum((x >= C - r.h["left"]) & (x < C))), nr=int(np.sum((x >= C) & (x <= C + r.h["right"]))))


def binned_theta(x, w=0.0025, h=0.05):
    """McCrary-type: local linear fit of normalised bin frequencies on each side; theta = ln f+ - ln f-."""
    n = len(x)
    edges = np.arange(C - h, C + h + w / 2, w)
    cnt, _ = np.histogram(x, edges)
    f = cnt / (n * w)
    mid = (edges[:-1] + edges[1:]) / 2
    out = []
    for side in (mid < C, mid >= C):
        xm, fm = mid[side] - C, f[side]
        k = np.clip(1 - np.abs(xm) / h, 0, None)
        X = np.c_[np.ones_like(xm), xm]
        W = np.diag(k)
        b = np.linalg.lstsq(X.T @ W @ X, X.T @ W @ fm, rcond=None)[0]
        out.append(b[0])
    fl, fr = out
    return np.log(fr) - np.log(fl) if fl > 0 and fr > 0 else np.nan, fl, fr


def cluster_boot(df, B=499):
    g = {s: v["omega"].values for s, v in df.groupby("symbol")}
    keys = np.array(list(g))
    th = []
    for _ in range(B):
        x = np.concatenate([g[k] for k in rng.choice(keys, len(keys))])
        th.append(binned_theta(x)[0])
    th = np.array(th)
    return np.nanstd(th), np.nanpercentile(th, [2.5, 97.5])


def report(df, lab, full=True, boot=True):
    x = df["omega"].values
    x = x[(x >= 0.60) & (x <= 1.30)]
    r = [f"{lab}: n in [0.60, 1.30] = {len(x)} (stock-days), stocks {df['symbol'].nunique()}; "
         f"n in [0.90, 0.95) {int(((x >= .9) & (x < .95)).sum())}, in [0.95, 1.00) {int(((x >= .95) & (x < 1)).sum())}"]
    if len(x) < 200 or ((x >= C) & (x < C + 0.05)).sum() < 20:
        r.append("  too few observations near the cutoff for the density test")
        return r, None
    m = cjm(x)
    r.append(f"  CJM (p=2, MSE-optimal h): f(0.95-) {m['fl']:.3f}, f(0.95+) {m['fr']:.3f}, log ratio "
             f"{np.log(m['fr'] / m['fl']):+.3f}; robust T {m['t']:+.2f}, p = {m['p']:.3g}; h_left {m['hl']:.3f} "
             f"(n {m['nl']}), h_right {m['hr']:.3f} (n {m['nr']})")
    if full:
        for kw, nm in [(dict(p=1), "p=1"), (dict(p=3), "p=3"), (dict(h=0.02), "h=0.02"), (dict(h=0.05), "h=0.05")]:
            try:
                q = cjm(x, **kw)
                r.append(f"    {nm}: log ratio {np.log(q['fr'] / q['fl']):+.3f}, T {q['t']:+.2f}, p = {q['p']:.3g}")
            except Exception as e:
                r.append(f"    {nm}: failed ({e.__class__.__name__})")
    th, fl, fr = binned_theta(df["omega"].values)
    if boot:
        # log ratio is invariant to the normalising n, so resampling stocks within the fitting window is enough
        se, ci = cluster_boot(df[df["omega"].between(C - 0.06, C + 0.06)])
        r.append(f"  binned (w 0.0025, h 0.05): theta = ln f+ - ln f- = {th:+.3f}; stock-cluster bootstrap se {se:.3f}, "
                 f"95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
    else:
        r.append(f"  binned (w 0.0025, h 0.05): theta = {th:+.3f}")
    return r, m


def main():
    P = panel()
    pre = P[(P["date"] >= "2015-01-01") & (P["date"] < REFORM)]
    r = ["Density of utilisation at the 95% trigger (PAP §11.5 C8). Treatment side only.", ""]
    main_pop = pre[~pre["ban_prev"].fillna(True).astype(bool) & ~pre["ban"] & (pre["omega_prev"] < C)]
    lit_pop = pre[~pre["ban"]]
    out, m_main = report(main_pop, "MAIN: transitions (not in ban on d-1 and d; omega_(d-1) < 0.95), 2015 to Sep 2025")
    r += out
    r += [""] + report(lit_pop, "LITERAL: all stock-days not in a ban on d (mechanically discontinuous; see C8 b)")[0]
    r += ["", "Robustness and sub-samples (main population definition):"]
    r += report(main_pop[~main_pop["mwpl_change"].fillna(True)], "  excluding days with an MWPL change", full=False)[0]
    r += report(main_pop[main_pop["date"] < INTRADAY], "  end-of-day enforcement (to 22 Mar 2020)", full=False)[0]
    r += report(main_pop[main_pop["date"] >= INTRADAY], "  peak-intraday enforcement (23 Mar 2020 to Sep 2025)", full=False)[0]
    ps = P[(P["date"] < "2015-01-01")]
    ps = ps[~ps["ban_prev"].fillna(True).astype(bool) & ~ps["ban"] & (ps["omega_prev"] < C)]
    r += report(ps, "  pre-sample 2010 to 2014", full=False)[0]
    po = P[P["date"] >= REFORM]
    po = po[~po["ban_prev"].fillna(True).astype(bool) & ~po["ban"] & (po["omega_prev"] < C)]
    r += report(po, "  after 1 Oct 2025 (FutEq utilisation; descriptive)", full=False, boot=False)[0]
    # supplementary: daily change in utilisation by omega_(d-1) bin
    s = main_pop.copy()
    s["d_omega"] = s["omega"] - s["omega_prev"]
    s["bin"] = pd.cut(s["omega_prev"], [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.925, 0.95], right=False)
    tab = s.groupby("bin", observed=True)["d_omega"].agg(["size", "mean", "median", lambda v: (v > 0).mean()])
    tab.columns = ["n", "mean d_omega", "median d_omega", "share rising"]
    r += ["", "Supplementary: daily change in utilisation by omega_(d-1), main population:", tab.round(4).to_string()]
    s["cross"] = s["omega"] >= C
    tab2 = s[s["omega_prev"] >= 0.85].groupby(pd.cut(s["omega_prev"], np.arange(0.85, 0.951, 0.01), right=False),
                                               observed=True)["cross"].agg(["size", "mean"])
    r += ["", "Share crossing 0.95 the next day by omega_(d-1):", tab2.round(4).to_string()]
    r += exploratory(main_pop, m_main)
    txt = "\n".join(r)
    open(os.path.join(OUT, "density_test.txt"), "w").write(txt + "\n")
    print(txt)
    figure(main_pop, lit_pop)


def exploratory(main_pop, m, B=499):
    """EXPLORATORY (added 7 Nov 2026 after the C8 results were seen; PAP §11.2): the CJM estimate and the binned
    (non-bias-corrected) estimate disagree. (1) stock-cluster bootstrap of the CJM log density ratio at the main
    MSE-optimal bandwidths (dependence-robust se for the pre-specified estimator); (2) the binned estimate at other
    bandwidths."""
    from rddensity import rddensity
    r = ["", "EXPLORATORY (added after the results were seen; PAP §11.2)"]
    df = main_pop[main_pop["omega"].between(0.60, 1.30)]
    g = {s_: v["omega"].values for s_, v in df.groupby("symbol")}
    keys = np.array(list(g))
    h = [m["hl"], m["hr"]]
    lr = []
    for _ in range(B):
        x = np.concatenate([g[k] for k in rng.choice(keys, len(keys))])
        try:
            q = rddensity(X=x, c=C, h=h)
            lr.append(np.log(q.hat["right"] / q.hat["left"]))
        except Exception:
            pass
    lr = np.array(lr)
    r.append(f"  (1) CJM log ratio at h = ({h[0]:.3f}, {h[1]:.3f}): {np.log(m['fr'] / m['fl']):+.3f}; stock-cluster "
             f"bootstrap ({len(lr)} draws) se {lr.std():.3f}, 95% interval [{np.percentile(lr, 2.5):+.3f}, "
             f"{np.percentile(lr, 97.5):+.3f}]")
    x = main_pop["omega"].values
    for hh in (0.02, 0.03, 0.04, 0.05, 0.075, 0.10):
        r.append(f"  (2) binned theta, h = {hh}: {binned_theta(x, h=hh)[0]:+.3f}")
    return r


def figure(main_pop, lit_pop):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=False)
    for ax, df, ttl in [(axes[0], main_pop, "Stocks below 95% the day before"),
                        (axes[1], lit_pop, "All stock-days not in a ban")]:
        x = df["omega"].values
        x = x[(x >= 0.80) & (x < 1.10)]
        ax.hist(x, bins=np.arange(0.80, 1.10001, 0.005), color="#4a6b8a", edgecolor="white", linewidth=0.3)
        ax.axvline(C, color="#b03a2e", linestyle="--", linewidth=1)
        ax.set_title(ttl, fontsize=9)
        ax.set_xlabel("Utilisation of the MWPL (end of day)", fontsize=8)
        ax.tick_params(labelsize=7)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0].set_ylabel("Stock-days per bin", fontsize=8)
    fig.tight_layout()
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, "density_95.pdf"))


if __name__ == "__main__":
    main()
