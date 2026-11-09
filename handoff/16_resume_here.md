# 16. RESUME HERE (updated 9 November 2026, end of session)

This card supersedes everything below it. The older cards are kept, unedited, as a record.

## 16.A Where the project stands
- **Research complete.** Theory (Model C, verified); data built and audited; frozen plan `pap-v1` (85dac3a); all primary
  tests (+ Holm) and secondary tests; band chapter; constraint index; further checks (spurious bans, placebos, COVID
  halving and restoration); deep audit with a full reproduction (every output reproduces). Results: `docs/14`, `15`, `16`;
  every number: `memory/09_findings_digest.md`.
- **Deliverables (repo root), all built 9 Nov 2026:**
  - `BSP_Thesis_Final_Nov2026.pdf`, 78 pp. Source `thesis/` (`main.tex`, `bspstyle.sty`, `frontmatter.tex`, `abstract.tex`,
    chapters incl. `ch_literature.tex`, appendices A to C with the model native in `appC_model.tex`). Figures:
    `analysis/thesis_figures_final.py` -> `thesis/figs/`.
  - `BSP_Presentation_Nov2026.pptx` (+ `.pdf`), 37 slides, consulting format. Source `deck/build_deck.js`; charts
    `analysis/deck_figures.py` -> `deck/figs/`.
  - `BSP_Presentation_Academic_Nov2026.pdf`, 56 pages, Beamer (Madrid, blue). Source `beamer/main.tex`; charts
    `analysis/beamer_figures.py` -> `beamer/figs/`.
  - `BSP_Thesis_Short_Nov2026.pdf`, 50 pp, short version for quick readers (the full thesis remains the version of
    record). Source `thesis_short/`: copies of the chapter files, trimmed; `main.tex` sets `\input@path` to `../thesis/`
    for `bspstyle.sty` and `\graphicspath` to `../thesis/figs/`. Cut from the full version: approval, certificate,
    declaration, acknowledgements, lists of figures/tables, symbols; appendices B (data) and C (model); literature
    chapter condensed to three sections + Table tab:litbands; 10 supporting figures from the chapters (aum, modelpath, mwpl,
    basisexp, index, h4, spurious, covid, levelgroups, h5) plus the appendix figures: 18 of 29 remain; ch5 paragraphs "Capital as a state"
    and "Peak margins"; shorter ch6 caveats and ch4 validation paragraph. Added an "About this version" page.
    **Any text change to the full thesis must be copied into `thesis_short/` by hand.**
  - Superseded but kept: `BSP_Thesis_Draft_Nov2026.pdf`; `BSP_First_Results_Nov2026.pdf` (NOT SENT, not maintained).
- **Guide:** has the project document (Sep) and the October progress report only. Nothing sent since.

## 16.B Waiting on the user
1. Review of the thesis, its short version and both decks; cosmetic changes.
2. Front-page wording: degree "Bachelor of Science in Economics", date November 2026, acknowledgements (neutral draft for
   the user to rewrite), certificate text.
3. Go-ahead before sending anything to the guide (then mention the SLB correction against the October report).
4. Optional: library papers (Saurav et al. 2026 first), Prowess check, go-ahead to fix the project document, a .pptx
   version of the Beamer deck.

## 16.C First actions in a new session
1. `git status`; `git pull --ff-only origin claude/compassionate-rubin-s9gny2`; `git log --oneline -5`. The user sometimes
   commits files (templates, references) directly to the branch: pull before looking for them.
2. Read `CLAUDE.md`, this card, `memory/05_session_log.md` (last entries), `memory/09`, `memory/10`; for a full re-read
   follow `00_START_HERE.md`. If asked, read the final thesis PDF (`pdftotext -layout`).
3. Container check (not in git): `data/raw/`, `data/processed/basis_panel.csv.gz`, `returns_daily.csv.gz`,
   `mcap_daily.csv.gz`, `data/processed/cache/*.pkl`. Rebuild per `docs/12_reproducibility.md` if missing.
