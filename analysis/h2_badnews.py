"""Secondary: H2, bad news in bans (model Prop. bad news is incorporated more slowly in a ban). Specification: PAP §11.9 C12.
Outputs analysis/output/h2_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, treatment, PROC, CACHE, ROOT
from inference import feols, coef_table, lincomb

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
BP = 1e4


def load():
    days, pos = calendar()
    E = pd.read_pickle(os.path.join(CACHE, "event_outcomes.pkl"))
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["i"] = B["date"].map(pos)
    F = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"), parse_dates=["date"])
    F["fno"] = True
    E = E.merge(F[["symbol", "date", "fno"]].rename(columns={"date": "event_day"}), on=["symbol", "event_day"], how="left")
    E["fno"] = E["fno"].fillna(False).astype(bool)
    E["i0"] = E["event_day"].map(pos)
    ban = set(zip(B["symbol"], B["i"]))
    E["ban0"] = [(s, i) in ban for s, i in zip(E["symbol"], E["i0"])]
    E["banpre"] = [(s, i - 1) in ban for s, i in zip(E["symbol"], E["i0"])]
    E["ban05"] = [any((s, i + k) in ban for k in range(6)) for s, i in zip(E["symbol"], E["i0"])]
    lag, _ = treatment(days, pos)
    E = E.merge(lag.rename(columns={"i": "i0"}), on=["symbol", "i0"], how="left")      # omega_(t-1) on day 0
    # pre-announcement basis, days -5..-1
    S = basis_sample()
    nb = S[(S["date"] < REFORM) & ~S["ban"] & (S["omega_lag"] < 0.60)]
    cnt = nb.groupby("symbol").size()
    q50 = nb[nb["symbol"].isin(cnt[cnt >= 100].index)].groupby("symbol")["m"].median()
    S = S[S["symbol"].isin(q50.index)]
    S["dev"] = (S["m"] - S["symbol"].map(q50)) * BP
    W = S.pivot_table(index="i", columns="symbol", values="dev")
    W = W.reindex(range(len(days)))
    pre, npre = [], []
    for s, i in zip(E["symbol"], E["i0"]):
        if s in W.columns and i >= 5:
            v = W[s].values[i - 5:i]
            ok = np.isfinite(v)
            pre.append(v[ok].mean() if ok.sum() >= 3 else np.nan); npre.append(ok.sum())
        else:
            pre.append(np.nan); npre.append(0)
    E["pre_m"] = pre
    # market-cap decile (cross-section in e): previous month-end market cap decile within the cash universe
    M = pd.read_csv(os.path.join(PROC, "mcap_daily.csv.gz"), parse_dates=["date"])
    M["ym"] = M["date"].dt.to_period("M")
    me = M.sort_values("date").groupby(["symbol", "ym"]).tail(1)
    me["dec"] = me.groupby("ym")["mcap_cr"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    me["ym"] = me["ym"] + 1
    E["ym"] = E["event_day"].dt.to_period("M")
    E = E.merge(me[["symbol", "ym", "dec"]], on=["symbol", "ym"], how="left")
    E["qs"] = E["q"].astype(str)
    E["date_c"] = E["event_day"].astype(str)
    for c in ["bad", "good", "ban0", "banpre", "ban05", "fno"]:
        E[c] = E[c].fillna(False).astype(int)
    return E


def run(d, y, ban, fe="qs", extra=""):
    d = d.dropna(subset=[y]).copy()
    d["B"] = d[ban]
    d["Bbad"] = d["B"] * d["bad"]; d["Bgood"] = d["B"] * d["good"]
    fit = feols(d, f"{y} ~ bad + good + B + Bbad + Bgood{extra} | {fe}", cluster="symbol+date_c")
    return fit, coef_table(fit), d


def onesided(b, se, sign):
    from scipy import stats
    z = b / se
    return float(stats.norm.sf(z)) if sign == ">" else float(stats.norm.cdf(z))


def main():
    E = load()
    F = E[E["fno"] == 1]
    r = ["H2: bad news in bans (PAP §11.9 C12). Secondary, unadjusted p. SE two-way clustered (stock, event date).",
         f"F&O-stock events: {len(F)}; with BHAR {F['bhar_w'].notna().sum()}; on ban days {int(F['ban0'].sum())} "
         f"(bad {int((F['ban0'] & F['bad']).sum())}, good {int((F['ban0'] & F['good']).sum())}); "
         f"ban on day -1: {int(F['banpre'].sum())}", ""]
    fit, t, d = run(F, "bhar_w", "ban0")
    b4, se4 = t.loc["Bbad", "b"], t.loc["Bbad", "se"]
    p_main = onesided(b4, se4, "<")
    dd, sdd = lincomb(fit, {"Bbad": 1.0, "Bgood": -1.0})
    r += ["(b) DRIFT: BHAR_w[+2,+64] on Bad, Good, Ban0 and interactions, quarter FE (units: return, 0.01 = 1%)"]
    r += [f"  {k:6s} {t.loc[k, 'b']:+.4f} (se {t.loc[k, 'se']:.4f})" for k in ["bad", "good", "B", "Bbad", "Bgood"]]
    r += [f"  TEST: one-sided p (Ban0 x Bad < 0) = {p_main:.3g}; Ban0xBad - Ban0xGood = {dd:+.4f} (se {sdd:.4f})",
          f"  drift outside bans (bad - good) = {t.loc['bad', 'b'] - t.loc['good', 'b']:+.4f}; n = {len(d)}"]
    r += ["  robustness (Ban0 x Bad; Ban0 x Good):"]
    for nm, dat, ban, fe, y in [("stock FE added", F, "ban0", "qs + symbol", "bhar_w"),
                                ("non-ban events with omega_(t-1) >= 0.80 only", F[(F["ban0"] == 1) | (F["omega_lag"] >= 0.80)], "ban0", "qs", "bhar_w"),
                                ("ban on any of days 0..+5", F, "ban05", "qs", "bhar_w"),
                                ("unwinsorised BHAR", F, "ban0", "qs", "bhar"),
                                ("pre-reform only", F[F["event_day"] < REFORM], "ban0", "qs", "bhar_w")]:
        _, tt, dd2 = run(dat, y, ban, fe)
        r.append(f"    {nm:46s} {tt.loc['Bbad', 'b']:+.4f} ({tt.loc['Bbad', 'se']:.4f}); {tt.loc['Bgood', 'b']:+.4f} "
                 f"({tt.loc['Bgood', 'se']:.4f}); n {len(dd2)}, ban events {int(dd2['B'].sum())}")
    # (c) pre-announcement basis
    fit2, t2, d2 = run(F, "pre_m", "banpre")
    c12, s12 = lincomb(fit2, {"bad": 1.0, "good": -1.0})
    c45, s45 = lincomb(fit2, {"Bbad": 1.0, "Bgood": -1.0})
    r += ["", f"(c) PRE-ANNOUNCEMENT BASIS: mean of m - q50_i over days -5..-1 (bp), quarter FE; n = {len(d2)}, "
              f"in a ban on day -1: {int(d2['B'].sum())}"]
    r += [f"  {k:6s} {t2.loc[k, 'b']:+.3f} (se {t2.loc[k, 'se']:.3f})" for k in ["bad", "good", "B", "Bbad", "Bgood"]]
    r += [f"  outside bans, bad - good = {c12:+.3f} (se {s12:.3f}); one-sided p (< 0) = {onesided(c12, s12, '<'):.3g}",
          f"  in bans, change in (bad - good) = {c45:+.3f} (se {s45:.3f}); one-sided p (> 0) = {onesided(c45, s45, '>'):.3g}"]
    _, t3, d3 = run(F, "pre_m", "banpre", "qs + symbol")
    r.append(f"  with stock FE: bad - good outside bans {t3.loc['bad', 'b'] - t3.loc['good', 'b']:+.3f}; "
             f"Bbad {t3.loc['Bbad', 'b']:+.3f} ({t3.loc['Bbad', 'se']:.3f}), Bgood {t3.loc['Bgood', 'b']:+.3f} ({t3.loc['Bgood', 'se']:.3f})")
    # (e) cross-section cash-only vs F&O
    X = E.dropna(subset=["bhar_w", "dec"]).copy()
    X["non"] = 1 - X["fno"]
    X["nbad"] = X["non"] * X["bad"]; X["ngood"] = X["non"] * X["good"]
    X["decs"] = X["dec"].astype(int).astype(str)
    t4 = coef_table(feols(X, "bhar_w ~ bad + good + non + nbad + ngood | qs + decs", cluster="symbol+date_c"))
    r += ["", f"(e) ALSO REPORTED (association): all events with a market-cap decile, n = {len(X)} (cash-only {int(X['non'].sum())})",
          "  BHAR_w on Bad, Good, NonFnO and interactions, quarter and size-decile FE:"]
    r += [f"  {k:6s} {t4.loc[k, 'b']:+.4f} (se {t4.loc[k, 'se']:.4f})" for k in ["bad", "good", "non", "nbad", "ngood"]]
    r += ["", f"Secondary test statistic (C12 b): one-sided p (Ban0 x Bad < 0) = {p_main:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h2_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
