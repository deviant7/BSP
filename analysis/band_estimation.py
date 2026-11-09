"""Band-estimation chapter (master plan §5; specifications PAP §11.13 C16). Descriptive estimation of the no-arbitrage band.

  Pooled 3-regime threshold model on stock-demeaned basis (non-ban days), fast grid search via sorted cumulative sums;
  wild-bootstrap (clustered by date) linearity test; stock-cluster bootstrap for thresholds; estimates by period and
  state; exponential and logistic STAR; observed-transition STR (utilisation, days to expiry, arbitrage-fund assets);
  per-stock threshold models and their relation to the H1 friction index.
Outputs analysis/output/band_estimation.txt (+ band_by_year.csv, band_per_stock.csv).
"""
import os, sys, time
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, PROC, CACHE, ROOT
from inference import feols, coef_table

OUT = os.path.join(ROOT, "analysis", "output")
BP = 1e4
rng = np.random.default_rng(16)
QGRID = np.arange(0.05, 0.9501, 0.01)
STT = [("to Mar 2023", None, "2023-04-01"), ("Apr 2023 - Sep 2024", "2023-04-01", "2024-10-01"),
       ("Oct 2024 - Mar 2026", "2024-10-01", "2026-04-01"), ("from Apr 2026", "2026-04-01", None)]


# ----------------------------------------------------------------------------------------------------------------------
def load():
    S = basis_sample()
    S = S[~S["ban"] & S["dm"].notna() & S["m_lag"].notna()].copy()
    nb = basis_sample()
    nb = nb[~nb["ban"]]
    mu = nb.groupby("symbol")["m"].median()
    cnt = nb.groupby("symbol").size()
    S = S[S["symbol"].isin(cnt[cnt >= 100].index)]
    S["x"] = (S["m_lag"] - S["symbol"].map(mu)) * BP
    S["d"] = S["dm"] * BP
    S["month"] = S["date"].dt.to_period("M")
    A = pd.read_csv(os.path.join(PROC, "amfi_arbitrage_monthly.csv"))
    A["month"] = pd.PeriodIndex(A["month"], freq="M")
    S = S.merge(A[["month", "aum"]], on="month", how="left")
    S["laum"] = np.log(S["aum"])
    return S.reset_index(drop=True)


# ----------------------------------------------------------------------------------------------------------------------
class SortedData:
    """x sorted once; cumulative weighted sums for any y and weights give regime OLS SSRs in O(1) per threshold pair."""

    def __init__(self, x, cand):
        self.order = np.argsort(x, kind="mergesort")
        self.xs = x[self.order]
        self.cand = cand
        # index of first element > g (lower regime = [0, iL), upper = [iU, n))
        self.idx_lo = np.searchsorted(self.xs, cand, side="left")     # x < gL
        self.idx_hi = np.searchsorted(self.xs, cand, side="right")    # x > gU starts here

    def cums(self, y, w=None):
        ys = y[self.order]
        w = np.ones_like(ys) if w is None else w[self.order]
        xs = self.xs
        z = lambda a: np.concatenate([[0.0], np.cumsum(a)])
        return dict(n=z(w), x=z(w * xs), y=z(w * ys), xx=z(w * xs * xs), xy=z(w * xs * ys), yy=z(w * ys * ys))


def _ssr(C, a, b):
    """SSR of weighted OLS of y on [1, x] over sorted positions [a, b) (arrays allowed)."""
    n = C["n"][b] - C["n"][a]
    sx = C["x"][b] - C["x"][a]; sy = C["y"][b] - C["y"][a]
    sxx = C["xx"][b] - C["xx"][a]; sxy = C["xy"][b] - C["xy"][a]; syy = C["yy"][b] - C["yy"][a]
    with np.errstate(all="ignore"):
        vx = sxx - sx * sx / n
        cxy = sxy - sx * sy / n
        ssr = syy - sy * sy / n - np.where(vx > 0, cxy * cxy / vx, 0.0)
    return ssr, n


