# 04. Current state (updated 9 November 2026: final thesis built; earlier sections below kept as written)

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
| Data: added 7 Nov | NSE SLB bhavcopies 2015-2026 (`slb_daily.csv.gz`); AMFI monthly arbitrage-fund series Apr 2018-Sep 2026 | `data_pipeline/download_slb.py`, `build_slb.py`, `download_amfi_monthly.py` |
| Data: not yet collected | XBRL EPS (SUE, optional); index dividends | see 05 |
| Estimators | 3-regime SETAR (`analysis/setar.py`), tested on simulated data | `analysis/` |
| Main tests | **All four primary tests run + Holm** (5 Nov 2026) | `analysis/output/`, `docs/14_results.md`; summary §4.7 and §4.9 |
| Secondary tests | **All done 7 Nov 2026** (level effect, density, RD, hysteresis, H9, H2, H1, H4, H5) | §4.10; `docs/14_results.md` §14.7 to §14.16 |
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
  d72bdaa end-of-session save 5 Nov). 7 Nov session: beb11b5 (context fixes) → ... → 0538cd7 (checkpoint) → 8609699
  (band §11.13) → 0f6537e (band chapter) → b109ec0 (H7 IV) → 52119d4 (constraint index) → 36f4edc (thesis draft) →
  4b854e4 (first-results report) → e2ac3e9/f40ef9b (memory save) and the end-of-session save after it. Each PAP §11 entry
  was committed in its own commit before the analysis it governs (e.g. 25bd744 C7, 3f7ffab C8, f96bca8 C9, 3e72a35 C10,
  8484f59 C11, 0a90154 C12, e88fefe C13, da352a5 C14, 328010d C15, 8609699 C16, d5e2ff0 C17).
- `main` = 65ef0e3 (everything up to 28 Oct 2026). Work after that reaches `main` only through a new PR, which only the
  user can request.
- Tag `pap-v1` → 85dac3a is on GitHub (created by the user with GitHub Desktop, 5 Nov 2026; cloud sessions cannot push
  tags). Never move it: the frozen plan is the version at 85dac3a. Since the tag the plan file has only gained §11 text.

## 4.5 Container state

