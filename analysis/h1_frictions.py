"""Secondary: H1, ex-ante frictions and mispricing (model band and inventory results). Specification: PAP §11.10 C13.

Stock-quarter panel: outcomes in q (band width W, size A, persistence rho; non-ban days) on a friction index built in q-1
from Corwin-Schultz spread, Amihud illiquidity, idiosyncratic volatility, utilisation and SLB scarcity.
Outputs analysis/output/h1_results.txt and data/processed/cache/frictions_q.pkl.
"""
import glob, os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, PROC, RAW, CACHE, ROOT
from inference import feols, coef_table

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
BP = 1e4


def cs_spread(g):
    """Corwin-Schultz (2012) two-day spread with the overnight adjustment; g sorted by date for one stock."""
    H, L, Cl = g["high"].values.astype(float), g["low"].values.astype(float), g["close"].values.astype(float)
    ok = g["ok"].values
    S = np.full(len(g), np.nan)
    k = 3 - 2 * np.sqrt(2)
    for t in range(len(g) - 1):
        if not (ok[t] and ok[t + 1]) or min(H[t], L[t], H[t + 1], L[t + 1]) <= 0:
            continue
        h1, l1 = H[t + 1], L[t + 1]
        if l1 > Cl[t]:
            h1, l1 = h1 - (l1 - Cl[t]), Cl[t]
        elif h1 < Cl[t]:
            h1, l1 = Cl[t], l1 + (Cl[t] - h1)
        if l1 <= 0:
            continue
        beta = np.log(H[t] / L[t]) ** 2 + np.log(h1 / l1) ** 2
        gamma = np.log(max(H[t], h1) / min(L[t], l1)) ** 2
        alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
        S[t] = max(0.0, 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha)))
    return pd.Series(S, index=g.index)


def frictions(fno_syms):
    days, pos = calendar()
    # cash high/low/close (EQ) for F&O-ever symbols
    parts = []
    for f in sorted(glob.glob(os.path.join(RAW, "prices", "cash", "*.csv"))):
        d = pd.read_csv(f, usecols=["date", "symbol", "series", "high", "low", "close"])
        parts.append(d[(d["series"] == "EQ") & d["symbol"].isin(fno_syms)])
    C = pd.concat(parts, ignore_index=True)
    C["date"] = pd.to_datetime(C["date"])
    R = pd.read_csv(os.path.join(PROC, "returns_daily.csv.gz"), usecols=["date", "symbol", "series", "ret", "value_rs", "k_used", "flag"],
                    parse_dates=["date"])
    R = R[(R["series"] == "EQ") & R["symbol"].isin(fno_syms)]
    C = C.merge(R, on=["date", "symbol", "series"], how="left")
    C = C.sort_values(["symbol", "date"]).reset_index(drop=True)
    # two-day windows invalid across corporate actions: day t+1 must have k_used == 1 and a valid return
    C["ok"] = C["ret"].notna() & (C["k_used"].fillna(1) == 1) & C["flag"].isna()   # both days must be ok (checked in cs_spread)
    C["cs"] = C.groupby("symbol", group_keys=False).apply(cs_spread)
    C["amihud"] = C["ret"].abs() / (C["value_rs"] / 1e7)
    N = pd.read_csv(os.path.join(RAW, "indices", "nifty50_daily.csv"), usecols=["date", "close"], parse_dates=["date"])
    N = N.sort_values("date"); N["mkt"] = N["close"].pct_change()
    C = C.merge(N[["date", "mkt"]], on="date", how="left")
    C["q"] = C["date"].dt.to_period("Q")

    def ivol(g):
        g = g.dropna(subset=["ret", "mkt"])
        if len(g) < 40:
            return np.nan
        X = np.c_[np.ones(len(g)), g["mkt"].values]
        b = np.linalg.lstsq(X, g["ret"].values, rcond=None)[0]
        return np.std(g["ret"].values - X @ b, ddof=2)
    Fq = C.groupby(["symbol", "q"]).agg(cs=("cs", "mean"), amihud=("amihud", "mean")).reset_index()
    Fq["ivol"] = C.groupby(["symbol", "q"]).apply(ivol).values
    Fq["lamihud"] = np.log(Fq["amihud"].where(Fq["amihud"] > 0))
    # utilisation on non-ban days
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "util", "util_futeq"], parse_dates=["date"])
    P["omega"] = np.where(P["date"] >= REFORM, P["util_futeq"], P["util"])
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"]); B["ban"] = True
    P = P.merge(B[["date", "symbol", "ban"]], on=["date", "symbol"], how="left")
    P = P[P["ban"].isna()]
    P["q"] = P["date"].dt.to_period("Q")
    W = P.groupby(["symbol", "q"])["omega"].mean().rename("util").reset_index()
    # SLB activity and fee
    M = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"), parse_dates=["date"])
    M["q"] = M["date"].dt.to_period("Q")
    ndays = M.groupby(["symbol", "q"]).size().rename("fno_days")
    S = pd.read_csv(os.path.join(PROC, "slb_daily.csv.gz"), parse_dates=["date", "expiry"])
    S = S.merge(C[["date", "symbol", "close"]], on=["date", "symbol"], how="left")
    S["fee_ann"] = S["value"] / S["qty"] / S["close"] * 365 / (S["expiry"] - S["date"]).dt.days.clip(lower=1)
    S["q"] = S["date"].dt.to_period("Q")
    sd = S.groupby(["symbol", "q"]).agg(slb_days=("date", "nunique"), slb_fee=("fee_ann", "median")).reset_index()
    Fq = Fq.merge(W, on=["symbol", "q"], how="left").merge(sd, on=["symbol", "q"], how="left")
    Fq = Fq.merge(ndays.reset_index(), on=["symbol", "q"], how="left")
    Fq["slb_days"] = Fq["slb_days"].fillna(0)
    Fq["slb_scarce"] = 1 - (Fq["slb_days"] / Fq["fno_days"]).clip(upper=1)
    return Fq


