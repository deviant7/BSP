# 05. Next steps (detailed work plan)

Order is by dependency, not by date (no timelines). Everything must follow the frozen plan
`plan/pre_analysis_plan_v1.md`; read `07_test_plan.md` for interpretation notes. Any departure, however small, is logged
in PAP §11 with date and reason before results are reported, and the original specification is always reported too.

## CURRENT NEXT STEPS (9 Nov 2026; everything below this box is the original plan, all done)
1. The user reviews `BSP_Thesis_Final_Nov2026.pdf`, `BSP_Presentation_Nov2026.pptx` and
   `BSP_Presentation_Academic_Nov2026.pdf` and sends cosmetic changes; apply them in `thesis/`, `deck/build_deck.js`,
   `beamer/main.tex` (and the chart scripts), rebuild, re-run the style scan and `analysis/audit/check_numbers.py`.
2. Confirm front-page wording with the user: degree name, date, acknowledgements (neutral draft), certificate text.
3. Only on the user's go-ahead: send material to the guide; when sending, mention the SLB correction relative to the
   October report and that results are dated from the exchange's first dissemination time.
4. Optional items: Saurav et al. (2026) in full (library); Prowess check of pre-2017 market caps; XBRL SUE; put-call
   parity; fixing the project document's known errors (needs the user's go-ahead); a .pptx version of the Beamer deck.
5. Stage II (EC 497) work, if the user wants more analysis: intraday data for the ban tests; a longer post-reform sample;
   extending the model for blocked new demand; observed-state smooth-transition models of the band.

## Step 0. Session start checks (every new session)

1. `git status`, `git log --oneline -5`, `git ls-remote --tags origin` (`pap-v1` → 85dac3a is on GitHub since 5 Nov 2026).
   Full first-actions list: `16_resume_here.md` §16.2.
2. `ls data/raw data/processed`: if `data/raw` or `basis_panel.csv.gz` is missing, rebuild (`docs/12_reproducibility.md`;
   the price download takes about 2.5 hours and is resumable, so run it in the background).
3. `cd models_src/modelC && python3 verify_modelC.py` (ALL PASS) and `python3 -I analysis/test_setar_simulated.py`
   (known TAR -29.1/+15.2; model basis -10/0) as smoke tests.
4. Ask the user only what cannot be found in the repo (e.g. news from the guide).

## Step 1. Shared analysis infrastructure (before any test)

Create `analysis/samples.py` (build once, reuse everywhere) and write a counts report (`analysis/output/sample_report.txt`).

1. **Contract choice:** from `basis_panel.csv.gz`, for each stock-day take k = 0 unless the near contract has 3 or fewer
   **trading** days to expiry (count with the trading calendar = dates of `mwpl_oi_panel`), then take k = 1.
2. **Liquidity:** `n_contracts >= 5` (n_contracts is the number of contracts for both formats; UDiFF counts were moved from
   `qty` in the builder).
3. **Exclusions:** `pv > 0` (dividend within contract life), `event_in_life`, first 20 trading days after an F&O entry
   (`fno_events.csv`), `F_vwap` missing (lot failure). Keep `r_filled` rows but flag for a robustness drop.
4. **Changes:** Delta m_t = m_t - m_(t-1) only when both days are in the sample, consecutive trading days, and the **same
   expiry** (never across a roll). Lagged level m_(t-1) from the same contract.
5. **Winsorise** m at 1% and 99% within each calendar year for the main estimates; keep the raw value for robustness.
6. **Treatment merge (now allowed):** Ban_it = stock in `ban_days.csv.gz` on day t (any source; robustness: drop
   `source == imputed`). omega_(i,t-1) = `util` (before 1 Oct 2025) or `util_futeq` (from 1 Oct 2025) on day t-1.
   Spell variables from `ban_spells.csv.gz`: day of spell, spell length, and "an expiry date has passed since the spell
   start" (expiry dates from the basis panel).
7. **Inference helpers** (`analysis/inference.py`): two-way fixed effects (stock and date) by alternating demeaning;
   two-way clustered standard errors (Cameron, Gelbach and Miller: V = V_stock + V_date - V_stock-and-date);
   wild-cluster bootstrap (Rademacher or Webb weights) for event studies with few clusters; Holm correction.
   `pyfixest` is installable from PyPI in the container (checked 5 Nov 2026: pyfixest 0.60.0 downloads); cross-check the hand-written code against
   it on one regression. Write unit tests on simulated data with known coefficients.

## Step 2. Primary tests (order: H8, H7, H3, H6) — ALL DONE 5 Nov 2026 incl. Holm (results: 04 §4.7, §4.9; docs/14). Kept below for reference.

H8 first: it is the mechanical check that bans bind and that the ban timing is right; if it fails, the ban results need
re-thinking before anything else.

