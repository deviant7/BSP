# 14. Results

This page reports the tests of the frozen plan (`plan/pre_analysis_plan_v1.md`, git tag `pap-v1`) in the order they were
run. For each test the **pre-specified result comes first**. Analyses added after a result was seen are marked
**exploratory** and are listed in the plan's deviations log (§11.2). Output files: `analysis/output/`. Code: `analysis/`.

Status: all four primary tests are complete (H8, H7, H3, H6) and corrected for multiple testing (14.6). All secondary
tests of the plan are complete (14.7 to 14.15; summary 14.16), reported unadjusted and labelled exploratory as the plan
says.

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

**Exploratory, measurement noise** (added after the band estimation of [15_band_estimation.md](15_band_estimation.md)
showed that noise in daily prices inflates reversion slopes; `analysis/h7_iv.py`): with regimes classified by the
deviation two days earlier and yesterday's deviation instrumented by it, delta_up = -0.190 (se 0.077) and delta_lo =
+0.088 (0.015); the difference is -0.279 (0.079). The opposite-sign result is not caused by noisier prices on ban days.

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

**Exploratory, build-up type** (added after the RD of 14.9 showed the basis already low on the crossing day; code
`analysis/level_effect_buildup.py`). The ratio C cannot tell new longs from new shorts, so events are also classified, as
Indian market practice does, by open interest and price over days -5 to -1: long build-up (both up) -7.9 bp (se 2.7,
453 events), short build-up (open interest up, price down) -5.5 (2.2, 406), difference +2.4 (3.5); short covering and long
unwinding together have only 30 events, both +8.4 (imprecise). The in-ban fall is therefore not specific to new long
demand. The dip on the crossing day itself is concentrated in long build-up events.

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

## 14.10 Secondary: hysteresis between 80% and 95%

Question (model corollary on hysteresis): at the same utilisation between 80% and 95%, does a stock that is in a ban (it
crossed 95% earlier and has not yet fallen to 80%) have a different basis from a stock that is not? Details fixed before
running: plan §11.7 (C10). Code `analysis/hysteresis.py`; output `analysis/output/hysteresis.txt`.

Specification: basis level on Ban, utilisation, its change and five lags of the basis, with stock and date fixed effects
(15,832 stock-days, 5,237 in a ban, 163 stocks, 2015 to September 2025).

**Pre-specified result:** Ban +0.4 bp (se 0.8), two-sided p = 0.64. At equal utilisation and recent basis path, being in
the reduce-only state does not shift the basis level.

| Outcome (same specification) | Ban coefficient (se) |
|---|---|
| Change in the basis, same contract (bp) | +0.2 (0.8) |
| Close-based basis (bp) | +3.2 (1.0), p = 0.001 |
| Relative implied repo (annual rate, bp) | -50.9 (21.6), p = 0.02 |
| log(1 + futures contracts) | -1.92 (0.13) |
| R = (change in OI + volume) / volume | -0.55 (0.05) |
| Delivery share | +0.042 (0.005) |

Robustness for the basis level: utilisation bins +0.2 (0.8); adding the highest utilisation of the last ten days -1.1
(0.9); excluding imputed ban days +0.4; end-of-day era -0.5 (1.3); intraday era -0.4 (1.1); in-ban days before an expiry
in the spell +0.4, after -0.0 (43 days only). **Without the lagged basis the coefficient is -14.1 (2.4)**: stocks in a ban
carry a basis that is already low from the start of the spell, which the lags absorb. After October 2025 (302 ban days,
22 stocks; descriptive): -6.6 (2.8).

Reading. The ban's lasting effect inside this zone is on trading (futures volume, R and the delivery share move as
strongly as in H8), not on the basis level once its recent path is held fixed. The level falls when the ban begins
(14.7) and the fall persists rather than growing.

Measurement note. The VWAP-based and close-based basis disagree on ban days in several tests (here +0.4 against +3.2;
in 14.7 the overall level effect is -6.3 against -0.7). On thin ban days the futures and cash trades that make up each
day's VWAP may come at different times of day, and the futures closing price may be stale; daily data cannot tell which
measure is closer to the truth. Results that depend on the measure are reported for both.