4. Fresh container: `pip install pyfixest rddensity rdrobust xlrd`; for the deck, install pptxgenjs and jszip in a
   scratch folder (13 §13.9).

## 16.D Rebuild commands
- Thesis: `python3 -I analysis/thesis_figures_final.py` (needs caches; about 5 min) then `cd thesis && pdflatex main.tex`
  twice; copy `main.pdf` to `../BSP_Thesis_Final_Nov2026.pdf`.
- Consulting deck: `python3 -I analysis/deck_figures.py`; `NODE_PATH=<scratch>/node_modules node deck/build_deck.js`
  (writes `BSP_Presentation_Nov2026.pptx` and applies the theme); validate and render with the pptx skill scripts.
- Academic deck: `python3 -I analysis/beamer_figures.py`; `cd beamer && pdflatex main.tex` twice; copy `main.pdf` to
  `../BSP_Presentation_Academic_Nov2026.pdf`; delete the aux files.
- Short thesis: `cd thesis_short && pdflatex main.tex` twice; copy `main.pdf` to `../BSP_Thesis_Short_Nov2026.pdf`;
  delete the aux files.
- Checks after any text edit: style scan (no em/en dashes, no AI words, no internal labels) and
  `python3 -I analysis/audit/check_numbers.py` (only section numbers and one fee input should be unmatched).

