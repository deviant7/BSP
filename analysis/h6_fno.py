"""H6 (primary): short-sale access (F&O entry / eligibility exit) lowers price delay and bad-news drift.
Specification: PAP §5 H6 and §11.3 C6 (a)-(k). Then the Holm correction over the primary family (PAP §7, §11 C5).
Outputs analysis/output/h6_results.txt and analysis/output/primary_family.txt.
"""
import os, sys
import numpy as np
import pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from samples import PROC, CACHE, ROOT
from inference import feols, coef_table, holm

OUT = os.path.join(ROOT, "analysis", "output")
rng = np.random.default_rng(6)
YEARS = list(range(2015, 2026))


def events():
    E = pd.read_csv(os.path.join(PROC, "fno_events.csv"), parse_dates=["date"])
    E = E[E["note"].isna()].sort_values("date")
    F = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"), parse_dates=["date"])
    days = F["date"].drop_duplicates()
    ndays = days.groupby(days.dt.year).size()
    fy = F.groupby(["symbol", F["date"].dt.year]).size().div(ndays, level=1).rename("share").reset_index()
    fy.columns = ["symbol", "year", "share"]
    ever = set(F["symbol"])
    ent = E[E["type"] == "entry"].groupby("symbol")["date"].min()
    ext = E[E["type"] == "exit"].groupby("symbol")["date"].min()
    allex = E.groupby(["symbol", "type"])["date"].apply(list)
    return ent, ext, allex, ever, fy


class Panel:
    """Matrix form of the symbol-year panel for fast Callaway-Sant'Anna estimation and stock-cluster bootstrap
    (a bootstrap draw = integer weights on stocks)."""
    def __init__(self, P, ycol, xcols):
        self.syms = pd.Index(sorted(P["symbol"].unique())); self.years = YEARS
        piv = lambda c: P.pivot_table(index="symbol", columns="year", values=c).reindex(index=self.syms, columns=YEARS).values
        self.Y = piv(ycol); self.X = [piv(c) for c in xcols]
        self.col = {y: j for j, y in enumerate(YEARS)}


def cs_att(Pm, gvec, ctl_mask, cen, w=None):
    """ATT(g,t) cells: universal base g-2, outcome regression on base-year covariates.
    gvec: cohort per stock (nan if not treated); ctl_mask(g, t) -> boolean vector of eligible controls;
    cen: first censored year per stock (inf if none); w: stock weights (bootstrap)."""
    w = np.ones(len(Pm.syms)) if w is None else w
    cells = []
    for g in sorted(set(gvec[np.isfinite(gvec)].astype(int))):
        b = g - 2
        if b not in Pm.col:
            continue
        jb = Pm.col[b]
        Xb = np.column_stack([np.ones(len(Pm.syms))] + [x[:, jb] for x in Pm.X])
        okX = np.isfinite(Xb).all(1)
        for t in YEARS:
            if t in (g - 1, b):
                continue
            jt = Pm.col[t]
            dY = Pm.Y[:, jt] - Pm.Y[:, jb]
            base = np.isfinite(dY) & okX & (w > 0)
            tr = base & (gvec == g) & (t < cen)
            ct = base & ctl_mask(g, t)
            if w[tr].sum() < 3 or w[ct].sum() < 20:
                continue
            sw = np.sqrt(w[ct])
            beta = np.linalg.lstsq(Xb[ct] * sw[:, None], dY[ct] * sw, rcond=None)[0]
            att = np.average(dY[tr] - Xb[tr] @ beta, weights=w[tr])
            cells.append((g, t, t - g, float(w[tr].sum()), float(att)))
    return cells


def aggregate(cells):
    post = [c for c in cells if c[2] >= 0]
    pre = [c for c in cells if c[2] < 0]
    w = lambda cs: (sum(c[3] * c[4] for c in cs) / sum(c[3] for c in cs)) if cs else np.nan
    ev = {}
    for c in cells:
        ev.setdefault(c[2], []).append(c)
    return w(post), w(pre), {e: (w(v), int(sum(c[3] for c in v))) for e, v in sorted(ev.items())}


