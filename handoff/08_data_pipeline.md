# 08. Data pipeline deep dive

Polished version for outside readers: `docs/06_data_sources.md`, `docs/07_data_construction.md`,
`docs/10_data_quality_audit.md`. This page is the working reference: scripts, columns, every quirk and its fix.

## 8.1 Scripts and run order

All run from the repo root with `python3 -I`. Raw data in `data/raw/` (git-ignored); outputs in `data/processed/`.

| # | Script | Arguments | Reads | Writes | Time |
|---|---|---|---|---|---|
| 1 | `data_pipeline/download_nse_mwpl.py` | RAW START END | NSE archives | `raw/combineoi/combineoi_DDMMYYYY.zip`, `raw/secban/fo_secban_DDMMYYYY.csv`, `raw/download_log.tsv` | ~40 min, 6 threads |
| 2 | `download_nse_prices.py` | OUT START END [workers] | NSE archives (legacy + UDiFF F&O and cash bhavcopies, MTO) | `raw/prices/{fut,optsum,cash,deliv}/YYYYMMDD.csv`, `price_download_log.tsv` | ~2.5 h (resumable; exceeds the 2 h background limit, so restart if killed) |
| 3 | `download_rates_corpactions.py` | RAW Y0 Y1 | FRED (via curl), NSE corporate-actions API | `raw/rates/*.csv`, `raw/corpactions/ca_YYYYMM.json` | minutes |
| 4 | `download_results_filings.py` | RAW Y0 Y1 [mode] | NSE APIs | modes: (none) `raw/results/{Quarterly,Annual}_YYYYMM.json`; `integrated` `raw/results/Integrated_YYYYMM.json`; `boardmeetings` `raw/boardmeetings/bm_YYYYMM{a,b}.json`; `resultupdates` `raw/resultupdates/ru_YYYYMMDD.json` (4 threads) | 10 to 30 min each |
| 5 | `download_index_close.py` | OUT_CSV START END | NSE `ind_close_all` | `raw/indices/nifty50_daily.csv` (also copied to processed) | ~10 min |
| 6 | `build_mwpl_panel.py` | RAW OUT | combineoi, secban | `mwpl_oi_panel.csv.gz`, `ban_days.csv.gz`, `symbols.csv`, `build_report.txt` | minutes |
| 7 | `describe_bans.py` | PROC FIGS | panel, ban days | `ban_spells.csv.gz`, `descriptives.txt`, figs | minutes |
| 8 | `build_fno_events.py` | RAW OUT | prices/fut, prices/cash | `fno_membership.csv.gz`, `fno_events.csv`, `fno_events_report.txt` | minutes |
| 9 | `build_announcements.py` | RAW OUT | results, resultupdates, boardmeetings, prices/cash (ISIN history), panel, membership | `announcements.csv.gz`, `announcements_report.txt` | ~5 min |
| 10 | `build_basis.py` | RAW OUT | prices, corpactions, rates | `basis_panel.csv.gz` (git-ignored, 74 MB), `nifty_futures.csv.gz`, `basis_report.txt` | ~10 min, several GB RAM |
| 11 | `report_figs.py`, `report_tables.py` | PROC OUT | processed | `reports/figs/*.pdf`, `reports/tables/ban_by_year.tex` | seconds |
| 12 | `analysis/audit/audit_coverage.py`, `audit_prices.py`, `audit_oi_alignment.py` | RAW | raw + processed | stdout | minutes |

Separation (blind design): builders 1, 6, 7, 8 never read prices for outcomes; 10 never reads bans.

## 8.2 Processed data dictionary

**`mwpl_oi_panel.csv.gz`** (752,037 rows; 476 symbols; 4,120 days, 1 Feb 2010 to 27 Oct 2026):
`date, symbol, isin, mwpl` (shares, integer), `oi` (market-wide gross OI, shares), `futeq_oi` (from 1 Oct 2025),
`util = oi/mwpl`, `util_futeq = futeq_oi/mwpl`, `no_fresh_next_day` (True = in ban next trading day).

**`ban_days.csv.gz`** (11,765 rows): `date, symbol, source` (`list` official, `imputed` 7 rows).

**`ban_spells.csv.gz`** (2,181 spells 2010 to 2026; 1,788 starting 2015+): `symbol, spell, start, end, days`.

**`fno_membership.csv.gz`** (534,712 stock-days, 374 symbols, 2015 to 27 Oct 2026): `date, symbol, isin`.

**`fno_events.csv`** (410): `date, symbol, type` (entry/exit), `isin, cash_days_before_or_after, note`
("recent listing", "no cash trading after exit (merger/delisting/symbol change)" for 9 exits, blank otherwise).
239 entries, 171 exits (162 eligibility exits). Usable per PAP: 233 entries, 158 exits.

