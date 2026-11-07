"""EXPLORATORY (added 7 Nov 2026 AFTER the band chapter's noise check; logged in PAP §11.2): H7 with instrumental variables.

The band chapter found that classical noise in the daily VWAP basis inflates OLS reversion slopes toward -1. Ban days have
thinner trading, so noise could differ between ban and non-ban days and affect H7's delta coefficients. Here:
  regimes are defined by x_(t-2) (the same contract's deviation two days earlier, relative to the stock's 20th/80th
  percentiles on non-ban days, as in C2), so the classification is not driven by the noise in x_(t-1);
  dm_t = sum_r [beta_r + delta_r Ban_t] x_(t-1) 1{r} + stock FE + date FE, estimated by OLS and by 2SLS with
  x_(t-2) 1{r} and x_(t-2) 1{r} Ban_t as instruments; two-way clustered SE (stock, date).
Outputs analysis/output/h7_iv.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, ROOT
from h7_onesided import thresholds, BP

OUT = os.path.join(ROOT, "analysis", "output")
REG = ["up", "mid", "lo"]


def demean(df, cols, fes=("symbol", "date"), tol=1e-10, maxit=200):
    X = df[cols].astype(float).copy()
    g = [df[f].values for f in fes]
    codes = [pd.factorize(v)[0] for v in g]
    for it in range(maxit):
        old = X.values.copy()
        for c in codes:
            means = X.groupby(c).transform("mean")
            X = X - means
        if np.max(np.abs(X.values - old)) < tol:
            break
    return X


def cluster_vcov(Xh, u, clusters, bread):
    """Two-way (stock, date) clustered sandwich: V_s + V_d - V_sd."""
    def meat(codes):
        S = pd.DataFrame(Xh * u[:, None]).groupby(codes).sum().values
        return S.T @ S
    s, d = clusters
    sd = pd.factorize(pd.Series(s).astype(str) + "_" + pd.Series(d).astype(str))[0]
    M = meat(pd.factorize(s)[0]) + meat(pd.factorize(d)[0]) - meat(sd)
    V = bread @ M @ bread
    return V


def estimate(df, endog, instr, y="dm_bp", iv=True):
    cols = [y] + endog + instr
    D = demean(df, cols)
    Y = D[y].values
    X = D[endog].values
    Z = D[instr].values
    if iv:
        P = np.linalg.lstsq(Z, X, rcond=None)[0]
        Xh = Z @ P
    else:
        Xh = X
    b = np.linalg.solve(Xh.T @ X, Xh.T @ Y)
    u = Y - X @ b
    bread = np.linalg.inv(Xh.T @ Xh)
    V = cluster_vcov(Xh, u, (df["symbol"].values, df["date"].values), bread)
    se = np.sqrt(np.diag(V))
    out = pd.DataFrame({"b": b, "se": se}, index=endog)
    # first-stage strength: partial R2 / F for each endogenous variable (non-clustered, indicative)
    fs = {}
    if iv:
        for j, e in enumerate(endog):
            xh = Xh[:, j]; x = X[:, j]
            r2 = 1 - np.sum((x - xh) ** 2) / np.sum(x ** 2)
            fs[e] = r2
    return out, V, fs


def fmt(out, V, lab, endog):
    i_up, i_lo = endog.index("xb_up"), endog.index("xb_lo")
    d = out.loc["xb_up", "b"] - out.loc["xb_lo", "b"]
    sd = np.sqrt(V[i_up, i_up] + V[i_lo, i_lo] - 2 * V[i_up, i_lo])
    from scipy import stats
    p1 = stats.norm.sf(out.loc["xb_up", "b"] / out.loc["xb_up", "se"])
    p2 = stats.norm.sf(d / sd)
    lines = [lab] + [f"    {k:7s} {out.loc[k, 'b']:+.4f} (se {out.loc[k, 'se']:.4f}, t {out.loc[k, 'b'] / out.loc[k, 'se']:+.2f})" for k in endog]
    lines.append(f"    delta_up - delta_lo = {d:+.4f} (se {sd:.4f}); one-sided p(delta_up > 0) = {p1:.3g}; "
                 f"p(delta_up - delta_lo > 0) = {p2:.3g}; intersection-union p = {max(p1, p2):.3g}")
    return lines


def main():
    S = basis_sample()
    T = thresholds(S, "m", "m_lag", "dm", "pct")
    # x_(t-2): same contract two days back = the m_lag of the same contract's row on day t-1
    L = S[["symbol", "expiry", "i", "m_lag"]].copy()
    L["i"] += 1
    L = L.rename(columns={"m_lag": "m_lag2"})
    T = T.merge(L, on=["symbol", "expiry", "i"], how="left")
    T = T.dropna(subset=["dm", "m_lag", "m_lag2"]).copy()
    T["x1"] = (T["m_lag"] - T["mu"]) * BP
    T["x2"] = (T["m_lag2"] - T["mu"]) * BP
    T["dm_bp"] = T["dm"] * BP
    reg2 = np.where(T["m_lag2"] > T["gU"], "up", np.where(T["m_lag2"] < T["gL"], "lo", "mid"))
    ban = T["ban"].astype(float).values
    endog, instr = [], []
    for r in REG:
        I = (reg2 == r).astype(float)
        T[f"x_{r}"] = T["x1"] * I; T[f"xb_{r}"] = T["x1"] * I * ban
        T[f"z_{r}"] = T["x2"] * I; T[f"zb_{r}"] = T["x2"] * I * ban
        endog += [f"x_{r}", f"xb_{r}"]; instr += [f"z_{r}", f"zb_{r}"]
    endog = [f"x_{r}" for r in REG] + [f"xb_{r}" for r in REG]
    instr = [f"z_{r}" for r in REG] + [f"zb_{r}" for r in REG]
    r = ["EXPLORATORY: H7 with regimes defined by x_(t-2) and x_(t-1) instrumented by x_(t-2) (PAP §11.2). Units bp.",
         f"Observations {len(T)}, stocks {T['symbol'].nunique()}, ban days {int(T['ban'].sum())}; regime shares (by x_(t-2)): " +
         ", ".join(f"{k} {(reg2 == k).mean():.3f}" for k in REG), ""]
    o, V, _ = estimate(T, endog, instr, iv=False)
    r += fmt(o, V, "OLS (same sample, regimes by x_(t-2)):", endog)
    o, V, fs = estimate(T, endog, instr, iv=True)
    r += fmt(o, V, "2SLS (x_(t-1) terms instrumented by x_(t-2) terms):", endog)
    r.append("    first-stage R2 (within, indicative): " + ", ".join(f"{k} {v:.3f}" for k, v in fs.items()))
    for lab, a, z in [("end-of-day enforcement (to 22 Mar 2020)", "2015-01-01", "2020-03-23"),
                      ("peak-intraday enforcement (23 Mar 2020 to 30 Sep 2025)", "2020-03-23", "2025-10-01")]:
        Tm = T[(T["date"] >= a) & (T["date"] < z)]
        o, V, _ = estimate(Tm, endog, instr, iv=True)
        r += fmt(o, V, f"2SLS, {lab}:", endog)
    txt = "\n".join(r)
    open(os.path.join(OUT, "h7_iv.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