### H8: trading moves out of futures (pre-October 2025 bans)
- Unit: stock-day, F&O stocks, 2015 to 30 Sep 2025, excluding expiry days (open interest drops mechanically at expiry).
- Variables: near + next contracts: Delta OI and volume **in contracts**. Verified 5 Nov 2026: `oi` and `chg_oi` in
  the basis panel are in **shares** in both formats (oi / lot_used is an integer for 99.7% of legacy and 99.3% of UDiFF
  rows), so divide by `lot_used` to get contracts. Futures volume in contracts (`n_contracts`); cash volume `S_qty`; delivery share
  from `data/raw/prices/deliv` (deliverable / traded).
- Test 1: distribution of (Delta OI + volume) / volume on ban days; prediction about 0 (every trade closes for both sides).
- Test 2: within-stock comparison of ban days with the same stock's non-ban days in the same utilisation bin (e.g. bins of
  0.05 in omega_(t-1) from 0.80 to 1.00), regression of log futures volume, log cash volume, delivery share on Ban with
  stock-by-bin and date fixed effects; two-way clustered SE.
- Falsifier: (Delta OI + volume) not close to 0, or futures activity not lower.
- Report post-October 2025 bans separately and descriptively (delta-based rule allows cross-instrument offsets; the
  identity may fail by design).

### H7: one-sided correction
- Specification in `07_test_plan.md` and PAP §5. Regimes from the stock's own 20th/80th percentiles of m on non-ban days;
  mu_i = stock median on non-ban days; regressors (m_(t-1) - mu_i) x regime x {1, Ban}; stock and date FE; two-way SE.
- Prediction: delta_upper > 0, delta_lower <= 0; with the expiry-in-spell interaction, delta_lower moves toward 0 after an
  expiry inside the spell. Falsifier: delta_upper <= 0 or delta_upper = delta_lower (test the difference).
- Robustness (all pre-specified): thresholds from a per-stock 3-regime threshold model on non-ban days; fixed +/-25 bp
  around the median; state-dependent thresholds (thresholds depending on lagged OI/MWPL); unwinsorised; drop imputed ban
  days; drop `r_filled`; close-based basis; relative implied repo.
- Report pre- and post-October 2025 separately as well as pooled (post has 44 spells: low power, stated in advance).

### H3: costs set the band edges
- Dates: 1 Apr 2023, 1 Oct 2024, 1 Apr 2026. Windows +/-40 trading days. All F&O stocks.
- Outcome per stock and window: 80th and 20th percentiles of m (clean sample), and threshold-model edges.
- Prediction: upper edge rises after each date; ordering of the rises 2026 > 2024 > 2023 (cost changes: +0.03, +0.0075,
  +0.0025 percentage points of STT on the futures sale; plus whatever share of the round trip this represents; compute the
  implied change in c_plus in bp: 0.0025% = 0.25 bp, 0.0075% = 0.75 bp, 0.03% = 3 bp per side).
- **Important:** these cost changes are small (0.25 to 3 bp) relative to band widths of tens of bp; power will be low;
  the 2023 date is confounded with the debt-fund tax change (reported, not claimed). State this when reporting.
- Inference: paired stock-level differences, clustered by stock; wild bootstrap; placebo dates (e.g. index-only reform
  dates of 20 Nov 2024 and 1 Feb 2025, and random dates).

### H6: short-sale access (F&O entry and eligibility exit)
Needs inputs not yet built:
- **Daily returns for the cash universe** (all EQ/BE/BZ stocks): from `data/raw/prices/cash`. Checked 5 Nov 2026:
  NSE's `PREVCLOSE` is **not** adjusted (TATASTEEL 1:10 split, 28 Jul 2022: prevclose 959.4, close 100.35; RELIANCE 1:1
  bonus, 28 Oct 2024: prevclose 2655.70, close 1334.35). Build adjustment factors from corporate actions (splits:
  "From Rs X ... To Rs Y"; bonus "a:b" → factor (a+b)/b; rights and demergers flagged and excluded around ex-date).
- **Market capitalisation**: no free NSE file found (checked: `archives/equities/mcap/...` 404; the daily PR zips have no
  market-cap file). Plan: shares outstanding = paid-up equity capital / face value from each quarter's XBRL results filing
  (links in `announcements.csv.gz`), carried forward to the next filing; market cap = shares x close. Free float =
  MWPL/0.20 cross-checks F&O stocks.
- **Market return** for price delay: equal-weighted cash-universe return, or Nifty 50 / a broad index file.
- Outcomes: price delay (weekly returns, 52-week windows), VR(5), BHAR[+2,+64] after bad news (EAR in bottom tercile or
  quintile; pre-specify which in §11 before running if the PAP is silent).
- Design: Callaway and Sant'Anna staggered DiD for entries; separately for eligibility exits (158 usable); controls
  not-yet-treated and never-treated cash stocks matched on size, turnover, volatility over the 6 months before. Python
  options: `csdid` / `differences` packages, or implement group-time ATTs directly. Sun and Abraham as a check.
- Batches (45 entries on 29 Nov 2024; 34 exits on 28 Jun 2019) dominate; report with and without them.