**`announcements.csv.gz`** (94,071): `symbol` (symbol trading on the event date), `period_end`, `released` (timestamp;
midnight if time unknown), `timing_known`, `release_src` (announcement / filing / board_meeting), `after_close`,
`event_day` (day 0), `lag_days`, `meeting` (board-meeting date), `filing_released`, `ann_released`, `n_filings`,
`n_announcements`, `xbrl_standalone`, `xbrl_consolidated`, `filing_src` (legacy/integrated).

**`basis_panel.csv.gz`** (1,066,167 rows; near k = 0 and next k = 1): `date, symbol, expiry, k, tau` (cal. days/365),
`F_vwap, S_vwap, close` (futures close), `S_close, n_contracts, lot_used, value_rs, oi, chg_oi` (shares), `S_qty, S_value,
S_trades, r` (decimal p.a.), `r_filled, pv` (PV of dividends ex in (t, expiry]), `div_yield_in_life, m_vwap` (main basis,
log units), `m_close, theoretical_settle` (no trades all day), `r_implied, rel_repo, lot_snapped, event_in_life, src`.

**`nifty_futures.csv.gz`**: `date, expiry, F_vwap, close, underlying, n_contracts` (near Nifty future).
**`nifty50_daily.csv`**: Nifty 50 close, P/E, P/B, dividend yield (2,908 days; 9 missing at NSE in 2015 and 2016).
**`symbols.csv`**: last symbol/ISIN/name per symbol in the panel.

Reports: `build_report.txt`, `descriptives.txt`, `fno_events_report.txt`, `announcements_report.txt`, `basis_report.txt`.

## 8.3 Raw file formats (key fields)

- combineoi CSV: `Date, ISIN, Scrip Name, NSE Symbol, MWPL, Open Interest, [Future Equivalent Open Interest], Limit for Next Day`.
- fo_secban: `Securities in Ban For Trade Date DD-MON-YYYY:` then `n,SYMBOL` lines.
- Legacy F&O: `INSTRUMENT (FUTSTK/FUTIDX/OPTSTK/OPTIDX), SYMBOL, EXPIRY_DT, STRIKE_PR, OPTION_TYP, OPEN, HIGH, LOW, CLOSE,
  SETTLE_PR, CONTRACTS, VAL_INLAKH, OPEN_INT, CHG_IN_OI` (no lot size).
- UDiFF F&O: `FinInstrmTp (STF/IDF/STO/IDO), TckrSymb, XpryDt, ..., ClsPric, LastPric, SttlmPric, UndrlygPric, OpnIntrst,
  ChngInOpnIntrst, TtlTradgVol (= contracts), TtlTrfVal (rupees), TtlNbOfTxsExctd, NewBrdLotQty`.
- Compact `prices/fut` columns: `date, inst, symbol, expiry, open, high, low, close, last, settle, underlying, contracts,
  value_rs, qty, trades, oi, chg_oi, lot, src` (in UDiFF rows the contract count is in `qty`; `contracts` is empty).
- Compact `prices/optsum`: `inst (OPTSTK/OPTIDX legacy; STO/IDO UDiFF), symbol, contracts or qty, value_rs, oi, date, src`.
- Cash: `date, symbol, series, open, high, low, close, last, prevclose, qty, value_rs, trades, isin`.
- MTO delivery: record type 20 → `date, symbol, series, qty_traded, deliv_qty, deliv_pct`.
- Corporate actions JSON: `symbol, series, subject, exDate, recDate, ...`.
- Results JSON (legacy): `symbol, isin, toDate, fromDate, broadCastDate, filingDate, consolidated, audited, xbrl,
  relatingTo, period ...`; Integrated: `symbol, qe_Date, broadcast_Date, consolidated, audited, xbrl ...`.
- Result updates JSON: `symbol, sm_isin, an_dt (DD-Mon-YYYY HH:MM:SS), desc ("Financial Result Updates"), attchmntText
  ("... financial results for the period ended 30-Jun-2018")`.
- Board meetings JSON: `bm_symbol, sm_isin, bm_date, bm_purpose, bm_desc, bm_timestamp (intimation)`.

## 8.4 Complete catalogue of data quirks and how they are handled

### combineoi (MWPL / OI)
1. 107 files write the year with two digits (DD-MON-YY): both formats parsed (they were silently dropped once).
2. Misdated files: `combineoi_02112012` holds 5 Nov 2012 (dropped: 5 Nov has its own file); `combineoi_02102015` holds
   1 Oct 2015 (reassigned; 2 Oct is a holiday).
3. Zips bundling several days (1 and 2 Jul 2025 contain 30 Jun 2025 too): read every member; day's own file wins.
4. 13 corrupt files 1 to 19 Jun 2012 (and May 2012): corrupt at NSE (re-download byte-identical); damaged zips otherwise
   recovered by scanning local file headers.
