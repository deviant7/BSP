# 02 — Literature digest (verified by reading the PDFs in full, 28 Oct 2026)

Numbering follows `references/`. Items marked ⚠ are where existing notes/lit review are wrong or incomplete.

1. **Shleifer & Vishny (1997)** (NBER w5167, OCR'd). 3 periods; noise-trader pessimism S_t; p1=V−S1+D1, p2=V−S2+F2; F2=G(D1 p2/p1 + F1−D1),
   G'>0 (PBA). Full investment if recovery likely. Resiliency dp2/dS = −1/(1−G'F1/p1) < −1 (fire-sale). Markets with high
   *idiosyncratic* volatility deter specialised arbitrageurs; anomalies persist where arbitrage returns are volatile (vs Merton).
2. **Gromb & Vayanos (2010)** NBER 15821. Base: p_A = d̄_A + α σ_A²(1−ρ²) u (eq 6). Non-fundamental risk raises vol to
   σ_A√(1+α²σ_A⁴(1−ρ²)²σ_u²)/… (eq 10). Short-sale cost c: p_A = … + c if u>0 (13b). Leverage: margins m± ; LOP enforced iff
   W1 ≥ 2|u|ε (eq 17). ⚠ Notes Loewenstein–Willard (2006): DSSW's LOP failure not robust. Welfare: constrained inefficiency/pecuniary externality.
3. **DSSW (1990)** JPE. OLG, safe s (price 1) & unsafe u (unit supply), noise share μ, ρ_t~N(ρ*,σ_ρ²), CARA 2γ.
   p_t = 1 + μ(ρ_t−ρ*)/(1+r) + μρ*/r − (2γ)μ²σ_ρ²/[r(1+r)²]. Noise traders can earn more (hold-more/create-space vs price-pressure/
   Friedman). ⚠ Requires *market-wide* noise risk; idiosyncratic misperceptions are arbitraged away/unpriced → weak basis for
   putting IVOL in a stock-level index. Long horizons restore fundamentals.
4. **Aggarwal (2015)** IGIDR WP-2015-010. 141 NSE SSF/spot pairs, **1-second LOB data**, 1 Mar–31 Aug 2013 (120 days). Basis
   z=[F−S e^{(r−d)(T−t)}]/S (midquotes, MIBOR, no dividend). 3-regime TAR per stock per day; delay grid 1…300 s; AIC lags; ≥40% obs in
   middle regime. Upper +3 bp, lower −15 bp (band ≈18 bp), asymmetry & width rise with illiquidity; median basis negative in all
   quartiles. PCA on daily bandwidths: PC1 17% (first three 34% in intro, 37% in §5 — paper inconsistent). PC1 regressions:
   MIBOR R²≈18% (1 SD MIBOR → 1.22 SD band); RBI 15 Jul 2013 tightening (MIBOR 7.88→9.23%) spiked band; STT cut (1 Jun 2013) dummy negative.
5. **Stambaugh, Yu & Yuan (2015)** NBER 18560. Mispricing score = average rank over 11 anomalies (failure prob., O-score, net issues,
   composite issues, accruals, NOA, momentum, gross profitability, asset growth, ROA, investment/assets). IVOL = sd of daily FF3 residuals,
   previous month. Most overpriced: high−low IVOL −1.77%/mo; most underpriced +0.52%/mo; all stocks −1.30%. Stronger after high
   Baker–Wurgler sentiment. ⚠ Method = double-sorted VW portfolios + time-series sentiment regressions, **not Fama–MacBeth** (lit review wrong).
6. **Ofek, Richardson & Whitelaw (2004)** NBER 9423. OptionMetrics, 118 dates Jul 1999–Nov 2001; S ≥ PV(K)+C−P+EEP; R=100 ln(S/S*);
   near-ATM |ln(S/K)|<0.1, 91–182 days. R>0 for 65.1% (69.5% if rebate<0). After shorting & bid/ask costs: 13.63% above upper bound
   vs much fewer below (doc quotes 4.36%); mean violation 2.71–2.84%. 1-SD rebate drop → +0.67%. Short-leg returns: up to ~65% cumulative.
7a. **Dwyer, Locke & Yu (1996)** RFS. S&P 500 minute data 1982–90; symmetric TECM; thresholds ≈ ½ round-trip cost (median 0.00102–0.00163);
   delay ≤3 min later; Monte Carlo LR test; ARCH; basis converges in 5–7 min outside band vs 15 inside. Found NO asymmetry.
7b. **Ters & Urban (2020)** J. Financial Markets 47 (⚠ index says IREF 2019 — wrong). 3-regime TVECM, unknown β, constant β0;
   sequential dynamic grid search; θ and β0 individually poorly identified, **θ+β0 (= transaction cost) precise**; sup-LM with fixed-regressor
   & residual bootstrap; trimming π0=0.1; half-life = ln0.5/lnφ; HAS/GG price discovery; palladium example. Pitched for pre/post regulatory events.
