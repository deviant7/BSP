# 03. History and decisions (chronological)

Full detail: `memory/05_session_log.md`, the two chat logs at the repo root (`Very old conversation.txt`,
`Recent Conversation.txt`), `plan/archive/` and `plan/archive/REMOVED_ITEMS_REGISTER.md`.

## Phase 0: choosing the topic (before September 2026, desktop chats)

- The user asked for BSP ideas in market efficiency using Indian data. Seven ideas were proposed (expiry-day migration DiD,
  **F&O ban as a limits-to-arbitrage shock**, retail exit and noise-trader theory, losing weekly expiries, staggered T+0,
  anomalies risk vs mispricing, index inclusion).
- He wanted a multi-chapter research **programme** on public data. Two programmes were evaluated in depth:
  - **Program A (chosen): limits to arbitrage in Indian equities**, with the ban/MWPL as the constraint shock.
  - **Program B (dropped): the retail transformation 2019 to 2026.** Fatal measurement problem: participant-wise OI is
    market-level only; shareholding measures ownership, not trading; the 2024 to 2026 reforms are index-level (N of 1 or 2,
    no cross-section for DiD); welfare already estimated by SEBI with account data. It survives only as the concluding
    policy chapter.
- Advice then: make the constraint measure a deliverable that survives a null; run the density (McCrary) test early.
- A proposal (`BSP Proposal.docx`, not in the repo) was sent to Prof. Chaubal, who approved it.
- Note: two claims from that era later proved wrong and were removed: "position limits have been studied in Korea and
  Taiwan" (no source found) and "MWPL = 20% of free float **or 30 times prior-month volume**" (the volume leg ended in 2006).

## Phase 1: project document and literature (September 2026, desktop chats)

- `BSP_Project_Document.docx` (= `.pdf`): detailed study plan. Six chapters: constraint index (PCA), mispricing measures
  (basis, put-call parity, PEAD), causal identification (MWPL-denominator revisions as instrument; RD at 95% with
  McCrary), no-arbitrage band and 2025 regime shifts (TAR/STAR/Ters-Urban TVECM), cross-section (Fama-MacBeth on the
  45-signal library), policy chapter. Hypotheses H1 to H6. Timeline by weeks. The user's master plan (goals kept).
- 21 reference PDFs collected (user downloaded them via the library), verified, read in full; notes batches 1 to 5;
  Shleifer-Vishny OCR'd. A 29-page LaTeX literature review (`BSP_Literature_Review.pdf`).
- The guide then asked for a **mathematical model first**.
- Two candidate models were built: **Model A** (risk-averse arbitrageur with an MWPL cap; ban as a KKT shadow-price jump)
  and **Model B** (impulse-control band of inaction, b = (6K sigma^2/theta)^(1/4), "bridge" to TAR/TVECM), with 3-page
  guide versions and a 28 Sep 2026 progress note. **None of these was sent to the guide.**

## Phase 2: first cloud session (28 October 2026)

1. Read everything; built `memory/` and `CLAUDE.md` (user: save memory regularly).
2. **Audit of Models A and B** (`memory/04_models_and_audit.md`): both mis-model the ban (it restricts everyone, not only
   the arbitrageur; A conflated entity caps with the 95% market-wide trigger); A's Prop. 5 proof false; A's Prop. 4 theta
   ad hoc; B's QVI sign flipped and the "exact bridge" overstated; the identification claim "Cov(L,u) = 0 by timing" invalid;
   both were built to deliver H1 to H6 (reverse-engineering risk). Advice: one corrected model whose predictions can fail,
   plus a git-timestamped pre-analysis plan.
3. User corrections: the guide has not seen A/B or the progress note; **ignore timelines**; keep the document's goals;
   **the project is limits to arbitrage broadly, not only the ban**.
4. `plan/BSP_Research_Plan_v2.md` written (theory → PAP → blind data → validation → tests). Earlier plans archived;
   removed-items register created (user: keep all plans and deletions).
