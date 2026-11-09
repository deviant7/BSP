# 16. A constraint index for Indian stocks

A quarterly index of how hard arbitrage is in each NSE-listed stock, built only from frictions (never from mispricing
measures or ban status), published as a reusable data set: `data/processed/constraint_index_q.csv.gz`. Specification
fixed before it was built in the plan's deviations log (§11.14, C17). Code `analysis/constraint_index.py`; output
`analysis/output/constraint_index.txt`.

## 16.1 Construction

- Universe: NSE stocks in series EQ, BE and BZ with a quarter-end price of at least Rs 5 and at least 40 trading days in the
  quarter, 2015 Q1 to 2026 Q3: 80,042 stock-quarters, 3,310 stocks (11% of them F&O stock-quarters).
- Components, per stock and quarter:

| Component | Definition | Loading |
|---|---|---|
| No short channel | 1 if the stock is not in the F&O segment at quarter end (no stock futures; not eligible for short selling) | +0.49 |
| SLB scarcity | 1 - share of trading days with any securities-lending trade in the stock | +0.45 |
| Spread | Corwin-Schultz (2012) estimate from daily high and low prices, with the overnight-gap adjustment | +0.43 |
| Illiquidity | log of mean absolute daily return per Rs crore traded (Amihud 2002) | +0.49 |
| Idiosyncratic volatility | standard deviation of residuals of daily returns on the Nifty 50 return | +0.37 |

- Each component is standardised within the quarter; the index is the first principal component (53% of the variance),
  standardised within the quarter; terciles are also provided. Loadings re-estimated year by year stay within 0.25 to
  0.51 for every component, so the index measures the same thing throughout.
- Columns of the published file: symbol, quarter, trading days, quarter-end close, the five components (and the raw
  Amihud ratio and SLB trading days), index, tercile.

## 16.2 Properties

- Persistent: the mean rank correlation of the index between consecutive quarters is 0.90.
- Components move together: lacking a short channel correlates 0.70 with SLB scarcity and 0.55 with illiquidity; the
  spread correlates 0.52 with idiosyncratic volatility.

## 16.3 Validation (associations, with frictions measured before the outcomes)

| Outcome | Coefficient per s.d. of the index (se) | With a size control (se) |
|---|---|---|
| Price delay in year y (Hou-Moskowitz), on the index of year y-1, year fixed effects (mean delay 0.317) | +0.058 (0.003) | +0.036 (0.004), log market cap as control |
| Same, with stock fixed effects | +0.032 (0.005) | +0.028 (0.006) |
| Absolute drift after results announcements, previous-quarter index, quarter fixed effects (mean 0.152) | +0.023 (0.001) | +0.015 (0.001), size-decile fixed effects |
| Drift after bad news | -0.008 (0.001) | -0.001 (0.002) |
| Drift after good news | +0.001 (0.001) | +0.001 (0.002) |
| F&O stocks only: width of the futures-cash band | -6.4 bp (1.5) | |

The index lines up with slower price adjustment, also within a stock over time and after controlling for size, and with
larger post-announcement drift in either direction. Without a size control, drift after bad news (but not good news) is
stronger for more constrained stocks; **with size-decile fixed effects this asymmetry disappears** (-0.001, se 0.002), so
it reflects the smaller size of constrained stocks rather than the short-sale constraint itself (size check
`analysis/audit/index_size_check.py`, added after the validation). These are associations, not causal effects.

Within F&O stocks the index goes with narrower, not wider, futures-cash bands. Among F&O stocks the short-channel
component does not vary and SLB activity, which carries a large weight, appears to reflect demand to borrow rather than
ease of borrowing (the same pattern as in H1). For the futures-cash band of F&O stocks the F&O-specific index of H1
(spread, illiquidity, idiosyncratic volatility, utilisation of the position limit, SLB) is the relevant measure: a one
standard deviation higher value goes with a band 3.5 bp wider ([14_results.md](14_results.md), 14.13).
