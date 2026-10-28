"""Three-regime threshold autoregression for the basis (band estimation).

    dm_t = a_r + rho_r * m_{t-1} + e_t,   regime r = lower (m_{t-1} < gL), middle (gL <= m_{t-1} <= gU), upper (m_{t-1} > gU)

Thresholds are chosen by grid search over quantiles of m_{t-1} to minimise the sum of squared residuals, with at least
`trim` of the observations in each outer regime and `mid_min` in the middle regime (cf. Aggarwal 2015; Shankar et al. 2015).
Inputs are arrays of lagged levels and first differences that already respect contract continuity (no differences across
contract rolls or across gaps in the sample).
"""
import numpy as np


def _ols_ssr(x, y):
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    return float(r @ r), beta


def fit_setar3(mlag, dm, qgrid=np.arange(0.05, 0.951, 0.025), trim=0.10, mid_min=0.20):
    mlag, dm = np.asarray(mlag, float), np.asarray(dm, float)
    ok = np.isfinite(mlag) & np.isfinite(dm)
    mlag, dm = mlag[ok], dm[ok]
    n = len(mlag)
    cand = np.unique(np.quantile(mlag, qgrid))
    best = None
    for i, gl in enumerate(cand):
        lo = mlag < gl
        if lo.mean() < trim:
            continue
        for gu in cand[i + 1:]:
            hi = mlag > gu
            mid = ~lo & ~hi
            if hi.mean() < trim or mid.mean() < mid_min:
                continue
            ssr = 0.0
            for msk in (lo, mid, hi):
                s, _ = _ols_ssr(mlag[msk], dm[msk])
                ssr += s
            if best is None or ssr < best[0]:
                best = (ssr, gl, gu)
    if best is None:
        return None
    ssr, gl, gu = best
    out = {"n": n, "gL": gl, "gU": gu, "ssr": ssr}
    for name, msk in (("lower", mlag < gl), ("middle", (mlag >= gl) & (mlag <= gu)), ("upper", mlag > gu)):
        _, b = _ols_ssr(mlag[msk], dm[msk])
        out[f"a_{name}"], out[f"rho_{name}"], out[f"share_{name}"] = b[0], b[1], msk.mean()
        r = 1 + b[1]
        out[f"halflife_{name}"] = np.log(0.5) / np.log(r) if 0 < r < 1 else np.inf
    s_lin, _ = _ols_ssr(mlag, dm)
    out["F_vs_linear"] = ((s_lin - ssr) / 4) / (ssr / (n - 6))
    return out
