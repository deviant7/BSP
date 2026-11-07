"""Secondary: H5, anomaly returns by short-sale constraint (model Miller result). Specification: PAP §11.12 C15.

Monthly sorts within constraint groups (G1 F&O, G2 cash-only with SLB trades in the last 3 months, G3 cash-only without)
on a composite mispricing score (6 public anomalies); legs against the group's value-weighted return.
Outputs analysis/output/h5_results.txt; cache data/processed/cache/h5_monthly.pkl.
"""
import os, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
sys.path.insert(0, os.path.dirname(__file__))
from samples import PROC, RAW, CACHE, ROOT

OUT = os.path.join(ROOT, "analysis", "output")
ANOM = {"mom": -1, "rev": +1, "max": +1, "ivol": +1, "illiq": -1, "turn": +1}   # +1: high value = overpriced


def monthly_panel():
    path = os.path.join(CACHE, "h5_monthly.pkl")
    if os.path.exists(path):
        return pd.read_pickle(path)
    R = pd.read_csv(os.path.join(PROC, "returns_daily.csv.gz"), usecols=["date", "symbol", "series", "close", "value_rs", "ret"],
                    parse_dates=["date"])
    R = R[R["series"].isin(["EQ", "BE", "BZ"])]
    R = R.sort_values(["symbol", "date"]).drop_duplicates(["symbol", "date"], keep="first")
    N = pd.read_csv(os.path.join(RAW, "indices", "nifty50_daily.csv"), usecols=["date", "close"], parse_dates=["date"])
    N = N.sort_values("date"); N["mkt"] = N["close"].pct_change()
    R = R.merge(N[["date", "mkt"]], on="date", how="left")
    R["m"] = R["date"].dt.to_period("M")
    R["absr_v"] = R["ret"].abs() / (R["value_rs"] / 1e7)
    ok = R["ret"].notna() & R["mkt"].notna()
    X = R[ok].copy()
    X["rm"] = X["ret"] * X["mkt"]; X["r2"] = X["ret"] ** 2; X["m2"] = X["mkt"] ** 2
    g = X.groupby(["symbol", "m"])
    S = g.agg(n=("ret", "size"), sr=("ret", "sum"), sm=("mkt", "sum"), srm=("rm", "sum"), sr2=("r2", "sum"), sm2=("m2", "sum"))
    cov = S["srm"] / S["n"] - S["sr"] * S["sm"] / S["n"] ** 2
    vm = S["sm2"] / S["n"] - (S["sm"] / S["n"]) ** 2
    vr = S["sr2"] / S["n"] - (S["sr"] / S["n"]) ** 2
    resid = (vr - cov ** 2 / vm).clip(lower=0)
    S["ivol"] = np.sqrt(resid * S["n"] / (S["n"] - 2)).where(S["n"] >= 15)
    g2 = R.groupby(["symbol", "m"])
    M = pd.DataFrame({
        "mret": g2["ret"].apply(lambda x: np.prod(1 + x.dropna()) - 1 if x.notna().sum() >= 10 else np.nan),
        "max": g2["ret"].max(),
        "illiq": g2["absr_v"].mean(),
        "value": g2["value_rs"].sum(),
        "close": g2["close"].last(),
        "lastdate": g2["date"].max(),
    })
    M = M.join(S[["ivol"]], how="left").reset_index()
    C = pd.read_csv(os.path.join(PROC, "mcap_daily.csv.gz"), parse_dates=["date"])
    C["m"] = C["date"].dt.to_period("M")
    Cm = C.sort_values("date").groupby(["symbol", "m"])["mcap_cr"].last().rename("mcap").reset_index()
    M = M.merge(Cm, on=["symbol", "m"], how="left")
    M["turn"] = M["value"] / (M["mcap"] * 1e7)
    M = M.sort_values(["symbol", "m"])
    M["rev"] = M["mret"]
    lr = np.log1p(M["mret"])
    # momentum: months t-11..t-1 (11 months), at least 9 available; requires consecutive periods
    M["lr"] = lr
    M["pidx"] = M["m"].apply(lambda p: p.ordinal)
    def mom(df):
        s = pd.Series(df["lr"].values, index=df["pidx"].values)
        full = s.reindex(range(s.index.min(), s.index.max() + 1))
        roll = full.shift(1).rolling(11, min_periods=9).sum()
        return pd.Series(np.expm1(roll.reindex(df["pidx"].values).values), index=df.index)
    M["mom"] = M.groupby("symbol", group_keys=False).apply(mom)
    # next-month return (holding period), consecutive month only
    M["ret_next"] = M.groupby("symbol")["mret"].shift(-1)
    M["p_next"] = M.groupby("symbol")["pidx"].shift(-1)
    M.loc[M["p_next"] != M["pidx"] + 1, "ret_next"] = np.nan
    # constraint groups
    F = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"), parse_dates=["date"])
    F["m"] = F["date"].dt.to_period("M")
    last_day = F.groupby("m")["date"].max()
    Fm = F[F["date"].isin(last_day.values)][["symbol", "m"]].assign(fno=1)
    M = M.merge(Fm, on=["symbol", "m"], how="left")
    M["fno"] = M["fno"].fillna(0)
    SL = pd.read_csv(os.path.join(PROC, "slb_daily.csv.gz"), parse_dates=["date"])
    SL["m"] = SL["date"].dt.to_period("M")
    sl = SL.groupby(["symbol", "m"]).size().rename("slb_n").reset_index()
    M = M.merge(sl, on=["symbol", "m"], how="left")
    M["slb_n"] = M["slb_n"].fillna(0)
    M["slb3"] = M.groupby("symbol")["slb_n"].transform(lambda x: x.rolling(3, min_periods=1).sum())
    M["grp"] = np.where(M["fno"] == 1, "G1", np.where(M["slb3"] > 0, "G2", "G3"))
    M.drop(columns=["lr"]).to_pickle(path)
    return M