def _coef(C, a, b):
    n = C["n"][b] - C["n"][a]
    sx = C["x"][b] - C["x"][a]; sy = C["y"][b] - C["y"][a]
    sxx = C["xx"][b] - C["xx"][a]; sxy = C["xy"][b] - C["xy"][a]
    rho = (sxy - sx * sy / n) / (sxx - sx * sx / n)
    return (sy - rho * sx) / n, rho


def setar_fit(D, y, w=None, trim=0.10, mid_min=0.20, full=True):
    C = D.cums(y, w)
    N = C["n"][-1]
    K = len(D.cand)
    iL = D.idx_lo[:, None] * np.ones((1, K), int)       # lower regime ends at iL (gL = cand[i])
    iU = np.ones((K, 1), int) * D.idx_hi[None, :]       # upper regime starts at iU (gU = cand[j])
    valid = np.triu(np.ones((K, K), bool), 1)
    s1, n1 = _ssr(C, 0, iL)
    s3, n3 = _ssr(C, iU, len(D.xs))
    s2, n2 = _ssr(C, iL, iU)
    ok = valid & (n1 >= trim * N) & (n3 >= trim * N) & (n2 >= mid_min * N)
    tot = np.where(ok, s1 + s2 + s3, np.inf)
    i, j = np.unravel_index(np.argmin(tot), tot.shape)
    ssr = tot[i, j]
    slin, _ = _ssr(C, 0, len(D.xs))
    F = ((slin - ssr) / 4) / (ssr / (N - 6))
    out = dict(gL=D.cand[i], gU=D.cand[j], ssr=ssr, ssr_lin=slin, F=F, n=N)
    if full:
        for name, a, b in (("lower", 0, D.idx_lo[i]), ("middle", D.idx_lo[i], D.idx_hi[j]), ("upper", D.idx_hi[j], len(D.xs))):
            aa, rr = _coef(C, a, b)
            out[f"a_{name}"], out[f"rho_{name}"] = aa, rr
            out[f"share_{name}"] = (C["n"][b] - C["n"][a]) / N
            out[f"hl_{name}"] = np.log(0.5) / np.log(1 + rr) if -1 < rr < 0 else np.inf
    return out


def fmt_setar(o, lab):
    return (f"  {lab:34s} n {int(o['n']):7d}; gL {o['gL']:+6.1f}, gU {o['gU']:+6.1f} (width {o['gU'] - o['gL']:5.1f}); "
            f"rho lower/middle/upper {o['rho_lower']:+.3f}/{o['rho_middle']:+.3f}/{o['rho_upper']:+.3f}; "
            f"shares {o['share_lower']:.2f}/{o['share_middle']:.2f}/{o['share_upper']:.2f}; F {o['F']:.1f}")


def setar_on(df, lab):
    x, d = df["x"].values, df["d"].values
    D = SortedData(x, np.unique(np.quantile(x, QGRID)))
    o = setar_fit(D, d)
    return o, fmt_setar(o, lab)


# ----------------------------------------------------------------------------------------------------------------------
def linearity_boot(df, B=199):
    """Wild bootstrap (Rademacher, clustered by date) of the sup-F statistic under the linear null."""
    x, d = df["x"].values, df["d"].values
    D = SortedData(x, np.unique(np.quantile(x, QGRID)))
    o = setar_fit(D, d, full=False)
    X = np.c_[np.ones_like(x), x]
    b = np.linalg.lstsq(X, d, rcond=None)[0]
    fit, e = X @ b, d - X @ b
    codes = pd.factorize(df["date"])[0]
    G = codes.max() + 1
    Fs = []
    for _ in range(B):
        eta = rng.choice([-1.0, 1.0], G)[codes]
        Fs.append(setar_fit(D, fit + e * eta, full=False)["F"])
    Fs = np.array(Fs)
    return o["F"], float((Fs >= o["F"]).mean()), np.percentile(Fs, 95)


