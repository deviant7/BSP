# 12. Repository map (every tracked file)

Legend: **C** current; **S** superseded (kept on purpose; never delete); **G** has been seen by the guide; **I** internal only.

## Root
| File | What it is | Status |
|---|---|---|
| `BSP_Thesis_Draft_Nov2026.pdf` | Thesis draft (52 pp) compiled from `thesis/` (7 Nov 2026) | C, I |
| `BSP_First_Results_Nov2026.pdf` | First-results report for the guide, compiled from `progress_report_src/first_results_nov2026.tex`; NOT SENT | C |
| `CLAUDE.md` | Project memory loaded automatically by Claude Code; points to `handoff/16_resume_here.md` and `00_START_HERE.md` | C, I |
| `BSP_Project_Document.docx` / `.pdf` | Detailed study plan, Sep 2026 (identical content); the user's master plan of goals; has known errors (see 10) | C (goals), G |
| `BSP_Progress_Report_Oct2026.pdf` | Progress report sent to the guide (26 pp incl. model appendix); pre-audit numbers | C, G |
| `BSP_Model_C_Constrained_Arbitrage_India.pdf` | Current theory (15 pp); guide-safe | C, G (as appendix) |
| `BSP_Literature_Review.pdf` | 29-pp math-level review (Sep 2026); known errors | S/I |
| `BSP_Model_A_Constrained_Arbitrage.pdf`, `BSP_Model_A_for_guide.pdf` | Superseded Model A (full; 3-pp version) | S, I (never sent) |
| `BSP_Model_B_Band_of_Inaction.pdf`, `BSP_Model_B_for_guide.pdf` | Superseded Model B | S, I |
| `BSP_Progress_Report.pdf` | 4-pp progress note of 28 Sep 2026 | S, I (never sent) |
| `Claude outputs/` | Byte duplicates from the desktop era. NB `Claude outputs/BSP_Model_A_Constrained_Arbitrage.pdf` is actually the 3-pp guide version; `..._ORIGINAL.pdf` = original Model B | S |
| `Very old conversation.txt` | Log of the topic-selection chat (seven ideas; programmes A vs B) | I |
| `Recent Conversation.txt` | Log of the literature/model chats (Sep 2026) | I |
| `.gitignore` | Ignores `data/raw/`, `basis_panel.csv.gz`, LaTeX aux, `__pycache__`, the report build PDF | |