- Git-ignored, container-only files (full rebuild list in `16_resume_here.md` §16.2): `data/raw/` (about 1.4 GB),
  `basis_panel.csv.gz`, `returns_daily.csv.gz`, `mcap_daily.csv.gz`, `data/processed/cache/*.pkl`. On 7 Nov 2026 the same
  container was still in place (all present; pyfixest installed). Added on 7 Nov (container-only, rebuildable):
  `data/raw/slb/` (2,915 files), `data/raw/amfi_monthly/` (102 files), caches `frictions_q.pkl`, `h5_monthly.pkl`;
  packages installed this session: rddensity, rdrobust, xlrd.
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
| `BSP_Thesis_Draft_Nov2026.pdf` (`thesis/`) | Internal draft (guide style) | 52 pp, all results; 7 Nov 2026 |
| `BSP_First_Results_Nov2026.pdf` (`progress_report_src/first_results_nov2026.tex`) | Guide-facing, **NOT SENT** | 5 pp; send only on the user's go-ahead |
| `docs/` | Outside readers, final repo | Current (pages 01 to 16) |
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
Density test at 95% (PAP §11.5 C8; docs/14 §14.8): transition population (below 95% the day before), CJM log ratio -0.05,
p = 0.86; robust across p, h, regimes, MWPL-change days; binned check +0.31 is bandwidth-driven (exploratory); cluster
bootstrap se of CJM 0.29. No bunching below 95%; utilisation accelerates toward the trigger. RD usable as supporting.
RD at 95% (PAP §11.6 C9; docs/14 §14.9): sharp (99.7% vs 0.06% in ban). Futures contracts -1.53, R -0.66, delivery share
+0.051 (all strong); cash volume no jump. Basis level -12.9 (p 0.02) BUT crossing-day basis already -11.3 (p 0.048) and the
same-contract change on t only -2.8 (n.s.) → level gap precedes the ban. Futures jump -0.57 EoD era vs -2.29 intraday era.
Placebo cutoff 0.90 basis +24 (h 0.008, degenerate). Open interpretive issue: rising OI with a falling basis before
entry may reflect new SHORT futures demand, not long → exploratory long/short build-up split of the level effect.
Build-up split (exploratory): long build-up -7.9 (2.7), short build-up -5.5 (2.2), diff +2.4 n.s.; closing groups +8.4 (n 30).
In-ban fall not specific to new longs; crossing-day dip concentrated in long build-up. The H7/level "blocked long demand"
reading is therefore only partial; keep it labelled post hoc.
Hysteresis (PAP §11.7 C10; docs/14 §14.10): Ban +0.38 (0.81), p 0.64 with 5 basis lags; without lags -14.1 → no extra
level shift once the path is held fixed; trading effects as H8; close-based +3.2 (p 0.001), rel. repo -51. Recurrent
VWAP vs close discrepancy on ban days flagged as a measurement issue (handoff/14).
H9 (PAP §11.8 C11; docs/14 §14.11): A: U slope +0.079 (0.038) p 0.019; U share 0.20 → 0.26-0.27 (step near 0.75), L and
level (date FE) flat. B (1 Oct 2025): first stage +0.28; U +0.061 p 0.11; level +4.8; ban +0.023 (all n.s., right sign).
C (quarterly resets): first stage +0.24; outcomes n.s.
H2 (PAP §11.9 C12; docs/14 §14.12): Ban0 x Bad +0.0074 (0.0341), p 0.59 (no power); pre-EA basis outside bans bad - good
-1.96 bp (1.11) p 0.039 (Saurav et al. direction); in bans uninformative; cash-only: bad -0.67%, good +2.40% vs F&O
(under-reaction both ways).
H1 (PAP §11.10 C13; docs/14 §14.13): index +3.48 bp/sd on band width (p 0.002), +2.53 on size (p 0.0006); persistence
opposite (-0.033, noise); stock FE → 0 (cross-sectional only); SLB scarcity wrong sign (SLB activity = demand). SLB data
built (NSE SLBM bhavcopies 2015-2026). H4 (§11.11 C14; §14.14): AMFI arbitrage AUM Apr 2018-Sep 2026 built; q80 on lagged
flow -17.5 (14.2) p 0.11; first differences -20.6 (6.8) p 0.001; pre-2023 -26 (p 0.06), post-2023 +17. Weak support.
SLB eligibility correction: SLB covers non-F&O liquid stocks since Jul 2013 (docs/handoff fixed; sent PDFs not).
H5 (PAP §11.12 C15; docs/14 §14.15): VW short leg G3 - G1 +0.04% (p 0.57); EW -0.49% (p 0.001) but long leg +0.46% too
(symmetric small-stock effect); momentum short leg -0.51% (0.22) fits. Summary table of all secondary tests: docs/14 §14.16.

## 4.11 Band-estimation chapter (7 Nov 2026; PAP §11.13 C16; docs/15_band_estimation.md)
Pooled threshold model (non-ban, 473,110 obs): gL -34.5 [-37.2, -32.2], gU +23.9 [+20.3, +26.1] (stock-demeaned);
linearity rejected (sup-F 7,471, boot p < 0.005); slopes -0.08/-0.47/-0.81; BIC: threshold < LSTAR < ESTAR < linear.
Exploratory: noise check (IV with x_(t-2)) shrinks slopes to -0.12/-0.19/-0.14 → much daily reversion is noise; asymmetry
in speeds not robust. Period-demeaned thresholds by STT period -39/+24, -31/+19, -32/+23, -32/+29; slope above upper edge
-0.77 → -0.15 over time. States: lower edge wider far from expiry; at high utilisation the basis is more often rich.
Observed-transition STR: reversion weakens with utilisation (+0.225, se 0.053), faster in the last week (+0.221 above 7
days), faster with large arbitrage assets (-0.077). Per-stock: median -26/+17 (width 41), unrelated to friction index.
Cost band: open+hold 27-31 bp (STT period 1→4), roll 4-8 bp; vs upper threshold +22 to +28 and p90 +24 to +30.
H7 IV (exploratory, 7 Nov): 2SLS delta_up -0.190 (0.077), delta_lo +0.088 (0.015) → H7's opposite-sign result survives the noise correction (docs/14 §14.3).

## 4.12 Constraint index deliverable (7 Nov 2026; PAP §11.14 C17; docs/16_constraint_index.md)
All NSE stocks, 80,042 stock-quarters (3,310 stocks): no short channel, SLB scarcity, CS spread, log Amihud, IVOL; loadings
+0.49/+0.45/+0.43/+0.49/+0.37, 53% variance, stable by year; persistence 0.90. Validation: delay +0.058 (t 20.8; within
stock +0.032); |BHAR| +0.023 (t 27); bad-news BHAR -0.008, good-news +0.001 (asymmetric without a size control; **8 Nov audit: with
size-decile FE the asymmetry vanishes, -0.0007 (0.0023), so it is a size effect**; delay +0.036 with log mcap, +0.028
with stock FE too; |BHAR| +0.015 with size FE; PAP §11.2 entry; analysis/audit/index_size_check.py);
F&O band width -6.4 (opposite; H1 F&O index is the relevant one there). Published: data/processed/constraint_index_q.csv.gz.