## 14.11 Secondary: H9, anticipation below 95% and changes in the position limit

Details fixed before running: plan §11.8 (C11). Code `analysis/h9_regime.py`; output `analysis/output/h9_results.txt`.
Outcomes use each stock's own basis distribution on non-ban days with utilisation below 60%: U = 1 if the basis is above
that distribution's 80th percentile, L = 1 if below its 20th, and the level relative to its median.

**Part A, anticipation (non-ban days, 2015 to September 2025, 423,104 stock-days).** Pre-specified statistic: slope of U on
utilisation between 0.60 and 0.95, stock and date fixed effects: +0.079 (se 0.038), one-sided p = 0.019.

| Utilisation the day before | Share of days in the upper tail | U coefficient vs below 0.60 (se) | L coefficient (se) |
|---|---|---|---|
| below 0.60 | 0.200 | 0 | 0 |
| 0.60 to 0.70 | 0.22 | +0.009 to +0.012 (0.007) | 0.000 to -0.004 |
| 0.75 to 0.80 | 0.26 | +0.040 (0.009) | +0.006 (0.011) |
| 0.80 to 0.90 | 0.26 to 0.27 | +0.034 to +0.040 (0.010 to 0.011) | +0.001 |
| 0.90 to 0.95 | 0.27 | +0.031 (0.013) | +0.008 (0.013) |

Reading. As utilisation approaches the trigger the upper tail of the basis grows (more days with rich futures), while the
lower tail and the average level (after date effects) do not change: the upper edge loosens, as the model's anticipation
result predicts, and there is no further jump at 95% on non-ban days. The rise comes more as a step around 0.75 than as a
smooth slope. As stated in advance, high utilisation also signals demand pressure, so this is anticipation plus pressure.
Without date effects the median basis also rises with utilisation (0 to +4.9 bp), but that rise reflects periods with
high utilisation across many stocks.

**Part B, the 1 October 2025 formula (208 stocks; window July to December 2025).** Intensity = size of each stock's cut
in the MWPL (log points 0.24 to 0.69). First stage: utilisation rises by 0.28 per unit of intensity (se 0.03). Pre-specified
statistic: Post x intensity on U +0.061 (se 0.050), one-sided p = 0.11; level +4.8 bp (4.8); bans +0.023 (0.019); L -0.038.
All point in the predicted direction (bigger cuts, more upper-tail days and bans), none is significant. Robustness: predicted
utilisation change instead of intensity +0.008 (0.041) for U; non-ban days only +0.067 (0.050); window to March 2026 +0.051
(0.043). Monthly event study for the level: July +15.5 (8.0), August +2.5, October to December +9 to +12 (6 to 7.5), so
pre-trends are noisy.

**Part C, quarterly resets (January, April, July 2026; stacked).** First stage +0.24 (0.05); U +0.051 (0.052), level +3.9
(4.8), bans -0.002: no detectable effect.

## 14.12 Secondary: H2, bad news in bans

Details fixed before running: plan §11.9 (C12). Code `analysis/h2_badnews.py`; output `analysis/output/h2_results.txt`.
Events: 8,586 results announcements of F&O stocks, 179 with day 0 in a ban (55 bad news, 58 good news); low power was
stated in advance. Bad and good news are the bottom and top terciles of the announcement return within each quarter.

**Drift (pre-specified).** Buy-and-hold abnormal return over days +2 to +64 on bad, good, ban and their interactions,
quarter fixed effects. Outside bans the drift after bad news is -1.25% against the middle tercile (se 0.38) and +0.30%
after good news. In bans: Ban x Bad +0.7% (se 3.4), one-sided p (< 0) = 0.59; Ban x Good -1.3% (3.1). No evidence that bad
news drifts more in a ban; the standard errors are about ten times the effect sizes found elsewhere. Robustness (stock
fixed effects, near-ban comparison events only, ban on any of days 0 to +5, unwinsorised, pre-reform only) gives Ban x Bad
between -2.5% and +1.5%, all insignificant.

