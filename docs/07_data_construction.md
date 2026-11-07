# 7. Data construction and cleaning rules

This page states every rule used to turn the raw files ([06_data_sources.md](06_data_sources.md)) into the analysis
data sets, including each quirk of the NSE files and how it is handled. The code is in `data_pipeline/`; each builder
writes a plain-text report of its counts and checks to `data/processed/*_report.txt` or `build_report.txt`.

**Separation of treatment and outcome.** The treatment-side builders (MWPL, open interest, bans, F&O membership) never
read prices; the outcome builder (basis) never reads ban status or utilisation. This keeps the data build blind
([09_empirical_design.md](09_empirical_design.md), 9.1).

## 7.1 Trading calendar

The trading calendar is the set of dates with an NSE combined open-interest file (2010 onward) together with the dates of
the cash price files (2015 onward). Weekends never appear. A file dated on a holiday is treated as misdated (7.2).

## 7.2 MWPL, open interest and ban panel (`build_mwpl_panel.py`)

Output: `mwpl_oi_panel.csv.gz`, one row per trading day and F&O stock: `date, symbol, isin, mwpl, oi, futeq_oi, util,
util_futeq, no_fresh_next_day`; and `ban_days.csv.gz`, one row per stock-day in the ban: `date, symbol, source`.

Rules, in the order applied:

1. **Read every CSV member of each zip.** Some zips bundle earlier days' files (for example the files of 1 and
   2 July 2025 also contain 30 June 2025). Each member is dated by its own file name. Where a member duplicates a day that
   has its own file, the day's own file wins.
2. **Damaged zips.** If a zip's central directory is damaged, the CSV is recovered by scanning the local file headers.
   Thirteen files from May and June 2012 are corrupt at NSE and cannot be read; they fall before the main sample.
3. **Dates inside files.** NSE writes dates as DD-MON-YYYY and, in some years, DD-MON-YY; both are parsed.
4. **Misdated files.** If the date printed inside a file differs from its file-name date, the file is moved to the inner
   date when no other file covers that date, and dropped otherwise. Examples: the file named 2 October 2015 (a holiday)
   holds 1 October 2015 and is moved; the file named 2 November 2012 holds 5 November and is dropped because 5 November has
   its own file.
5. **Placeholder symbols.** In some files the symbol field reads "Not available in NSE-F&O" (713 rows). The symbol is
   restored from the same ISIN on the nearest date where it is given (204 distinct cases). On days when a company changed
   ISIN, the restored row can duplicate a row already present; the restored copy is dropped (25 rows).
6. **Numbers.** Thousands separators are removed. MWPL values can have nine digits; they are stored as integers, never
   with a fixed number of significant digits.
7. **Utilisation.** `util = oi / mwpl` (gross open interest). From 1 October 2025 the ban test uses
   `util_futeq = futeq_oi / mwpl` (futures-equivalent open interest). The utilisation that applies on day t is the one
   measured at the end of day t-1.
8. **Ban list.** The official list for each trade date is read from the securities-in-ban files. Trailing commas in
   symbols are removed. Misdated ban files are handled as in rule 4.
9. **Missing ban lists.** On trading days with no official list (6 May 2025 returns "not found" at NSE; 19 February and
   25 August 2014 have only misdated files), the list is **imputed**: stocks flagged "No Fresh Positions" in the
   previous day's open-interest file (they enter the ban that day), plus stocks in the ban on both the previous and the
   next trading day (the spell continues). Imputed rows carry `source = imputed` (7 stock-days in total).
10. **Consistency check.** The stocks flagged "No Fresh Positions" on day t must be the stocks in the next day's official
    list. The check is run on all days that have an official list (results in
    [10_data_quality_audit.md](10_data_quality_audit.md)).

## 7.3 Ban spells (`describe_bans.py`)

A **ban spell** is a run of consecutive trading days on which a stock is in the ban. Output `ban_spells.csv.gz`: symbol,
start, end, length in trading days. Spells are assigned to the year in which they start.

## 7.4 F&O membership and entry and exit events (`build_fno_events.py`)

1. **Membership.** A stock is in the F&O segment on day t if stock futures on it are listed in that day's F&O bhavcopy.
   The exchange's test symbol NSETEST is removed. (The combined open-interest file lists a new stock one day before its
   futures start trading, because its limits apply to the next day; membership therefore uses the bhavcopy.)
2. **Missing file.** The F&O bhavcopy of 30 March 2021 is missing at NSE. Consecutive membership is counted over days
   that have an F&O file, so this gap is not treated as an exit and re-entry.