## 16.E Design specifications (for further edits)
- **Thesis** (`bspstyle.sty`, after `Main_content_formatting.pdf`, kept single-column): TeX Gyre Heros + sfmath; ruled,
  numbered, letter-spaced section heads with blue numbers (#1F4E9A); italic chapter lead (`\chapterlead`); captions
  "FIGURE n.m" label + bold takeaway title + `\exsub{subtitle}` + `\exsource{source}`; tables `\thd` headers, blue bold
  first column, grey `\rowrule`; footer rule with title and page; `\statstrip` key-number tiles on the abstract page.
  Front pages from the IIT Bombay BTP template.
- **Consulting deck** (after GammaLong and the Canva example): 4:3; Arial; 12pt grey tracker; 24pt bold navy (#254780)
  action title; 15 to 16pt navy subtitle; double rule (navy 2.5pt + blue 0.75pt); 12 to 14pt bold panel headers with
  navy underline; yellow (#FFF2B3) black-bordered callout; 8pt source; 9pt page number; agenda dividers with a navy band;
  navy label boxes with grey text boxes; numbered navy circles; grey chevron to a "What the chart shows" panel; charts in
  bright blue #00A3E8, mid blue, steel, near-black with thin black outlines and no gridlines.
- **Academic deck** (after the Hyderabad and Trento templates): Beamer Madrid, structure colour #1F4E9A, red alert
  blocks, green example blocks, times + mathptmx, title page with IITB logo, outline at each section, numbered captions,
  ball bullets, Proposition/Assumption blocks, references, acknowledgement, Thank You, backup frames.

## 16.F Rules in brief
Continuity in two layers after every meaningful step (memory + handoff + CHANGELOG, then commit and push to
`claude/compassionate-rubin-s9gny2`); guide-facing text: no em dashes, no AI phrasing, no internal labels, plain first
person; `docs/` final form only; keep every past plan and deletion; no timelines; no PR unless asked; never send to the
guide without the user's go-ahead; never put model names in repo files. Full list: `02`.

---------------------------------------------------------------------------------------------------------------------
# Archive of earlier resume cards (kept for the record; all items below are done)

## PLAN FOR THE NEXT SESSION (agreed with the user, 8 Nov 2026, end of session)
"Write-up" means **the final submission report only**: the thesis built from `thesis/`. The first-results report
(`BSP_First_Results_Nov2026.pdf`, NOT SENT) is not to be updated further unless the user asks.

**Part 1. Finish the content (the next steps already listed):**
1. Add the §14.17 results to the thesis: spurious bans (ch5 position limits, ch8 policy), placebos (ch6 ban), COVID
   halving and restoration (ch5/ch6). Numbers: docs/14 §14.17, 04 §4.14, memory/09.
2. Policy section (ch8): framing with SEBI's study of retail F&O losses (master plan §8).
3. Literature chapter adapted from `litreview_src/` / `BSP_Literature_Review.pdf`, after fixing its known errors
   (11 §11.6). Verify every citation against the primary source.
4. Optional, as the master plan lists them: band-of-inaction derivation appendix; replication guide appendix.

**Part 2. Context-building re-read (before any formatting work):** read every word of everything: every thesis
chapter and appendix, the model PDF and its source, every file in `docs/`, `handoff/`, `memory/`, `plan/`, the
analysis outputs, the root PDFs and other artifacts. Purpose: full context, and catch any remaining inconsistency.

**Part 3. Final build with the user's cosmetic changes:**
- The user will give (a) a **zip of a LaTeX report template**: use only its **first few pages** (title page and front
  matter); (b) a **PDF whose content-page formatting/design the user likes**: match that for the body.
- Build the final PDF = the final deliverable.
- **Lots of images/figures** so it is easy to read and follow (existing figures in `reports/figs/`, made by
  `analysis/thesis_figures.py` and `data_pipeline/report_figs.py`; add more where they help: e.g. ban timeline, band
  diagram, event-study paths, index maps). Follow the guide-facing rules: no em dashes, no AI-sounding phrases, no
  internal references, plain first person.
- Unzip the template into its own empty directory (untrusted files); do not run scripts from it.


**Latest state (supersedes the rest of this card where it conflicts):** after the checkpoint below, the band-estimation
chapter (`docs/15`), an exploratory IV check of H7 (opposite sign survives), the constraint index (`docs/16`,
`data/processed/constraint_index_q.csv.gz`), the docs update, the **thesis draft** (`thesis/`, `BSP_Thesis_Draft_Nov2026.pdf`)
and the **first-results report** (`BSP_First_Results_Nov2026.pdf`, NOT SENT) were completed and pushed. Every finding with
its numbers: `memory/09_findings_digest.md`. **Next:** wait for the user's review; send the report only on the user's
go-ahead; then revise after the guide's comments (see `05_next_steps.md` Step 5).
Rebuild the write-ups after any change: `cd thesis && pdflatex main.tex` (twice) → copy `main.pdf` to
`../BSP_Thesis_Draft_Nov2026.pdf`; `cd progress_report_src && pdflatex first_results_nov2026.tex` (twice) → copy to
`../BSP_First_Results_Nov2026.pdf`. Figures: `python3 -I analysis/thesis_figures.py` (needs the caches). Before any
guide-facing edit: no em dashes, no AI-sounding words, no internal labels (see `02` §2.6 and memory/06).

# (Checkpoint of 7 November 2026, evening)

The user asked for a safe checkpoint ("update everything so that if we ended here we can pick up in the next session"),
then to continue with the **band-estimation chapter first** and the remaining next steps. This card is self-contained.

## 16.0 Where the project stands
- Theory (Model C) done and verified. Data built and audited; SLB bhavcopies and AMFI arbitrage-fund series added 7 Nov.
- Frozen plan `pap-v1` (85dac3a, on GitHub). Every open detail was fixed in PAP §11 before each test (C1 to C15);
  exploratory additions are logged in §11.2.
- **Primary tests (+ Holm), 5 Nov:** H8 supported; H3 supported on the pre-specified test (placebo-calibrated weak); H6
  supported through price delay (drift contradicts); H7 rejected with the opposite sign.
- **Secondary tests, 7 Nov (all done; summary table `docs/14_results.md` §14.16):** level effect (basis falls about
  6 bp at ban start, more after faster OI build-up; pre-specified split p = 0.083); density at 95% (no bunching, p = 0.86);
  RD (trading jumps sharp; basis gap already on the crossing day); hysteresis (no extra level shift, p = 0.64); H9 (upper
  tail widens toward 95%, p = 0.019; reform right sign, p = 0.11); H2 (no power in bans; pre-announcement basis lower
  before bad news outside bans, p = 0.04); H1 (frictions and band width across stocks, p = 0.002); H4 (weak, p = 0.11;
  first differences p = 0.001); H5 (not supported value-weighted, p = 0.57).
- Corrections verified 7 Nov against primary texts: the in-ban trading rule from 1 Oct 2025 is looser (delta-reducing new
  contracts allowed), the 2025 package is not; SLB covers liquid non-F&O stocks since 2013 (short selling is F&O-only;
  SEBI circular 5 Jan 2024 = references/25). The sent report and model PDF keep the old SLB wording: fix in the next
  guide-facing document.
- Where everything is: state `04_current_state.md` (§4.7 to §4.10), numbers `09_key_numbers.md`, theory status
  `06_theory.md` §6.7, open issues `14_open_issues_and_risks.md` §14.6, history `03` Phase 5, next steps `05` Step 3b and 5.

## 16.1a First actions in a new session
1. `git status`; `git log --oneline -5`; `git ls-remote --tags origin` (pap-v1 → 85dac3a).
2. Check container files (not in git): `data/raw/` (incl. `slb/`, `amfi_monthly/`), `data/processed/basis_panel.csv.gz`,
   `returns_daily.csv.gz`, `mcap_daily.csv.gz`, `data/processed/cache/*.pkl`. Rebuild per §16.2 below and
   `docs/12_reproducibility.md` (new steps: `download_slb.py`, `build_slb.py`, `download_amfi_monthly.py`; secondary-test
   scripts listed there).
3. `pip install pyfixest rddensity rdrobust xlrd` (statsmodels present).
4. Smoke tests: `python3 -I analysis/h8_trading.py` (b = -2.0036); `cd models_src/modelC && python3 verify_modelC.py`
   (ALL PASS; restore the figure PDFs with `git checkout` if only timestamps changed).

## 16.1b DONE 7 Nov 2026 (docs/15_band_estimation.md; results 04 §4.11): the band-estimation chapter (master plan §5, Ch 4)
Not a PAP test; it is estimation and description of the no-arbitrage band over time. Plan (write a dated note in PAP
§11 before any new hypothesis-like comparison):
1. Pooled and per-stock 3-regime threshold autoregressions of the basis (`analysis/setar.py`), by period (STT regimes,
   capital regimes, position-limit regimes), reporting thresholds as **average band edges** (simulation lesson P3).
2. Smooth-transition error-correction (ESTAR/LSTAR) models of the basis with the deviation as transition variable
   (Tse 2001), and with observed transition variables (utilisation, arbitrage-fund flows) as the guide's area suggests.
3. State-dependent thresholds (lagged OI/MWPL terciles), and the asymmetry of the band (lower edge further from zero).
4. Linearity tests (Hansen-type threshold test with bootstrap; Luukkonen-type tests for STAR) and model diagnostics.
5. Bottom-up cost band per period (STT, stamp duty, fees, funding) to compare with the estimated edges.
6. Write `docs/15_band_estimation.md` (final form) and a results section; update handoff/memory.
Done after it (7 Nov): H7 IV check (opposite sign survives noise correction; docs/14 §14.3) and the constraint index
(docs/16; data/processed/constraint_index_q.csv.gz; 04 §4.12). **Next now: the write-up** (thesis chapters in LaTeX and/or
a first-results PDF for the guide; ask the user which, and never send anything without asking).

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
- Nothing is waiting on the user. Optional for the user: Prowess market caps 2015 to mid-2017 (verification); the Saurav,
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
5. Summarise the state to the user in about ten lines and continue with 16.3 unless the user says otherwise.

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
