# 07 — Fact-check log (internet verification, 28 Oct 2026)

Status codes: **✔P** verified against a primary source (circular / paper PDF / official page);
**✔S** verified only via consistent secondary sources (brokers, news, law-firm notes);
**✎** claim was wrong or imprecise → correction given; **?** could not be verified; **NEW** new fact found.
Primary PDFs in `references/` (SEBI 2024/132, SEBI 2025/79, SEBI PR 22/2024, all papers) count as ✔P.

## A. F&O ban and MWPL
| Claim | Status | Evidence / correction |
|---|---|---|
| Ban starts when market-wide OI > 95% of MWPL (EoD), from next day; only position-reducing trades | ✔P | NSE Clearing circ. 119/2025 (8 Sep 2025), SOP §2.1.1, 2.2 (`references/19_…pdf`); SEBI 2025/79; Dec 2024 Master Circular as quoted by NSE |
| **Ban exit at 80%** | ✔P | NSE Clearing 119/2025 §2.1.2: "In line with existing practice, normal trading… resumed only after the Combined FutEq OI across all Exchanges comes down to 80% of the MWPL" (also BSE page wording "80% or below") |
| Ban applies to all expiries of that stock's futures *and* options; index derivatives exempt; cash segment unaffected | ✔S | Broker FAQs (Zerodha, ICICI, Angel One); consistent with "trade only to decrease positions" |
| **Rollover not permitted during ban** (rolling = new position in next expiry) | ✔S | Geojit, Kotak, 5paisa FAQs citing SEBI; not seen in a circular |
| Penalty for increasing positions in ban | ✔P NEW | 1% of violation value, min ₹5,000, max ₹1,00,000 per entity per stock per day (NSE Clearing 119/2025 §2.5) |
| **Pre-2025 MWPL = 20% of non-promoter shares** | ✔P | SEBI 2025/79 §5.2.1 (quoting Master Circular); SEBI/DNPD/Cir-31/2006 (22 Sep 2006) "henceforth linked to free float… 20% of the number of shares held by non-promoters" |
| Project doc: MWPL was "20% of free float **or 30× prior-month volume**" | ✎ | The "lower of 30× average daily shares traded in previous month or 20% non-promoter" rule is from **SEBI/DNPD/Cir-26/2004/07/16 (16 Jul 2004)**; the 2006 circular replaced it with 20% free float. For the 2015–2025 sample MWPL = 20% FF only. Delete the "30×" leg from the project doc and pipeline. |
| New MWPL = min(15% FF, 65×ADDV), floor 10% FF, quarterly, effective 1 Oct 2025 | ✔P | SEBI 2025/79 §5.2.2 & table; NSE Clearing 119/2025 "effective from October 01, 2025" |
| ADDV is a *value* | ✎ | NSE Clearing SOP: "65 times market wide ADDV **[in terms of quantity]**" — computed in shares. Window example: MWPL from 1 Oct 2025 uses trades 16 Jun–15 Sep 2025; applicable for next 3 calendar months; published by the 20th of the last month of the quarter; adjusted for corporate actions on ex-date |
| Ban test on FutEq OI from 1 Oct 2025; gross-OI monitoring discontinued | ✔P | NSE Clearing 119/2025 §2.1.1, 2.1.5. (A Zerodha note dates the switch to 6 Dec 2025 — conflicts with the NSE circular; NSE circular is authoritative; check ban files around Oct–Dec 2025 in the data) |
| Ban-period delta rule: EoD FutEq must not rise; sign flip = violation; passive changes not a breach; deltas from 2 PM SPAN file | ✔P | NSE Clearing 119/2025 §2.2 |
| Intraday MWPL monitoring single stocks, ≥4 random snapshots, from 3 Nov 2025 | ✔P | SEBI 2025/79; NSE Surveillance circ. 849/2025 (31 Oct 2025) |
| Entity limits from 1 Oct 2025 (Client 10%, Pro 20%, FPI-I/MF/Pro+Client 30% of MWPL) | ✔P | SEBI 2025/79 §5.8 |
| **NEW: COVID-19 MWPL halving** | ✔S NEW | SEBI measures of 20 Mar 2020: exchanges cut MWPL to 50% for F&O stocks with avg daily high–low variation ≥15% over last 5 sessions *or* avg MWPL utilisation ≥40%; effective 23 Mar 2020; extended (to 30 Jul, 24 Sep 2020); withdrawn effective end of 26 Nov 2020 (JSA, Moneylife, TaxGuru, NSE circular) → mechanical, rule-based MWPL variation inside the sample |
| 2016: combined F&O position limit for brokers/FPIs/MFs = 20% of MWPL | ✔S | Business Standard 27 Dec 2016; TaxHeal |
| Index trading-member position limits raised Oct 2024 (higher of ₹7,500 cr or 15% OI) | ✔S NEW | Business Standard Oct 2024 (index only) |