3. **Renames.** A spell that ends on day k and another symbol's spell that starts on day k+1 with the same ISIN (taken from
   the cash bhavcopy) are one stock that changed its symbol (for example ZOMATO to ETERNAL). Renames are not events.
4. **Events.** An **entry** is the first day of a membership spell (other than the sample start); an **exit** is the
   first trading day after a spell ends (other than the sample end).
5. **Event types.** An entry is flagged "recent listing" if the stock had fewer than 60 cash trading days before entry
   (a new listing rather than a change of status). An exit is flagged "no cash trading after exit" if the stock traded for
   fewer than 5 days in the cash market afterwards (merger, delisting or unlinked symbol change). Only the other exits are
   **eligibility exits**, where the stock keeps trading without derivatives.

Outputs: `fno_membership.csv.gz` (date, symbol, isin), `fno_events.csv` (date, symbol, type, isin, cash days before or
after, note).

## 7.5 Price files (`download_nse_prices.py`)

Each day's F&O bhavcopy, cash bhavcopy and delivery file is reduced to compact CSVs under `data/raw/prices/`:

- `fut/`: every futures row (stock and index): date, instrument (legacy FUTSTK and FUTIDX are mapped to STF and IDF),
  symbol, expiry, open, high, low, close, last, settlement price, underlying price (UDiFF only), contracts, traded value in
  rupees, quantity, number of trades, open interest, change in open interest, lot size (UDiFF only), and the file format.
- `optsum/`: options summed per underlying and instrument: contracts (or quantity), traded value, open interest.
- `cash/`: series EQ, BE and BZ: prices, traded quantity and value, trades, ISIN.
- `deliv/`: quantity traded and deliverable quantity per symbol and series. On days the delivery file is missing at NSE
  (all of them holidays), an empty marker file is written so the download is not retried.

Format details handled: in the UDiFF F&O file the traded-volume field counts **contracts**; traded value is in rupees in
UDiFF and in lakh rupees in the legacy file (converted).

## 7.6 Lot sizes for the legacy futures files

The legacy F&O bhavcopy does not report the lot size, which is needed to turn traded value into a price. Rules:

1. Open interest and the change in open interest are whole multiples of the lot. For each contract (stock and expiry) the
   **greatest common divisor** of all non-zero values of both is a first estimate.
