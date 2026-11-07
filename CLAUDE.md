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

## State in one paragraph (7 Nov 2026)
Theory done and verified (`BSP_Model_C_Constrained_Arbitrage_India.pdf`, `models_src/modelC/`). Data built and audited
(`data_pipeline/`, `data/processed/`, `docs/10_data_quality_audit.md`); SLB and AMFI arbitrage-fund series added 7 Nov.
The guide received the October progress report, liked it and gave the go-ahead. Pre-analysis plan `plan/pre_analysis_plan_v1.md`
frozen as git tag **`pap-v1` at 85dac3a** (on GitHub). Tests run exactly as the plan specifies; every open detail was
written into its §11 before each run (C1-C15), exploratory additions in §11.2. **All primary tests (+ Holm) and all
secondary tests are done** (results: `docs/14_results.md`, summary §14.16; `handoff/04_current_state.md` §4.7-4.10).
Next: the band-estimation chapter and the write-up (`handoff/05_next_steps.md` Step 3b, 5); ask the user before sending
anything to the guide. All work up to 28 Oct 2026 is on `main` (PR #1); later work reaches `main` only through a new PR
when the user asks.

## Folders
- `handoff/` continuity brief · `docs/` final-form documentation · `memory/` assistant notes (05 = session log)
- `plan/` master plan v2, frozen PAP, archive + removed-items register
- `data_pipeline/` scripts + README · `data/processed/` outputs (raw data and basis panel git-ignored; rebuild per `docs/12`)
- `analysis/` estimators, simulated-data tests, audit scripts · `models_src/` model sources · `references/` papers + notes
- Root PDFs: project document (guide has it), Oct 2026 progress report (sent), current model; superseded Models A/B,
  Sep 28 note and literature review are internal and kept.

## Tooling notes
- `pdftotext` for most PDFs; `1_shleifer_vishny_limits.pdf` needs OCR (tesseract). `pandoc` reads the .docx.
- LaTeX sources exist for all generated PDFs; rebuild rather than hand-edit PDFs. More in `handoff/13_environment_and_tooling.md`.
