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

## NOT verified by any repo primary source (need NSE/SEBI circular before using)
- Ban **exit when OI < 80% of MWPL** (widely known rule; believed correct).
- Historical MWPL leg "**30 × average daily traded quantity in previous month**" (lower of 20% FF or 30× volume). The 2024 Master
  Circular as quoted only states 20% FF — status/timing of the volume leg unknown.

## Short selling in India (as framed in the project)
- Intraday cash shorting allowed; naked overnight shorting prohibited; SLB exists (since Apr 2008) but thin → persistent short
  exposure via SSF. Arbitrage mutual funds cannot short (Slivka) → forward (cash-and-carry) arbitrage only.
- Settlement: cash T+1 now (T+2 in 2013); SSF cash-settled... (NB: Indian SSF moved to physical settlement in 2018–19 — verify if used).

## Data files (from project doc §8)
sec_bhavdata_full (delivery), UDiFF bhavcopy (ISIN-keyed, 2024+), F&O bhavcopy (settle/OI), combined OI/MWPL (with FutEq post-2025),
securities-in-ban CSV, shareholding pattern, results calendar, India VIX, F&O eligibility lists. Wrappers: R `nser`, Python scrapers.
