# 9. Empirical design

The complete test plan is `plan/pre_analysis_plan_v1.md`, frozen with the git tag `pap-v1`. This page explains it in
plain language: how the project guards against fitting the data, what is estimated, and how uncertainty is measured.

## 9.1 Safeguards against confirmation bias

1. **Theory before data.** Hypotheses and falsifiers come from the model ([05_hypotheses.md](05_hypotheses.md)).
2. **Blind data build.** Until the plan is tagged, no table, figure or regression relates an outcome (basis, returns,
   drift, delay) to a treatment (ban, utilisation, MWPL changes, STT dates, F&O entry or exit, the tax change). Allowed
   while blind: data-quality checks, treatment-side facts (e.g. how many bans), and outcome distributions on their own.
   The code enforces the separation: treatment builders never read prices, the outcome builder never reads bans.
3. **Pre-analysis plan with a git tag.** The tag fixes the plan's text at a commit that anyone can inspect. Any later
   change is logged in the plan's deviations section with date and reason, and results under the original specification
   are always reported.
4. **Estimators tested on simulated data** from the model before use (9.6).
5. **Placebos.** Index-only reforms (single-stock outcomes should not move), fake ban dates, and non-F&O stocks.
6. **All pre-specified tests are reported**, including nulls.

## 9.2 Samples

| Sample | Definition |
|---|---|
| Basis sample | Stock-days in the F&O segment, 1 January 2015 to 27 October 2026; near-month contract, switching to the next month when 3 or fewer trading days remain; at least 5 contracts traded |
| Main exclusions | A dividend or other corporate event going ex within the contract's life; the first 20 trading days after F&O entry; rows whose lot size could not be recovered |
| Pre-sample | 2010 to 2014, ban and MWPL only, for treatment-side robustness |
| Cash universe | All NSE stocks in series EQ, BE and BZ, 2015 to 2026 (for F&O entry and exit tests) |

## 9.3 Primary tests

### H7: one-sided correction in bans

    Delta m_it = sum over regimes r of [beta_r + delta_r * Ban_it] * (m_i,t-1 - mu_i) * 1{regime r} + alpha_i + lambda_t + e_it

- Regimes: **upper** when m_i,t-1 is above the stock's 80th percentile of m on non-ban days; **lower** when below its
  20th percentile; middle otherwise. mu_i is the stock's median.
- beta_r is the normal speed of reversion in regime r (negative means reversion); delta_r is the change in a ban.
- **Prediction:** delta_upper > 0 (upward deviations revert less in bans) and delta_lower <= 0 (downward deviations
  revert as fast or faster). Interacting with "an expiry has occurred inside the current ban spell": delta_lower moves
  toward zero after it (the inventory floor wears out).
- **Fails if** delta_upper <= 0, or delta_upper = delta_lower.
- **Robustness:** thresholds from a three-regime threshold error-correction model estimated per stock on non-ban days;
  fixed thresholds of plus and minus 25 bp around the stock's median; state-dependent thresholds (9.6).

### H8: trading moves out of futures

- On ban days before October 2025: Delta OI + volume should be about zero for near plus next futures; futures volume
  should fall and cash volume and the delivery share should rise, relative to the same stock's non-ban days with similar
  utilisation.
- **Fails if** Delta OI + volume is not close to zero, or futures activity does not fall.

### H3: costs set the band edges

- Event windows of plus and minus 40 trading days around each STT increase (1 April 2023, 1 October 2024,
  1 April 2026). Outcome: each stock's 80th and 20th percentiles of m, and the estimated threshold-model edges, before
  versus after, for all F&O stocks.
- **Prediction:** the upper edge rises, by more for larger cost changes (2026 > 2024 > 2023).
- **Fails if** no shift, or the ordering is unrelated to the cost change.
- 1 April 2023 is also the date of the debt-fund tax change, so that date is reported but not used as evidence on its own.

### H6: short-sale access

