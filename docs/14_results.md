# 14. Results

This page reports the tests of the frozen plan (`plan/pre_analysis_plan_v1.md`, git tag `pap-v1`) in the order they were
run. For each test the **pre-specified result comes first**. Analyses added after a result was seen are marked
**exploratory** and are listed in the plan's deviations log (§11.2). Output files: `analysis/output/`. Code: `analysis/`.

Status: three of the four primary tests are complete (H8, H7, H3). H6 (F&O entry and exit) and the secondary tests are
still to be run, so the multiple-testing correction over the primary family is not yet computed.

## 14.1 Common set-up

- Basis sample (§2 of the plan, details in its §11 C1): 486,040 stock-days (371 stocks, 2015 to 27 Oct 2026), one futures
  contract per stock and day (the near month, or the next month when 3 or fewer trading days remain), at least 5 contracts
  traded, no dividend or other corporate event within the contract's life, not in the first 20 trading days after an F&O
  entry. 8,851 of these stock-days are ban days. The basis is winsorised at 1% and 99% within each year.
- Regressions use stock and date fixed effects and standard errors clustered by stock and by date (two-way). The code was
  checked on simulated panels with known coefficients (`analysis/test_inference.py`).

## 14.2 H8: in a ban, trading moves out of futures

**Pre-specified test** (`analysis/h8_trading.py`, output `h8_results.txt`). Ban days compared with the same stock's
non-ban days at similar lagged utilisation (80% to 95% of MWPL, the only range where both exist), before October 2025,
expiry days excluded:

| Outcome | Effect of a ban | Standard error |
|---|---|---|
| log(1 + futures contracts traded) | **-2.00** (about -87%) | 0.11 |
| log(1 + cash shares traded) | **+0.073** (about +7.5%) | 0.027 |
| Delivery share of cash volume | **+0.041** (non-ban mean 0.26) | 0.0045 |

All three move as predicted. The pre-specified family statistic (one-sided p for the futures-volume effect) is
p < 1e-10. **H8 is supported.**

The second, descriptive part of H8 is the identity "change in open interest = minus volume" in a ban, measured by
R = (change in OI + volume) / volume (R = 0 if every trade closes positions on both sides; about 1 on normal days).
Pre-specified reading: the identity holds if the ban-day mean of R is below 0.10. **Result: mean 0.42; the identity does
not hold over the whole period.**

**Explanation found afterwards (exploratory, documented with primary sources).** R depends on how the exchanges enforce
the rule:

| Period | How violations were checked | Ban days | Mean R | Median R |
|---|---|---|---|---|
| to 22 Mar 2020 | End-of-day positions only (intraday round trips were not violations) | 3,715 | 0.855 | 0.871 |
| 23 Mar 2020 to 30 Sep 2025 | **Peak intraday positions** (SEBI press release 18/2020; kept by press release 59/2020) | 4,924 | 0.099 | 0.011 |
| 1 Oct to 7 Dec 2025 | End-of-day futures-equivalent positions against a base position (NSE Clearing 119/2025) | 43 | 0.277 | 0.193 |
| from 8 Dec 2025 | as above (brokers' delta-based checks) | 354 | 0.446 | 0.357 |

On non-ban days R is about 1.01 in every year, and NSE's change-in-OI field equals the change in OI levels, so the break
is not a data artefact. When the rule binds trade by trade, as the model assumes, the identity holds almost exactly. The
effect of a ban on futures volume is -0.97 log points before 23 Mar 2020 and -2.72 after.

## 14.3 H7: one-sided correction in bans

**Pre-specified test** (`analysis/h7_onesided.py`, output `h7_results.txt`):
Delta m on the lagged deviation from the stock's median, by regime (upper: above the stock's 80th percentile on non-ban
days; lower: below the 20th), with the change in each slope on ban days (delta). Prediction: delta_upper > 0 (rich futures
revert more slowly in bans), delta_lower <= 0.

