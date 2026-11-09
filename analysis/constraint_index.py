"""Constraint index for all NSE stocks (project-document deliverable; specification PAP §11.14 C17).

Per stock-quarter (2015 Q1 to 2026 Q3, price >= Rs 5, >= 40 trading days): no short channel (not in F&O), SLB scarcity,
Corwin-Schultz spread, log Amihud illiquidity, idiosyncratic volatility; index = first principal component of the
components standardised within quarter. Validation against price delay, post-announcement drift and (F&O stocks) the basis
band width. Outputs data/processed/constraint_index_q.csv.gz and analysis/output/constraint_index.txt.
"""
import glob, os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import PROC, RAW, CACHE, ROOT
from inference import feols, coef_table

OUT = os.path.join(ROOT, "analysis", "output")
COMP = ["no_short", "slb_scarce", "cs", "lamihud", "ivol"]


def daily():
    parts = []
    for f in sorted(glob.glob(os.path.join(RAW, "prices", "cash", "*.csv"))):
        d = pd.read_csv(f, usecols=["date", "symbol", "series", "high", "low", "close"])
        parts.append(d[d["series"].isin(["EQ", "BE", "BZ"])])
    C = pd.concat(parts, ignore_index=True)
    C["date"] = pd.to_datetime(C["date"])
    R = pd.read_csv(os.path.join(PROC, "returns_daily.csv.gz"), usecols=["date", "symbol", "series", "ret", "value_rs", "k_used", "flag"],
                    parse_dates=["date"])
    C = C.merge(R, on=["date", "symbol", "series"], how="inner")
    C["srank"] = C["series"].map({"EQ": 0, "BE": 1, "BZ": 2})
    C = C.sort_values(["symbol", "date", "srank"]).drop_duplicates(["symbol", "date"], keep="first")
    C = C.sort_values(["symbol", "date"]).reset_index(drop=True)
    return C


def corwin_schultz(C):
    """Vectorised two-day Corwin-Schultz estimator with the overnight adjustment."""
    g = C.groupby("symbol")
    H, L, Cl = C["high"].astype(float), C["low"].astype(float), C["close"].astype(float)
    H1, L1 = g["high"].shift(-1).astype(float), g["low"].shift(-1).astype(float)
    ok = C["ret"].notna() & (C["k_used"].fillna(1) == 1) & C["flag"].isna()
    ok1 = g["ret"].shift(-1).notna() & (g["k_used"].shift(-1).fillna(1) == 1) & g["flag"].shift(-1).isna()
    up = L1 > Cl
    dn = H1 < Cl
    H1a = np.where(up, H1 - (L1 - Cl), np.where(dn, Cl, H1))
    L1a = np.where(up, Cl, np.where(dn, L1 + (Cl - H1), L1))
    k = 3 - 2 * np.sqrt(2)
    with np.errstate(all="ignore"):
        beta = np.log(H / L) ** 2 + np.log(H1a / L1a) ** 2
        gamma = np.log(np.maximum(H, H1a) / np.minimum(L, L1a)) ** 2
        alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
        S = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
    S = np.where(ok & ok1 & (L > 0) & (L1a > 0), np.maximum(S, 0.0), np.nan)
    return S