### Multiple testing
Holm across the four primary tests at 5% (one p-value per hypothesis; decide in §11 before running which statistic is
the hypothesis's p-value where several exist, e.g. delta_upper - delta_lower for H7, the mean (Delta OI + volume) / volume
or the futures-volume coefficient for H8).

## Step 3. Secondary tests — ALL DONE 7 Nov 2026 (PAP §11.4 to §11.12, each committed before running; results docs/14 §14.7 to §14.16; summary in 04 §4.10)
Level effect, density test, RD, hysteresis, H9, H2, H1, H4, H5. Scripts in `analysis/` (level_effect.py,
level_effect_buildup.py [exploratory], density_test.py, rd_95.py, hysteresis.py, h9_regime.py, h2_badnews.py,
h1_frictions.py, h4_capital.py, h5_anomalies.py). New data: SLB bhavcopies, AMFI monthly arbitrage-fund series.

## Step 3b. Analyses in the master plan that are not PAP tests (still to do; ask the user which first)
1. **DONE 7 Nov 2026 (docs/15_band_estimation.md; PAP §11.13 C16 + §11.2).** No-arbitrage band chapter (master plan §5, Ch 4; the guide's area, non-linear time series): 3-regime threshold
   models (per stock and pooled, by period) and smooth-transition (ESTAR/LSTAR) error-correction models of the basis;
   thresholds/adjustment speeds against the dated cost, capital and limit changes; state-dependent thresholds (lagged
   OI/MWPL). The estimators exist (`analysis/setar.py`) and were tested on simulated data; H3 used quantile edges. This
   is descriptive/estimation work, not a new confirmatory test; anything new it tests needs a §11 entry first.
2. **DONE 7 Nov 2026 (docs/16; PAP §11.14 C17).** **Constraint index as a stand-alone deliverable** (project-document goal): the H1 index (Corwin-Schultz, Amihud, IVOL,
   utilisation, SLB) is built per stock-quarter (`data/processed/cache/frictions_q.pkl`); document, validate against bands,
   decide on the SLB input (its sign suggests it measures borrowing demand).
3. Optional: XBRL EPS for SUE (secondary surprise measure for H2/H6); index dividends; announcement-aware dividend
   adjustment; BSE-only results.
4. DONE 7 Nov: H7 with x_(t-2) as instrument (opposite sign survives; docs/14 §14.3).
5. Open interpretive threads (handoff/14): VWAP vs close basis on ban days; long vs short build-up; RD basis gap before the
   ban; 8 Dec 2025 broker date.

## Step 3c. DONE 8 Nov 2026: remaining master-plan items (PAP §11.15; docs/14 §14.17)
Spurious bans (counterfactual ban simulation), placebos (fake bans, index-only reforms, peak margins), COVID halving and
restoration. To fold into the thesis (ch5 position limits, ch6 ban, ch8 policy) and the first-results report in the
final write-up. Then: deep audit of the whole project (user request, 8 Nov), then the final write-up with the user's
cosmetic changes. Literature-review chapter: adapt the existing 29-page review (litreview_src/) after fixing its known
errors (handoff/11 §11.6), at the final write-up stage (user, 8 Nov).
**Deep audit DONE 8 Nov (04 §4.15). Agreed plan for the next session: `16_resume_here.md`, "PLAN FOR THE NEXT SESSION".** Next: the final write-up stage above (fold §14.17 in, retail-loss framing, literature
chapter), then the user's cosmetic changes.

## Step 4. Inputs (status 7 Nov 2026)

| Input | Status |
|---|---|
| AMFI monthly arbitrage-fund series | DONE (Apr 2018 to Sep 2026) |
| SLB bhavcopy | DONE (2015 to 2026) |
| Market capitalisation | DONE (AMFI half-yearly + back-cast; Prowess only to verify pre-Jul-2017) |
| EPS from XBRL filings | not collected (optional, SUE) |
| Index dividends; BSE-only results; dividend adjustment | optional |

## Step 5. Writing and reporting

1. `docs/14_results.md` (final-form results page): every pre-specified test, original specification first, nulls
   included. Complete for primary and secondary tests (7 Nov 2026).
2. Thesis chapters in LaTeX (structure in 01). The literature-review PDF needs its known errors fixed before reuse.
3. DONE 7 Nov 2026 (draft, NOT SENT): `BSP_First_Results_Nov2026.pdf`. Thesis draft: `BSP_Thesis_Draft_Nov2026.pdf`
   (`thesis/`). Next: the user reviews both; send the report only on the user's go-ahead; revise the thesis after the
   guide's comments; read the three library papers when obtained; consider a model extension for blocked new demand
   (only if the guide agrees; the model itself is not changed to fit results).
4. With the user's go-ahead only: correct the project document's known errors (short-selling line, 30x leg,
   "relaxations", timeline). The next guide-facing document must also correct the SLB-eligibility wording of the sent
   report and model PDF (SLB is not limited to F&O stocks; short selling is).

## Step 6. Keep continuity

After each step: update `memory/05_session_log.md`, the relevant `handoff/` files (at least 04, 05, 09, CHANGELOG),
`docs/` if something final changed, commit, push.
