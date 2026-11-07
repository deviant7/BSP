"""Secondary (supporting): regression discontinuity at the 95% trigger. Specification: PAP §11.6 C9.

Units: stock-days t (2015 to Sep 2025) with the stock not in a ban on t-1; running variable omega_(t-1); cutoff 0.95.
Outputs analysis/output/rd_95.txt.
"""
import os, sys, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, calendar, PROC, ROOT

warnings.filterwarnings("ignore")
OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
INTRADAY = pd.Timestamp("2020-03-23")
BP = 1e4
C = 0.95


def frame():
    days, pos = calendar()
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl", "util", "util_futeq"],
                    parse_dates=["date"])
    P["omega"] = np.where(P["date"] >= REFORM, P["util_futeq"], P["util"])
    P["d"] = P["date"].map(pos)
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["i"] = B["date"].map(pos)
    ban = set(zip(B["symbol"], B["i"]))
    P = P.sort_values(["symbol", "d"])
    P["mwpl_chg"] = P.groupby("symbol")["mwpl"].diff().fillna(0) != 0
    F = pd.DataFrame({"symbol": P["symbol"].values, "i": P["d"].values + 1, "x": P["omega"].values,
                      "mwpl_chg": P["mwpl_chg"].values})
    F = F[F["i"] < len(days)]
    F["date"] = days[F["i"].values]
    F["ban_prev"] = [(s, i - 1) in ban for s, i in zip(F["symbol"], F["i"])]
    F["ban"] = [(s, i) in ban for s, i in zip(F["symbol"], F["i"])]
    F = F[~F["ban_prev"] & F["x"].notna()]
    S = basis_sample()
    keep = ["symbol", "i", "m", "dm", "mc", "rr"]
    T = S[keep].copy()
    for c in ["m", "dm", "mc", "rr"]:
        T[c] = T[c] * BP
    F = F.merge(T, on=["symbol", "i"], how="left")
    F["valid"] = F["m"].notna().astype(float)
    for lag in (1, 2):
        L = S[["symbol", "i", "m"]].copy(); L["i"] += lag; L["m"] *= BP
        F = F.merge(L.rename(columns={"m": f"m_l{lag}"}), on=["symbol", "i"], how="left")
    A = futures_activity()
    A["i"] = A["date"].map(pos)
    A["ly_fut"] = np.log1p(A["vol"]); A["ly_cash"] = np.log1p(A["S_qty"])
    Ak = A[["symbol", "i", "ly_fut", "ly_cash", "R", "deliv_share", "expiry_day"]]
    F = F.merge(Ak, on=["symbol", "i"], how="left")
    L2 = Ak[["symbol", "i", "ly_fut"]].copy(); L2["i"] += 2
    F = F.merge(L2.rename(columns={"ly_fut": "ly_fut_l2"}), on=["symbol", "i"], how="left")
    for c in ["ly_fut", "ly_cash", "R", "deliv_share"]:
        F.loc[F["expiry_day"].fillna(False).astype(bool), c] = np.nan
    F["cl"] = F["symbol"].astype("category").cat.codes
    return F


def rd(F, y, c=C, fuzzy=False, **kw):
    from rdrobust import rdrobust
    d = F.dropna(subset=[y, "x"])
    if len(d) < 200:
        return None
    try:
        r = rdrobust(d[y].values, d["x"].values, c=c, cluster=d["cl"].values,
                     fuzzy=d["ban"].astype(float).values if fuzzy else None, **kw)
    except Exception as e:
        return dict(err=str(e)[:60])
    return dict(b=float(r.coef.iloc[0, 0]), se=float(r.se.iloc[0, 0]), lo=float(r.ci.iloc[2, 0]), hi=float(r.ci.iloc[2, 1]),
                p=float(r.pv.iloc[2, 0]), h=float(r.bws.iloc[0, 0]), nl=int(r.N_h[0]), nr=int(r.N_h[1]))


def line(lab, q):
    if q is None:
        return f"  {lab:46s} too few observations"
    if "err" in q:
        return f"  {lab:46s} failed: {q['err']}"
    return (f"  {lab:46s} {q['b']:+9.3f} (se {q['se']:.3f}); robust 95% CI [{q['lo']:+.3f}, {q['hi']:+.3f}], p = {q['p']:.3g}; "
            f"h {q['h']:.3f}; n {q['nl']}/{q['nr']}")


