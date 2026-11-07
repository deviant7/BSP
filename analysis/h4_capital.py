"""Secondary: H4, arbitrage capital and the upper part of the basis distribution. Specification: PAP §11.11 C14.
Monthly time series, May 2018 to September 2026; Newey-West (6 lags) standard errors.
Outputs analysis/output/h4_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, PROC, RAW, ROOT

OUT = os.path.join(ROOT, "analysis", "output")
BP = 1e4


def monthly():
    S = basis_sample()
    S = S[~S["ban"]].copy()
    S["month"] = S["date"].dt.to_period("M")
    g = S.groupby("month")["m"]
    Y = pd.DataFrame({"q80": g.quantile(0.8), "q90": g.quantile(0.9), "q50": g.quantile(0.5), "q20": g.quantile(0.2),
                      "n": g.size()}) * 1.0
    for c in ["q80", "q90", "q50", "q20"]:
        Y[c] *= BP
    Y["width"] = Y["q80"] - Y["q20"]
    A = pd.read_csv(os.path.join(PROC, "amfi_arbitrage_monthly.csv"))
    A["month"] = pd.PeriodIndex(A["month"], freq="M")
    A = A.set_index("month").sort_index()
    A["flow"] = A["net_inflow"] / A["aum"].shift(1)
    A["dlaum"] = np.log(A["aum"]).diff()
    A["laum"] = np.log(A["aum"])
    R = pd.read_csv(os.path.join(RAW, "rates", "INDIR3TIB01STM.csv"))
    R["month"] = pd.PeriodIndex(pd.to_datetime(R["observation_date"]), freq="M")
    R = R.set_index("month")["INDIR3TIB01STM"].rename("rate")
    D = Y.join(A[["flow", "dlaum", "laum", "net_inflow", "aum"]], how="inner").join(R, how="left")
    D["flow_l1"] = D["flow"].shift(1)
    D["drate"] = D["rate"].diff()
    t = D.index.to_timestamp()
    D["tax23"] = (t >= "2023-04-01").astype(float)
    D["stt24"] = (t >= "2024-10-01").astype(float)
    D["stt26"] = (t >= "2026-04-01").astype(float)
    D["trend"] = np.arange(len(D)) / 12.0
    D["dq80"] = D["q80"].diff()
    return D


def ols(D, y, xs, lags=6):
    d = D[[y] + xs].dropna()
    X = sm.add_constant(d[xs])
    f = sm.OLS(d[y], X).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return f, len(d)


def line(f, n, x, lab, sign="<"):
    b, se, t = f.params[x], f.bse[x], f.tvalues[x]
    from scipy import stats
    p1 = stats.norm.cdf(t) if sign == "<" else stats.norm.sf(t)
    return f"  {lab:58s} {x} {b:+9.3f} (NW se {se:.3f}, t {t:+.2f}); one-sided p({sign} 0) = {p1:.3g}; n {n}"


def main():
    D = monthly()
    D = D[D.index >= pd.Period("2018-05", "M")]
    steps = ["tax23", "stt24", "stt26"]
    r = ["H4: arbitrage capital and the upper part of the basis distribution (PAP §11.11 C14). Secondary, unadjusted.",
         f"Months {D.index.min()} to {D.index.max()} (n {len(D)}); flow = net inflow / previous month-end AUM: mean "
         f"{D['flow'].mean():.4f}, sd {D['flow'].std():.4f}; q80 mean {D['q80'].mean():.2f} bp, sd {D['q80'].std():.2f}", ""]
    f, n = ols(D, "q80", ["flow_l1"] + steps)
    r.append("MAIN: q80_t on flow_(t-1) and step dummies (tax/STT Apr 2023, STT Oct 2024, STT Apr 2026):")
    r.append(line(f, n, "flow_l1", "q80 (bp) per unit flow (1 = 100% of AUM)"))
    r.append("  steps: " + ", ".join(f"{s} {f.params[s]:+.2f} ({f.bse[s]:.2f})" for s in steps))
    from scipy import stats
    p_main = stats.norm.cdf(f.tvalues["flow_l1"])
    r += ["", "Also reported:"]
    specs = [("q80", ["flow"] + steps, "flow", "contemporaneous flow"),
             ("q80", ["dlaum"] + steps, "dlaum", "change in log AUM"),
             ("q80", ["laum", "trend"] + steps, "laum", "log AUM level with linear trend"),
             ("q90", ["flow_l1"] + steps, "flow_l1", "outcome q90"),
             ("q50", ["flow_l1"] + steps, "flow_l1", "outcome q50"),
             ("q20", ["flow_l1"] + steps, "flow_l1", "outcome q20"),
             ("width", ["flow_l1"] + steps, "flow_l1", "outcome q80 - q20"),
             ("dq80", ["flow_l1"], "flow_l1", "first differences: Delta q80 on flow_(t-1)"),
             ("q80", ["flow_l1", "drate"] + steps, "flow_l1", "adding change in 3-month interbank rate")]
    for y, xs, x, lab in specs:
        f2, n2 = ols(D, y, xs)
        r.append(line(f2, n2, x, lab))
    ex = D[~D.index.isin(pd.period_range("2020-03", "2020-05", freq="M"))]
    f3, n3 = ols(ex, "q80", ["flow_l1"] + steps)
    r.append(line(f3, n3, "flow_l1", "excluding March to May 2020"))
    pre = D[D.index < pd.Period("2023-04", "M")]
    f4, n4 = ols(pre, "q80", ["flow_l1"])
    r.append(line(f4, n4, "flow_l1", "before April 2023"))
    post = D[D.index >= pd.Period("2023-04", "M")]
    f5, n5 = ols(post, "q80", ["flow_l1", "stt24", "stt26"])
    r.append(line(f5, n5, "flow_l1", "from April 2023"))
    r += ["", "Monthly series (bp; flow in % of AUM):"]
    tab = D[["q20", "q50", "q80", "flow", "aum"]].copy(); tab["flow"] *= 100
    r += [tab.round(2).to_string()]
    r += ["", f"Secondary test statistic (C14 c): one-sided p (b < 0) = {p_main:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h4_results.txt"), "w").write(txt + "\n")
    print("\n".join(r[:30]))


if __name__ == "__main__":
    main()
