# Pre-analysis plan — v1 (28 Oct 2026)

**Status.** Complete. To be git-tagged `pap-v1` once the user confirms (the progress report asks the guide whether she wants
to see the test plan first; if she asks for changes they are made before tagging). **Until the tag, no outcome is related to
any treatment.** After the tag, every change is logged in §11 with date and reason; results under the original specification
are always reported.
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
| Results announcements | NSE results API (to Mar 2025) + Integrated Filing (from Mar 2025 quarter) | 2014 – 2026 | ~4 events per stock-year |
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
  trading day.
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
- **H2:** bad-news drift on ban days vs non-ban days (188 announcements in bans → low power, stated in advance); pre-announcement
  basis (days −5…−1) in bans vs not.
- **H1:** friction index (bid–ask proxy, Amihud, IVOL, lagged headroom 1−ω, SLB availability if obtained) vs band width.
- **H4:** arbitrage-fund flows vs the upper quantile of the cross-sectional basis (monthly).
- **H5:** anomaly asymmetry by constraint terciles (double sorts).

## 7. Inference
Two-way clustered SEs (stock, date). Event studies with few clusters: wild-cluster bootstrap. Primary family {H7, H8, H3, H6}:
Holm correction at 5%. Outliers: main estimates winsorise m at 1/99% within year; robustness without.

## 8. Power notes (treatment-side counts, known before any outcome analysis)
Ban spells 2015–2026: 1,789 (44 after Oct 2025); ban stock-days 9,414; stocks ever banned 141; not-in-ban stock-days with
ω ∈ (0.90, 0.95]: 2,441 pre-reform / 139 post; F&O entries 233 / eligibility exits 158; F&O announcements 7,910 (188 on ban
days). Post-reform ban analyses and H2-in-bans are low-powered.

## 9. Falsifiers (from the model)
No upper/lower asymmetry in bans (H7); no change in futures activity in bans (H8); band unrelated to dated cost shocks (H3);
no effect of F&O entry/exit on delay or bad-news drift (H6).

## 10. Open items that do not change the specification
AMFI arbitrage-fund AUM series; XBRL EPS extraction for SUE; index dividends for the Nifty futures check; SLB data.

## 11. Deviations log
(empty)
