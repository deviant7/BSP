# 16. RESUME HERE (updated 7 November 2026, after all secondary tests)

**Update 7 Nov 2026 (supersedes §16.1 and §16.3 where they conflict):** the user asked to "go ahead with the next steps
carefully ... keep updating docs, memory and handoff". Done this session: broader context read (memory, plans, notes,
chat logs); corrections verified against primary sources (in-ban rule from Oct 2025 is looser; SLB is not F&O-only);
**all secondary tests run**, each with a dated PAP §11 entry committed first (C7 level effect, C8 density, C9 RD, C10
hysteresis, C11 H9, C12 H2, C13 H1, C14 H4, C15 H5); new data: SLB bhavcopies 2015-2026 and AMFI monthly arbitrage-fund
series. Results: `docs/14_results.md` §14.7-14.16 (summary table §14.16); state `04_current_state.md` §4.10; next steps
`05_next_steps.md` Step 3b (band-estimation chapter, constraint index deliverable) and Step 5 (write-up; ask before
sending anything to the guide). Extra pip installs needed in a fresh container: `rddensity rdrobust xlrd` (statsmodels
present). New git-ignored inputs to rebuild if lost: `data/raw/slb/` (download_slb.py, ~30 min), `data/raw/amfi_monthly/`
(download_amfi_monthly.py); caches `frictions_q.pkl`, `h5_monthly.pkl` rebuild automatically.

## (Original card of 5 November 2026 follows)

The user ended the session with: "Save everything to memory ... We will pick up from exactly where we left off in the next
session." This page says exactly where that is and what to do first. Read `00_START_HERE.md` (reading order) and this
page; the detailed state is in `04_current_state.md`.

## 16.1 Where we stopped

- **All four primary tests are done and Holm-corrected** (frozen plan `pap-v1`, commit 85dac3a; implementation details
  fixed in PAP §11 before each run):

| Test | Result | Pre-specified p | Holm p |
|---|---|---|---|
| H8 trading moves out of futures | supported (futures volume -2.00 log points, cash +7.3%, delivery share +4.1 pp); the "dOI = -V" identity holds only under intraday enforcement (23 Mar 2020 to Sep 2025) | 1.9e-41 | 7.4e-41 |
| H3 costs set band edges | supported on the pre-specified statistic (+6.4 / +7.4 bp in 2024 / 2026, ordering holds) but placebo-calibrated p ~ 0.05; width and edge-relative-to-median not unusual | 1.8e-24 | 5.5e-24 |
| H6 short-sale access | supported through price delay (entry -0.109, se 0.023; SA -0.063); drift components contradict (entry makes bad-news drift stronger, -0.040) | 5.2e-6 | 1.0e-5 |
| H7 one-sided correction | rejected with the opposite sign (delta_up -0.089, delta_lo +0.081); exploratory: concentrated at spell starts, era-dependent, not noise | 1 | 1 |

- The user approved the plan for the next steps ("The plans seem fine"), asked for deep research on the open questions
  (done, see `04_current_state.md` §4.8 and `docs/14_results.md`), asked to get the H6 data (done from free sources; Prowess
  only optional, to verify pre-July-2017 back-cast market caps), and asked to keep memory, docs and handoff updated (done).
- **Last thing the assistant told the user:** next come the secondary tests, starting with the ban level-effect test, each
  with its open details written into the plan's log (§11) before it runs.
- Nothing is waiting on the user. Optional for him: Prowess market caps 2015 to mid-2017 (verification); the Saurav,
  Srivastava and Agarwalla (2026) paper from the library (positioning of H2/H7 before writing); go-ahead to fix the errors in
  the project document.

## 16.2 First actions in the next session (in order)

1. `git status`, `git log --oneline -5` (latest commits are the 7 Nov 2026 context-gathering saves after beb11b5), `git ls-remote --tags origin`
   (`pap-v1` → 85dac3a).
2. Check what the container still has. These are **not in git** and must be rebuilt if missing:

| File | Size | Rebuild | Time |
|---|---|---|---|
| `data/raw/` | 1.4 GB | download scripts (`docs/12_reproducibility.md` §12.3, step 1, now including `build_amfi_mcap.py` which downloads the 18 AMFI PDFs into `data/raw/amfi_mcap/`) | ~4 h (prices ~2.5 h, resumable) |
| `data/processed/basis_panel.csv.gz` | 71 MB | `python3 -I data_pipeline/build_basis.py data/raw data/processed` | ~10 min |
| `data/processed/returns_daily.csv.gz` | 113 MB | `python3 -I data_pipeline/build_returns.py data/raw data/processed` | ~3 min |
| `data/processed/mcap_daily.csv.gz` | 31 MB | `python3 -I data_pipeline/build_mcap.py data/processed` (needs returns + `amfi_mcap.csv.gz`, which is committed) | ~1.5 min |
| `data/processed/cache/*.pkl` | 180 MB | `python3 -I analysis/samples.py` then `python3 -I analysis/h6_outcomes.py` | ~1 min |

3. `pip install pyfixest` (not preinstalled; version 0.60.0 was used) and check `pdftotext` exists.
4. Smoke test: `python3 -I analysis/h8_trading.py` must reproduce `analysis/output/h8_results.txt` (b = -2.0036 on log
   futures contracts). `cd models_src/modelC && python3 verify_modelC.py` must say ALL PASS.
5. Summarise the state to the user in about ten lines and continue with 16.3 unless he says otherwise.

## 16.3 The next piece of work: secondary tests (PAP §6), in this order

