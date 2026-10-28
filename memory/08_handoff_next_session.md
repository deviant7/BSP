# 08 — HANDOFF FOR THE NEXT SESSION (written 28 Oct 2026, end of session)

Read this file first, then CLAUDE.md and memory/01–07. It states exactly where the project is, what is waiting on whom,
every artefact, every rule, and how to rebuild everything.

---------------------------------------------------------------------------------------------------------------------
## 0. Git / GitHub (the user asked about this)
- All work is on branch **`claude/compassionate-rubin-s9gny2`** of `deviant7/bsp` (pushed; remote == local at session end).
- **PR #1 (https://github.com/deviant7/BSP/pull/1) was opened and merged by the user on 28 Oct 2026** → `main` (merge commit
  65ef0e3) now contains all work up to 0e78747. The working branch was then restarted from `origin/main`. Later work on the
  branch needs a new PR to reach `main` (create one only if the user asks).
- Commit trailers required: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and
  `Claude-Session: https://claude.ai/code/session_01M6SKm82udXsHf6727aGMNw`. Never put model names in repo files.
- `data/raw/` (1.2 GB) and `data/processed/basis_panel.csv.gz` (74 MB) are git-ignored → **lost when the container ends**;
  rebuild with the scripts (§5). Everything else needed is committed.

## 1. Where things stand (one paragraph)
Theory (Model C) is written and verified; the ban/MWPL panel (2010–2026), F&O membership/events, price data, basis panel,
announcements, Nifty series are built and checked; the guide-facing progress report is final (26 pp) but **not yet sent**;
the pre-analysis plan v1 is complete but **NOT tagged** — **the user decided (28 Oct 2026) to wait for the guide's reply
before locking it**. Blind rule in force: **no outcome (basis, returns, drift, delay) may be related to any treatment (ban,
utilisation, MWPL shocks, STT dates, F&O entry/exit, tax change) until `pap-v1` is tagged.**

## 2. Waiting on the user / guide
1. User sends `BSP_Progress_Report_Oct2026.pdf` to Prof. Aditi **Chaubal** (user once typed "Chawla" — spelling not yet
   confirmed; report uses "Chaubal").
2. User removed §7 "Points on which I would value your guidance" from the report (kept in
   `progress_report_src/removed_guidance_questions.tex`); the user will ask these personally:
   (1) wider framing OK? (2) theory depth? (3) TAR vs STAR, state-dependent thresholds? (4) Prowess/EPS access (now less
   needed: EPS via NSE XBRL, free float via MWPL)? (5) does she want the test plan before main estimates?
3. Guide's reply → adjust PAP if she asks → **tag `pap-v1`** (git tag) → only then run outcome-vs-treatment analyses.
4. Full texts still needed via IITB library (blocked online): Saurav–Srivastava–Agarwalla (2026, SSRN, "Decoupled…" —
   closest competitor to H2/H7), Gagnon (2018, Financial Review 53(1) 5–50), Brennan–Schwartz (1990, J. Business 63(1) S7–S31).

## 3. What can be done next WITHOUT breaking the blind rule
- AMFI monthly arbitrage-fund AUM/flows (from mid-2018) — capital series for H4.
- XBRL EPS extraction for SUE (links in `data/processed/announcements.csv.gz`: xbrl_standalone / xbrl_consolidated;
  legacy XML until Mar 2025, Integrated-Filing XML after).
- Corporate-action-aware dividend adjustment (announcement-date based) to fix the dividend over-correction.
- SLB data (NSE SLB bhavcopy) for the friction index.
- Cash-universe efficiency measures (Hou–Moskowitz delay, VR) — outcome construction only.
- State-dependent-threshold estimator (thresholds depending on lagged OI/MWPL) + test on model-simulated data.
- Formal density test of utilisation at 95% (treatment-side; allowed).
- Optional: fix the project document / lit review errors listed in memory/04 (awaiting user go-ahead).

