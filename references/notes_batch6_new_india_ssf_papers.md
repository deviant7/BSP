# Notes batch 6 — newly found Indian SSF-mispricing papers and primary sources (read in full, 28 Oct 2026)

## #20 Shankar R.L., Ganesh Sankar & Kiran Kumar K. (2015), "Mispricing in single stock futures: Empirical examination of Indian markets", NSE Working Paper WP/16/2015 (June 2015)
Published version: *Emerging Markets Finance and Trade* 55(7) 1619–1633 (2019), DOI 10.1080/1540496X.2018.1477681 (paywalled; WP read).
File: `20_shankar_sankar_kirankumar_2015_nse_wp_ssf_mispricing.pdf`.

**Data.** NSE high-frequency transaction data (not free), 102 stocks (of 170 in F&O on Jan 2007, dropping 30 newly added and
38 later removed/merged → survivorship), Jan 2007–Dec 2009. Prices sampled every 5 minutes (last trade in window); spurious ticks
removed (Zhou 1996 median filter, 5%). Near-month contract, switching to next month in expiry week.
**Mispricing.** π_t = (F^M − F)/S with F = (S − PV(D))e^{r(T−t)}, r = 14-day MIBOR, NSE dividend file (announcement & ex-dates).
Range −273 to +16 bp; median −12 bp (significantly ≠ 0). Mean mispricing −0.22%, mean raw basis +0.08% (Table 1).
**Method.** 3-regime SETAR, AR(6) in each regime, threshold variable π_{t−1}, thresholds by grid search minimising RSS (Yadav,
Pope & Paudyal 1994). Estimated **weekly** per firm (Mon–Fri, 5-min data), then firm means → cross-sectional mean (t-stats on
firm means). Model-free bounds = percentiles (10/20/25 and 90/80/75) of 5-min mispricing.
Panel regressions (firm FE, Petersen SEs) of weekly bounds on weekly realised variance (5-min returns, AR(1)-corrected),
lagged bound, weeks-to-maturity, SLB dummy; extended with relative impact cost (cash & futures, from 2 PM order-book snapshot,
₹5 lakh order).
**Results.**
- Mean κ_L = −39 bp, κ_H = −10 bp (both negative!), band κ_H − κ_L = 28 bp (Table 2). Authors note the negative upper bound is
  "surprising" if bands = costs; robust to model-free bounds and to raw basis (bands ~equal; so not an r artefact per authors).
- Pre-SLB (Jan 2007–Apr 2008) vs post-SLB (May 2008–Dec 2009): band 30 vs 28 bp; bounds less negative after → early SLB ineffective.
  Panel: D_SLB coefficient −0.0003 (band narrower by ~3 bp after SLB, significant).
- Liquidity terciles (pre-sample 2006 impact cost): band 27 bp (most liquid) vs 29 bp (least liquid) — economically weak;
  κ_L more negative for *liquid* stocks (−52 vs −20 bp) — unexplained ("we can only speculate").
- Volatility: weekly variance ↑ → band ↑ (coef 0.10); κ_L falls more than κ_H (−0.154 vs −0.069) → asymmetric, attributed to
  short-sale constraints (reverse arbitrage — long futures/short stock — infeasible; naked long futures faces margin calls).
  Model-free: +1% weekly variance → band +9.6 bp, LMB −12.1 bp, UMB −3.3 bp.
- Joint: cash RIC 0.0009 (t 3.5), futures RIC 0.0013 (t 5.2) → futures liquidity matters more; RV still positive.
- Bands narrow toward maturity (WTM positive).
**Institutional facts reported (secondary for us):** SEBI banned short selling (institutions) Mar 2001; Dec 2007 framework allowed
institutional short selling, naked shorting prohibited; SLB launched Apr 2008 with 7-day tenure → 1 month → 12 months (Jan 2010);
<0.5 mn shares lent in 2009 (80 trades). NSE publishes monthly impact cost (₹1 lakh order, 4 random snapshots/day).
**Assessment / relevance to BSP.**
- Closest precedent for our band chapter: Indian SSF, multi-regime, cross-section of ~100 stocks; it does **not** use the ban or MWPL
  → the gap claim survives.