5. 713 placeholder symbols "Not available in NSE-F&O": restored from ISIN (204 cases); 25 restored rows dropped on ISIN-change
   days.
6. Never write MWPL with `float_format` (9-digit values lose precision; a bug once).
7. combineoi lists a new stock one day before its futures trade and drops exits a day early; PNBHOUSING had an MWPL row with
   OI = 0 for Aug to Dec 2019 without futures. Membership therefore comes from the bhavcopy.
8. OI vs bhavcopy: equal on 95% of stock-days; expiry days differ (bhavcopy counts expiring contracts); April 2021 about
   2 to 3% apart for all stocks (unexplained; not a one-day shift); small subsets early 2015, Feb 2016, Feb 2020.
   combineoi is NSE's own ban input and stays authoritative.
9. FutEq OI column only from 1 Oct 2025 (market-level FutEq was disseminated separately before the reform).

### fo_secban (ban list)
10. Trailing commas in symbols: stripped.
11. Misdated: 19 Feb 2014 file says 19 Mar; 25 Aug 2014 says 26 Aug (dropped; those days imputed).
12. 6 May 2025: no file at NSE (404). Imputed: previous day's "No Fresh Positions" flags plus stocks in the ban on both
    t-1 and t+1 (MANAPPURAM entered; RBLBANK continued). Before the fix a 2025 spell was split.
13. Flag vs list agreement 11,753 of 11,764 flags; residuals on 23 Mar 2020 (COVID halving day), 14 Jun 2012 (corrupt
    period), single dated files; 5 listed-not-flagged including 23 Jan 2024 IRCTC.

### F&O bhavcopy
14. 30 Mar 2021 missing at NSE (all URLs 404): membership bridged (it had created 156 fake exits/entries); no basis that day.
15. Legacy files lack lot size: gcd of all non-zero OI and Delta OI per contract, then snap the daily estimate
    value/(contracts x mid) to a multiple of the gcd (lots change mid-contract with splits/revisions; raw gcd failed for
    about 2.5%); 2.0% of legacy rows snapped (`lot_snapped`). VWAP outside [low, high] +/-0.5% → missing (0.23%).
16. UDiFF `TtlTradgVol` is contracts (stored in `qty`); value in rupees (legacy in lakh, converted).
17. OI and Delta OI are in shares in both formats (verified: OI/lot integer for >99%).
18. Format switch 8 Jul 2024 (some F&O old-format files stop in May 2024; both parsed): continuous (181 stocks).
19. Exchange test symbol NSETEST (6 Nov 2023): removed.
20. NSE theoretical settlement price on days without trades in the last half hour: use VWAPs; `theoretical_settle` marks
    only no-trade days (lower bound; near-month share ~0%, next-month 2.4% zero-contract rows).
21. Expiry weekday: Thursday until Aug 2025, Tuesday from the 30 Sep 2025 expiry; holiday expiries move earlier
    (e.g. a Monday 30 Mar 2026; Wednesdays pre-2025).

### Cash and delivery
22. Series priority EQ > BE > BZ for the basis; all kept for the cash universe.
23. Delivery (MTO) empty marker files only on holidays (167 of 3,084 files).
24. `sec_bhavdata_full` not available for early years (2019 = 404): not used.
25. Closing auction for F&O stocks from 3 Aug 2026: close-based measures have a break; VWAP basis less affected.
26. PREVCLOSE is **not** adjusted for corporate actions (verified 5 Nov 2026; handled in `build_returns.py`, see 45).

### Corporate actions and dividends
27. "sub-division" contains "div": the dividend regex requires the word "dividend" followed by "Rs/Re/INR X".
28. Same event listed twice ("purpose revised"): max per (symbol, ex-date).
29. Non-dividend events (bonus, split, rights, debentures, demerger, scheme, capital reduction, buyback, distribution,
    merger, amalgamation): `event_in_life`, excluded from the main sample (e.g. NTPC bonus debentures 20 Mar 2015, about -6%
    basis).
30. Ex-date dividend adjustment over-corrects (+9.7 bp vs +1.1 bp clean; unadjusted -48.8): probable look-ahead on not yet
    announced dividends → dividend contracts excluded; announcement-aware adjustment is a to-do.
31. Monthly counts stable (about 1,900 to 2,700 per year); no API caps.

### Results announcements
32. Legacy results API misses ~10% of F&O stock-quarters before 2024 (26% for Jun 2022 quarter).
33. Its broadcast times are often re-filing times: vs board meeting, same day 55%, next day 29%, >= 6 days 12%; in 2017 and
    2018 ~90% are >= 2 days late (HINDUNILVR Jun 2018: released 16 Jul 15:38, feed 3 Aug). Fixed via "Financial Result
    Updates" announcements (first dissemination) + board meetings (filing-only times > 1 day after meeting replaced by the
    meeting date, time unknown; 747 cases) .
