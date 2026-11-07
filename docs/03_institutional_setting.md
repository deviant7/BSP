# 3. Institutional setting

This page sets out the rules of the Indian market that the project relies on, with dates and sources. The primary
documents are in `references/` (numbers in brackets refer to that folder). Where a rule is documented only by
secondary sources (broker notes, financial press), this is stated.

## 3.1 Market structure

- **Exchange.** All data come from the National Stock Exchange of India (NSE), the dominant exchange for both cash
  equities and equity derivatives.
- **Trading hours.** Normal trading runs 9:15 to 15:30 IST. Results released at or after 15:30 can only be traded the
  next trading day.
- **Cash settlement cycle.** T+1, phased in from 25 February 2022 and complete from 27 January 2023.
- **Stock derivatives.** Monthly futures and options on each F&O stock, with three expiries listed at a time. Monthly
  expiry was the last Thursday of the month; from September 2025 it is the last Tuesday (the expiry dates in the data
  confirm the switch). When the expiry day is a holiday, expiry moves to the previous trading day. Stock options are European
  (from the January 2011 expiry). Stock derivatives are **physically settled**: phased in from the July 2018 expiry, all
  stocks from the October 2019 expiry.
- **Daily settlement price of a stock future.** The weighted average price of the last half hour of trading. If the
  contract does not trade in the last half hour, NSE sets a **theoretical price** equal to the cost-of-carry value. On
  those days a basis built from settlement prices is zero by construction, which is why the project uses traded prices
  (see [08_variables_and_measures.md](08_variables_and_measures.md)).
- **Cash closing price.** The volume-weighted average price of the last 30 minutes, until 3 August 2026. From
  3 August 2026 the closing price of F&O stocks is set by a **closing auction** (a measurement break for any close-based
  measure; the main basis measure uses daily VWAPs and is not affected in the same way).
- **File format.** NSE replaced its old daily files ("bhavcopies") with the standardised **UDiFF** format in July 2024
  (old cash bhavcopy discontinued from 8 July 2024). The project reads both formats.

## 3.2 Which stocks have derivatives (F&O eligibility)

Eligibility for single-stock derivatives is set by SEBI using size and liquidity criteria, reviewed regularly.

| Framework | Main criteria (rolling six months) | Exit rule |
|---|---|---|
| 2018 framework | Among the top 500 stocks by market capitalisation and by traded value; median quarter-sigma order size at least Rs 25 lakh; MWPL at least Rs 500 crore; average daily delivery value at least Rs 10 crore | Stocks failing the criteria are excluded after a notice period |
| SEBI circular SEBI/HO/MRD/MRD-PoD-2/P/CIR/2024/116 (30 Aug 2024) | Median quarter-sigma order size at least Rs 75 lakh; MWPL at least Rs 1,500 crore; average daily delivery value at least Rs 35 crore | Exit after failing for three consecutive months |

Entries and exits happen in batches. In the data the largest are 45 entries on 29 November 2024 (after the 2024 revision),
34 exits on 28 June 2019 and 16 exits on 28 February 2025. Sources: secondary (exchange selection-criteria page citing the
circular; financial press).

**Why this matters.** Under SEBI's short-selling framework (Master Circular of 16 October 2023, Annexure 3) only
securities traded in the F&O segment are eligible for short selling and for stock lending and borrowing (SLB).
Naked short selling is prohibited (SEBI circular of 20 December 2007), and SLB trading is thin. So entering the F&O
segment gives a stock three short channels at once (futures and options, formal short-selling eligibility, SLB
eligibility), and leaving it removes them.

## 3.3 The market-wide position limit (MWPL)

The MWPL caps the total open interest that all participants together may hold in a stock's derivatives.

| Period | MWPL rule | Numerator used for the ban test | Recomputed |
|---|---|---|---|
| 22 Sep 2006 to 30 Sep 2025 | 20% of the number of shares held by non-promoters (free float) (SEBI/DNPD/Cir-31/2006) | Gross open interest in shares, futures and options | Monthly (from non-promoter holding data) |
| 20/23 Mar 2020 to 26 Nov 2020 (COVID measures) | MWPL halved for F&O stocks whose average daily high-low range was at least 15%, or whose average MWPL utilisation was at least 40%, over the previous five sessions | As above | Rule applied by the exchanges from 23 March 2020; withdrawn at the end of 26 November 2020 (secondary sources; matches the data) |
| From 1 Oct 2025 | Lower of 15% of free float and 65 times the market-wide average daily delivery **in shares**, with a floor of 10% of free float (SEBI circular SEBI/HO/MRD/TPD-1/P/CIR/2025/79 of 29 May 2025; NSE Clearing circular 119/2025 of 8 Sep 2025 [19]) | **Futures-equivalent (delta-adjusted) open interest** | Quarterly, on the previous three months' deliveries (e.g. the MWPL valid from 1 Oct 2025 uses 16 June to 15 September 2025) |

Before 2006 the MWPL also had a leg of 30 times the average daily shares traded in the previous month (SEBI circular
of 16 July 2004). That leg plays no role in the sample period.