def quarterly(C):
    C["cs"] = corwin_schultz(C)
    C["amihud"] = C["ret"].abs() / (C["value_rs"] / 1e7)
    N = pd.read_csv(os.path.join(RAW, "indices", "nifty50_daily.csv"), usecols=["date", "close"], parse_dates=["date"])
    N = N.sort_values("date"); N["mkt"] = N["close"].pct_change()
    C = C.merge(N[["date", "mkt"]], on="date", how="left")
    C["q"] = C["date"].dt.to_period("Q")
    X = C[C["ret"].notna() & C["mkt"].notna()].copy()
    X["rm"] = X["ret"] * X["mkt"]; X["r2"] = X["ret"] ** 2; X["m2"] = X["mkt"] ** 2
    S = X.groupby(["symbol", "q"]).agg(n=("ret", "size"), sr=("ret", "sum"), sm=("mkt", "sum"), srm=("rm", "sum"),
                                         sr2=("r2", "sum"), sm2=("m2", "sum"))
    cov = S["srm"] / S["n"] - S["sr"] * S["sm"] / S["n"] ** 2
    vm = S["sm2"] / S["n"] - (S["sm"] / S["n"]) ** 2
    vr = S["sr2"] / S["n"] - (S["sr"] / S["n"]) ** 2
    S["ivol"] = np.sqrt((vr - cov ** 2 / vm).clip(lower=0) * S["n"] / (S["n"] - 2)).where(S["n"] >= 40)
    Q = C.groupby(["symbol", "q"]).agg(days=("date", "size"), cs=("cs", "mean"), amihud=("amihud", "mean"),
                                        close=("close", "last"), lastdate=("date", "max")).join(S[["ivol"]]).reset_index()
    Q["lamihud"] = np.log(Q["amihud"].where(Q["amihud"] > 0))
    F = pd.read_csv(os.path.join(PROC, "fno_membership.csv.gz"), parse_dates=["date"])
    F["q"] = F["date"].dt.to_period("Q")
    last = F.groupby("q")["date"].max()
    fq = F[F["date"].isin(last.values)][["symbol", "q"]].assign(fno=1)
    Q = Q.merge(fq, on=["symbol", "q"], how="left")
    Q["no_short"] = 1.0 - Q["fno"].fillna(0)
    SL = pd.read_csv(os.path.join(PROC, "slb_daily.csv.gz"), parse_dates=["date"])
    SL["q"] = SL["date"].dt.to_period("Q")
    sd = SL.groupby(["symbol", "q"])["date"].nunique().rename("slb_days").reset_index()
    Q = Q.merge(sd, on=["symbol", "q"], how="left")
    Q["slb_days"] = Q["slb_days"].fillna(0)
    Q["slb_scarce"] = 1 - (Q["slb_days"] / Q["days"]).clip(upper=1)
    Q = Q[(Q["close"] >= 5) & (Q["days"] >= 40) & (Q["q"] <= pd.Period("2026Q3"))]
    return Q


def build_index(Q):
    Z = Q.dropna(subset=COMP).copy()
    zc = []
    for c in COMP:
        Z["z_" + c] = Z.groupby("q")[c].transform(lambda x: (x - x.mean()) / x.std() if x.std() > 0 else x * 0)
        zc.append("z_" + c)
    X = Z[zc].values
    w, V = np.linalg.eigh(np.corrcoef(X, rowvar=False))
    v = V[:, -1]
    if v.sum() < 0:
        v = -v
    Z["index"] = X @ v
    Z["index"] = Z.groupby("q")["index"].transform(lambda x: (x - x.mean()) / x.std())
    Z["tercile"] = Z.groupby("q")["index"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=[1, 2, 3]).astype(int))
    return Z, v, w[-1] / w.sum()


