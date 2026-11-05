# 10. Institutional facts (with verification status)

Status: **P** verified against a primary source (circular, exchange page, paper PDF); **S** verified only via consistent
secondary sources (broker notes, press); **D** confirmed in our own data; **?** unverified. Detailed log with sources:
`memory/07_fact_check.md` and `memory/03_institutional_facts.md`. Primary PDFs: `references/16` (SEBI 2024/132),
`17` (SEBI 2025/79), `18` (NSE MWPL page), `19` (NSE Clearing 119/2025), `22` (NSE Clearing FAQ, Oct 2025).

## Ban and MWPL
| Fact | Status |
|---|---|
| Ban entry: market-wide OI > 95% of MWPL at end of day; ban from next day; only position-reducing trades | P, D (99.4%) |
| Ban exit: combined OI <= 80% of MWPL ("in line with existing practice", NSE Clearing 119/2025 §2.1.2) | P, D (99.7%) |
| Ban covers all expiries of the stock's futures and options; index derivatives and cash unaffected | S |
| Rollover not allowed in a ban | S (broker FAQs citing SEBI) |
| Penalty for increasing positions: 1% of value, min Rs 5,000, max Rs 1 lakh per entity per stock per day (from 1 Oct 2025) | P |
| **Ban enforcement regimes** (found 5 Nov 2026): to 22 Mar 2020 end-of-day positions only (intraday round trips not violations; some brokers allowed them, Zerodha did not); **from 23 Mar 2020 peak-intraday positions** (SEBI PR 18/2020; ICCL notice 22 Mar 2020: penalty lower of 1% or Rs 5 lakh per client, min Rs 50,000), continued after 26 Nov 2020 "till further directions" (PR 59/2020); **from 1 Oct 2025 end-of-day FutEq vs base position** (NSE Clearing 119/2025). Data: ban-day (dOI+V)/V median 0.87 / 0.011 / 0.19-0.36 in the three regimes | P, D |
| Broker notices cite 8 Dec 2025 for "delta-based exposure limits on open positions in ban period" (Angel One); the market-level FutEq trigger is visibly in force from 1 Oct 2025 in our data (805 gross > 95% stock-days without bans in Oct to early Dec 2025). 8 Dec 2025 is probably the brokers' implementation of the entity-level delta check; unresolved | S, D |
| Pre-Oct 2025 MWPL = 20% of non-promoter shares (SEBI/DNPD/Cir-31/2006, 22 Sep 2006) | P, D (free float = MWPL/0.20 reproduces Oct 2025 limits) |
| 30x prior-month-volume leg: SEBI/DNPD/Cir-26/2004 (16 Jul 2004), replaced in 2006; irrelevant for the sample | P |
| MWPL recomputed monthly before the reform (monthly non-promoter holding data); quarterly after | P (FAQ) |
| COVID: MWPL halved for F&O stocks with avg high-low range >= 15% or avg utilisation >= 40% over 5 sessions, effective 23 Mar 2020, extended, withdrawn end of 26 Nov 2020 | S, D |
| New MWPL from 1 Oct 2025: min(15% FF, 65 x market-wide ADDV in shares), floor 10% FF; recomputed quarterly on the previous 3 months (MWPL from 1 Oct 2025 uses 16 Jun to 15 Sep 2025), valid 3 months, published by the 20th of the last month of the quarter; corporate-action adjusted | P |
| Ban test on futures-equivalent (delta) OI from 1 Oct 2025; gross-OI monitoring discontinued | P (FAQ; broker claims of Dec 2025 unexplained) |
| In-ban rule from 1 Oct 2025: entity's end-of-day FutEq delta must move toward zero; sign flip = violation; passive changes not breaches; deltas from 2 PM SPAN file | P |
| Intraday MWPL monitoring (>= 4 random snapshots) from 3 Nov 2025 (NSE surveillance circular 849/2025) | P |
| Entity limits from 1 Oct 2025: client 10%; prop 20%; TM with clients, FPI-I, MF 30%; FPI-II 20%/10% of MWPL | P |
| SEBI stated aim (2025/79): "reduce instances of spurious F&O ban periods" | P |
| Market-level FutEq OI disseminated daily before the reform | P (FAQ) |
| An NSE alert at 60% utilisation | ? (one secondary source) |

