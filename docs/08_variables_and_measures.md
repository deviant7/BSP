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
| Day 0 | Release day if released before 15:30, otherwise the next trading day (board-meeting events: the meeting day) |
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
| COVID halving | MWPL halved for 61 stocks in the files of 20 to 27 March 2020 (effective the next trading day); restored for 70 stocks on 26 November 2020 | panel (MWPL changes) |
| 1 Oct 2025 intensity | ln(MWPL_new / MWPL_old) per stock, and the predicted change in utilisation from pre-reform open-interest composition | panel |
| Quarterly MWPL resets | MWPL changes on recomputation dates after October 2025 | panel |
| STT dates | 1 April 2023, 1 October 2024, 1 April 2026 | fixed dates |
| F&O entry, eligibility exit | Event dates (usable: 233 entries, 158 eligibility exits) | fno_events.csv |
| Arbitrage capital | Arbitrage-fund assets and flows (to be collected) | AMFI |

## 8.3 Controls and conditioning variables

| Variable | Use |
|---|---|
| Stock fixed effects alpha_i, date fixed effects lambda_t | Remove stock-specific levels and market-wide shocks |
| Stock's percentile thresholds of m on non-ban days (20th, 80th) | Define the lower and upper regimes for H7 |
| Lagged basis (5 lags), lagged utilisation path, change in utilisation | Control for selection on past paths (hysteresis, event-study matching) |
| Size, turnover, volatility in the 6 months before an event | Matching of controls for F&O entry and exit |
| Pre-ban composition: change in OI over volume in the 5 days before entry | Splits the level-effect test |
| Days to expiry | Band edges shrink toward expiry |

## 8.4 Friction index (for H1)

Built only from ex-ante frictions, never from the outcome (basis) or the treatment (ban): a bid-ask spread proxy, the
Amihud illiquidity ratio, idiosyncratic volatility, lagged headroom (1 - omega) and securities-lending availability if
obtained. Weights from principal components and, as an alternative, from the model.
