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

## Session 5 Nov 2026 (new session; context re-gathered)
- Container persisted: data/raw (1.2 GB) and basis_panel.csv.gz still present; no rebuild needed. Re-read CLAUDE.md, memory 01–08,
  plan v2, PAP v1, removed-items register, both conversation logs, reference index + notes batches 1–6, the guide-facing report,
  model C (all propositions), all data-build reports. Re-ran verify_modelC.py (ALL PASS) and test_setar_simulated.py (same
  results); all processed datasets load (panel 752,037 rows; ban days 11,758; spells 2,184; membership 534,712; events 410;
  announcements 89,452; basis 1,066,167). No `pap-v1` tag; origin/main unchanged (65ef0e3).
- Found and fixed one stale number in the guide report: the year table had been generated before the placeholder-symbol fix;
  2017 'F&O stocks (avg per day)' is 200, not 201. Table + report figures regenerated, report PDF rebuilt (26 pp). All other
  report numbers verified against current data.
- Unknown at session start (ask user): was the report sent? has the guide replied? guide's name spelling?

- **User (5 Nov):** report WAS sent; guide liked it and gave the go-ahead for further work; name spelling confirmed "Chaubal".
  Asked: are the 3 library papers needed? (answered: not blocking; Saurav et al. first, for positioning only). Asked for a
  `docs/` folder documenting the FINAL project form (not history), thorough, for non-experts, finalized items only; and an
  audit of the data collection before moving on.
- **Data audit (5 Nov), scripts in `analysis/audit/`:** coverage of every raw source vs the trading calendar; duplicates;
  legacy->UDiFF continuity; combineoi OI vs bhavcopy OI; corporate actions; results; rates; Nifty. Findings:
  1. secban list missing at NSE for 6 May 2025 (404) and misdated-only for 19 Feb / 25 Aug 2014 -> ban days were missing and
     one spell was split. FIX: impute (prev-day No-Fresh flag + in ban on t-1 and t+1), `source=imputed` (7 stock-days).
     Now: 2015-26 spells 1,788 (was 1,789), ban stock-days 9,416 (was 9,414); entry/exit rule checks 99.4%/99.7%;
     flag->list agreement 11,753/11,764.
  2. FRED 3M rate ends Sep 2026 -> all Oct 2026 basis rows had r=NaN. FIX: carry last value forward max 2 months,
     `r_filled` flag (7,225 rows). Clean near-month sample now 503,170 (median 1.2, p10 -33.0, p90 26.2 bp).
  3. combineoi OI = bhavcopy stock fut+opt OI on 95% of stock-days; mismatches = expiry days (bhavcopy still counts expiring
     contracts) + Apr 2021 (~2-3% gap all stocks) + small subsets in early 2015, Feb 2016, Feb 2020. combineoi is the file NSE
     uses for bans -> kept as authoritative; documented.
  4. Nifty index file: 9 days missing at NSE (2015-16) -> validation series only; documented.
  5. RESULTS DATES (important): legacy results API misses ~10% of F&O stock-quarters pre-2024 (26% for Jun-2022 quarter),
     AND its timestamps are often later re-filings: vs board-meeting dates, release = meeting day 55%, +1 day 29%, >=6 days
     12%; in 2017-18 ~90% are >=2 days late (e.g. HINDUNILVR Jun-2018: meeting 16 Jul, feed says 3 Aug). Spot checks with
     the corporate-announcements API ("Financial Result Updates") show the true first release on the meeting day, often in
     market hours. FIX in progress: download board meetings (done, data/raw/boardmeetings, 312 half-month files) and all
     "Financial Result Updates" announcements 2014-2026 (data/raw/resultupdates, 4-day windows) and rebuild day 0 from the
     earliest release.
  - Checks that passed: no duplicate futures/cash rows; UDiFF switch 8 Jul 2024 continuous (181 stocks both sides; UDiFF
    contracts are in `qty`, handled); empty delivery markers all on holidays; corporate-action counts stable, no caps;
    expiry weekday switch to Tuesday from 30 Sep 2025 visible; every stock-day has a near contract.
- **docs/ started:** 01 concepts, 02 question, 03 institutions, 04 theory, 05 hypotheses, 06 sources, 07 construction,
  08 variables (written while downloads ran). Still to write: README, 09 design, 10 audit, 11 facts, 12 reproducibility,
  13 references.
