# Limits to Arbitrage in the Indian Equity Market: project documentation

Bachelor's thesis project (EC 495 / EC 497), BS Economics, IIT Bombay.
Author: Prince Kumar. Guide: Prof. Aditi Chaubal.

## What this project is about, in one paragraph

In theory, two ways of getting the same asset should cost the same: owning a share and holding a future on that share
should be priced consistently, and any gap should be closed quickly by arbitrageurs. In practice arbitrage is limited by
costs, by rules that make short selling hard, by limited capital and by position limits, so gaps can persist. India
changes almost every one of these limits on known dates, and it has an unusual rule, the **F&O ban**: when open interest in
a stock's derivatives reaches 95% of an exchange-set limit, every trader may only reduce positions until it falls to 80%.
This project builds a theory of arbitrage under India's limits, derives testable predictions with the results that would
contradict them, fixes the tests in advance, and tests them on a data set built entirely from public National Stock
Exchange files for 2015 to 2026 (bans from 2010).

## Main findings

1. **Bans bind on trading.** In a ban futures trading falls by about 2 log points, cash delivery rises, and every futures
   trade closes positions when the rule is enforced on intraday positions (from March 2020).
2. **Correction is not one-sided in the way the model predicts.** Rich futures revert faster, not slower, in a ban,
   mostly at the start of a spell; the result survives a correction for measurement noise.
3. **The basis falls when a ban starts,** by about 6 bp against similar stocks that stay just below the trigger, more when
   open interest was building fast; there is no sign of bunching below the trigger.
4. **Costs and the band.** The upper part of the basis distribution rose around the 2024 and 2026 tax increases, but
   mostly as a common shift; the band is about -35 to +24 bp around each stock's median, and the full cost of a new
   cash-and-carry position (27 to 31 bp) sits in its outer tail.
5. **Short-sale access.** After a stock enters the F&O segment its price responds faster to market news; drift after bad
   news does not weaken. Across all stocks, a constraint index built from frictions predicts slower price adjustment (also after
   controlling for size) and larger post-announcement drift.
6. **Position-limit rules.** Measured against the old rule applied to the same stocks, the October 2025 rules cut ban days
   by about three quarters; restoring halved limits in November 2020 lowered utilisation and made a rich basis less common.
   Placebo checks at false ban dates show neither the reversion result nor the fall in the basis at ban start.

Details, including the tests that failed: [14_results.md](14_results.md), [15_band_estimation.md](15_band_estimation.md),
[16_constraint_index.md](16_constraint_index.md).

## How to read this documentation

Read the pages in order if the field is new to you; each page assumes only the ones before it.

| Page | Content |
|---|---|
| [01_background_concepts.md](01_background_concepts.md) | Stocks, futures, options, open interest, the basis, arbitrage, short selling, the MWPL and the ban, the statistical tools, a glossary |
| [02_research_question.md](02_research_question.md) | The question, why India, the approach, the contribution, the scope |
| [03_institutional_setting.md](03_institutional_setting.md) | The Indian rules used in the project, with dates and sources |
| [04_theoretical_framework.md](04_theoretical_framework.md) | The model, step by step, and what each result implies |
| [05_hypotheses.md](05_hypotheses.md) | Primary and secondary hypotheses, each with its falsifier |
| [06_data_sources.md](06_data_sources.md) | Every data source, its address, format and coverage |
| [07_data_construction.md](07_data_construction.md) | Every rule used to build the data sets, including how each quirk of the source files is handled |
| [08_variables_and_measures.md](08_variables_and_measures.md) | Exact definitions of outcomes, treatments and controls |
| [09_empirical_design.md](09_empirical_design.md) | The pre-analysis plan in plain language: safeguards, samples, tests, inference, power |
| [10_data_quality_audit.md](10_data_quality_audit.md) | Every check run on the data and its result |
| [11_descriptive_facts.md](11_descriptive_facts.md) | Facts about bans, position limits, F&O membership, announcements and the basis (no outcome is related to any treatment) |
| [12_reproducibility.md](12_reproducibility.md) | Repository layout, software, the exact rebuild sequence, outputs |
| [13_references.md](13_references.md) | Papers and regulatory documents |
| [14_results.md](14_results.md) | Results of all pre-specified tests (primary H8, H7, H3, H6 with the multiple-testing correction; all secondary tests), with exploratory additions marked as such |
| [15_band_estimation.md](15_band_estimation.md) | Estimation of the no-arbitrage band: threshold and smooth-transition models, the band over time and across states, per-stock bands, and a bottom-up cost band |
| [16_constraint_index.md](16_constraint_index.md) | A quarterly constraint index for all NSE stocks (published data set), its construction and validation |

## Where the project stands

| Part | Status |
|---|---|
| Theoretical framework | Complete; every closed form checked numerically |
| Pre-analysis plan | Complete and frozen (git tag `pap-v1`) |
| Data set | Built and audited (sources, construction, checks in pages 06, 07 and 10) |
| Tests | All primary tests (with Holm correction) and all secondary tests run (page 14; summary 14.16) |
| Band estimation | Threshold and smooth-transition estimates, states, costs (page 15) |
| Constraint index | Built for all NSE stocks, 2015 to 2026, validated (page 16; data `constraint_index_q.csv.gz`) |
| Further checks | Spurious bans before and after the 2025 reform, placebos, the 2020 halving and restoration (page 14, 14.17) |
| Reproduction | A full rerun from the processed data reproduces every reported number (page 12) |
| Write-ups | Final thesis `BSP_Thesis_Final_Nov2026.pdf` (source `thesis/`) and its short version `BSP_Thesis_Short_Nov2026.pdf` (source `thesis_short/`); presentation decks `BSP_Presentation_Nov2026.pptx` (consulting format, source `deck/`) and `BSP_Presentation_Academic_Nov2026.pdf` (Beamer, source `beamer/`) |

## Conventions

- Basis points (bp): 1 bp = 0.01%.
- "F&O stock": a stock with single-stock futures listed on NSE on that day.
- Dates are trading days unless stated otherwise; "day t-1" is the previous trading day.
- File and column names in `code font` refer to the repository (`data/processed/`, `data_pipeline/`).
