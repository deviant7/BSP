# 6. Data sources

All data are public. Everything comes from NSE archive files and NSE web endpoints, except the interest rate, which comes
from the OECD Main Economic Indicators via FRED. Every file is downloaded by a script in `data_pipeline/`, so the data
set can be rebuilt from scratch ([12_reproducibility.md](12_reproducibility.md)). Raw downloads are kept in `data/raw/`,
which is not committed (about 1.2 GB).

Archive URLs below start with `https://nsearchives.nseindia.com/`. Web endpoints start with `https://www.nseindia.com/api/`.

## 6.1 Summary

| # | Source | Content used | Frequency | Coverage | Script |
|---|---|---|---|---|---|
| 1 | Combined open interest file (`combineoi`) | MWPL, market-wide open interest, futures-equivalent OI (from 1 Oct 2025), next-day status ("No Fresh Positions") | Daily | 1 Feb 2010 to 27 Oct 2026 | `download_nse_mwpl.py` |
| 2 | Securities in ban (`fo_secban`) | Official list of stocks in the ban for the trade date | Daily | Feb 2010 to 27 Oct 2026 | `download_nse_mwpl.py` |
| 3 | F&O bhavcopy | Stock and index futures: prices, traded value, contracts, OI, lot size; options activity summed per underlying | Daily | 1 Jan 2015 to 27 Oct 2026 | `download_nse_prices.py` |
| 4 | Cash bhavcopy | Stock prices (open, high, low, close, last, previous close), traded quantity and value, number of trades, ISIN | Daily | 1 Jan 2015 to 27 Oct 2026 | `download_nse_prices.py` |
| 5 | Security-wise delivery file (MTO) | Quantity traded and quantity delivered per stock | Daily | 1 Jan 2015 to 27 Oct 2026 | `download_nse_prices.py` |
| 6 | Corporate actions | Dividends, splits, bonuses, rights and other events, with ex-dates | Event list, by month | Jan 2014 to Nov 2026 | `download_rates_corpactions.py` |
| 7 | Financial results filings | Release timestamp of each quarterly and annual result, period end, links to XBRL filings | Event list, by month | 2014 to Oct 2026 | `download_results_filings.py` |
| 7b | Financial result announcements | Exchange dissemination time of each results filing (category "Financial Result Updates") | Event list | 2014 to Oct 2026 | `download_results_filings.py ... resultupdates` |
| 8 | Board meetings | Date and purpose of board meetings (used to fill gaps in source 7) | Event list | 2014 to 2026 | `download_results_filings.py ... boardmeetings` |
| 9 | All-index closing file | Nifty 50 close, P/E, P/B and trailing dividend yield | Daily | 2015 to 27 Oct 2026 | `download_index_close.py` |
| 10 | Interest rates (FRED, OECD MEI) | India 3-month interbank rate (main), call money rate | Monthly | 2011 to Sep 2026 | `download_rates_corpactions.py` |

## 6.2 Details by source

### (1) Combined open interest: `archives/nsccl/mwpl/combineoi_DDMMYYYY.zip`
One zip per trading day containing a CSV with one row per F&O stock: date, ISIN, scrip name, NSE symbol, MWPL (shares),
open interest (shares, all futures and options across exchanges), from 1 October 2025 the futures-equivalent open
interest, and "Limit for Next Day" (the text "No Fresh Positions" marks stocks in the ban the next day). This is the file
the exchange itself uses to decide bans, so it is the authoritative source for the treatment.

### (2) Securities in ban: `archives/fo/sec_ban/fo_secban_DDMMYYYY.csv`
A header line "Securities in Ban For Trade Date DD-MON-YYYY" followed by numbered symbols. Empty lists are possible.

### (3) F&O bhavcopy
- Legacy format (to early July 2024): `content/historical/DERIVATIVES/YYYY/MON/foDDMONYYYYbhav.csv.zip` with
  INSTRUMENT (FUTSTK, FUTIDX, OPTSTK, OPTIDX), SYMBOL, EXPIRY_DT, STRIKE_PR, OPTION_TYP, OPEN, HIGH, LOW, CLOSE,
  SETTLE_PR, CONTRACTS, VAL_INLAKH (traded value in lakh rupees), OPEN_INT, CHG_IN_OI. **No lot size.**
