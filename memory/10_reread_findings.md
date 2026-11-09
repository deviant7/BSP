# 10 — Findings from the full re-read (9 Nov 2026, Part 2 of the agreed plan)

Purpose: context building before the final thesis build, and a last consistency check. Each item: where, what, action.

## Thesis (read in full: main, ch1 to ch8, literature chapter, appendices A and B, references)
- ch4 counts (1,788 spells, 9,416 stock-days, 141 stocks; 11,753 of 11,764 flags) match docs/09, 10, 11 and the ban table.
- ch2 arbitrage-fund assets (Rs 56,218 cr Apr 2018; 71,106 cr Apr 2023; 1.99 lakh cr Oct 2024; 2.98 lakh cr Sep 2026)
  match docs/07, 11, 14.
- Halving count: thesis ch2 says 61 stocks (correct in total: 60 in the 20 to 27 March 2020 files plus 1 on 29 April);
  docs/08, 10, 11 corrected on 9 Nov to say so; the COVID test uses the 60 March stocks.
- Post-reform spells: 44 began on or after 1 Oct 2025; the counterfactual table counts 45 because one spell began on
  30 Sep 2025 (footnote in ch5).

## Model (models_src/modelC tex, read in full)
- It enters the thesis as Appendix C through includepdf: separate title page, "Theoretical framework for the BS Project",
  "October 2026" date, own header and fonts. **Part 3: convert it into a native appendix chapter** in the thesis format
  (update tense: "the empirical work will compute a cost band" is now done).
- Its hypothesis map frames H6 as "inclusion lowers overpricing"; the plan and the thesis test H6 through price delay and
  bad-news drift (the Diamond-Verrecchia leg). When converting, state both and keep the plan's version as the test.
- Content otherwise consistent with thesis ch3 (Results 1 to 11 map to Props 1 to 11; Miller closed form matches).

## docs/ (read in full: README, 01 to 16)
- Fixed 9 Nov: docs/03 3.6 arbitrage-fund assets now from AMFI's own reports (was "financial press"); docs/09 9.6 adds the
  CS and level-effect simulated-data checks; docs/11 halving sentence; docs/13 adds the literature-chapter references and
  SEBI PR 22/2024; docs/14 status line points to 14.17.
- Consistent with the thesis: H8, H7, H3, H6 tables; Holm table; secondary results and summary 14.16; band chapter
  numbers (IV slopes -0.121 / -0.192 / -0.141 are by x(t-2) regimes); index table; descriptive facts.
- docs/README "Main findings" has no line on the 2025 reform's ban count or the placebos; "Where the project stands" has
  no row for 14.17. Optional addition.

## handoff/ and memory/ (internal)
- handoff/00 §1 item 5 and its "Last full update" line still describe 7 Nov; handoff/01 1.9 and 1.6 describe the planned
  structure (now superseded by the thesis). Update at the end of this session.
- Fixed 9 Nov: handoff/10 AUM fact now D (AMFI); memory/09 gains a §14.17 section; PAP log note on the §4(a) halving
  count (60 in the March files + 1 on 29 Apr). handoff/03 lacks Phases 6 (8 Nov) and 7 (9 Nov); handoff/04 header,
  status board ("docs 01 to 14"), and 4.6 document table (thesis 52 pp) are stale: update at session end.

## plan/ (master plan v2, PAP v1 sections 1 to 10 and the log)
- Master-plan items not done and not needed for the thesis: put-call parity (optional), SUE from XBRL (optional), an RD
  on the F&O eligibility criteria (mentioned in §7, never specified in the PAP), a separate crowding index. The band
  chapter uses pooled univariate threshold models (fixed in C16), not the TVECM the master plan named as workhorse.
  The thesis does not claim either; no change needed. Can be listed as further work.
- PAP frozen text has pre-audit numbers in §1 (99.85%, 99.2%/99.5%) and "61 stocks" in §4(a); these are the frozen
  record, the thesis uses current numbers.

## Conversation logs and root PDFs
- Logs (Very old, Recent) are history of Sep to Oct 2026 (topic choice, literature, Models A/B); nothing that
  conflicts with the current state.
- The October report the guide received says "only F&O-segment stocks are eligible for short selling and securities
  lending": the thesis corrects the SLB part. Mention the correction in the covering note when the thesis is sent.
- Analysis outputs: every decimal number quoted in the thesis matched an output (check_numbers.py, 9 Nov); the three
  new §14.17 passages were checked by hand against spurious_bans.txt, placebos.txt and covid_halving.txt.
