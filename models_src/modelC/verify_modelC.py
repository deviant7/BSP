"""Numerical verification and illustration of Model C (constrained arbitrage under Indian limits).

Checks every closed form in the model against a brute-force equilibrium solver, and produces the
illustrative simulations used in the figures. Parameters are illustrative (units: basis points),
NOT calibrated estimates.
Run:  python3 verify_modelC.py   (writes figs/*.pdf and prints a check report)
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20261028)
TOL = 1e-7

# ---------------------------------------------------------------- primitives
PHI = 1.0      # Phi: combined liquidity of outside traders, 1/Phi = 1/psi_F + 1/psi_S
GAMMA = 1.0    # gamma = alpha * sigma^2 (risk-bearing cost of the arbitrage sector)
C_PLUS = 15.0  # cost of opening cash-and-carry (bp)
C_MINUS = 60.0 # cost of reverse arbitrage = c + c_s (bp) (static section only)
C_U = 10.0     # cost of unwinding cash-and-carry inventory (bp)


def best_response_static(m):
    """Arbitrage position given basis m (no inventory): Prop 1."""
    if m > C_PLUS:
        return (m - C_PLUS) / GAMMA
    if m < -C_MINUS:
        return (m + C_MINUS) / GAMMA
    return 0.0


def best_response_dyn(m, a_prev, ban=False):
    """Arbitrage position given basis m and inventory a_prev >= 0; a >= 0 (no reverse arbitrage).
    Ban = reduce-only: a <= a_prev."""
    if m - GAMMA * a_prev > C_PLUS and not ban:
        return (m - C_PLUS) / GAMMA
    if m - GAMMA * a_prev < -C_U:
        return max(0.0, (m + C_U) / GAMMA)
    return a_prev


def solve_fixed_point(br, u, *args):
    """Solve a = br((u - a)/PHI, *args) by bisection; br(m(a)) is non-increasing in a."""
    g = lambda a: br((u - a) / PHI, *args) - a          # strictly decreasing in a
    lo, hi = -1e4, 1e4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    a = 0.5 * (lo + hi)
    return a, (u - a) / PHI


report = []

# ---------------------------------------------------------------- Prop 1 (static band)
def m_closed_static(u):
    if u > PHI * C_PLUS:
        return (GAMMA * u + C_PLUS) / (GAMMA * PHI + 1)
    if u < -PHI * C_MINUS:
        return (GAMMA * u - C_MINUS) / (GAMMA * PHI + 1)
    return u / PHI

us = np.linspace(-200, 200, 2001)
err = max(abs(solve_fixed_point(best_response_static, u)[1] - m_closed_static(u)) for u in us)
report.append(("Prop 1 static band closed form vs solver (max abs err, bp)", err, err < 1e-6))

# ---------------------------------------------------------------- Prop 3 (inventory-dependent no-trade region)
def m_closed_dyn(u, a_prev, ban=False):
    m0 = (u - a_prev) / PHI
    if (m0 - GAMMA * a_prev > C_PLUS) and not ban:
        return (GAMMA * u + C_PLUS) / (GAMMA * PHI + 1)
    if m0 - GAMMA * a_prev < -C_U:
        a = max(0.0, (u + PHI * C_U) / (GAMMA * PHI + 1))
        return (u - a) / PHI
    return m0

err_n = err_b = 0.0
for a_prev in [0.0, 5.0, 20.0, 60.0]:
    for u in us:
        err_n = max(err_n, abs(solve_fixed_point(best_response_dyn, u, a_prev, False)[1] - m_closed_dyn(u, a_prev, False)))
        err_b = max(err_b, abs(solve_fixed_point(best_response_dyn, u, a_prev, True)[1] - m_closed_dyn(u, a_prev, True)))
report.append(("Prop 3 dynamic step (normal) closed form vs solver", err_n, err_n < 1e-6))
report.append(("Prop 4 dynamic step (ban) closed form vs solver", err_b, err_b < 1e-6))

# Prop 4: in a ban, floor = gamma*a_t - c_u while a_t > 0; no ceiling (slope 1/PHI above)
a_prev = 40.0
floor_ok = True
for u in us:
    a, m = solve_fixed_point(best_response_dyn, u, a_prev, True)
    if a > 1e-9 and m < GAMMA * a - C_U - 1e-6:
        floor_ok = False
slope_hi = (m_closed_dyn(150, a_prev, True) - m_closed_dyn(149, a_prev, True))
report.append(("Prop 4 floor gamma*a - c_u respected in ban", 0.0, floor_ok))
report.append(("Prop 4 slope above no-trade region in ban = 1/PHI", slope_hi, abs(slope_hi - 1 / PHI) < 1e-9))
slope_norm = (m_closed_dyn(150, a_prev, False) - m_closed_dyn(149, a_prev, False))
report.append(("Normal-times slope beyond upper edge = gamma/(gamma*PHI+1)", slope_norm,
               abs(slope_norm - GAMMA / (GAMMA * PHI + 1)) < 1e-9))


# Lemma (ban weakly raises m for the same u) and Prop 6 (one-period level comparison)
LAM_CHECK = 0.5
lemma_ok, mono_ok, pos0_ok, neg_far_ok = True, True, True, True
for a_prev in [0.0, 10.0, 30.0, 60.0]:
    for u0 in np.linspace(-50, 150, 81):
        if m_closed_dyn(u0, a_prev, True) < m_closed_dyn(u0, a_prev, False) - 1e-9:
            lemma_ok = False
        eps = np.linspace(0, 200, 401)
        diff = np.array([m_closed_dyn(u0 - LAM_CHECK * e, a_prev, True) - m_closed_dyn(u0 + e, a_prev, False) for e in eps])
        if np.any(np.diff(diff) > 1e-9): mono_ok = False
        if diff[0] < -1e-9: pos0_ok = False
        if diff[-1] >= 0: neg_far_ok = False
report.append(("Lemma: for the same u, m(ban) >= m(normal)", 0.0, lemma_ok))
report.append(("Prop 6: m^B - m^N non-increasing in new-exposure demand", 0.0, mono_ok))
report.append(("Prop 6: m^B - m^N >= 0 at zero new demand, < 0 for large new demand", 0.0, pos0_ok and neg_far_ok))

# ---------------------------------------------------------------- Prop 11 (Miller / F&O inclusion)
def miller_price(v, delta, Q, k, cs, n=200001):
    """Price with valuations ~U[v-delta, v+delta], demand k(v_i-p) if long, k(v_i-p+cs) if v_i<p-cs."""
    x = np.linspace(v - delta, v + delta, n)
    def excess(p):
        d = np.where(x > p, k * (x - p), 0.0) + np.where(x < p - cs, k * (x - p + cs), 0.0)
        return d.mean() - Q
    lo, hi = v - delta - 10 * Q / k - 10, v + delta + 10
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if excess(mid) > 0 else (lo, mid)
    return 0.5 * (lo + hi)

v, delta, Q, k = 100.0, 20.0, 2.0, 1.0
p_ns = miller_price(v, delta, Q, k, cs=1e9)
p_u = miller_price(v, delta, Q, k, cs=0.0)
closed_ns = v + delta - 2 * np.sqrt(delta * Q / k)
closed_gap = (np.sqrt(delta) - np.sqrt(Q / k)) ** 2
report.append(("Prop 11 no-short price closed form", abs(p_ns - closed_ns), abs(p_ns - closed_ns) < 1e-3))
report.append(("Prop 11 overpricing (sqrt(delta)-sqrt(Q/k))^2", abs((p_ns - p_u) - closed_gap), abs((p_ns - p_u) - closed_gap) < 1e-3))
pc = [miller_price(v, delta, Q, k, cs) for cs in [0, 2, 5, 10, 20, 40, 1e9]]
report.append(("Prop 11 price non-decreasing in short cost c_s", 0.0, all(np.diff(pc) >= -1e-6)))

# ---------------------------------------------------------------- dynamic simulation (Props 4-6 illustration)
RHO, MU_U, SD_N, SD_C, LAM = 0.9, 25.0, 6.0, 6.0, 0.5

def simulate(T, ban_start=None, ban_len=0, shocks=None, a0=None, u0=None, mu_new=0.0):
    """mu_new: mean daily flow of NEW-exposure futures demand during the ban window (spills to cash in a ban,
    enters futures otherwise). Shocks en, ec are mean-zero."""
    en, ec = shocks
    u = np.empty(T); a = np.empty(T); m = np.empty(T)
    u_prev = MU_U if u0 is None else u0
    a_prev = 0.0 if a0 is None else a0
    for t in range(T):
        ban = ban_start is not None and ban_start <= t < ban_start + ban_len
        in_win = ban_start is not None and ban_start <= t < ban_start + ban_len
        flow = en[t] + (mu_new if in_win else 0.0)
        du_new = (-LAM * flow) if ban else flow             # new-exposure demand spills to cash in a ban
        u[t] = MU_U + RHO * (u_prev - MU_U) + du_new + ec[t]
        a[t], m[t] = solve_fixed_point(best_response_dyn, u[t], a_prev, ban)
        u_prev, a_prev = u[t], a[t]
    return u, a, m

# one illustrative path
T, B0, BL = 260, 120, 40
sh = (rng.normal(0, SD_N, T), rng.normal(0, SD_C, T))
_, a_n, m_n = simulate(T, None, 0, sh)
_, a_b, m_b = simulate(T, B0, BL, sh)
fig, ax = plt.subplots(2, 1, figsize=(7.5, 5.2), sharex=True)
ax[0].plot(m_n, color="0.55", lw=1.2, label="no ban (same shocks)")
ax[0].plot(m_b, color="#1F3A5F", lw=1.4, label="ban on days 120-159")
ax[0].axvspan(B0, B0 + BL, color="#C9D6E8", alpha=0.6)
ax[0].set_ylabel("basis m (bp)"); ax[0].legend(frameon=False, fontsize=8)
ax[1].plot(a_n, color="0.55", lw=1.2); ax[1].plot(a_b, color="#1F3A5F", lw=1.4)
ax[1].axvspan(B0, B0 + BL, color="#C9D6E8", alpha=0.6)
ax[1].set_ylabel("arbitrage inventory a"); ax[1].set_xlabel("day")
fig.tight_layout(); fig.savefig("figs/fig_path.pdf"); plt.close(fig)

# paired Monte Carlo: effect of a ban on basis level and on upper/lower tails, by shock composition
def episode(share_new, mu_new=0.0):
    Tn = 200
    sd_n, sd_c = SD_N * np.sqrt(2 * share_new), SD_C * np.sqrt(2 * (1 - share_new))
    sh = (rng.normal(0, sd_n, Tn), rng.normal(0, sd_c, Tn))
    _, _, mn = simulate(Tn, 150, 40, sh, mu_new=mu_new) if False else simulate_noban(Tn, sh, mu_new)
    _, _, mb = simulate(Tn, 150, 40, sh, mu_new=mu_new)
    w = slice(150, 190)
    return mb[w].mean() - mn[w].mean(), np.percentile(mb[w], 90) - np.percentile(mn[w], 90), \
           np.percentile(mb[w], 10) - np.percentile(mn[w], 10)

def simulate_noban(Tn, sh, mu_new):
    """Counterfactual: same shocks and same new-exposure flow on days 150-189, but no ban (flow enters futures)."""
    en, ec = sh
    en = en.copy(); en[150:190] += mu_new
    return simulate(Tn, None, 0, (en, ec))

print("\nPaired MC (ban minus no-ban, same shocks; bp): share_new, mu_new, d_mean, d_p90, d_p10")
rows = []
for s_ in [0.5]:
    for mu in [0.0, 1.0, 2.0, 4.0]:
        eff = np.array([episode(s_, mu) for _ in range(300)])
        rows.append((s_, mu, *eff.mean(axis=0)))
        print("  %.1f  %4.1f  %+7.2f  %+7.2f  %+7.2f" % rows[-1])
level_signs = [np.sign(r[2]) for r in rows]
report.append(("Prop 6 level effect: >0 with no new-exposure inflow, <0 with large inflow", 0.0,
               rows[0][2] > 0 and rows[-1][2] < 0))

# persistence: reversion speed of positive vs negative deviations inside bans (pooled episodes)
def reversion(mser, lo_thr, hi_thr):
    d = np.diff(mser); lag = mser[:-1]
    hi = lag > hi_thr; lo = lag < lo_thr
    bh = np.polyfit(lag[hi], d[hi], 1)[0] if hi.sum() > 30 else np.nan
    bl = np.polyfit(lag[lo], d[lo], 1)[0] if lo.sum() > 30 else np.nan
    return bh, bl

mb_all, mn_all = [], []
for _ in range(300):
    sh = (rng.normal(0, SD_N, 200), rng.normal(0, SD_C, 200))
    _, _, mn = simulate(200, None, 0, sh); _, _, mb = simulate(200, 150, 40, sh)
    mb_all.append(mb[150:190]); mn_all.append(mn[150:190])
mb_all = np.concatenate(mb_all); mn_all = np.concatenate(mn_all)
q_lo, q_hi = np.percentile(mn_all, [20, 80])
print("\nAdjustment slope of dm on lagged m (more negative = faster reversion):")
print("  normal: above p80 %.3f | below p20 %.3f" % reversion(mn_all, q_lo, q_hi))
print("  ban   : above p80 %.3f | below p20 %.3f" % reversion(mb_all, q_lo, q_hi))

fig, ax = plt.subplots(figsize=(6.2, 3.4))
bins = np.linspace(min(mn_all.min(), mb_all.min()), max(mn_all.max(), mb_all.max()), 60)
ax.hist(mn_all, bins=bins, color="0.6", alpha=0.7, density=True, label="no ban")
ax.hist(mb_all, bins=bins, color="#1F3A5F", alpha=0.6, density=True, label="ban")
ax.set_xlabel("basis m during the 40 ban days (bp)"); ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig("figs/fig_hist.pdf"); plt.close(fig)

# static band figure
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.plot(us, [m_closed_static(u) for u in us], color="#1F3A5F", lw=1.6, label="with arbitrage")
ax.plot(us, us / PHI, color="0.6", ls="--", lw=1.0, label="no arbitrage (u/Phi)")
ax.axhline(C_PLUS, color="0.3", lw=0.6, ls=":"); ax.axhline(-C_MINUS, color="0.3", lw=0.6, ls=":")
ax.set_xlabel("relative demand pressure u"); ax.set_ylabel("basis m (bp)"); ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig("figs/fig_band.pdf"); plt.close(fig)

print("\nCHECK REPORT")
ok_all = True
for name, val, ok in report:
    ok_all &= bool(ok)
    print("  [%s] %s  (%.2e)" % ("PASS" if ok else "FAIL", name, val))
print("ALL PASS" if ok_all else "SOME CHECKS FAILED")