**Pre-announcement basis (pre-specified).** Mean basis over days -5 to -1 relative to the stock's normal median. Outside
bans it is 2.0 bp lower before bad news than before good news (se 1.1, one-sided p = 0.039; 1.1 bp with stock fixed effects),
the direction reported by Saurav, Srivastava and Agarwalla (2026). In bans (110 events with a ban on day -1) the
difference cannot be estimated with useful precision (change +3.0, se 20.1). The basis before announcements in a ban is
about 20 bp lower for both bad and good news, in line with the low in-ban level found in 14.7.

**Also reported, cash-only versus F&O stocks (association).** All 72,429 events with a size decile, quarter and size-decile
fixed effects: relative to F&O stocks, cash-only stocks drift -0.67% more after bad news (se 0.42) and +2.40% more after
good news (se 0.43). Prices of cash-only stocks under-react in both directions, which does not show the bad-news
asymmetry the short-sale mechanism predicts; the F&O entry and exit design (14.5) is the causal test of that channel.

## 14.13 Secondary: H1, frictions and mispricing

Details fixed before running: plan §11.10 (C13). Code `analysis/h1_frictions.py`; output `analysis/output/h1_results.txt`.
Stock-quarters of F&O stocks, outcomes from 2015 Q2 to 2025 Q3 on non-ban days (7,398 stock-quarters, 347 stocks); frictions
from the previous quarter. Index = first principal component of five frictions standardised within quarter: Corwin-Schultz
spread (loading +0.57), log Amihud illiquidity (+0.37), idiosyncratic volatility (+0.55), utilisation of the MWPL (+0.45)
and SLB scarcity (share of days without any SLB trade, +0.18); it explains 44% of their variance.

**Pre-specified result:** a one standard deviation higher index goes with a band (q80 - q20 of the basis) 3.5 bp wider
(se 1.1, one-sided p = 0.002; mean width 40.8 bp) and a mean absolute basis 2.5 bp larger (se 0.7, p = 0.0006). Persistence
(the daily autoregressive coefficient of the basis, mean 0.41) is lower, not higher, in high-friction stocks (-0.033, se
0.006), contrary to the prediction; daily measurement noise is larger in less liquid stocks and lowers measured
persistence, so this measure is not reliable at a daily frequency.

Also reported. All five frictions jointly: Amihud illiquidity (+6.4) and idiosyncratic volatility (+2.5) and the spread
(+1.6) widen the band; utilisation does not (-1.0); **SLB scarcity has the wrong sign (-9.7)**: stocks with more SLB trading
have wider bands, which suggests that SLB activity reflects demand to borrow rather than ease of borrowing. The index
without the SLB input gives +4.5 (1.2). With stock fixed effects the effect disappears (0.0, se 1.7): the relation is
between stocks, not within a stock over time. Including ban days +4.1; period to 2026 Q3 +3.6. The median annualised SLB
fee, where a stock is lent at all, is 3.5% a year (10th to 90th percentile 0.9% to 12.4%).

Reading. Frictions line up with wider bands and larger mispricing across stocks, as the model's band result implies, but
the evidence is an association across stocks (frictions travel with size and liquidity), not variation over time within
a stock.

## 14.14 Secondary: H4, arbitrage capital

Details fixed before running: plan §11.11 (C14). Code `analysis/h4_capital.py`; output `analysis/output/h4_results.txt`.
Monthly series May 2018 to September 2026 (101 months). Arbitrage-fund assets (AMFI) grew from about Rs 57,000 crore to
Rs 2.98 lakh crore; flows are net inflows as a share of the previous month's assets (mean 1.9%, sd 6.9%). Outcome: the 80th
percentile of the basis across all non-ban stock-days of the month (mean 17.6 bp).

