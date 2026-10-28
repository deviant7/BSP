"""Check that the threshold estimator recovers known bands on simulated data (no real data used).
1) Classic 3-regime TAR with known thresholds.  2) Basis simulated from the theoretical model (inventory dynamics)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from setar import fit_setar3

rng = np.random.default_rng(7)

# 1) known TAR: random walk inside [-30, 15] bp, mean reversion (rho = -0.4) toward the edge outside
T, gl, gu = 2500, -30.0, 15.0
m = np.zeros(T)
for t in range(1, T):
    x = m[t - 1]
    drift = -0.4 * (x - gu) if x > gu else (-0.4 * (x - gl) if x < gl else 0.0)
    m[t] = x + drift + rng.normal(0, 6)
res = fit_setar3(m[:-1], np.diff(m))
print("known TAR: true gL=-30, gU=15 | est gL=%.1f gU=%.1f | rho lower/middle/upper = %.2f/%.2f/%.2f | F=%.1f"
      % (res["gL"], res["gU"], res["rho_lower"], res["rho_middle"], res["rho_upper"], res["F_vs_linear"]))

# 2) basis from the model: u AR(1), arbitrage with inventory, c+ = 15, c_u = 10 (bp), Phi = gamma = 1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models_src", "modelC"))
PHI, GAMMA, CP, CU = 1.0, 1.0, 15.0, 10.0
def step(u, a_prev):
    m0 = (u - a_prev) / PHI
    if m0 - GAMMA * a_prev > CP:
        m = (GAMMA * u + CP) / (GAMMA * PHI + 1); return (m - CP) / GAMMA, m
    if m0 - GAMMA * a_prev < -CU:
        a = max(0.0, (u + PHI * CU) / (GAMMA * PHI + 1)); return a, (u - a) / PHI
    return a_prev, m0
u, a, ms = 10.0, 0.0, []
for t in range(3000):
    u = 10 + 0.9 * (u - 10) + rng.normal(0, 8)
    a, mm = step(u, a)
    ms.append(mm)
ms = np.array(ms)
res2 = fit_setar3(ms[:-1], np.diff(ms))
print("model basis: est gL=%.1f gU=%.1f | rho lower/middle/upper = %.2f/%.2f/%.2f | shares %.2f/%.2f/%.2f"
      % (res2["gL"], res2["gU"], res2["rho_lower"], res2["rho_middle"], res2["rho_upper"],
         res2["share_lower"], res2["share_middle"], res2["share_upper"]))