def threshold_boot(df, B=199):
    """Stock-cluster bootstrap of thresholds and regime slopes (weights = multiplicity of each stock in the draw)."""
    x, d = df["x"].values, df["d"].values
    D = SortedData(x, np.unique(np.quantile(x, QGRID)))
    codes = pd.factorize(df["symbol"])[0]
    G = codes.max() + 1
    res = []
    for _ in range(B):
        m = np.bincount(rng.integers(0, G, G), minlength=G).astype(float)
        o = setar_fit(D, d, w=m[codes])
        res.append((o["gL"], o["gU"], o["rho_lower"], o["rho_middle"], o["rho_upper"]))
    return pd.DataFrame(res, columns=["gL", "gU", "rho_lower", "rho_middle", "rho_upper"])


# ----------------------------------------------------------------------------------------------------------------------
def ols_ssr(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    return float(r @ r), b


def star(df):
    """Exponential and logistic STAR in x (profile over gamma, c). Returns dicts with SSR, BIC and coefficients."""
    x, d = df["x"].values, df["d"].values
    n = len(x)
    sx = x.std()
    gam = np.exp(np.linspace(np.log(0.05), np.log(50), 25))
    out = {}
    best = None
    for c in np.quantile(x, [0.3, 0.4, 0.5, 0.6, 0.7]):
        for g in gam:
            G = 1 - np.exp(-g * ((x - c) / sx) ** 2)
            s, b = ols_ssr(np.c_[np.ones(n), x, x * G], d)
            if best is None or s < best[0]:
                best = (s, g, c, b)
    s, g, c, b = best
    out["ESTAR"] = dict(ssr=s, gamma=g, c=c, a=b[0], rho_inner=b[1], rho_outer=b[1] + b[2], k=5)
    best = None
    for c in np.quantile(x, np.arange(0.1, 0.91, 0.1)):
        for g in gam:
            G = 1 / (1 + np.exp(-g * (x - c) / sx))
            s, b = ols_ssr(np.c_[np.ones(n), x, x * G], d)
            if best is None or s < best[0]:
                best = (s, g, c, b)
    s, g, c, b = best
    out["LSTAR"] = dict(ssr=s, gamma=g, c=c, a=b[0], rho_low=b[1], rho_high=b[1] + b[2], k=5)
    return out


def bic(ssr, n, k):
    return n * np.log(ssr / n) + k * np.log(n)


def lst_test(df):
    d = df[["d", "x", "symbol", "date"]].copy()
    d["x2"] = d["x"] ** 2 / 100; d["x3"] = d["x"] ** 3 / 1e4
    fit = feols(d, "d ~ x + x2 + x3 | symbol + date")
    names = list(fit.coef().index)
    V = np.asarray(fit._vcov); b = np.asarray(fit.coef().values)
    ix = [names.index("x2"), names.index("x3")]
    W = float(b[ix] @ np.linalg.inv(V[np.ix_(ix, ix)]) @ b[ix])
    from scipy import stats
    t = coef_table(fit)
    return W, float(stats.chi2.sf(W, 2)), t


def str_observed(df, s_col, lab):
    """Delta m = a + [rho0 + rho1 G(s)] x; logistic G in standardised s; profile (gamma, c) by OLS, then FE + clustered SE."""
    d = df.dropna(subset=[s_col]).copy()
    x, y, s = d["x"].values, d["d"].values, d[s_col].values
    z = (s - s.mean()) / s.std()
    n = len(x)
    best = None
    for c in np.quantile(z, np.arange(0.1, 0.91, 0.1)):
        for g in [0.5, 1, 2, 5, 10, 25, 50]:
            G = 1 / (1 + np.exp(-g * (z - c)))
            ss, b = ols_ssr(np.c_[np.ones(n), x, x * G], y)
            if best is None or ss < best[0]:
                best = (ss, g, c)
    ss, g, c = best
    d["G"] = 1 / (1 + np.exp(-g * (z - c)))
    d["xG"] = d["x"] * d["G"]
    t = coef_table(feols(d, "d ~ x + xG | symbol + date"))
    s_at_c = c * s.std() + s.mean()
    return (f"  transition {lab:34s} gamma {g:5.1f}, location (s) {s_at_c:+.3f}; rho0 {t.loc['x', 'b']:+.3f} "
            f"({t.loc['x', 'se']:.3f}); rho1 {t.loc['xG', 'b']:+.3f} ({t.loc['xG', 'se']:.3f}, t {t.loc['xG', 't']:+.2f}); "
            f"n {n}")


# ----------------------------------------------------------------------------------------------------------------------
def per_stock(df):
    rows = []
    for s, g in df.groupby("symbol"):
        if len(g) < 500:
            continue
        x, d = g["x"].values, g["d"].values
        D = SortedData(x, np.unique(np.quantile(x, np.arange(0.05, 0.951, 0.025))))
        o = setar_fit(D, d)
        rows.append(dict(symbol=s, n=len(g), gL=o["gL"], gU=o["gU"], width=o["gU"] - o["gL"], rho_lower=o["rho_lower"],
                         rho_middle=o["rho_middle"], rho_upper=o["rho_upper"], F=o["F"]))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    S = load()
    r = ["Band-estimation chapter (PAP §11.13 C16). Non-ban days; x = m_(t-1) - stock median (bp); d = Delta m_t (bp).",
         f"Observations {len(S)}, stocks {S['symbol'].nunique()}, {S['date'].min().date()} to {S['date'].max().date()}; "
         f"x percentiles p5/p25/p50/p75/p95: " + "/".join(f"{v:.1f}" for v in np.percentile(S['x'], [5, 25, 50, 75, 95])), ""]
    o, line = setar_on(S, "POOLED, full sample")
    r.append("1. Pooled 3-regime threshold model")
    r.append(line)
    r.append(f"     intercepts lower/middle/upper {o['a_lower']:+.2f}/{o['a_middle']:+.2f}/{o['a_upper']:+.2f}; "
             f"half-lives (days) {o['hl_lower']:.2f}/{o['hl_middle']:.2f}/{o['hl_upper']:.2f}")
    F, p, c95 = linearity_boot(S)
    r.append(f"  linearity test: sup-F {F:.1f}; wild-bootstrap (date clusters, 199 draws) p = {p:.3f}; 95% critical value {c95:.1f}")
    TB = threshold_boot(S)
    r.append("  stock-cluster bootstrap (199 draws), 2.5/97.5 percentiles: " +
             "; ".join(f"{c} [{TB[c].quantile(.025):+.2f}, {TB[c].quantile(.975):+.2f}]" for c in TB.columns))
    # 2. by period and state
    r += ["", "2. Threshold model by period and state"]
    yrows = []
    for yv, g in S.groupby(S["date"].dt.year):
        o, line = setar_on(g, f"year {yv}")
        r.append(line); yrows.append(dict(year=yv, **{k: o[k] for k in ["gL", "gU", "rho_lower", "rho_middle", "rho_upper", "F", "n"]}))
    pd.DataFrame(yrows).to_csv(os.path.join(OUT, "band_by_year.csv"), index=False)
    for lab, a, b in STT:
        g = S
        if a: g = g[g["date"] >= a]
        if b: g = g[g["date"] < b]
        r.append(setar_on(g, f"STT period {lab}")[1])
    S["dexp_t"] = pd.qcut(S["d_exp"].rank(method="first"), 3, labels=["near expiry", "middle", "far from expiry"])
    for k, g in S.groupby("dexp_t", observed=True):
        r.append(setar_on(g, f"days to expiry: {k} ({g['d_exp'].min()}-{g['d_exp'].max()})")[1])
    S["om_t"] = pd.qcut(S["omega_lag"].rank(method="first"), 3, labels=["low", "middle", "high"])
    for k, g in S.groupby("om_t", observed=True):
        r.append(setar_on(g, f"utilisation tercile: {k} ({g['omega_lag'].min():.2f}-{g['omega_lag'].max():.2f})")[1])
    SA = S.dropna(subset=["laum"]).copy()
    SA["aum_t"] = pd.qcut(SA["laum"].rank(method="first"), 3, labels=["low", "middle", "high"])
    for k, g in SA.groupby("aum_t", observed=True):
        r.append(setar_on(g, f"arbitrage-fund assets: {k} (descriptive; orders time)")[1])
    # 3. smooth transition
    r += ["", "3. Smooth-transition models (pooled, full sample)"]
    st = star(S)
    n = len(S)
    o_full, _ = setar_on(S, "x")
    r.append(f"  linear: SSR {o_full['ssr_lin']:.4e}, BIC {bic(o_full['ssr_lin'], n, 2):.1f}")
    r.append(f"  3-regime threshold: SSR {o_full['ssr']:.4e}, BIC {bic(o_full['ssr'], n, 8):.1f}")
    e = st["ESTAR"]
    r.append(f"  ESTAR: gamma {e['gamma']:.3f}, centre {e['c']:+.2f}; rho inner {e['rho_inner']:+.3f}, outer {e['rho_outer']:+.3f}; "
             f"SSR {e['ssr']:.4e}, BIC {bic(e['ssr'], n, e['k']):.1f}")
    l = st["LSTAR"]
    r.append(f"  LSTAR in x: gamma {l['gamma']:.3f}, location {l['c']:+.2f}; rho below {l['rho_low']:+.3f}, above {l['rho_high']:+.3f}; "
             f"SSR {l['ssr']:.4e}, BIC {bic(l['ssr'], n, l['k']):.1f}")
    W, pW, t = lst_test(S)
    r.append(f"  auxiliary nonlinearity test (d on x, x^2/100, x^3/1e4, stock and date FE, two-way clustered): "
             f"x2 {t.loc['x2', 'b']:+.4f} ({t.loc['x2', 'se']:.4f}), x3 {t.loc['x3', 'b']:+.5f} ({t.loc['x3', 'se']:.5f}); "
             f"Wald chi2(2) {W:.1f}, p = {pW:.3g}")
    # 4. observed transitions
    r += ["", "4. Observed-transition models: d = a + [rho0 + rho1 G(s)] x, logistic G (stock and date FE; two-way clustered SE)"]
    r.append(str_observed(S, "omega_lag", "utilisation omega_(t-1)"))
    r.append(str_observed(S, "d_exp", "trading days to expiry"))
    r.append(str_observed(S, "laum", "log arbitrage-fund assets (from Apr 2018)"))
    # 5. per stock
    P = per_stock(S)
    P.to_csv(os.path.join(OUT, "band_per_stock.csv"), index=False)
    r += ["", f"5. Per-stock threshold models (non-ban days, >= 500 obs): stocks {len(P)}",
          "  percentiles p10/p25/p50/p75/p90: " + "; ".join(
              f"{c} " + "/".join(f"{v:+.1f}" for v in np.percentile(P[c], [10, 25, 50, 75, 90])) for c in ["gL", "gU", "width"]),
          "  regime slopes (median): lower {:+.3f}, middle {:+.3f}, upper {:+.3f}".format(
              P["rho_lower"].median(), P["rho_middle"].median(), P["rho_upper"].median())]
    try:
        from h1_frictions import build_index, FR
        Fq = pd.read_pickle(os.path.join(CACHE, "frictions_q.pkl"))
        Z, v, _ = build_index(Fq, FR)
        zi = Z.groupby("symbol")["index"].mean().rename("index")
        Q = P.merge(zi, left_on="symbol", right_index=True, how="inner")
        import statsmodels.api as sm
        f = sm.OLS(Q["width"], sm.add_constant(Q["index"])).fit(cov_type="HC1")
        r.append(f"  width on stock-mean friction index (HC1): {f.params['index']:+.2f} bp per unit (se {f.bse['index']:.2f}); "
                 f"n {len(Q)}; corr {Q[['width', 'index']].corr().iloc[0, 1]:.2f}")
    except Exception as ex:
        r.append(f"  friction-index relation not computed ({ex})")
    r.append(f"\n(run time {time.time() - t0:.0f} s)")
    txt = "\n".join(r)
    open(os.path.join(OUT, "band_estimation.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
