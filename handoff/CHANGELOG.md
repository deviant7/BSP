# Handoff changelog (newest at the bottom)

- 5 Nov 2026: handoff folder created at the user's request (two-layer continuity: `memory/` for the assistant, `handoff/`
  for any new chat or model). Files 00 to 15 written from the full repository, memory, both chat logs, plans, PAP, docs,
  build reports and the model source. State: audit done, `pap-v1` at 85dac3a (local tag), main tests not yet run.
  Verified while writing: OI and Delta OI in the basis panel are in shares in both file formats; pyfixest installable.
- 5 Nov 2026: PAP §11 C1-C5 clarifications committed before any test (c6b1701); analysis sample + inference helpers;
  H8, H7, H3 run (results in 04 §4.7, `analysis/output/`); PAP §11.2 exploratory note (March 2020 break). 05 updated with
  PREVCLOSE finding and market-cap plan for H6.
- 5 Nov 2026: `pap-v1` confirmed on GitHub (annotated tag → 85dac3a), created by the user.
- 5 Nov 2026: research on H8 break (enforcement regimes, primary sources saved as references/23-24), H7 diagnostics, H3 placebo calibration; docs/14_results.md; facts updated in docs/03, handoff/10, memory/03, memory/07; PAP §11.2 extended.
- 5 Nov 2026: H6 inputs (adjusted returns, AMFI market caps, daily mcap), PAP §11.3 C6 before estimation, H6 run, Holm over the family; docs 06/07/09/10/12/14 and handoff 04/05/08/09/12/14 updated.
- 5 Nov 2026 (session end): `16_resume_here.md` resume card; 00 reading order, 04, 12, 15 (session-end rule), CLAUDE.md, memory 05/06/08 updated.
- 7 Nov 2026 (new session, context re-gathered): stale entries fixed in 04 (git, container, H6 row, status), 05 (tag, market cap), 07 (§11 contents), 08 (quirk 26), 09 (primary-test numbers added), 12 (counts), 13 (tools, sizes); memory/01 status rewritten; data_pipeline/README lists the three new builders.
- 7 Nov 2026 (broader context read: all memory files, plans, PAP v0, register, model ban section, report as sent, reference notes, chat logs, code): wording fix for the H7 spell-start diagnostic (days 0 to 4 after start) in PAP §11.2 note, docs/14, 09; correction boxes in references/notes_batch1 and batch5; memory/08 §6 marked pre-audit; 16 last-commit pointer.
- 7 Nov 2026 (re-verification of the morning's fixes): in-ban trading rule from 1 Oct 2025 is looser (SEBI 2025/79 Table 2) — earlier 'not a relaxation' notes corrected in references/notes_batch5 box, reference index, docs/03, 10; short-selling box in notes_batch1 checked against SEBI 5 Jan 2024 circular (new references/25); memory/07 §L.
- 7 Nov 2026: level-effect secondary test: PAP §11.4 C7 (before estimation), analysis/level_effect.py, results docs/14 §14.7 (14.8 = to come), 04 §4.10, 09, 16 (item 1 done), PAP §11.2 exploratory entry.
- 7 Nov 2026: density test at 95% (PAP §11.5 C8; analysis/density_test.py; docs/14 §14.8; 04 §4.10; 09; reports/figs/density_95.pdf).
- 7 Nov 2026: RD at 95% (PAP §11.6 C9; analysis/rd_95.py; docs/14 §14.9; 04; 09).
- 7 Nov 2026: exploratory build-up split of the level effect (analysis/level_effect_buildup.py; docs/14 §14.7; PAP §11.2; 04).
- 7 Nov 2026: hysteresis (PAP §11.7 C10; analysis/hysteresis.py; docs/14 §14.10; 04; 09; 14 open issues added).
- 7 Nov 2026: H9 (PAP §11.8 C11; analysis/h9_regime.py; docs/14 §14.11; 04; 09).
- 7 Nov 2026: H2 (PAP §11.9 C12; analysis/h2_badnews.py; docs/14 §14.12; 04; 09).
- 7 Nov 2026: H1 and H4 (PAP §11.10-11.11; analysis/h1_frictions.py, h4_capital.py; docs/14 §14.13-14.14; 04; 08 new data builders; 09); SLB and AMFI data; SLB-eligibility correction.
- 7 Nov 2026: H5 (PAP §11.12 C15; analysis/h5_anomalies.py; docs/14 §14.15) and secondary summary §14.16; 00, 04, 05 (Step 3 done, 3b new), 09, 16 header, CLAUDE.md, memory/01 status.
- 7 Nov 2026 CHECKPOINT: 00, 02, 03 (Phase 5), 06 (§6.7), 11, 12, 13 (§13.8), 14 (§14.6), 15, 16 (checkpoint card); docs 08, 09, 10, 11; memory 02/03/04/06; data_pipeline/README.
- 7 Nov 2026: band-estimation chapter (PAP §11.13 C16, §11.2 entry; analysis/band_estimation.py, band_exploratory.py, band_costs.py; docs/15; 04 §4.11; 05; 09; 14; 16).
- 7 Nov 2026: H7 IV exploratory check (analysis/h7_iv.py; PAP §11.2; docs/14 §14.3; 04; 05; 09; 14); PAP §11.14 C17 constraint index.
- 7 Nov 2026: constraint index deliverable (PAP §11.14 C17; analysis/constraint_index.py; data/processed/constraint_index_q.csv.gz; docs/16; 04 §4.12; 05; 09; 12; 16; CLAUDE.md; memory/01).
- 7 Nov 2026: write-ups (thesis/ draft 52 pp; first-results report 5 pp, not sent); docs updated first; memory/09 findings digest; 03, 04 (§4.13 + documents), 05, 12, 16 header, CLAUDE.md.
- 7 Nov 2026 END OF SESSION: register changelog, master-plan status note, 07 (C16-C17), 04 (git, container), 14 (waiting list), 16 (write-up rebuild commands), neutral pronouns; memory/05 end entry.
- 8 Nov 2026 (new session): context re-gathered; smoke tests pass; stale entries fixed (01 pronoun, 10 statuses, memory/04); open master-plan items listed in memory/05.
- 8 Nov 2026: spurious bans, placebos, COVID halving (PAP §11.15 C18-C20 + results entry; analysis/spurious_bans.py, placebos.py, covid_halving.py; docs/14 §14.17; 04 §4.14; 05 Step 3c; 09).
- 8 Nov 2026: deep audit (04 §4.15): full rerun reproduces outputs; estimator tests for CS and level effect; number check; fixes (ch4 99.85%, appendix wording, model SLB wording, index bad-news asymmetry = size effect, all write-ups corrected); PAP §11.2 size-check entry; docs/12 rerun + checks; 05, 09, 14 §14.7, 16; memory/05, 09.
- 8 Nov 2026 END OF SESSION: next-session plan agreed and saved (16 top, 05 Step 3c pointer; memory/05).
- 9 Nov 2026: Part 1 of the plan: §14.17 results and SEBI retail-loss framing in thesis ch5/ch6/ch8, literature chapter (ch_literature.tex), references, halving count fix (docs/08, 10, 11); 16; memory/05.
- 9 Nov 2026: Parts 2 and 3: re-read (memory/10); final thesis BSP_Thesis_Final_Nov2026.pdf (bspstyle.sty, frontmatter, native model appendix, 26 figures via analysis/thesis_figures_final.py); docs/12 and rerun_all.sh updated; 00, 03, 04 §4.16, 16; CLAUDE.md; memory/05, 10.
- 9 Nov 2026: presentation deck BSP_Presentation_Nov2026.pptx/.pdf (deck/build_deck.js, analysis/deck_figures.py, deck/figs/); 04, 16, CLAUDE.md, memory/05.
- 9 Nov 2026: academic Beamer deck BSP_Presentation_Academic_Nov2026.pdf (beamer/main.tex, analysis/beamer_figures.py, beamer/figs/); 04, 16, CLAUDE.md, memory/05.
- 9 Nov 2026 END OF SESSION: in-depth update of memory (01-06, 08, 09), handoff (00-07, 09, 11-14, 16 rewritten), docs (README, 12), CLAUDE.md, master-plan status.
- 9 Nov 2026: short thesis BSP_Thesis_Short_Nov2026.pdf (50 pp, thesis_short/); 00, 04, 12, 16; docs README, 12; CLAUDE.md; memory/05, 09.
- 10 Nov 2026: guide's comments on the short thesis; BSP1/BSP2 split decided (BSP1/README.md); memory/05.
