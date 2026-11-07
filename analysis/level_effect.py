"""Secondary test: the level effect of a ban (PAP §6 first bullet; model Prop. 6). Specification: PAP §11.4 C7.

Stacked ban-entry event study. Treated: ban spells (day 0 = first ban day) with no ban on days -5..-1, omega_(t-1) > 0.95
and a valid basis on day -1. Controls: other stocks' stock-days in the same calendar week with omega_(s-1) in
[0.85, 0.95), no ban on s-5..s+5 and a valid basis on s-1; up to 5 nearest neighbours (Mahalanobis on omega days -1..-5
and m_(-1)). Outcome: y_k = m_(t0+k) - m_(t0-1); D_k = treated minus mean control; D = mean of D_k over the in-ban days
k = 0..min(4, L-1). Prediction: D lower for C > 0 (rising OI before entry = new exposure) than for C <= 0.

Outputs analysis/output/level_effect_results.txt (and level_effect_events.csv.gz with one row per event).
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, calendar, treatment, PROC, ROOT
from inference import feols, coef_table, lincomb

OUT = os.path.join(ROOT, "analysis", "output")
BP = 1e4
REFORM = pd.Timestamp("2025-10-01")
INTRADAY = pd.Timestamp("2020-03-23")
KMIN, KMAX = -20, 20
NN = 5


def wide(S, col, syms, n_days):
    W = np.full((len(syms), n_days), np.nan)
    r = S["symbol"].map({s: j for j, s in enumerate(syms)}).values
    W[r, S["i"].values] = S[col].values * BP
    return W


def build():
    days, pos = calendar()
    nT = len(days)
    S = basis_sample()
    A = futures_activity()
    lag, B = treatment(days, pos)
    syms = sorted(set(S["symbol"]) | set(lag["symbol"]))
    sid = {s: j for j, s in enumerate(syms)}
    M = {c: wide(S, c, syms, nT) for c in ["m", "m_vwap", "rr", "mc"]}
    # omega_(t-1) attached to day t (from the previous trading day's file)
    OM = np.full((len(syms), nT + 1), np.nan)
    lg = lag[lag["i"].between(0, nT)].dropna(subset=["i"])
    OM[lg["symbol"].map(sid).values, lg["i"].astype(int).values] = lg["omega_lag"].values
    OM = OM[:, :nT]
    BAN = np.zeros((len(syms), nT), bool)
    B["i"] = B["date"].map(pos)
    B = B.dropna(subset=["i"])
    BAN[B["symbol"].map(sid).values, B["i"].astype(int).values] = True
    IMP = np.zeros((len(syms), nT), bool)
    Bi = B[B["ban_source"] == "imputed"]
    IMP[Bi["symbol"].map(sid).values, Bi["i"].astype(int).values] = True
    # futures activity for the composition ratio
    A["i"] = A["date"].map(pos)
    DOI = np.full((len(syms), nT), np.nan); VOL = np.full((len(syms), nT), np.nan)
    a = A[A["symbol"].isin(sid)]
    DOI[a["symbol"].map(sid).values, a["i"].values] = a["d_oi"].values
    VOL[a["symbol"].map(sid).values, a["i"].values] = a["vol"].values
    return dict(days=days, pos=pos, syms=syms, sid=sid, M=M, OM=OM, BAN=BAN, IMP=IMP, DOI=DOI, VOL=VOL)


def omega_path(D, j, i):
    """omega on days -1..-5 relative to day i = omega_lag attached to days i, i-1, ..., i-4."""
    if i - 4 < 0:
        return None
    return D["OM"][j, i - 4:i + 1][::-1]


def events(D, post):
    sp = pd.read_csv(os.path.join(PROC, "ban_spells.csv.gz"), parse_dates=["start", "end"])
    sp = sp[sp["start"] >= "2015-01-01"]
    sp = sp[(sp["start"] >= REFORM) if post else (sp["start"] < REFORM)]
    pos = D["pos"]
    rows, log = [], {"spells": len(sp)}
    drop = {"ban in -5..-1": 0, "omega <= 0.95": 0, "no basis on -1": 0, "missing omega path": 0}
    for r in sp.itertuples():
        j, i0, i1 = D["sid"].get(r.symbol), pos[r.start], pos[r.end]
        if j is None or i0 < 25:
            continue
        if D["BAN"][j, i0 - 5:i0].any():
            drop["ban in -5..-1"] += 1; continue
        if not D["OM"][j, i0] > 0.95:
            drop["omega <= 0.95"] += 1; continue
        if np.isnan(D["M"]["m"][j, i0 - 1]):
            drop["no basis on -1"] += 1; continue
        w = omega_path(D, j, i0)
        if w is None or np.isnan(w).any():
            drop["missing omega path"] += 1; continue
        vol = np.nansum(D["VOL"][j, i0 - 5:i0]); doi = np.nansum(D["DOI"][j, i0 - 5:i0])
        C = doi / vol if vol > 0 else np.nan
        rows.append(dict(symbol=r.symbol, j=j, i0=i0, L=i1 - i0 + 1, date=r.start, C=C,
                         x=np.r_[w, D["M"]["m"][j, i0 - 1]],
                         imputed=D["IMP"][j, i0:i0 + 5].any()))
    log.update(drop)
    return pd.DataFrame(rows), log


def candidates(D, post):
    """Control stock-days (j, s) per C7 (c)."""
    days = D["days"]
    lo = np.searchsorted(days, REFORM) if post else 25
    hi = len(days) if post else np.searchsorted(days, REFORM)
    J, I = np.where((D["OM"] >= 0.85) & (D["OM"] < 0.95) & ~D["BAN"])
    keep = (I >= lo) & (I < hi)
    J, I = J[keep], I[keep]
    rows = []
    nT = len(days)
    for j, s in zip(J, I):
        if D["BAN"][j, max(0, s - 5):min(nT, s + 6)].any():
            continue
        if np.isnan(D["M"]["m"][j, s - 1]):
            continue
        w = omega_path(D, j, s)
        if w is None or np.isnan(w).any():
            continue
        rows.append(dict(j=j, s=s, date=days[s], x=np.r_[w, D["M"]["m"][j, s - 1]]))
    Cd = pd.DataFrame(rows)
    Cd["wk"] = Cd["date"].dt.to_period("W")
    return Cd


def match(E, Cd, same_day=False):
    X = np.vstack(Cd["x"].values)
    Vi = np.linalg.pinv(np.cov(X, rowvar=False))
    by = Cd.groupby("date" if same_day else "wk").indices
    out = []
    for r in E.itertuples():
        key = r.date if same_day else r.date.to_period("W")
        idx = by.get(key)
        if idx is None:
            out.append(np.array([], int)); continue
        idx = idx[Cd["j"].values[idx] != r.j]
        if len(idx) == 0:
            out.append(np.array([], int)); continue
        dx = X[idx] - r.x
        d2 = np.einsum("ij,jk,ik->i", dx, Vi, dx)
        out.append(idx[np.argsort(d2)[:NN]])
    return out


def paths(D, E, Cd, M_idx, col):
    """D_k for k = KMIN..KMAX per event (treated minus mean control change from day -1)."""
    Mx = D["M"][col]
    nT = Mx.shape[1]
    ks = np.arange(KMIN, KMAX + 1)
    out = np.full((len(E), len(ks)), np.nan)
    cj, cs = Cd["j"].values, Cd["s"].values
    for e, r in enumerate(E.itertuples()):
        idx = M_idx[e]
        if len(idx) == 0:
            continue
        ii = r.i0 + ks
        ok = (ii >= 0) & (ii < nT)
        yt = np.full(len(ks), np.nan)
        yt[ok] = Mx[r.j, ii[ok]] - Mx[r.j, r.i0 - 1]
        yc = np.full((len(idx), len(ks)), np.nan)
        for q, c in enumerate(idx):
            si = cs[c] + ks
            okc = (si >= 0) & (si < nT)
            yc[q, okc] = Mx[cj[c], si[okc]] - Mx[cj[c], cs[c] - 1]
        with np.errstate(all="ignore"):
            out[e] = yt - np.nanmean(yc, axis=0)
    return ks, out


def main_stat(E, ks, P):
    k0 = np.where(ks == 0)[0][0]
    Dm = np.full(len(E), np.nan)
    for e, L in enumerate(E["L"].values):
        seg = P[e, k0:k0 + min(5, L)]
        if np.isfinite(seg).any():
            Dm[e] = np.nanmean(seg)
    return Dm


def regress(E, rhs):
    d = E.dropna(subset=["D"] + [c for c in rhs if c != "1"]).copy()
    d["date_c"] = d["date"].astype(str)
    fit = feols(d, f"D ~ {' + '.join(rhs)}", cluster="symbol+date_c")
    return fit, coef_table(fit), d


def fmt_b(t, name):
    return f"{t.loc[name, 'b']:+.2f} (se {t.loc[name, 'se']:.2f}, t {t.loc[name, 't']:+.2f})"


def analyse(E, lab):
    r = []
    E = E.copy()
    E["new"] = (E["C"] > 0).astype(int)
    E["high"] = (E["C"] > E["C"].median()).astype(int)
    E["Cz"] = (E["C"] - E["C"].mean()) / E["C"].std()
    d = E.dropna(subset=["D"])
    r.append(f"{lab}: events with D: {len(d)} (stocks {d['symbol'].nunique()}); C <= 0: {int((d['new'] == 0).sum())}, "
             f"C > 0: {int((d['new'] == 1).sum())}")
    if len(d) < 20:
        r.append("  too few events for regressions; group means only: "
                 + "; ".join(f"C<=0 {g.mean():+.2f} (n={len(g)})" if k == 0 else f"C>0 {g.mean():+.2f} (n={len(g)})"
                             for k, g in d.groupby("new")["D"]))
        return r, None
    fit, t, _ = regress(E, ["new"])
    b_new, se_new = lincomb(fit, {"Intercept": 1.0, "new": 1.0})
    p_one = t.loc["new", "p_two"] / 2 if t.loc["new", "b"] < 0 else 1 - t.loc["new", "p_two"] / 2
    r += [f"  all events: mean D {d['D'].mean():+.2f} bp, median {d['D'].median():+.2f}",
          f"  pre-specified split: mean D, C <= 0 (closing): {fmt_b(t, 'Intercept')}; C > 0 (new exposure): "
          f"{b_new:+.2f} (se {se_new:.2f}, t {b_new / se_new:+.2f})",
          f"    difference (C > 0) - (C <= 0): {fmt_b(t, 'new')}; one-sided p (difference < 0) = {p_one:.3g}"]
    fit2, t2, _ = regress(E, ["high"])
    b_hi, se_hi = lincomb(fit2, {"Intercept": 1.0, "high": 1.0})
    p2 = t2.loc["high", "p_two"] / 2 if t2.loc["high", "b"] < 0 else 1 - t2.loc["high", "p_two"] / 2
    r += [f"  median split (median C {E['C'].median():.3f}): low C {fmt_b(t2, 'Intercept')}; high C {b_hi:+.2f} "
          f"(se {se_hi:.2f}); difference {fmt_b(t2, 'high')}; one-sided p = {p2:.3g}"]
    _, t3, _ = regress(E, ["Cz"])
    p3 = t3.loc["Cz", "p_two"] / 2 if t3.loc["Cz", "b"] < 0 else 1 - t3.loc["Cz", "p_two"] / 2
    r.append(f"  slope on standardised C: {fmt_b(t3, 'Cz')}; one-sided p (slope < 0) = {p3:.3g}; "
             f"intercept (D at mean C) {fmt_b(t3, 'Intercept')}")
    return r, p_one


def profile(E, ks, P, lab):
    r = [f"  event-time profile ({lab}): mean D_k (bp) with two-way clustered se; n events with D_k"]
    E = E.copy()
    line = []
    for q, k in enumerate(ks):
        E["D"] = P[:, q]
        d = E.dropna(subset=["D"])
        if len(d) < 20:
            continue
        if k == -1:
            line.append(f"k=-1: 0 by construction")
            continue
        _, t, _ = regress(E, ["1"])
        line.append(f"k={k:+d}: {t.loc['Intercept', 'b']:+.2f} ({t.loc['Intercept', 'se']:.2f}) n={len(d)}")
    for a in range(0, len(line), 4):
        r.append("    " + "; ".join(line[a:a + 4]))
    return r


def run(D, post, r):
    lab = "POST-REFORM (from 1 Oct 2025; descriptive)" if post else "PRE-REFORM (2015 to Sep 2025)"
    E, log = events(D, post)
    Cd = candidates(D, post)
    r += ["", "=" * 100, lab, f"  spells: {log['spells']}; dropped: " + ", ".join(f"{k} {v}" for k, v in log.items() if k != "spells"),
          f"  usable events: {len(E)}; candidate control stock-days: {len(Cd)}"]
    if len(E) == 0 or len(Cd) == 0:
        return None
    Mi = match(E, Cd)
    nc = np.array([len(x) for x in Mi])
    r.append(f"  events with >= 1 control: {int((nc > 0).sum())} (mean controls per matched event {nc[nc > 0].mean():.2f}); "
             f"distinct control stock-days used {len(set(np.concatenate([x for x in Mi if len(x)])))}")
    X = np.vstack(E["x"].values)
    Xc = np.vstack([Cd["x"].values[x].mean(axis=0) if len(x) else np.full(6, np.nan) for x in Mi])
    with np.errstate(all="ignore"):
        r.append("  balance (treated mean / matched-control mean): omega_-1 {:.3f}/{:.3f}, omega_-5 {:.3f}/{:.3f}, m_-1 {:.1f}/{:.1f} bp".format(
            X[nc > 0, 0].mean(), np.nanmean(Xc[:, 0]), X[nc > 0, 4].mean(), np.nanmean(Xc[:, 4]),
            X[nc > 0, 5].mean(), np.nanmean(Xc[:, 5])))
    ks, P = paths(D, E, Cd, Mi, "m")
    E["D"] = main_stat(E, ks, P)
    res, p = analyse(E, "MAIN (winsorised basis, in-ban days k=0..min(4,L-1))")
    r += res
    r += profile(E, ks, P, "all events")
    out_events = E.drop(columns=["x"]).copy()
    if post:
        return None
    # robustness
    r += ["", "  ROBUSTNESS (pre-specified, C7 g)"]
    for col, nm in [("m_vwap", "unwinsorised basis"), ("rr", "relative implied repo"), ("mc", "close-based basis")]:
        _, Pc = paths(D, E, Cd, Mi, col)
        Ec = E.copy(); Ec["D"] = main_stat(Ec, ks, Pc)
        r += ["  " + x for x in analyse(Ec, nm)[0]]
    Ms = match(E, Cd, same_day=True)
    _, Ps = paths(D, E, Cd, Ms, "m")
    Es = E.copy(); Es["D"] = main_stat(Es, ks, Ps)
    r += ["  " + x for x in analyse(Es, "same-day controls only")[0]]
    Ei = E[~E["imputed"]].copy()
    r += ["  " + x for x in analyse(Ei, "excluding events with imputed ban days in k=0..4")[0]]
    # exploratory: enforcement regimes
    r += ["", "  EXPLORATORY (C7 g): enforcement regimes"]
    for nm, msk in [("end-of-day checks (to 22 Mar 2020)", E["date"] < INTRADAY),
                    ("peak-intraday checks (23 Mar 2020 to 30 Sep 2025)", E["date"] >= INTRADAY)]:
        r += ["  " + x for x in analyse(E[msk].copy(), nm)[0]]
    r += exploratory(E, ks, P, Xc)
    out_events.to_csv(os.path.join(OUT, "level_effect_events.csv.gz"), index=False)
    return p


def exploratory(E, ks, P, Xc):
    """EXPLORATORY (added 7 Nov 2026 AFTER the pre-specified level-effect results were seen; logged in PAP §11.2).
    (1) baseline = mean of D_k over k = -10..-2 instead of day -1 (the treated basis dips on day -1, the day utilisation
    crosses 95%); (2) control for the day -1 basis gap between treated and matched controls (matching left treated
    10 bp lower); (3) event-time paths by median-C group."""
    r = ["", "  EXPLORATORY (added after the pre-specified results were seen; PAP §11.2)"]
    E = E.copy()
    kb = (ks >= -10) & (ks <= -2)
    with np.errstate(all="ignore"):
        base = np.nanmean(P[:, kb], axis=1)
    Ealt = E.copy(); Ealt["D"] = E["D"] - base
    r += ["  " + x for x in analyse(Ealt, "(1) baseline = mean over k=-10..-2")[0]]
    E["gap"] = np.vstack(E["x"].values)[:, 5] - Xc[:, 5]
    for rhs in (["new", "gap"], ["high", "gap"], ["Cz", "gap"]):
        E2 = E.copy()
        E2["new"] = (E2["C"] > 0).astype(int); E2["high"] = (E2["C"] > E2["C"].median()).astype(int)
        E2["Cz"] = (E2["C"] - E2["C"].mean()) / E2["C"].std()
        _, t, d = regress(E2, rhs)
        r.append(f"  (2) D ~ {' + '.join(rhs)} (n={len(d)}): {rhs[0]} {fmt_b(t, rhs[0])}; gap {fmt_b(t, 'gap')}; "
                 f"intercept {fmt_b(t, 'Intercept')}")
    r.append(f"      corr(C, gap) = {E[['C', 'gap']].corr().iloc[0, 1]:.3f}; mean gap {E['gap'].mean():.2f} bp")
    hi = (E["C"] > E["C"].median()).values
    sel = [-10, -5, -2, 0, 1, 2, 3, 4, 7, 10, 15, 20]
    for nm, msk in (("low C", ~hi), ("high C", hi)):
        with np.errstate(all="ignore"):
            vals = [f"{k:+d}: {np.nanmean(P[msk, list(ks).index(k)]):+.1f}" for k in sel]
        r.append(f"  (3) mean D_k, {nm} (n={int(msk.sum())}): " + "; ".join(vals))
    return r


def main():
    D = build()
    r = ["Level effect of bans (secondary; PAP §6, §11.4 C7). Units: bp. D = treated minus matched-control change in the",
         "basis level from day -1, averaged over in-ban days k = 0..min(4, L-1). Prediction (Prop. 6): D lower when OI was",
         "rising before entry (C > 0, new exposure) than when falling (C <= 0, closing); expected sign + for closing, - for",
         "strong new demand. SEs two-way clustered by stock and event date."]
    p = run(D, False, r)
    run(D, True, r)
    r += ["", f"Secondary test statistic (C7 f): one-sided p that D(C>0) - D(C<=0) < 0, pre-reform: {p:.3g} (unadjusted)"]
    txt = "\n".join(r)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "level_effect_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
