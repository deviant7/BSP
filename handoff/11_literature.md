# 11. Literature (verified from the PDFs) and positioning

PDFs: `references/1_...` to `22_...`; index `references/00_reference_index.md` (its corrections block at the end matters);
deep notes `references/notes_batch1..6_*.md`; verified digest `memory/02_literature_digest.md`; internal 29-page review
`BSP_Literature_Review.pdf` (LaTeX in `litreview_src/`, has known errors listed below). Shleifer-Vishny's PDF has a garbled
font layer: OCR with tesseract to read it.

## 11.1 Theory spine
- **Shleifer and Vishny (1997)**, JF 52(1) 35-55 (#1; NBER w5167). Specialised arbitrageurs with other people's money;
  performance-based arbitrage F2 = G(D1 p2/p1 + F1 - D1), G' > 0; resiliency dp2/dS = -1/(1 - G'F1/p1) < -1 (fire sales);
  high idiosyncratic volatility deters arbitrage; mispricing can widen before it closes.
- **Gromb and Vayanos (2010)**, ARFE 2, 251-275 (#2; NBER 15821). Survey; base price p_A = d_A + alpha sigma_A^2 (1 - rho^2) u;
  short-sale cost wedge c (one-sided); margins and leverage, LOP holds iff W >= 2|u| eps; constrained inefficiency.
  Caveat: Loewenstein and Willard (2006) show DSSW-type LOP failure is not robust.
- **De Long, Shleifer, Summers and Waldmann (1990)**, JPE 98(4) 703-738 (#3). OLG noise traders; price term
  -(2 gamma) mu^2 sigma_rho^2 / [r(1+r)^2]. Requires market-wide noise risk: weak basis for idiosyncratic volatility in a
  stock-level index.

## 11.2 Closest Indian precedents
- **Aggarwal (2015)**, IGIDR WP-2015-010 (#4). 141 NSE stock futures, one-second limit order book, 1 Mar to 31 Aug 2013;
  basis on midquotes with MIBOR, no dividends; 3-regime TAR per stock per day; bands +3 / -15 bp (~18 bp), wider and more
  asymmetric for illiquid stocks; median basis negative; PCA of daily bandwidths (PC1 17%); MIBOR explains ~18% of PC1;
  RBI 15 Jul 2013 tightening spiked bands; STT cut 1 Jun 2013 narrowed. Never uses the ban. Intraday market makers, not
  overnight carriers.
- **Shankar R.L., Sankar and Kiran Kumar (2015)**, NSE WP/16/2015; EMFT 55(7) 1619-1633 (2019) (#20). 102 stocks, 5-minute
  data 2007 to 2009; weekly 3-regime SETAR (AR(6), delay 1); kappa_L -39 bp, kappa_H -10 bp (both negative), band 28 bp;
  band 30 → 28 bp around SLB introduction (Apr 2008); liquid vs illiquid 27 vs 29 bp; volatility widens band, lower bound
  moves twice as much (short-sale asymmetry); futures impact cost matters more; model-free percentile bounds agree. No ban.
- **Nandan, Agrawal and Bhargava (2014)**, APJMRI 10(4) 413-422 (#8; not "Vision"). Nifty futures 2003 to 2012, daily
  close: 71% negative; mean -Rs 8.19; efficiency improved by 2012; no costs.
- **Nandan, Agrawal and Jindal (2015)**, IJF 9(9) 23-35 (#21). 5 stocks, 2012-13; underpricing larger but rarer; weak.
- **Roy and Chakraborty (2023)**, GBR 24(6) 1326-1352 (#9). 10 stocks 2011 to 2017, VECM: spot does most error
  correction (8 of 10); the old notes saying futures lead are wrong.
- **Slivka, Shah and Wu (2011)** (#11; published IJF 6(1) 11-18, 2012). Cost band ~2.47% for JSWSTEEL; their claim that
  arbitrage funds are barred from shorting is outdated.
- **Saurav, Srivastava and Agarwalla (2026)**, SSRN, "Decoupled: Disagreement, short-sale constraints, and
  law-of-one-price violations around earnings announcements". **Not read in full (paywalled from the container).**
  Abstract: Indian stock-futures basis turns negative before earnings and reverses after; strongest with high disagreement
  and strong short-sale constraints; vanishes near expiry; 1 SD lower pre-announcement basis → -0.22% returns days +1 to +5.
  **Closest competitor** to H2 and H7; the model's P10 remark predicts this pre-announcement signal should vanish in bans.
  Read before writing results.
- Jain, Agarwalla, Varma and Pandey (2018, JFM): informed trading around earnings shows in spot; stock futures dominate
  stock options in India.
- Vipul (2005, Vikalpa 30(4); 2008, JEMF 7(3)): high-volume stock futures generally overpriced; mispricing and OI.

## 11.3 Measurement and cross-section
- **Stambaugh, Yu and Yuan (2015)**, JF 70(5) 1903-1948 (#5). Mispricing score from 11 anomalies; IVOL effect negative
  among overpriced (-1.77%/month), positive among underpriced (+0.52%); method = double-sorted portfolios and sentiment
  regressions, **not Fama-MacBeth** (the internal lit review says FM: wrong).
- **Ofek, Richardson and Whitelaw (2004)**, JFE 74(2) 305-342 (#6). Put-call parity violations: R > 0 for 65.1%; after
  costs 13.63% above the upper bound; rebate spread predicts violations.
- **Harshita, Singh and Yadav (2018)**, TEL 8(14) 3178-3195 (#10). PEAD in India; SUE = (EPS_q - EPS_(q-4))/price; drift
  BHAR[+2,+64]; SUE x IVOL and SUE x illiquidity insignificant; survivorship (fixed Nifty-500 list).
- **Sehgal, Vasishth and Deisting (2024)**, Borsa Istanbul Review 24, 449-459 (#14). India: only MAX(L5) significant;
  **high-IVOL stocks outperform** (opposite of US); lottery factor.
- Hou and Moskowitz (2005, RFS 18(3)): price delay. Danielsen and Sorescu (2001, JFQA): option listing relaxes short
  constraints. Gagnon (2018, Financial Review 53(1) 5-50; **not obtained**): ~1,300 SSF listings lowered lending
  utilisation and fees. Miller (1977); Diamond and Verrecchia (1987).

## 11.4 Band econometrics
- **Dwyer, Locke and Yu (1996)**, RFS 9(1) 301-332 (#7a): symmetric TECM on S&P 500 minute data; thresholds about half
  the round-trip cost; no asymmetry.
- **Ters and Urban (2020)**, J. Financial Markets 47, 100503 (#7b; not IREF 2019): 3-regime TVECM, unknown beta;
  theta + beta0 (the cost) precisely identified though each is not; sup-LM tests with bootstrap; pre/post event use.
- **Tse (2001)**, JBF 25(10) 1829-1855 (#7c): ESTAR with heterogeneous arbitrageurs; reversion survives removing
  out-of-band observations.
- Hansen and Seo (2002, J. Econometrics); Dumas (1992, RFS) proportional-cost band.
- Brennan and Schwartz (1990, J. Business 63(1) S7-S31; **not obtained**): early-unwind option of arbitrage positions.

## 11.5 Retail and policy
- SEBI press release 22/2024 and study (#12): 93% of individual F&O traders lost money FY22 to FY24, average Rs 2 lakh,
  total > Rs 1.8 lakh crore; algorithmic share of prop/FPI profits 96 to 97%.
- Kumar (2009, JF 64(4)): lottery stocks; Barber and Odean (2000, JF; 2013 Handbook).

## 11.6 Known errors in the internal literature review PDF (fix before reuse)
SYY described as Fama-MacBeth; PEAD definitions; Roy-Chakraborty direction; Sehgal MAX(L5)/IVOL reversal omitted; DSSW
idiosyncratic caveat missing; GV's Loewenstein-Willard caveat missing; wrong venues for Nandan 2014, Ters-Urban, Sehgal.

## 11.7 Positioning statement (current)
"The ban is essentially unstudied" rests on targeted web, SSRN and Semantic Scholar searches (Oct 2026): no study of ban
effects found; re-check on Google Scholar/SSRN before writing it as fact, and read Saurav et al. in full.

## 11.8 Library papers (user offered to fetch)
Not blocking. Priority: (1) Saurav-Srivastava-Agarwalla 2026 (positioning of H2/H7); (2) Gagnon 2018 (H6 precedent);
(3) Brennan-Schwartz 1990 (early unwind; theory already built without it).

## Added 7 Nov 2026 (methods used in the secondary tests; standard references, details in docs/13)
Amihud (2002) illiquidity; Bali, Cakici and Whitelaw (2011) MAX; Calonico, Cattaneo and Titiunik (2014) robust RD;
Cattaneo, Jansson and Ma (2020) density test; Corwin and Schultz (2012) high-low spread; McCrary (2008); Newey and West
(1987); Sehgal, Vasishth and Deisting (2024) Indian lottery/IVOL premium (positive IVOL premium in India, so H5's IVOL
leg is two-sided). Saurav, Srivastava and Agarwalla (2026): our H2 finds their pre-announcement pattern (basis lower
before bad news) outside bans, 2 bp. Still not read in full (library).

## 11.9 Added 9 Nov 2026
The thesis now has a literature chapter (`thesis/ch_literature.tex`) written from the verified digest (memory/02), with
the old review's errors fixed (SYY double sorts; Harshita BHAR[+2,+64] and price-scaled SUE; Roy-Chakraborty: spot does the
correction; Sehgal: high IVOL outperforms in India; DSSW market-wide caveat; Loewenstein-Willard; correct venues). Claims
from papers not read in full (Saurav et al.; Gagnon; Brennan-Schwartz) are kept to what their abstracts or notes support.
The internal `BSP_Literature_Review.pdf` still has its known errors and is not used.