## 4.13 Write-ups (7 Nov 2026)
Thesis draft (`thesis/`, 8 chapters + 3 appendices, 52 pp, `BSP_Thesis_Draft_Nov2026.pdf`) and first-results report for the
guide (`BSP_First_Results_Nov2026.pdf`, 5 pp, not sent). Both follow the guide-facing style rules. The report corrects the
October report's SLB wording and counts. Digest of every finding: `memory/09_findings_digest.md`.

## 4.14 Remaining master-plan items (8 Nov 2026; PAP §11.15 C18-C20; docs/14 §14.17)
Spurious bans: pre-reform entries OI-driven (0.4% denominator-driven); post-reform simulation (validated 99.99%/100%):
actual 412 ban days/45 spells/11 stocks vs old rule 1,505/112/36; gross+new limit 6,256; FutEq+old limit 1 → reform cut
bans ~73%. Placebos: fake bans null for H7 and level effect; index-only and peak-margin dates within placebo range.
COVID restoration (70 stocks, 27 Nov 2020): utilisation -0.21, ban -4.6 pp, U -0.068 (t -2.1), level n.s.; fake-date
check clean except futures volume. Halving confounded by the crash. To fold into thesis ch5/ch6/ch8 and the report.

## 4.15 Deep audit of the whole project (8 Nov 2026; user asked for it before the submission write-up)
- Reproduction: `analysis/audit/rerun_all.sh` cleared the caches and reran all 28 analysis scripts: every one exits 0;
  outputs identical to the committed ones apart from run times and the last digit of one p-value. Now also runs the two
  new estimator tests and the index size check (docs/12 §12.3).
- New estimator tests: `analysis/test_cs_att.py` (CS ATT recovers -0.100: -0.1007, pre +0.0018; biased without the
  covariate) and `analysis/test_level_effect.py` (level-effect code recovers +10 and -6 bp shifts).
- Number check: `analysis/audit/check_numbers.py`; all decimals in thesis chapters, report and docs results pages match
  outputs except section numbers and one fee-schedule input.
- Fixes: thesis ch4 had the pre-audit "99.85%" agreement figure (corrected); "audit" wording removed from thesis appendices
  A and B; the model PDF (also thesis Appendix C) had the old "SLB lists drawn from F&O securities" wording in three
  places (corrected, PDF rebuilt; the version the guide received is archived as
  `models_src/modelC/BSP_Model_C_as_sent_Oct2026.pdf`); **the constraint index's bad-news asymmetry is a size effect**
  (corrected in docs/16, docs/README, thesis abstract, ch1, ch4 table, ch7 text and summary, report §7); ch4 index table
  given a size-control column and fitted to the page.
- Style scan of all guide-facing sources: no em dashes, no internal labels, no AI-sounding words. Both PDFs rebuilt
  (thesis 52 pp, 0 overfull boxes; report 5 pp).

## 4.16 Final write-up (9 Nov 2026)
- Thesis content completed (literature chapter; spurious bans, placebos, COVID restoration; SEBI retail-loss framing).
- Full re-read of the project (memory/10_reread_findings.md).
- Final thesis `BSP_Thesis_Final_Nov2026.pdf` (78 pp) in the new design: template front pages, exhibit-style figures and
  tables (26 figures, 12 tables), native model appendix. The 7/8 Nov draft PDF `BSP_Thesis_Draft_Nov2026.pdf` is kept.
- Open for the user: cosmetic changes; degree wording, date, acknowledgements; send decision.
- Presentation deck (9 Nov): `BSP_Presentation_Nov2026.pptx` and `.pdf`, 37 slides, format of `GammaLong_Finals_v11.pdf`
  and `Presentation Deck Example.pdf`; source `deck/build_deck.js`, charts `analysis/deck_figures.py` -> `deck/figs/`.
- Academic backup deck (9 Nov): `BSP_Presentation_Academic_Nov2026.pdf` (Beamer, Madrid recoloured blue, from the user's
  Hyderabad and Trento Overleaf templates); source `beamer/main.tex`, charts `analysis/beamer_figures.py` -> `beamer/figs/`.

