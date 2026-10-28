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

## Open threads
- Finish downloads → build panels → treatment-side descriptives (ban spells, rule checks, MWPL shocks, utilisation density) →
  fill PAP numbers → build basis series (VWAP-based) + Nifty validation vs Nandan et al. → tag PAP → then progress report
  (one PDF, guide-facing, incl. 3-pp theory).
- User to review Model C (guide-safe now). Get full texts of Saurav et al. (2026), Gagnon (2018),
  Brennan–Schwartz (1990) via IITB library and check Model C against them. Estimator-on-simulated-data exercise.
- Next steps per plan v2 §12: Phase 0 fact checks → corrected model + simulation → send guide model + 1-page note.
- Guide's response on the revised framework (she has seen only the project doc).
- Fix project doc (short-selling line, "relaxations", timeline with theory stage).
- Fix lit-review / notes / reference-index errors (listed in 04) — awaiting user go-ahead.
- Verify 80% ban-exit rule and historical 30× volume MWPL leg from NSE circulars.
- Data feasibility: ban list archive depth, combined OI files back to 2015, option settle-price quality, EPS source.
