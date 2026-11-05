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

## Where the project stands

| Part | Status |
|---|---|
| Theoretical framework | Complete; every closed form checked numerically |
| Pre-analysis plan | Complete and frozen (git tag `pap-v1`) |
| Data set | Built and audited (sources, construction, checks in pages 06, 07 and 10) |
| Tests | To be run under the frozen plan; results will be added as a new page |

## Conventions

- Basis points (bp): 1 bp = 0.01%.
- "F&O stock": a stock with single-stock futures listed on NSE on that day.
- Dates are trading days unless stated otherwise; "day t-1" is the previous trading day.
- File and column names in `code font` refer to the repository (`data/processed/`, `data_pipeline/`).
