# 06. Theory (the current model, with proposition numbers as in the PDF)

Source of truth: `models_src/modelC/ModelC_constrained_arbitrage_india.tex` (15 pp) → `BSP_Model_C_Constrained_Arbitrage_India.pdf`
(guide-safe: no internal labels inside the PDF). Numerical checks: `models_src/modelC/verify_modelC.py` → `verify_output.txt`
(ALL PASS), figures in `models_src/modelC/figs/`. Plain-language version: `docs/04_theoretical_framework.md`.
Internally this is called "Model C"; never use that label in guide-facing text.

## 6.1 Environment

- Basis m = ln F - ln F*, F* = (S - PV(D)) e^{r_b (T-t)}; s, f = deviations of spot and futures from fundamentals, m ~ f - s.
- Outside demand: cash D_S - psi_S s; futures D_F - psi_F f. Arbitrage holds a units of cash-and-carry (long cash, short
  futures).
- Clearing: D_S - psi_S s + a = 0, D_F - psi_F f - a = 0 ⇒ **m = (u - a)/Phi**, 1/Phi = 1/psi_F + 1/psi_S,
  u = Phi (D_F/psi_F - D_S/psi_S) (relative demand pressure toward futures).
- Arbitrage objective (Assumption 1): Pi(a) = a m - (gamma/2) a^2 - c_+ a^+ - c_- a^-, gamma = alpha sigma^2.
  c_+ = tau_+ + (r_A - r_b)(T-t); c_- = tau_- + (l_s + r_b - r_L)(T-t).
- Indian limits as parameters: STT/fees → tau; short-sale cost → c_- (infinite overnight for cash-only stocks); capital →
  alpha, r_A; risk → sigma^2; position limits → caps on a and the reduce-only rule; depth → psi, Phi.

## 6.2 Propositions

| # | Name | Statement |
|---|---|---|
| P1 | Asymmetric band and passthrough | Unique equilibrium: m = (gamma u + c_+)/(gamma Phi + 1) if u > Phi c_+; m = u/Phi if -Phi c_- <= u <= Phi c_+; m = (gamma u - c_-)/(gamma Phi + 1) if u < -Phi c_-. Arbitrage a = (u - Phi c_+)/(gamma Phi + 1) above, 0 inside, (u + Phi c_-)/(gamma Phi + 1) below. Passthrough 1/Phi inside, gamma/(gamma Phi + 1) outside |
| P2 | Comparative statics | (i) costs set the edges, one-for-one (STT); (ii) capital and risk set passthrough beyond the edge; (iii) edges affine in T-t, converge to tau at expiry; (iv) centre (c_+ - c_-)/2 < 0 if c_- > c_+; upper edge < 0 if (r_b - r_A)(T-t) > tau_+ (cheap, tax-advantaged cash-and-carry capital) |
| Remark | Indian evidence | Band centred below zero (Shankar et al.: -39/-10 bp; negative median basis in Aggarwal and Nandan et al.); 1 Apr 2023 debt-fund tax change should lower r_A and the upper edge, confounded with the STT rise |
| P3 | Inventory-dependent no-trade region | With a_(t-1) >= 0, costs c_+ to add and c_u to unwind (reverse arbitrage set aside): trade only outside [gamma a_(t-1) - c_u, gamma a_(t-1) + c_+]. With m0 = (u - a_(t-1))/Phi: (a) add if m0 > gamma a_(t-1) + c_+, m = (gamma u + c_+)/(gamma Phi + 1); (b) unwind if m0 < gamma a_(t-1) - c_u, a = max{0, (u + Phi c_u)/(gamma Phi + 1)}; (c) otherwise hold |
| Assumption 2 | Ban | (B1) 0 <= a_t <= a_(t-1); (B2) new-exposure demand eps^n is blocked, share chi moves to cash; maps eps^n into -lambda eps^n, lambda = chi psi_F/psi_S |
| Lemma 1 | Ban weakly raises m | Same u and a_(t-1): m(ban) >= m(normal) |
| P4 | One-sided correction | (i) no ceiling: for u >= a_(t-1)(1 + gamma Phi) - Phi c_u, m = (u - a_(t-1))/Phi, slope 1/Phi; (ii) floor m = gamma a_t - c_u while inventory lasts; (iii) floor wears out at a = 0; expiry in a ban removes expiring inventory (no rollover) |
| P5 | Sign reversal | Normal: dm/d eps^n = 1/Phi (inside) or gamma/(gamma Phi + 1) (beyond upper edge). Ban: -lambda/Phi inside, -lambda gamma/(gamma Phi + 1) on the floor; strict iff chi > 0 |
| P6 | Level effect ambiguous | m^B - m^N non-increasing in eps^n; >= 0 at eps^n = 0 (strictly if closing pressure would have triggered new arbitrage); < 0 for large eps^n. Sign condition: composition of order flow (closing vs new) |
| P7 | Trading and measurement in a ban | (i) contract-level reduce-only ⇒ Delta OI = -V outside expiry days (cross-instrument offsets allowed from 1 Oct 2025 break it); (ii) futures volume falls, spreads widen; (iii) theoretical settlement price on no-trade-in-last-half-hour days ⇒ settlement basis ~ 0 mechanically |
| Assumption 3 | Exit costlier in a ban | Unwinding costs c_u + l, l > 0; pi(omega) = probability a position opened at omega meets a ban, continuous, increasing |
| P8 | Anticipation | Outside a ban the effective entry cost is c_+ + pi(omega) l: the upper edge rises smoothly toward 95%; the jump at 0.95 contains only the reduce-only effects. Density test not signed (arbitrageurs hold back vs speculators rush in) |
| Cor. 1 | Hysteresis | omega in [0.80, 0.95): in-ban (reduce-only) vs not (anticipation) at equal omega |
| P9 | MWPL is not a clean instrument | The MWPL enters the ban state, pi(omega) and entity caps; changing it moves m even without a ban ⇒ exclusion fails; denominator variation identifies total-regime effects |
| P10 | Bad news slower in a ban | Share k impounded on the day; share rho of informed selling via short futures; ban ⇒ k(1 - rho) impounded; drift after bad news (1 - k + k rho) delta instead of (1 - k) delta; good news unaffected. Remark: pre-announcement negative basis (Saurav et al.) should vanish in bans |
| P11 | Miller overpricing | v_i ~ U[v - delta, v + delta], long demand k(v_i - p), shorting cost c_s, supply Q: p non-decreasing in c_s; free shorting p = v - Q/k; no shorting (delta >= Q/k) p = v + delta - 2 sqrt(delta Q/k), overpricing (sqrt(delta) - sqrt(Q/k))^2, increasing in delta. F&O inclusion lowers c_s |

