"""Check the inference helpers on simulated panels with known coefficients (no real data used).
1) Two-way FE regression with regime-by-treatment interactions: estimates should recover the true betas and deltas, and
   two-way clustered SEs should give about 5% rejection of true nulls over replications.
2) Holm correction on known p-values."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from inference import feols, coef_table, lincomb, holm

rng = np.random.default_rng(11)


def sim(N=150, T=300, d_up=0.10, d_lo=-0.05):
    sym = np.repeat(np.arange(N), T); date = np.tile(np.arange(T), N)
    a_i = rng.normal(0, 1, N)[sym]; l_t = rng.normal(0, 1, T)[date]
    x = rng.normal(0, 1, N * T) + 0.5 * rng.normal(0, 1, T)[date]        # regressor correlated within date
    up, lo = x > 0.84, x < -0.84
    mid = ~up & ~lo
    ban = rng.random(N * T) < 0.03
    beta = {"up": -0.3, "mid": -0.05, "lo": -0.25}
    y = (a_i + l_t + x * (beta["up"] * up + beta["mid"] * mid + beta["lo"] * lo)
         + x * ban * (d_up * up + d_lo * lo)
         + rng.normal(0, 1, N * T) + 0.7 * rng.normal(0, 1, T)[date] * rng.normal(0, 1, N)[sym])
    df = pd.DataFrame({"symbol": sym, "date": date, "y": y})
    for r, msk in (("up", up), ("mid", mid), ("lo", lo)):
        df[f"x_{r}"] = x * msk
        df[f"xb_{r}"] = x * msk * ban
    return df


df = sim()
fit = feols(df, "y ~ x_up + x_mid + x_lo + xb_up + xb_mid + xb_lo | symbol + date")
print(coef_table(fit).round(4))
b, se = lincomb(fit, {"xb_up": 1, "xb_lo": -1})
print(f"delta_up - delta_lo: {b:.4f} (se {se:.4f}); true 0.15")

# size of the test for a true null (delta_mid = 0) over replications
rej = 0
R = 40
for _ in range(R):
    t = coef_table(feols(sim(N=80, T=150), "y ~ x_up + x_mid + x_lo + xb_up + xb_mid + xb_lo | symbol + date"))
    rej += t.loc["xb_mid", "p_two"] < 0.05
print(f"rejection rate of a true null at 5% over {R} replications: {rej / R:.3f}")
print(holm({"H7": 0.001, "H8": 0.04, "H3": 0.03, "H6": 0.2}))
