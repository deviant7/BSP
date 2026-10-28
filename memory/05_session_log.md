# 05 — Session log (append newest at bottom)

## Before this repo (from the two conversation logs)
- Project selection (Very old conversation): Program A (limits to arbitrage / F&O ban) chosen over Program B (retail transformation).
- Project document written (Sep 2026). Guide asked for a theoretical framework first.
- Recent conversation: literature collected (21 PDFs), notes batches 1–5, 29-pp literature review (LaTeX), Models A & B (full + 3-pp guide
  versions), progress report to guide (Sep 28 2026) asking which model to lead with. No data work yet.

## Session 28 Oct 2026 (cloud session, branch claude/compassionate-rubin-s9gny2)
- Read both conversation logs, the project doc (docx = pdf), all 21 references in full (Shleifer–Vishny via OCR), notes, lit review,
  models, progress report. Built the audit in `04_models_and_audit.md` and the verified digest in `02_literature_digest.md`.
- User instruction: save memory regularly → created `CLAUDE.md` + `memory/` (this folder).
- User question: is the project-doc plan right, and is the pivot to modelling right? Advice given (summary):
  1. Guide's principle (theory before data) is right *for the core mechanism*, especially because the ban's effect on the basis has
     no obvious sign. But Models A/B were built to deliver H1–H6, so they rationalise the plan rather than discipline it; and they
     mis-model the ban (it freezes fresh OI for everyone). As built, they don't give the protection the guide wanted.
  2. Real guard against confirmation bias = a short corrected model whose predictions can come out either way + a written,
     git-timestamped pre-analysis plan (outcomes, specs, signs, tests) before looking at outcome–treatment relationships.
  3. Project-doc plan is too broad for the time left (6 chapters, 3 mispricing measures, 4 frameworks), has data gaps (EPS, accounting
     data), a circular constraint index, weak pre-2025 instrument, and all-confirmatory "expected results".
  4. Recommended core: (a) one model of the ban as a market-wide freeze of fresh futures OI, with daily-horizon arbitrageurs;
     (b) data pipeline built in parallel, blind to outcomes (treatment-side descriptives allowed); (c) identification: ban-entry
     event study vs near-miss controls, RD at 95% with McCrary, and the 1 Oct 2025 MWPL formula change as a continuous-treatment
     DiD using predicted ΔMWPL from pre-reform FF & ADDV; (d) TVECM bands pre/post as the dynamics lens.
     Demote: constraint index → descriptive; PCP → robustness if option data adequate; PEAD → only if EPS via Prowess/library;
     45-signal FM → drop/appendix (also check internship NDA/IP on the signal library). Policy chapter short.
  5. (Timeline advice given here was WITHDRAWN — see user correction below.)
- **User corrections (28 Oct 2026):**
  - Prof. Chaubal has NOT been sent the progress report or Models A/B. She knows only the project document.
    → A/B can be replaced freely; next thing she sees should be the corrected theory framework.
  - **Ignore the timeline entirely.** No time pressure; work at our own pace. Never plan around Stage I/II deadlines.
  - User agrees with most recommendations but thinks the project-document *goals* are good → keep them.
- Wrote `plan/BSP_Research_Plan_v2.md` (the master plan going forward). Key content:
  - Keep all six doc goals; order = theory → PAP → blind data build → validation → tests.
  - Theory: one model "ban as a reduce-only market-wide freeze": one-sided arbitrage in ban (positive-basis
    deviations persist, negative revert via unwinding of long-cash/short-futures inventory), spot spillover
    (level effect can be negative), anticipation/bunching below 95%, hysteresis (95/80). Keep A's static band
    (Props 1–2); replace A Props 3–6; B demoted to econometrics appendix with fixes. Simulate model and run
    all estimators on simulated data.
  - Hypotheses revised: H1 index (frictions only), H2 PEAD asymmetric (bad news in ban), H3 estimated vs
    cost-implied band, H4 heterogeneous 1 Oct 2025 effects (no "relaxation"), H5 two-sided, H6 mechanical
    variation; new H7 (one-sided correction) and H8 (spillover to cash).
  - Designs: near-miss ban-entry event study; RD (supporting); hysteresis design; quarterly MWPL
    recalculation dates; 1 Oct 2025 predicted-Δutilisation intensity (FutEq numerator + new denominator).
  - Measurement: basis + relative implied repo; put–call–futures parity; SUE (if EPS via NSE XBRL/Prowess)
    and EAR (price-only); constraint index from frictions only, crowding index separate, validated vs bands.
  - Cross-section: SYY double sorts + FM; public anomaly set; F&O inclusion/exclusion events as staggered
    DiD over ~2,000 stocks (power fix). Internship 45-signal library only if cleared under the agreement.
  - Pipeline validation: replicate Nandan et al. (2014) Nifty futures basis.