- UDiFF format (from 8 July 2024): `content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip` with FinInstrmTp
  (STF, IDF, STO, IDO), TckrSymb, XpryDt, prices including LastPric and UndrlygPric, SttlmPric, OpnIntrst, ChngInOpnIntrst,
  TtlTradgVol (**number of contracts**), TtlTrfVal (rupees), TtlNbOfTxsExctd (number of trades), NewBrdLotQty (lot size).
- The download script keeps every futures row (stock and index) and sums options per underlying (contracts, value, OI).

### (4) Cash bhavcopy
- Legacy: `content/historical/EQUITIES/YYYY/MON/cmDDMONYYYYbhav.csv.zip` (SYMBOL, SERIES, OHLC, CLOSE, LAST, PREVCLOSE,
  TOTTRDQTY, TOTTRDVAL, TOTALTRADES, ISIN).
- UDiFF: `content/cm/BhavCopy_NSE_CM_0_0_0_YYYYMMDD_F_0000.csv.zip` (same fields under UDiFF names).
- Series kept: EQ (normal), BE and BZ (trade-for-trade). All listed stocks are kept, not only F&O stocks, because the
  F&O entry and exit tests use the whole cash market.

### (5) Delivery: `archives/equities/mto/MTO_DDMMYYYY.DAT`
Record type 20 gives, per symbol and series, the quantity traded, the deliverable quantity and the delivery percentage.

### (6) Corporate actions: `api/corporates-corporateActions?index=equities&from_date=..&to_date=..`
One JSON list per month: symbol, series, subject (free text, e.g. "Dividend - Rs 5 Per Share", "Bonus 1:1",
"Face Value Split (Sub-Division)"), ex-date and record date.

### (7) Results filings
- To the quarter ended December 2024: `api/corporates-financial-results?index=equities&period=Quarterly|Annual&from_date=..&to_date=..`
  (symbol, ISIN, period from and to dates, broadcast timestamp, consolidated or standalone, audited or not, XBRL link).
- From the quarter ended March 2025: `api/integrated-filing-results?...&type=Integrated Filing- Financials&size=20000`
  (paginated; the script checks that the number of records equals the reported total).

### (7b) Financial result announcements: `api/corporate-announcements?index=equities&from_date=..&to_date=..&subject=Financial%20Result%20Updates`
Symbol, dissemination timestamp (`an_dt`) and a text such as "X Limited has submitted to the Exchange the financial
results for the period ended June 30, 2024". Downloaded in four-day windows. This is the first public release time of
each result.

### (8) Board meetings: `api/corporate-board-meetings?index=equities&from_date=..&to_date=..`
Symbol, meeting date, purpose (e.g. "Results", "Financial Results/Dividend"), intimation timestamp. Downloaded in
half-month windows. Used to fill quarters missing from sources 7 and 7b and to detect re-filing times (see
[07_data_construction.md](07_data_construction.md), 7.8).

### (9) All-index closing file: `content/indices/ind_close_all_DDMMYYYY.csv`
One row per index; the Nifty 50 row is kept (close, P/E, P/B, dividend yield). Used only to validate the cost-of-carry
inputs with Nifty futures.

### (10) Interest rates: FRED series `INDIR3TIB01STM` (main) and `IRSTCI01INM156N`
Monthly averages in percent per year, published with a lag of about one month.

## 6.3 Sources not used, and why

| Source | Reason |
|---|---|
| `sec_bhavdata_full` (cash file with delivery and average price) | Not available in the archive for early years (2019 returns 404); sources 4 and 5 together give the same information for the whole sample. |
| Futures settlement prices as the main price | NSE sets a theoretical cost-of-carry price on days without trades in the last half hour, which would bias the basis toward zero mechanically. Settlement-based measures are kept only as a secondary, flagged measure. |
| Commercial databases (e.g. CMIE Prowess) | Not needed: free float follows from the MWPL, results dates and XBRL links come from NSE, and every other input is in the NSE archives. |

## 6.4 Inputs still to be collected (do not affect anything built so far)

| Input | Use | Source |
|---|---|---|
| Arbitrage-fund assets and flows | Arbitrage-capital hypothesis (H4) | AMFI monthly data (separate category from mid-2018) |
| Earnings per share from XBRL filings | Standardised unexpected earnings (secondary surprise measure) | XBRL links already stored with each announcement |
| Securities lending (SLB) activity | Friction index (H1) | NSE SLB bhavcopy |
| Index dividends | Sharper validation with Nifty futures | NSE index data |
