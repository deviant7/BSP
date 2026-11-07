# 14. Results

This page reports the tests of the frozen plan (`plan/pre_analysis_plan_v1.md`, git tag `pap-v1`) in the order they were
run. For each test the **pre-specified result comes first**. Analyses added after a result was seen are marked
**exploratory** and are listed in the plan's deviations log (§11.2). Output files: `analysis/output/`. Code: `analysis/`.

Status: all four primary tests are complete (H8, H7, H3, H6) and corrected for multiple testing (14.6). Secondary tests
(reported unadjusted, labelled exploratory by the plan) start in 14.7.

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
- The faster reversion of upward deviations is concentrated in the start day and the next four calendar days of a spell (-0.163, against
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

## 14.5 H6: short-sale access (F&O entry and eligibility exit)

**Pre-specified test** (`analysis/h6_fno.py`, output `h6_results.txt`; outcomes `analysis/h6_outcomes.py`; details in the
plan's §11.3). Units: stocks by calendar year, 2015 to 2025. A stock's cohort is the first calendar year fully after its
event; the event year itself is a transition year. Price delay: Callaway-Sant'Anna with base-year covariates (log market
cap, log traded value, volatility), controls never-treated and not-yet-treated, stock-cluster bootstrap (499 draws).
Bad-news drift: stacked difference-in-differences at the announcement level. Entries in 2015 have no pre-year in the data
and cannot enter the delay design; cohorts used for entries: 2017, 2018, 2021, 2022, 2025.

| Component | Prediction | Estimate | Standard error | One-sided p |
|---|---|---|---|---|
| Entry: price delay | < 0 | **-0.109** (median delay 0.24) | 0.023 | 1.3e-6 |
| Entry: BHAR after bad news | > 0 (weaker drift) | **-0.040** (stronger drift) | 0.018 | 0.99 |
| Exit: price delay | > 0 | +0.053 | 0.040 | 0.091 |
| Exit: BHAR after bad news | < 0 | +0.014 | 0.020 | 0.77 |

Family statistic (Bonferroni across the four components): p_H6 = 5.2e-6. **On the pre-specified statistic H6 is
supported, through price delay: prices of stocks that enter the F&O segment respond much faster to market-wide news,
and prices of stocks that leave respond somewhat more slowly. The drift components go the other way:** after entry the
drift that follows bad news is stronger, not weaker, and exits do not strengthen it.

Checks: Sun-Abraham estimate for entries -0.063 (0.019); leads three and four years before entry close to zero (+0.009,
+0.013); without the 2024 batch -0.120; with cohorts whose base year is from 2018 (no back-cast market caps) -0.099; the
variance ratio moves toward 1 after entry (+0.023). Exits without the 2019 batch: +0.071.

Caveat: entry into the F&O segment requires a stock to have grown in size and liquidity, which by itself lowers price
delay. The covariates are measured two years before the event, and the leads do not show a trend over the last years
before entry, but selection on growth cannot be ruled out.

## 14.6 The primary family (Holm correction, 5%)

| Hypothesis | Pre-specified p | Holm-adjusted p | Rejected at 5% |
|---|---|---|---|
| H8 (trading moves out of futures) | 1.9e-41 | 7.4e-41 | yes |
| H3 (costs set band edges) | 1.8e-24 | 5.5e-24 | yes (placebo-calibrated p about 0.05; see 14.4) |
| H6 (short-sale access) | 5.2e-6 | 1.0e-5 | yes (through price delay; drift components contradict) |
| H7 (one-sided correction) | 1 | 1 | no (opposite sign) |

## 14.7 Secondary: the level effect of a ban

Question (model result on the level effect): does a ban raise or lower the basis level, and does the sign follow the
composition of trading before the ban? The model predicts a higher basis when the pressure comes from closing trades and a
lower basis when new speculative demand keeps arriving (it can no longer enter futures and part of it moves to the stock).
Details fixed before estimation: plan §11.4 (C7). Code `analysis/level_effect.py`; output
`analysis/output/level_effect_results.txt`.

Design. Each ban spell from 2015 to September 2025 with no ban in the five days before it is an event (day 0 = first ban
day). Controls are other stocks in the same week with utilisation between 85% and 95%, no ban within five days either
side, matched (up to five, nearest by Mahalanobis distance) on the utilisation path of days -5 to -1 and the basis on day
-1. Outcome: the change in the basis from day -1, treated minus matched controls, averaged over the ban days among days
0 to 4. Composition C = change in futures open interest over days -5 to -1 divided by futures volume over the same days.

**Pre-specified result (889 matched events, 129 stocks; bp):**

| | Mean effect (se) |
|---|---|
| All events | -6.3 (median -7.8) |
| C <= 0, falling OI before entry (30 events) | +8.4 (10.9) |
| C > 0, rising OI before entry (859 events) | -6.8 (1.8) |
| Difference | -15.2 (10.9); one-sided p = 0.083 |
| Median split of C (difference high minus low) | -5.8 (2.9); one-sided p = 0.025 |
| Slope on standardised C | -4.8 (1.6); one-sided p = 0.0014 |

Reading. The signs are as the model predicts: positive (not significant) when open interest was falling, negative and
significant when it was rising, and more negative the faster it rose. On average the basis falls by about 6 bp during
the first days of a ban, relative to the matched controls, and returns to its earlier level about a week after day 0. The
pre-specified split has little power because only 30 events had falling open interest before entry (open interest must
rise for utilisation to cross 95%), so its difference is not significant at 5%; the median split and the continuous
measure, fixed in the same entry before estimation, are.

Checks (pre-specified): unwinsorised basis -11.3 overall, slope p = 0.013; close-based basis -0.7 overall (no level
effect) but a strong composition gradient (slope -4.7, p = 0.0002; closing group +23.1, se 10.9); relative implied repo (an annualised rate, so in different units):
negative level, no significant gradient; **same-day controls only (685 events): level -4.0 (se 2.0), gradient not
significant (slope -2.1, se 1.8)**; excluding imputed ban days: unchanged. By enforcement regime (exploratory): the
gradient appears in both (slope -5.0 to 22 March 2020, -6.1 after). After the October 2025 reform: 19 matched events,
all with rising open interest, mean -2.8 (too few to test).

Caveats. Matching is imperfect: on day -1 the treated basis is 10 bp below that of its controls, and the treated basis
dips on day -1 itself (the day utilisation crosses 95%), so the event-time profile shows a positive pre-period of about
+4 to +6 bp relative to day -1. **Exploratory (added after the results were seen):** with the baseline taken over days
-10 to -2 the in-ban level effect is -11.3 (se 1.5) and the slope on C -3.1 (p = 0.007); controlling for the day -1 gap
(which shows the expected mean reversion, coefficient -0.29) gives -9.2 at average composition and a slope of -3.5
(se 1.6). The result is consistent with the H7 diagnostics: at the start of a ban the basis falls as new long demand
for futures is blocked.

## 14.8 Secondary (supporting): density of utilisation at 95%

Question: do stocks bunch just below the 95% trigger (traders holding back to avoid a ban) or just above it (a rush to
open positions before an expected ban)? The model does not sign this; the answer decides whether a regression
discontinuity at 95% can be read as local randomisation. Details fixed before running: plan §11.5 (C8). Code
`analysis/density_test.py`; output `analysis/output/density_test.txt`; figure `reports/figs/density_95.pdf`.

Population. End-of-day utilisation of stocks that were not in a ban and were below 95% the day before (47,503 stock-days in
[0.60, 1.30], 2015 to September 2025). Using all non-ban stock-days instead would build in a drop above 95% mechanically
(a stock above the trigger is in the ban from the next day); that version is also reported.

**Pre-specified result (Cattaneo-Jansson-Ma, local quadratic, robust bias-corrected):** density just below 0.326, just
above 0.311, log ratio -0.05; T = -0.18, p = 0.86. No discontinuity. The same holds for local linear (p = 0.59) and cubic
(p = 0.49) fits, fixed bandwidths of 0.02 (p = 0.93) and 0.05 (p = 0.23), all non-ban stock-days (p = 0.93), excluding
days with an MWPL change (p = 0.94), and each enforcement regime separately (p = 0.37 and 0.43). The pre-sample 2010 to
2014 shows a positive jump (log ratio +1.10, p = 0.008) that the binned check does not confirm (-0.03). After October 2025
there are too few observations (36 just above the cutoff).

A binned McCrary-type check with a stock-clustered bootstrap (pre-specified because the test above treats repeated days
of a stock as independent) gives +0.31 (95% interval +0.08 to +0.62). **Exploratory (added after the results were seen):**
the binned estimate rises with the bandwidth (+0.12 at 0.02, +0.31 at 0.05, +0.34 at 0.075), the pattern expected from
fitting straight lines to a convex, falling density, whereas the main estimator corrects for this bias; a
stock-clustered bootstrap of the main estimate gives a standard error of 0.29 (interval -0.62 to +0.54).

Reading. There is no sign of bunching below 95%: utilisation does not stall as it nears the trigger. The mean daily change
in utilisation is larger, not smaller, just below 95% (+0.008 to +0.014 against about 0 further below), and the share of
stocks crossing the next day rises steadily with yesterday's utilisation (7% at 0.85, about 50% at 0.93 to 0.95). The
regression discontinuity can therefore be read as supporting evidence, with the caveat that the density test has limited
power against moderate discontinuities once dependence within stocks is allowed for.

## 14.9 Secondary (supporting): regression discontinuity at 95%

Details fixed before running: plan §11.6 (C9). Code `analysis/rd_95.py`; output `analysis/output/rd_95.txt`. Units:
stock-days whose stock was not in a ban the day before (49,029 in the utilisation range 0.60 to 1.30, 2015 to September
2025). Above 95% the stock is in the ban the next day in 99.7% of cases (0.06% below), so the design is sharp. Local linear
fits with the MSE-optimal bandwidth, robust bias-corrected inference, clustering by stock.

| Outcome on the first possible ban day | Jump at 95% (se) | Robust p |
|---|---|---|
| **Basis level (bp), main** | -12.9 (5.2) | 0.020 |
| Change in the basis that day, same contract (bp) | -2.8 (4.1) | 0.75 |
| Close-based basis (bp) | -11.9 (5.0) | 0.016 |
| log(1 + futures contracts) | -1.53 (0.14) | 2e-21 |
| R = (change in OI + volume) / volume | -0.66 (0.06) | 4e-29 |
| log(1 + cash shares traded) | +0.04 (0.35) | 0.84 |
| Delivery share | +0.051 (0.015) | 0.0006 |
| Check: basis two days before (bp) | -6.7 (4.9) | 0.17 |
| Check: futures contracts two days before | +0.17 (0.14) | 0.17 |
| Check: basis on the crossing day itself (bp) | -11.3 (5.7) | 0.048 |
| Check: share with a valid basis | +0.016 (0.021) | 0.51 |

Reading. The mechanism outcomes jump sharply and in the predicted direction: futures trading falls by about 1.5 log
points, every futures trade closes positions (R falls toward 0), and the delivery share of cash trading rises; cash volume
does not jump. The basis level is lower above the cutoff, but almost all of that gap is already present on the crossing
day, before the ban starts (-11.3 bp), and the change on the first ban day is small and insignificant. The RD therefore
does not separate an effect of the ban on the level from the pressure that pushes utilisation over 95%; the basis tends to
be low on the day open interest crosses the trigger. Selection into the basis sample does not jump.

Robustness. The basis jump is stable in size (-10.7 to -14.9) across double bandwidth, local quadratic, a donut, days
without an MWPL change and the intraday-enforcement era, but not significant at half the bandwidth (-11.0, p = 0.43), in
the end-of-day era (-12.1, p = 0.19) or as a fuzzy RD (-9.5, p = 0.20). The futures-volume jump is robust everywhere; it is
-0.57 under end-of-day enforcement and -2.29 under intraday enforcement, matching the enforcement regimes found for H8.
Placebo cutoffs: none for futures volume; for the basis, none at 0.85 or 1.00, but a jump of +24 bp at 0.90 with a
degenerate bandwidth (0.008), which is a reminder that the basis RD is noisy. After October 2025: futures volume -1.7,
basis not estimable with precision (37 stock-days just above the cutoff).

## 14.10 To come

Hysteresis, H9 (anticipation and the 1 October 2025 reform), H2 (bad news in bans), H1 (friction index), H4 (arbitrage
capital), H5 (anomalies).
