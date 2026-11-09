# 8. Variables and measures

This page defines every variable used in the tests: what it measures, the exact formula, and why it is built that way.
Column names refer to the processed files in `data/processed/` ([07_data_construction.md](07_data_construction.md)).

## 8.1 Outcomes (mispricing and market behaviour)

### O1. The futures-cash basis (main outcome)

    m_it = ln F_it - ln(S_it - PV_it(D)) - r_t * tau_it              (column m_vwap)

| Element | Definition |
|---|---|
| F_it | Daily VWAP of the stock future: traded value / (contracts x lot size) |
| S_it | Daily VWAP of the stock in the cash market: traded value / traded quantity |
| PV_it(D) | Present value of cash dividends going ex after day t and on or before expiry |
| r_t | 3-month interbank rate for the month (per year, continuously applied) |
| tau_it | Calendar days to expiry / 365 |

Reported in basis points (multiply by 10,000).

**Why VWAPs and not closing or settlement prices.** On days when a future does not trade in the last half hour, NSE
sets its settlement price at a theoretical cost-of-carry value, so a settlement-price basis is zero by construction on
exactly the thin-trading days that bans create. Closing prices of the stock and the future are also taken at slightly
different moments. Daily VWAPs use only actual trades in both markets over the same day.

**Secondary version:** `m_close`, from closing prices, with theoretical-settlement days flagged.

### O2. Relative implied repo rate

    r_implied_it = [ln F_it - ln(S_it - PV_it)] / tau_it
    rel_repo_it  = r_implied_it - median over stocks of r_implied on day t (same contract order; tau >= 7 days)

The implied repo is the financing rate at which the future would be fairly priced. Subtracting the day's cross-sectional
median removes any error in the benchmark rate, which is common to all stocks on a day.

### O3. Reversion of the basis

The daily change of the basis, `Delta m_it = m_it - m_i,t-1`, computed only within the same contract (never across a
contract roll or a gap in the sample), regressed on the lagged level by regime ([09_empirical_design.md](09_empirical_design.md)).

### O4. Trading activity

| Variable | Definition |
|---|---|
| Futures volume | Contracts traded, near plus next month (column n_contracts) |
| Change in open interest | Contracts, near plus next month (column chg_oi divided by lot) |
| Delta OI + volume | Zero when every trade closes positions for both sides (the ban prediction) |
| Cash volume | Shares traded (S_qty) |
| Delivery share | Deliverable quantity / quantity traded (delivery file) |

### O5. Earnings drift

| Variable | Definition |
|---|---|
| Day 0 | Release day if released before 15:30, otherwise the next trading day; if the release time is unknown, the next trading day after the release date ([07_data_construction.md](07_data_construction.md), 7.8) |
| Surprise (main) | EAR: abnormal return over days -1 to +1 |
| Surprise (secondary) | SUE from earnings per share in the XBRL filings, if extraction succeeds |
| Drift | BHAR[+2, +64]: buy-and-hold return from day +2 to day +64 minus that of a size-matched portfolio |
| Good and bad news | Top and bottom of the surprise distribution |

### O6. Price efficiency in the cash market

| Variable | Definition |
|---|---|
| Price delay (Hou and Moskowitz 2005) | From weekly returns over 52-week windows: 1 minus the R-squared of a regression on the contemporaneous market return divided by the R-squared with four lags of the market return added |
| Variance ratio VR(5) | Variance of 5-day returns / (5 x variance of daily returns); 1 for a random walk |

## 8.2 Treatments (constraints)

