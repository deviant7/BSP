# CLAUDE.md — BSP project memory (read this first, every session)

This repository is Prince Kumar's (Roll 23B3032, BS Economics, IIT Bombay, 2023–27) Bachelor's thesis project
(EC 495 Stage I, 6 cr, Sem 7 → EC 497 Stage II, 12 cr, Sem 8). Guide: **Prof. Aditi Chaubal** (Economics; non-linear time series).
Topic: **Limits to Arbitrage in the Indian Equity Market** — does India's MWPL "F&O ban" (fresh single-stock derivative
positions barred once market-wide OI > 95% of MWPL) widen/prolong mispricing? Uses public NSE data, 2015–2026, ~220 F&O stocks.

## Standing instruction from the user (durable)
- **Save to memory regularly.** After any meaningful step (a decision, a new document, a finding, a user correction),
  update the files in `memory/` and append to `memory/05_session_log.md`, then commit and push to the session branch.
  The container is ephemeral; only what is committed to this repo survives.
- The user wants thorough, unbiased, academically rigorous work; read primary sources, not just notes. Flag errors honestly.

## Read these before answering anything substantive
1. `memory/01_project_context.md` — the research design, chapters, hypotheses, data, timeline, decision history.
2. `memory/02_literature_digest.md` — verified facts/numbers from all 21 papers (read from the PDFs).
3. `memory/03_institutional_facts.md` — SEBI/NSE rules and exact dates (verified vs unverified).
4. `memory/04_models_and_audit.md` — Models A and B, and the audit of their (and the docs') errors.
5. `memory/05_session_log.md` — chronological log of what was done, decided, and what is open.
6. `memory/06_user_working_style.md` — how the user likes to work.
7. `memory/07_fact_check.md` — internet verification of every rule/date/citation (28 Oct 2026), with corrections.

## Current master plan
- `plan/BSP_Research_Plan_v2.md` — how the project proceeds (supersedes the project doc's §7 methods ordering and §12 timeline;
  the doc's goals stand). The guide has seen only the project document. **No time pressure — ignore timelines.**

## File map (repo root)
- `BSP_Project_Document.docx` / `.pdf` — the detailed study plan (Sep 2026); identical content. The user's master plan.
- `BSP_Literature_Review.pdf` + `litreview_src/` — 29-pp math-level review (LaTeX, compiles).
- `BSP_Model_A_Constrained_Arbitrage.pdf`, `BSP_Model_B_Band_of_Inaction.pdf` + `models_src/` — the two candidate models (full).
- `BSP_Model_A_for_guide.pdf`, `BSP_Model_B_for_guide.pdf` — 3-pp plain-language versions sent/for guide.
- `BSP_Progress_Report.pdf` + `progress_report_src/` — 4-pp progress note to the guide (Sep 28 2026).
- `Claude outputs/` — byte-identical duplicates (NB: `Claude outputs/BSP_Model_A_Constrained_Arbitrage.pdf` is actually the 3-pp guide version).
- `references/` — 21 PDFs (`1_…` to `18_…`), plus `19_nse_clearing_circ119_2025_mwpl_sop.pdf` (primary source for new MWPL,
  80% exit, ban penalties), `00_reference_index.md`, `notes_batch1..5_*.md`.
- `Very old conversation.txt`, `Recent Conversation.txt` — logs of earlier chat sessions (project origin → models).
- Not in repo (referenced in old chats): original `BSP Proposal.docx` sent to the guide; earlier assistant memory notes.

## Tooling notes
- `pdftotext` works for most PDFs; `1_shleifer_vishny_limits.pdf` has a garbled font layer → OCR with tesseract
  (`apt-get install -y tesseract-ocr`, then `pdftoppm -r 200 -gray` + `tesseract`). `pandoc` reads the .docx.
- LaTeX sources exist for all generated PDFs; rebuild rather than hand-edit PDFs.