2. When the lot changes during a contract's life (stock splits, lot revisions), the gcd falls below the true lot. A daily
   estimate, traded value / (contracts x mid-price of the day's high and low), is **snapped to the nearest multiple** of
   the gcd. Rows where this changes the lot are flagged (`lot_snapped`; 2.0% of legacy rows).
3. UDiFF files give the lot directly.

## 7.7 The basis panel (`build_basis.py`)

Output `basis_panel.csv.gz`: one row per stock, day and contract, for the near (k = 0) and next (k = 1) month.

1. **Futures VWAP.** `F_vwap = traded value / (contracts x lot)`. Rows with no contracts traded have no VWAP. If the
   VWAP falls outside the day's [low, high] range (with 0.5% tolerance), the lot size is wrong for that row and the VWAP
   is set to missing (0.23% of traded rows).
2. **Contract order.** Within each stock and day, contracts are ordered by expiry; k = 0 is the nearest.
3. **Cash VWAP.** `S_vwap = traded value / traded quantity`, from the EQ series (BE or BZ if EQ is absent). Every
   futures row has a matching cash row.
4. **Rate.** `r` = the monthly 3-month interbank rate, applied to every day of the month. The OECD series is published
   with a lag of about one month; months after the last published value use the last value, at most two months forward,
   and are flagged `r_filled = True` (October 2026 in the current build).
5. **Time to expiry.** `tau` = calendar days to expiry / 365.
6. **Dividends.** Cash dividends are parsed from the corporate-action subject text with the pattern "dividend ... Rs X"
   (the word "dividend" is required: the text "sub-division" also contains the letters "div"). Several dividends in one
   announcement are added; an event listed twice (for example a revised purpose) is counted once. For each row, `pv` is
   the present value at rate r of the dividends going ex after day t and on or before expiry.
7. **Other corporate events.** Bonus issues, splits, rights, debentures, demergers, schemes, capital reductions,
   buybacks, distributions, mergers and amalgamations are found by keyword. `event_in_life = True` if such an event goes
   ex within the contract's remaining life (0.9% of rows). Example: the NTPC bonus debentures of March 2015.
8. **Basis.** `m_vwap = ln F_vwap - ln(S_vwap - pv) - r * tau` (main measure, see
   [08_variables_and_measures.md](08_variables_and_measures.md)).
9. **Close-based basis.** `m_close` uses the futures closing price and the cash closing price (secondary measure).
   `theoretical_settle = True` when the contract had no trades all day (UDiFF: number of trades is zero; legacy:
   contracts is zero), the case in which NSE's settlement price is certainly a theoretical value. This is a lower bound:
   the daily files do not show whether a contract traded in the last half hour.
10. **Implied repo.** `r_implied = [ln F_vwap - ln(S_vwap - pv)] / tau`; `rel_repo` = r_implied minus the day's
    cross-sectional median for the same contract order, using rows with at least 7 calendar days to expiry.

## 7.8 Results announcements (`build_announcements.py`)

Output `announcements.csv.gz`: one row per stock and period end (a quarter).

Three NSE sources are combined, because none is complete on its own:

| Source | Gives | Weakness found in the audit |
|---|---|---|
| Results filings (source 7) | Period end, broadcast time, XBRL links | Misses about 10% of F&O stock-quarters before 2024; its time is often that of a later re-filing (in 2017 and 2018 most times are days or weeks after the results were first released) |
| "Financial Result Updates" announcements (source 7b, category of the corporate-announcements feed) | The exchange's dissemination time of each results filing, to the second | Period end must be read from the text ("...for the period ended 30-Jun-2018") |
| Board meetings (source 8) | The date of the board meeting that approved the results | No time of day |

Listed companies must disclose results within 30 minutes of the end of the board meeting that approves them, so the
meeting date bounds the release date.

Rules:

1. **Period.** For filings, the period end given in the filing. For announcements, the date after "period ended" in the
   text, moved to its month end; if it cannot be read or is implausible (before the announcement or more than 200 days
   earlier), the last quarter end before the announcement. For board meetings, the last quarter end before the meeting.
2. **Release time.** The earliest timed release across the announcements and the filings for that stock and quarter
   (`release_src` = announcement or filing).
3. **Re-filing guard.** If a board meeting on results is known and the only timed release comes from the filing feed
   and is more than one calendar day after the meeting, that time is treated as a re-filing: the release is the meeting
   date with unknown time (`release_src = board_meeting`, `timing_known = False`). An announcement time is kept even if
   it is later than the meeting, because that usually means the meeting was postponed.
4. **Board-meeting-only quarters.** Quarters known only from a board meeting get the meeting date, time unknown. For
   board meetings, the latest intimation for a stock and quarter gives the final date; status notices (postponed,
   rescheduled, adjourned, cancelled) are not used as dates.
5. **Event day.** Day 0 is the release day if the result was released before the 15:30 close, otherwise the next trading
   day. If the time is unknown, day 0 is the next trading day after the release date (most results are released after
   the close); the announcement-return window [-1, +1] then contains the release day either way. The trading calendar
   used here starts in 2010, so that events before 2015 are dated correctly.
6. **Plausibility.** Events released before the period end or more than 200 days after it are dropped.
7. **XBRL links** are kept for the earliest standalone and the earliest consolidated filing.

## 7.9 Nifty futures validation series

`nifty_futures.csv.gz` keeps the near-month Nifty future (VWAP, close, underlying, contracts) for a check of the
cost-of-carry inputs against the index's published dividend yield; `nifty50_daily.csv` keeps the index close and
dividend yield.

## 7.10 Daily returns adjusted for corporate actions (`build_returns.py`)

NSE's previous-close field is **not** adjusted for splits or bonuses (Tata Steel's 1:10 split on 28 July 2022 shows a
previous close of Rs 959.4 and a close of Rs 100.35). Rules:

1. One row per stock and day (series EQ, else BE, else BZ). Rights-entitlement symbols ("-RE") and exchange-traded
   funds (symbols containing ETF or ending in BEES) are dropped.
2. Share-count factor k on an ex-date: a split from face value a to b gives k = a/b; a bonus of x new shares for every
   y held gives k = (x + y)/y; a split and a bonus on the same day multiply (NSE lists them as separate records).
   Bonus debentures and preference shares are not bonuses of shares.
3. Return = (close x k + dividend) / previous close - 1 on an ex-date, close / previous close - 1 otherwise.
4. Every factor is checked against the price jump on the ex-date: 99.6% agree within 25%.
5. Ex-dates of rights issues, demergers and schemes of arrangement: return set to missing (their price effect needs
   issue prices or values that the announcement text does not give reliably).
6. The first trading day of a symbol after 1 Jan 2015 (new listing, relisting, demerged entity): return missing (the
   previous close is a base price).