def block(F, lab, outcomes, **kw):
    r = [lab]
    for y, nm in outcomes:
        r.append(line(nm, rd(F, y, **kw)))
    return r


BASIS = [("m", "basis level m_t (bp) [MAIN]"), ("dm", "Delta m_t, same contract (bp)"), ("mc", "close-based basis (bp)"),
         ("rr", "relative implied repo (bp, annual rate)")]
MECH = [("ly_fut", "log(1 + futures contracts)"), ("R", "R = (dOI + V)/V"), ("ly_cash", "log(1 + cash shares)"),
        ("deliv_share", "delivery share")]
PLAC = [("m_l2", "placebo: m_(t-2) (bp)"), ("ly_fut_l2", "placebo: log futures contracts on t-2"),
        ("m_l1", "crossing day: m_(t-1) (bp)"), ("valid", "selection: valid basis on t (share)")]


def main():
    F = frame()
    pre = F[(F["date"] >= "2015-01-02") & (F["date"] < REFORM) & F["x"].between(0.60, 1.30)]
    r = ["Regression discontinuity at the 95% trigger (PAP §11.6 C9). Supporting only.",
         f"Units: stock-days not in a ban on t-1, omega_(t-1) in [0.60, 1.30], 2015 to Sep 2025: n = {len(pre)}, "
         f"stocks {pre['symbol'].nunique()}",
         f"Share in a ban on t: omega_(t-1) in [0.90, 0.95): {pre.loc[pre['x'].between(0.90, 0.95, inclusive='left'), 'ban'].mean():.4f}; "
         f"[0.95, 1.00): {pre.loc[pre['x'].between(0.95, 1.00, inclusive='left'), 'ban'].mean():.4f}",
         "Local linear, triangular kernel, MSE-optimal h, conventional estimate with robust bias-corrected CI, SE clustered by stock.", ""]
    r += block(pre, "Basis outcomes:", BASIS)
    r += block(pre, "Mechanism outcomes (expiry days excluded):", MECH)
    r += block(pre, "Validity checks:", PLAC)
    r += block(pre, "Fuzzy RD (treatment = in a ban on t):", [("m", "basis level m_t"), ("ly_fut", "log(1 + futures contracts)")],
               fuzzy=True)
    # robustness on the main outcome and the futures-volume outcome
    q0 = rd(pre, "m")
    h0 = q0["h"] if q0 and "h" in q0 else 0.05
    r += ["", "Robustness (main outcome m_t; and log futures contracts):"]
    for nm, kw, d in [("half bandwidth", dict(h=h0 / 2), pre), ("double bandwidth", dict(h=h0 * 2), pre),
                      ("local quadratic", dict(p=2), pre),
                      ("donut |omega - 0.95| >= 0.005", {}, pre[(pre["x"] - C).abs() >= 0.005]),
                      ("no MWPL change on t-1", {}, pre[~pre["mwpl_chg"]]),
                      ("end-of-day enforcement (to 22 Mar 2020)", {}, pre[pre["date"] < INTRADAY]),
                      ("peak-intraday enforcement (from 23 Mar 2020)", {}, pre[pre["date"] >= INTRADAY])]:
        r.append(line(f"m_t: {nm}", rd(d, "m", **kw)))
        r.append(line(f"futures: {nm}", rd(d, "ly_fut", **kw)))
    r += ["", "Placebo cutoffs (main outcome m_t; futures contracts):"]
    for c, d in [(0.85, pre[pre["x"] < C]), (0.90, pre[pre["x"] < C]), (1.00, pre[pre["x"] >= C])]:
        r.append(line(f"m_t at {c:.2f}", rd(d, "m", c=c)))
        r.append(line(f"futures at {c:.2f}", rd(d, "ly_fut", c=c)))
    po = F[(F["date"] >= REFORM) & F["x"].between(0.60, 1.30)]
    r += ["", f"After 1 Oct 2025 (FutEq utilisation; descriptive): n = {len(po)}, "
              f"n in [0.95, 1.00) {int(po['x'].between(0.95, 1.0, inclusive='left').sum())}"]
    r += block(po, "", [("m", "basis level m_t"), ("ly_fut", "log(1 + futures contracts)")])
    txt = "\n".join(r)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "rd_95.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
