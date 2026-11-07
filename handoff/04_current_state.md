# 04. Current state (as of 7 November 2026; level-effect secondary test run)

Resume card with first actions: `16_resume_here.md`. Results for outside readers: `docs/14_results.md`.

## 4.1 Status board

| Component | State | Where |
|---|---|---|
| Theory | Complete, verified (ALL PASS) | `BSP_Model_C_Constrained_Arbitrage_India.pdf`, `models_src/modelC/` |
| Pre-analysis plan | **Frozen**: `pap-v1` at commit 85dac3a, on GitHub (created by the user, 5 Nov 2026) | `plan/pre_analysis_plan_v1.md` |
| Master plan | v2 (goals of the project document; order of work) | `plan/BSP_Research_Plan_v2.md` |
| Data: treatment side | Built, audited | `data/processed/mwpl_oi_panel.csv.gz`, `ban_days`, `ban_spells`, `fno_membership`, `fno_events` |
| Data: outcome side | Basis built, audited; announcements rebuilt | `basis_panel.csv.gz` (git-ignored), `announcements.csv.gz` |
| Data: added 5 Nov | adjusted daily returns; AMFI half-yearly market caps; daily market caps (back-cast before Jul 2017) | `data_pipeline/build_returns.py`, `build_amfi_mcap.py`, `build_mcap.py` |
| Data: not yet collected | AMFI arbitrage-fund AUM (H4); XBRL EPS (SUE, secondary); SLB (H1); index dividends | see 05 |
| Estimators | 3-regime SETAR (`analysis/setar.py`), tested on simulated data | `analysis/` |
| Main tests | **All four primary tests run + Holm** (5 Nov 2026) | `analysis/output/`, `docs/14_results.md`; summary §4.7 and §4.9 |
| Final-form docs | Complete for the current state, incl. results page | `docs/` (README + 01 to 14) |
| Guide | Has the project document and the Oct 2026 progress report; approved continuing | |
| Library papers | Not obtained: Saurav et al. 2026 (most useful), Gagnon 2018, Brennan and Schwartz 1990 | user can fetch via IITB library |

## 4.2 The blind rule

Until `pap-v1`, no outcome (basis, returns, drift, delay) was related to any treatment (ban, utilisation, MWPL changes, STT
dates, F&O entry/exit, the tax change). This was respected throughout. From the tag on, tests may be run **exactly as
specified**; deviations go in PAP §11. Treatment-side counts (e.g. 180 announcements on ban days) and outcome
distributions on their own were always allowed.

## 4.3 What changed in the 5 Nov audit (numbers differ from the sent report)

| Quantity | In the report sent to the guide | Now |
|---|---|---|
| Ban spells 2015 to 2026 | 1,789 | 1,788 |
| Ban stock-days | 9,414 | 9,416 |
| Entry/exit rule checks | 99.2% / 99.5% | 99.4% / 99.7% |
| Non-ban stock-days with utilisation in (0.90, 0.95] pre-reform | 2,441 | 2,439 |
| Results announcements for F&O stocks | 7,910 (188 on ban days) | 8,594 (180 on ban days) |
| Share released after close | 63% | 62% (F&O events with known time) |
| Clean near-month basis sample | 499,682 | 503,170 (October 2026 now included via carried-forward rate) |

The sent PDF was intentionally **not** rebuilt (it is the record of what she received). The source table
`reports/tables/ban_by_year.tex` has been regenerated, so rebuilding the report would change those numbers. When results
are presented to the guide, mention briefly that the results-date construction was corrected (in guide-facing language,
without "audit" jargon: e.g. "I now date results from the exchange's first dissemination time").

## 4.4 Git state

- Branch `claude/compassionate-rubin-s9gny2` is pushed and up to date (key commits: 85dac3a = frozen plan; c6b1701 = §11
  clarifications before tests; f33bb9e H8; 870e295 H7; a44836c H3; dbdfcde/e9ba556 H6 clarifications; c48e2e9 H6 + Holm;
  d72bdaa end-of-session save 5 Nov).
- `main` = 65ef0e3 (everything up to 28 Oct 2026). Work after that reaches `main` only through a new PR, which only the
  user can request.
- Tag `pap-v1` → 85dac3a is on GitHub (created by the user with GitHub Desktop, 5 Nov 2026; cloud sessions cannot push
  tags). Never move it: the frozen plan is the version at 85dac3a. Since the tag the plan file has only gained §11 text.

## 4.5 Container state

- Git-ignored, container-only files (full rebuild list in `16_resume_here.md` §16.2): `data/raw/` (about 1.4 GB),
  `basis_panel.csv.gz`, `returns_daily.csv.gz`, `mcap_daily.csv.gz`, `data/processed/cache/*.pkl`. On 7 Nov 2026 the same
  container was still in place (all present; pyfixest installed).
- Raw folders: `combineoi/`, `secban/`, `prices/{fut,cash,optsum,deliv}/`, `corpactions/` (156 monthly JSON),
  `results/` (Quarterly/Annual 156 each, Integrated 24), `resultupdates/` (1,173 four-day JSON), `boardmeetings/`
  (312 half-month JSON), `amfi_mcap/` (18 PDFs), `rates/` (2 FRED CSV), `indices/nifty50_daily.csv`, `download_log.tsv`,
  `prices/price_download_log.tsv`.

## 4.6 Documents and who they are for