**Pre-specified result:** q80 on last month's flow, with step dummies for April 2023 (tax change and STT), October 2024
and April 2026 (STT), Newey-West errors: -17.5 bp per unit flow (se 14.2), one-sided p = 0.11; a 10% inflow goes with a
1.7 bp lower upper quantile the next month. Direction as predicted, not significant.

Also reported: same-month flow +4.5 (14.7), consistent with the return-chasing bias stated in advance; change in log assets
+4.2; log assets with a trend -5.2 (3.3), p = 0.06; q90 -22.1 (15.0), p = 0.07; median -14.4; q20 -11.7; first differences
**-20.6 (se 6.8), p = 0.001**; adding the change in the interbank rate -17.6; excluding March to May 2020 -17.6 (21.9);
before April 2023 -26.0 (16.5), p = 0.06; from April 2023 +17.1 (16.9). The April 2026 STT step is +5.0 bp (1.8).

Reading. There is weak evidence that inflows of arbitrage capital are followed by a lower upper quantile of the basis,
mainly before April 2023 and in month-on-month changes; after the 2023 tax change, when assets grew fastest, the relation
is not visible. With about a hundred monthly observations and flows that chase returns, the test has little power.

## 14.15 Secondary: H5, anomaly returns by short-sale constraint

Details fixed before running: plan §11.12 (C15). Code `analysis/h5_anomalies.py`; output `analysis/output/h5_results.txt`.
All NSE stocks priced at Rs 5 or more, signals at each month-end from January 2016 to September 2026, returns the next month
(228,795 stock-months). Constraint groups at each month-end: G1 F&O stocks (median market cap Rs 43,513 crore), G2
cash-only stocks with SLB trades in the last three months (Rs 11,402 crore), G3 cash-only stocks without SLB trades (Rs 770
crore). Within each group, stocks are sorted into terciles of a composite mispricing score (average percentile rank of
momentum, short-term reversal, maximum daily return, idiosyncratic volatility, illiquidity and turnover, oriented so that
high means overpriced). Legs are measured against the group's value-weighted return.

**Pre-specified result (value-weighted):** short leg G1 -0.17% a month (se 0.25), G3 -0.13% (0.16); difference G3 - G1
+0.04% (Newey-West se 0.20), one-sided p = 0.57; long-leg difference -0.03% (0.14). The overpriced side does not do worse
where shorting is constrained.

| Check | Short leg G3 - G1 (se) | Long leg G3 - G1 (se) |
|---|---|---|
| Equal-weighted | **-0.49% (0.16)**, p = 0.001 | **+0.46% (0.15)** |
| Excluding stocks below median market cap | +0.06% (0.21) | -0.18% (0.11) |
| Holding months to September 2025 | +0.01% (0.22) | +0.01% (0.15) |
| G2 vs G1 (value-weighted) | -0.01% (0.38) | -0.09% (0.27) |
| IVOL terciles as groups (I3 - I1) | +0.02% (0.27) | -0.64% (0.54) |

Single anomalies (value-weighted long-short returns per month, G1 / G2 / G3): momentum +0.36% / +0.94% / +1.12%, with the
short leg of constrained stocks lower by 0.51% (se 0.22), as the model predicts; short-term reversal +0.55% / +0.26% / -0.10%
(the opposite pattern); maximum return, idiosyncratic volatility, illiquidity and turnover show no systematic
difference.

Reading. Value-weighted, there is no sign that constrained stocks' overpriced side underperforms more. Equal-weighted, the
anomaly spread is much larger among small cash-only stocks, but on both sides (long leg +0.72%, short leg -0.87% a month in
G3), which is a small-stock effect rather than the one-sided pattern of the short-sale mechanism. Momentum alone fits the
prediction. The groups differ greatly in size, which limits what this comparison can show (caveat stated in advance).

## 14.16 Summary of the secondary tests