For each test: (i) write the open implementation details into PAP §11 as a new dated subsection (§11.4, §11.5, ...),
(ii) commit and push, (iii) run, (iv) report the pre-specified result first, exploratory additions after and logged in
§11.2, (v) update `docs/14_results.md`, `handoff/04`, `handoff/09`, `memory/05`, CHANGELOG; commit and push.
All secondary tests are labelled exploratory in reporting (PAP §6).

1. **DONE 7 Nov 2026 (results docs/14 §14.7, PAP §11.4 C7).** Level effect of bans (PAP §6 first bullet; model Prop. 6). Spec in the plan: stacked ban-entry event study, window
   -20 to +20 trading days; controls = stock-days with omega in [0.85, 0.95) in the same week that do not enter, matched
   on the 5-day omega path and basis level; split by composition of pre-ban activity (dOI / volume over the 5 days before
   entry: rising OI = new-exposure demand, falling = closing). Prediction: the level effect's sign follows composition
   (closing → basis higher in the ban; new demand → lower).
   Details to fix in §11.4 before running (draft): entry events = ban spells starting 2015 to 30 Sep 2025 (pre-reform rule;
   post-reform reported separately), one per spell; outcome = m_(t+k) - m_(t-1) of the chosen contract (C1 sample, same
   contract where possible; if the contract changes across the window, use the chosen contract each day and the level m,
   not differences); controls: for each entry day t, stock-days of other stocks with omega_(t-1) in [0.85, 0.95) not in a
   ban and not entering a ban within t..t+5 in the same calendar week; matching: nearest neighbours (up to 5, with
   replacement) on standardised omega_(t-1..t-5) and m_(t-1) (Mahalanobis); estimate = mean over events of treated minus
   matched-control path; composition C = sum of dOI over days -5..-1 / sum of volume (futures, near + next, contracts);
   split at C > 0 vs C <= 0; inference: event-clustered bootstrap or regression with stack fixed effects and SE clustered
   by stock. Note from H7 diagnostics and H8: the ban's bite differs across the three enforcement regimes (to 22 Mar 2020;
   23 Mar 2020 to 30 Sep 2025; from 1 Oct 2025): report by regime as exploratory.
2. **Density test at 95%** (treatment-side; supporting the RD): Cattaneo-Jansson-Ma (Python `rddensity` on PyPI may work;
   otherwise implement the local-polynomial density estimator) on omega_(t-1) for non-ban days and entry days, pre-reform.
3. **RD at 95%** (local linear on omega_(t-1), outcome next-day basis; supporting only).
4. **Hysteresis**: omega in [0.80, 0.95): in-ban vs not, controlling for omega, d omega, five lags of m (stock and date FE).
   (The H8 comparison already used this zone for trading outcomes.)
5. **H9**: basis quantiles by omega bins (0.60 to 0.95) on non-ban days; 1 Oct 2025 intensity DiD (ln MWPL_new/MWPL_old
   per stock; predicted change in utilisation) with stock and date FE.
6. **H2**: bad-news drift on ban days vs non-ban days (180 F&O announcements in bans; low power stated in advance);
   pre-announcement basis (days -5..-1) in bans vs not. Inputs ready (`data/processed/cache/event_outcomes.pkl`).
7. **H1**: friction index (bid-ask proxy, e.g. Corwin-Schultz from daily high/low, which the cash files have; Amihud from
   returns and traded value; idiosyncratic volatility; lagged headroom 1 - omega; SLB if obtained) vs band width;
   PCA weights. SLB data not collected (NSE SLB bhavcopy) — decide whether to collect or drop the SLB input (log it).
8. **H4**: arbitrage-fund AUM and flows (AMFI monthly, from mid-2018) vs the upper quantile of the cross-sectional basis,
   monthly. **Data not collected yet** — first find and download the AMFI monthly report series.
9. **H5**: anomaly asymmetry by constraint terciles (double sorts; public anomalies: momentum, reversal, MAX, IVOL,
   illiquidity, turnover; returns and market caps are ready).

After the secondary tests: write up (thesis chapters in LaTeX; next guide-facing PDF "first results" — ask the user before
sending; guide-facing rules apply: no internal references, no em dashes, plain first person). When describing the
results-date correction to the guide, say plainly that results are dated from the exchange's first dissemination time.

## 16.4 Things learned this session that must not be lost

- Ban enforcement regimes (primary sources `references/23`, `references/24`, `references/19`): end-of-day checks to
  22 Mar 2020; peak-intraday checks 23 Mar 2020 to 30 Sep 2025 (SEBI PR 18/2020, kept by PR 59/2020); end-of-day FutEq vs
  base position from 1 Oct 2025 (NSE Clearing 119/2025). Market-level FutEq trigger confirmed in data from 1 Oct 2025;
  broker notices' "8 Dec 2025" is probably broker-side entity checks (unresolved).
- NSE PREVCLOSE is not adjusted for corporate actions; split and bonus on the same day are separate records (multiply);
  the CA feed misses some splits (424 inferred); sub-rupee stocks create tick artefacts (price filter Rs 5).
- Results XBRL links exist only from 2018; NSE shareholding API only from 2021; AMFI half-yearly market-cap PDFs exist from
  Jul to Dec 2017 (URLs in `data_pipeline/build_amfi_mcap.py`).
- Two-way clustering by stock only (as in the H3 pre-specified test) over-rejects when all observations share an event
  date; placebo calibration is the honest check.
- The pre-specified H7 isolates the reduce-only arbitrage channel (P4) but the data are dominated at ban starts by the
  opposite channel (blocked new demand, P5). The level-effect test is the natural place to examine this, labelled as such.
- Entry into F&O selects on growth; the H6 delay effect may partly reflect that.