- **User note (28 Oct 2026): the project is limits to arbitrage in Indian equities broadly — the ban is an important focus but
  not the whole project.** Plan v2 revised accordingly: §0 maps each kind of limit (short-sale, costs, capital/funding, arbitrage
  risk, position limits) to an Indian shock; one model with each limit as a parameter; new chapters: Ch 4 bands over time
  (costs/capital/reforms), Ch 5 ban, Ch 6 F&O eligibility + cross-section; hypotheses renumbered H1–H9; §10 lists trimmed items
  (PCP → optional, per-day TAR, latent-factor index, 45-signal FM chapter, OSF, CS-DiD for 2025 reforms, pre-2025 FF instrument).
- **Internet fact-check of all claims done** → `memory/07_fact_check.md`. Key corrections: "30× volume" MWPL leg ended 2006
  (pre-2025 MWPL = 20% FF); ADDV in quantity terms; MFs may short (Slivka outdated); "Korea/Taiwan position-limit studies" unsupported;
  80% exit confirmed (NSE Clearing 119/2025, saved as references/19). New facts: COVID MWPL halving 2020; STT 0.05% from 1 Apr 2026;
  closing auction for F&O stocks from 3 Aug 2026 (basis measurement break); ban penalty schedule; two Indian SSF-mispricing papers to read.

- **Second pass (28 Oct 2026):** archived plan v1/v2.0/v2.1 in `plan/archive/` + REMOVED_ITEMS_REGISTER.md (user: keep all past
  plans and deletions). Closed open checks (§I of 07_fact_check): STT 2026 confirmed by NSE circular; FutEq ban test from 1 Oct 2025
  confirmed by NSE Clearing FAQ (saved as references/22); MWPL was monthly pre-reform; FutEq OI published pre-reform; short-selling
  eligibility formally limited to F&O securities; AMFI arbitrage series from mid-2018. Read in full: #20 Shankar–Sankar–Kiran Kumar
  2015 (SETAR bands, both bounds negative, 28 bp; no ban) and #21 Nandan–Agrawal–Jindal 2015 (weak) → notes_batch6. Found closest
  competitor: Saurav–Srivastava–Agarwalla (2026 SSRN) on SSF basis around earnings & short-sale constraints — to read.

- **Model C written (28 Oct 2026, "go ahead")**: tried to obtain Saurav et al. 2026, Gagnon 2018, Brennan–Schwartz 1990 — all
  paywalled/blocked (abstracts only; user to fetch via IITB library). Verified STT 2023 step and NSE theoretical-settlement rule.
  Installed TeX Live + numpy/matplotlib in container. Wrote `models_src/modelC/` (tex, verify script, figs) and
  `BSP_Model_C_Constrained_Arbitrage_India.pdf` (15 pp, 11 propositions, H1–H9 map with falsifiers). All numerical checks pass
  after correcting the level-effect proposition (first version failed: mean-zero spillover cannot shift the mean).

- **User (28 Oct 2026):** nothing shared with guide since the project doc; next deliverable = ONE progress-report PDF (incl. 3-pp
  theory version), but only after MORE progress. Guide-facing docs must contain no internal references (rule saved in 06).
  Asked: "can we just work with data without modelling?" → answered: possible in principle (design-based empirics), but keep the
  existing model as is (guide asked for it; it already changed the design: MWPL-instrument invalid, settlement-price trap,
  ambiguous level sign, inventory-dependent thresholds, STT/tax confound) and do no further theory unless data demand it.
  From now on mostly data.
