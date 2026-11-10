# BSP1: the Stage I version of the thesis and presentations

Built 10 November 2026 after the guide's comments on the short thesis. Nothing outside this folder was changed by this
work: the full thesis (`thesis/`), its short version (`thesis_short/`) and both earlier decks (`deck/`, `beamer/`)
stay as they were.

## The guide's comments (as relayed by the user)
1. Design: too much like a report, not like a paper. Keep the formatting design, the structure, the sectioning, the
   font, the theme and the title page; make it look like a paper.
2. Language: write as a paper, readable to an unknown reader; give context; drop small decisions and side findings
   that do not bear on the question, method or results; undergraduate author voice.
3. The model's derived statements are theoretical derivations, not "results": do not call them results.
4. Restrict the thesis and presentations to BSP1 (Stage I, EC 495): a little more than half of the work done. The rest,
   and later additions, form BSP2 (Stage II, EC 497).
5. Remove the "Report Approval" page.

## The split
**BSP1 (this folder):** question and motivation; institutions; literature; the full model (propositions, with the ban
predictions marked for Stage II); the research design and frozen test plan; the data set and descriptive facts; the
no-arbitrage band (pooled threshold model, linearity test, smooth-transition models, noise check, by year and by time to
expiry, per-stock bands, comparison with earlier Indian estimates); what sets the band (pre-specified cost test H3 with
its placebo calibration; bottom-up cost band; frictions across stocks H1); does the ban bind on trading (pre-specified
H8; enforcement regimes and the open-interest identity; the 95% trigger: density test and the trading jumps of the
discontinuity); how the October 2025 rules changed the number of bans.

**BSP2 (Stage II, not in this folder):** what the ban does to prices (H7 one-sided correction and its noise check, the
level effect at ban start and its build-up split, the basis part of the discontinuity, hysteresis, placebo bans, H2 bad
news in bans); the position-limit regime and prices (H9 anticipation and the 2025 reform intensity, the 2020 halving and
restoration); arbitrage capital (H4, capital as a state, peak margins); short-sale constraints (H6 F&O entry and exit,
H5 anomalies, the constraint index for all stocks, drift of cash-only stocks); policy (SEBI retail losses, enforcement,
spurious bans); new work (intraday data, a longer post-reform sample, extensions of the model for blocked new demand).

## Files
- `paper/`: LaTeX source of the paper-style Stage I report (`main.tex`, `bsp1style.sty`, section files, `figs/`).
- `deck/`: consulting-format deck generator for Stage I (`build_deck_bsp1.js`, `figs/`).
- `beamer/`: academic Beamer deck for Stage I (`main.tex`, `figs/`).
- Outputs: `BSP1_Report_Nov2026.pdf`, `BSP1_Presentation_Nov2026.pptx` (+ `.pdf`),
  `BSP1_Presentation_Academic_Nov2026.pdf`.