- **Results-date fix completed (5 Nov):** downloaded 'Financial Result Updates' announcements 2014–2026 (1,173 four-day
  files, 74,255 records; period parsed from text for 99.2%). New build_announcements: release = earliest of announcement and
  filing; board meetings (purposes containing 'result', status notices excluded, latest intimation) fill gaps and override
  filing-only times >1 day after the meeting (747 cases); every record mapped to the symbol trading on the event date via
  cash-bhavcopy ISIN history (NSE feeds label old records with CURRENT symbols, e.g. CADILAHC under ZYDUSLIFE — this alone
  was most of the 10% coverage gap). Result: 94,071 events; F&O coverage 98–100% per quarter (median 99.1%); timed release on
  meeting day 90.2% / next day 6.5%; 8,594 F&O events (180 on ban days), timing known 99%. vs old build: 51.5% of the 7,910 old
  F&O events moved EARLIER (36% by >=2 days), none later. Remaining gap 86 stock-quarters = BSE-only listings (MCX, Abbott,
  Nestle pre-2023). Unknown-time rule: day 0 = next trading day after the release date.
- Other checks: combineoi symbols vs F&O bhavcopy membership agree on 99.97% of stock-days (combineoi lists new stocks a day
  early). Report table `reports/tables/ban_by_year.tex` regenerated (1,788 / 9,416); the sent PDF was NOT rebuilt (it is the
  record of what the guide received).
- **docs/ completed:** README + 01–13 (concepts, question, institutions, theory, hypotheses, sources, construction,
  variables, design, audit, facts, reproducibility, references). Final form only.