| Document | Audience | State |
|---|---|---|
| `BSP_Project_Document.docx/.pdf` | Guide (seen) | September 2026; contains known errors (short-selling line, 30x volume leg, "relaxations", timeline without theory stage); fixing it needs the user's go-ahead |
| `BSP_Progress_Report_Oct2026.pdf` | Guide (seen, liked) | Final as sent |
| `BSP_Model_C_Constrained_Arbitrage_India.pdf` | Guide-safe (also the report's appendix) | Current theory |
| `BSP_Literature_Review.pdf` | Internal (not sent) | Has known errors listed in `memory/04` (SYY is not Fama-MacBeth, PEAD definitions, Roy-Chakraborty direction, etc.) |
| Models A and B PDFs, 28 Sep progress note | Internal (never sent) | Superseded; kept |
| `docs/` | Outside readers, final repo | Current |
| `handoff/`, `memory/`, `plan/` | Internal continuity | Current |

## 4.7 Primary results so far (5 Nov 2026; pre-specified, after the §11 C1 to C5 clarifications)

| Test | Pre-specified statistic | Result | Notes |
|---|---|---|---|
| H8 | one-sided p, Ban coefficient on log futures contracts < 0 | b = -2.00 (se 0.11), p ~ 0: **supported** | cash volume +7.3%, delivery share +4.1 pp (as predicted). Identity (dOI+V)/V ~ 0 **fails** pooled (mean 0.42). Exploratory: break mid-March 2020 (before 0.86, after median 0.01) = intraday enforcement from 23 Mar 2020 (§4.8) |
| H7 | IU p = max(p(delta_up > 0), p(delta_up - delta_lo > 0)) | delta_up = -0.089 (t -2.4), delta_lo = +0.081 (t +2.7), p = 1: **rejected; opposite sign** | robust across pre-specified checks except close-based (delta_up ~ 0) and unwinsorised (delta_up +0.08, t 1.6). After an expiry in the spell, downward reversion much faster |
| H3 | one-sided p, mean change in stock q80, 2024+2026, stock-clustered | +6.96 bp (se 0.61), p = 1.8e-24; ordering 2026 > 2024 > 2023 holds: **supported by the pre-specified test** | pre-specified placebo: sd 7.4 bp across pseudo-events, 2024 rank 0.10, 2026 0.07: weak once common shocks are allowed for; shifts larger than the cost changes |
| H6 | Bonferroni of four components (§11.3 C6 h) | p = 5.2e-6: **supported through delay; drift contradicts** | see §4.9 |

(This table was written before the research of §4.8 and H6 of §4.9; the open questions it raised were then researched:
the March 2020 break is the intraday-enforcement change, the H7 reversal has exploratory diagnostics, and H3 is reported
with its placebo calibration.)

## 4.8 Research on the open questions (5 Nov 2026, user asked for it)
1. **H8 March 2020 break: resolved.** SEBI PR 18/2020 made violations in banned stocks be checked on peak intraday
   positions from 23 Mar 2020 (references/24); kept by PR 59/2020 (references/23); from 1 Oct 2025 end-of-day FutEq checks
   (references/19). The identity holds when enforcement is intraday (median R 0.011). See docs/14 §14.2.
2. **H7:** exploratory diagnostics (docs/14 §14.3): not noise; era-dependent; concentrated at spell starts; post-hoc reading
   = blocked new demand (P5) dominates at ban start.
3. **H3:** placebo-calibrated evidence weak (docs/14 §14.4): mostly a common level shift.
Full results page for outside readers: `docs/14_results.md`.

## 4.9 H6 and the primary family (5 Nov 2026)
| H6 component | Prediction | Estimate (se) | One-sided p |
|---|---|---|---|
| entry: price delay (CS) | < 0 | -0.109 (0.023); Sun-Abraham -0.063 (0.019) | 1.3e-6 |
| entry: bad-news BHAR (stacked) | > 0 | -0.040 (0.018) stronger drift | 0.99 |
| exit: price delay | > 0 | +0.053 (0.040) | 0.091 |
| exit: bad-news BHAR | < 0 | +0.014 (0.020) | 0.77 |
p_H6 = 5.2e-6 (Bonferroni of components). Holm: H8 7.4e-41, H3 5.5e-24, H6 1.0e-5 rejected; H7 not.
Interpretation notes: delay supports short-sale-access (or a liquidity/attention channel: F&O entry selects on growth);
drift contradicts. H3 strength overstated by stock-only clustering.

## 4.10 Secondary tests (7 Nov 2026 onward)
Level effect (PAP §11.4 C7; `analysis/level_effect.py`; docs/14 §14.7): 889 matched pre-reform ban entries. Basis falls
-6.3 bp in the first ban days vs matched controls and recovers by about day 7. Pre-specified split: C <= 0 (30 events)
+8.4 (se 10.9), C > 0 -6.8 (1.8), difference -15.2, p = 0.083 (n.s.: closing group tiny); median split -5.8, p = 0.025;
slope on C -4.8, p = 0.0014. Signs as Prop. 6 predicts. Fragile: same-day controls only, gradient n.s. (-2.1, se 1.8);
matching leaves treated 10 bp lower on day -1 and a dip on day -1. Exploratory: baseline k=-10..-2 level -11.3, slope p
0.007; gap-adjusted level -9.2, slope -3.5 (se 1.6). Post-reform 19 events, all C > 0, mean -2.8.