def outcomes():
    S = basis_sample()
    S = S[~S["ban"]].copy()
    S["q"] = S["date"].dt.to_period("Q")
    out = []
    for (s, q), g in S.groupby(["symbol", "q"]):
        if len(g) < 30:
            continue
        m = g["m"].values * BP
        row = dict(symbol=s, q=q, W=np.quantile(m, 0.8) - np.quantile(m, 0.2), A=np.mean(np.abs(m)), n=len(g))
        h = g.dropna(subset=["m_lag"])
        if len(h) >= 30:
            x, y = h["m_lag"].values, h["m"].values
            row["rho"] = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
        out.append(row)
    return pd.DataFrame(out)


def outcomes_all():
    S = basis_sample()
    S["q"] = S["date"].dt.to_period("Q")
    g = S.groupby(["symbol", "q"])["m"]
    o = pd.DataFrame({"W_all": (g.quantile(0.8) - g.quantile(0.2)) * BP, "n_all": g.size()}).reset_index()
    return o[o["n_all"] >= 30]


FR = ["cs", "lamihud", "ivol", "util", "slb_scarce"]


def build_index(Fq, cols):
    Z = Fq[["symbol", "q"] + cols].dropna().copy()
    for c in cols:
        Z[c] = Z.groupby("q")[c].transform(lambda x: (x - x.mean()) / x.std())
    X = Z[cols].values
    w, V = np.linalg.eigh(np.corrcoef(X, rowvar=False))
    v = V[:, -1]
    if v.sum() < 0:
        v = -v
    Z["index"] = X @ v
    Z["index"] = Z.groupby("q")["index"].transform(lambda x: (x - x.mean()) / x.std())
    return Z, v, w[-1] / w.sum()