- **PAP:** pre-tag revisions (a)–(d) written into the status block; power counts updated; register changelog updated;
  plan v2 Phase 2 status updated; data_pipeline/README completed. **Tagged `pap-v1` at commit 85dac3a** (local; tag push
  refused by the session's git proxy, HTTP 403 → user to create the tag on GitHub; commit itself pushed).
- **User (5 Nov): continuity in two layers.** (1) memory for the assistant; (2) a very extensive `handoff/` folder any new
  chat/model can be pointed to. Created `handoff/` (00_START_HERE with reading order, rules, bootstrap prompt and self-check;
  01 overview; 02 people/rules/style; 03 history and decisions; 04 current state; 05 detailed next steps; 06 theory with
  all propositions; 07 frozen test plan + implementation notes; 08 data pipeline deep dive (scripts, data dictionary,
  44-item quirk catalogue, NSE access); 09 key numbers; 10 institutional facts with status; 11 literature; 12 repo map;
  13 environment; 14 open issues/risks; 15 maintenance protocol; CHANGELOG). CLAUDE.md rewritten to point to handoff/ and
  state the two-layer rule; memory/08 marked superseded. Verified while writing: basis-panel OI/ΔOI in shares (both formats);
  pyfixest installable.

- **Primary tests run (5 Nov, after `pap-v1` and the §11 C1–C5 clarifications committed in c6b1701):**
  Sample (analysis/samples.py): 486,040 chosen-contract stock-days, 371 stocks; next contract used 18.5%; 8,851 ban days.
  Inference: pyfixest two-way FE + two-way clustered SE, validated on simulated panels (analysis/test_inference.py).
  - **H8** (analysis/output/h8_results.txt): in [0.80,0.95) zone, Ban → log futures contracts −2.00 (se 0.11), log cash
    shares +0.073 (0.027), delivery share +0.041 (0.0045); p_H8 ≈ 0. Identity R=(ΔOI+V)/V on ban days: mean 0.42 (pre-set
    reading FAILS). Exploratory: break between 6 and 24 Mar 2020: before mean 0.86 (no R<=0.01), after mean 0.10/median 0.012;
    non-ban R ≈ 1.01 all years; chg_oi = ΔOI levels. Cause unknown (likely intraday round trips tolerated before) → ask user.
    Futures volume effect −0.97 before vs −2.72 after. Logged in PAP §11.2.
  - **H7** (h7_results.txt): REJECTED. δ_up = −0.089 (t −2.4), δ_lo = +0.081 (t +2.7): in bans rich futures revert FASTER,
    cheap futures SLOWER (opposite of the model); p_H7 = 1. Robust: fixed ±25 bp, SETAR thresholds, state-dependent, no
    imputed, no r_filled, rel. repo; close-based δ_up ≈ 0; unwinsorised δ_up +0.077 (t 1.6). After an expiry inside the
    spell δ_lo + δ_lo_exp = −0.83 (much faster downward reversion; opposite of 'floor wears out'). Post-reform n.s.
    Candidate readings for discussion (not claimed): closing pressure by speculative longs dominates (long liquidation
    pushes futures down); noise in thin-trading VWAPs; contract-level selection (≥5 contracts on ban days).
  - **H3** (h3_results.txt): mean Δq80 2023 −2.12, 2024 +6.42, 2026 +7.44 bp (ordering YES); p_H3 = 1.8e-24 (stock-clustered,
    as pre-specified). Placebo (pre-specified): sd 7.4 bp across 30 pseudo-events; 2024 rank 0.10, 2026 0.067 → stock-only
    clustering understates uncertainty (common date shocks); shifts exceed cost changes and d50/d20 also move (level shift).
  - H6 not run: needs (i) split/bonus adjustment (NSE PREVCLOSE is NOT adjusted: TATASTEEL split 28 Jul 2022 prevclose 959.4,
    close 100.35); (ii) market cap: no free NSE file found (PR zips have none); plan = shares from XBRL paid-up capital / face
    value; (iii) §11 dated entry for H6 details before running.

- **User (5 Nov, later): plans fine; do deep research on the three open questions; get H6 data (else Prowess via college);
  keep memory, docs and handoff updated.**
- Research results:
  1. **March 2020 break = enforcement change (resolved, primary sources):** SEBI PR 18/2020 (20 Mar 2020) → ICCL/BSE notice
     20200322-2: from 23 Mar 2020 ban violations identified from PEAK INTRADAY positions (before: end of day); PR 59/2020
     keeps it "till further directions"; from 1 Oct 2025 NSE Clearing 119/2025 entity EOD FutEq vs base position. Ban-day R
     median 0.871 / 0.011 / 0.193 (Oct–7 Dec 2025) / 0.357 (8 Dec 2025 →). Saved references/23 (PR 59/2020 pdf), 24 (ICCL
     notice text). Also confirmed in data that the market-level FutEq trigger applies from 1 Oct 2025 (805 gross>95%
     stock-days Oct–early Dec 2025 without ban); Angel One's "8 Dec 2025" = broker-side entity checks (unresolved).
  2. **H7 exploratory diagnostics** (analysis/h7_diagnostics.py): not noise (stronger on liquid days); era split: EOD era
     δ_up +0.016 n.s., δ_lo +0.126; intraday era δ_up −0.201, δ_lo −0.120; faster upward reversion concentrated in first
     4 days of spell (−0.163 vs −0.008). Reading (post hoc): blocked new-exposure demand at ban start (P5/B2) removes the
     rich-futures pressure; H7 derived from P4 alone. Legs regression too noisy to separate futures vs cash.
  3. **H3 calibration:** avg Δq80 (2024, 2026) exceeded by 4.6% of placebo pairs; width 23.4%; q80−median 27.4% →
     mostly a common level shift; stock-only clustering over-rejects (Kolari–Pynnönen 2010). No academic ban study found.
- docs/14_results.md created (H8, H7, H3 with exploratory parts marked); docs/03 gained the enforcement-regime row and the
  2020 penalty; docs/13 refs added (SEBI PR 18/2020, 59/2020, ICCL notice, Kolari–Pynnönen). PAP §11.2 extended.

- **H6 inputs built (5 Nov):** (1) `data_pipeline/build_returns.py`: split/bonus/dividend-adjusted returns, 5.33 m
  stock-days, 3,723 stocks; factors match price jumps 99.6% (after MULTIPLYING same-day split+bonus records — first version
  took the max, 4.2% mismatches); listing days, rights/demerger/scheme ex-dates → NaN; 424 likely-missing CAs (price ratio at
  a standard split ratio) → NaN + inferred factor; ETFs and -RE symbols dropped; 448 jumps flagged. (2) AMFI half-yearly
  average market caps (18 PDFs, Jul–Dec 2017 → Jan–Jun 2026; `build_amfi_mcap.py`; parser handles wrapped rows and ISINs
  glued to names); matched 89–97% of NSE stocks by count, 95–99.8% by value; free-float check median 0.48, 99.5% plausible.
  (3) `build_mcap.py`: daily mcap = split-adjusted price × half-year share count; back-cast before Jul 2017 (3-year
  back-cast test: 82% within 10%); 94.7% of stock-days; 99.4–99.6% of event stocks. XBRL results only from 2018 (pre-2018
  links blank) and NSE shareholding API only from 2021 → not used. Prowess optional (verify pre-2018 back-cast).
- **PAP §11.3 C6 (a)–(k)** fixed and committed BEFORE estimation (dbdfcde, e9ba556): calendar-year CS design, anticipation
  1 year, covariates, delay D1, EAR/BHAR vs size-decile EW, bad = bottom EAR tercile per quarter, stacked DiD for drift,
  Bonferroni p_H6, price ≥ Rs 5 filter (penny tick artefacts: BHAR up to 8,190), winsorising.
- **H6 results (analysis/output/h6_results.txt):** entry delay ATT −0.109 (boot se 0.023, p 1.3e-6; SA −0.063 (0.019);
  leads −3/−4 ≈ 0; robust); entry bad-news drift −0.040 (0.018) = STRONGER drift (opposite); exit delay +0.053 (p 0.09);
  exit drift +0.014 (opposite, n.s.). p_H6 = 5.2e-6. Caveat: F&O entry selects on growth.
- **Holm (analysis/output/primary_family.txt):** H8 7.4e-41, H3 5.5e-24, H6 1.0e-5 rejected; H7 1 not rejected.
- docs updated: 06 (AMFI source), 07 (7.10 returns, 7.11 mcap, 7.12 H6 outcomes), 09 (H6 implementation), 10 (10.7
  returns/mcap checks), 12 (rebuild + tests), 14 (H6, Holm).

- **END OF SESSION 5 Nov 2026 (user: "Save everything ... pick up from exactly where we left off").** State: all four
  primary tests + Holm done (H8, H3, H6 rejected at 5%; H7 not, opposite sign); research on the open questions done
  (enforcement regimes; H7 diagnostics; H3 placebo calibration); H6 data from free sources (returns, AMFI mcaps; Prowess
  optional). Resume card written: `handoff/16_resume_here.md` (first actions, rebuild list of git-ignored files:
  data/raw 1.4 GB, basis_panel, returns_daily, mcap_daily, cache/*.pkl; pip install pyfixest; smoke tests; next =
  secondary tests in order: level effect → density test → RD → hysteresis → H9 → H2 → H1 → H4 (needs AMFI arbitrage AUM)
  → H5; each with a dated PAP §11 entry first). Working tree clean at the end; tag pap-v1 on GitHub.

## Session 7 Nov 2026 (new session; context re-gathered)
- User: "gather full context before we proceed ... use the conversations, chats, artifacts, memory files". Read CLAUDE.md,
  handoff 16 → 00 → 01–15 + CHANGELOG, memory 01/05/06 (02/03/04/07 known and current), PAP v1 in full (diff since tag =
  §11 additions only), docs/14, every analysis/output file, data_pipeline/README; the two chat logs had been read in full on
  5 Nov.
- Container unchanged: data/raw (1.4 GB incl. amfi_mcap), basis_panel, returns_daily, mcap_daily, cache/*.pkl present;
  pyfixest 0.60.0 installed. Smoke tests pass: h8_trading reproduces b = -2.0036; verify_modelC ALL PASS (figure PDFs
  rewritten with new timestamps only → restored); SETAR test -29.1/+15.2 and -10.4/-0.3.
- Consistency fixes (repo wins over handoff): 04 git/container/H6 row/status; 05 tag + market cap; 07 §11 contents;
  08 quirk 26; 09 primary numbers; 12 counts; 13 tools/sizes; memory/01 status (+ ADDV in quantity, not value);
  data_pipeline/README new builders. Not changed: PAP §1 table still shows pre-audit rule checks 99.2/99.5% (frozen text;
  current 99.4/99.7% in §8 and docs).
- User (7 Nov, second request): read ALL memory files and any other file that adds context before the level-effect test.
  Read in full: memory 01–08 (incl. the whole session log), plan v2, PAP v1 + v0 draft, removed-items register, model C
  ban section (Lemma, P4–P7), progress report tex as sent + removed guidance questions, reference index + notes batches
  1–6, both chat logs (re-read), docs 02/05/09/11, analysis code samples/inference/h7/h7_diagnostics/h8, handoff 00/03/04/
  16/CHANGELOG. Findings fixed: (1) H7 diagnostic "first 4 calendar days" = days 0–4 after spell start (code: dos <= 4);
  wording corrected in PAP §11.2 (dated note), docs/14, handoff/09; numbers unchanged. (2) notes batches 1 and 5 carried
  facts later corrected (30× leg, ADDV value, "relaxation", MWPL instrument, "no cash shorting") → correction boxes added
  (text kept). (3) memory/08 §6 marked pre-audit; handoff/16 last-commit pointer updated. No other inconsistencies found.
  Earliest history confirmed from the chat logs: a short proposal (BSP Proposal.docx, not in repo) went to the guide first,
  then the detailed project document; the guide asked for theory first; Models A/B were never sent.

## Open threads (current; older lists superseded)
- All four primary tests run + Holm (5 Nov). Next: secondary tests (level effect, H9, density test + RD, hysteresis, H2, H1, H4 needs AMFI arbitrage AUM, H5); optional Prowess check of pre-2018 market caps.
- Tag pap-v1 now on GitHub (refs/tags/pap-v1 → 85dac3a), created by the user, 5 Nov 2026.
- Library full texts: Saurav–Srivastava–Agarwalla 2026, Gagnon 2018, Brennan–Schwartz 1990.
- Blind-safe work available: AMFI arbitrage AUM; XBRL EPS (SUE); announcement-aware dividend adjustment; SLB data; cash-universe
  delay/VR; state-dependent-threshold estimator; density test at 95%.
- Optional (user go-ahead needed): fix project-document and literature-review errors listed in memory/04.
- User (7 Nov): "make sure the edits were correct and were wrong in the first place; do not assume". Re-verified each:
  (1) H7 spell-start wording: code `dos = (date - start).days <= 4`, spell start = first ban-list day (100%) → days 0–4
  (5 calendar days incl. start); old "first 4 calendar days" was imprecise → fix confirmed. (2) batch-5 box: 20% FF only
  confirmed (SEBI 2025/79 §5.2.1 + data); ADDV in quantity confirmed (NSE 119/2025, FAQ); **my item (3) was WRONG**: the
  in-ban trading rule from 1 Oct 2025 IS looser (SEBI 2025/79 §5.3 + Table 2: new delta-reducing contracts allowed) — only
  the package as a whole is not a relaxation → box rewritten; the 28 Oct reference-index note had the same error → dated
  correction appended; docs/03 and handoff/10 now state it; memory/07 §L. Item (4) MWPL instrument matches the model.
  (3) batch-1 box: short-selling framework checked against SEBI circular 5 Jan 2024 (saved references/25): all investors
  may short; naked barred; institutions no day trading; F&O securities eligible; "and SLB" was not in that primary →
  box now says SLB list is F&O-based per secondary sources. 2004 origin of the 30× leg could not be re-verified today
  (✔S). (4) memory/08 note reworded (not all §6 numbers changed).
- **Level effect run (7 Nov).** Treatment-side look first (C distribution: median +0.053, C<=0 only 8%; 1,201 spells with
  >=5 clean pre-days; 2,451 candidate control days). PAP §11.4 C7 committed (25bd744) BEFORE estimation, incl. a median
  split and continuous C. Code checked on synthetic data (recovers +10/-6). Results: 889 matched events; mean D -6.3 bp;
  C<=0 (30) +8.4 (10.9), C>0 -6.8 (1.8), diff p 0.083; median split p 0.025; slope p 0.0014 → signs as Prop. 6; basis
  recovers by ~day 7. Weak spots: same-day controls only → gradient n.s.; day -1 imbalance (treated 10 bp lower) and day -1
  dip. Exploratory (logged §11.2): baseline -10..-2 → -11.3, slope p 0.007; gap-adjusted -9.2, slope -3.5 (1.6).
  Post-reform 19 events, all C>0, -2.8. Consistent with H7 diagnostics (blocked new long demand at ban start).
  Next: density test at 95% (treatment-side), then RD.
- **Density test (7 Nov):** PAP §11.5 C8 committed first (3f7ffab). Key design point: literal population (all non-ban days)
  is mechanically discontinuous (absorption into ban) → main = one-step transitions from below 0.95. rddensity 3.0 /
  rdrobust 2.1.1 installed (pip). Result: no discontinuity (CJM p 0.86, robust); binned McCrary +0.31 shown (exploratory)
  to grow with bandwidth → boundary bias; CJM cluster-boot se 0.29 (limited power). No bunching; utilisation accelerates
  near 95%. Figure reports/figs/density_95.pdf. Next: RD at 95%.
- **RD at 95% (7 Nov):** PAP §11.6 C9 committed first (f96bca8). Mechanism jumps strong (futures -1.53, R -0.66, delivery
  +5.1 pp; cash volume none). Basis level -12.9 (p 0.02) but already -11.3 on the crossing day; same-day change -2.8 n.s. →
  RD cannot separate a ban level effect from the crossing pressure. Placebo 0.90 basis +24 at h 0.008 (degenerate). New
  insight: rising OI + falling basis before entry ⇒ maybe new SHORT futures demand; C cannot sign it → exploratory
  long/short build-up split (price direction with OI) for the level effect next.
- Build-up split (exploratory, 7 Nov): long build-up -7.9, short build-up -5.5 (diff n.s.); closing +8.4 (n 30). The in-ban
  fall is not specific to blocked new longs → the post-hoc "blocked long demand" reading of H7 is only partial.
- **Hysteresis (7 Nov):** PAP §11.7 C10 committed first (3e72a35). Ban +0.38 (0.81), p 0.64 with 5 lags; without lags -14.1;
  trading as H8; close-based +3.2 (p 0.001) → recurring VWAP-vs-close discrepancy on ban days logged in handoff/14.
  Post-reform -6.6 (2.8). Next: H9.
- **H9 (7 Nov):** PAP §11.8 C11 committed first (8484f59). A: upper-tail share rises with omega (slope p 0.019; step near
  0.75), lower tail/level flat → upper edge loosens (anticipation + pressure). B: 1 Oct 2025 intensity: first stage strong,
  U +0.061 p 0.11 (right sign, n.s.). C: quarterly resets n.s. Next: H2.
- **H2 (7 Nov):** PAP §11.9 C12 committed first (0a90154). Drift in bans: no evidence, very imprecise (Bbad +0.007, se
  0.034). Pre-EA basis outside bans lower before bad news (-2.0 bp, p 0.039; replicates Saurav et al. direction); bans
  uninformative. Cash-only vs F&O: drift larger both ways (good +2.4%) → general under-reaction, not bad-news asymmetry.
  Next: H1.
- **H1 (7 Nov):** PAP §11.10 C13 committed first. SLB data found (NSE SLBM_BC files) and built; discovered SLB covers
  non-F&O stocks (eligibility widened Jul 2013) → corrected docs 01/02/03, handoff 01/10, plan v2, notes batch 1, memory 07;
  sent PDFs keep old wording (handoff/14). Result: index +3.5 bp/sd on band width (p 0.002), size +2.5; persistence
  opposite; no within-stock effect; SLB activity wrong sign.
- **H4 (7 Nov):** AMFI monthly arbitrage-fund series built (Apr 2018-Sep 2026; two layouts; checks vs published figures
  pass). PAP §11.11 C14 committed first. Lagged flow -17.5 (p 0.11); first differences -20.6 (p 0.001); pre-2023 only.
  Next: H5. pip installs this session: rddensity, rdrobust, xlrd (statsmodels present).
- **H5 (7 Nov):** PAP §11.12 C15 committed first. VW short leg G3 - G1 +0.04% (p 0.57) → not supported; EW both legs
  stronger in small cash-only stocks (symmetric); momentum short leg fits (-0.51%). **All secondary tests done**; summary
  table docs/14 §14.16. Docs 06/07/12/13 updated (SLB, AMFI, rebuild steps, references). Handoff 00/04/05/09/16 + CLAUDE.md
  + memory/01 status updated. Next (needs the user's choice): band-estimation chapter (threshold/STAR; guide's area),
  constraint-index deliverable, write-up / first-results PDF for the guide (ask before sending).
- **CHECKPOINT (7 Nov, user request):** "update memory, documents and handoff with everything new ... safe checkpoint; then
  band-estimation chapter first, then remaining next steps". Updated: handoff 00 (date), 02 (verify-don't-assume,
  checkpoints, thoroughness), 03 (Phase 5 + new decisions), 06 (§6.7 empirical status per proposition), 11 (methods refs),
  12 (repo map: new scripts/data/ref 25/figure), 13 (§13.8 packages, SLB/AMFI URLs), 14 (§14.6 risks), 15 (checkpoint
  rule), 16 (self-contained checkpoint card + band-chapter plan); docs 08 (§8.4 friction index, §8.5 secondary measures),
  09 (secondary implementation), 10 (§10.9 SLB/AMFI checks), 11 (§11.6 SLB, §11.7 arbitrage funds); memory 02, 03, 04
  (empirical status of Model C; model SLB wording to fix), 06; data_pipeline/README. Next: band-estimation chapter.
- **Band chapter (7 Nov):** PAP §11.13 C16 committed first (8609699). Fast cumulative-sum SETAR (matches fit_setar3
  exactly) with wild-bootstrap linearity test and stock-cluster threshold CIs; ESTAR/LSTAR; observed-transition STR;
  per-stock; cost band (sources: NSE 1/2018 STT 0.1% physical settlement; stamp duty Jul 2020; NSE charges Oct 2024).
  Pooled band -34.5/+23.9 bp, nonlinear; threshold model best by BIC. Exploratory: period demeaning fixes 2026; IV check
  shows much daily reversion is VWAP noise (asymmetry in speeds not robust) → flag H7 IV check. docs/15 written.
  Next: constraint-index deliverable, H7 IV (exploratory), write-up.
- H7 IV (7 Nov, exploratory): opposite-sign result survives noise correction (2SLS delta_up -0.19, delta_lo +0.09). PAP §11.14 C17 committed (constraint index).
- **Constraint index (7 Nov):** PAP §11.14 C17 committed first. All-stock quarterly index published
  (data/processed/constraint_index_q.csv.gz; docs/16). Validation: delay +0.058 (within stock +0.032), |drift| +0.023,
  bad-news drift -0.008 vs good +0.001 (asymmetric, as predicted; no size control); within F&O the all-stock index is
  negatively related to band width (SLB component) → H1 F&O index is the one for the band. Next: write-up (ask user).
- **Docs first (7 Nov):** README main findings; docs/02 contributions (band chapter, index); docs/04 SLB wording; docs/12
  layout (thesis/). No em dashes in docs.
- **Thesis draft (7 Nov):** `thesis/` main.tex + ch1 intro, ch2 institutions, ch3 theory, ch4 data (+constraint index),
  ch5 band (H3, H4, H9, H1, costs), ch6 ban (H8, H7, level, density, RD, hysteresis, H2), ch7 eligibility (H6, H5, index),
  ch8 conclusion/policy; appA plan + log; appB data; appendix C = model PDF via pdfpages; references. New figures via
  analysis/thesis_figures.py. Compiled 52 pp, no overfull boxes; style scan clean. Root copy BSP_Thesis_Draft_Nov2026.pdf;
  thesis/main.pdf git-ignored.
- **First-results report (7 Nov):** progress_report_src/first_results_nov2026.tex → BSP_First_Results_Nov2026.pdf (5 pp),
  guide-facing, NOT SENT. Includes the two corrections to the October report (SLB wording; counts after dating results
  from first dissemination). Ends with two questions for the guide.
- **Memory save (7 Nov):** new memory/09_findings_digest.md (all results and numbers); handoff 03/04/05/12/16, CLAUDE.md,
  CHANGELOG updated.
- **END OF SESSION 7 Nov 2026** (user: "save every bit of context ... we will end the session and pick up next time").
  Final gap check of the context stores (CLAUDE.md; memory/01-09; handoff/00-16 + CHANGELOG; docs/; plan/ PAP §11 log +
  REMOVED_ITEMS_REGISTER + master plan; git history). Added: register changelog for 7 Nov; master-plan status note; handoff/07
  C16-C17; handoff/04 git commits and container additions; handoff/14 waiting-on-user list (review thesis + report, send
  decision, two questions for the guide, optional Prowess, unresolved 8 Dec 2025 date); handoff/16 rebuild commands for
  the write-ups; neutral pronouns for the user in handoff/memory. Next session starts with handoff/16 and memory/09.

## Session 8 Nov 2026 (new session; context re-gathered)
- Same container (data/raw, basis panel, returns, caches present); tree clean; remote = local (52f5dda); tag pap-v1 → 85dac3a.
  Packages present; smoke tests pass (H8 b = -2.0036; verify_modelC ALL PASS, figure PDFs restored).
- Read: handoff 16, 00, 01, 05, 07, 10, 11, 14, 15; memory 09 digest; master plan §8-9 and PAP; project-document section
  list; the rest was in context from 7 Nov. Fixed stale entries: handoff/01 pronoun; handoff/10 statuses (naked shorting P
  via references/25; 2004 origin of the 30x leg S); memory/04 (model WAS shown to the guide as the report appendix).
- Found master-plan items not yet done: (1) policy count of "spurious" (denominator- or measure-driven) bans before vs after
  Oct 2025 (plan §8); (2) placebos from plan §9 (index-only reforms, fake ban dates, non-F&O stocks); (3) COVID MWPL halving
  design (plan §6.4; PAP §4a treatment without a specified test); (4) peak-margin phase-in as a capital shock (plan §0);
  (5) thesis lacks a literature-review chapter (internal lit review PDF has known errors) and the policy chapter lacks the
  SEBI retail-loss framing (plan §8); appendix on the band-of-inaction derivation and a replication guide (plan §11) are
  thin. Optional: XBRL SUE; put-call parity. Waiting on the user: review of thesis draft and first-results report; send
  decision; library papers; Prowess (optional); go-ahead to fix the project document.
- **8 Nov: remaining master-plan items** (PAP §11.15 C18-C20 committed first, 1772cb9). Spurious bans: pre-reform OI-driven;
  post-reform reform cut bans ~73% vs old rule (simulation validated). Placebos: fake bans null; index-only and peak-margin
  dates in placebo range. COVID restoration: utilisation -0.21, bans -4.6 pp, U -0.068 (anticipation fits); halving
  confounded. docs/14 §14.17; handoff 04 §4.14, 05 Step 3c, 09. User (8 Nov): after these, a deep audit of the whole
  project, then the final write-up (user will specify mostly cosmetic changes); lit-review chapter from the existing
  review later.
- **8 Nov: deep audit of the whole project** (user request). Full rerun (`analysis/audit/rerun_all.sh`): all 28 scripts
  exit 0, outputs reproduce. New tests: CS ATT (-0.1007 vs -0.10) and level-effect code (+10/-6 bp recovered). Number
  check script: everything matches. Fixes: thesis ch4 "99.85%" (pre-audit figure); "audit" wording in thesis appendices;
  model PDF SLB wording (3 places; sent copy archived); **index bad-news asymmetry disappears with size-decile FE
  (-0.0007, se 0.0023)**: corrected docs/16, README, thesis abstract/ch1/ch4/ch7, report §7; delay survives (+0.036 log
  mcap; +0.028 with stock FE). PAP §11.2 entry logged. Both PDFs rebuilt clean. Lesson: check every cross-sectional
  "constraint" result against size before writing it up.
- **8 Nov END OF SESSION (user near usage limit).** Agreed plan for the next session, saved in handoff/16 ("PLAN FOR
  THE NEXT SESSION"): (1) finish content in the thesis only ("write-up" = final submission report; first-results report
  not updated further): §14.17 results, SEBI retail-loss framing, literature chapter from litreview_src after fixing its
  errors, optional appendices; (2) re-read every word of every file, artifact and memory to rebuild context; (3) user
  gives a LaTeX template zip (use only its first few pages) and a PDF whose body formatting they like; build the final PDF
  with many figures, no em dashes, no AI-sounding phrases.
- **9 Nov (new session): Part 1 of the agreed plan done.** User committed `IIT_Bombay_Unofficial_LaTeX_B_Tech_Project__BTP__Template.zip`
  and `Main_content_formatting.pdf` (root) for Part 3; deliverable = final thesis PDF only. Thesis additions: ch5 (index-reform
  placebo in costs; peak margins in capital; spurious-bans table + COVID restoration in position limits; summary), ch6
  (placebo section: fake bans null), ch8 policy rewritten (SEBI PR 22/2024 retail losses verified from references/12; 2024/132
  cites retail participation; 2025/79 para 4.2 "spurious" bans; reform cut ban days ~3/4), ch1 (outline + finding 4),
  new ch_literature.tex (Related literature; built from memory/02 verified digest, known lit-review errors fixed: SYY
  double sorts, Harshita BHAR/price-scaled SUE, Roy-Chakraborty spot corrects, Sehgal IVOL reversed, DSSW market-wide
  caveat, Loewenstein-Willard, venues), 13 references added, appB reproducibility note. Found and fixed: halving was 60
  stocks in 20-27 Mar files + 1 on 29 Apr (docs/08, 10, 11 said 61 in March files). Thesis 61 pp, clean build.
- **9 Nov: Part 2 (re-read) and Part 3 (final build) done.** Re-read findings in memory/10_reread_findings.md (small doc
  fixes; all thesis numbers match outputs). Final thesis: `BSP_Thesis_Final_Nov2026.pdf` (78 pp), source `thesis/`:
  - `bspstyle.sty`: single-column academic page in the design language of `Main_content_formatting.pdf` (TeX Gyre Heros +
    sfmath; ruled, numbered, letter-spaced section heads with blue numbers; italic chapter leads; exhibit-style captions:
    grey "FIGURE n.m" label, bold takeaway title, grey subtitle via \exsub, source line via \exsource; tables with \thd
    headers, blue bold first column, grey \rowrule; ruled footer; key-number strip \statstrip/\stattile).
    Chose single column over the PDF's two columns because the user asked to keep it academic (equations, wide tables).
  - `frontmatter.tex`: template's first pages adapted (title page with IITB logo, Report Approval, Certificate,
    Declaration, Acknowledgements, Abstract (abstract.tex, with a key-number strip), Contents, List of Figures, List of
    Tables, Abbreviations, Symbols). Degree written as "Bachelor of Science in Economics", Department of Economics,
    November 2026. Acknowledgements are a short neutral draft: the user should rewrite them in their own words.
  - Model appendix is now native LaTeX (`appC_model.tex`, generated from the model source; tense updated; H6 row aligned
    with the plan). Old main kept in `thesis/archive/main_draft_nov7.tex`.
  - 26 figures from `analysis/thesis_figures_final.py` -> `thesis/figs/` (Liberation Sans; palette #1F4E9A/#C0504D/greys,
    validated with the dataviz validator) + one TikZ design diagram; 12 restyled tables. Ch4 basis description now uses
    the analysis sample (median +1.1, p10 -39.1, p90 +26.8; written to analysis/output/thesis_figures_stats.txt).
