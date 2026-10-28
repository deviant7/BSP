# BSP Reference Library — Master Index

**Project:** Limits to Arbitrage in the Indian Equity Market
**Guide:** Prof. Aditi Chaubal · **Student:** Prince (23B3032)
**Purpose:** relevance-ordered reading list + download checklist. Read top-down — Tier 1 first.

Legend: ⭐ = read line-by-line, core to the thesis · ○ = read carefully, chapter-specific · ▹ = skim / reference as needed
Access: **[free]** downloadable now · **[lib]** use IITB library / journal access · **[gov]** public regulator/exchange doc

---

## Tier 1 — Foundational theory (the spine of the whole project)

**1. ⭐ Shleifer, A. & Vishny, R. (1997). "The Limits of Arbitrage." *Journal of Finance* 52(1).**
The anchor paper. Arbitrage is done by specialists using other people's money; when prices move against them, capital is withdrawn exactly when the opportunity is best, so mispricing can widen before it corrects. This is the *mechanism* our entire project measures.
Extract: the performance-based-arbitrage model; why arbitrage is least effective when most needed; the "prices can get worse before better" logic.
[free] NBER WP 5167: https://www.nber.org/papers/w5167 · [lib] JF DOI: 10.1111/j.1540-6261.1997.tb03807.x

**2. ⭐ Gromb, D. & Vayanos, D. (2010). "Limits of Arbitrage: The State of the Theory." NBER WP 15821 / *Annual Review of Financial Economics*.**
The map of the whole field — organises every friction (funding constraints, margin, segmentation, noise-trader risk) into one framework. Read this second to see where our MWPL-ban mechanism sits in the taxonomy.
Extract: the funding-constraint models; how position/capital limits generate price gaps; the survey's open questions (our contribution answers one).
[free] https://www.nber.org/papers/w15821

**3. ⭐ De Long, Shleifer, Summers & Waldmann (1990). "Noise Trader Risk in Financial Markets." *Journal of Political Economy* 98(4).**
Why rational arbitrageurs don't fully correct errors: the noise traders' own unpredictability is a risk that limits arbitrage. Foundational for the "why mispricing survives" framing and for the retail/policy chapter.
Extract: noise-trader risk as a limit; the survival of mispricing in equilibrium.
[lib] JPE DOI: 10.1086/261703 (free PDFs widely available via Scholar)

---

## Tier 2 — Method + closest Indian precedent (this is where our contribution lives)

**4. ⭐ Aggarwal, N. (2015). "Limits to Arbitrage: The Case of Single Stock Futures and Spot Prices." IGIDR WP-2015-010.**
THE closest precedent. Builds no-arbitrage bands between Indian single-stock futures and spot, finds large cross-sectional variation and that funding liquidity drives the common component — but never uses the F&O ban / MWPL. Our project = her method + the ban as the identifying shock. Read every line; our Chapter 1 & 4 method starts here.
Extract: exact band-construction methodology; her data and sample; the funding-liquidity result; precisely what she does NOT do (the gap).
[free] IGIDR: http://www.igidr.ac.in/pdf/publication/WP-2015-10.pdf · SSRN 2585876 · RePEc: https://ideas.repec.org/p/ind/igiwpp/2015-010.html

**5. ⭐ Stambaugh, R., Yu, J. & Yuan, Y. (2015). "Arbitrage Asymmetry and the Idiosyncratic Volatility Puzzle." *Journal of Finance* 70(5).**
The template for our cross-sectional chapter (Ch 5): anomalies are stronger where arbitrage is harder, and short-side constraints make the effect asymmetric. Directly motivates H5.
Extract: how they proxy arbitrage difficulty (idiosyncratic vol); the asymmetry argument; the Fama-MacBeth-style cross-sectional design.
[free] NBER WP 18560: https://www.nber.org/papers/w18560 · SSRN 2155491 · [lib] JF DOI: 10.1111/jofi.12286