7. A fall whose price ratio is within 3% of a standard split or bonus ratio (1.25, 4/3, 1.5, 2, 2.5, 3, 4, 5, 10, 20)
   with no corporate action on record is treated as a corporate action missing from the feed: return missing, and the
   ratio is used as the share-count factor for market capitalisation (424 cases).
8. Other moves larger than 50% are kept and flagged `jump` (448 cases, mostly sub-rupee stocks and relistings).

## 7.11 Daily market capitalisation (`build_amfi_mcap.py`, `build_mcap.py`)

1. The 18 AMFI half-yearly lists are parsed: a record starts at its serial number and may wrap onto the next line; the
   ISIN is found by its structure (it is sometimes printed glued to the company name); the last number on the row is the
   average market cap across exchanges.
2. An adjusted price A_t = close_t x K_t is formed, where K_t is the cumulative product of share-count factors (7.10), so
   that A_t is comparable across splits and bonuses.
3. For each half-year h, the share count in adjusted units is S_h = AMFI average market cap_h / mean of A_t over h; AMFI
   rows are matched to stocks by ISIN within the half-year, else by the NSE symbol printed in the row.
4. Market cap on day t = A_t x S_h(t). Before a stock's first AMFI half-year (in particular all of January 2015 to June
   2017) the first S_h is used ("back-cast"); after its last, the last S_h. This ignores new issues and buybacks; tested
   inside the AMFI window, a share count taken from three years later is within 10% for 82% of stock-halves.

## 7.12 Outcomes for the F&O entry and exit tests (`analysis/h6_outcomes.py`)

- **Price delay**: calendar-week returns (at least 3 valid days in the week); value-weighted market return of the cash
  universe (weights = previous day's market cap); per stock and calendar year (at least 40 weeks), D1 = 1 - R2 of the
  regression on the contemporaneous market return / R2 with four weekly lags added. Stock-years with an average price
  below Rs 5 are excluded.
- **Size deciles**: each month, on the previous month-end market cap, over the whole cash universe; equal-weighted daily
  decile returns form the benchmark.
- **EAR** = cumulative return over days -1 to +1 around the results day 0 minus that of the stock's size-decile portfolio;
  **BHAR** = buy-and-hold return over days +2 to +64 minus that of the decile portfolio (at least 50 valid days);
  **bad news** = bottom tercile of EAR among all results in the same calendar quarter. Events with a day-0 price below
  Rs 5 are excluded (tick-size artefacts); duplicate (stock, day) events counted once; EAR and BHAR winsorised at 1% and
  99% within each year for the main estimates.

## 7.13 Securities lending (`download_slb.py`, `build_slb.py`)

Each daily SLBS bhavcopy is a padded, comma-separated file without a header: company name, symbol, series (tenure code),
contract expiry, a flag, previous close fee, open, high, low and close fee (Rs per share), a blank field, quantity (shares),
value (Rs), upper and lower bands, trade date and number of trades. The trade date inside each file equals the file date
for all 2,915 files. Rows with positive quantity are kept. The annualised lending fee of a trade is value / quantity /
cash closing price x 365 / calendar days to the SLB contract's expiry. SLB is not limited to F&O stocks: non-F&O stocks
account for 6% to 23% of trade records in each year from 2019 (eligibility was widened to liquid non-F&O stocks in 2013).

## 7.14 Arbitrage-fund assets (`download_amfi_monthly.py`)

From each monthly AMFI Excel report the arbitrage-fund category is read. April 2018 to March 2019 use an older layout
(net inflow and redemptions in one table, net assets in another, no average assets); from April 2019 a single row gives
schemes, folios, funds mobilised, redemptions, net inflow, net assets and average assets. Checks: net assets of
Rs 71,106 crore in April 2023 and Rs 1,98,981 crore in October 2024 match published figures. Monthly flow = net inflow /
previous month-end net assets.

## 7.15 Rules for the analysis samples

These are applied when the tests are run, not when the panels are built; they are fixed in the pre-analysis plan:

- **Contract choice:** near month, switching to the next month when 3 or fewer trading days remain to expiry.
- **Liquidity:** at least 5 futures contracts traded that day.
- **Main exclusions:** a dividend (`pv > 0`) or other corporate event (`event_in_life`) going ex within the contract's
  life; the first 20 trading days after F&O entry; rows whose lot size could not be recovered.
- **Outliers:** the basis is winsorised at the 1st and 99th percentiles within each year for the main estimates;
  robustness checks use unwinsorised values.
