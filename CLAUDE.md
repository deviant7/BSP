# CLAUDE.md — BSP project memory (read this first, every session)

This repository is Prince Kumar's (Roll 23B3032, BS Economics, IIT Bombay, 2023–27) Bachelor's thesis project
(EC 495 Stage I, 6 cr, Sem 7 → EC 497 Stage II, 12 cr, Sem 8). Guide: **Prof. Aditi Chaubal** (Economics; non-linear time series).
Topic: **Limits to Arbitrage in the Indian Equity Market** — how strongly do trading costs, short-sale constraints, arbitrage
capital, arbitrage risk and position limits bind in Indian equities, with India's MWPL "F&O ban" (reduce-only trading for
everyone once market-wide OI > 95% of MWPL, until 80%) as the sharpest lens. Public NSE data; bans 2010–2026, prices 2015–2026.

## START HERE
**Resuming? Read `handoff/16_resume_here.md` first** (where the last session stopped, rebuild list, next steps), then
**`handoff/00_START_HERE.md`** — the complete continuity brief (reading order, rules, current state, next steps, theory,
test plan, data pipeline, numbers, facts, literature, repo map, environment, open issues, maintenance protocol).
Read all of `handoff/` in the order it gives before doing substantive work.

## Standing instructions from the user (durable)
- **Keep continuity in two layers, regularly.** After any meaningful step (a decision, a new document, a finding, a user
  correction, a result): (1) update `memory/` and append to `memory/05_session_log.md` (the assistant's own notes);
  (2) update the relevant files in `handoff/` and add a line to `handoff/CHANGELOG.md` (the brief any new chat/model can be
  pointed to); then commit and push to `claude/compassionate-rubin-s9gny2`. The container is ephemeral; only what is
  committed survives. Protocol: `handoff/15_maintenance_protocol.md`.
- Thorough, unbiased, academically rigorous work; read primary sources, not just notes; flag errors honestly.
- No timelines; project = limits to arbitrage broadly (the ban is one lens); keep every past plan and deletion
  (`plan/archive/`, `REMOVED_ITEMS_REGISTER.md`); guide-facing documents have no internal references, no em dashes, no
  AI-sounding phrases; `docs/` documents the final form only (no history). Full list: `handoff/02_people_rules_and_working_style.md`.

## State in one paragraph (9 Nov 2026)
Theory done and verified (`BSP_Model_C_Constrained_Arbitrage_India.pdf`, `models_src/modelC/`). Data built and audited
(`data_pipeline/`, `data/processed/`, `docs/10_data_quality_audit.md`); SLB and AMFI arbitrage-fund series added 7 Nov.
The guide received the October progress report, liked it and gave the go-ahead. Pre-analysis plan `plan/pre_analysis_plan_v1.md`
frozen as git tag **`pap-v1` at 85dac3a** (on GitHub). Tests run exactly as the plan specifies; every open detail was
written into its §11 before each run (C1-C15), exploratory additions in §11.2. **All primary tests (+ Holm) and all
secondary tests are done** (results: `docs/14_results.md`, summary §14.16; `handoff/04_current_state.md` §4.7-4.10).
Band-estimation chapter (`docs/15`) and constraint index (`docs/16`) done 7 Nov. **Write-ups done 7 Nov:** thesis draft
(`thesis/`, `BSP_Thesis_Draft_Nov2026.pdf`) and first-results report for the guide (`BSP_First_Results_Nov2026.pdf`,
**not sent**; send only on the user's go-ahead). Digest of all findings: `memory/09_findings_digest.md`. **8 Nov:** remaining master-plan items done (spurious bans, placebos, COVID restoration; PAP §11.15, `docs/14` §14.17) and a deep audit of the whole project (`handoff/04_current_state.md` §4.15: full rerun reproduces every output; the constraint index's bad-news asymmetry is a size effect, all write-ups corrected). **9 Nov:** final thesis built: `BSP_Thesis_Final_Nov2026.pdf` (source `thesis/`, design `thesis/bspstyle.sty`, figures `analysis/thesis_figures_final.py`). Presentation deck `BSP_Presentation_Nov2026.pptx` (37 slides, consulting format of the user's reference decks; `deck/build_deck.js`, `analysis/deck_figures.py`). Academic backup deck (Beamer): `BSP_Presentation_Academic_Nov2026.pdf` (`beamer/main.tex`, `analysis/beamer_figures.py`). Short thesis for quick readers: `BSP_Thesis_Short_Nov2026.pdf` (50 pp; `thesis_short/`, reuses the main thesis style and figures; the full thesis stays the version of record). **10 Nov:** the guide read the short thesis and asked for a paper-style, reader-focused **Stage I (BSP1)** version; built in `BSP1/` (report `BSP1_Report_Nov2026.pdf`, 39 pp; consulting deck 37 slides; Beamer deck 49 pp; split, design and rebuild in `BSP1/README.md`). Next: the user's review of the BSP1 files. All work up to 28 Oct 2026 is on `main` (PR #1); later work reaches `main` only through a new PR
when the user asks.

## Folders
- `handoff/` continuity brief · `docs/` final-form documentation · `memory/` assistant notes (05 = session log)
- `plan/` master plan v2, frozen PAP, archive + removed-items register
- `data_pipeline/` scripts + README · `data/processed/` outputs (raw data and basis panel git-ignored; rebuild per `docs/12`)
- `analysis/` estimators, simulated-data tests, audit scripts · `models_src/` model sources · `references/` papers + notes
- Root PDFs: **final thesis `BSP_Thesis_Final_Nov2026.pdf`** (+ short version `BSP_Thesis_Short_Nov2026.pdf`), **decks `BSP_Presentation_Nov2026.pptx`/.pdf (consulting) and
  `BSP_Presentation_Academic_Nov2026.pdf` (Beamer)**, project document (guide has it), Oct 2026 progress report (sent),
  current model, earlier thesis draft, first-results report (not sent, not maintained); superseded Models A/B, Sep 28 note
  and literature review are internal and kept. User-supplied templates and design references are also in the root.
- **`BSP1/` Stage I report (paper style) and decks (current deliverables for EC 495)**; `thesis/` final thesis LaTeX (`bspstyle.sty` design); `thesis_short/` 50-page short version; `deck/` consulting deck generator; `beamer/` academic deck;
  `memory/09_findings_digest.md` = every result in one place; `memory/10_reread_findings.md` = last full re-read.

## Tooling notes
- `pdftotext` for most PDFs; `1_shleifer_vishny_limits.pdf` needs OCR (tesseract). `pandoc` reads the .docx.
- LaTeX sources exist for all generated PDFs; rebuild rather than hand-edit PDFs. More in `handoff/13_environment_and_tooling.md`.
