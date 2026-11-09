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
- Pre-Oct-2025 MWPL was recomputed **monthly** (NPH files = monthly non-promoter holding → free-float data source); now quarterly.
- Market-level FutEq OI published daily before the reform ("Combined Delta Equivalent OI" report); `combineoi` gains FutEq field from 1 Oct 2025.
- STT 1 Apr 2026 confirmed by NSE circular FATAX73524 (primary).
- NSE Clearing FAQ (13 Oct 2025) saved as `references/22_…pdf`.

## Short selling in India (as framed in the project)
- **Eligibility: "securities traded in F&O segment shall be eligible for short selling"** (SEBI framework; Master Circular 16 Oct 2023 Annex 3). Intraday shorting of non-F&O stocks: broker-dependent, unresolved.
- Intraday cash shorting allowed (F&O-eligible stocks); naked short selling prohibited (SEBI 20 Dec 2007); SLB / institutional shorting from 21 Apr 2008
  but thin → persistent short exposure via SSF. MFs are legally *permitted* to short/SLB (MF Regs amended 2007; Slivka's "barred"
  is wrong/outdated), but arbitrage funds in practice run long-cash/short-futures.
- Settlement: cash T+1 (fully from 27 Jan 2023); stock F&O physically settled (all from Oct 2019 expiry).

## Data files (from project doc §8)
sec_bhavdata_full (delivery), UDiFF bhavcopy (ISIN-keyed, 2024+), F&O bhavcopy (settle/OI), combined OI/MWPL (with FutEq post-2025),
securities-in-ban CSV, shareholding pattern, results calendar, India VIX, F&O eligibility lists. Wrappers: R `nser`, Python scrapers.

## Added 5 Nov 2026: ban enforcement regimes (primary sources: references/23, references/24, references/19)
- To 22 Mar 2020: increases checked on END-OF-DAY positions only (NSE penalty text "at the end of each day ... increased
  his existing positions"); intraday round trips not violations (some brokers allowed them; Zerodha blocked them).
- 23 Mar 2020 →: SEBI PR 18/2020 (20 Mar 2020) Annex A 1(i): exchanges/CCs "shall check on an intra-day basis (monitoring of
  Peak intraday OI or Periodic intraday monitoring of OI)"; ICCL/BSE notice 20200322-2: violations "based on the monitoring
  of peak intraday positions"; penalty lower of 1% of value in violation or Rs 5 lakh per client, min Rs 50,000. Kept
  "till further directions" by PR 59/2020 (25 Nov 2020) although the MWPL halving was withdrawn.
- 1 Oct 2025 →: NSE Clearing 119/2025 §2.2: entity EOD FutEq vs base position (2 PM SPAN delta); penalty 1%, min 5,000,
  max 1 lakh. Broker notices date "delta-based exposure limits in ban period" to 8 Dec 2025 (unresolved).
- Data confirm: ban-day (ΔOI+V)/V median 0.871 (to 22 Mar 2020), 0.011 (23 Mar 2020–Sep 2025), 0.193 (Oct–7 Dec 2025),
  0.357 (8 Dec 2025 →).

## Added 7 Nov 2026 (re-verified against primary texts)
- **In-ban trading rule from 1 Oct 2025 is LOOSER than before** (SEBI 2025/79 §5.3.1 vs §5.3.2 + Table 2): old rule "trade
  only to decrease their positions through offsetting positions"; new rule: any trade allowed if the entity's end-of-day
  FutEq OI falls (e.g. adding a long put or a short call to a long future is permissible). The 2025 PACKAGE is not a
  relaxation (every MWPL fell; intraday MWPL monitoring with surveillance actions from 3 Nov 2025, §5.4).
- **Short selling** (SEBI circular SEBI/HO/MRD/MRD-PoD-3/P/CIR/2024/1, 5 Jan 2024, references/25, restating the 2007
  framework): all classes of investors may short; naked short selling not permitted (delivery at settlement mandatory);
  institutional investors may not day trade; securities traded in the F&O segment are eligible for short selling.
- **SLB is NOT limited to F&O stocks**: SEBI widened SLB to liquid non-F&O securities from 1 Jul 2013 (Business Standard,
  30 May 2013; secondary). NSE SLB bhavcopies: non-F&O stocks 0.5-2% of trade records 2015-17, 6-23% from 2019.
- NSE SLB bhavcopy URL: nsearchives.nseindia.com/archives/slbs/bhavcopy/SLBM_BC_DDMMYYYY.DAT (2015 → present).
- AMFI monthly report URL: portal.amfiindia.com/spages/am{mon}{yyyy}repo.xls; arbitrage funds a separate category from
  Apr 2018 (older layout to Mar 2019). AUM Apr 2018 56,218 cr → Sep 2026 2,97,632 cr.
- 30× volume MWPL leg: 2006 change to free float confirmed (Oneindia, 23 Sep 2006; SEBI 2010 circular keeps the 2006 method);
  the 2004 circular's text was not retrievable on 7 Nov.

## Added 9 Nov 2026
- COVID halving: 60 stocks halved in the 20 to 27 March 2020 files plus 1 on 29 April 2020 (61 in all); 70 restored in the
  26 November 2020 file (rule applied dynamically, so more stocks were halved at the end than in March).
- SEBI 2025/79 para 4.2 states the aim "Reduce instances of spurious F&O ban periods in single stocks"; para 5.2.5 ties
  the MWPL to delivery volume "to reduce the potential manipulation". SEBI 2024/132 para 2 cites increased retail
  participation and speculative expiry-day volumes.
- SEBI PR 22/2024 (23 Sep 2024): 93% of >1 crore individual F&O traders lost money FY22-FY24 (avg ~Rs 2 lakh incl. costs),
  aggregate >Rs 1.8 lakh crore; FY24 prop +Rs 33,000 cr, FPI +Rs 28,000 cr gross; 96-97% of their profits algorithmic.