def boot(Pm, gvec, ctl_mask, cen, B=499):
    n = len(Pm.syms); est = []
    for _ in range(B):
        wb = np.bincount(rng.integers(0, n, n), minlength=n).astype(float)
        est.append(aggregate(cs_att(Pm, gvec, ctl_mask, cen, wb))[0])
    est = np.array(est)
    return float(np.nanstd(est)), est


def sun_abraham(P, cohort, never, ycol):
    D = P[P["symbol"].isin(set(cohort) | never)].copy()
    D["g"] = D["symbol"].map(cohort)
    D["e"] = D["year"] - D["g"]
    D = D[~(D["e"] == -1)]                                    # transition year
    names, share = [], {}
    for g in sorted(D["g"].dropna().unique()):
        for e in sorted(D.loc[D["g"] == g, "e"].unique()):
            if e == -2:
                continue
            n = f"d_{int(g)}_{int(e)}".replace("-", "m")
            D[n] = ((D["g"] == g) & (D["e"] == e)).astype(float)
            names.append(n); share[n] = (int(g), int(e), int(((D["g"] == g) & (D["e"] == e)).sum()))
    D = D.dropna(subset=[ycol])
    names = [n for n in names if D[n].sum() > 0]
    fit = feols(D, f"{ycol} ~ " + " + ".join(names) + " | symbol + year", cluster="symbol")
    b = fit.coef(); V = np.asarray(fit._vcov); idx = list(b.index)
    post = [n for n in names if share[n][1] >= 0 and n in idx]
    w = np.zeros(len(idx))
    tot = sum(share[n][2] for n in post)
    for n in post:
        w[idx.index(n)] = share[n][2] / tot
    est = float(w @ b.values); se = float(np.sqrt(w @ V @ w))
    return est, se


def stacked_drift(A, cohort, clean_ok, base_size, ycol="bhar_w"):
    stacks = []
    for g in sorted(set(cohort.values())):
        tr = [s for s, gg in cohort.items() if gg == g]
        win = list(range(g - 4, g + 3))
        sz = [base_size.get((s, g - 2)) for s in tr]
        sz = [x for x in sz if x is not None and np.isfinite(x)]
        if len(sz) < 3:
            continue
        lo, hi = min(sz), max(sz)
        ctl = [s for s in A["symbol"].unique() if clean_ok(s, g) and lo <= base_size.get((s, g - 2), np.nan) <= hi]
        x = A[A["symbol"].isin(set(tr) | set(ctl)) & A["year"].isin(win) & (A["year"] != g - 1)].copy()
        x["stack"] = g; x["treated"] = x["symbol"].isin(tr).astype(float); x["post"] = (x["year"] >= g).astype(float)
        stacks.append(x)
    S = pd.concat(stacks, ignore_index=True)
    S["tp"] = S["treated"] * S["post"]
    S["ss"] = S["stack"].astype(str) + "_" + S["symbol"]; S["sq"] = S["stack"].astype(str) + "_" + S["q"].astype(str)
    S = S.dropna(subset=[ycol])
    t = coef_table(feols(S, f"{ycol} ~ tp | ss + sq", cluster="symbol"))
    return t.loc["tp"], int(S["treated"].sum()), S["symbol"].nunique()


