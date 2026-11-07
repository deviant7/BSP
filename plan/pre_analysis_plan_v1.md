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
