# 10. Data quality audit

Every data set was checked against the trading calendar, against the exchange's own rules and against the other
sources. This page lists each check, its result and, where a problem was found, the rule that now handles it
([07_data_construction.md](07_data_construction.md)). The checks are scripted (`analysis/audit/`, and the build reports in
`data/processed/`), so they rerun with every rebuild.

## 10.1 Coverage against the trading calendar

| Source | Trading days expected | Missing | Explanation and handling |
|---|---|---|---|
| Combined open interest | 4,120 (Feb 2010 to 27 Oct 2026) | 0 after reassignment | The file for 1 October 2015 is stored under 2 October (a holiday) and is moved to its inner date. 13 files of May and June 2012 are corrupt at NSE (before the main sample). |
| Securities in ban | same | 6 May 2025 (not found at NSE); 19 Feb and 25 Aug 2014 (only misdated files) | Lists imputed from the previous day's "No Fresh Positions" flags and from continuing spells (7 stock-days, flagged). Before the fix, one 2025 spell was split in two and ban days were missing. |
| F&O bhavcopy | 2,917 (2015 to 27 Oct 2026) | 30 Mar 2021 (not found at NSE) | Membership is bridged across the gap; no basis for that day. |
| Cash bhavcopy | same | none | |
| Delivery file | same | none | Empty marker files exist only for holidays. |
| Nifty index file | same | 9 days in 2015 and 2016 (not found at NSE) | Used only for a validation series. |
| 3-month interbank rate | monthly | October 2026 not yet published | Last value carried forward at most two months, flagged `r_filled` (7,225 basis rows). |

No file of any source falls on a weekend.

## 10.2 Duplicates and format changes

- No duplicate futures rows (stock, day, expiry) and no duplicate cash rows (stock, day, series).
- NSE's change of file format (legacy to UDiFF) on 8 July 2024 is seamless: 181 stock futures on both sides of the
  switch, and open interest continuous across it. The UDiFF traded-volume field counts contracts; this is handled.
- Expiry dates switch from Thursday to Tuesday from the September 2025 expiry, as announced; every F&O stock-day has a
  near-month contract and almost all have a next-month contract.

## 10.3 The ban data against the exchange's rules

| Check | Result |
|---|---|
| Stocks flagged "No Fresh Positions" on day t versus the official list for day t+1 | 11,753 of 11,764 flags agree (99.9%); 5 listed stocks were not flagged. The differences trace to the COVID halving days of March 2020, one corrupt 2012 file and single dated files. |
| Entry rule: utilisation above 95% on the day before a spell starts | 99.4% of 2,181 spells (median 1.006) |
| Exit rule: utilisation at or below 80% on the last ban day | 99.7% of spells (99.9% at or below 82%) |
| COVID halving dates | MWPL halved for 61 stocks in the files of 20 to 27 March 2020; restored for 70 stocks on 26 November 2020, as in the regulatory record |
| 1 October 2025 formula | The new MWPL of the 85 stocks at 15% of free float is reproduced exactly from pre-reform free float (MWPL / 0.20) |

## 10.4 Open interest against the price files

