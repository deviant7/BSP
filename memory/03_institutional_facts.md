# 03 — Institutional facts (SEBI / NSE)

## Verified from primary sources in repo
**SEBI Circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132, 1 Oct 2024** — ALL six measures are *index-derivative* measures:
| Measure | Effective |
|---|---|
| Index contract size ≥ ₹15 lakh at launch, ₹15–20 lakh at review (was ₹5–10 lakh, set 2015) | 20 Nov 2024 |
| One benchmark index with weekly expiry per exchange | 20 Nov 2024 |
| +2% ELM on short options on expiry day | 20 Nov 2024 |
| Upfront option premium collection from buyers | 1 Feb 2025 |
| No calendar-spread benefit on expiry day | 1 Feb 2025 |
| Intraday monitoring of index position limits (≥4 random snapshots) | 1 Apr 2025 |

**SEBI Circular SEBI/HO/MRD/TPD-1/P/CIR/2025/79, 29 May 2025** — objectives incl. "reduce instances of spurious F&O ban periods in single stocks".
- 5.1 FutEq OI = net delta-adjusted positions per UCC, gross-summed across UCCs — "already implemented".
- 5.2 Old MWPL (Master Circular 30 Dec 2024, cl. 3.3.2.1.1) = **20% of non-promoter (free-float) shares** (no volume leg mentioned).
  New: **MWPL = min(15% FF, 65 × ADDV across CCs), floor 10% FF; recalculated every 3 months on rolling 3-month ADDV**.
  Ban test: market-wide FutEq OI > 95% of MWPL (EoD).
- 5.3 Ban period: trades must reduce EoD FutEq delta toward 0; sign flip not a reduction; passive increase not a breach. (1 Oct 2025)
- 5.4 Intraday MWPL monitoring single stocks, ≥4 random times (a *tightening*). (3 Nov 2025)
- 5.5 Index options: net FutEq ₹1,500 cr / gross ₹10,000 cr per PAN (glide 1 Jul–5 Dec 2025; normal 6 Dec 2025);
  index futures: higher of 15% OI or ₹500 cr (FPI-I/MF/Pro/Clients), 10%/5% for FPI-II categories (1 Jul 2025).
- 5.6 Pre-open session for current-month futures (single stocks & indices) (6 Dec 2025).
- 5.7 Non-benchmark index eligibility (≥14 constituents, top ≤20%, top-3 ≤45%) (3 Nov 2025).
- 5.8 Entity single-stock limits as % of new MWPL: Client/NRI 10%; Pro 20%; Pro+Client / FPI-I / MF 30%; FPI-II 20%/10% (1 Oct 2025).

**NSE MWPL web page (ref 18 html)**: mostly navigation; states 95% ban entry and "trade only to decrease positions"; links to
combined-OI zip and securities-in-ban CSV + archives. Cites NSCC/F&O/C&S/365 (26 Aug 2004) for penalties.

**NSE Clearing circular 119/2025 (8 Sep 2025; `references/19_…pdf`)** — SOP for new MWPL, effective 1 Oct 2025:
MWPL = lower of 15% FF and 65× market-wide ADDV **in quantity terms**, floor 10% FF; recomputed quarterly on prior 3 months
(e.g., MWPL from 1 Oct 2025 uses 16 Jun–15 Sep 2025), valid 3 calendar months, published by 20th of last month of quarter;
ban if EoD FutEq OI > 95% MWPL (from next day); **exit when combined FutEq OI ≤ 80% of MWPL ("in line with existing practice")**;
gross-OI monitoring discontinued; entity check vs base position using 2 PM SPAN delta; penalty 1% of violation value
(min ₹5,000, max ₹1 lakh per entity/stock/day).

## Resolved by web check (28 Oct 2026) — full log in `07_fact_check.md`
- 80% exit: CONFIRMED (above).
- "30× volume" leg: from SEBI/DNPD/Cir-26/2004 (16 Jul 2004); replaced by 20% FF in SEBI/DNPD/Cir-31/2006 (22 Sep 2006).
  → 2015–Sep 2025 MWPL = 20% FF, except the COVID halving (23 Mar–26 Nov 2020) for volatile/high-utilisation stocks.
- Rollover not allowed during ban (broker FAQs citing SEBI).
- Stock derivatives physically settled (phased Jul 2018 / Apr–Oct 2019); stock options European from 27 Jan 2011.
- STT futures: 0.01% from 1 Jun 2013; 0.02% from 1 Oct 2024; 0.05% from 1 Apr 2026 (Budget 2026).
- Closing Auction Session for F&O stocks from 3 Aug 2026.

## Short selling in India (as framed in the project)
- Intraday cash shorting allowed; naked short selling prohibited (SEBI 20 Dec 2007); SLB / institutional shorting from 21 Apr 2008
  but thin → persistent short exposure via SSF. MFs are legally *permitted* to short/SLB (MF Regs amended 2007; Slivka's "barred"
  is wrong/outdated), but arbitrage funds in practice run long-cash/short-futures.
- Settlement: cash T+1 (fully from 27 Jan 2023); stock F&O physically settled (all from Oct 2019 expiry).

## Data files (from project doc §8)
sec_bhavdata_full (delivery), UDiFF bhavcopy (ISIN-keyed, 2024+), F&O bhavcopy (settle/OI), combined OI/MWPL (with FutEq post-2025),
securities-in-ban CSV, shareholding pattern, results calendar, India VIX, F&O eligibility lists. Wrappers: R `nser`, Python scrapers.
