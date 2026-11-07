# 07. The test plan (frozen) and how to implement it faithfully

The authoritative text is `plan/pre_analysis_plan_v1.md` at commit **85dac3a** (tag `pap-v1`). Plain-language version:
`docs/09_empirical_design.md`. Earlier draft: `plan/archive/pre_analysis_plan_v0_draft_2026-10-28.md`.
This page summarises it and adds implementation notes that do not change the specification.

## 7.1 Structure of the plan

| Section | Content |
|---|---|
| Status | Frozen 5 Nov 2026; pre-tag revisions (a) to (d) from the audit |
| §1 Data | Sources, coverage, checks |
| §2 Samples | Basis sample (F&O stock-days, near month, switch at <= 3 trading days to expiry, >= 5 contracts); exclusions (dividend or corporate event in contract life; first 20 trading days after F&O entry; lot failures); pre-sample 2010 to 2014; cash universe EQ/BE/BZ |
| §3 Outcomes | O1 VWAP basis (secondary close-based); O2 relative implied repo (tau >= 7 days); O3 reversion Delta m on m_(t-1) by regime; O4 trading (contracts, Delta OI, Delta OI + volume, cash volume, delivery %); O5 drift BHAR[+2,+64] vs size-matched portfolio, surprise EAR[-1,+1] (SUE secondary), day 0 rule; O6 Hou-Moskowitz delay (weekly, 52-week windows), VR(5) |
| §4 Treatments | Ban list; omega on t-1 (gross OI before 1 Oct 2025, FutEq after); MWPL shocks (COVID halving; 1 Oct 2025 intensity ln(new/old) and predicted Delta utilisation; quarterly resets); STT dates; capital (tax change; AMFI); F&O entries (233 usable) and eligibility exits (158) |
| §5 Primary | H7, H8, H3, H6 with predictions and falsifiers |
| §5b | Lesson from estimators on simulated data (average edges, edge changes, state-dependent thresholds) |
| §6 Secondary | Level effect (stacked event study, near-miss controls omega in [0.85, 0.95) same week, matched on 5-day omega path and basis level, split by pre-ban composition); H9; RD (density test first); hysteresis; H2; H1; H4; H5 |
| §7 Inference | Two-way clustered SE (stock, date); wild-cluster bootstrap for few-cluster event studies; Holm on {H7, H8, H3, H6} at 5%; winsorise m at 1/99% within year (robustness without) |
| §8 Power | 1,788 spells (44 post-reform), 9,416 ban stock-days, 141 stocks, 2,439/139 near-threshold non-ban days, 233/158 events, 8,594 F&O announcements (180 on ban days) |
| §9 Falsifiers | No asymmetry (H7); no futures-activity change (H8); band unrelated to cost dates (H3); no entry/exit effect (H6) |
| §10 Open items not changing the specification | AMFI; XBRL EPS; index dividends; SLB |
| §11 Deviations log | Empty at tag time; now: 11.1 clarifications C1-C5 (before any test), 11.2 exploratory additions after results (H8 break and its resolution, H7 diagnostics, H3 calibration), 11.3 H6 clarifications C6 (a)-(k); 11.4-11.12 secondary-test clarifications C7-C15 (level effect, density, RD, hysteresis, H9, H2, H1, H4, H5), each committed before its run; 11.13 C16 band-estimation chapter and 11.14 C17 constraint index (specifications before estimation); §11.2 also logs the exploratory additions to the level effect (baseline, gap, build-up split) and the density test |

## 7.2 H7 equation (exact)

    Delta m_it = sum_r [beta_r + delta_r * Ban_it] * (m_i,t-1 - mu_i) * 1{regime r} + alpha_i + lambda_t + e_it

- regimes: upper if m_(i,t-1) > stock's 80th percentile of m on non-ban days; lower if < 20th; middle otherwise.
- Prediction delta_upper > 0, delta_lower <= 0; expiry-in-spell interaction: delta_lower closer to 0 after an expiry.
- Fails if delta_upper <= 0 or delta_upper = delta_lower.
- Robustness: per-stock TVECM thresholds (non-ban days), fixed +/-25 bp around median, state-dependent thresholds.

## 7.3 Implementation notes (choices the plan leaves open; log them in §11 BEFORE running) — items 1 to 9 were all settled in §11.1 and §11.3 on 5 Nov 2026

These are places where the text does not pin down a detail. Decide, write the choice into §11 with the date, then run.

1. Ban timing for H7: Ban_it refers to day t (the day the change Delta m_it happens). The regime uses m_(i,t-1).
   A day-t-1-in-ban alternative is a robustness.
2. Whether Ban includes imputed days (7 stock-days): main yes; robustness without.
3. Percentiles for regimes: computed over each stock's full-sample non-ban days (not rolling). Rolling is a robustness.
4. Pooled vs split at 1 Oct 2025: report pooled as main (as written) plus split.
5. H8 "similar omega": bins of width 0.05 on omega_(t-1) within stock; expiry days excluded.
6. H3 statistic: the change in the stock-level 80th percentile, averaged over stocks, per date; ordering test as a
   rank comparison of the three average changes (descriptive; three events cannot give a powerful test).
7. H6 "bad news": bottom tercile of EAR within each calendar quarter (state it); size matching depends on finding market
   capitalisation (see 05 step 2, H6).
8. Holm: one p-value per primary hypothesis (H7: delta_upper - delta_lower > 0 one-sided, together with delta_upper > 0;
   choose and state the single test statistic).
9. Two-way clustering with ~370 stocks and ~2,900 dates is fine; for event studies with few events use the wild bootstrap.

## 7.4 Reporting rules

- Report every pre-specified test, nulls included, with the original specification first.
- Label secondary tests "exploratory".
- Never re-specify after seeing results without logging it as a deviation and reporting both.
- In guide-facing text, describe the plan as "the test plan I fixed before running the tests"; no internal jargon.