def nw(series, lags=6):
    y = series.dropna()
    f = sm.OLS(y.values, np.ones(len(y))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(f.params[0]), float(f.bse[0]), len(y)


def composite(D, anoms):
    P = pd.DataFrame(index=D.index)
    for a in anoms:
        rk = D.groupby("m")[a].rank(pct=True)
        P[a] = rk if ANOM[a] > 0 else 1 - rk
    cnt = P.notna().sum(axis=1)
    return P.mean(axis=1).where(cnt >= min(4, len(anoms)))


def legs(D, score, group_col="grp", vw=True):
    """Per month and group: short-leg (top tercile of score) and long-leg (bottom tercile) returns minus group return."""
    D = D.assign(score=score).dropna(subset=["score", "ret_next", "mcap"])
    D = D[D["mcap"] > 0]
    D["terc"] = D.groupby(["m", group_col])["score"].transform(
        lambda x: pd.qcut(x.rank(method="first"), 3, labels=False) if len(x) >= 15 else np.nan)
    D = D.dropna(subset=["terc"])
    w = D["mcap"] if vw else pd.Series(1.0, index=D.index)
    D = D.assign(w=w, wr=w * D["ret_next"])
    grp = D.groupby(["m", group_col]).apply(lambda x: x["wr"].sum() / x["w"].sum()).rename("gret")
    tr = D.groupby(["m", group_col, "terc"]).apply(lambda x: x["wr"].sum() / x["w"].sum()).unstack("terc")
    out = tr.join(grp)
    out["short"] = out[2.0] - out["gret"]
    out["long"] = out[0.0] - out["gret"]
    out["ls"] = out[0.0] - out[2.0]
    return out[["short", "long", "ls", "gret"]].unstack(group_col)


def report_legs(L, lab, a="G3", b="G1"):
    r = [f"{lab}:"]
    for g in sorted(L["short"].columns):
        s, ses, n = nw(L["short"][g]); l, sel, _ = nw(L["long"][g]); ls, sels, _ = nw(L["ls"][g])
        r.append(f"  {g}: short leg {s * 100:+.3f}% (se {ses * 100:.3f}); long leg {l * 100:+.3f}% ({sel * 100:.3f}); "
                 f"long-short {ls * 100:+.3f}% ({sels * 100:.3f}) per month; months {n}")
    ds, sds, n = nw(L["short"][a] - L["short"][b])
    dl, sdl, _ = nw(L["long"][a] - L["long"][b])
    from scipy import stats
    p = stats.norm.cdf(ds / sds)
    r.append(f"  short leg {a} - {b}: {ds * 100:+.3f}% (NW se {sds * 100:.3f}); one-sided p (< 0) = {p:.3g}; "
             f"long leg {a} - {b}: {dl * 100:+.3f}% ({sdl * 100:.3f}), two-sided p = {2 * stats.norm.sf(abs(dl / sdl)):.3g}")
    return r, p


def main():
    M = monthly_panel()
    D = M[(M["close"] >= 5) & (M["m"] >= pd.Period("2016-01", "M")) & (M["m"] <= pd.Period("2026-09", "M"))].copy()
    r = ["H5: anomaly returns by short-sale constraint (PAP §11.12 C15). Secondary, unadjusted. Monthly, Newey-West (6 lags).",
         f"Stock-months (signal months Jan 2016 to Sep 2026, price >= Rs 5): {len(D)}; by group: " +
         ", ".join(f"{k} {v}" for k, v in D["grp"].value_counts().sort_index().items()),
         "Median market cap by group (Rs crore): " + ", ".join(f"{k} {v:.0f}" for k, v in D.groupby("grp")["mcap"].median().items()), ""]
    sc = composite(D, list(ANOM))
    L = legs(D, sc)
    out, p_main = report_legs(L, "MAIN: composite score terciles within group, value-weighted, legs vs group VW return")
    r += out
    out2, _ = report_legs(L, "  G2 vs G1", a="G2", b="G1")
    r += [out2[-1]]
    r += [""]
    r += report_legs(legs(D, sc, vw=False), "Equal-weighted")[0]
    big = D[D["mcap"] >= D.groupby("m")["mcap"].transform("median")]
    r += report_legs(legs(big, composite(big, list(ANOM))), "Excluding stocks below the median market cap")[0]
    pre = D[D["m"] <= pd.Period("2025-08", "M")]
    r += report_legs(legs(pre, composite(pre, list(ANOM))), "Holding months to September 2025")[0]
    # IVOL-tercile grouping (SYY), composite without IVOL
    D["ivt"] = D.groupby("m")["ivol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=["I1", "I2", "I3"]))
    sc5 = composite(D, [a for a in ANOM if a != "ivol"])
    r += report_legs(legs(D.dropna(subset=["ivt"]), sc5.loc[D.dropna(subset=["ivt"]).index], group_col="ivt"),
                     "IVOL terciles as groups (I3 = highest arbitrage risk), composite without IVOL", a="I3", b="I1")[0]
    r += ["", "Each anomaly separately (terciles within group; short = predicted-low-return tercile):"]
    for a in ANOM:
        s = D[a] if ANOM[a] > 0 else -D[a]
        s = s.where(D[a].notna())
        Lx = legs(D, s.groupby(D["m"]).rank(pct=True))
        ds, sds, n = nw(Lx["short"]["G3"] - Lx["short"]["G1"])
        dl, sdl, _ = nw(Lx["long"]["G3"] - Lx["long"]["G1"])
        ls = {g: nw(Lx["ls"][g])[0] * 100 for g in ["G1", "G2", "G3"]}
        r.append(f"  {a:6s} long-short G1 {ls['G1']:+.2f}% G2 {ls['G2']:+.2f}% G3 {ls['G3']:+.2f}%; short leg G3-G1 "
                 f"{ds * 100:+.3f}% ({sds * 100:.3f}); long leg G3-G1 {dl * 100:+.3f}% ({sdl * 100:.3f})")
    r += ["", f"Secondary test statistic (C15 e): one-sided p (short leg G3 - G1 < 0) = {p_main:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h5_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