**6. ○ Ofek, E., Richardson, M. & Whitelaw, R. (2004). "Limited Arbitrage and Short Sales Restrictions: Evidence from the Options Markets." *Journal of Financial Economics* 74(2).**
The put-call-parity-violation methodology we use to measure mispricing (Ch 2). Shows PCP deviations track short-sale constraints.
Extract: the PCP-deviation measure; how they link it to constraints; the near-the-money focus (relevant to our thin-strike caveat).
[free] NBER WP 9423: https://www.nber.org/papers/w9423 · [lib] JFE DOI: 10.1016/j.jfineco.2003.05.008

**7. ○ Threshold / smooth-transition arbitrage-band econometrics (pick 2–3):**
The estimation toolkit for the no-arbitrage band (Ch 4). Our band is a threshold object, hence TAR/STAR/TVECM.
 - Dwyer, Locke & Yu (1996), "Index arbitrage and nonlinear dynamics between the S&P 500 futures and cash," *Review of Financial Studies*. [lib] DOI: 10.1093/rfs/9.1.301
 - Three-regime threshold VECM for arbitrage costs, *International Review of Economics & Finance* (2019). [lib] https://www.sciencedirect.com/science/article/abs/pii/S1386418119300084
 - Smooth-transition error-correction index arbitrage. [lib] https://www.sciencedirect.com/science/article/abs/pii/S037842660000162X
Extract: how the no-trade band is estimated; how transaction costs map to the threshold; specification/testing choices.

---

## Tier 3 — Indian market mispricing & efficiency evidence (background + calibration)

**8. ○ Nandan, T., Agrawal, P. & Bhargava, S. (2014). "Mispricing in CNX Nifty Futures: An Empirical Investigation." *Vision* (Sage).**
Baseline Indian index-futures basis-mispricing evidence — magnitude and behaviour of the basis we'll be modelling.
[lib] DOI: 10.1177/2319510X14553726

**9. ▹ Roy, P. S. & Chakraborty, T. (2023). "Efficiency of Indian Equity Futures Market." *Global Business Review* (Sage).**
More recent Indian arbitrage-efficiency evidence; useful for framing and comparison.
[lib] DOI: 10.1177/0972150920920462

**10. ○ "Post-Earnings-Announcement Drift Anomaly in India: A Test of Market Efficiency." *Theoretical Economics Letters* (2018).**
Establishes PEAD exists in India — the third mispricing measure (Ch 2). Open access.
[free] https://www.scirp.org/pdf/tel_2018102515432009.pdf

**11. ▹ Slivka, R., Shah, V. & Wu, J. "Arbitrage of Single Stocks Versus Futures in India." SSRN.**
Practitioner-flavoured single-stock arbitrage evidence for India; useful cross-check on band magnitudes.
[free] SSRN 1953878: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1953878

---

## Tier 4 — Behavioural & retail (for the concluding policy chapter)

**12. ○ SEBI (2024). "Analysis of Profit and Loss of Individual Traders in Equity F&O Segment."**
The authoritative retail-loss study: 93% of individual F&O traders lost money; ₹1.8 lakh cr over FY22–24. The policy-chapter backbone and the reason we don't try to re-estimate welfare ourselves.
[gov] Press release: https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html

**13. ▹ Kumar, A. (2009). "Who Gambles in the Stock Market?" *Journal of Finance* 64(4).**
Lottery-stock preference among retail — frames who crowds into constrained names.
[lib] JF DOI: 10.1111/j.1540-6261.2009.01483.x (author PDF on request/Scholar)

**14. ▹ "Lottery factor and stock returns: Evidence from India" (2024), *J. Behavioral & Experimental Finance*.**
The Indian lottery-preference result already exists — cite it, don't re-do it.
[lib] https://www.sciencedirect.com/science/article/pii/S2214845024000267

**15. ▹ Barber, B. & Odean, T. — individual-investor trading & performance (e.g., "Trading Is Hazardous to Your Wealth," 2000; "The Behavior of Individual Investors," 2013).**
Classic retail-underperformance evidence for the policy framing.
[free] Author PDFs via UC Davis / Haas faculty pages.

