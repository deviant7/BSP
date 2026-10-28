# Reading Notes — Batch 2: Methods & measurement (the how-to tier)

Covers references 4, 6, 7a–7c, read in full from the PDFs. This is the tier that tells us *exactly how to build the project*. Ends with a concrete methods blueprint mapping each technique to our chapters.

---

## 4. Aggarwal (2015), IGIDR WP-2015-010 — the methodological backbone ⭐⭐

**Setting & data.** NSE single-stock-futures (SSF) vs spot — a "clean" law-of-one-price pair (no index-basket staleness, no ADR time-zone issues, and *futures and spot trade on the same NSE platform*, so no time-asynchronicity). Intraday **limit-order-book data, 1-second frequency**, **141 F&O stocks**, **1 Mar–31 Aug 2013 (120 trading days)**. Near-month SSF, rolled 2 days before expiry. MIBOR as the funding/risk-free rate.

**The basis (our mispricing variable), exact definition:**
> z_{i,t} = [ F_{i,t} − S_{i,t}·exp((r_t − d_t)(T−t)) ] / S_{i,t}
where F, S are futures/spot **midquotes**, r = MIBOR, d = dividend yield (she drops d, citing Miller et al. 1994 — overnight ex-div removed by using intraday). Computed at 1-second frequency; daily value = intraday median.

**Supporting variables (all per-stock, per-day, from 1-sec data, annualised where risk):** basis risk σ_z (SD of basis in 5-min windows); liquidity cost = round-trip bid-ask spread on spot+SSF; liquidity risk σ_liq; stock volatility σ_r. These are the raw ingredients of a constraint measure.

**The band estimator — three-regime TAR (Yadav-Pope-Paudyal 1994; Dwyer et al. 1996):**
Regimes on the basis z_t: lower (z_{t−d} ≤ C1), middle/no-arbitrage (C1 < z_{t−d} < C2), upper (z_{t−d} > C2). In the middle band z is near-random-walk (no correction); outside it z is stationary and mean-reverts fast (arbitrage kicks in). Estimated **per stock, per day**; AIC picks lag length; delay parameter d chosen from a grid {1,5,…,300 sec} to meet stationarity + min AIC; ≥40% of obs constrained to the no-arb regime. **Bandwidth bw = C2 − C1.**

**Headline results (our benchmarks):**
- Average **upper threshold = 3 bps**, **lower threshold = −15 bps** → **band ≈ 18 bps, strongly asymmetric**. The wide *negative* side is the fingerprint of **short-sale constraints** (reverse-cash-and-carry needs borrowing stock; India's SLB is thin) — median basis is *negative* across every liquidity quartile for the same reason.
- **Cross-sectional variation:** band width and asymmetry *both rise as liquidity falls* (Q1 most-liquid upper threshold ≈ 0; Q4 least-liquid bands much wider).
- **Commonality (PCA on the cross-section of daily bandwidths):** first 3 PCs explain ~37%; **first PC = 17%** ("systematic component" of arbitrage frictions).
- **What drives the systematic component:** regressions on market liquidity/vol/liq-risk and **MIBOR**. **Funding liquidity (MIBOR) is the single strongest driver — R² ≈ 18%.** The **15–16 July 2013 RBI liquidity tightening** (MIBOR 7.88%→9.23% overnight) is used as a natural experiment: the systematic band component *jumped* on the intervention date — "an unintended consequence of an action by the regulator."

**Why this is our backbone.** Her pipeline *is* our Chapter-1/Chapter-4 pipeline: compute the basis, estimate the 3-regime TAR band per stock-day, PCA the bandwidths for a systematic constraint factor, then regress that factor on constraint drivers. **Our novelty is the driver:** she uses a funding-liquidity shock (RBI rate move); we swap in the **MWPL/F&O-ban mechanism and the 2024–26 rule changes** as the arbitrage-capacity shock — a stock-specific, mechanical, repeated shock she never touches. We also extend from her 6-month window to 2015–2026.
*Replication to-dos from her exact spec: midquote basis, 40% no-arb-regime constraint, AIC lag choice, delay-grid, per-stock-per-day estimation.*

---

## 6. Ofek, Richardson & Whitelaw (2004) — the put-call-parity mispricing measure ⭐

**Question.** Does put-call parity (PCP) break when you can't short, and by how much? PCP for American options: **S ≥ PV(K) + C − P + EEP**; the option-implied stock value is S* = PV(K) + C − P + EEP. Deviation S − S* is the mispricing.

**Short-sale-cost measure.** The **rebate-rate spread** — how far a stock's short-rebate rate sits below the normal ("cold") rate; a direct, continuous proxy for how binding the short-sale constraint is (the US analogue of India's missing-SLB problem). Data: OptionMetrics, July 1999–Nov 2001.