- Model document made guide-safe (no Model A/B/C labels, audit, internal paths, reading-status notes).
- **Data pipeline started** (`data_pipeline/`, README documents sources/formats): NSE archives reachable from container.
  combineoi (MWPL, OI, FutEq OI post-reform, next-day ban flag) + fo_secban downloaded for 2010–2026 (running);
  prices (futures rows, options summary, cash EQ/BE/BZ, MTO delivery) for 2015–2026 (running; resumable).
  Raw data in data/raw (git-ignored). Draft pre-analysis plan written: `plan/pre_analysis_plan_draft.md` (blind; to be tagged pap-v1).

- **Data error checks (28 Oct 2026):** panel builder fixed for (i) 107 combineoi files with 2-digit-year dates (were silently
  dropped), (ii) NSE misdated files (combineoi_02112012 holds 5 Nov data; combineoi_02102015 holds 1 Oct; secban 19 Feb 2014 says
  19 Mar; secban 25 Aug 2014 says 26 Aug) → dates now taken from file names and inner-date mismatches dropped, (iii) trailing
  commas in secban symbols, (iv) a date-format bug in the flag-vs-ban-list check. After fixes: 99.5% of 'No Fresh Positions'
  flags match next-day ban lists (2010–2020 partial run). Known gap: 13 combineoi files 1–19 Jun 2012 corrupt at source
  (re-download byte-identical); pre-sample only.

- **Ban/MWPL panel built (data/processed/, 2010-02 → 2026-10-27; 4,120 days, 473 symbols).** Extra fixes: NSE bundled
  several days' CSVs into the 1–2 Jul 2025 zips (now all members read; 30 Jun & 2 Jul 2025 recovered); 1 Oct 2015 data sits in
  the 2 Oct 2015 file (reassigned); precision bug from float_format caught and fixed (MWPL is 9 digits). Flag vs next-day ban list:
  11,753/11,771 agree (99.85%); residuals = NSE misdated files 2014, corrupt Jun 2012 files, 23 Mar 2020, 23 Jan 2024 IRCTC.
  Universe = futures bhavcopy STF symbols exactly (145 on 1 Jan 2015; 166 on 1 Jan 2016).
- **Treatment-side facts (data/processed/descriptives.txt; figs in reports/figs):** main sample 2015–2026: 1,789 ban spells,
  9,414 ban stock-days, 141 stocks; spells median 4 days (mean 5.2) up to Sep 2025 vs median 9 (mean 9.3, n=44) from Oct 2025;
  entry rule (util > 95% day before) holds in 99.2% of spells, exit rule (util ≤ 80% on last day) in 99.5% → 80% exit confirmed in
  data. MWPL changes cluster in Feb/May/Aug/Nov (quarterly free-float updates). COVID halving: 61 stocks halved in files dated
  20–27 Mar 2020 (28 on 20 Mar, i.e. effective 23 Mar), 70 doubled back in the 26 Nov 2020 file. 1 Oct 2025: all 208 stocks' MWPL
  fell; median ratio 0.73; 17% at the floor (0.5), 48% at 15% FF (0.75). Ban stock-days peak 2017 (1,586) and 2024 (1,656).
  Utilisation density smooth through 95% pre-reform (no visible bunching; formal test pending).

- **Prices/basis (in progress):** price download 2015→2026 running (resumable). Known source gap: F&O bhavcopy 30 Mar 2021
  missing at NSE (all URLs 404). Rates: FRED INDIR3TIB01STM (3M interbank, monthly, from Nov 2011) + IRSTCI01INM156N (call money);
  FRED needs curl (Python connection dropped). Corporate actions: NSE API works without cookies; 28,251 records 2014–2026;
  dividend regex must require the word 'dividend' ('sub-division' = split). `build_basis.py`: futures VWAP needs lot size —
  legacy files lack it → gcd of OI/ΔOI per contract, snapped to a multiple using value/(contracts×mid) because lots change
  mid-contract (splits/revisions; raw gcd failed for ~2.5%); after fix 99.7% of VWAPs inside [low, high]. Test run 2015–2023:
  near-month usable stock-days 363k; basis median ≈ 0–9 bp/yr, p10–p90 ≈ −40 to +30 bp; |m| shrinks toward expiry; theoretical-
  settlement days ~0% for near-month (2.4% of next-month rows have zero contracts). No ban linkage done (blind).

