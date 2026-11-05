# 11. Descriptive facts

These facts describe the treatments and the outcome **separately**. No outcome is related to any treatment here
([09_empirical_design.md](09_empirical_design.md), 9.1). All numbers come from `data/processed/descriptives.txt`,
`fno_events_report.txt`, `announcements_report.txt` and `basis_report.txt`, and reproduce from the build
([12_reproducibility.md](12_reproducibility.md)).

## 11.1 The F&O universe

- 2015 to 27 October 2026: 534,712 F&O stock-days, 374 distinct stocks, on average 183 F&O stocks per day (140 in 2020,
  216 in 2025).
- 239 entries and 171 exits. 162 exits are eligibility exits after which the stock kept trading in the cash market; 9 are
  mergers, delistings or unlinked symbol changes. 21 symbol changes are linked through the ISIN and are not events.
- Entries and exits come in batches: 45 entries on 29 November 2024 (after the August 2024 revision of the criteria),
  34 exits on 28 June 2019 (2018 framework), 16 exits on 28 February 2025, 16 entries each on 28 April 2017 and
  26 February 2021.

| Year | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Entries | 20 | 16 | 41 | 0 | 0 | 6 | 60 | 2 | 0 | 45 | 33 | 16 |
| Exits | 3 | 3 | 5 | 11 | 56 | 13 | 0 | 8 | 8 | 5 | 48 | 11 |

## 11.2 F&O bans

| Year | F&O stocks (avg per day) | Stocks banned | Ban spells | Ban stock-days | Median spell (days) | Longest spell (days) |
|---|---|---|---|---|---|---|
| 2015 | 154 | 16 | 69 | 367 | 4 | 21 |
| 2016 | 172 | 27 | 136 | 645 | 4 | 17 |
| 2017 | 200 | 43 | 287 | 1,586 | 5 | 24 |
| 2018 | 206 | 38 | 162 | 810 | 4 | 31 |
| 2019 | 176 | 23 | 86 | 508 | 4 | 17 |
| 2020 | 140 | 40 | 178 | 756 | 3 | 13 |
| 2021 | 163 | 26 | 162 | 789 | 4 | 16 |
| 2022 | 196 | 23 | 100 | 457 | 4 | 13 |
| 2023 | 187 | 41 | 193 | 942 | 4 | 17 |
| 2024 | 185 | 49 | 289 | 1,656 | 5 | 22 |
| 2025 | 216 | 37 | 93 | 558 | 5 | 16 |
| 2026 (to 27 Oct) | 209 | 10 | 33 | 342 | 10 | 29 |
| **2015 to 2026** | **183** | **141** | **1,788** | **9,416** | **4** | **31** |

Spells are counted in the year they start.

- Bans are concentrated: the median banned stock had 6 spells over 2015 to 2026; the most frequently banned (SAIL) had 76.
- A typical spell lasts 4 trading days (mean 5.3; 7% last a single day).
- **Before and after the October 2025 reform:** 1,744 spells from 2015 to September 2025 (median 4 days, mean 5.2); 44
  spells from October 2025 (median 9 days, mean 9.3). Under the new rules spells are fewer and longer.
- Including the pre-sample (2010 to 2014): 2,181 spells and 11,765 ban stock-days.

## 11.3 The MWPL and utilisation

- Outside the special events below, the MWPL changes mainly in February, May, August and November (1,485, 1,612,
  1,558 and 1,529 stock-day changes respectively, against at most 457 in any other month), when free float is updated from
  quarterly shareholding filings.
- **March 2020:** the MWPL was halved for 61 stocks in the files of 20 to 27 March 2020 (28 on 20 March, 13 on
  23 March, the rest over the following days) and restored for 70 stocks on 26 November 2020.
- **1 October 2025:** the new formula lowered the MWPL of all 208 F&O stocks. Ratio of new to old: 10th percentile 0.50,
  median 0.73, 90th percentile 0.75. 17% of stocks are at the floor (10% of free float, half the old limit) and 48% at
  15% of free float (three quarters of the old limit). Because the cut differs across stocks and was set from data
  before the reform, it measures treatment intensity.
- **Near the threshold:** on non-ban days before the reform there are 2,439 stock-days with utilisation in (0.90, 0.95]
  and 961 in (0.95, 1.00] (stocks about to enter the next day); after the reform, 139 and 37 (futures-equivalent
  utilisation). Before the reform the density of utilisation thins out smoothly through 95%, with no visible pile-up just
  below it; a formal density test is part of the plan.

## 11.4 Results announcements

- 94,071 results events (stock and quarter) for 2014 to October 2026, about four per company per year.
- 8,594 events fall on days when the stock is in the F&O segment; 180 of them on ban days.
- Release time known for 99.0% of the F&O events; 62% of timed F&O releases come at or after the 15:30 close, so their
  day 0 is the next trading day.
- Median time from quarter end to release: 42 days.

## 11.5 The basis (outcome distribution on its own)

On the clean near-month sample (503,170 stock-days with at least five contracts traded and no dividend or other corporate
event within the contract's life):

| Statistic | Value (bp) |
|---|---|
| Median | +1.2 |
| 10th percentile | -33.0 |
| 90th percentile | +26.2 |
| Share more than 200 bp from zero | 0.65% |

- The distribution is stable over time (all near-month stock-days with at least five contracts): yearly medians lie between -1.8 bp (2018) and +9.2 bp (2021), and the 10th
  and 90th percentiles move within roughly -46 to -18 bp and +24 to +34 bp.
- The basis shrinks toward expiry: the median absolute basis falls from 16.6 bp with 21 to 35 days left to 12.8 bp in
  the last three days.
- The lower tail is wider than the upper (the 10th percentile is further from zero than the 90th), the asymmetry the model
  expects when reverse arbitrage is costlier than cash-and-carry. This is a description, not a test.