## 4. Rules from the user (all durable)
- Save to memory after every meaningful step; commit + push.
- No timelines/time pressure; order work by dependency.
- Project = limits to arbitrage in Indian equities broadly; F&O ban is one important lens, not the whole project.
- Keep every past plan and every deletion (`plan/archive/`, `REMOVED_ITEMS_REGISTER.md`); update the register on any change.
- Guide-facing documents: NO internal references (no Model A/B/C labels, audit, memory, phases, file paths, reading-status
  notes, our past mistakes). No em dashes, no AI-sounding phrases; plain first-person language. One PDF to the guide.
- Honest, rigorous, primary sources; flag errors plainly. Verify facts online when needed.
- User's earlier question "can we work with data without modelling?" → answered: keep the existing model (guide asked; it
  changed the design), no further theory unless data demand it; mostly data from now on.

## 5. Rebuild recipe (fresh container)
Tools: `apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`;
`pip install numpy pandas matplotlib openpyxl`. NSE archives reachable via the agent proxy; FRED needs curl.
```
python3 -I data_pipeline/download_nse_mwpl.py data/raw 2010-01-01 2026-10-27          # ~40 min, 6 threads
python3 -I data_pipeline/download_nse_prices.py data/raw/prices 2015-01-01 2026-10-27 3 # ~2.5 h (resumable; >2h bg limit)
python3 -I data_pipeline/download_rates_corpactions.py data/raw 2014 2026
python3 -I data_pipeline/download_results_filings.py data/raw 2014 2026
python3 -I data_pipeline/download_results_filings.py data/raw 2025 2026 integrated
python3 -I data_pipeline/download_index_close.py data/raw/indices/nifty50_daily.csv 2015-01-01 2026-10-27
python3 -I data_pipeline/build_mwpl_panel.py data/raw data/processed
python3 -I data_pipeline/describe_bans.py data/processed reports/figs
python3 -I data_pipeline/build_fno_events.py data/raw data/processed
python3 -I data_pipeline/build_announcements.py data/raw data/processed   # needs mwpl panel + fno_membership first
python3 -I data_pipeline/build_basis.py data/raw data/processed
python3 -I data_pipeline/report_figs.py data/processed reports/figs
python3 -I data_pipeline/report_tables.py data/processed reports/tables
python3 -I analysis/test_setar_simulated.py
cd models_src/modelC && python3 verify_modelC.py     # all checks PASS
```
Report: `cd progress_report_src && pdflatex progress_report_oct2026.tex` (twice) → copy to repo root.

## 6. Key verified numbers (for any later writing)
- Ban/MWPL panel: 4,120 trading days (Feb 2010–27 Oct 2026), 476 symbols. Flags vs next-day ban list 11,753/11,771 (99.85%).
  Entry rule (ω>0.95 day before) 99.2%; exit rule (ω≤0.80 last ban day) 99.5% of spells.
- Main sample 2015–2026: 1,789 spells, 9,414 ban stock-days, 141 stocks; median spell 4 days pre-Oct-2025 (mean 5.2), 9 days
  after (n=44, mean 9.3). Peaks 2017 (1,586 ban days) and 2024 (1,656).
- COVID halving: 61 stocks halved in files 20–27 Mar 2020; 70 restored in 26 Nov 2020 file.
- 1 Oct 2025: all 208 F&O stocks' MWPL fell; median ratio 0.73; 17% at floor (0.5), 48% at 15% FF (0.75). Rebuild from
  pre-reform data exact for the 15%-FF leg (85 stocks); ADDV leg: actual ≈ +6.5% vs NSE-only deliveries (BSE).
- MWPL changes cluster Feb/May/Aug/Nov (quarterly free-float updates). Pre-Oct-2025 FF = MWPL/0.20.
- F&O membership = STF listed that day; 534,712 stock-days 2015–2026, 374 symbols; 239 entries, 171 exits (162 eligibility);
  usable 233 / 158; 21 renames linked by ISIN; batches 29 Nov 2024 (45 entries), 28 Jun 2019 (34 exits), 28 Feb 2025 (16 exits).