---

## Tier 5 — Regulatory & exchange primary sources (institutional detail — read for exact rules/dates)

**16. ⭐ SEBI circular (1 Oct 2024): "Measures to Strengthen Equity Index Derivatives Framework for Investor Protection."**
The reform package: lot-size hike, weekly-expiry consolidation, upfront premium, ELM, calendar-spread margin, intraday monitoring — with exact dates. Primary source for our reform timeline.
[gov] sebi.gov.in → Legal → Circulars (Oct 2024)

**17. ⭐ SEBI circular (30 May 2025): FutEq (delta-based OI), revised MWPL, ban-period relaxation, new position limits.**
The Oct 2025 / Dec 2025 changes that give us the constraint-intensity shocks and the volume-linked MWPL denominator (key to identification).
[gov] sebi.gov.in → Legal → Circulars (May 2025)

**18. ○ NSE — MWPL / F&O ban methodology & daily reports documentation.**
The mechanical rules (95% entry, 80% release; MWPL formula) and the data-file layouts we'll actually download.
[gov] nseindia.com → Products → Derivatives → Position Limits; Historical Reports.


**19. ⭐ NSE Clearing circular 119/2025 (8 Sep 2025) — SOP for new MWPL & ban-period monitoring.** (`19_nse_clearing_circ119_2025_mwpl_sop.pdf`)
Primary source: MWPL = min(15% FF, 65× ADDV in quantity), floor 10% FF, quarterly; ban at FutEq OI > 95%, exit at 80%; penalties. Effective 1 Oct 2025.

**20. ⭐ Shankar, Sankar & Kiran Kumar (2015), "Mispricing in single stock futures: Empirical examination of Indian markets", NSE WP/16/2015; publ. Emerging Markets Finance & Trade 55(7) 1619–1633 (2019).** (`20_…pdf`)
Closest Indian multi-regime (SETAR) precedent: 102 stocks, 5-min data 2007–09; band ≈ 28 bp, both bounds negative; volatility & futures illiquidity widen the band. No ban/MWPL.

**21. ○ Nandan, Agrawal & Jindal (2015), "An Empirical Investigation of Mispricing in Stock Futures at the NSE", Indian Journal of Finance 9(9) 23–35.** (`21_…pdf`)
5 stocks, daily 2012–13; underpricing larger than overpricing; weak methods (see notes batch 6).

**22. ○ NSE Clearing FAQ on position limits, limit monitoring and ban period (updated 13 Oct 2025).** (`22_…pdf`)
Data-file details (combineoi FutEq field, NPH files, base-position files); MWPL previously monthly.

**Corrections to entries above (fact-check 28 Oct 2026, see `memory/07_fact_check.md`):** #7b Ters–Urban is *J. Financial Markets* 47 (2020) 100503, not IREF 2019; #8 Nandan et al. (2014) is *Asia-Pacific J. Mgmt Research & Innovation* 10(4) 413–422, not *Vision*; #14 Sehgal et al. is *Borsa Istanbul Review* 24 (2024) 449–459; #11 Slivka et al. also published as Indian J. Finance 6(1) 11–18 (2012); #17's "ban-period relaxation" wording is inaccurate (new rule = must reduce FutEq delta; 3 Nov 2025 intraday monitoring is a tightening).

---

## Reading order (suggested)
1) Papers 1 → 2 → 3 (theory), 2) Paper 4 (Aggarwal — the method + gap), 3) Papers 5, 6 (cross-section + PCP), 4) Paper 7 cluster (band econometrics), 5) Papers 16–18 (institutional rules), 6) Tier 3 for Indian calibration, 7) Tier 4 last (policy chapter).

## Notes
- Per-paper reading notes will be saved alongside as `notes_<n>_<shortname>.md`.
- [lib] items: download the journal PDF via IITB access and drop it here as `<n>_<shortname>.pdf` so it can be read line-by-line.