def main():
    Q = quarterly(daily())
    Z, v, share = build_index(Q)
    r = ["Constraint index for all NSE stocks (PAP §11.14 C17).",
         f"Stock-quarters {len(Z)} ({Z['symbol'].nunique()} stocks, {Z['q'].min()} to {Z['q'].max()}); F&O share "
         f"{(1 - Z['no_short']).mean():.3f}; any SLB trade in quarter {(Z['slb_days'] > 0).mean():.3f}",
         "Loadings (first principal component, components standardised within quarter): " +
         ", ".join(f"{c} {x:+.3f}" for c, x in zip(COMP, v)) + f"; variance share {share:.3f}",
         "Correlations of standardised components:", Z[["z_" + c for c in COMP]].corr().round(2).to_string(), ""]
    # loadings by year
    r.append("Loadings by year:")
    for y in sorted(Z["q"].dt.year.unique()):
        X = Z.loc[Z["q"].dt.year == y, ["z_" + c for c in COMP]].values
        w, V = np.linalg.eigh(np.corrcoef(X, rowvar=False)); vv = V[:, -1]; vv = vv if vv.sum() > 0 else -vv
        r.append(f"  {y}: " + ", ".join(f"{c} {x:+.2f}" for c, x in zip(COMP, vv)) + f" (share {w[-1] / w.sum():.2f})")
    # persistence
    Z = Z.sort_values(["symbol", "q"])
    Zn = Z[["symbol", "q", "index"]].copy(); Zn["q"] = Zn["q"] - 1
    P = Z.merge(Zn.rename(columns={"index": "index_next"}), on=["symbol", "q"])
    rc = P.groupby("q").apply(lambda g: g["index"].rank().corr(g["index_next"].rank())).mean()
    r += ["", f"Persistence: mean quarter-to-quarter rank correlation {rc:.3f}"]
    out = Z[["symbol", "q", "days", "close", "no_short", "slb_days", "slb_scarce", "cs", "amihud", "lamihud", "ivol", "index", "tercile"]].copy()
    out["q"] = out["q"].astype(str)
    out.to_csv(os.path.join(PROC, "constraint_index_q.csv.gz"), index=False)
    # validation (i): price delay
    r += ["", "Validation (associations; frictions measured before outcomes):"]
    D = pd.read_pickle(os.path.join(CACHE, "delay_panel.pkl"))
    Zy = Z.assign(year=Z["q"].dt.year + 1).groupby(["symbol", "year"])["index"].mean().rename("index_prev").reset_index()
    Dv = D.merge(Zy, on=["symbol", "year"], how="inner").dropna(subset=["delay"])
    Dv["ys"] = Dv["year"].astype(str)
    t = coef_table(feols(Dv, "delay ~ index_prev | ys", cluster="symbol"))
    r.append(f"  (i) price delay D1 (year y) on mean index of year y-1, year FE: {t.loc['index_prev', 'b']:+.4f} "
             f"(se {t.loc['index_prev', 'se']:.4f}, t {t.loc['index_prev', 't']:+.2f}); n {len(Dv)}; mean delay {Dv['delay'].mean():.3f}")
    t = coef_table(feols(Dv, "delay ~ index_prev | ys + symbol", cluster="symbol"))
    r.append(f"      with stock FE: {t.loc['index_prev', 'b']:+.4f} (se {t.loc['index_prev', 'se']:.4f})")
    # (ii) drift
    E = pd.read_pickle(os.path.join(CACHE, "event_outcomes.pkl"))
    E["q0"] = E["event_day"].dt.to_period("Q") - 1
    Zq = Z[["symbol", "q", "index"]].rename(columns={"q": "q0", "index": "index_prev"})
    Ev = E.merge(Zq, on=["symbol", "q0"], how="inner").dropna(subset=["bhar_w"])
    Ev["abs_bhar"] = Ev["bhar_w"].abs()
    Ev["qs"] = Ev["q"].astype(str); Ev["date_c"] = Ev["event_day"].astype(str)
    t = coef_table(feols(Ev, "abs_bhar ~ index_prev | qs", cluster="symbol+date_c"))
    r.append(f"  (ii) |BHAR[+2,+64]| on previous-quarter index, quarter FE: {t.loc['index_prev', 'b']:+.4f} "
             f"(se {t.loc['index_prev', 'se']:.4f}, t {t.loc['index_prev', 't']:+.2f}); n {len(Ev)}; mean |BHAR| {Ev['abs_bhar'].mean():.4f}")
    Eb = Ev[Ev["bad"] == True]
    t = coef_table(feols(Eb, "bhar_w ~ index_prev | qs", cluster="symbol+date_c"))
    r.append(f"       bad-news BHAR on index: {t.loc['index_prev', 'b']:+.4f} (se {t.loc['index_prev', 'se']:.4f}); n {len(Eb)}")
    Eg = Ev[Ev["good"] == True]
    t = coef_table(feols(Eg, "bhar_w ~ index_prev | qs", cluster="symbol+date_c"))
    r.append(f"       good-news BHAR on index: {t.loc['index_prev', 'b']:+.4f} (se {t.loc['index_prev', 'se']:.4f}); n {len(Eg)}")
    # (iii) F&O band width
    try:
        from h1_frictions import outcomes
        O = outcomes()
        Zb = Z[["symbol", "q", "index"]].copy(); Zb["q"] = Zb["q"] + 1
        B = O.merge(Zb, on=["symbol", "q"], how="inner").dropna(subset=["W"])
        B["qs"] = B["q"].astype(str)
        t = coef_table(feols(B, "W ~ index | qs", cluster="symbol+qs"))
        r.append(f"  (iii) F&O band width W on previous-quarter index: {t.loc['index', 'b']:+.3f} bp (se {t.loc['index', 'se']:.3f}); n {len(B)}")
    except Exception as ex:
        r.append(f"  (iii) not computed ({ex})")
    txt = "\n".join(r)
    open(os.path.join(OUT, "constraint_index.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