- Price data: 2,916 trading days with futures+cash+delivery (gap: F&O file 30 Mar 2021 missing at NSE).
- Basis: 1.65 m futures rows; VWAP inside [low, high] 99.77% (2.0% of legacy rows needed lot snapping); clean near-month
  sample 499,682 stock-days: median +1.2 bp, p10 −33.0, p90 +26.1; |m|>200 bp 0.65% (distressed stocks; kept).
  Dividend days over-corrected (+9.7 vs +1.1 bp; unadjusted −48.8) → flagged; non-dividend events flagged (0.9%).
- Announcements: 89,452 events (symbol×quarter), 7,910 for stocks while in F&O (188 on ban days); 63% after 15:30.
- Nifty check (Nov–Mar contracts): implied repo (incl. trailing yield) vs 3M interbank: corr 0.47, gap +0.67 pp; ~+2 pp since 2021.
- SETAR estimator: recovers known TAR (−30/+15 → −29.1/+15.2); on model-simulated basis gives −10/0 (inventory-dependent
  thresholds) → fixed thresholds = average edges, not costs.

## 7. Data errors found and fixed (so they are not re-introduced)
combineoi: 107 files with 2-digit years; misdated files (02112012 holds 5 Nov; 02102015 holds 1 Oct → reassigned); bundled
multi-day zips around 30 Jun–2 Jul 2025 (read all members); 13 corrupt files May–Jun 2012 (corrupt at NSE); 713
'Not available in NSE-F&O' placeholder symbols (restored from ISIN; 25 dropped on ISIN-change days); never use float_format on
9-digit MWPL. fo_secban: trailing commas in symbols; misdated 19 Feb 2014 (says 19 Mar) and 25 Aug 2014. F&O bhavcopy: 30 Mar 2021
missing (bridge in membership); legacy files lack lot size (gcd of OI/ΔOI, snapped to multiples via value/(contracts×mid));
UDiFF TtlTradgVol = contracts. Corporate actions: 'sub-division' contains 'div' (use the word 'dividend'); NTPC bonus debentures
(20 Mar 2015) etc. → event flag. NSE theoretical settlement price on no-trade days → use VWAPs. Results: API changed to
Integrated Filing from Mar-2025 quarter (paginated; size=20000, check totalCount); calendar must start 2010 (else pre-2015 events
land on 1 Jan 2015). User's F&O sheet: index rows, 3 truncated symbols, NSETEST, no muhurat days, ends 23 Dec 2025.

## 8. Artefact map (what each file is)
- Root PDFs: `BSP_Progress_Report_Oct2026.pdf` (FINAL guide report, 26 pp incl. model appendix; not sent),
  `BSP_Model_C_Constrained_Arbitrage_India.pdf` (theory, guide-safe), older A/B/progress PDFs (superseded, kept).
- `plan/BSP_Research_Plan_v2.md` (master plan), `plan/pre_analysis_plan_v1.md` (test plan, untagged), `plan/archive/*`.
- `data_pipeline/*.py` + README (sources, URL patterns, formats, measurement notes, blind protocol).
- `data/processed/`: mwpl_oi_panel.csv.gz, ban_days.csv.gz, ban_spells.csv.gz, symbols.csv, descriptives.txt, build_report.txt,
  fno_membership.csv.gz, fno_events.csv(+report), announcements.csv.gz(+report), basis_report.txt, nifty_futures.csv.gz,
  nifty50_daily.csv; basis_panel.csv.gz (git-ignored).
- `reports/figs/*.pdf`, `reports/tables/ban_by_year.tex` (used by the report).
- `analysis/setar.py`, `analysis/test_setar_simulated.py`.
- `models_src/modelC/` (tex, verify_modelC.py, verify_output.txt, figs).
- `references/` 1–22 + notes batches 1–6 + 00_reference_index.md (with corrections appended).