7c. **Tse (2001)** JBF. DJIA futures, 5-min, Jun 1998–Mar 1999; ESTAR with heterogeneous arbitrageurs; mean reversion survives removing
   out-of-band obs (simulation) → arbitrage not stale-price illusion; STAR-ECM with EGARCH; futures lead; faster response to negative mispricing.
8. **Nandan, Agrawal & Bhargava (2014)** ⚠ *Asia-Pacific J. Mgmt Research & Innovation* 10(4) (index says *Vision* — wrong).
   Nifty futures daily close 2003–12, 2,382 obs; mean −₹8.19; 71% negative; neg −₹13.99 vs pos +₹6.04; falls with days-to-expiry;
   −₹24.3 (2007) → −₹0.23 (2012); non-parametric tests; ignores costs. Cites Vipul (2005): high-volume *stock* futures generally overpriced.
9. **Roy & Chakraborty (2023)** GBR 24(6). 10 stocks, daily, Jan 2011–Jan 2017, Johansen/VECM/IRF. ⚠ **Spot does most error correction**
   (8/10); neither market dominates price discovery; basis AR(2)+ → "unexploited arbitrage" (no costs). Notes/review say futures lead — wrong.
10. **Harshita, Singh & Yadav (2018)** TEL. Nifty-500 (fixed 31 Mar 2014 list → survivorship), 2002Q4–2017Q3, Ace Equity (paid) data.
   ⚠ SUE = (EPS_q − EPS_{q−4}) / **price** (6–12 days pre); PEAD = **BHAR [+2,+64]**; FM on coded SUE: 0.06 (6%). Interactions:
   SUE×Value +, SUE×Beta −; **SUE×IVOL and SUE×illiquidity insignificant** (bad news for an IVOL-based H2).
11. **Slivka, Shah & Wu (2011)** NYU-Poly WP. Cost-based zero-arbitrage band for SSF ≈ **2.47%** (JSWSTEEL), 2× S&P/FTSE (~1%);
   arbitrage mostly intraday single-stock; arbitrage MFs barred from shorting → forward arb only; short selling permitted only on F&O stocks then.
   ⚠ Not reconciled with Aggarwal's 18 bp (different arbitrageur/horizon).
12. **SEBI PR 22/2024** (23 Sep 2024): 93% of >1 cr individuals lost FY22–24, avg ₹2 lakh; total >₹1.8 lakh cr; FY24 Pro +₹33k cr, FPI +₹28k cr,
   individuals −₹61k cr; 96–97% of Pro/FPI profits algorithmic; <30 yrs 31%→43%; 72% B30; >75% income <₹5 lakh; >75% loss-makers continued.
13. **Kumar (2009)** JF. Lottery stocks = low price, high IVOL, high idio skew (k=50th pct, independent sorts); US discount broker 1991–96.
   Retail overweights (3.74% vs mkt 1.25%), institutions underweight; price strongest characteristic; demand ↑ with unemployment;
   lottery stocks underperform ≥4%/yr; investors lose 1.1–3%/yr; regressive.
14. **Sehgal, Vasishth & Deisting (2024)** Borsa Istanbul Rev. 24(3) (⚠ index says JBEF). NSE Dec 2001–Mar 2021. Only **MAX(L5)**
   (max return in last 5 days of prior month) significant (1.33%/mo); ⚠ **high-IVOL stocks OUTperform** (1.5%/mo) — reverse of US;
   low-price effect = size effect; lottery index (MAX, skew, tail risk, low IVOL) 2.01%/mo; lottery factor absorbs anomalies in FF5;
   retail-driven (low institutional holdings); stronger in bull markets/attention. Footnote: shorts can't be held overnight in India.
15a. **Barber & Odean (2000)** JF. 66,465 households 1991–96; top-turnover quintile net 11.4% vs market 17.9%, least-trading 18.5%;
   avg household FF alpha −31 bp/mo; gross returns ordinary → costs + overconfidence. Not about price impact.
15b. **Barber & Odean (2013)** Handbook survey: underperformance before & after costs (except short-horizon US); disposition effect;
   attention-driven buying; under-diversification; short-run order-imbalance predictability; Hirshleifer et al. (2008) could not tie
   PEAD to individual trades.
16–18: see `03_institutional_facts.md`.

## Cross-cutting implications noted
- Our planned data are DAILY; the 18 bp band is an intraday HFT object. Daily close / settlement (NSE uses last-30-min VWAP for both)
  measures a persistent component; calibration of c, c_s must say which arbitrageur.
- India-specific reversals (IVOL premium positive; low-price = size) mean US results (SYY, Kumar) cannot be transplanted blindly.