def main():
    r = ["H6: F&O entry and eligibility exit (PAP §5 H6, §11.3 C6). Delay = Hou-Moskowitz D1 (calendar year);",
         "drift = BHAR[+2,+64] after bad-news announcements (bottom EAR tercile in the quarter), winsorised.", ""]
    ent, ext, allex, ever, fy = events()
    P = pd.read_pickle(os.path.join(CACHE, "delay_panel.pkl"))
    A = pd.read_pickle(os.path.join(CACHE, "event_outcomes.pkl"))
    A = A[A["bad"]].copy()
    xcols = ["log_mcap", "log_value", "vol"]
    inF = {(s, y) for s, y, sh in fy.itertuples(index=False) if sh >= 0.9}
    never = set(P["symbol"]) - ever
    base_size = {(s, y): v for s, y, v in P[["symbol", "year", "log_mcap"]].itertuples(index=False)}
    res, pvals = {}, {}

    Pm = Panel(P, "delay", xcols)
    Pv = Panel(P, "vr5", xcols)
    S = Pm.syms
    nev = S.isin(list(never))
    inF_m = {y: np.array([(s, y) in inF for s in S]) for y in YEARS}

    # ---------- entries
    coh_e = {s: d.year + 1 for s, d in ent.items() if d.year + 1 <= 2025}
    cen_e = {}
    for s in coh_e:
        later = [d for d in allex.get((s, "exit"), []) if d > ent[s]]
        if later:
            cen_e[s] = later[0].year
    g_e = np.array([coh_e.get(s, np.nan) for s in S], dtype=float)
    c_e = np.array([cen_e.get(s, np.inf) for s in S], dtype=float)
    ok_e = lambda g, t: nev | (np.nan_to_num(g_e, nan=-9) - 1 > t)
    cells = cs_att(Pm, g_e, ok_e, c_e)
    att, pre, ev = aggregate(cells)
    se, _ = boot(Pm, g_e, ok_e, c_e)
    p = float(stats.norm.cdf(att / se))
    pvals["entry_delay"] = p
    r += ["ENTRIES (Callaway-Sant'Anna, outcome regression on base-year covariates; controls never- and not-yet-treated)",
          f"  cohorts used: {sorted(set(c[0] for c in cells))}; treated stock-years in post cells: {int(sum(c[3] for c in cells if c[2] >= 0))}",
          f"  delay ATT (post) = {att:+.4f} (bootstrap se {se:.4f}); prediction < 0; one-sided p = {p:.3g}; pre-period average {pre:+.4f}",
          "  event-time profile (e: ATT, treated n): " + "; ".join(f"{e}: {v[0]:+.3f} ({v[1]})" for e, v in ev.items())]
    sa, sase = sun_abraham(P, coh_e, never, "delay")
    r.append(f"  Sun-Abraham check (never-treated reference): {sa:+.4f} (se {sase:.4f})")
    clean_e = lambda s, g: (s in never) or (s in coh_e and coh_e[s] >= g + 4)
    t, nt, ns = stacked_drift(A, coh_e, clean_e, base_size)
    p = 1 - float(stats.norm.cdf(t["b"] / t["se"]))
    pvals["entry_drift"] = p
    r.append(f"  bad-news drift (stacked DiD): Treated x Post = {t['b']:+.4f} (se {t['se']:.4f}); prediction > 0; one-sided p = {p:.3g}; "
             f"treated bad-news events {nt}, stocks in sample {ns}")
    t2, _, _ = stacked_drift(A, coh_e, clean_e, base_size, ycol="bhar")
    r.append(f"    robustness unwinsorised: {t2['b']:+.4f} (se {t2['se']:.4f})")

    # ---------- eligibility exits
    coh_x = {s: d.year + 1 for s, d in ext.items() if d.year + 1 <= 2025}
    cen_x = {}
    for s in coh_x:
        later = [d for d in allex.get((s, "entry"), []) if d > ext[s]]
        if later:
            cen_x[s] = later[0].year
    g_x = np.array([coh_x.get(s, np.nan) for s in S], dtype=float)
    c_x = np.array([cen_x.get(s, np.inf) for s in S], dtype=float)
    def ok_x(g, t):
        return inF_m[g - 2] & inF_m[t] & ~(np.nan_to_num(g_x, nan=9999) - 1 <= t)
    cells = cs_att(Pm, g_x, ok_x, c_x)
    att, pre, ev = aggregate(cells)
    se, _ = boot(Pm, g_x, ok_x, c_x)
    p = 1 - float(stats.norm.cdf(att / se))
    pvals["exit_delay"] = p
    r += ["", "ELIGIBILITY EXITS (controls: stocks in F&O in the base year and in year t that have not exited by t)",
          f"  cohorts used: {sorted(set(c[0] for c in cells))}; treated stock-years in post cells: {int(sum(c[3] for c in cells if c[2] >= 0))}",
          f"  delay ATT (post) = {att:+.4f} (bootstrap se {se:.4f}); prediction > 0; one-sided p = {p:.3g}; pre-period average {pre:+.4f}",
          "  event-time profile: " + "; ".join(f"{e}: {v[0]:+.3f} ({v[1]})" for e, v in ev.items())]
    clean_x = lambda s, g: ((s, g - 2) in inF) and not (s in coh_x and coh_x[s] < g + 4) and all((s, y) in inF for y in range(g - 2, min(g + 3, 2026)))
    t, nt, ns = stacked_drift(A, coh_x, clean_x, base_size)
    p = float(stats.norm.cdf(t["b"] / t["se"]))
    pvals["exit_drift"] = p
    r.append(f"  bad-news drift (stacked DiD): Treated x Post = {t['b']:+.4f} (se {t['se']:.4f}); prediction < 0; one-sided p = {p:.3g}; "
             f"treated bad-news events {nt}, stocks in sample {ns}")

    # ---------- robustness (C6 j)
    r += ["", "Robustness (C6 j):"]
    g2 = np.where(g_e == 2025, np.nan, g_e)
    ok2 = lambda g, t: nev | (np.nan_to_num(g_e, nan=-9) - 1 > t)
    r.append(f"  entries without the 2024 event year (29 Nov 2024 batch): delay ATT {aggregate(cs_att(Pm, g2, ok2, c_e))[0]:+.4f}")
    g3 = np.where(g_e - 2 >= 2018, g_e, np.nan)
    r.append(f"  entries with base year >= 2018 (no back-cast market caps): delay ATT {aggregate(cs_att(Pm, g3, ok_e, c_e))[0]:+.4f}")
    r.append(f"  entries, VR(5) as outcome: ATT {aggregate(cs_att(Pv, g_e, ok_e, c_e))[0]:+.4f} (efficiency: closer to 1)")
    gx2 = np.where(g_x == 2020, np.nan, g_x)
    r.append(f"  exits without the 2019 event year (28 Jun 2019 batch): delay ATT {aggregate(cs_att(Pm, gx2, ok_x, c_x))[0]:+.4f}")

    pH6 = min(1.0, 4 * min(pvals.values()))
    r += ["", "Component one-sided p-values: " + ", ".join(f"{k} {v:.3g}" for k, v in pvals.items()),
          f"Family test statistic (C6 h): p_H6 = min(1, 4 x min p) = {pH6:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h6_results.txt"), "w").write(txt + "\n")
    print(txt)

    # ---------- primary family, Holm (PAP §7)
    fam = {"H7": 1.0, "H8": float(stats.t.sf(18.11, 166)), "H3": 1.84e-24, "H6": pH6}
    H = holm(fam)
    t2 = ["Primary family {H7, H8, H3, H6}: Holm correction at 5% (PAP §7). p-values are the pre-specified family statistics",
          "(H7 analysis/output/h7_results.txt; H8 h8_results.txt, t = -18.11 with 167 stock clusters; H3 h3_results.txt; H6 above).",
          H.to_string(index=False),
          "", "Note: H3's pre-specified p ignores cross-sectional correlation; its placebo-calibrated p is about 0.05 (exploratory)."]
    open(os.path.join(OUT, "primary_family.txt"), "w").write("\n".join(t2) + "\n")
    print("\n".join(t2))


if __name__ == "__main__":
    main()