## B. Short selling, SLB, settlement
| Claim | Status | Evidence / correction |
|---|---|---|
| Naked short selling not permitted; all investors may short sell with obligation to deliver at settlement (SEBI MRD/DoP/SE/Dep/Cir-14/2007, 20 Dec 2007) | ✔S | BSE short-selling page; Nishith Desai; Legal500 |
| Intraday cash shorting allowed; no overnight naked shorts; SLB thin → SSF the practical overnight short | ✔S | as above; project-doc line "no genuine short selling in the cash market" remains wrong |
| SLB / institutional short selling from 21 Apr 2008 | ✔S | Business Standard/2008 commentary ("short selling by institutional investors reintroduced from April 21, 2008") |
| Slivka: "arbitrage mutual funds are barred from shorting" | ✎ | SEBI amended MF Regulations (Nov 2007) to *enable* MF short selling and SLB; current MF Master Circular permits it with disclosures. In practice arbitrage funds run long-cash/short-futures. Write: "MFs may legally short via SLB but in practice do cash-and-carry via futures." |
| Stock derivatives physically settled | ✔S | SEBI framework Apr 2018 moved stocks failing enhanced criteria to physical settlement (from Jul 2018 expiry); Dec 2018 framework: bottom 50 from Apr 2019 expiry, next 50 Jul 2019, rest Oct 2019 → all physically settled from Oct 2019 |
| Stock options European | ✔S | SEBI circ. 27 Oct 2010; NSE: all stock options expiring 27 Jan 2011 onward European |
| T+1 cash settlement | ✔S | Phased from 25 Feb 2022 (bottom 100 stocks); fully implemented 27 Jan 2023 |
| Cash closing price = VWAP of last 30 min | ✔S | NSE practice (multiple sources) — **until 3 Aug 2026 for F&O stocks** |
| **NEW: Closing Auction Session (CAS)** | ✔S NEW | From 3 Aug 2026 closing price of F&O stocks set by a closing auction (3:15–3:35 PM, random close 3:28–3:30); non-F&O stocks keep VWAP close; derivatives trade to 3:40 PM (Zerodha bulletin 23 Jan 2026 citing NSE circ. CMPT72373). Pre-open changes 7 Sep 2026 → **measurement break for the basis in the last months of the sample** |
| Stock futures daily settlement = last half-hour weighted average price (across exchanges) | ✔P | NSE equity-derivatives settlement-price page |
| UDiFF format | ✔P | Old CM common bhavcopy discontinued w.e.f. 8 Jul 2024 (NSE circ. 62424, 12 Jun 2024); F&O old format dates staggered (some from May 2024) — parse both |

## C. Costs, margins, capital
| Claim | Status | Evidence |
|---|---|---|
| Futures STT cut 0.017% → 0.01% (sell side), 1 Jun 2013 | ✔S | Business Standard / NSE (Finance Act 2013) — Aggarwal's "STT cut 1 Jun 2013" consistent |
| Futures STT 0.0125% → 0.02%; options 0.0625% → 0.1% of premium, 1 Oct 2024 | ✔S | Budget July 2024 coverage (Business Standard etc.) |
| **NEW: Budget 2026: futures STT 0.02% → 0.05%; options premium 0.1% → 0.15%, exercise 0.125% → 0.15%; effective 1 Apr 2026** | ✔S NEW | Multiple outlets (HDFC Sky, Groww, 1Finance, ELP law note). Check Finance Act 2026 text before final use. → large dated cost shock |
| Peak margin: 25% (Dec 2020), 50% (Mar 2021), 75% (Jun 2021), 100% (1 Sep 2021) | ✔S | Upstox, Moneylife, Money9 |
| Debt-fund tax change from 1 Apr 2023 (≤35% equity → slab rate); arbitrage funds still equity-taxed → inflows | ✔S | Business Standard, Value Research, Freefincal |
| Arbitrage-fund AUM ≈ ₹71,106 cr (Apr 2023) → ₹1,98,981 cr (Oct 2024) (AMFI) | ✔S | Business Standard Nov 2024 — confirm from AMFI monthly data |

