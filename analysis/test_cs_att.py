"""Audit check (8 Nov 2026): does the Callaway-Sant'Anna implementation in h6_fno.py recover a known effect on simulated
data? Units by year 2015-2025; staggered cohorts; outcome trends depend on a base-year covariate that also predicts
treatment (so unconditional parallel trends fail and the outcome regression must correct it). True ATT = -0.10 from the
cohort year on; the year before the cohort is a transition year (excluded, as in the plan).
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import h6_fno as h6

rng = np.random.default_rng(11)
YEARS = h6.YEARS


class SimPanel:
    def __init__(self, Y, X):
        self.syms = pd.Index([f"s{i}" for i in range(Y.shape[0])]); self.years = YEARS
        self.Y = Y; self.X = [X]; self.col = {y: j for j, y in enumerate(YEARS)}


def simulate(n=800, att=-0.10):
    x = rng.normal(size=n)
    prob = 1 / (1 + np.exp(-(x - 1.0)))
    treated = rng.random(n) < prob
    g = np.full(n, np.nan)
    g[treated] = rng.choice([2018, 2020, 2022, 2024], treated.sum())
    T = len(YEARS)
    t = np.arange(T)
    Y = (rng.normal(0, 0.3, n)[:, None] + 0.05 * t[None, :] + 0.04 * x[:, None] * t[None, :]
         + rng.normal(0, 0.05, (n, T)))
    for i in np.where(treated)[0]:
        Y[i, np.array(YEARS) >= g[i]] += att
    X = np.repeat(x[:, None], T, axis=1)
    return SimPanel(Y, X), g


def main():
    est = []
    for rep in range(20):
        Pm, g = simulate()
        ctl = lambda gg, tt, g=g: ~np.isfinite(g) | (g > max(gg, tt) + 1)
        cen = np.full(len(g), np.inf)
        post, pre, _ = h6.aggregate(h6.cs_att(Pm, g, ctl, cen))
        est.append((post, pre))
    E = np.array(est)
    print(f"true ATT -0.100: mean post estimate {E[:, 0].mean():+.4f} (sd across replications {E[:, 0].std():.4f}); "
          f"mean pre-period estimate {E[:, 1].mean():+.4f}")
    # without the covariate the estimate should be biased (unconditional parallel trends fail)
    Pm, g = simulate()
    Pm.X = []
    ctl = lambda gg, tt, g=g: ~np.isfinite(g) | (g > max(gg, tt) + 1)
    post, pre, _ = h6.aggregate(h6.cs_att(Pm, g, ctl, np.full(len(g), np.inf)))
    print(f"without the covariate (should be biased): post {post:+.4f}, pre {pre:+.4f}")


if __name__ == "__main__":
    main()