def main():
    M = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"))
    path = os.path.join(CACHE, "frictions_q.pkl")
    if os.path.exists(path):
        Fq = pd.read_pickle(path)
    else:
        Fq = frictions(set(M["symbol"]))
        Fq.to_pickle(path)
    O = outcomes().merge(outcomes_all(), on=["symbol", "q"], how="left")
    r = ["H1: ex-ante frictions and mispricing (PAP §11.10 C13). Secondary, unadjusted. SE two-way clustered (stock, quarter).", ""]
    Z, v, share = build_index(Fq, FR)
    r.append("Index loadings (first principal component, frictions standardised within quarter): " +
             ", ".join(f"{c} {x:+.3f}" for c, x in zip(FR, v)) + f"; variance share {share:.3f}")
    corr = Z[FR].corr().round(2)
    r += ["Correlations of standardised frictions:", corr.to_string()]
    Z["q"] = Z["q"] + 1                      # frictions of q-1 attached to outcome quarter q
    D = O.merge(Z, on=["symbol", "q"], how="inner")
    D["qs"] = D["q"].astype(str)
    main_d = D[(D["q"] >= pd.Period("2015Q2")) & (D["q"] <= pd.Period("2025Q3"))]
    r += ["", f"Stock-quarters (outcomes 2015Q2-2025Q3 with lagged frictions): {len(main_d)}, stocks {main_d['symbol'].nunique()}",
          "Outcome means: " + ", ".join(f"{c} {main_d[c].mean():.2f}" for c in ["W", "A", "rho"]), ""]
    pW = None
    for y, nm in [("W", "band width W = q80 - q20 (bp)"), ("A", "mispricing size A = mean |m| (bp)"), ("rho", "persistence rho")]:
        d = main_d.dropna(subset=[y])
        t = coef_table(feols(d, f"{y} ~ index | qs", cluster="symbol+qs"))
        b, se, p = t.loc["index", "b"], t.loc["index", "se"], t.loc["index", "p_two"]
        p1 = p / 2 if b > 0 else 1 - p / 2
        r.append(f"MAIN {nm:36s}: beta (per 1 sd of index) {b:+.4f} (se {se:.4f}, t {b / se:+.2f}); one-sided p(> 0) = {p1:.3g}; n {len(d)}")
        if y == "W":
            pW = p1
    r += ["", "Also reported:"]
    for y in ["W", "A", "rho"]:
        d = main_d.dropna(subset=[y])
        t = coef_table(feols(d, f"{y} ~ {' + '.join(FR)} | qs", cluster="symbol+qs"))
        r.append(f"  {y} on all five frictions (standardised): " + "; ".join(f"{c} {t.loc[c, 'b']:+.3f} ({t.loc[c, 'se']:.3f})" for c in FR))
        t = coef_table(feols(d, f"{y} ~ index | qs + symbol", cluster="symbol+qs"))
        r.append(f"  {y} with stock FE: {t.loc['index', 'b']:+.4f} ({t.loc['index', 'se']:.4f})")
    d = main_d.dropna(subset=["W_all"])
    t = coef_table(feols(d, "W_all ~ index | qs", cluster="symbol+qs"))
    r.append(f"  W on all days incl. ban days: {t.loc['index', 'b']:+.4f} ({t.loc['index', 'se']:.4f})")
    d = D[D["q"] >= pd.Period("2015Q2")].dropna(subset=["W"])
    t = coef_table(feols(d, "W ~ index | qs", cluster="symbol+qs"))
    r.append(f"  W, period to 2026Q3 (n {len(d)}): {t.loc['index', 'b']:+.4f} ({t.loc['index', 'se']:.4f})")
    Z4, v4, _ = build_index(Fq, FR[:-1])
    Z4["q"] = Z4["q"] + 1
    D4 = O.merge(Z4, on=["symbol", "q"], how="inner"); D4["qs"] = D4["q"].astype(str)
    D4 = D4[(D4["q"] >= pd.Period("2015Q2")) & (D4["q"] <= pd.Period("2025Q3"))].dropna(subset=["W"])
    t = coef_table(feols(D4, "W ~ index | qs", cluster="symbol+qs"))
    r.append(f"  W, index without SLB (loadings " + ", ".join(f"{c} {x:+.2f}" for c, x in zip(FR[:-1], v4)) +
             f"): {t.loc['index', 'b']:+.4f} ({t.loc['index', 'se']:.4f})")
    fee = Fq.dropna(subset=["slb_fee"])
    r.append(f"  SLB fee (annualised, median over traded days): stock-quarters with any SLB trade {len(fee)} of {len(Fq)}; "
             f"median fee {fee['slb_fee'].median() * 100:.2f}% a year (p10 {fee['slb_fee'].quantile(.1) * 100:.2f}%, "
             f"p90 {fee['slb_fee'].quantile(.9) * 100:.2f}%)")
    r += ["", f"Secondary test statistic (C13 e): one-sided p (beta > 0 for W) = {pW:.3g}"]
    txt = "\n".join(r)
    open(os.path.join(OUT, "h1_results.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