## D. F&O eligibility
| Claim | Status | Evidence |
|---|---|---|
| 2018 criteria: top 500 by mcap & traded value; MQSOS ≥ ₹25 lakh; MWPL ≥ ₹500 cr; ADDV ≥ ₹10 cr (6-month rolling) | ✔S | Moneylife, marketcalls, SEBI 2024 consultation summaries |
| SEBI circ. SEBI/HO/MRD/MRD-PoD-2/P/CIR/2024/116 (30 Aug 2024): MQSOS ₹75 lakh, MWPL ₹1,500 cr, ADDV ₹35 cr; exit after failing for 3 consecutive months; 6-month gestation for existing stocks | ✔S | NSE selection-criteria page cites it; Angel One, LiveLaw, BusinessWorld |
| F&O universe ≈ 220 stocks | ✔S | ~213 single-stock F&O underlyings on 21 Oct 2026 (Algotest), 6 added 28 Oct 2026; quarterly entry/exit continues (e.g., 8 added 1 Apr 2026; exits announced May 2026) |

## E. Index-derivative reforms (project doc table)
| Claim | Status | Evidence |
|---|---|---|
| 20 Nov 2024 one weekly benchmark per exchange; NSE kept only Nifty 50 weekly (Bank Nifty, FinNifty, Midcap Select weeklies ended 13/18/19 Nov 2024) | ✔P/✔S | SEBI 2024/132; NSE circ. 10 Oct 2024 (Business Today, Outlook) |
| Later: expiries standardised to Tuesday/Thursday (2025); NSE moved to Tuesday | ✔S NEW | Business Standard 26 May 2025; Business Today Jun 2025 |
| Other 2024/132 measures & dates | ✔P | repo PDF |
| SEBI PR 22/2024 numbers | ✔P | repo PDF |

## F. Literature: bibliographic details
| Reference | Status | Note |
|---|---|---|
| Shleifer & Vishny (1997) JF 52(1) 35–55 | ✔ | NBER w5167 (1995) is the version in repo |
| Gromb & Vayanos (2010) ARFE 2: 251–275 | ✔ | repo = NBER w15821 "…The State of the Theory" |
| De Long et al. (1990) JPE 98(4) 703–738 | ✔ | |
| Aggarwal (2015) IGIDR WP-2015-010 | ✔ | RePEc igiwpp/2015-010 |
| Stambaugh, Yu & Yuan (2015) JF 70(5) 1903–1948 | ✔ | repo = NBER 18560 (2012); numbers quoted are from the WP — check against JF version if cited |
| Ofek, Richardson & Whitelaw (2004) JFE 74(2) 305–342 | ✔ | repo = NBER 9423; ">65% cumulative abnormal returns" confirmed in NBER abstract |
| Dwyer, Locke & Yu (1996) RFS 9(1) 301–332 | ✔ | |
| **Ters & Urban (2020) JFM 47, 100503** | ✔ | DOI 10.1016/j.finmar.2019.07.002; earlier BIS WP 689 (2018). Reference index's "IREF 2019" is wrong |
| Tse (2001) JBF 25(10) 1829–1855 | ✔ | |
| **Nandan, Agrawal & Bhargava (2014) APJMRI 10(4) 413–422** | ✔P | from PDF header (Shachi Bhargava), DOI 10.1177/2319510X14553726. Index's "*Vision*" is wrong |
| **Roy & Chakraborty, GBR 24(6) 1326–1352 (2023)** | ✔P | from PDF; online first 2020; DOI 10.1177/0972150920920462 |
| Harshita, Singh & Yadav (2018) TEL 8(14) 3178–3195 | ✔P | |
| Slivka, Shah & Wu (2011) NYU-Poly WP | ✔P | PDF (12 Sep 2011) |
| Kumar (2009) JF 64(4) 1889–1933 | ✔ | |
| **Sehgal, Vasishth & Deisting (2024) Borsa Istanbul Rev. 24, 449–459** | ✔P | PDF header; index's "JBEF" is wrong |
| Barber & Odean (2000) JF 55(2) 773–806; (2013) Handbook Econ. Finance 2B 1533–1570 | ✔ | |
| Hansen & Seo (2002) J. Econometrics 110(2) 293–318 | ✔ | |
| Loewenstein & Willard (2006) JF 61(1) 231–258 | ✔ | abstract confirms LOP-violation result is not robust |
| Miller (1977) JF 32(4); Diamond & Verrecchia (1987) JFE 18(2) 277–311 | ✔ | (Miller page numbers not seen online) |
| Danielsen & Sorescu (2001) JFQA 36(4) 451–484 | ✔ | |
| Hou & Moskowitz (2005) RFS 18(3) 981–1020 | ✔ | |
| Dumas (1992) RFS 5(2) 153–180 | ✔ | |
| Callaway & Sant'Anna (2021) JoE 225(2) 200–230; Sun & Abraham (2021) JoE 225(2) 175–199 | ✔ | |
| McCrary (2008) JoE 142(2) 698–714 | ✔S | NBER TWP 334 confirmed; journal pages from memory |