34. **NSE feeds label old records with the CURRENT symbol and ISIN** (CADILAHC under ZYDUSLIFE etc.): records mapped to
    the symbol trading on the event date through the cash-bhavcopy ISIN history (ISINs that follow each other under one
    symbol within 15 days are linked as one company). This was most of the coverage gap.
35. Board-meeting purposes before 2018 read "Results", "Results/Dividend"; from 2018 "Financial Results...": match
    "result"; exclude status notices (postponed, rescheduled, adjourned, cancelled).
36. Results API changed to "Integrated Filing - Financials" from the Mar 2025 quarter (paginated: size=20000, compare
    totalCount).
37. Trading calendar for event days must start in 2010 (once pre-2015 events landed on 1 Jan 2015).
38. Unknown-time events: day 0 = next trading day after the release date.
39. Remaining gap: 86 stock-quarters, BSE-only listings (MCX; Abbott India; Nestle India before 2023).
40. Comparison with the old build: 51.5% of the 7,910 old F&O events moved earlier (36% by >= 2 calendar days), none later.

### Rates and index
41. FRED needs curl (Python connections dropped). Series end Sep 2026 at build time: last value carried forward at most
    two months (`r_filled`, 7,225 rows in Oct 2026).
42. Nifty index file: 9 days missing in 2015 and 2016; three April 2023 files write dates month-first.
43. Nifty futures check: Nov to Mar contracts, implied repo with trailing yield vs 3M interbank: monthly corr 0.47, mean gap
    +0.67 pp; from 2021 implied about 2 pp above (index-futures premium, economic). The UDiFF `UndrlygPric` equals the cash
    close within 2 bp.

### The user's F&O membership sheet (`fno_pit_3.xlsx`, not in repo)
44. 367 symbols x 2,463 dates (1 Jan 2016 to 23 Dec 2025), 0/1; contains index rows, 3 truncated symbols (MCDOWELL,
    TV, NAM), NSETEST, 4 special weekend sessions, but misses the 5 Diwali muhurat sessions. After cleaning it matched the
    bhavcopy membership on all 452,616 stock-days. Used only as a cross-check.

## 8.5 NSE access notes

- Archives `https://nsearchives.nseindia.com/...`: plain GET with a browser User-Agent works; holidays return 404.
- APIs `https://www.nseindia.com/api/...`: work with `User-Agent` + `Accept: application/json` + a `Referer` from the
  matching NSE page; **do not** fetch the homepage first (it returns 403 from the container).
- Useful endpoints: `corporates-corporateActions`, `corporates-financial-results`, `integrated-filing-results`,
  `corporate-board-meetings`, `corporate-announcements` (with `&subject=Financial%20Result%20Updates`).
- Keep request windows small (half-month or four-day) and check for suspicious round counts.

## 8.6 Added 5 Nov 2026: returns, market caps, analysis caches
| Script | Writes | Notes |
|---|---|---|
| `data_pipeline/build_returns.py RAW OUT` | `returns_daily.csv.gz` (git-ignored), `returns_report.txt` | columns date, symbol, isin, series, close, prevclose, qty, value_rs, k, k_used, div, ret, flag (other_ca / first_day / factor_mismatch / likely_missing_ca / jump) |
| `data_pipeline/build_amfi_mcap.py RAW OUT` | `raw/amfi_mcap/*.pdf`, `amfi_mcap.csv.gz`, report | 18 half-years; URLs hard-coded (names differ; 2026H1 on portal.amfiindia.com/spages/) |
| `data_pipeline/build_mcap.py OUT` | `mcap_daily.csv.gz` (git-ignored), `mcap_report.txt` | src amfi / backcast / forward / interpolated |
| `analysis/samples.py` | `data/processed/cache/basis_sample.pkl`, `futures_activity.pkl` (git-ignored) | shared samples per PAP §11 C1 |
| `analysis/h6_outcomes.py` | cache `delay_panel.pkl`, `event_outcomes.pkl` | D1 delay, VR5, covariates; EAR, BHAR, bad/good |
More quirks: 45. NSE PREVCLOSE unadjusted for corporate actions. 46. Split and bonus on the same day are separate CA records
(multiply factors). 47. CA feed misses some splits/bonuses (424 inferred). 48. ETFs trade in EQ series; '-RE' rights
entitlements in BE. 49. Sub-rupee stocks tick 0.05 → 0.10 (100% "returns"); price filter Rs 5 for event outcomes.
50. AMFI PDFs: wrapped rows; ISIN glued to names; Jan–Jun 2018 parses 96%. 51. Results XBRL links blank before 2018; NSE
shareholding API only from 2021. 52. pdftotext needed.