| Test | Pre-specified statistic | Result | In one line |
|---|---|---|---|
| Level effect (14.7) | D(rising OI) - D(falling OI) < 0 | -15.2 bp, p = 0.083 | Signs as predicted; basis falls about 6 bp at ban start; closing group tiny; same-day-control version weak |
| Density at 95% (14.8) | CJM test | p = 0.86 | No bunching; RD usable as supporting |
| RD at 95% (14.9) | jump in basis level | -12.9 bp, p = 0.02 | Gap already present on the crossing day; trading jumps are sharp |
| Hysteresis (14.10) | Ban coefficient | +0.4 bp, p = 0.64 | No extra level shift at equal utilisation and path; trading effects as H8 |
| H9 anticipation (14.11 A) | slope of upper-tail share | +0.079, p = 0.019 | Upper tail widens as utilisation rises (anticipation plus pressure) |
| H9 reform (14.11 B) | Post x intensity on upper tail | +0.061, p = 0.11 | Right direction, not significant; strong first stage |
| H2 (14.12) | Ban x Bad on drift | +0.7%, p = 0.59 | No power; pre-announcement basis pattern found outside bans |
| H1 (14.13) | friction index on band width | +3.5 bp per sd, p = 0.002 | Across stocks yes; not within stocks; persistence measure fails |
| H4 (14.14) | lagged flow on q80 | -17.5, p = 0.11 | Weak; significant in first differences and before 2023 |
| H5 (14.15) | short leg G3 - G1 | +0.04%, p = 0.57 | Not supported value-weighted; symmetric small-stock effect equal-weighted |

All secondary p-values are unadjusted, as the plan states; with ten secondary statistics, one or two values below 0.05
would be expected by chance even with no effects.

## 14.17 Further checks from the master plan (exploratory)

Specified before running in the plan's log (§11.15). Code `analysis/spurious_bans.py`, `analysis/placebos.py`,
`analysis/covid_halving.py`; outputs of the same names.

**How many bans were "spurious"?** Before October 2025 bans were driven by open interest, not by the limit: on the day
utilisation crossed 95% the MWPL fell for 8 of 1,744 entries, and only 7 (0.4%) would not have crossed at the previous
day's limit. For the year after the reform, a simulation of the ban rule (which reproduces the official ban lists exactly)
compares the new rule with counterfactual rules for the same stocks:

| Rule (1 Oct 2025 to 27 Oct 2026) | Ban stock-days | Spells | Stocks |
|---|---|---|---|
| New rule: delta-adjusted OI, new MWPL (actual) | 412 | 45 | 11 |
| Old rule: gross OI, old-formula limit | 1,505 | 112 | 36 |
| Gross OI, new MWPL | 6,256 | 296 | 85 |
| Delta-adjusted OI, old-formula limit | 1 | 1 | 1 |

The reform cut bans by about three quarters relative to the old rule. Measuring open interest in delta terms removes almost
all bans; the lower limit on its own would have multiplied them; the new rule combines the two. (The old-formula limit
keeps each stock's ratio of old to new limit from 1 October 2025, an approximation.)

**Placebos.** Shifting every pre-reform ban spell 60 trading days later (same stock and length, away from real bans) gives
no H7 effect (delta_up +0.037, se 0.047; delta_lo -0.028, se 0.038) and no level effect (mean +1.0 bp, no composition
gradient), so neither result is produced by the method. The index-derivative reforms of November 2024, February 2025 and
April 2025 do not move single-stock band edges beyond the placebo range. The peak-margin phases of December 2020 to
September 2021 move the upper percentile in both directions (+9.6 bp at 50%, -9.9 bp at 75%), with no consistent effect.

**The 2020 halving and restoration of the MWPL.** When the limit was restored for 70 stocks on 27 November 2020, their
utilisation fell by 0.21 (se 0.02) and their ban days by 4.6 percentage points relative to other F&O stocks, and their
basis was less often in its upper tail (-0.068, se 0.032), as the anticipation result predicts: a looser limit makes rich
futures less common. The basis level did not change significantly (-2.8 bp), and a fake date 20 days earlier shows no
effect on utilisation, bans or the upper tail. Futures volume rose, but it was already rising before. The March 2020
halving coincided with the crash and selected stocks on volatility and utilisation; it is reported but not interpreted.