## G. Research-gap and positioning claims
| Claim | Status | Note |
|---|---|---|
| "India's MWPL ban is essentially unstudied" | ✔ (provisional) | Several targeted searches found no academic study of ban effects — only broker explainers. Re-check on Google Scholar/SSRN/JSTOR before writing it as fact |
| "Position limits have been studied in Korea and Taiwan" (project doc §6) | ? | No supporting study found; drop or replace with a real citation |
| Related Indian work found (not yet read) | NEW | Nandan, Agrawal & Jindal (2015) *Indian J. Finance* 9(9) — stock-futures mispricing at NSE, mostly underpricing, attributed to short-sale restrictions; NSE working paper (2015, Shankar R.L., Ganesh Sankar, Kiran Kumar K.) on mispricing bounds in SSF using multi-regime models for 100+ stocks — **must read: closest daily/multi-regime precedent** |

## H. Implications carried into plan v2
1. Remove the 30× leg; MWPL pre-Oct-2025 = 20% FF (with the 2020 COVID halving as an exception).
2. ADDV in quantity; quarterly windows as in NSE SOP.
3. 80% exit confirmed → hysteresis design is feasible.
4. New dated shocks: STT 1 Apr 2026; COVID MWPL halving 23 Mar–26 Nov 2020; CAS 3 Aug 2026 (measurement break).
5. MF short-selling statement corrected.
6. Read the two newly found Indian papers.

## I. Open checks closed (28 Oct 2026, second pass)
| Item | Status | Evidence |
|---|---|---|
| Futures STT 0.05%, options premium 0.15%, exercise 0.15% from 1 Apr 2026 | ✔P | NSE circular FATAX73524 (Finance Act 2026, Presidential assent 30 Mar 2026); I-T Dept FAQ: delivery/other STT unchanged |
| FutEq-based ban test from 1 Oct 2025 (vs secondary claims of 6/8 Dec 2025) | ✔P | NSE Clearing FAQ updated 13 Oct 2025 (`references/22_…pdf`): ban under "new mechanism" on FutEq; limits effective trade date 1 Oct 2025. December dates in broker blogs remain unexplained — check the daily ban files Oct–Dec 2025 in the data |
| MWPL recomputation frequency before Oct 2025 | ✔P NEW | NSE Clearing FAQ: quarterly now, "in contrary to the erstwhile **monthly** basis" (monthly NPH files) |
| Market-level FutEq OI published before the reform | ✔P NEW | FAQ: symbol-wise FutEq OI disseminated daily ("Combined Delta Equivalent Open Interest across exchanges"); client-level method NCL/CMPT/65087 (14 Nov 2024) |
| Short-selling eligibility | ✔S NEW / ✎ | SEBI framework (2007; Master Circular 16 Oct 2023, Annexure 3; restated 5 Jan 2024): "**securities traded in F&O segment shall be eligible for short selling**"; SLB-eligible list likewise. Practice for intraday shorts in non-F&O stocks is broker-dependent (unresolved). → "intraday cash shorting allowed" must be qualified: formally for F&O securities. SEBI to set up a working group (2026) to review short selling/SLB (Multibagg, Jul 2026) |
| AMFI arbitrage-fund series | ✔S | AMFI discloses arbitrage-fund flows/AUM separately from mid-2018 (Cafemutual); e.g., Oct 2018 AUM ₹59,538 cr; Sep 2017 ₹55,921 cr (pre-categorisation figure). Monthly series feasible from 2018 |
| "Ban essentially unstudied" | ✔ (stronger, still provisional) | Web + Semantic Scholar search (API rate-limited) found no study of ban effects. Closest: Shankar et al. (2015/2019) — bands, no ban; Saurav, Srivastava & Agarwalla (2026, SSRN) — basis around earnings & short-sale constraints (must read; may use ban/OI) |
| Slivka et al. published version | NEW | *Indian Journal of Finance* 6(1) 11–18 (2012) (cited by Nandan et al. 2015) |
| NSE "60% MWPL" alert | ? | One secondary source mentions an NSE alert at 60% utilisation — unverified |