Market-wide open interest in the combined file (the exchange's own number, used for bans) was compared with the sum of
open interest over all stock futures and stock options in the F&O bhavcopy for the same stock and day:

- equal (within 1%) on 95% of stock-days;
- on expiry days the bhavcopy still counts the expiring contracts and the combined file does not: this explains 83% of
  the differences;
- the rest: April 2021 (all stocks, about 2 to 3% apart, not explained by a one-day shift) and small subsets of stocks in
  early 2015, February 2016 and February 2020 (1 to 3% apart).

Because the combined file is the one the exchange uses to decide bans, it remains the source for utilisation; the
differences are recorded here. The set of stocks in the combined file and the set of stock futures in the bhavcopy agree
on 99.97% of stock-days (the combined file lists a new stock one day before its futures start trading).

## 10.5 Prices and the basis

| Check | Result |
|---|---|
| Futures VWAP inside the day's [low, high] range | 99.77% of traded rows; the rest (wrong lot size after a mid-contract lot change) set to missing |
| Legacy rows whose lot was snapped above the gcd | 2.0% |
| Futures rows with a matching cash price | 100% |
| Basis distribution across the July 2024 format change | Stable (yearly medians between -1.8 and +9.2 bp; no break in 2024) |
| Basis convergence toward expiry | Median absolute basis falls from 16.6 bp (21 to 35 days) to 12.8 bp (last 3 days) |
| Corporate events | Non-dividend events (e.g. NTPC bonus debentures, March 2015) move the futures price relative to the stock; such contracts (0.9% of rows) are flagged and excluded from the main sample |
| Dividends | Adjusting with actual ex-dates over-corrects a little on dividend days (probably dividends not yet announced earlier in the contract's life); dividend contracts are flagged and excluded from the main sample |
| Extreme values | 0.65% of clean stock-days lie more than 200 bp from zero, mainly stocks under heavy selling pressure; kept, handled by winsorising in the main estimates |
| Cost-of-carry inputs (Nifty futures) | Implied financing rate (with the index's trailing dividend yield, November to March contracts) moves with the interbank rate: monthly correlation 0.47, mean gap 0.7 percentage points |

## 10.6 Results announcements

This is where the audit found the largest problem.

1. **The results-filings feed is incomplete.** Before 2024 about 10% of F&O stock-quarters had no filing (26% for the
   June 2022 quarter).
2. **Its timestamps are often late re-filings.** Compared with the board meeting that approved the results, the feed's
   time falls on the meeting day only 55% of the time, the next day 29%, and six or more days later 12%. In 2017 and 2018
   most times are days or weeks late. Example: Hindustan Unilever's June 2018 results were released on 16 July 2018 at
   15:38 (board meeting the same day); the feed says 3 August 2018. Spot checks of other stocks (Escorts, IPCA
   Laboratories, MRPL, HUDCO, Tata Chemicals) show the same pattern.
3. **Old records carry the current symbol.** NSE's event feeds label historical records with the company's present symbol
   (for example the filings of CADILAHC appear under ZYDUSLIFE), so renamed companies seemed to have no results.

Fixes ([07_data_construction.md](07_data_construction.md), 7.8): the release time is now the earliest of the
"Financial Result Updates" announcement (the exchange's dissemination time) and the filing; board meetings fill
remaining quarters and flag late re-filings; every record is mapped to the symbol trading on the event date through the
ISIN history of the cash bhavcopy.

After the fixes:

| Measure | Result |
|---|---|
| F&O stocks with a results event for the quarter | 98% to 100% in every quarter 2015 to 2026 (median 99.1%) |
| Remaining gap | 86 stock-quarters, almost all of companies listed only on BSE and traded on NSE under "permitted to trade" (MCX; Abbott India; Nestle India before 2023), whose results are filed with BSE |
| Timed release on the board-meeting day, or the next day | 90.2% and 6.5% (where both are known) |
| F&O events with a known release time | 99.0% |
| Change relative to the feed alone | For 51.5% of the F&O events the event day moved earlier (36% by two or more calendar days); none moved later |

## 10.7 Returns and market capitalisation

| Check | Result |
|---|---|
| Split and bonus factors against the price jump on the ex-date | 99.6% of 769 ex-dates agree within 25% (after multiplying same-day split and bonus records) |
| Unexplained daily moves above 50% | 448 (0.84 per 10,000 stock-days), mostly sub-rupee stocks and relistings; flagged |
| Likely corporate actions missing from NSE's feed | 424 falls at standard split/bonus ratios with no record; return set to missing |
| AMFI rows parsed | 98% to 100% of serial numbers in every half-year except Jan to Jun 2018 (96%) |
| NSE stocks matched to an AMFI market cap | 89% to 97% by count, 95% to 99.8% by traded value, 93% to 99.7% of F&O stocks, depending on the half-year |
| AMFI total market cap against free-float market cap from the MWPL (F&O stocks) | implied free-float share between 0.05 and 1.05 for 99.5% of stock-halves; median 0.48 |
| Back-cast of market cap (share count from 3 years later) | median error 0.3%; within 10% for 82%; 90th percentile error 20% |
| Market cap available | 94.7% of cash stock-days; 99.4% to 99.6% of F&O entry and exit stocks in the six months before their event |

## 10.8 Corporate actions

Monthly record counts are stable (about 1,900 to 2,700 per year), with no sign of truncation by the API, and the
dividend parser separates dividends from splits ("sub-division") and other events.

## 10.9 What the audit does not cover

- Intraday data are not used, so whether a future traded in its last half hour (which decides NSE's theoretical
  settlement price) is not observed; the `theoretical_settle` flag only marks days with no trades at all.
- Dividends are adjusted with their actual ex-dates, not with the information available at the time; dividend contracts
  are therefore excluded from the main sample.
- Results of companies that file only with BSE are missing (10.6).
- Market caps before July 2017 are back-cast from later share counts (10.7); a commercial database (CMIE Prowess) could
  verify them.