What each design identifies (model section 7): RD at 95% = local jump in reduce-only effects (if omega not precisely
manipulable); hysteresis = reduce-only vs anticipation; ban-entry event study with near-miss controls = P4 to P7
dynamically; 1 Oct 2025 reform and quarterly resets = total-regime reduced form.

Section 9 (heterogeneous arbitrageurs): cost distribution G ⇒ aggregate arbitrage smooth and convex ⇒ smooth-transition
ECM (Tse 2001) or 3-regime TVECM with thresholds = quantiles of G (Dwyer-Locke-Yu; Ters-Urban); thresholds move with
inventory; in bans the upper regime's reversion falls toward 0.

Section 10 (calibration): overnight round-trip costs are tens of bp (cash STT 0.1% each side; futures STT 0.01 to 0.05%;
0.1% on physical delivery; stamp duty, fees, impact), not the few-bp bands of one-second data. Simulation numbers are
illustrative: c_+ = 15, c_u = 10, c_- = 60 bp.

Section 11: hypothesis map H1 to H9 with falsifiers (same as `05_hypotheses` in docs). Section 12 limitations: partial
equilibrium; the closing/new split (B2) drives P5 and P6; reverse arbitrage folded into depth; anticipation rests on
Assumption 3; P10/P11 fix directions only.

## 6.3 Numerical verification (verify_modelC.py, seed 20261028)

All PASS: P1 closed form vs solver (err 2.8e-14); P3 and P4 steps; P4 floor; P4 slope above region = 1/Phi; beyond-edge
slope gamma/(gamma Phi + 1); Lemma 1; P6 monotone and sign change; P11 price, overpricing, monotonicity.
Simulations (Phi = gamma = 1, c_+ = 15, c_u = 10, u AR(1) persistence 0.9 around 25 bp, shock sd 6 bp per component,
lambda = 0.5, 300 paired paths, 40-day ban): reversion slope above p80 -0.182 → -0.130 in ban, below p20 -0.116 →
-0.163; level effect +4.93 bp (no new inflow), -3.09 / -10.83 / -26.03 bp with 1 / 2 / 4 bp/day of new demand.
History: the first version of P6 failed its check (mean-zero spillover cannot move the mean); P6 was corrected to depend on
the inflow of new demand. This is a good example of why the checks exist.

## 6.4 Estimators on simulated data (analysis/test_setar_simulated.py)

`fit_setar3(mlag, dm)`: 3-regime SETAR, grid over quantiles 0.05 to 0.95 step 0.025, each outer regime >= 10% of
observations, middle >= 20%; returns thresholds, regime intercepts/slopes, shares, half-lives, F vs linear.
(1) Known TAR (-30/+15 bp, rho = -0.4 outside): estimates -29.1/+15.2. (2) Model-simulated basis (inventory dynamics,
c_+ = 15, c_u = 10): estimates -10/0 bp. Lesson: fixed thresholds estimate average edges, not costs ⇒ H3 compares changes
of edges; state-dependent thresholds added as robustness (PAP §5b).

## 6.5 Superseded models (kept, internal only)

- **Model A** (`models_src/ModelA_constrained_arbitrage.tex`, `BSP_Model_A_Constrained_Arbitrage.pdf`): CARA arbitrageur
  with position cap L = kappa x MWPL; band [-(c + c_s), c]; ban as KKT multiplier jump; Props 4 to 6 flawed (theta ad hoc,
  Prop 5 proof false, "Cov(L, u) = 0 by timing" invalid); ban modelled as freezing only the arbitrageur.
- **Model B** (`models_src/ModelB_band_of_inaction.tex`): impulse control, b = (6 K sigma^2/theta)^(1/4) (derivation
  correct), QVI obstacle sign flipped, g(omega) → infinity assumed, "exact bridge" to TAR overstated (impulse control
  resets to 0 so outer regimes are never populated).
- The corrected model keeps A's static band (as P1, P2), replaces the rest, and keeps B's band-of-inaction idea as an
  appendix interpretation of the threshold. Full audit: `memory/04_models_and_audit.md`.

## 6.6 Rule on theory from here

The user decided (28 Oct 2026): keep this model as is; no further theory unless the data demand it. If results contradict
a proposition, report it; do not modify the model to fit.