- Staggered difference-in-differences (Callaway and Sant'Anna 2021; Sun and Abraham 2021 as a check) for F&O entries and,
  separately, eligibility exits.
- Controls: not-yet-treated stocks, and never-treated cash-market stocks matched on size, turnover and volatility over
  the six months before.
- Outcomes: drift after bad news (O5) and price delay (O6).
- **Prediction:** after entry, bad-news drift and delay fall; after exit they rise. **Fails if** no change or opposite
  signs.
- Implementation (fixed before running, plan §11.3): calendar-year panel, cohort = first year fully after the event;
  delay by Callaway-Sant'Anna with base-year covariates; drift (which exists only at announcement events) by a stacked
  difference-in-differences with clean controls; family p-value = Bonferroni across the four components (entry/exit x
  delay/drift).

## 9.4 Secondary tests (labelled exploratory)

| Test | Design |
|---|---|
| Level effect of bans | Stacked ban-entry event study, window -20 to +20 days. Controls: stock-days with utilisation in [0.85, 0.95) in the same week that do not enter, matched on the 5-day utilisation path and basis level. Split by the composition of pre-ban activity (Delta OI / volume over the 5 days before entry). Prediction: the sign follows the composition. |
| H9 anticipation and regime | Basis quantiles by utilisation bins (0.60 to 0.95) on non-ban days; difference-in-differences on the 1 October 2025 intensity with stock and date fixed effects. Prediction: the upper quantile rises smoothly with utilisation; the reform effect follows the intensity. |
| Regression discontinuity at 95% | Local linear in utilisation on day t-1; density test (Cattaneo, Jansson and Ma 2020) first. Supporting only. |
| Hysteresis | Utilisation in [0.80, 0.95): in a ban versus not, controlling for utilisation, its change and five lags of the basis. |
| H2 | Bad-news drift on ban days versus non-ban days (few events, stated in advance); pre-announcement basis (days -5 to -1) in bans versus not. |
| H1 | Friction index versus band width. |
| H4 | Arbitrage-fund flows versus the upper quantile of the cross-sectional basis, monthly. |
| H5 | Anomaly returns by constraint terciles (double sorts). |

## 9.5 Inference

- Standard errors clustered two ways, by stock and by date.
- Event studies with few clusters: wild-cluster bootstrap.
- The primary family {H7, H8, H3, H6} is corrected with the Holm method at 5%.
- Outliers: the basis is winsorised at 1% and 99% within each year for the main estimates; robustness without.

## 9.6 What the estimators do on simulated data

A three-regime threshold autoregression (`analysis/setar.py`: grid search over quantiles of the lagged basis, minimum
share of observations in each regime) was run on two kinds of simulated data (`analysis/test_setar_simulated.py`):

1. A textbook threshold process with known thresholds of -30 and +15 bp: estimates -29.1 and +15.2 bp. The estimator works.
2. A basis simulated from the model, where the no-trade region moves with arbitrage inventory: estimates -10 and 0 bp,
   although the cost edge is +15 bp.

Consequences written into the plan: estimated fixed thresholds are reported as **average band edges, not costs**; H3
compares **changes** in edges around STT dates (inventory is roughly constant within plus and minus 40 days) rather than
levels; and a threshold model whose thresholds depend on lagged open interest and MWPL is the main robustness check for
H7 and H3.

## 9.7 Power (known before any outcome analysis)

| Quantity | Count |
|---|---|
| Ban spells 2015 to 2026 | 1,788 (44 after 1 October 2025) |
| Ban stock-days | 9,416 |
| Stocks ever banned | 141 |
| Non-ban stock-days with utilisation in (0.90, 0.95] | 2,439 before the reform, 139 after |
| F&O entries / eligibility exits (usable) | 233 / 158 |
| Results announcements while in F&O | see [11_descriptive_facts.md](11_descriptive_facts.md) |

Post-reform ban analyses and the earnings-drift test inside bans have low power; this is stated in advance.