- Intraday (5-min) — not reproducible with free daily data; their 28 bp band is a 5-minute object (cf. Aggarwal's 18 bp at 1 s).
- Two non-obvious facts to explain in our model: (i) **both bounds negative** — the "no-arbitrage band" is centred below zero
  (persistent underpricing, i.e., cash-and-carry capacity abundant while reverse arbitrage is blocked; or mis-measured carry);
  (ii) volatility widens the lower bound more → short-side constraint.
- The SLB-introduction comparison is a (weak) short-constraint shock design — precedent for our F&O-eligibility chapter.
- Weaknesses: survivorship (dropped removed stocks), weekly SETAR with AR(6) on ~375 obs (threshold estimates noisy, no inference
  on thresholds beyond t-stats of means), no transaction-cost benchmark, minor citation errors (Roll et al. dated 2009 for JF 2007).
- Useful method to copy: **model-free percentile bounds** as a cheap robustness check for our TVECM thresholds.
- New references to follow: Brennan & Schwartz (1990, J. Business 63(1) S7–S31) — early-exit (early unwinding) option — directly
  relevant to our ban model (in a ban, early *exit* is allowed but entry is not); Roll, Schwartz & Subrahmanyam (2007, JF 62(5))
  liquidity and the futures-cash basis; Fung & Draper (1999, JFM 19) short-sale relaxation in Hong Kong reduced mispricing;
  Yadav & Pope (1994); Vipul (2008, JFM 28(9)) PCP in India; Oehmke (2009) gradual arbitrage; Kondor (2009, JF 64) arbitrage risk.

## #21 Nandan, T., Agrawal, P. & Jindal, S. (2015), "An Empirical Investigation of Mispricing in Stock Futures at the National Stock Exchange", *Indian Journal of Finance* 9(9) 23–35, DOI 10.17010/ijf/2015/v9i9/77193
File: `21_nandan_agrawal_jindal_2015_ijf_stock_futures_mispricing.pdf`.

**Data.** 5 stocks (ICICI Bank, Infosys, Reliance, SBI, Tata Motors), daily near-month futures closes, 1 Jan 2012–24 Dec 2013;
expiry days dropped; 2,380 obs stated (tables sum to 2,365). One-month MIBOR; dividend-yield adjustment. Mispricing measured in
**rupees** (not normalised by price → not comparable across stocks). No transaction costs.
**Results.** Grand mean mispricing −₹1.15; overpricing more frequent but smaller, underpricing less frequent but ≥1.5× larger in
magnitude (except Reliance, Tata Motors 2013). Wilcoxon: significant only for SBI (negative) and Reliance (positive); **not
significant for 3 of 5** — so the abstract's "significant mispricing … mostly underpriced" overstates. Mispricing becomes less
negative toward expiry (Kruskal–Wallis significant for 4/5). Mispricing differs by sign of basis.
**Problems.** The "Theoretical Framework" states arbitrage directions *reversed* (says underpriced futures → short futures/long spot;
correct is long futures/short spot); basis defined as spot − futures; normality "p < 0.5" typo; tiny sample; no costs; closing-price
non-synchronicity acknowledged.
**Relevance.** Weak evidence, but consistent with the asymmetry (large underpricing ↔ blocked reverse arbitrage). Useful citations:
**Slivka, Wu & Shah (2012), "Arbitrage of single stocks versus futures in India: A case study", *Indian Journal of Finance* 6(1)
11–18** (= published version of our ref #11); Vipul (2005, *Vikalpa* 30(4) 25–38) temporal variation in futures mispricing;
Vipul (2008, *J. Emerging Market Finance* 7(3) 263–292) mispricing, volume, volatility and OI in Indian futures; Misra, Kannan &
Misra (2006); Fung & Draper (1999). States: "short-selling is restricted to intra-day in the spot market".

## #19 & #22 NSE Clearing primary sources (Sep/Oct 2025)
- #19 NCL circular 119/2025 (8 Sep 2025): SOP for new MWPL & ban-period monitoring (see `memory/07_fact_check.md` §A).
- #22 NCL FAQ "Recent changes in Equity Derivative segment … Securities in Ban Period" (updated 13 Oct 2025). Adds:
  - MWPL was previously disseminated **monthly** ("erstwhile monthly basis"), now quarterly (by the 20th of the last month).
  - Symbol-wise market-level FutEq OI already disseminated daily ("Combined Delta Equivalent Open Interest across exchanges"
    report); client-level FutEq method since NCL circular 14 Nov 2024 (NCL/CMPT/65087) → **pre-reform FutEq data exist** for
    the 1 Oct 2025 intensity design (no need to reconstruct deltas, if the archive goes back far enough).
  - From 1 Oct 2025, `combineoi_DDMMYYYY` and `ncloi` files gain a "FutEq OI" field; monthly `NPH_mmmyyyy.csv`
    (non-promoter holding → free float per stock) discontinued — **historic NPH files are a free-float data source**.
  - Ban penalty: lower of 1% of violating quantity value or ₹1 lakh, min ₹5,000, per entity per stock per day.
  - Expiry-day increase in FutEq OI for a banned stock due to expiry of near-month positions = passive breach, not penalised.

## Other related work found (not yet obtained)
- **Saurav, S., Srivastava, P. & Agarwalla, S.K. (2026), "Decoupled: Disagreement, Short-Sale Constraints, and Law-of-One-Price
  Violations Around Earnings Announcements", SSRN (Jan 2026).** Indian SSF: futures–cash basis turns negative before earnings and
  reverses after; strongest with high disagreement and strong short-sale constraints; vanishes near expiry; 1-SD lower pre-EA basis
  → −0.22% returns over days +1 to +5. **Very close to our H2/H7 — must read in full and position against it.**
- Jain, S., Agarwalla, S.K., Varma, J.R. & Pandey, A. (2018), "Informed trading around earnings announcements — Spot, futures, or
  options?", *J. Futures Markets* — informed trading shows in spot, SSF dominate SSO in India.
- Gagnon, L. (2018), "Short Sale Constraints and Single Stock Futures Introductions", *Financial Review* 53(1) 5–50 — ~1,300 OneChicago
  SSF listings 2003–09 lowered lending-market utilisation and loan fees → futures as synthetic shorting; precedent for Ch 6.
- Banerjee, A. & Banerjee, A. (2020), *J. Futures Markets* 40(3) 355–373 — minimum trade size in Indian SSF binds for algos.
- Kotha, K.K. (2018?), "Mis-pricing in Single Stock Futures: Evidence from National Stock Exchange of India" (likely related to #20).