| Variable | Definition | Column or file |
|---|---|---|
| Utilisation omega | Market-wide open interest / MWPL at the end of day t-1. Gross OI before 1 Oct 2025; futures-equivalent OI from 1 Oct 2025 | util, util_futeq |
| Ban | Stock on the official ban list for day t | ban_days.csv.gz |
| Ban spell | Consecutive ban days; length; days since start; whether an expiry has occurred inside the spell | ban_spells.csv.gz |
| Near miss | Not in a ban, with omega in [0.85, 0.95) (control group for ban entries) | panel |
| Hysteresis zone | omega in [0.80, 0.95), in a ban or not | panel |
| COVID halving | MWPL halved for 60 stocks in the files of 20 to 27 March 2020 and one more on 29 April 2020 (effective the next trading day); restored for 70 stocks on 26 November 2020 | panel (MWPL changes) |
| 1 Oct 2025 intensity | I = -ln(MWPL_new / MWPL_old) per stock (0.24 to 0.69), and the predicted change in log utilisation ln(FutEq OI / gross OI on 1 Oct 2025) + I | panel |
| Quarterly MWPL resets | MWPL changes on recomputation dates after October 2025 | panel |
| STT dates | 1 April 2023, 1 October 2024, 1 April 2026 | fixed dates |
| F&O entry, eligibility exit | Event dates (usable: 233 entries, 158 eligibility exits) | fno_events.csv |
| Arbitrage capital | Monthly flow = arbitrage-fund net inflow / previous month-end net assets; net assets (AMFI, April 2018 to September 2026) | amfi_arbitrage_monthly.csv |
| Short-sale constraint group (H5) | G1 F&O stock; G2 cash-only with an SLB trade in the last three months; G3 cash-only without | fno_membership, slb_daily |

## 8.3 Controls and conditioning variables

| Variable | Use |
|---|---|
| Stock fixed effects alpha_i, date fixed effects lambda_t | Remove stock-specific levels and market-wide shocks |
| Stock's percentile thresholds of m on non-ban days (20th, 80th) | Define the lower and upper regimes for H7 |
| Lagged basis (5 lags), lagged utilisation path, change in utilisation | Control for selection on past paths (hysteresis, event-study matching) |
| Size, turnover, volatility in the 6 months before an event | Matching of controls for F&O entry and exit |
| Pre-ban composition C: change in OI over volume (near + next futures, contracts) in the 5 days before entry; build-up type from the signs of the OI change and the cash price change | Splits the level-effect test |
| Days to expiry | Band edges shrink toward expiry |

## 8.4 Friction index (for H1)

Built only from ex-ante frictions, never from the outcome (basis) or the treatment (ban), per stock and quarter, used in
the next quarter:

| Component | Definition |
|---|---|
| Spread | Corwin-Schultz (2012) two-day estimate from daily cash high and low prices, with the overnight-gap adjustment, negative values set to 0, quarterly mean |
| Illiquidity | log of the quarterly mean of absolute daily return / traded value (Rs crore) (Amihud 2002) |
| Idiosyncratic volatility | standard deviation of residuals of daily returns on the Nifty 50 return (at least 40 days) |
| Utilisation | mean omega on non-ban days (less headroom = more friction) |
| SLB scarcity | 1 - share of trading days with any SLB trade in the stock |

Each component is standardised within quarter; the index is the first principal component (loadings 0.57, 0.37, 0.55,
0.45, 0.18; 44% of variance). The SLB component enters with the wrong sign in the outcome regressions, which suggests that
SLB activity reflects demand to borrow; an index without it is reported alongside.

## 8.5 Measures used in the secondary tests

| Measure | Definition | Test |
|---|---|---|
| Event difference D | Change in the basis from day -1 of a ban entry, treated minus matched near-miss controls, averaged over the in-ban days 0 to 4 | Level effect |
| Upper and lower exceedance U, L | 1 if the basis is above the stock's 80th (below its 20th) percentile on non-ban days with utilisation below 0.60 | H9 |
| Band width W, size A, persistence rho | Per stock-quarter on non-ban days: q80 - q20 of m; mean absolute m; slope of m_t on m_(t-1) (same contract) | H1 |
| Monthly upper quantile | 80th percentile of m across all non-ban stock-days of the month | H4 |
| Composite mispricing score | Average percentile rank of momentum (t-11 to t-1), short-term reversal, maximum daily return, idiosyncratic volatility, Amihud illiquidity and turnover, oriented so that high = overpriced | H5 |
| Annualised SLB fee | Value / quantity / cash close x 365 / days to SLB expiry | Descriptive |