- **Progress report drafted (28 Oct 2026, user request):** `progress_report_src/progress_report_oct2026.tex` →
  `BSP_Progress_Report_Oct2026.pdf` (one PDF for the guide; main text ~9 pp + full model as Appendix A via pdfpages).
  Sections: summary; refinements (scope table, corrected institutional facts, design changes); 3-pp theory summary; data built
  (sources, checks, ban facts table/figures, MWPL shocks, basis measure); pre-specified tests table; plan (ordered, no dates);
  questions for the guide. Style rules applied: no em dashes (also removed from model doc), plain first-person language, no
  internal references, AI-phrase scan clean. Basis numbers are macros (\basisN etc.) filled from the full basis run.
  The older Sep-28 progress report (never sent) is superseded but kept.

- **Price data complete (2015-01-01 → 2026-10-27):** 2,916 trading days with futures+cash+delivery; only gap 30 Mar 2021 (F&O
  file missing at NSE). Trading days match the MWPL panel exactly (2,917). **Basis panel built** (`data/processed/basis_panel.csv.gz`,
  74 MB, git-ignored, rebuild with build_basis.py): 1.65 m futures rows; F_vwap inside [low, high] 99.77% (2.0% of legacy rows needed
  lot snapping); all futures rows match cash. Near-month usable (≥5 contracts) 531,007; CLEAN sample (no dividend/other corporate event
  in contract life) 499,682: median +1.2 bp, p10 −33.0, p90 +26.1, |m|>200 bp 0.65% (mostly distressed stocks: JETAIRWAYS, DHFL,
  YESBANK, IDEA, JUSTDIAL…; kept). Stable across legacy→UDiFF switch. Errors found: (i) non-dividend events (e.g. NTPC bonus
  debentures 20 Mar 2015, −6% basis) → `event_in_life` flag (0.9% of rows); (ii) ex-date dividend adjustment over-corrects
  (+9.7 bp vs +1.1 bp; unadjusted −48.8) → likely look-ahead on unannounced dividends; flag/announcement-date adjustment needed.
  Nifty implied repo (UDiFF period, F_close vs UndrlygPric, which equals cash close within 2 bp) swings 3–8% with July–Sep lows =
  dividend season; no clean validation without index dividends (to do: Nifty TRI vs price index).
- **Progress report finalised:** `BSP_Progress_Report_Oct2026.pdf` (25 pp: ~9 pp report + model appendix). Numbers filled from data.

- **User's F&O membership sheet (fno_pit_3.xlsx, from an earlier project) evaluated (28 Oct 2026):** 367 symbols × 2,463 dates,
  0/1, 1 Jan 2016 → 23 Dec 2025. Calendar: trading days only (no holidays); 4 weekend columns = genuine special sessions
  (1 Feb 2020 & 1 Feb 2025 budget Saturdays, 20 Jan 2024, 18 May 2024); MISSING the 5 Diwali muhurat sessions (19 Oct 2017,
  7 Nov 2018, 4 Nov 2021, 24 Oct 2022, 1 Nov 2024). Contains index underlyings (NIFTY, BANKNIFTY, FINNIFTY, NIFTYIT, MIDCPNIFTY,
  S&P, DJIA, FTSE, INDIAVIX…), 3 truncated symbols (MCDOWELL=MCDOWELL-N, TV=TV18BRDCST, NAM=NAM-INDIA) and a test symbol NSETEST
  (6 Nov 2023). After fixing those, it matches futures-bhavcopy STF membership EXACTLY (452,616 stock-days). Verdict: accurate
  but redundant (our futures-based membership covers 2015–Oct 2026 incl. muhurat days); used as an independent cross-check.
  It revealed 713 'Not available in NSE-F&O' placeholder symbols in combineoi → now restored from ISIN (204, all post-2012 ones);
  25 restored rows dropped on ISIN-change days. Ban facts unchanged.
- **Membership definition:** a stock is in F&O on day t if STF contracts are listed in that day's F&O bhavcopy. combineoi lists
  entrants one day early (limits apply to next day) and drops exits a day before the last expiry. PNBHOUSING had an MWPL row with
  OI = 0 for Aug–Dec 2019 without futures.
- **F&O events (data/processed/fno_events.csv):** 239 entries, 171 exits 2015–2026 (162 eligibility exits with continued cash
  trading); 21 symbol renames linked by ISIN (e.g. ZOMATO→ETERNAL, TATAMOTORS→TMPV, MCDOWELL-N→UNITDSPR); missing F&O file
  30 Mar 2021 bridged (it had created 156 fake exits/entries). Big batches: 45 entries 29 Nov 2024 (Aug-2024 criteria),
  34 exits 28 Jun 2019, 16 exits 28 Feb 2025.