5. **Internet fact-check of every rule, date and citation** (`memory/07_fact_check.md`). Main corrections: no 30x volume
   leg after 2006; ADDV in quantity; 80% exit confirmed (NSE Clearing circular 119/2025, saved as `references/19`); mutual
   funds may legally short; new facts: COVID MWPL halving 2020, STT 0.05% from 1 Apr 2026, closing auction for F&O stocks
   from 3 Aug 2026, ban penalties, short-selling eligibility limited to F&O securities, MWPL was recomputed monthly before
   the reform. Two more Indian papers found and read (#20 Shankar et al. 2015; #21 Nandan, Agrawal and Jindal 2015).
6. **Model C written** ("go ahead"): one model with every limit as a parameter, the ban as reduce-only for everyone,
   inventory, spillover to cash, anticipation, hysteresis, the MWPL-not-an-instrument result, bad news in bans, Miller
   overpricing. All closed forms verified numerically. A first version of the level-effect proposition **failed** its
   check (mean-zero spillover cannot shift the mean) and was corrected to depend on the inflow of new demand.
7. User asked "can we just work with data without modelling?" Answer: possible in principle, but keep the existing model
   (the guide asked for it and it already changed the design); no more theory unless the data demand it.
8. **Data pipeline built** (blind): MWPL/OI/ban panel 2010 to 2026; prices 2015 to 2026; basis; F&O membership and events
   (the user's own membership sheet `fno_pit_3.xlsx` matched exactly after cleaning, used as a cross-check);
   announcements; Nifty validation. Many NSE file quirks found and fixed (catalogue in 08).
9. **Pre-analysis plan v1** written; tests on simulated data showed fixed-threshold SETAR recovers textbook thresholds but
   not the model's cost band (inventory moves thresholds), which changed H3 and added state-dependent thresholds.
10. **Progress report** (`BSP_Progress_Report_Oct2026.pdf`, 26 pp) written to guide-facing rules; the user asked to remove
    the "points on which I would value your guidance" section (kept in a separate file).
11. The user chose to **wait for the guide** before tagging the plan. Handoff written (`memory/08`). PR #1 opened and merged
    by the user (main = 65ef0e3).

## Phase 3: second cloud session (5 November 2026)

1. Full context re-gathered; one stale number fixed in the report table (2017 average F&O stocks 200, not 201).
2. User: the report was **sent**, the guide **liked it** and gave the go-ahead; name is "Chaubal". Asked whether the three
   library papers are needed (answer: not blocking; Saurav et al. first, for positioning). Asked for (a) a data audit,
   (b) a `docs/` folder of the final form, then (c) next steps.
3. **Data audit** (`docs/10_data_quality_audit.md`, scripts in `analysis/audit/`). Fixed: missing ban lists (imputed);
   October 2026 rate missing (carried forward, flagged); **results dates** (the filing feed had late re-filing times and
   current symbols; rebuilt from "Financial Result Updates" announcements + filings + board meetings + ISIN symbol
   history; 51.5% of old F&O events had been dated too late; coverage now 98 to 100%). Documented: combineoi vs bhavcopy
   OI differences; 9 missing Nifty days; BSE-only listings without results.
4. **`docs/`** written: README + 13 pages.
5. **Pre-analysis plan finalised** with pre-tag revisions (a) to (d) and **tagged `pap-v1`** at commit 85dac3a (tag push
   refused by the session's git proxy; the user must create the tag on GitHub).
6. User asked for a dedicated **`handoff/` folder** for continuity across chats/models (this folder), alongside memory.

## Phase 4: main tests (5 November 2026, same session, after the handoff was created)

1. Implementation details the plan left open were written into PAP §11 (C1 to C5) and committed before any test ran.
2. Shared sample and inference code (pyfixest two-way FE and clustering, checked on simulated panels).
3. H8 run: supported; identity failed pooled → research found the enforcement regimes (SEBI PR 18/2020 intraday checks
   from 23 Mar 2020; PR 59/2020; NSE Clearing 119/2025 end-of-day FutEq from 1 Oct 2025); the identity holds under
   intraday enforcement.
4. H7 run: rejected with the opposite sign; exploratory diagnostics (not noise; era-dependent; concentrated at spell
   starts → blocked-new-demand channel).
5. H3 run: supported on the pre-specified statistic; placebo calibration weak (common shocks).
6. User: plans fine; research the open questions deeply; get the H6 data (Prowess as fallback); keep memory, docs,
   handoff updated. Built adjusted returns (NSE prevclose unadjusted) and AMFI half-yearly market caps (back-cast before
   Jul 2017); H6 details fixed in §11.3 before estimation; H6 run (delay supports, drift contradicts); Holm over the family.
7. Session ended with a full save; resume card `16_resume_here.md`.

## Phase 5: third cloud session (7 November 2026)

1. Full context re-gathered (all handoff, memory, plans, PAP v0/v1, register, reference notes, report as sent, both chat
   logs, code). Stale handoff/memory entries fixed.
2. User: "make sure the edits were correct ... do not assume". Every correction re-checked against code, data and primary
   texts. Two of the assistant's own corrections were wrong and were fixed: (a) the in-ban trading rule from 1 Oct 2025
   IS looser than before (SEBI 2025/79 §5.3, Table 2: new delta-reducing contracts allowed); only the 2025 package as a
   whole is not a relaxation; (b) SLB eligibility is not limited to F&O stocks (SEBI widened it in July 2013; NSE SLB data
   show many non-F&O stocks). Short-selling eligibility (F&O securities) confirmed from SEBI's 5 Jan 2024 circular
   (saved as references/25).
3. **All secondary tests run**, each with a dated PAP §11 entry committed before the run (C7 to C15): level effect
   (signs as predicted, pre-specified split p = 0.083), density at 95% (no bunching), RD at 95% (trading jumps sharp,
   basis gap present on the crossing day), hysteresis (no extra level shift), H9 (upper tail widens with utilisation;
   reform in the right direction, n.s.), H2 (no power in bans; pre-announcement basis pattern outside bans), H1 (frictions
   and band width across stocks), H4 (weak), H5 (not supported value-weighted). Summary: `docs/14_results.md` §14.16.
4. New data: NSE SLB bhavcopies 2015 to 2026; AMFI monthly arbitrage-fund series April 2018 to September 2026.
5. User asked for a full checkpoint, then the band-estimation chapter: done (docs/15; noise check shows much daily reversion
   is VWAP noise). Then an exploratory IV check of H7 (opposite sign survives) and the constraint index for all stocks
   (docs/16; published data set).
6. User: "update the docs first, then option 3" → docs updated (main findings, contributions); thesis draft (8 chapters,
   52 pp) and a 5-page first-results report for the guide (not sent); extensive memory save (memory/09 digest).

## Phase 6: fourth cloud session (8 November 2026)
Remaining master-plan items (spurious bans, placebos, COVID halving and restoration; PAP §11.15) and a deep audit of the
whole project (full rerun reproduces every output; the constraint index's bad-news asymmetry is a size effect).

## Phase 7: fifth cloud session (9 November 2026)
Part 1: thesis content completed (literature chapter from the verified digest, with the old review's errors fixed;
§14.17 results; retail-loss policy framing). Part 2: re-read of every file (memory/10). Part 3: final thesis built in the
design of the user's formatting PDF (kept single-column and academic) with the template's front pages and 26 figures.

Phase 7, continued (9 Nov 2026): the user committed two consulting decks and asked for a deck in the same format:
`BSP_Presentation_Nov2026.pptx` (37 slides, pptxgenjs, charts as images in the reference style). Then two Overleaf
Beamer templates and a request for an academic backup deck: `BSP_Presentation_Academic_Nov2026.pdf` (Beamer, Madrid
recoloured blue, 56 pages). End of session: all memory, handoff and docs files updated.

## Phase 8: sixth cloud session (10 November 2026)
The user showed the guide the short thesis. She asked for a paper look, reader-focused language, no "results" for
theory, Stage I content only, and no approval page. After a full context re-read, the split was decided (BSP1:
foundations, the band, costs and frictions, trading in a ban; BSP2: price effects of the ban and position limits,
capital, short-sale constraints, policy) and the Stage I report and both decks were built in `BSP1/`.

## Decisions and their reasons (quick reference)

| Decision | Reason |
|---|---|
| Program A over B | B's treatment cannot be measured per stock with public data; reforms are index-level |
| Theory before data | Guide's instruction; guards against confirmation bias |
| One model (C) replacing A and B | A/B mis-modelled the ban and were reverse-engineered to H1 to H6 |
| Ban = reduce-only for everyone | That is the rule (NSE Clearing 119/2025; SEBI 2025/79) |
| MWPL not an instrument | It moves anticipation and caps even without a ban (Prop. 9) |
| VWAP basis, not settlement | Theoretical settlement price on no-trade days |
| 3-month interbank rate (monthly, OECD/FRED) | No daily T-bill series obtainable; relative implied repo removes common rate error |
| H7 regimes by stock-level 20/80 percentiles on non-ban days | Model-free, robust to inventory-moving thresholds; TVECM and fixed bands as robustness |
| H3 on changes of edges around STT dates | Fixed thresholds estimate average edges, not costs (simulation) |
| H9 and level effect secondary | Lower power / sign set by composition |
| 1 Apr 2023 not used alone for H3 | Same day as the debt-fund tax change |
| F&O entry/exit for H6 over ~2,000 cash stocks | Much more power than ~200 F&O stocks |
| Friction index from frictions only | Basis (outcome) and ban (treatment) as inputs would be circular |
| Put-call parity demoted | Thin, stale stock-option prices |
| 45-signal Fama-MacBeth chapter dropped | IP risk, accounting data not free; public anomalies with SYY double sorts instead |
| Git tag instead of OSF registration | Timestamp is enough (OSF if the guide wants) |
| Wait for guide before tag; then tag 5 Nov | User's choice; guide approved |
| Implementation details fixed in PAP §11 before each test | Keeps the frozen plan honest where it left details open |
| Exploratory additions labelled and logged in §11.2 | Pre-specified results always reported first |
| Free data (AMFI) for market caps; Prowess only for verification | User asked to try free sources first |
| H6 drift via stacked DiD; p_H6 Bonferroni of 4 components | Drift exists only at events; one p-value needed for Holm |
| Price >= Rs 5 filter for event outcomes | Sub-rupee tick artefacts (BHAR up to 8,190) |
| Density test on one-step transitions from below 95% | All-non-ban-days density is discontinuous mechanically (absorption into the ban) |
| Level-effect composition split also at the median and continuous | Only 8% of entries have falling OI before entry (OI must rise to cross 95%) |
| Exploratory build-up split (OI x price) | C cannot tell new longs from new shorts; the model's sign depends on it |
| SLB input in H1 measured as activity | Only a few dozen stocks trade in SLB per day; eligibility barely varies among F&O stocks |
| H4 on lagged flows with step dummies | Same-month flows chase returns (bias against the prediction); STT/tax dates shift the level |
| H5 constraint groups F&O / cash-only with SLB / cash-only without | Institutionally grounded short-sale constraint; IVOL terciles as robustness |
| Thesis kept single-column though the formatting PDF is two-column | User asked to keep it academic; equations and wide tables |
| Consulting deck charts as images, not native PowerPoint charts | Matches the reference decks' chart style; same data as the thesis |
| Academic deck in Beamer, not .pptx | Both supplied templates are Beamer sources |
| Literature chapter built from the verified digest, not the old review | The old review has known errors (11 §11.6) |
| Stage I = foundations + band + costs/frictions + trading in a ban | Coherent first half: measure the object and check the sharpest limit binds on quantities; price effects (the novel, more fragile results) need Stage II's space; both primary tests here (H3, H8) are the two smallest p-values, so their Holm values do not depend on Stage II |
| Full model shown in Stage I, with Stage II predictions marked | The model was Stage I work and frames both stages |

