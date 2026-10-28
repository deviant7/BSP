# Data pipeline (NSE public archives)

All sources are free NSE archive files. Raw downloads go to `data/raw/` (git-ignored; re-creatable).
Processed, compact outputs go to `data/processed/` (committed when small).

## Sources verified (28 Oct 2026)
| Kind | URL pattern (`https://nsearchives.nseindia.com/` + …) | Coverage checked | Notes |
|---|---|---|---|
| MWPL & open interest | `archives/nsccl/mwpl/combineoi_DDMMYYYY.zip` | Feb 2010 → Oct 2026 (Jan 2010 = 404) | cols: Date, ISIN, Scrip Name, NSE Symbol, MWPL, Open Interest, [Future Equivalent Open Interest from 1 Oct 2025], Limit for Next Day ("No Fresh Positions" = in ban next day) |
| Securities in ban | `archives/fo/sec_ban/fo_secban_DDMMYYYY.csv` | 2010 → 2026 | "Securities in Ban For Trade Date DD-MON-YYYY" then `n,SYMBOL` |
| F&O bhavcopy (legacy) | `content/historical/DERIVATIVES/YYYY/MON/foDDMONYYYYbhav.csv.zip` | 2015 → Jul 2024 | INSTRUMENT, SYMBOL, EXPIRY_DT, STRIKE_PR, OPTION_TYP, OHLC, CLOSE, SETTLE_PR, CONTRACTS, VAL_INLAKH, OPEN_INT, CHG_IN_OI |
| F&O bhavcopy (UDiFF) | `content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip` | Jul 2024 → (2015 = 404) | FinInstrmTp (STF/IDF/STO/IDO), TckrSymb, XpryDt, ClsPric, **LastPric**, SttlmPric, **UndrlygPric**, OpnIntrst, TtlTradgVol (**contracts**), TtlTrfVal (₹), TtlNbOfTxsExctd, NewBrdLotQty |
| Cash bhavcopy (legacy) | `content/historical/EQUITIES/YYYY/MON/cmDDMONYYYYbhav.csv.zip` | 2019 checked | SYMBOL, SERIES, OHLC, CLOSE, LAST, PREVCLOSE, TOTTRDQTY, TOTTRDVAL, TOTALTRADES, ISIN |
| Cash bhavcopy (UDiFF) | `content/cm/BhavCopy_NSE_CM_0_0_0_YYYYMMDD_F_0000.csv.zip` | 2025 checked | same fields, UDiFF names |
| Delivery (MTO) | `archives/equities/mto/MTO_DDMMYYYY.DAT` | 2019, 2025 checked | record type 20: Sr, Symbol, Series, Qty traded, Deliverable qty, % |
| sec_bhavdata_full | `products/content/sec_bhavdata_full_DDMMYYYY.csv` | 2025 OK, 2019 = 404 | OHLC + AVG_PRICE + DELIV_QTY/PER (recent years only) |

## Scripts
- `download_nse_mwpl.py RAW START END` — combineoi + fo_secban (treatment side), 6 threads.
- `build_mwpl_panel.py RAW OUT` — stock-day panel (MWPL, OI, FutEq OI, utilisation, next-day ban flag) + ban list; cross-checks
  "No Fresh Positions" flags against the next day's ban list.
- `describe_bans.py PROCESSED FIGS` — treatment-side facts only: ban spells, rule checks (95% entry, 80% exit), MWPL changes
  (incl. 23 Mar 2020 halving, 1 Oct 2025 formula), utilisation density near 95%.
- `download_nse_prices.py OUT START END [workers]` — per-day compact files: futures rows (stock + index), options summary per
  underlying, cash EQ/BE/BZ series, delivery. Raw zips not kept.

## Measurement notes (from the model and NSE rules)
- NSE sets the futures settlement price at a **theoretical cost-of-carry value when a contract is not traded in the last half
  hour**, so a settlement-price basis is ≈ 0 by construction on such days. Use trade-based prices: daily VWAP of futures
  (value / (contracts × lot)) against daily VWAP of cash (TOTTRDVAL / TOTTRDQTY), and flag low-volume days.
- From 3 Aug 2026 the cash closing price of F&O stocks comes from a closing auction (measurement break for close-based measures).
- Lot sizes: UDiFF gives NewBrdLotQty; legacy files do not → lot size = (VAL_INLAKH × 1e5) / (CONTRACTS × average price), or
  NSE lot-size files.

## Blind protocol
Until the pre-analysis plan is written and tagged, no table or figure may relate an outcome (basis, returns, drift) to ban
status, utilisation or reforms. Treatment-side descriptives and outcome distributions on their own are allowed.
