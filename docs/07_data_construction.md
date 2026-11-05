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
   `theoretical_settle = True` when the contract had no trades (UDiFF: number of trades is zero; legacy: contracts is
   zero), the case in which NSE's settlement price is a theoretical value.
10. **Implied repo.** `r_implied = [ln F_vwap - ln(S_vwap - pv)] / tau`; `rel_repo` = r_implied minus the day's
    cross-sectional median for the same contract order, using rows with at least 7 calendar days to expiry.

## 7.8 Results announcements (`build_announcements.py`)

Output `announcements.csv.gz`: one row per stock and period end (a quarter).

1. **Filings.** Every standalone and consolidated filing for the period is read. The event's release time is the
   **earliest** broadcast time across them. XBRL links are kept for the standalone and the consolidated filing.
2. **Filling gaps from board meetings.** The legacy results feed lacks some filings (for example 52 of 198 F&O stocks have
   no filing for the June 2022 quarter there). For each stock and quarter missing from the filings, the board meeting on
   financial results is used: the period is the last quarter end before the meeting date; when a meeting is rescheduled,
   the latest intimation gives the final date. These events have a date but no time: `timing_known = False`,
   `src = board_meeting`.
3. **Event day.** Day 0 is the release day if the result was released before the 15:30 close, otherwise the next trading
   day. For board-meeting events, day 0 is the meeting day (the next trading day if it is a holiday). The trading calendar
   used here starts in 2010, so that events before 2015 are dated correctly.
4. **Plausibility.** Events released more than 200 days after the period end, or before it, are dropped.

## 7.9 Nifty futures validation series

`nifty_futures.csv.gz` keeps the near-month Nifty future (VWAP, close, underlying, contracts) for a check of the
cost-of-carry inputs against the index's published dividend yield; `nifty50_daily.csv` keeps the index close and
dividend yield.

## 7.10 Rules for the analysis samples

These are applied when the tests are run, not when the panels are built; they are fixed in the pre-analysis plan:

- **Contract choice:** near month, switching to the next month when 3 or fewer trading days remain to expiry.
- **Liquidity:** at least 5 futures contracts traded that day.
- **Main exclusions:** a dividend (`pv > 0`) or other corporate event (`event_in_life`) going ex within the contract's
  life; the first 20 trading days after F&O entry; rows whose lot size could not be recovered.
- **Outliers:** the basis is winsorised at the 1st and 99th percentiles within each year for the main estimates;
  robustness checks use unwinsorised values.
