# 15. The no-arbitrage band: estimation

This page estimates and describes the band within which the futures-cash basis moves without triggering arbitrage. It is
estimation, not a confirmatory test (the confirmatory test of costs and band edges is H3 in [14_results.md](14_results.md)).
Specifications were fixed before estimation in the plan's deviations log (§11.13, C16); checks added after seeing the
estimates are marked exploratory (§11.2). Code: `analysis/band_estimation.py`, `analysis/band_exploratory.py`,
`analysis/band_costs.py`; outputs `analysis/output/band_estimation.txt`, `band_exploratory.txt`, `band_costs.txt`,
`band_by_year.csv`, `band_per_stock.csv`.

## 15.1 Data and models

- Non-ban stock-days of the analysis sample (the band in normal times), 2 January 2015 to 27 October 2026: 473,110
  observations of the daily change in the basis of the same contract, 360 stocks.
- The deviation x is yesterday's basis minus the stock's median basis on non-ban days (bp); its 5th, 50th and 95th
  percentiles are -71.7, -0.1 and +34.0 bp.
- **Three-regime threshold model:** the daily change in the basis is regressed on x separately below a lower threshold,
  between the thresholds, and above an upper threshold, with the thresholds chosen to minimise the sum of squared residuals
  (grid over the 5th to 95th percentiles of x; at least 10% of observations in each outer regime, 20% in the middle).
  Linearity is tested with a sup-F statistic and a wild bootstrap clustered by date; threshold uncertainty comes from
  resampling whole stocks.
- **Smooth-transition models:** an exponential STAR (reversion speed changes smoothly and symmetrically with the size of the
  deviation, as with traders who face different costs) and a logistic STAR in x (allows different speeds below and above).
- **Observed-transition models:** the reversion speed changes smoothly with an observed state variable: utilisation of the
  position limit, trading days to expiry, or arbitrage-fund assets.
- Fixed thresholds estimate **average band edges**, not costs: in data simulated from the model, where the no-trade region
  moves with the arbitrage book, the estimated edges sit inside the cost band ([09_empirical_design.md](09_empirical_design.md), 9.6).

## 15.2 The pooled band