**Findings we use.**
- Violations are **asymmetric in the direction of the short-sale constraint**: after shorting costs, **13.63%** of stocks sit *above* the options-implied upper bound vs only **4.36%** below; mean deviation **2.71%**. (Same asymmetry logic as Aggarwal's −15 vs +3 bps.)
- Magnitude & probability of violation rise with the rebate-rate spread — a 1-SD drop in rebate spread → +0.67% deviation. Robust to option/equity liquidity and transaction costs.
- **Predictive:** bigger PCP violations + high shorting cost → **lower future stock returns** (over-optimism that can't be arbitraged away); long-industry/short-flagged-stocks CARs up to ~65% over the sample.

**For our project (Ch 2, mispricing measure #2).** Gives the exact PCP-deviation construction and the "restrict to near-the-money, account for early-exercise premium" discipline. Their asymmetry + predictability results are what we expect to find *amplified* in India, where the short side is near-shut. Caveat we already flagged: Indian single-stock option quotes are thin off-ATM, so keep to near-ATM strikes.

---

## 7. The no-arbitrage-band econometrics lineage (Ch 4 toolkit)

**7a. Dwyer, Locke & Yu (1996), *RFS* — the origin.** Cost-of-carry model with non-zero transaction costs → **threshold error-correction** between S&P 500 futures and cash. Establishes that "discontinuous arbitrage" produces a no-trade band and non-linear, regime-dependent mean reversion. This is the intellectual root of Aggarwal's TAR and of everything below.

**7b. Ters & Urban (2020), *J. Financial Markets* — our workhorse estimator. ⭐**
A **3-regime threshold VECM** with **two (asymmetric) thresholds** and an **unknown cointegrating vector** (extends Hansen-Seo 2002's 2-regime TVECM; adds a constant in the cointegration relation to handle a persistent non-zero basis). It estimates (i) the **no-arbitrage band** (where arbitrageurs don't trade), (ii) **overall transaction/arbitrage costs** even when they're opaque, and (iii) asymmetric positive vs negative thresholds. Critically, the authors pitch it **explicitly for pre-/post-event regulatory analysis**: "regulators can… monitor how fast markets return to equilibrium after an exogenous shock… a pre- and post-event analysis can evaluate the effectiveness of policy actions." That is *precisely* our 2025-reform design. Advantages over smooth models: no transition function to specify, and long-run estimation error doesn't contaminate short-run terms (Seo 2011).

**7c. Tse (2001), *JBF* — the smooth-transition alternative.** Models DJIA futures-cash mispricing as a **STAR** process where the *speed of adjustment varies smoothly with the size of the mispricing*, motivated by **heterogeneous** arbitrageurs (different costs/capital). Shows the mean reversion is real (heterogeneous traders), not a stale-price illusion. This is our robustness alternative to the "abrupt" threshold: if traders are heterogeneous, a smooth transition fits better.

**Lineage to cite in one breath:** Cost-of-carry + transaction costs (Dwyer 1996) → univariate TAR (Yadav-Pope-Paudyal 1994; Martens et al. 1998; Forbes et al. 1999) → smooth-transition/STAR for heterogeneity (Tse 2001) → multivariate threshold cointegration (Balke-Fomby 1997; Hansen-Seo 2002) → **3-regime TVECM for event studies (Ters-Urban 2020)**. Aggarwal (2015) applied the univariate-TAR branch to Indian SSF; we upgrade to the Ters-Urban branch to exploit our dated policy shocks.

---

## Methods blueprint for our project (what to build, from this tier)

**Chapter 1 — constraint index.** Reuse Aggarwal's per-stock-per-day pipeline: compute the midquote basis z, estimate the 3-regime band, and PCA the cross-section of bandwidths for a *systematic arbitrage-constraint factor*. Augment the raw inputs with the MWPL-specific variables (ban dummy, %MWPL utilisation, delivery %, ownership breadth) so our index is richer than hers.

**Chapter 2 — mispricing.** Three measures: (a) futures-basis deviation (Aggarwal's z); (b) PCP deviation, near-ATM, with EEP (Ofek et al.); (c) PEAD (Batch 3). Each matched to the constraint index.

**Chapter 4 — bands + causal regime shifts.** Estimate no-arbitrage bands with the **Ters-Urban 3-regime TVECM** (asymmetric thresholds, unknown cointegrating vector), let the thresholds depend on the constraint index, and run **pre-/post-event windows around the dated 2024–26 reforms** (esp. 1 Oct 2025 ban relaxation + volume-linked MWPL, and Dec 2025 changes). Cross-check with a STAR spec (Tse) for heterogeneity robustness. This is the exact use case Ters-Urban advertise.

**The one methodological gap to solve early.** Aggarwal/Ters-Urban both use *high-frequency intraday* data; the sharpest band estimates want intraday, which is the one input we don't have free at scale for 2015–2026. Decision: estimate bands at the finest frequency we can obtain (daily settlement basis at minimum; intraday for a sub-sample/sub-period if we can source it), and lean on the *daily* ban/MWPL panel — which is fully public — for the causal identification. Confirm the frequency feasibility in Stage-I week 1–3.

---
**Progress:** Batches 1–2 done (theory spine + methods). **Next:** Batch 3 — Indian market evidence (8 Nandan, 9 Roy-Chakraborty, 10 PEAD-India, 11 Slivka); Batch 4 — behavioural/retail (13 Kumar, 14 lottery-India, 15a/b Barber-Odean) + SEBI study (12); Batch 5 — primary sources (16, 17 SEBI circulars, 18 NSE MWPL rules). Plus an OCR pass on #1 Shleifer-Vishny to upgrade Batch-1 notes from the actual text.
