"""Inference helpers for the pre-registered tests (PAP §7): two-way fixed effects with two-way clustered standard errors
(via pyfixest), one-sided p-values, intersection-union tests and the Holm correction.
Validated on simulated data in analysis/test_inference.py."""
import numpy as np
import pandas as pd
from scipy import stats


def feols(df, formula, cluster="symbol+date"):
    import pyfixest as pf
    return pf.feols(formula, data=df, vcov={"CRV1": cluster})


def coef_table(fit):
    t = fit.tidy()
    return t[["Estimate", "Std. Error", "t value", "Pr(>|t|)"]].rename(
        columns={"Estimate": "b", "Std. Error": "se", "t value": "t", "Pr(>|t|)": "p_two"})


def one_sided(b, se, df, direction=">"):
    """p-value for H1: beta > 0 (direction '>') or beta < 0 ('<'), t distribution with df degrees of freedom."""
    t = b / se
    return float(stats.t.sf(t, df)) if direction == ">" else float(stats.t.cdf(t, df))


def lincomb(fit, weights):
    """Estimate and standard error of sum_j w_j * beta_j using the fitted (clustered) covariance matrix."""
    names = list(fit.coef().index)
    w = np.array([weights.get(n, 0.0) for n in names])
    V = np.asarray(fit._vcov)
    b = np.asarray(fit.coef().values)
    return float(w @ b), float(np.sqrt(w @ V @ w))


def cluster_df(fit, df, cluster_cols):
    """Small-sample degrees of freedom for clustered inference: min(G) - 1 over the clustering dimensions."""
    return int(min(df[c].nunique() for c in cluster_cols) - 1)


def holm(pvals, alpha=0.05):
    """Holm step-down. pvals: dict name -> p. Returns DataFrame with adjusted p-values and decisions."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running, stop = [], 0.0, False
    for j, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - j) * p))
        running = adj
        reject = (not stop) and p <= alpha / (m - j)
        if not reject:
            stop = True
        out.append((k, p, adj, reject))
    return pd.DataFrame(out, columns=["hypothesis", "p", "p_holm", "reject_5pct"])