- **1 Oct 2025 MWPL rebuilt from pre-reform data:** 15%-FF leg exact (85 stocks, median error 0.0%) → FF = old MWPL/0.20 confirmed;
  ADDV leg: actual exceeds NSE-only-delivery prediction by median 6.5% (BSE deliveries); use actual published MWPLs for intensity.
- **Announcements (data/processed/announcements.csv.gz):** NSE results API (`corporates-financial-results`, 2014 → Mar 2025) +
  Integrated Filing API (`integrated-filing-results`, paginated: use size=20000, check totalCount; from quarter ended Mar 2025,
  NSE/CML/2025/20). 89,452 events (symbol × quarter), 14,930 for F&O symbols (median 4/yr); 63% released after 15:30 → day 0 =
  next trading day. XBRL links kept → EPS/SUE feasible from free data (to do). Bug fixed: pre-2015 events had been mapped to the
  first 2015 day (calendar now from the 2010+ panel).
- Nifty TRI not available (niftyindices API refused); downloading daily Nifty close + trailing div yield (ind_close_all) for a
  Nov–Mar index-futures check.

- **PAP v1 written** (`plan/pre_analysis_plan_v1.md`; v0 archived). Primary family {H7, H8, H3, H6}; secondary: level effect,
  H9, RD, hysteresis, H2, H1, H4, H5. Power: 1,789 spells (44 post-reform), 233 entries / 158 eligibility exits, 7,910 F&O
  announcements (188 in bans). Tag `pap-v1` only after user OK (guide may want to see it).
- **Band estimator** `analysis/setar.py` (3-regime SETAR, grid search, trims) + `analysis/test_setar_simulated.py`: recovers a
  known TAR (−30/+15 → −29.1/+15.2) but NOT the cost band on model-simulated basis (inventory-dependent thresholds → −10/0 bp):
  fixed thresholds = average edges, not costs; PAP §5b adds state-dependent thresholds (lagged OI/MWPL) and edge *changes* for H3.

- **Nifty check done:** daily Nifty 50 close + trailing div yield (NSE ind_close_all; 2,908 days, 9 missing in 2015–16; three
  Apr-2023 files write dates month-first). Nov–Mar contracts: Nifty futures implied repo (incl. trailing yield) vs 3M interbank:
  monthly corr 0.47, mean gap +0.67 pp (≈ bias from full-year yield in low-dividend season); from 2021 implied ≈ 2 pp above →
  index-futures premium (economic, not data error). Report updated (data section + new subsection on F&O events, free float,
  results dates; plan step 1 now = AMFI + XBRL EPS). Report is 26 pp; no em dashes.

- **User asked to remove §7 'Points on which I would value your guidance' from the report** (done; summary line adjusted; the
  removed text is kept in `progress_report_src/removed_guidance_questions.tex`; the user will raise the questions personally).

- **End of session (28 Oct 2026):** user decided to WAIT for the guide's reply before tagging `pap-v1`. Asked to save
  everything → wrote `memory/08_handoff_next_session.md` (full state, rebuild recipe, numbers, data errors, artefact map).
  User could not see new files on GitHub: all work is on branch `claude/compassionate-rubin-s9gny2` (19 commits ahead of
  `main`, which has only the initial commit); explained; no PR created. Removed committed __pycache__ files; ignored them.

- User opened and merged PR #1 (branch → main, merge commit 65ef0e3); verified main has all files. Branch restarted from main.

## Open threads (current; older lists superseded)
- Waiting: user sends the progress report; guide's reply (framing, theory depth, TAR/STAR, test plan) → then tag `pap-v1`.
- Confirm guide's name spelling (Chaubal).
- Library full texts: Saurav–Srivastava–Agarwalla 2026, Gagnon 2018, Brennan–Schwartz 1990.
- Blind-safe work available: AMFI arbitrage AUM; XBRL EPS (SUE); announcement-aware dividend adjustment; SLB data; cash-universe
  delay/VR; state-dependent-threshold estimator; density test at 95%.
- Optional (user go-ahead needed): fix project-document and literature-review errors listed in memory/04.