From 1 October 2025 SEBI also set **entity-level limits** as a share of the new MWPL: clients 10%; proprietary
trading members 20%; trading members with client positions, category I foreign portfolio investors and mutual funds 30%.
From 3 November 2025 the exchanges monitor the MWPL at least four random times during the day (NSE surveillance
circular 849/2025), which tightens the rule.

## 3.4 The F&O ban

| Element | Rule | Source |
|---|---|---|
| Entry | Market-wide open interest above **95% of MWPL** at the end of the day; the stock is in the ban from the next trading day. The exchange's daily open-interest file marks such stocks "No Fresh Positions" for the next day. | NSE Clearing 119/2025 [19]; NSE MWPL page [18] |
| During the ban | Every participant may trade **only to reduce** positions in that stock's futures and options, all expiries. From 1 October 2025 the test is that the entity's end-of-day futures-equivalent delta must move toward zero; a change of sign counts as a violation; passive changes (e.g. from price moves) are not breaches; deltas come from the 2 PM SPAN file. This is more flexible than the earlier rule of trading only through offsetting positions: new contracts that lower the delta (for example a long put against a long future) are allowed. | NSE Clearing 119/2025 [19]; SEBI 2025/79 |
| Rollover | Rolling a position into the next expiry is a new position and is not allowed. | Secondary (broker notes citing SEBI) |
| Penalty | 1% of the value of the increase, minimum Rs 5,000, maximum Rs 1 lakh per entity per stock per day (from 1 Oct 2025). From 23 Mar 2020 the clearing corporations' notices set 1% of the value in violation or Rs 5 lakh per client, whichever is lower, with a minimum of Rs 50,000. | NSE Clearing 119/2025 [19]; BSE/ICCL notice 20200322-2 [24] |
| How compliance is checked | **To 22 Mar 2020:** end-of-day positions only, so a position opened and closed within the day was not a violation. **23 Mar 2020 to 30 Sep 2025:** violations identified from *peak intraday* positions (SEBI press release 18/2020, kept "till further directions" by press release 59/2020). **From 1 Oct 2025:** each entity's end-of-day futures-equivalent position is compared with its base position (NSE Clearing 119/2025). The data show this: on ban days, the change in open interest equals minus the volume traded almost exactly in the middle period, but not before or after (see [14_results.md](14_results.md), 14.2). | SEBI PR 18/2020 and 59/2020 [23]; [24]; [19] |
| Exit | Normal trading resumes when combined open interest falls to **80% of MWPL** or below ("in line with existing practice"). | NSE Clearing 119/2025 [19] |
| Scope | Index derivatives and the cash market of the stock are unaffected. | Secondary (broker notes) |

The rule binds **every** participant, outside traders as much as arbitrageurs. This is central to the theory
([04_theoretical_framework.md](04_theoretical_framework.md)).

## 3.5 Trading costs

| Item | Rate | Dates |
|---|---|---|
| STT on the sale of a future | 0.01% | from 1 June 2013 (was 0.017%) |
| | 0.0125% | from 1 April 2023 (Finance Act 2023; NSE circular FATAX56235) |
| | 0.02% | from 1 October 2024 (Budget July 2024) |
| | 0.05% | from 1 April 2026 (Finance Act 2026; NSE circular FATAX73524) |
| STT on options | premium 0.05% (to Mar 2023), 0.0625% (Apr 2023), 0.1% (Oct 2024), 0.15% (Apr 2026); exercise 0.15% from Apr 2026 | same sources |
| STT on cash delivery trades | 0.1% on purchase and on sale | unchanged in the sample |
| STT on physically settled derivatives | 0.1% | unchanged |

Other costs (stamp duty, exchange and clearing fees, brokerage, price impact, funding) add to these.

## 3.6 Arbitrage capital

- **Arbitrage mutual funds** run cash-and-carry (long stock, short future). They are taxed as equity funds.
- On **1 April 2023** the tax treatment of debt funds changed (funds with up to 35% in equities taxed at the slab rate),
  which made arbitrage funds relatively attractive. Reported arbitrage-fund assets rose from about Rs 71,000 crore
  (April 2023) to about Rs 1.99 lakh crore (October 2024) (AMFI data as reported by the financial press). This date
  coincides with an STT increase, so the two cannot be separated in a time series.
- **Peak-margin rules** (margins checked against intraday peaks) were phased in at 25% (December 2020), 50% (March 2021),
  75% (June 2021) and 100% (1 September 2021).
- AMFI publishes arbitrage-fund flows and assets separately from mid-2018.

## 3.7 Index-derivative reforms (used only as placebos)

SEBI circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132 (1 October 2024) changed only **index** derivatives (larger contract
sizes and one weekly expiry per exchange from 20 November 2024; upfront premium collection and no calendar-spread benefit
on expiry day from 1 February 2025; intraday monitoring of index position limits from 1 April 2025). Because these do not
touch single-stock derivatives, they serve as placebo dates for single-stock outcomes.

## 3.8 Results announcements

Listed companies file quarterly results with the exchange; the filing carries a broadcast timestamp. From the quarter
ended March 2025 results are filed as "Integrated Filing - Financials". Quarterly results are due within 45 days of the
quarter end, annual (fourth-quarter) results within 60 days.
