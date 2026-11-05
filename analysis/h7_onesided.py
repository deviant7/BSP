"""H7 (primary): in a ban, correction of the basis becomes one-sided. Specification: PAP §5 and §11 C1, C2.

  dm_it = sum_r [beta_r + delta_r Ban_it] (m_(i,t-1) - mu_i) 1{regime r} + alpha_i + lambda_t + e_it
Prediction: delta_upper > 0, delta_lower <= 0; with an expiry inside the spell, delta_lower closer to 0.
Outputs analysis/output/h7_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, PROC, ROOT
from inference import feols, coef_table, lincomb
from setar import fit_setar3

OUT = os.path.join(ROOT, "analysis", "output")
BP = 1e4
REG = ["up", "mid", "lo"]


def thresholds(S, level, lagcol, dcol, method):
    """Per-stock mu and regime cut-offs from non-ban days (C2 a, f). Returns S with columns mu, gL, gU (and drops stocks
    with fewer than 100 non-ban observations)."""
    nb = S[~S["ban"] & S[level].notna()]
    cnt = nb.groupby("symbol").size()
    keep = cnt[cnt >= 100].index
    S = S[S["symbol"].isin(keep)].copy()
    nb = nb[nb["symbol"].isin(keep)]
    mu = nb.groupby("symbol")[level].median()
    if method == "pct":
        gL, gU = nb.groupby("symbol")[level].quantile(0.2), nb.groupby("symbol")[level].quantile(0.8)
    elif method == "fixed25":
        gL, gU = mu - 0.0025, mu + 0.0025
    elif method == "setar":
        g = {}
        for s, v in nb.dropna(subset=[lagcol, dcol]).groupby("symbol"):
            f = fit_setar3(v[lagcol].values, v[dcol].values)
            if f is not None:
                g[s] = (f["gL"], f["gU"])
        gL = pd.Series({k: a for k, (a, b) in g.items()}); gU = pd.Series({k: b for k, (a, b) in g.items()})
        S = S[S["symbol"].isin(gL.index)].copy()
    S["mu"] = S["symbol"].map(mu)
    if method == "state":
        # within each stock's terciles of omega_(t-1) on non-ban days
        nb = nb.dropna(subset=["omega_lag"])
        cuts = nb.groupby("symbol")["omega_lag"].quantile([1 / 3, 2 / 3]).unstack()
        S = S[S["symbol"].isin(cuts.index)].copy()
        def terc(df):
            c1 = df["symbol"].map(cuts[1 / 3]); c2 = df["symbol"].map(cuts[2 / 3])
            return np.where(df["omega_lag"] <= c1, 0, np.where(df["omega_lag"] <= c2, 1, 2))
        nb = nb[nb["symbol"].isin(cuts.index)].copy(); nb["terc"] = terc(nb)
        S["terc"] = np.where(S["omega_lag"].notna(), terc(S.fillna({"omega_lag": -1})), -1)
        q = nb.groupby(["symbol", "terc"])[level].quantile([0.2, 0.8]).unstack()
        key = pd.MultiIndex.from_arrays([S["symbol"], S["terc"]])
        S["gL"] = q[0.2].reindex(key).values; S["gU"] = q[0.8].reindex(key).values
        S = S[S["gL"].notna()]
    else:
        S["gL"] = S["symbol"].map(gL); S["gU"] = S["symbol"].map(gU)
    return S


def design(S, lagcol, dcol, postexp=False):
    D = S.dropna(subset=[lagcol, dcol]).copy()
    x = (D[lagcol] - D["mu"]) * BP
    up, lo = D[lagcol] > D["gU"], D[lagcol] < D["gL"]
    mid = ~up & ~lo
    ban = D["ban"].astype(float)
    D["y"] = D[dcol] * BP
    for r, msk in zip(REG, (up, mid, lo)):
        D[f"x_{r}"] = x * msk
        D[f"xb_{r}"] = x * msk * ban
        if postexp:
            D[f"xbe_{r}"] = x * msk * ban * D["postexp"]
    return D


def estimate(D, postexp=False):
    rhs = [f"x_{r}" for r in REG] + [f"xb_{r}" for r in REG] + ([f"xbe_{r}" for r in REG] if postexp else [])
    fit = feols(D, "y ~ " + " + ".join(rhs) + " | symbol + date")
    t = coef_table(fit)
    G = min(D["symbol"].nunique(), D["date"].nunique()) - 1
    b, se = lincomb(fit, {"xb_up": 1, "xb_lo": -1})
    p1 = float(stats.t.sf(t.loc["xb_up", "b"] / t.loc["xb_up", "se"], G))
    p2 = float(stats.t.sf(b / se, G))
    out = {"n": len(D), "stocks": D["symbol"].nunique(), "ban_obs": int(D["ban"].sum()), "t": t,
           "diff": (b, se), "p1": p1, "p2": p2, "p_iu": max(p1, p2)}
    if postexp:
        b2, se2 = lincomb(fit, {"xb_lo": 1, "xbe_lo": 1})
        out["lo_after_expiry"] = (b2, se2)
    return out


def fmt(name, o):
    t = o["t"]
    L = [f"{name}: n={o['n']}, stocks {o['stocks']}, ban observations {o['ban_obs']}"]
    for c in t.index:
        L.append(f"    {c:7s} {t.loc[c,'b']:+.4f}  (se {t.loc[c,'se']:.4f}, t {t.loc[c,'t']:+.2f})")
    L.append(f"    delta_up - delta_lo = {o['diff'][0]:+.4f} (se {o['diff'][1]:.4f}); one-sided p(delta_up>0) = {o['p1']:.3g}; "
             f"p(delta_up-delta_lo>0) = {o['p2']:.3g}; intersection-union p = {o['p_iu']:.3g}")
    if "lo_after_expiry" in o:
        b, se = o["lo_after_expiry"]
        L.append(f"    delta_lo after an expiry inside the spell (delta_lo + delta_lo_exp) = {b:+.4f} (se {se:.4f})")
    return "\n".join(L)


def add_postexp(S):
    sp = pd.read_csv(os.path.join(PROC, "ban_spells.csv.gz"), parse_dates=["start", "end"])
    exps = np.array(sorted(pd.read_csv(os.path.join(PROC, "basis_panel.csv.gz"), usecols=["expiry"],
                                       parse_dates=["expiry"])["expiry"].unique()), dtype="datetime64[ns]")
    b = S[S["ban"]][["symbol", "date"]].reset_index()
    b = b.merge(sp[["symbol", "start", "end"]], on="symbol")
    b = b[(b["date"] >= b["start"]) & (b["date"] <= b["end"])]
    # any expiry e with start <= e < t
    lo = np.searchsorted(exps, b["start"].values.astype("datetime64[ns]"), side="left")
    hi = np.searchsorted(exps, b["date"].values.astype("datetime64[ns]"), side="left")
    b["postexp"] = (hi > lo).astype(float)
    S["postexp"] = 0.0
    S.loc[b["index"].values, "postexp"] = b["postexp"].values
    return S


def main():
    S = basis_sample()
    S = add_postexp(S)
    r = ["H7: one-sided correction in bans (PAP §5, §11 C1-C2). Units: basis points; dm on (m_(t-1) - mu_i) by regime.",
         "Coefficients: x_r = normal reversion slope in regime r (negative = reversion); xb_r = change in a ban (delta_r).",
         "Prediction: delta_up (xb_up) > 0, delta_lo (xb_lo) <= 0. Two-way FE (stock, date); SE clustered by stock and date.", ""]
    T = thresholds(S, "m", "m_lag", "dm", "pct")
    D = design(T, "m_lag", "dm")
    main_o = estimate(D)
    r.append(fmt("MAIN (pooled 2015-2026, stock 20/80 percentiles on non-ban days, winsorised)", main_o))
    r.append(f"  share of observations by regime (non-ban): up {((D['x_up']!=0)&~D['ban']).sum()/(~D['ban']).sum():.3f}, "
             f"lo {((D['x_lo']!=0)&~D['ban']).sum()/(~D['ban']).sum():.3f}; ban obs in up {int(((D['x_up']!=0)&D['ban']).sum())}, "
             f"lo {int(((D['x_lo']!=0)&D['ban']).sum())}, mid {int(((D['x_mid']!=0)&D['ban']).sum())}")
    r.append(f"\nFamily test statistic p_H7 (C2 d) = {main_o['p_iu']:.3g}\n")
    r.append(fmt("SPEC 2: with expiry-inside-spell interaction", estimate(design(T, "m_lag", "dm", postexp=True), postexp=True)))
    r.append("\nSplits (C2 e):")
    r.append(fmt("  pre 1 Oct 2025", estimate(D[~D["post"]])))
    r.append(fmt("  post 1 Oct 2025 (44 spells; low power)", estimate(D[D["post"]])))
    r.append("\nRobustness (C2 f and PAP):")
    for lab, meth in [("fixed +/-25 bp", "fixed25"), ("per-stock threshold model (SETAR) on non-ban days", "setar"),
                      ("state-dependent: percentiles within omega_(t-1) terciles", "state")]:
        r.append(fmt("  " + lab, estimate(design(thresholds(S, "m", "m_lag", "dm", meth), "m_lag", "dm"))))
    r.append(fmt("  unwinsorised basis", estimate(design(thresholds(S, "m_vwap", "m_lag_raw", "dm_raw", "pct"), "m_lag_raw", "dm_raw"))))
    r.append(fmt("  excluding imputed ban days", estimate(D[D["ban_source"] != "imputed"])))
    r.append(fmt("  excluding carried-forward-rate rows", estimate(D[~D["r_filled"].astype(bool)])))
    S2 = S.copy(); S2["dmc"] = S2["mc"] - S2["mc_lag"]
    r.append(fmt("  close-based basis", estimate(design(thresholds(S2, "mc", "mc_lag", "dmc", "pct"), "mc_lag", "dmc"))))
    S3 = S.copy(); S3["drr"] = S3["rr"] - S3["rr_lag"]
    S3 = S3[S3["tau"] >= 7 / 365]
    r.append(fmt("  relative implied repo (tau >= 7 days; units 1e-4 per year)", estimate(design(thresholds(S3, "rr", "rr_lag", "drr", "pct"), "rr_lag", "drr"))))
    txt = "\n".join(r)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "h7_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
