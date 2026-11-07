"""Secondary: H9, anticipation below 95% and the position-limit regime changes. Specification: PAP §11.8 C11.

Part A: upper/lower exceedances and level of the basis by omega_(t-1) bins on non-ban days (2015 to Sep 2025).
Part B: 1 Oct 2025 MWPL formula change, continuous intensity I_i = -ln(MWPL_new/MWPL_old).
Part C: stacked quarterly MWPL resets (1 Jan, 1 Apr, 1 Jul 2026).
Outputs analysis/output/h9_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, PROC, ROOT
from inference import feols, coef_table

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
BP = 1e4
EDGES = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]


def thresholds(S):
    nb = S[(S["date"] < REFORM) & ~S["ban"] & (S["omega_lag"] < 0.60)]
    cnt = nb.groupby("symbol").size()
    nb = nb[nb["symbol"].isin(cnt[cnt >= 100].index)]
    q = nb.groupby("symbol")["m"].quantile([0.2, 0.5, 0.8]).unstack()
    q.columns = ["q20", "q50", "q80"]
    return q


def outcomes(S, q):
    S = S.merge(q, left_on="symbol", right_index=True, how="inner")
    S["U"] = (S["m"] > S["q80"]).astype(float)
    S["L"] = (S["m"] < S["q20"]).astype(float)
    S["lev"] = (S["m"] - S["q50"]) * BP
    return S


def p1(t, name, sign=">"):
    b, p = t.loc[name, "b"], t.loc[name, "p_two"]
    return p / 2 if (b > 0) == (sign == ">") else 1 - p / 2


def part_a(S, r):
    A = S[(S["date"] < REFORM) & ~S["ban"] & S["omega_lag"].notna() & (S["omega_lag"] < 0.95)].copy()
    A["bin"] = pd.cut(A["omega_lag"], [-1] + EDGES, right=False, labels=["ref"] + [f"{e:.2f}" for e in EDGES[:-1]])
    for e in EDGES[:-1]:
        A[f"b{int(e * 100)}"] = (A["bin"] == f"{e:.2f}").astype(int)
    dums = " + ".join(f"b{int(e * 100)}" for e in EDGES[:-1])
    r += ["PART A: anticipation on non-ban days, 2015 to Sep 2025 (thresholds from each stock's days with omega < 0.60)",
          f"  stock-days {len(A)}, stocks {A['symbol'].nunique()}; by bin: " +
          ", ".join(f"{k} {v}" for k, v in A["bin"].value_counts(sort=False).items())]
    r.append("  Descriptive percentiles of m - q50_i (bp) by omega_(t-1) bin:")
    desc = A.groupby("bin", observed=True)["lev"].quantile([0.2, 0.5, 0.8]).unstack().round(2)
    desc["share U"] = A.groupby("bin", observed=True)["U"].mean().round(3)
    desc["share L"] = A.groupby("bin", observed=True)["L"].mean().round(3)
    r += ["    " + x for x in desc.to_string().split("\n")]
    for y, nm in [("U", "upper exceedance U"), ("L", "lower exceedance L"), ("lev", "level m - q50 (bp)")]:
        t = coef_table(feols(A, f"{y} ~ {dums} | symbol + date"))
        r.append(f"  {nm}: bin coefficients vs omega < 0.60 (stock and date FE): " +
                 "; ".join(f"[{e:.2f}) {t.loc[f'b{int(e * 100)}', 'b']:+.4f} ({t.loc[f'b{int(e * 100)}', 'se']:.4f})" for e in EDGES[:-1]))
    Z = A[A["omega_lag"] >= 0.60]
    out = {}
    for y in ["U", "L", "lev"]:
        t = coef_table(feols(Z, f"{y} ~ omega_lag | symbol + date"))
        out[y] = t.loc["omega_lag"]
        r.append(f"  slope of {y} on omega_(t-1) in [0.60, 0.95): {t.loc['omega_lag', 'b']:+.4f} (se {t.loc['omega_lag', 'se']:.4f}); "
                 f"one-sided p(> 0) = {p1(t, 'omega_lag'):.3g}; n {len(Z)}")
    pA = p1(coef_table(feols(Z, "U ~ omega_lag | symbol + date")), "omega_lag")
    r.append(f"  TEST STATISTIC A: one-sided p (slope of U > 0) = {pA:.3g}")
    return pA


def panel_treat():
    days, pos = calendar()
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl", "oi", "futeq_oi", "util",
                                                                          "util_futeq"], parse_dates=["date"])
    P["omega"] = np.where(P["date"] >= REFORM, P["util_futeq"], P["util"])
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["ban"] = 1.0
    P = P.merge(B[["date", "symbol", "ban"]], on=["date", "symbol"], how="left")
    P["ban"] = P["ban"].fillna(0.0)
    return P


def part_b(S, q, P, r):
    a = P[P["date"] == "2025-09-30"].set_index("symbol")
    b = P[P["date"] == "2025-10-01"].set_index("symbol")
    j = a.join(b, lsuffix="_o", rsuffix="_n", how="inner")
    I = (-np.log(j["mwpl_n"] / j["mwpl_o"])).rename("I")
    Pp = (np.log(j["futeq_oi_n"] / j["oi_n"]) + I).rename("Pint")
    r += ["", f"PART B: 1 Oct 2025 MWPL formula. Stocks {len(I)}; I = -ln(new/old): median {I.median():.3f}, "
              f"range {I.min():.3f} to {I.max():.3f}; predicted d ln(util) P: median {Pp.median():.3f}, sd {Pp.std():.3f}; "
              f"corr(I, P) {np.corrcoef(I, Pp.reindex(I.index))[0, 1]:.3f}"]
    lo, hi = pd.Timestamp("2025-07-01"), pd.Timestamp("2025-12-31")
    Sb = S[(S["date"] >= lo) & (S["date"] <= hi) & S["symbol"].isin(I.index)].copy()
    Sb = outcomes(Sb, q)
    Sb = Sb.join(I, on="symbol").join(Pp, on="symbol")
    Sb["post"] = (Sb["date"] >= REFORM).astype(float)
    Sb["postI"] = Sb["post"] * Sb["I"]; Sb["postP"] = Sb["post"] * Sb["Pint"]
    Tb = P[(P["date"] >= lo) & (P["date"] <= hi) & P["symbol"].isin(I.index)].join(I, on="symbol").join(Pp, on="symbol")
    Tb["post"] = (Tb["date"] >= REFORM).astype(float)
    Tb["postI"] = Tb["post"] * Tb["I"]; Tb["postP"] = Tb["post"] * Tb["Pint"]
    r.append(f"  window 1 Jul to 31 Dec 2025: basis stock-days {len(Sb)} (stocks {Sb['symbol'].nunique()}); treatment-side stock-days {len(Tb)}")
    pB = None
    for nm, d, y in [("utilisation omega_t (first stage)", Tb, "omega"), ("in a ban", Tb, "ban"),
                     ("upper exceedance U", Sb, "U"), ("lower exceedance L", Sb, "L"), ("level m - q50 (bp)", Sb, "lev")]:
        t = coef_table(feols(d.dropna(subset=[y]), f"{y} ~ postI | symbol + date"))
        r.append(f"  {nm:36s} Post x I: {t.loc['postI', 'b']:+.4f} (se {t.loc['postI', 'se']:.4f}, t {t.loc['postI', 't']:+.2f}); "
                 f"one-sided p(> 0) = {p1(t, 'postI'):.3g}")
        if y == "U":
            pB = p1(t, "postI")
    r.append(f"  TEST STATISTIC B: one-sided p (Post x I > 0 for U) = {pB:.3g}")
    r.append("  Robustness:")
    for nm, d, y, x in [("U with predicted utilisation P", Sb, "U", "postP"), ("ban with P", Tb, "ban", "postP"),
                        ("U non-ban days only", Sb[~Sb["ban"]], "U", "postI"),
                        ("level non-ban days only", Sb[~Sb["ban"]], "lev", "postI")]:
        t = coef_table(feols(d.dropna(subset=[y, x]), f"{y} ~ {x} | symbol + date"))
        r.append(f"    {nm:34s} {t.loc[x, 'b']:+.4f} (se {t.loc[x, 'se']:.4f}, t {t.loc[x, 't']:+.2f})")
    # extended window to 31 Mar 2026
    hi2 = pd.Timestamp("2026-03-31")
    Se = outcomes(S[(S["date"] >= lo) & (S["date"] <= hi2) & S["symbol"].isin(I.index)].copy(), q).join(I, on="symbol")
    Se["postI"] = (Se["date"] >= REFORM).astype(float) * Se["I"]
    Te = P[(P["date"] >= lo) & (P["date"] <= hi2) & P["symbol"].isin(I.index)].join(I, on="symbol")
    Te["postI"] = (Te["date"] >= REFORM).astype(float) * Te["I"]
    for nm, d, y in [("U, window to 31 Mar 2026", Se, "U"), ("level, window to 31 Mar 2026", Se, "lev"),
                     ("ban, window to 31 Mar 2026", Te, "ban")]:
        t = coef_table(feols(d.dropna(subset=[y]), f"{y} ~ postI | symbol + date"))
        r.append(f"    {nm:34s} {t.loc['postI', 'b']:+.4f} (se {t.loc['postI', 'se']:.4f}, t {t.loc['postI', 't']:+.2f})")
    # monthly event study, September = reference
    Sb["mon"] = Sb["date"].dt.month
    Tb["mon"] = Tb["date"].dt.month
    for nm, d, y in [("U", Sb, "U"), ("ban", Tb, "ban"), ("level", Sb, "lev")]:
        d = d.copy()
        cols = []
        for mth in [7, 8, 10, 11, 12]:
            d[f"m{mth}"] = (d["mon"] == mth).astype(float) * d["I"]; cols.append(f"m{mth}")
        t = coef_table(feols(d.dropna(subset=[y]), f"{y} ~ {' + '.join(cols)} | symbol + date"))
        r.append(f"    monthly event study {nm:6s} (x I; Sep = 0): " +
                 "; ".join(f"{c[1:]}: {t.loc[c, 'b']:+.3f} ({t.loc[c, 'se']:.3f})" for c in cols))
    return pB


def part_c(S, q, P, r):
    days, pos = calendar()
    r += ["", "PART C: stacked quarterly MWPL resets (1 Jan, 1 Apr, 1 Jul 2026), window +/-30 trading days; intensity -ln(after/before)"]
    stacks_s, stacks_t = [], []
    for R in ["2026-01-01", "2026-04-01", "2026-07-01"]:
        R = pd.Timestamp(R)
        iR = days.searchsorted(R)
        before = P[P["date"] == days[iR - 1]].set_index("symbol")["mwpl"]
        after = P[P["date"] == days[iR]].set_index("symbol")["mwpl"]
        I = (-np.log(after / before)).dropna().rename("I")
        lo, hi = days[max(0, iR - 30)], days[min(len(days) - 1, iR + 29)]
        s = outcomes(S[(S["date"] >= lo) & (S["date"] <= hi) & S["symbol"].isin(I.index)].copy(), q).join(I, on="symbol")
        t = P[(P["date"] >= lo) & (P["date"] <= hi) & P["symbol"].isin(I.index)].join(I, on="symbol")
        for d in (s, t):
            d["stack"] = R.strftime("%Y%m")
            d["postI"] = (d["date"] >= R).astype(float) * d["I"]
            d["sk_sym"] = d["stack"] + "_" + d["symbol"]
            d["sk_date"] = d["stack"] + "_" + d["date"].astype(str)
        stacks_s.append(s); stacks_t.append(t)
        r.append(f"  {R.date()}: stocks {len(I)}, intensity median {I.median():+.3f}, p10 {I.quantile(.1):+.3f}, p90 {I.quantile(.9):+.3f}")
    Ss, Ts = pd.concat(stacks_s), pd.concat(stacks_t)
    for nm, d, y in [("utilisation (first stage)", Ts, "omega"), ("in a ban", Ts, "ban"), ("upper exceedance U", Ss, "U"),
                     ("lower exceedance L", Ss, "L"), ("level m - q50 (bp)", Ss, "lev")]:
        t = coef_table(feols(d.dropna(subset=[y]), f"{y} ~ postI | sk_sym + sk_date", cluster="symbol+date"))
        r.append(f"  {nm:30s} Post x intensity: {t.loc['postI', 'b']:+.4f} (se {t.loc['postI', 'se']:.4f}, t {t.loc['postI', 't']:+.2f})")


def main():
    S = basis_sample()
    q = thresholds(S)
    r = ["H9: anticipation and position-limit regime (PAP §11.8 C11). Secondary; p-values unadjusted. SE two-way clustered "
         "(stock, date).", ""]
    Sx = outcomes(S.copy(), q)
    pA = part_a(Sx, r)
    P = panel_treat()
    pB = part_b(S, q, P, r)
    part_c(S, q, P, r)
    r += ["", f"Summary: test A p = {pA:.3g}; test B p = {pB:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h9_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