| | Lower regime | Middle regime | Upper regime |
|---|---|---|---|
| Threshold (bp, relative to the stock's median) | below -34.5 | | above +23.9 |
| Share of observations | 12% | 76% | 12% |
| Slope of the daily change on x | -0.084 | -0.468 | -0.809 |

- Stock-cluster bootstrap intervals: lower threshold -37.2 to -32.2 bp, upper +20.3 to +26.1 bp.
- Linearity is rejected: sup-F 7,471 against a bootstrap 95% critical value of 31 (p < 0.005).
- The band is about 58 bp wide and asymmetric: the lower edge is further from the centre than the upper edge, as expected
  when reverse arbitrage (selling the stock, buying the future) is costlier than cash-and-carry.
- Model comparison (BIC): the threshold model fits best (3,005,493), the logistic STAR is almost as good (3,005,545; slow
  reversion below +5.4 bp, fast above), the exponential STAR is worse (3,008,092) and the linear model worst (3,034,394). The
  symmetric exponential form does not fit an asymmetric band.
- An auxiliary regression with squared and cubed deviations (stock and date fixed effects) also rejects linearity
  (Wald chi-squared 2,066).

**How much of the reversion is real.** The middle regime shows strong reversion (half-life about one day), unlike the
textbook band in which deviations inside the band are not corrected. Daily volume-weighted prices contain noise, and
classical noise in the basis biases these slopes toward -1. **Exploratory check:** instrumenting yesterday's deviation with
the deviation two days earlier shrinks the slopes from -0.49 to -0.19 in the middle, from -0.52 to -0.14 above the upper
edge and from -0.17 to -0.12 below the lower edge. Much of the day-to-day reversion is therefore noise, and once it is
removed the reversion speeds above and below the band are similar; the apparent slow reversion of cheap futures in the
threshold model should not be read as a finding on its own. The threshold locations, which describe where the basis
spends its time, are less affected.

## 15.3 The band over time

Thresholds by STT period, with the deviation measured from the stock's median within each period (exploratory: the
full-sample median does not remove the level shift of 2026 and makes that year's upper threshold collapse to about -2 bp):

| Period (futures STT) | Lower threshold | Upper threshold | Slope above the upper threshold |
|---|---|---|---|
| to March 2023 (0.01%) | -39.1 | +23.8 | -0.77 |
| April 2023 to September 2024 (0.0125%) | -30.9 | +18.9 | -0.55 |
| October 2024 to March 2026 (0.02%) | -31.5 | +23.1 | -0.20 |
| from April 2026 (0.05%) | -31.5 | +28.9 | -0.15 |

- The upper threshold is highest in the period with the highest STT, but it does not rise step by step with the tax.
- Reversion above the upper edge becomes much weaker over time. This coincides with rising STT and with the growth of
  arbitrage-fund assets, so the two cannot be separated in this description.
- By calendar year (full-sample demeaning; `band_by_year.csv`) the thresholds are stable around -25 to -47 bp and +17 to
  +34 bp, apart from 2020 (lower threshold -59 bp, the March 2020 dislocation).

## 15.4 States: expiry, utilisation and capital

| State | Lower threshold | Upper threshold | Slope above |
|---|---|---|---|
| 0 to 10 trading days to expiry | -28.2 | +22.1 | -0.74 |
| 10 to 17 days | -28.6 | +23.1 | -0.78 |
| 17 to 28 days | -40.4 | +22.6 | -0.86 |
| Utilisation low (below 0.15) | -33.6 | +25.9 | -0.91 |
| Utilisation middle (0.15 to 0.32) | -29.2 | +25.9 | -0.83 |
| Utilisation high (0.32 and above) | -37.0 | +19.8 | -0.72 |

- The lower edge is wider far from expiry, consistent with edges that shrink as expiry approaches.
- At high utilisation the upper threshold is lower and more observations lie above it: the basis is more often rich.

Observed-transition models (stock and date fixed effects; two-way clustered standard errors):

| Transition variable | Slope at low values | Change at high values (se) | Reading |
|---|---|---|---|
| Utilisation (location 0.07) | -0.449 | +0.225 (0.053) | Reversion weakens as utilisation rises, consistent with anticipation of bans and larger arbitrage books |
| Trading days to expiry (location 7 days) | -0.474 | +0.221 (0.023) | Reversion is faster in the last week before expiry |
| Log arbitrage-fund assets (location about Rs 95,000 crore) | -0.258 | -0.077 (0.019) | Reversion is faster when arbitrage capital is larger (this variable also orders time) |

## 15.5 Stock by stock

Threshold models for the 258 stocks with at least 500 non-ban observations: median lower threshold -26.4 bp (10th to 90th
percentile -61.5 to -7.7), median upper threshold +16.5 bp (-4.9 to +26.1), median width 40.9 bp (18.5 to 75.5). Per-stock
widths are not related to the stock's average friction index (slope +2.2 bp per unit, se 1.9; correlation 0.07), unlike the
quarterly percentile widths of H1.

## 15.6 Costs against the estimated band

Bottom-up round-trip cost of an overnight cash-and-carry position (long cash, short future), bp of notional, with an
institutional brokerage of 0.01% per leg:

| Period | A: open and hold to expiry | B: roll an existing position one month | Upper threshold (levels) | 90th percentile of the basis |
|---|---|---|---|---|
| to March 2023 | 27.1 | 4.0 | +27.5 | +27.5 |
| April 2023 to September 2024 | 27.3 | 4.3 | +23.6 | +24.7 |
| October 2024 to March 2026 | 28.0 | 5.0 | +21.5 | +24.2 |
| from April 2026 | 31.0 | 8.0 | +24.1 | +29.7 |

Components: STT of 0.1% on the cash purchase and 0.1% on delivery at expiry (stock derivatives are physically settled;
closing by selling the stock costs the same), STT on the futures sale (0.01%, 0.0125%, 0.02%, 0.05%), stamp duty on the
purchase (0.015% from July 2020), exchange transaction charges (cash 0.00322% then 0.00297%; futures 0.00188% then
0.00173% from October 2024), SEBI fee and 18% GST on charges and brokerage. With brokerage between 0.005% and 0.03% per
leg, scenario A ranges from 25 to 38 bp.

Reading. The cost of a new round trip (27 to 31 bp) is above the estimated upper threshold and close to the 90th to 95th
percentiles of the basis: entry by new capital is rare and happens only at large deviations. The marginal cost of keeping
capital in place and rolling (4 to 8 bp) is far lower; arbitrage funds that roll their book can lean against much smaller
deviations, which is one reason why fixed thresholds sit inside the full cost band. The basis is measured net of the
3-month interbank rate, so a fund whose required return differs from that rate shifts the whole band.

## 15.7 Summary

1. The basis behaves nonlinearly: a wide, asymmetric band (about -35 to +24 bp around each stock's median) with stronger
   correction outside it.
2. Day-to-day reversion is inflated by measurement noise in daily prices; corrected for noise, reversion speeds above and
   below the band are similar.
3. The band is wider far from expiry, the basis is more often rich at high utilisation, and reversion weakens as
   utilisation rises and strengthens near expiry and when arbitrage capital is large.
4. Upper thresholds do not move one-for-one with STT; the full cost of a new position lies near the outer tail of the basis,
   while the cost of rolling an existing position is a few basis points.