## Folders
| Path | Content |
|---|---|
| `handoff/` | This continuity brief (00 to 16 + CHANGELOG; 16 = resume card) |
| `docs/` | Final-form documentation for outside readers (README, 01 to 14; 14 = results) |
| `memory/` | Assistant's running notes: 01 context, 02 literature digest, 03 institutional facts, 04 models and audit, 05 session log (chronological, most detailed), 06 user style, 07 fact-check log, 08 earlier handoff (superseded by `handoff/`, kept) |
| `plan/BSP_Research_Plan_v2.md` | Master plan (scope table, theory summary, hypotheses H1 to H9, phases, measurement, chapters) |
| `plan/pre_analysis_plan_v1.md` | Frozen test plan (`pap-v1` at 85dac3a) |
| `plan/archive/` | `plan_v1_project_document_Sep2026.md`, `plan_v2.0_first_draft_2026-10-28.md`, `plan_v2.1_broadened_2026-10-28.md`, `pre_analysis_plan_v0_draft_2026-10-28.md`, `REMOVED_ITEMS_REGISTER.md` (every removed/changed item with reason and how to reintroduce; changelog at the end) |
| `data_pipeline/` | 18 scripts + README (see 08; incl. `build_returns.py`, `build_amfi_mcap.py`, `build_mcap.py`, and from 7 Nov `download_slb.py`, `build_slb.py`, `download_amfi_monthly.py`) |
| `data/processed/` | Processed data and build reports (see 08 §8.2); `basis_panel.csv.gz` present only in a container that built it |
| `data/raw/` | Raw downloads (not tracked) |
| `analysis/` | `setar.py`, `test_setar_simulated.py`, `audit/`; `samples.py`, `inference.py`, `test_inference.py`; tests `h8_trading.py`, `h7_onesided.py`, `h7_diagnostics.py` (exploratory), `h3_costs.py`, `h6_outcomes.py`, `h6_fno.py`; secondary tests (7 Nov) `level_effect.py`, `level_effect_buildup.py` (exploratory), `density_test.py`, `rd_95.py`, `hysteresis.py`, `h9_regime.py`, `h2_badnews.py`, `h1_frictions.py`, `h4_capital.py`, `h5_anomalies.py`; `output/` result files (one `.txt` per test, plus `level_effect_events.csv.gz`) |
| `models_src/` | LaTeX of Models A and B and their guide versions (superseded); `modelC/` (tex, compiled PDF copy, `verify_modelC.py`, `verify_output.txt`, `figs/fig_band.pdf`, `fig_path.pdf`, `fig_hist.pdf`) |
| `progress_report_src/` | `progress_report_oct2026.tex` (the sent report; includes `../reports/tables/ban_by_year.tex` and figures; macros like `\basisN` hold basis numbers), `removed_guidance_questions.tex`, `progress_report.tex` (Sep 28 note) |
| `thesis/` | LaTeX of the thesis draft: `main.tex`, `ch1_introduction` to `ch8_conclusion`, `appA_plan`, `appB_data`, `references` (appendix C includes the model PDF) |
| `litreview_src/` | LaTeX of the literature review (main + 6 parts + references) |
| `reports/figs/` | `ban_days_per_month.pdf`, `spell_lengths.pdf`, `utilisation_near_threshold.pdf`, `mwpl_ratio_oct2025.pdf`, `density_95.pdf` (7 Nov) |
| `reports/tables/` | `ban_by_year.tex` (regenerated after the audit: 1,788 / 9,416) |
| `references/` | 25 numbered items (#18 HTML page, #24 text file), `00_reference_index.md`, `notes_batch1..6` (batches 1 and 5 carry correction boxes added 7 Nov) |

## references/ numbering
1 Shleifer-Vishny; 2 Gromb-Vayanos; 3 DSSW; 4 Aggarwal; 5 Stambaugh-Yu-Yuan; 6 Ofek et al.; 7a Dwyer-Locke-Yu;
7b Ters-Urban; 7c Tse; 8 Nandan et al. (Nifty); 9 Roy-Chakraborty; 10 PEAD India (Harshita et al.); 11 Slivka et al.;
12 SEBI F&O retail-loss study; 13 Kumar; 14 lottery factor India (Sehgal et al.); 15a/15b Barber-Odean; 16 SEBI 2024/132;
17 SEBI 2025/79; 18 NSE MWPL methodology page (HTML); 19 NSE Clearing 119/2025; 20 Shankar et al. 2015; 21 Nandan-Agrawal-
Jindal 2015; 22 NSE Clearing FAQ Oct 2025; 23 SEBI PR 59/2020 (review of the March 2020 measures); 24 BSE/ICCL notice
20200322-2 implementing SEBI PR 18/2020 (text); 25 SEBI circular 2024/1 (5 Jan 2024), framework for short selling.

New processed data (7 Nov, committed): `data/processed/slb_daily.csv.gz`, `slb_report.txt`, `amfi_arbitrage_monthly.csv`,
`constraint_index_q.csv.gz`. New analysis scripts: `band_estimation.py`, `band_exploratory.py`, `band_costs.py`,
`h7_iv.py`, `constraint_index.py`. New docs pages: `docs/15_band_estimation.md`, `docs/16_constraint_index.md`.
Git-ignored, rebuildable: `data/raw/slb/`, `data/raw/amfi_monthly/`, caches `frictions_q.pkl`, `h5_monthly.pkl`.

## Not in the repo
- `BSP Proposal.docx` (the original proposal sent to the guide; desktop era).
- The user's `fno_pit_3.xlsx` membership sheet (from an earlier project; evaluated, matched exactly).
- Earlier desktop-assistant memory notes (their content is reflected in the chat logs and `memory/`).
