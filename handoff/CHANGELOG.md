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