## Short selling, settlement, market structure
| Fact | Status |
|---|---|
| Naked short selling prohibited (SEBI 20 Dec 2007); short sellers must deliver | S |
| Only F&O-segment securities eligible for short selling and SLB (Master Circular 16 Oct 2023, Annexure 3) | S |
| SLB / institutional shorting from 21 Apr 2008; SLB thin | S |
| Intraday shorting of non-F&O stocks: broker-dependent | ? |
| Mutual funds may legally short/SLB (MF Regulations amended 2007); arbitrage funds in practice run long cash / short futures | S |
| Stock derivatives physically settled: phased from Jul 2018 expiry; all from Oct 2019 expiry | S |
| Stock options European from the Jan 2011 expiry | S |
| T+1 cash settlement: phased from 25 Feb 2022, complete 27 Jan 2023 | S |
| Futures daily settlement = last half-hour weighted average; theoretical price F = S e^{rt} if not traded in the last half hour | P (NSE page) |
| Cash close = last 30-minute VWAP; for F&O stocks a closing auction from 3 Aug 2026 (3:15 to 3:35 PM, random close 3:28 to 3:30); pre-open changes 7 Sep 2026 | S |
| UDiFF: old cash bhavcopy discontinued from 8 Jul 2024 (NSE circular 62424) | P, D |
| Monthly expiry Thursday until Aug 2025; Tuesday from Sep 2025 (NSE) | S, D (first Tuesday 30 Sep 2025) |
| Results due within 45 days of quarter end (60 for Q4), disclosure within 30 minutes of the board meeting's end (SEBI LODR) | S |
| Integrated Filing - Financials from the Mar 2025 quarter (NSE/CML/2025/20) | S, D |

## Costs, margins, capital
| Fact | Status |
|---|---|
| Futures STT (sell): 0.017% → 0.01% on 1 Jun 2013; → 0.0125% on 1 Apr 2023 (NSE FATAX56235); → 0.02% on 1 Oct 2024; → 0.05% on 1 Apr 2026 (NSE FATAX73524, Finance Act 2026) | P/S |
| Options STT premium 0.05% → 0.0625% (Apr 2023) → 0.1% (Oct 2024) → 0.15% (Apr 2026); exercise 0.125% → 0.15% (Apr 2026) | P/S |
| Cash delivery STT 0.1% each side; physically settled derivatives 0.1% | S |
| Debt-fund tax change 1 Apr 2023 (<= 35% equity taxed at slab); arbitrage funds equity-taxed | S |
| Arbitrage-fund AUM ~Rs 71,106 crore (Apr 2023) → Rs 1,98,981 crore (Oct 2024) | S (confirm with AMFI) |
| AMFI reports arbitrage funds separately from mid-2018 | S |
| Peak margin 25% (Dec 2020), 50% (Mar 2021), 75% (Jun 2021), 100% (1 Sep 2021) | S |

## F&O eligibility
| Fact | Status |
|---|---|
| 2018: top 500 by mcap and traded value; MQSOS >= Rs 25 lakh; MWPL >= Rs 500 crore; ADDV >= Rs 10 crore (6-month rolling) | S |
| SEBI/HO/MRD/MRD-PoD-2/P/CIR/2024/116 (30 Aug 2024): MQSOS Rs 75 lakh, MWPL Rs 1,500 crore, ADDV Rs 35 crore; exit after failing 3 consecutive months | S, D (45 entries 29 Nov 2024) |
| Universe ~210 to 220 stocks in 2026; quarterly additions (e.g. 8 on 1 Apr 2026, 6 on 28 Oct 2026) | S, D |

## Index-only reforms (placebos)
SEBI 2024/132 (1 Oct 2024; P): index contract size Rs 15 lakh, one weekly benchmark per exchange, +2% ELM on short options
on expiry day (20 Nov 2024); upfront premium, no calendar-spread benefit on expiry day (1 Feb 2025); intraday index
position-limit monitoring (1 Apr 2025). NSE ended Bank Nifty/FinNifty/Midcap Select weeklies (13/18/19 Nov 2024).

## Claims found to be wrong (never reuse)
- "No genuine short selling in the cash market" (project document §1): intraday shorting exists; overnight needs SLB.
- "MWPL = 20% FF or 30x volume" for the sample period.
- "October and December 2025 relaxations": the 3 Nov 2025 change is a tightening; Dec 2025 changes are index options and
  pre-open.
- "Position limits studied in Korea and Taiwan": no source.
- "Arbitrage mutual funds are barred from shorting" (Slivka et al.): outdated.
- ADDV as a delivery value: it is in quantity terms in the NSE SOP.