| | Normal slope | Change in a ban (delta) |
|---|---|---|
| Upper regime | -0.712 (0.010) | **-0.089 (0.037)** |
| Middle | -0.393 (0.026) | +0.099 (0.062) |
| Lower regime | -0.204 (0.010) | **+0.081 (0.030)** |

delta_upper - delta_lower = -0.170 (0.046). Pre-specified family statistic p_H7 = 1. **H7 is rejected: in bans, rich
futures revert faster and cheap futures revert more slowly, the opposite of the prediction.** The result holds with fixed
+/-25 bp thresholds, per-stock threshold-model thresholds, state-dependent thresholds, without imputed ban days, without
carried-forward rates, and for the relative implied repo. With the close-based basis delta_upper is about 0; with the
unwinsorised basis delta_upper is +0.077 (t = 1.6). After an expiry inside the ban spell, downward deviations revert much
faster (delta_lower + interaction = -0.83), also against the prediction. After October 2025 (44 spells) nothing is
significant.

**Exploratory diagnostics** (`analysis/h7_diagnostics.py`, output `h7_diagnostics.txt`):

- Not measurement noise from thin trading: on liquid days (at least 1,000 contracts on both days) the pattern is stronger
  (delta_upper -0.154, delta_lower +0.130).
- Differs by enforcement period: before 23 Mar 2020, delta_upper +0.016 (not significant) and delta_lower +0.126; from
  23 Mar 2020 to Sep 2025, delta_upper -0.201 and delta_lower -0.120 (downward deviations revert faster, as the model
  predicts for the lower regime).
- The faster reversion of upward deviations is concentrated in the first four calendar days of a spell (-0.163, against
  -0.008 later).

A reading consistent with these facts, but not tested in advance: when a ban starts, new demand for futures exposure is
blocked (the model's second ban channel, which reverses the response of the basis to new demand). That removes the
pressure that had made futures rich, so upward deviations close quickly. The pre-specified H7 was derived from the
reduce-only arbitrage channel alone and did not net out this opposing channel.

## 14.4 H3: costs set the band edges

**Pre-specified test** (`analysis/h3_costs.py`, output `h3_results.txt`): change in each stock's 80th percentile of the
basis from the 40 trading days before to the 40 from each STT increase.

| Event | STT change on futures sale | Stocks | Mean change in 80th percentile (bp) | 20th | Median |
|---|---|---|---|---|---|
| 3 Apr 2023 (confounded with the debt-fund tax change) | +0.25 bp | 181 | -2.12 | +0.24 | +0.27 |
| 1 Oct 2024 | +0.75 bp | 172 | **+6.42** | +4.55 | +5.39 |
| 1 Apr 2026 | +3.0 bp | 192 | **+7.44** | +2.10 | +6.30 |

Pre-specified family statistic (2024 and 2026 pooled, standard errors clustered by stock): +6.96 bp (0.61), one-sided
p = 1.8e-24. The predicted ordering 2026 > 2024 > 2023 holds. **On the pre-specified statistic, H3 is supported.**

**Placebo test (pre-specified) and its implication.** At 30 pseudo-event dates (every 80 trading days, away from the true
dates) the same statistic has a standard deviation of 7.4 bp, because shocks common to all stocks move the whole
distribution. The 2024 and 2026 changes rank at 0.10 and 0.067 among the placebos. **Exploratory** calibration: the average
of 2024 and 2026 is exceeded by 4.6% of placebo pairs; but the change in band width (80th minus 20th percentile) is
exceeded by 23.4% of pairs, and the change in the 80th percentile relative to the median by 27.4%. The rise is mostly a
shift of the whole distribution rather than of its upper edge, and the shifts are larger than the cost changes. Standard
errors clustered only by stock ignore cross-sectional correlation, which over-rejects when all observations share the same
event date (Kolari and Pynnonen 2010). The evidence that costs set the edge is therefore weak.

## 14.5 To come

H6 (F&O entry and exit; needs returns adjusted for splits and bonuses and market capitalisation), the Holm correction over
{H7, H8, H3, H6}, and the secondary tests (level effect, H9, RD, hysteresis, H2, H1, H4, H5).
