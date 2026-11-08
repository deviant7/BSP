# Pre-analysis plan — v1 (28 Oct 2026)

**Status.** Final; frozen with the git tag `pap-v1` (5 Nov 2026, after the guide's go-ahead and the data audit).
**Until the tag, no outcome was related to any treatment.** After the tag, every change is logged in §11 with date and
reason; results under the original specification are always reported.

**Pre-tag revisions from the data audit (5 Nov 2026; no outcome had been related to any treatment):**
(a) days without an official ban list (6 May 2025; 19 Feb and 25 Aug 2014) use an imputed list (previous day's "No Fresh
Positions" flags plus continuing spells), flagged; (b) months after the last published interbank rate use the last value,
at most two months forward, flagged `r_filled` (robustness: drop them); (c) results day 0 now comes from the earliest of the
exchange's "Financial Result Updates" announcement and the filing, with board meetings filling gaps and overriding late
re-filing times, and records mapped to the symbol trading on the event date (the filing feed alone dated 51.5% of F&O
events too late); if the release time is unknown, day 0 = next trading day after the release date (robustness: drop
these events); (d) power counts in §8 updated.
Previous version: `plan/archive/pre_analysis_plan_v0_draft_2026-10-28.md`.

---

## 1. Data (built; see `data_pipeline/README.md`)
| Object | Source | Coverage | Key checks passed |
|---|---|---|---|
| MWPL, OI, FutEq OI, ban flag | NSE combineoi | Feb 2010 – 27 Oct 2026 | flags vs next-day ban list 99.85%; 95%/80% rules hold in 99.2%/99.5% of spells |
| Ban list | NSE fo_secban | same | — |
| F&O membership | STF rows of F&O bhavcopy | 2015 – 27 Oct 2026 | identical to an independent membership sheet (2016–2025) |
| Futures, cash, delivery | NSE bhavcopies, MTO | 2015 – 27 Oct 2026 (gap: F&O file 30 Mar 2021) | VWAP inside [low, high] 99.77%; 100% cash match |
| Dividends, corporate events | NSE corporate-actions API | 2014 – 2026 | parser separates dividends from splits ('sub-division') |
| Results announcements | NSE 'Financial Result Updates' announcements + results filings (Integrated Filing from Mar 2025 quarter) + board meetings | 2014 – 2026 | 98–100% of F&O stock-quarters; release time known for 99% |
| Rates | OECD MEI via FRED: 3-month interbank (main), call money | monthly, 2011 – 2026 | — |

## 2. Samples
- **Basis sample:** stock-days on which the stock is in the F&O segment (STF listed), 1 Jan 2015 – 27 Oct 2026.
  Contract: near-month; switch to next month when ≤ 3 trading days to expiry. Require ≥ 5 futures contracts traded.
- **Main exclusions:** dividend (`pv > 0`) or other corporate event (`event_in_life`) going ex within the contract life;
  first 20 trading days after F&O entry; rows whose lot size could not be recovered (VWAP outside [low, high]).
- **Pre-sample** 2010–2014 (ban/MWPL only) for robustness of treatment-side results.
- **Cash universe (Ch 6):** all NSE EQ/BE/BZ stocks, 2015 – 2026.

## 3. Outcomes
- **O1 basis (primary):** m_it = ln F̄_it − ln(S̄_it − PV_it(D)) − r_t·τ_it; F̄, S̄ daily VWAPs; r = 3-month interbank
  (monthly); τ = calendar days to expiry / 365. Secondary: close-based basis (theoretical-settlement days flagged).
- **O2 relative implied repo:** r̂_it = [ln F̄ − ln(S̄ − PV)]/τ minus the day's cross-sectional median (τ ≥ 7 days).
- **O3 reversion:** Δm_it on m_{i,t−1} by regime (§5).
- **O4 trading:** futures contracts traded, ΔOI (contracts), ΔOI + volume, cash volume, delivery %.
- **O5 earnings drift:** BHAR[+2,+64] (vs size-matched F&O/cash portfolio); surprise = EAR = abnormal return [−1,+1] around day 0
  (main); SUE from XBRL EPS (secondary, if extraction succeeds). Day 0 = release day if released before 15:30, else next
  trading day (time unknown: next trading day after the release date).
- **O6 cash efficiency:** Hou–Moskowitz delay (weekly returns, 52-week windows), VR(5).

## 4. Treatments
- **Ban:** official ban list; ω = OI/MWPL (gross OI before 1 Oct 2025, FutEq OI from 1 Oct 2025), measured on day t−1.
- **MWPL shocks:** (a) COVID halving: MWPL halved for 61 stocks in files dated 20–27 Mar 2020 (effective next trading day),
  restored for 70 on 26 Nov 2020; (b) 1 Oct 2025 formula: intensity = ln(MWPL_new/MWPL_old) and the predicted change in
  utilisation using pre-reform OI composition; (c) quarterly MWPL resets after Oct 2025.
- **Cost shocks:** futures STT 1 Apr 2023 (0.01→0.0125%), 1 Oct 2024 (→0.02%), 1 Apr 2026 (→0.05%).
- **Capital:** 1 Apr 2023 debt-fund tax change (same day as an STT change → not separately identified in the time series);
  arbitrage-fund AUM (AMFI, monthly from mid-2018; to be collected).
- **Short channel:** F&O entries (233 usable) and eligibility exits (158 usable), 2015–2026; batches on 29 Nov 2024 (45 entries),
  28 Jun 2019 (34 exits), 28 Feb 2025 (16 exits).

## 5. Primary hypotheses (family for multiple-testing correction)
**H7 — one-sided correction in bans.**
Δm_it = Σ_r [β_r + δ_r·Ban_it]·(m_{i,t−1} − μ_i)·1{regime r} + α_i + λ_t + e_it,
regimes: upper = m_{i,t−1} above the stock's 80th percentile of m on non-ban days; lower = below the 20th percentile.
Prediction: δ_upper > 0 (upward deviations revert less), δ_lower ≤ 0 (unchanged or faster). Interaction with "expiry has
occurred inside the current ban spell": δ_lower closer to 0 after it. *Fails if* δ_upper ≤ 0, or δ_upper = δ_lower.
Robustness: thresholds from 3-regime TVECM per stock (non-ban days), fixed ±25 bp around the stock median.

**H8 — mechanism: trading moves out of futures.**
On ban days (pre-Oct 2025): ΔOI_t + Vol_t ≈ 0 for near+next futures; futures volume falls and cash volume / delivery share rise
relative to the stock's own non-ban days with similar ω. *Fails if* ΔOI + Vol is not ≈ 0 or futures activity does not fall.

**H3 — costs set the band edges.**
Event windows ±40 trading days around each STT date; outcome: stock-level upper/lower quantiles (80/20) of m and the TVECM
thresholds, pre vs post, all F&O stocks. Prediction: upper edge rises; size ordered with the cost change (2026 > 2024 > 2023).
*Fails if* no shift or the ordering is unrelated to the cost change. (2023 confounded with the tax change: reported, not
claimed.)

**H6 — short-sale access lowers overpricing and speeds up bad news.**
Staggered DiD (Callaway–Sant'Anna; Sun–Abraham as check) for entries and, separately, eligibility exits; controls: not-yet-treated
and never-treated cash stocks matched on size, turnover and volatility in the 6 months before. Outcomes O5 (bad-news drift),
O6 (delay). Prediction: after entry, bad-news drift and delay fall; reverse after exit. *Fails if* no change or opposite signs.

## 5b. Lesson from estimators on simulated data (before any real-data estimation)
A fixed-threshold 3-regime TAR recovers known thresholds well (true −30/+15 bp → −29.1/+15.2), but on a basis simulated from
the model (thresholds move with arbitrage inventory) it does not recover the cost band (estimates −10/0 bp vs c₊ = 15 bp).
Therefore: (i) estimated fixed thresholds are reported as *average* band edges, not as costs; (ii) H3 compares the *change* in
edges across STT dates (inventory roughly unchanged within ±40 days) rather than their levels; (iii) a threshold model whose
thresholds depend on lagged OI/MWPL (state-dependent band) is added as the main robustness for H7 and H3
(`analysis/test_setar_simulated.py`).

## 6. Further pre-specified tests (secondary; reported, labelled exploratory)
- **Level effect of bans (Prop. 6):** stacked ban-entry event study (window −20…+20; controls = stock-days with ω ∈ [0.85, 0.95)
  in the same week that do not enter, matched on 5-day ω path and basis level); split by composition of pre-ban activity
  (ΔOI/volume over 5 days before entry: rising OI = new-exposure demand; falling = closing). Prediction: sign follows composition.
- **H9 regime and anticipation:** basis quantiles by ω bins (0.60–0.95) on non-ban days; 1 Oct 2025 intensity DiD (stock and date
  FE). Prediction: upper quantile rises smoothly with ω; reform effect follows the intensity.
- **RD at 95%:** local linear on ω_{t−1}; Cattaneo–Jansson–Ma density test first. Supporting only.
- **Hysteresis:** ω ∈ [0.80, 0.95): in-ban vs not-in-ban, controlling for ω, Δω, 5 lags of m.
- **H2:** bad-news drift on ban days vs non-ban days (180 announcements in bans → low power, stated in advance); pre-announcement
  basis (days −5…−1) in bans vs not.
- **H1:** friction index (bid–ask proxy, Amihud, IVOL, lagged headroom 1−ω, SLB availability if obtained) vs band width.
- **H4:** arbitrage-fund flows vs the upper quantile of the cross-sectional basis (monthly).
- **H5:** anomaly asymmetry by constraint terciles (double sorts).

## 7. Inference
Two-way clustered SEs (stock, date). Event studies with few clusters: wild-cluster bootstrap. Primary family {H7, H8, H3, H6}:
Holm correction at 5%. Outliers: main estimates winsorise m at 1/99% within year; robustness without.

## 8. Power notes (treatment-side counts, known before any outcome analysis)
Ban spells 2015–2026: 1,788 (44 after Oct 2025); ban stock-days 9,416; stocks ever banned 141; not-in-ban stock-days with
ω ∈ (0.90, 0.95]: 2,439 pre-reform / 139 post; F&O entries 233 / eligibility exits 158; F&O announcements 8,594 (180 on ban
days). Post-reform ban analyses and H2-in-bans are low-powered.

## 9. Falsifiers (from the model)
No upper/lower asymmetry in bans (H7); no change in futures activity in bans (H8); band unrelated to dated cost shocks (H3);
no effect of F&O entry/exit on delay or bad-news drift (H6).

## 10. Open items that do not change the specification
AMFI arbitrage-fund AUM series; XBRL EPS extraction for SUE; index dividends for the Nifty futures check; SLB data.

## 11. Deviations log
Entries are dated. "Clarification" = a detail the plan left open, fixed before any test was run; "Deviation" = a change
to something the plan specified.

### 11.1 Clarifications fixed on 5 Nov 2026, after the tag and BEFORE any primary or secondary test was run
Only treatment-side counts had been looked at (stock-days by lagged utilisation bin and ban status).

**C1. Analysis sample for all basis tests (§2, §3).**
(a) Trading days to expiry d_t = number of trading days after t up to and including the expiry day (expiry day: d = 0).
The near contract is used if d_t > 3, otherwise the next contract. Contracts are identified by expiry date, not by order.
(b) ">= 5 contracts" applies to the chosen contract on day t. (c) Exclusions apply to the chosen contract row: dividend
going ex within its life (pv > 0), other corporate event (event_in_life), missing VWAP (lot failure), and trading days 1 to
20 of a membership spell that starts with an F&O entry event. (d) Delta m_t = m_t - m_(t-1) for the same contract on the
previous trading day; the day-(t-1) row must satisfy (b) and (c) itself (it need not be the chosen contract at t-1, e.g. on
a switch day). (e) Winsorisation: 1st and 99th percentiles of m per calendar year, computed on the chosen-contract sample,
applied to every level (m_t and m_(t-1)) by the year of its date; Delta m uses the winsorised levels. (f) Ban_it = stock on
the ban list for day t (official or imputed). omega_(t-1) = util (gross OI) on files dated before 1 Oct 2025, util_futeq
from 1 Oct 2025, taken from the previous trading day's file.

**C2. H7.** (a) mu_i, and the 20th/80th percentiles defining the regimes, are computed from stock i's analysis-sample
levels m_t on non-ban days over the full sample (winsorised). Stocks with fewer than 100 such observations are dropped.
(b) The regression includes the middle regime: all three regimes have a beta and a delta. (c) "Expiry inside the current
ban spell": PostExp_it = 1 if Ban_it = 1 and an expiry date of the stock's futures falls in [spell start, t-1]; the
interaction (m_(t-1) - mu_i) x regime x Ban x PostExp is added in a second specification. (d) Test statistic for the
multiple-testing family: intersection-union p-value p_H7 = max(p1, p2), p1 one-sided for delta_upper > 0, p2 one-sided for
delta_upper - delta_lower > 0, two-way clustered standard errors (stock, date). (e) Main estimate pooled 2015 to 2026;
pre- and post-1 Oct 2025 reported separately. (f) Robustness thresholds: fixed +/-25 bp around mu_i; per-stock thresholds
from the 3-regime threshold autoregression of the basis on non-ban days (`analysis/setar.py`; the basis imposes the
cointegrating vector beta = 1, so the univariate threshold model on m is used in place of a TVECM); state-dependent
thresholds = the 20th/80th percentiles computed separately within each stock's terciles of omega_(t-1) on non-ban days.

**C3. H8.** (a) Period 1 Jan 2015 to 30 Sep 2025 (gross-OI rule); post-reform days reported descriptively only.
(b) Expiry days of the near contract are excluded. (c) Delta OI and volume summed over the near and next contracts, in
contracts: Delta OI = chg_oi / lot_used, volume = contracts traded. R_it = (Delta OI + V) / V for V > 0. (d) Identity
test: mean and median of R on ban days with bootstrap (stock-clustered) confidence intervals, against non-ban days.
R >= 0 always holds arithmetically; the prediction is R close to 0 in bans. Pre-set reading: the identity "holds" if the
mean of R on ban days is below 0.10 and below one tenth of the mean on comparison non-ban days. (e) Comparison sample:
stock-days with omega_(t-1) in [0.80, 0.95) (the only range where both ban and non-ban days exist; above 0.95 there are
almost no non-ban days). Regressions of y on Ban with stock-by-bin fixed effects (bins [0.80, 0.85), [0.85, 0.90),
[0.90, 0.95)) and date fixed effects, two-way clustered SE; y = log(1 + futures contracts, near + next),
log(1 + cash shares traded), delivery share (deliverable / traded quantity, EQ series), and R. (f) Test statistic for the
family: one-sided p-value that the Ban coefficient on log futures contracts is < 0.

**C4. H3.** (a) Event days: 3 Apr 2023 (first trading day on or after 1 Apr 2023), 1 Oct 2024, 1 Apr 2026. Pre window
= the 40 trading days before the event day; post window = the event day and the next 39 trading days. (b) Analysis
sample of C1; stocks with at least 20 observations in each window. (c) Stock-level outcome: Delta q80_i = 80th percentile of
winsorised m in the post window minus that in the pre window (also q20 and the median). (d) Test statistic for the family:
one-sided p-value that the mean of Delta q80 over stock-event observations from the 2024 and 2026 events (2023 excluded as
confounded) is > 0, standard errors clustered by stock. (e) Ordering 2026 > 2024 > 2023 judged on point estimates
(descriptive; three events). (f) Placebo: the same statistic at pseudo-event days spaced 80 trading days apart from
Jan 2015, excluding any window overlapping a true STT date; the true events' ranks in this distribution are reported.
(g) Threshold-model edges: pooled 3-regime threshold model on stock-demeaned m within each window (robustness).

**C5. Family.** Holm at 5% over {p_H7, p_H8, p_H3, p_H6}. H6 details are fixed in a later dated entry before it is run.

### 11.2 Analyses added after seeing results (exploratory; the pre-specified results are always reported first)
- 5 Nov 2026, H8: the pre-specified identity reading failed (ban-day mean R = 0.42). Diagnostics showed a break in ban-day
  R between 6 and 24 March 2020 (before: mean 0.86, no day with R <= 0.01; after: mean 0.10, median 0.012), absent on
  non-ban days, with NSE's change-in-OI field equal to the change in OI levels. Added an exploratory split at 15 Mar 2020.
  The cause (probably intraday round trips tolerated in bans before then) is not documented in sources found so far.
- 5 Nov 2026, H8 (resolution of the break): SEBI press release 18/2020 (20 Mar 2020; clearing-corporation notice of
  22 Mar 2020) made the clearing corporations identify ban violations "based on the monitoring of peak intraday positions"
  from 23 Mar 2020 (before: end-of-day positions only), continued "till further directions" by PR 59/2020 (25 Nov 2020).
  From 1 Oct 2025 NSE Clearing 119/2025 checks entity positions at end of day in FutEq terms. Ban-day R by regime: to
  22 Mar 2020 mean 0.855 / median 0.871; 23 Mar 2020 to 30 Sep 2025 mean 0.099 / median 0.011; 1 Oct to 7 Dec 2025 median
  0.193; from 8 Dec 2025 median 0.357. The identity holds when the rule is enforced intraday, as the model's P7(i) assumes.
- 5 Nov 2026, H7 (exploratory diagnostics, `analysis/h7_diagnostics.py`): the reversal is stronger, not weaker, on liquid
  days (>= 1,000 contracts on t and t-1: delta_up -0.154, delta_lo +0.130), so measurement noise does not explain it;
  end-of-day-enforcement era: delta_up +0.016 (n.s.), delta_lo +0.126; peak-intraday era: delta_up -0.201, delta_lo
  -0.120; faster upward reversion concentrated in the first 4 calendar days of a spell (-0.163 vs -0.008 later).
  Reading (post hoc, not a confirmation): blocked new-exposure demand at ban start (model P5/B2) removes the pressure that
  made futures rich; the pre-specified H7 isolates P4 and ignores this opposing channel.
  (Wording corrected 7 Nov 2026: "first 4 calendar days" means the spell's start day and the next four calendar days,
  i.e. 0 to 4 calendar days after the start, as coded in `analysis/h7_diagnostics.py`; the numbers are unchanged.)
- 5 Nov 2026, H3 (exploratory calibration): against the 30 pre-specified placebo dates, the average Delta q80 of 2024 and
  2026 is exceeded by 4.6% of placebo pairs; band width (q80 - q20) by 23.4%; q80 relative to the median by 27.4%. The
  rise is mostly a common level shift; stock-clustered SEs ignore cross-sectional correlation (Kolari and Pynnonen 2010).

### 11.3 Clarifications for H6, fixed on 5 Nov 2026 BEFORE any H6 outcome was related to F&O status
Inputs built first (no outcome-by-treatment output): split/bonus/dividend-adjusted daily returns for all EQ/BE/BZ stocks
(`data_pipeline/build_returns.py`; NSE's prevclose is not adjusted) and daily market capitalisation from AMFI's half-yearly
lists (direct from Jul 2017; back-cast with split factors before that; `data_pipeline/build_amfi_mcap.py`, `build_mcap.py`).

**C6. H6.** (a) *Treated units.* Entries: a stock's first F&O entry in the sample (stocks in F&O on 1 Jan 2015 are never
in the entry design); established stocks only (fno_events note blank). Eligibility exits: a stock's first exit with
continued cash trading (note blank). Post periods are censored at the next opposite event (exit after an entry, re-entry
after an exit). (b) *Time unit:* calendar years 2015 to 2025 (2026 incomplete, not used). Cohort g = first calendar year
fully after the event (event year + 1); the event year itself is a transition year and is excluded for that unit
(anticipation = 1 year in Callaway-Sant'Anna terms, so the base period is g - 2). (c) *Controls:* entries: not-yet-treated
and never-treated cash-market stocks (never in F&O during 2015 to 2026); exits: not-yet-exited and never-exited F&O stocks.
Covariates (Callaway-Sant'Anna outcome-regression estimator) measured in the base year: log average market cap, log
average daily traded value, standard deviation of daily returns. (d) *Outcome O6, price delay:* Hou-Moskowitz
D1 = 1 - R2(restricted)/R2(unrestricted) from calendar-week returns in the calendar year, regressing the stock's weekly
return on the contemporaneous value-weighted cash-universe return (restricted) plus four weekly lags (unrestricted);
at least 40 valid weeks. (e) *Outcome O5, bad-news drift:* EAR = cumulative return over days -1 to +1 minus that of the
equal-weighted portfolio of the stock's market-cap decile (deciles formed each month on the previous month-end market cap,
whole cash universe); bad news = EAR in the bottom tercile of all EARs in the same calendar quarter; BHAR[+2,+64] = buy-
and-hold return from day +2 to +64 minus the buy-and-hold return of the same decile portfolio (at least 50 valid daily
returns). Because drift exists only at announcement events, H6-drift is estimated as a stacked difference-in-differences at
the announcement level (one stack per event cohort year; treated stocks' bad-news events and those of clean controls as in
(c), three years either side; stack-by-stock and stack-by-quarter fixed effects; SE clustered by stock), which keeps the
Callaway-Sant'Anna comparison of treated cohorts with not-yet- and never-treated units. (f) *Main estimates:* delay: overall
ATT (cohort-size-weighted average of post-period ATT(g,t)), with event-time profile; drift: Treated x Post coefficient
on bad-news BHAR. Inference: cluster (stock) bootstrap, 499 draws, for the Callaway-Sant'Anna aggregates.
(g) *Predictions:* entry: delay ATT < 0, bad-news BHAR ATT > 0 (drift weaker); exit: delay ATT > 0, bad-news BHAR ATT < 0.
(h) *Test statistic for the family:* p_H6 = min(1, 4 x min of the four one-sided p-values) (Bonferroni across the four
components); each component is reported. (i) *Sun-Abraham check:* interaction-weighted event study on the annual delay
panel with never-treated units as the reference. (j) *Robustness:* drop the batch cohorts (entries in 2024 incl. the
29 Nov 2024 batch; exits in 2019 incl. the 28 Jun 2019 batch); drop stock-years whose market cap is back-cast; VR(5)
as an alternative efficiency outcome.
(k) *Added the same day, still before any H6 outcome was related to F&O status* (after inspecting outcome
distributions alone): sub-rupee stocks produce tick-size artefacts (a Rs 0.05 to Rs 0.10 move is a 100% return; the
largest BHARs exceed 8,000). Therefore: events with a day-0 closing price below Rs 5 are excluded; duplicate events
(same stock and event day) are counted once; EAR and BHAR are winsorised at 1% and 99% within each calendar year for the
main estimates (robustness without); stock-years with an average price below Rs 5 are excluded from the delay panel;
in the drift design, control stocks are restricted to the range (min, max) of base-year log market cap of the treated
cohort in the stack.

### 11.4 Clarifications for the level effect (PAP §6, first bullet), fixed on 7 Nov 2026 BEFORE any basis value was related to a ban entry
Looked at first (treatment side and data availability only; no basis value): of 1,744 pre-reform ban spells (2015 to
Sep 2025), 1,201 have at least 5 non-ban trading days before the start (a quarter re-enter within 3 days of the previous
spell); the composition ratio C (below) has median +0.053 and only 142 spells (8.1%) have C <= 0, as expected because open
interest must rise for utilisation to cross 95%; candidate control stock-days total 2,451; 79.5% of spells have at least
one candidate in the same calendar week, 51% at least five.

**C7. Level effect.** (a) *Events:* ban spells starting 1 Jan 2015 to 30 Sep 2025; day 0 = first ban day (t0). Required:
no ban day for the stock on days -5 to -1; omega_(t-1) > 0.95 on day 0; a valid analysis-sample basis (C1) on day -1.
Post-reform spells (from 1 Oct 2025) are run the same way and reported separately (descriptive).
(b) *Composition:* C = (sum of Delta OI over days -5 to -1) / (sum of futures volume over days -5 to -1), near + next
contracts, in contracts (as in C3 c). Pre-specified split: C <= 0 (closing pressure) versus C > 0 (new exposure).
Because only 8% of events have C <= 0, a second split at the median of C over events is added (high C = more new
exposure), and C is also used as a continuous variable.
(c) *Controls:* stock-days (j, s) of other stocks with s in the same calendar week (Monday to Sunday) as t0, omega_(s-1) in
[0.85, 0.95), not in a ban on any of days s-5 to s+5, valid basis on day s-1. Up to 5 nearest neighbours, with
replacement, by Mahalanobis distance on (omega on days -1 to -5, m_(-1)), covariance from the pooled candidate
pool. Events without any candidate are dropped (count reported).
(d) *Outcome:* for each event-time k, the change in the winsorised basis level from day -1, y_k = m_(t0+k) - m_(t0-1),
using the chosen contract of C1 on each day (levels, so a roll is allowed; treated and controls share the exchange's
expiry calendar). Event difference D_k = y_k(treated) - mean over available controls of y_k(control).
(e) *Main statistic:* per event, D = mean of D_k over k = 0 to min(4, L - 1), L = spell length in trading days (in-ban
days only, at most the median spell length). Units bp.
(f) *Prediction (Prop. 6):* the level effect falls with new-exposure demand: mean D lower for C > 0 than for C <= 0; with
the sign expected positive for C <= 0 and negative for large new demand. *Test statistic (secondary, reported
unadjusted):* one-sided p that the coefficient on 1{C > 0} in a regression of D on a constant and 1{C > 0} is < 0; also the
group means with their signs, the median-split version, and the slope on C (standardised). SEs two-way clustered by stock
and event date.
(g) *Also reported:* the event-time profile k = -20 to +20 (pre-trends; note earlier spells can fall before day -5);
robustness: same-day controls only; unwinsorised basis; relative implied repo; close-based basis; excluding imputed ban
days. Exploratory: the two pre-reform enforcement regimes (to 22 Mar 2020; 23 Mar 2020 to 30 Sep 2025).
- 7 Nov 2026, level effect (exploratory additions in `analysis/level_effect.py`, after the C7 results were seen): matching
  left the treated basis 10 bp below its controls on day -1, and the treated basis dips on day -1 (event-time profile
  about +4 to +6 bp before day -1). Added: (1) baseline = mean of D_k over k = -10..-2: level -11.3 bp (se 1.5), slope on
  standardised C -3.1 (p = 0.007), median split -4.5 (p = 0.049); (2) control for the day -1 treated-minus-control gap:
  gap coefficient -0.29 (mean reversion), level at mean C -9.2, slope -3.5 (se 1.6); (3) event-time paths by median C:
  high-C events fall about 7 to 8 bp on days 0 to 1 and recover by day 7. Pre-specified C7 results are reported first.

### 11.5 Clarifications for the density test at 95% (PAP §6, "RD at 95%": density test first), fixed on 7 Nov 2026 BEFORE it was run
This is a treatment-side test (utilisation only; no outcome).
**C8. Density test.** (a) *Running variable:* end-of-day utilisation omega_d from the file dated d (gross OI / MWPL before
1 Oct 2025; FutEq OI / MWPL from 1 Oct 2025); cutoff 0.95 (above it the stock enters the ban on d+1).
(b) *Main population (transition):* stock-days with the stock not in a ban on d-1 or on d and omega_(d-1) < 0.95, i.e. the
distribution of today's utilisation for stocks that were below the trigger yesterday. Reason: in the literal population
"all stock-days not in a ban", a stock above 0.95 is observed for one day only (it is in the ban from the next day)
while a stock just below can be observed for many days, so that density is discontinuous at 0.95 mechanically even
without any manipulation. One-step transitions from below do not have this absorption problem. The literal population
(not in a ban on d) is also reported, with this caveat.
(c) *Estimator:* Cattaneo-Jansson-Ma local-polynomial density test (Python `rddensity` 3.0; defaults: p = 2, triangular
kernel, jackknife variance, MSE-optimal bandwidths on each side, robust bias-corrected statistic), on omega in [0.60, 1.30].
Robustness: p = 1 and p = 3; fixed bandwidths 0.02 and 0.05.
(d) *Dependence:* the CJM test treats observations as independent; repeated days of the same stock are not. Therefore also a
McCrary-type binned estimate: frequencies in bins of width 0.0025, local linear fits on each side within 0.05 of the cutoff
(triangular weights), theta = ln f(0.95+) - ln f(0.95-), with a stock-cluster bootstrap (499 draws) for its standard error.
(e) *Samples:* main 2 Jan 2015 to 30 Sep 2025. Also: excluding days on which the stock's MWPL changed (utilisation then
jumps through the denominator); the two pre-reform enforcement regimes; the pre-sample 2010 to 2014; after 1 Oct 2025
(descriptive, few observations).
(f) *Reading:* the model does not sign the test (holding back by arbitrageurs thins the density just below 0.95; a rush to
open positions before an expected ban does the opposite). A significant discontinuity in the main population means the RD
at 95% is not credible as a local randomisation and is reported as descriptive only. Supplementary (treatment side): the
mean daily change in utilisation by bins of omega_(d-1) between 0.80 and 0.95, against bins further below.
- 7 Nov 2026, density test (exploratory additions in `analysis/density_test.py`, after the C8 results were seen): the
  pre-specified CJM test finds no discontinuity (log ratio -0.05, p = 0.86) while the pre-specified binned check gives +0.31
  (CI +0.08 to +0.62). Added: (1) stock-cluster bootstrap of the CJM log ratio at the main bandwidths: se 0.29, interval
  -0.62 to +0.54; (2) binned estimate by bandwidth: +0.12 (0.02), +0.19 (0.03), +0.29 (0.04), +0.31 (0.05), +0.34 (0.075),
  +0.30 (0.10) — rising with h, consistent with boundary bias from linear fits to a convex falling density.

### 11.6 Clarifications for the regression discontinuity at 95% (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Known beforehand: the density test (C8) finds no discontinuity; the level-effect study (C7) found a basis dip on the day
utilisation crosses 95% (day t-1 here), which motivates the placebo outcomes in (e).
**C9. RD.** (a) *Units:* stock-days t, 2 Jan 2015 to 30 Sep 2025, with the stock not in a ban on t-1 (at risk of entry).
Running variable omega_(t-1) (utilisation in the file of day t-1, gross OI); cutoff 0.95; above it the stock is in the
ban on t (sharp in design; the share actually in a ban on each side is reported, and a fuzzy RD with Ban_t as treatment is
reported alongside).
(b) *Estimator:* `rdrobust` 2.1.1 (Calonico, Cattaneo and Titiunik): local linear, triangular kernel, MSE-optimal bandwidth
(common on both sides), conventional estimate with robust bias-corrected confidence interval and p-value, standard errors
clustered by stock.
(c) *Main outcome:* the winsorised basis level m_t of the C1 analysis sample (bp). Secondary basis outcomes: Delta m_t
(same contract), close-based basis, relative implied repo.
(d) *Mechanism outcomes (sample of H8, expiry days excluded):* log(1 + futures contracts, near + next), R = (Delta OI + V)/V,
log(1 + cash shares traded), delivery share.
(e) *Validity checks:* pre-determined placebo outcomes m_(t-2) and log futures contracts on t-2; m_(t-1) is also reported
but it is the crossing day itself, so it may move with the same pressure that pushes utilisation over 95%. Selection: the share
of at-risk stock-days with a valid basis on t (>= 5 contracts) is itself estimated as an RD outcome, because bans thin
futures trading and the basis sample could be selected at the cutoff.
(f) *Robustness:* half and double the MSE-optimal bandwidth; local quadratic; donut excluding |omega - 0.95| < 0.005;
excluding days with an MWPL change on t-1; the two enforcement regimes; placebo cutoffs 0.85 and 0.90 (stocks below 0.95
only) and 1.00 (above 0.95 only). After 1 Oct 2025 (FutEq utilisation): descriptive.
(g) *Reading:* supporting evidence only (PAP §6). The model predicts the reduce-only effects at the cutoff (futures
volume falls; R near 0 under intraday enforcement; basis level sign set by composition, mostly new exposure, so negative
on average per C7); anticipation is continuous through 0.95 and does not create a jump.
- 7 Nov 2026, level effect, build-up split (exploratory, `analysis/level_effect_buildup.py`, added after the C7 and C9
  results were seen; motivated by the RD finding that the basis is already low on the crossing day, and by the fact that
  C cannot tell new longs from new shorts): events classified by OI change and cash-price change over days -5..-1. In-ban
  D: long build-up -7.9 (se 2.7, n 453), short build-up -5.5 (2.2, n 406), difference +2.4 (3.5); short covering and long
  unwinding +8.4 each (n 9 and 21; imprecise). The crossing-day dip is concentrated in long build-up events (D at k = -2:
  +8.2 vs -0.3). Same-day controls: long -5.4, short minus long +3.3 (4.3).

### 11.7 Clarifications for the hysteresis comparison (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Known beforehand: H8 already compared trading outcomes in the same utilisation zone (Ban coefficient on log futures
contracts -2.00 with stock-by-bin and date fixed effects).
**C10. Hysteresis.** (a) *Sample:* C1 analysis sample, 2 Jan 2015 to 30 Sep 2025, stock-days with omega_(t-1) in
[0.80, 0.95). In-ban stock-days in this zone are days of a spell after utilisation fell back below 95% but not yet to 80%.
(b) *Main specification:* m_t = b*Ban_t + g1*omega_(t-1) + g2*(omega_(t-1) - omega_(t-2)) + sum_{l=1..5} r_l*m_(t-l)
+ stock FE + date FE + e; m_(t-l) = winsorised chosen-contract basis levels on the previous five trading days (all must be
in the analysis sample); SEs two-way clustered (stock, date). Units bp.
(c) *Test statistic (secondary, unadjusted):* two-sided p for b = 0 (the plan states "in a ban vs not" without a sign). The
model's reading (Lemma: for the same pressure and inventory the basis in a ban is at least as high; in this zone open
interest is falling, i.e. closing pressure) leans to b > 0; the one-sided p for b > 0 is also reported.
(d) *Secondary outcomes, same specification:* Delta m_t (same contract); close-based basis; relative implied repo;
log(1 + futures contracts), R and delivery share (expiry days excluded) for comparison with H8.
(e) *Robustness:* utilisation as bin dummies ([0.80, 0.85), [0.85, 0.90), [0.90, 0.95)) instead of linear; without the
lagged basis; adding the maximum of omega over t-10..t-1 (recent path); excluding imputed ban days; the two enforcement
regimes; the in-ban days split into before and after an expiry within the spell (PostExp, as in C2 c). After 1 Oct 2025:
descriptive.

### 11.8 Clarifications for H9 (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Known beforehand (treatment side): on 1 Oct 2025 all 208 F&O stocks' MWPL fell, ln(new/old) from -0.69 to -0.24 (median
-0.32); FutEq OI exists in our files only from 1 Oct 2025 (ratio FutEq/gross OI on 1 Oct: median 0.73); later quarterly
MWPL resets on 1 Jan, 1 Apr and 1 Jul 2026 (about 155 stocks each). Known outcome-side results: level effect, RD,
hysteresis (C7, C9, C10).
**C11. H9.** Part A, anticipation (2 Jan 2015 to 30 Sep 2025, C1 sample, non-ban days only):
(a) Stock-specific tail thresholds from each stock's non-ban days with omega_(t-1) < 0.60: q20_i, q50_i, q80_i of the
winsorised basis (stocks with fewer than 100 such days dropped). Outcomes: U_it = 1{m_t > q80_i} (upper exceedance),
L_it = 1{m_t < q20_i}, and the level m_t - q50_i (bp).
(b) Specification: outcome on omega_(t-1) bin dummies [0.60, 0.65), ..., [0.90, 0.95) (reference: omega_(t-1) < 0.60) +
stock FE + date FE; SE two-way clustered (stock, date). Also reported: the raw 20th/50th/80th percentiles of m - q50_i by
bin (descriptive).
(c) *Test statistic A (secondary, unadjusted):* one-sided p that the slope of U on omega_(t-1), estimated on
omega_(t-1) in [0.60, 0.95) with stock and date FE, is > 0. Smoothness: the bin coefficients are reported in order; a
"jump only at 95% with no gradient" pattern contradicts. Caveat stated in advance: high utilisation also marks demand
pressure, so the gradient is anticipation plus pressure; it is not a clean anticipation estimate.
Part B, the 1 Oct 2025 reform:
(d) Stocks in F&O on both 30 Sep and 1 Oct 2025. Intensity I_i = -ln(MWPL_new / MWPL_old) (positive; larger = bigger cut,
pre-determined by pre-reform free float and deliveries). Secondary intensity: predicted change in log utilisation
P_i = ln(FutEq OI / gross OI on 1 Oct 2025) + I_i (uses the 1 Oct composition because FutEq OI is not in our files before).
(e) Window 1 Jul 2025 to 31 Dec 2025 (before the 1 Jan 2026 reset). y_it = b * Post_t * I_i + stock FE + date FE; SE
two-way clustered; outcomes U_it and L_it (thresholds as in a, from each stock's pre-reform data), m_t - q50_i, and, as
first stage and treatment-side checks, utilisation omega_t and the ban indicator. Ban days included in the main
estimate (the reform acts on the whole regime, Prop. "MWPL not an instrument"); non-ban days only as robustness.
(f) *Prediction:* larger cuts raise utilisation and bans and raise U (a higher upper edge through anticipation and more
reduce-only days). *Test statistic B (secondary):* one-sided p that b > 0 for U.
(g) Robustness: P_i instead of I_i; window extended to 31 Mar 2026 (intensity fixed at 1 Oct); monthly event study
(July to December, September = reference); non-ban days only.
(h) Quarterly resets (PAP §4 c), also reported: stacked design over the resets of 1 Jan, 1 Apr and 1 Jul 2026, intensity
-ln(MWPL after / MWPL before), window 30 trading days before and after, stack-by-stock and stack-by-date FE. 1 Apr 2026 is
also the STT increase (common to all stocks, absorbed by date FE, but interactions cannot be excluded).

### 11.9 Clarifications for H2 (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Known beforehand (counts only): 8,586 announcement events of F&O stocks (event outcomes of C6 e and k), 179 with day 0 on a
ban day (55 bad news, 58 good news by the EAR tercile rule). H6 found stronger bad-news drift after F&O entry.
**C12. H2.** (a) *Events:* results announcements (C6 e, k: price >= Rs 5, duplicates removed) of stocks in the F&O segment
on day 0, 2015 to 2026. Ban0 = stock on the ban list on day 0. Bad/Good = bottom/top EAR tercile within the calendar
quarter (C6 e); middle tercile is the reference.
(b) *Drift:* BHAR_w[+2,+64] (winsorised, C6 k) = a + b1 Bad + b2 Good + b3 Ban0 + b4 Ban0*Bad + b5 Ban0*Good + quarter FE;
SE two-way clustered (stock, event date). *Prediction:* b4 < 0 (more negative drift after bad news in a ban); b5 about 0.
*Test statistic (secondary, unadjusted):* one-sided p that b4 < 0. Also reported: b4 - b5.
(c) *Pre-announcement basis:* pre_m = mean over days -5..-1 of (m_t - q50_i) in bp (C1 sample, winsorised; q50_i = the
stock's median on non-ban days with omega < 0.60, as C11 a; at least 3 valid days). BanPre = stock in a ban on day -1.
pre_m = c0 + c1 Bad + c2 Good + c3 BanPre + c4 BanPre*Bad + c5 BanPre*Good + quarter FE. *Prediction:* outside bans the
basis is lower before bad news than before good news (c1 - c2 < 0; the pattern reported by Saurav, Srivastava and
Agarwalla 2026); in a ban this disappears (c4 - c5 > 0). One-sided p-values reported for both.
(d) *Robustness:* stock FE added; non-ban comparison events restricted to omega_(t-1) >= 0.80 on day 0; ban defined as any
ban day in days 0..+5; EAR from days 0..+1 only is not recomputed (C6 definition kept); unwinsorised BHAR; pre-reform only.
(e) *Also reported (cross-section, association only):* bad-news drift in cash-only stocks versus F&O stocks, all events
2015 to 2026: BHAR_w on Bad, Good, NonFnO and their interactions, quarter FE and log market-cap decile FE (the H6 design
gives the causal version through entry and exit).

### 11.10 Clarifications for H1 (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
SLB data: NSE's daily SLBS bhavcopies (`SLBM_BC_DDMMYYYY.DAT`, 2015 to 2026) were found and are being downloaded
(`data_pipeline/download_slb.py`); only a few dozen stocks trade in SLB on a typical day, so the SLB input is activity-based.
**C13. H1.** (a) *Unit:* F&O stock x calendar quarter. Main period: outcomes 2015 Q2 to 2025 Q3 (frictions from the previous
quarter, 2015 Q1 to 2025 Q2; utilisation is gross-OI based throughout); robustness to 2026 Q3.
(b) *Outcomes in quarter q* (C1 sample, winsorised m, non-ban days only, at least 30 days): band width W = q80 - q20 of m
(bp); mispricing size A = mean |m| (bp); persistence rho = OLS slope of m_t on the same contract's m_(t-1) (at least 30 pairs).
(c) *Frictions in quarter q-1* (all from data that do not involve the basis or the ban): (1) Corwin-Schultz (2012) spread
from daily cash high and low prices (EQ series; two-day estimator with the overnight-gap adjustment; negative two-day
estimates set to 0; quarterly mean); (2) Amihud illiquidity = mean of |return| / traded value in Rs crore (log); (3)
idiosyncratic volatility = standard deviation of residuals from daily stock returns on the Nifty 50 return (at least 40
days); (4) mean utilisation omega on non-ban days (higher = less headroom); (5) SLB scarcity = 1 - share of trading days with
any SLB trade in the stock. Annualised SLB fee (fee / cash close x 365 / days to SLB expiry, median over traded days) is
reported but not in the index (missing for most stock-quarters).
(d) *Index:* first principal component of the five frictions, each standardised within quarter; sign chosen so that the
sum of loadings is positive; loadings reported.
(e) *Specification:* outcome_iq = beta * Index_i,q-1 + quarter FE; SE two-way clustered (stock, quarter). *Prediction:*
beta > 0 for W, A and rho. *Test statistic (secondary, unadjusted):* one-sided p that beta > 0 for W.
(f) *Also reported:* all five frictions jointly (standardised); stock FE added (within-stock variation); outcomes on all
days including ban days; period to 2026 Q3; index without the SLB input.
(g) Caveat stated in advance: frictions are correlated with size and liquidity, so beta is an association, not a causal
effect; this is H1's role in the plan.

### 11.11 Clarifications for H4 (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Data collected (treatment side): AMFI monthly reports, arbitrage-fund category, April 2018 to September 2026
(`data_pipeline/download_amfi_monthly.py` -> `data/processed/amfi_arbitrage_monthly.csv`; net inflow, net AUM; average AUM
from April 2019). Checked against two published figures (April 2023 and October 2024 AUM match exactly). Known outcome
results: H3 (level shifts around STT dates).
**C14. H4.** (a) *Monthly outcome:* the 80th percentile of the winsorised basis across all stock-days of the month in the C1
sample on non-ban days (bp); also the 90th, 50th and 20th percentiles and q80 - q20.
(b) *Capital measure:* flow_t = net inflow in month t / net AUM at the end of month t-1.
(c) *Main specification:* q80_t = a + b * flow_(t-1) + c1 * 1{t >= Apr 2023} + c2 * 1{t >= Oct 2024} + c3 * 1{t >= Apr 2026}
+ e_t (step dummies for the debt-fund tax change and the three STT increases; the April 2023 tax change and STT step share
one dummy), May 2018 to September 2026; Newey-West standard errors with 6 lags.
*Prediction:* b < 0 (inflows of arbitrage capital lower the upper part of the basis distribution). *Test statistic
(secondary, unadjusted):* one-sided p that b < 0.
(d) *Caveat stated in advance:* arbitrage-fund returns rise with the basis, so return-chasing flows create a positive
association that biases b upward (against the prediction); contemporaneous flows are more exposed to this than lagged ones.
(e) *Also reported:* contemporaneous flow_t; change in log AUM; log AUM with a linear trend; the other quantiles and the
width; first differences (Delta q80 on flow_(t-1)); excluding March to May 2020 (COVID redemptions and MWPL halving);
sub-periods before and from April 2023; adding the monthly change in the 3-month interbank rate.

### 11.12 Clarifications for H5 (PAP §6), fixed on 7 Nov 2026 BEFORE it was run
Known beforehand: H2(e) found larger drift for cash-only stocks after both good and bad news; H6 found faster price
adjustment after F&O entry. No anomaly portfolio had been formed.
**C15. H5.** (a) *Universe and timing:* NSE EQ/BE/BZ stocks with an adjusted return and a market cap
(`returns_daily`, `mcap_daily`), month-end price >= Rs 5; signals at the end of month t, holding month t+1; portfolio
months February 2016 to October 2026 (month-end October 2026 is the last holding month with data to 27 Oct).
(b) *Constraint groups (each month-end):* G1 = in the F&O segment (short-selling eligible, stock futures); G2 = cash-only
with at least one SLB trade in the previous three months; G3 = cash-only without SLB trades (most constrained). Alternative
grouping (robustness): terciles of idiosyncratic volatility (arbitrage risk, as in Stambaugh, Yu and Yuan 2015).
(c) *Anomalies (month t):* momentum (return over months t-11 to t-1, skipping t; low = overpriced); short-term reversal
(return in month t; high = overpriced); MAX (largest daily return in month t; high = overpriced); idiosyncratic volatility
(residual sd of daily returns on the Nifty 50 return; high = overpriced, the US sign; India's IVOL premium is positive per
Sehgal et al. 2024, so H5 is two-sided for IVOL); Amihud illiquidity (liquid = lower expected return, treated as the
"short" side); turnover (value traded / market cap; high = overpriced). Composite mispricing score = average percentile
rank (0 to 1) across the available anomalies, oriented so that high = overpriced (at least 4 of 6 available).
(d) *Portfolios:* within each constraint group and month, terciles of the composite score; value-weighted (previous
month-end market cap) returns in month t+1. Leg returns are measured against the group's value-weighted return that month:
short leg = most-overpriced tercile minus group return; long leg = most-underpriced tercile minus group return.
(e) *Prediction (Miller):* the short leg is more negative where shorting is constrained (G3 < G1), while the long leg
does not differ. *Test statistic (secondary, unadjusted):* one-sided p that mean[short leg G3 - short leg G1] < 0 over
months, Newey-West (6 lags). Also: long-leg difference (expected about 0; two-sided p), long-short spreads by group.
(f) *Also reported:* G2 vs G1; equal-weighted; each anomaly separately (tercile sorts, predicted-high minus predicted-low,
legs as above); IVOL-tercile grouping; excluding stocks below the cross-sectional median market cap; pre-reform
(to September 2025) only.
(g) Caveats stated in advance: G1 stocks are much larger than G2/G3; within-group sorting and benchmarking against the
group return remove the level difference but not differences in the cross-sectional dispersion of returns; delisting
returns are not available.

### 11.13 Band-estimation chapter (master plan §5), specifications fixed on 7 Nov 2026 BEFORE estimation
Not a confirmatory test of the plan (the confirmatory band test is H3, already reported); it estimates and describes the
no-arbitrage band. Known beforehand: all primary and secondary results, including H3 (upper quantile rose around the
2024/2026 STT dates, mostly a common level shift), H7 (reversion by percentile regime), H9 A (upper tail widens with
utilisation), H4 (weak capital effect) and the simulation lesson that fixed thresholds estimate average edges (§5b).
**C16. Band estimation.** (a) *Data:* C1 sample, non-ban days, 2 Jan 2015 to 27 Oct 2026; x_(t-1) = m_(t-1) - mu_i (mu_i =
the stock's median on non-ban days, winsorised levels, as C2 a), Delta m_t same contract (bp).
(b) *Pooled 3-regime threshold model:* Delta m_t = a_r + rho_r x_(t-1) + e in regimes x < gL, gL <= x <= gU, x > gU; grid
over the 5th to 95th percentiles of x (step 1 percentile), at least 10% of observations in each outer regime and 20% in the
middle. Linearity test: sup-F against the linear model, p-value from a wild bootstrap clustered by date (Rademacher
weights, 199 draws). Threshold uncertainty: stock-cluster bootstrap (199 draws). Reported: thresholds, regime slopes,
half-lives, shares.
(c) *By period and state (same estimator):* calendar years; STT periods (to 31 Mar 2023; 3 Apr 2023 to 30 Sep 2024;
1 Oct 2024 to 31 Mar 2026; from 1 Apr 2026); ban-enforcement eras are not used (non-ban days only); days to expiry
(terciles); lagged utilisation (terciles of omega_(t-1)); arbitrage-capital regimes (terciles of monthly arbitrage-fund
net assets relative to total F&O stock market activity are NOT used: simply terciles of log net assets over April 2018 to
September 2026, which mostly orders time, so it is reported as descriptive only).
(d) *Smooth transition:* exponential STAR, Delta m_t = a + [rho_1 + rho_2 (1 - exp(-gamma (x_(t-1) - c)^2 / s_x^2))] x_(t-1) + e
(s_x = sd of x), and logistic STAR with transition variable x_(t-1) (asymmetric edges); estimated by profiling (grid over
gamma and c, OLS given them); compared with the threshold and linear models by SSR and BIC. Linearity check against STAR:
auxiliary regression of Delta m on x, x^2, x^3 (stock and date FE, two-way clustered); joint test of x^2 and x^3.
(e) *Observed transition variables (state-dependent adjustment):* Delta m_t = a + [rho_0 + rho_1 G(s; gamma, c)] x_(t-1) + e,
logistic G, s in {omega_(t-1); trading days to expiry; log arbitrage-fund net assets (monthly, from April 2018)}; profile
estimation over (gamma, c); rho's with two-way clustered SE at the chosen (gamma, c).
(f) *Per-stock models:* the threshold model per stock on non-ban days (at least 500 observations); distribution of gL,
gU and gU - gL; cross-sectional relation of the band width to the H1 friction index (stock means), reported as an
association.
(g) *Cost band:* a bottom-up round-trip cost for an overnight cash-and-carry position in each STT period (STT on cash
delivery and on futures, stamp duty, exchange and clearing charges, GST on charges; brokerage at an institutional rate),
with every component sourced; compared descriptively with the estimated edges.
(h) Units: bp; all estimates are descriptive; inference is reported for the linearity tests and threshold intervals only.
- 7 Nov 2026, band chapter (exploratory, `analysis/band_exploratory.py`, after the C16 estimates were seen): (1) with
  full-sample demeaning the 2026 / post-April-2026 upper threshold collapses (about -2 bp; 53-58% of observations in the
  upper regime) because of the level shift found in H3; re-estimated with demeaning within each STT period: lower/upper
  thresholds -39.1/+23.8, -30.9/+18.9, -31.5/+23.1, -31.5/+28.9; slope above the upper edge -0.77, -0.55, -0.20, -0.15.
  (2) Measurement noise: instrumenting x_(t-1) with x_(t-2) shrinks the slopes (linear -0.26 to -0.14; middle regime -0.49
  to -0.19; upper -0.52 to -0.14; lower -0.17 to -0.12), so much of the daily reversion is noise and the upper/lower
  asymmetry in reversion speed is not robust.

### 11.14 Constraint index as a stand-alone deliverable (project-document goal; master plan §4), fixed on 7 Nov 2026 BEFORE it was built
Known beforehand: H1 (F&O-only friction index; SLB activity entered with the wrong sign), H5 (constraint groups), H6
(price delay falls after F&O entry), H2(e) (cash-only stocks drift more after good and bad news).
**C17. Constraint index.** (a) *Universe:* all NSE EQ/BE/BZ stocks with a quarter-end price >= Rs 5 and at least 40 trading
days in the quarter, 2015 Q1 to 2026 Q3. (b) *Components per stock-quarter* (frictions only; no basis, no ban): (1) no
short channel = 1 if the stock is not in the F&O segment at quarter end; (2) SLB scarcity = 1 - share of trading days
with any SLB trade; (3) Corwin-Schultz spread (as C13 c); (4) log Amihud illiquidity; (5) idiosyncratic volatility
(daily, on the Nifty 50). (c) *Index:* first principal component of the components standardised within quarter, sign
such that the loadings sum to a positive number; loadings for each year reported for stability; the index is published
with its components (`data/processed/constraint_index_q.csv.gz`). The F&O-only index with utilisation (C13) is kept as a
separate position-limit index. (d) *Validation (associations, frictions measured before outcomes):* (i) annual price delay
D1 (calendar year y) on the mean index over the four quarters of year y-1, year FE, SE clustered by stock; prediction
positive; (ii) absolute post-announcement drift |BHAR_w[+2,+64]| on the index of the previous quarter, quarter FE, SE
two-way (stock, event date); prediction positive; and bad-news BHAR on the index (prediction negative); (iii) F&O subset:
quarterly basis band width on the index (as H1); (iv) persistence: quarter-to-quarter rank correlation of the index.
- 7 Nov 2026, H7 with instrumental variables (exploratory, `analysis/h7_iv.py`, motivated by the band chapter's noise
  check): regimes by x_(t-2) (stock 20/80 percentiles), x_(t-1) terms instrumented by x_(t-2) terms, stock and date FE,
  two-way clustered SE (456,344 obs, 8,027 ban days). 2SLS: delta_up -0.190 (se 0.077), delta_lo +0.088 (0.015),
  delta_up - delta_lo -0.279 (0.079); OLS on the same sample -0.085 / +0.102. The opposite-sign rejection of H7 is not a
  measurement-noise artefact. By era (2SLS): end-of-day -0.153 / +0.090; intraday -0.381 (0.236) / +0.012.

### 11.15 Remaining master-plan items, specifications fixed on 8 Nov 2026 BEFORE they were run
Known beforehand: all results above. These items come from the master plan (§6.4 COVID halving, §8 policy, §9 placebos,
§0 peak margins); none is in the frozen primary or secondary lists, so all are reported as exploratory/descriptive.
**C18. Spurious bans (treatment side only).** (a) *Pre-reform entries* (2015 to Sep 2025, spells as in C7 a without the
clean-pre-period filter): decompose the change in log utilisation over the crossing day (file of day t0-1 against
t0-2) into the change in log gross OI and minus the change in log MWPL. An entry is *denominator-driven* if the MWPL fell
on that day and OI_(t0-1) / MWPL_(t0-2) <= 0.95 (it would not have crossed at the old limit); reported with the share of
entries whose MWPL fell within the five days before. (b) *Post-reform counterfactual bans* (1 Oct 2025 to 27 Oct 2026):
a ban state machine (enter the next day when end-of-day utilisation > 0.95; leave after the day utilisation <= 0.80),
validated by applying it to actual FutEq utilisation and comparing with the official ban list; then applied to (i) gross
OI / new MWPL (old measure, new limit), (ii) FutEq OI / old-formula limit, (iii) gross OI / old-formula limit (the old
rule). Old-formula limit = new MWPL x stock-specific ratio MWPL(30 Sep 2025) / MWPL(1 Oct 2025), which keeps the new
limit's corporate-action and quarterly updates and freezes the old-to-new ratio (approximation stated). Outcomes: ban
stock-days, spells, stocks. Same machine on pre-reform gross utilisation as a validation of the machine.
**C19. Placebos.** (a) *Fake ban dates:* every actual pre-reform spell shifted 60 trading days later for the same stock
(same length), kept only if no actual ban day of that stock falls within the fake spell or 5 days either side; run the H7
specification (C2, pct thresholds) with the fake ban indicator replacing the real one (real ban days dropped), and the
level-effect design (C7) with fake entries. Prediction: no effect. (b) *Index-only reforms* (SEBI 2024/132; single-stock
derivatives not targeted): the H3 statistic (C4: change in stock q80, 40 trading days each side) at 20 Nov 2024, 3 Feb 2025
(first trading day on or after 1 Feb) and 1 Apr 2025, ranked against the 30 H3 placebo dates. Prediction: not unusual.
Windows overlapping the STT event of 1 Oct 2024 are noted. (c) *Peak-margin phase-in* (25% 1 Dec 2020, 50% 1 Mar 2021,
75% 1 Jun 2021, 100% 1 Sep 2021): the same statistic at each date (descriptive; the model gives no sharp prediction
because margin rules mainly bind intraday leverage). (d) The master plan's "non-F&O stocks for ban effects" is covered
by design: the basis exists only for F&O stocks and date fixed effects already use non-banned stocks as controls.
**C20. COVID MWPL halving and restoration.** (a) *Restoration (main):* treated = stocks whose MWPL doubled in the file of
26 Nov 2020 (effective 27 Nov); controls = all other F&O stocks; window 40 trading days before and after; DiD
y = b * Post x Treated + stock FE + date FE, SE two-way clustered; outcomes: utilisation omega_t (first stage), ban
indicator, log(1 + futures contracts), upper/lower exceedance U, L and level m - q50 (C11 a thresholds). Prediction (model
anticipation result): restoring the limit lowers utilisation and bans and lowers U. (b) *Halving:* treated = stocks halved
in the files of 20 to 27 Mar 2020; same outcomes and window around 23 Mar 2020; reported with the caveat that the halving
coincided with the March 2020 crash and selected stocks on volatility and utilisation. (c) Robustness for (a): controls
restricted to stocks with utilisation above 0.20 in the pre-window; window 20 days.
- 8 Nov 2026, results of §11.15 (C18-C20; exploratory by design): (C18) pre-reform entries are OI-driven: the MWPL fell on
  the crossing day for 8 of 1,744 entries and only 7 (0.4%) would not have crossed at the old limit; mean change in log
  utilisation on the crossing day 0.194, of which 0.192 from OI. The ban state machine reproduces the official lists
  (99.99% pre-reform, 100% post-reform). Post-reform counterfactuals (1 Oct 2025 to 27 Oct 2026): actual 412 ban
  stock-days / 45 spells / 11 stocks; old rule (gross OI, old-formula limit) 1,505 / 112 / 36; gross OI with the new limit
  6,256 / 296 / 85; FutEq with the old limit 1 / 1 / 1. (C19) fake bans: H7 delta_up +0.037 (0.047), delta_lo -0.028
  (0.038); level effect mean +1.0, no gradient; index-only reform dates and peak-margin dates within the placebo range
  (peak margin 50% +9.6, 75% -9.9: no consistent sign). (C20) restoration (70 stocks, 27 Nov 2020): utilisation -0.214
  (0.019), in a ban -0.046 (0.014), log futures +0.243 (0.079; pre-trend +0.214 in the fake-date check), U -0.068 (0.032),
  level -2.8 (3.1); fake date 20 days earlier: utilisation, ban, U null. Halving (60 stocks, crash period): utilisation
  +0.092, ban 0.000, futures -0.184, U +0.026, level -15.7 (7.7).
