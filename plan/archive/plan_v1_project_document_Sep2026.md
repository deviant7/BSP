**Bachelor\'s Thesis --- Final Project Document**

**Limits to Arbitrage in the Indian Equity Market**

*Why do mispricings survive, and what does that tell us about who sets
prices?*

**Student:** Prince · Roll No. 23B3032 · BS Economics, IIT Bombay
(2023--2027)

**Project guide:** Prof. Aditi Chaubal, Department of Economics, IIT
Bombay

**Course structure:** EC 495 --- Stage I (6 credits, Sem 7) · EC 497 ---
Stage II (12 credits, Sem 8)

**Date:** September 2026

**Contents**

**1. Overview and goal**

This project studies why price errors survive in Indian stocks. Textbook
theory says that if a stock is mispriced, arbitrageurs will trade
against the error and push the price back to fair value almost
instantly. In reality, mispricings persist for days or weeks. The
standard explanation is that arbitrage is not free: the traders who
would correct an error face capital limits, trading costs, and rules
that cap how large a position they may hold. These frictions are the
"limits to arbitrage."

India is an unusually clean laboratory for measuring these limits
because they are unusually visible and, in several cases, mechanically
imposed by the regulator. There is no genuine short selling in the cash
market, the stock-lending-and-borrowing (SLB) market is thin, and there
is an explicit rule --- the F&O "ban period" --- that halts fresh
derivative positions in a stock once open interest crosses 95% of that
stock's Market-Wide Position Limit (MWPL). The ban is mechanical,
precisely dated, and published every day by NSE.

The goal is to build a validated, reproducible measure of how tightly
arbitrage constraints bind across Indian stocks over time, and then to
establish *causally* how much of the observed mispricing in Indian
equities those constraints explain --- using the MWPL/ban mechanism and
the 2024--26 SEBI reforms as sources of identifying variation. The end
product is both a research contribution and a public-data toolkit that
other researchers can reuse.

**2. Motivation and basis**

**2.1 Why this question matters**

Whether a return pattern reflects risk or mispricing is one of the
central questions in asset pricing. If a pattern earns higher returns
precisely where arbitrage is hardest, that is evidence it is mispricing
being prevented from correcting, not compensation for risk. Measuring
the limits directly --- rather than assuming them --- lets us adjudicate
this for the Indian market, where the evidence is thin. The question is
also directly policy-relevant: through 2024--26 SEBI has been actively
resetting position limits, explicitly trading off speculation control
against market quality. This project measures the market-quality side of
that trade-off.

**2.2 Why India, and why now**

Two features make the timing ideal. First, India's constraint
architecture is distinct from the US and even from other emerging
markets --- the MWPL ban is a repeated, stock-specific,
mechanically-triggered contraction in arbitrage capacity that has
essentially no direct counterpart in the literature. Second, the
2024--26 reform wave delivered a dense sequence of dated, market-wide
changes to exactly the constraints this project studies. These are
natural experiments in which efficiency is the outcome variable, not the
assumption. The key reforms are summarised below.

  --------------------------------------------------------------------------
  **Reform**          **Effective**   **What changed**
  ------------------- --------------- --------------------------------------
  Minimum contract    20 Nov 2024     Fewer, larger index contracts; sharp
  size raised to      (phased to Feb  reduction in small-retail
  ₹15--20 lakh        2025)           participation

  Weekly expiries cut 20 Nov 2024     Bank Nifty, Fin Nifty, Midcap Select
  to one benchmark                    weeklies removed; only Nifty 50 weekly
  per exchange                        retained on NSE

  2% ELM on           20 Nov 2024     Higher cost of carrying speculative
  expiry-day short    (ELM) / 1 Feb   option positions
  options; upfront    2025 (premium)  
  option-premium                      
  collection                          

  Calendar-spread     1 Feb 2025      Higher margin for expiry-day spread
  margin benefit                      positions
  removed on expiry                   
  day                                 

  Intraday monitoring 1 Apr 2025      Limits checked through the day, not
  of index position                   only end-of-day
  limits                              

  New                 1 Jul 2025      Tighter caps on large index positions;
  index-derivative                    OI now measured in future-equivalent
  position limits                     (delta) terms
  (net ₹1,500 cr /                    
  gross ₹10,000 cr                    
  per PAN); FutEq                     
  (delta-based) OI in                 
  force                               

  New MWPL formula +  1 Oct 2025      MWPL = lower of {15% of free float,
  ban-period rule                     65× Average Daily Delivery Value
  recast in delta                     (ADDV)}, floor 10% of free float,
  terms                               recomputed quarterly; during a ban,
                                      positions must reduce end-of-day FutEq
                                      (delta) OI

  Intraday MWPL       3 Nov 2025      Stricter, higher-frequency MWPL
  monitoring for                      enforcement
  single stocks (≥4                   
  random checks/day);                 
  ≥14 constituents                    
  for non-benchmark                   
  index derivatives                   

  Pre-open session    6 Dec 2025      Further change to how the constraint
  extended to F&O;                    binds
  index-option limits                 
  move to normal                      
  (delta) enforcement                 
  --------------------------------------------------------------------------

Crucially, from 1 October 2025 the MWPL denominator is tied to Average
Daily Delivery Value --- a trailing cash-market delivery quantity
recomputed only once a quarter (rolling three-month ADDV) --- subject to
a 10%-of-free-float floor. Because that denominator moves for reasons
unrelated to today's derivative speculation and is reset only quarterly,
it is a clean source of variation in ban status, and it is central to
the identification strategy in Section 7. SEBI states one explicit aim
of this reform is to "reduce instances of spurious F&O ban periods in
single stocks" --- the very mechanism this project studies.

**3. Research questions**

**Primary question.** How strongly do arbitrage constraints bind in
Indian equities, and how much of the observed, persistent mispricing can
be attributed to them?

This decomposes into five sub-questions, each of which maps to a
chapter:

1.  Can we construct a single, credible, publicly-reproducible index of
    arbitrage-constraint intensity at the stock-day level?

2.  Do mispricings (futures-basis deviations, put-call-parity
    violations, post-earnings drift) widen and persist longer when
    constraints are tighter?

3.  Is the relationship causal --- i.e., does exogenously-induced ban
    status widen mispricing, once we strip out the endogenous crowding
    that triggers bans in the first place?

4.  How wide is the "no-arbitrage band" inside which prices do not
    correct, how does it vary across stocks, and did the 2025 reforms
    move it?

5.  Cross-sectionally, do well-known return signals pay more in
    high-constraint stocks --- the signature of mispricing rather than
    risk?

**4. Hypotheses**

Each hypothesis is stated with the theory it tests, so that a rejection
is as informative as a confirmation.

  --------------------------------------------------------------------------
  **\#**   **Hypothesis**                             **Grounded in**
  -------- ------------------------------------------ ----------------------
  H1       Mispricing magnitude rises with the        Shleifer--Vishny
           constraint index; deviations are both      (1997); Gromb--Vayanos
           larger and slower to correct when          
           constraints are tight.                     

  H2       Post-earnings-announcement drift is larger Limits-to-arbitrage
           for constrained stocks, and largest on     view of PEAD
           days a stock is actually in the ban.       

  H3       The no-arbitrage band is wider for         Transaction-cost band
           smaller, less liquid, more retail-owned    models; Aggarwal
           stocks, and widens with the constraint     (2015)
           index.                                     

  H4       The Oct 2025 (delivery-value-linked MWPL,  Constraint-intensity
           delta-based ban rule) and Dec 2025 changes interpretation of the
           narrow the band and shorten mispricing     reforms
           half-lives.                                

  H5       Known return signals earn higher returns   Stambaugh--Yu--Yuan
           among high-constraint stocks, consistent   (2015)
           with mispricing rather than risk.          

  H6       Mispricing responds to ban status induced  Identification /
           by MWPL-denominator revisions (variation   falsification
           orthogonal to current crowding), not only  
           to endogenous crowding.                    
  --------------------------------------------------------------------------

**5. Conceptual framework**

The organising idea is the no-arbitrage band. In a frictionless market,
the futures price equals its cost-of-carry fair value and put-call
parity holds exactly; any deviation is instantly traded away. With
frictions --- financing costs, short-sale and lending limits, and hard
position caps --- there is a band around fair value inside which the
expected profit from an arbitrage trade does not cover its cost, so
prices are left uncorrected. Only when a deviation pushes past the edge
of the band does correction kick in. The width of this band is a direct,
interpretable measure of the limits to arbitrage.

This yields a clean chain of reasoning that the whole project tests:
tighter constraints → a wider band → larger and more persistent
mispricing → and, in the cross-section, higher realised returns to
signals that bet against those mispricings. The MWPL ban is a sharp,
observable tightening of the constraint; the 2025 reforms are dated
shifts in its intensity. The band is naturally a non-linear, threshold
object --- prices barely adjust inside it and adjust quickly outside it
--- which is why the estimation uses threshold and smooth-transition
models rather than linear regressions, and why Prof. Chaubal's work in
non-linear time series is a strong fit.

**6. Literature and the research gap**

The project sits on three bodies of work. The theory of limits to
arbitrage --- Shleifer and Vishny (1997), the Gromb--Vayanos survey on
capital-constrained arbitrage, and Ofek, Richardson and Whitelaw (2004)
on put-call-parity violations under short-sale constraints --- provides
the mechanisms and the mispricing measures. The asset-pricing
consequence is Stambaugh, Yu and Yuan (2015), whose test of whether
anomalies concentrate where arbitrage is hardest is the template for the
cross-sectional chapter. The econometrics of transaction-cost bands ---
threshold and smooth-transition error-correction models of index-futures
arbitrage --- provides the estimation toolkit.

**The gap.** The closest Indian precedent is Aggarwal (2015, IGIDR), who
measures no-arbitrage bands between single-stock futures and spot prices
and finds funding liquidity drives their common variation --- but she
does not use the F&O ban / MWPL mechanism at all. Internationally,
position limits have been studied in Korea and Taiwan, but India's
specific MWPL ban is essentially unstudied as a shock to arbitrage
capacity. The existing Indian literature on derivatives and mispricing
is largely descriptive. So the measurement method exists and is
validated, and the constraint mechanism exists and is precisely
observable --- but no one has tied the two together. That junction is
the contribution.

**7. Methodology**

The work is organised into five methodological blocks that also serve as
thesis chapters, plus a concluding policy chapter. Each block uses a
genuinely different technique, which gives the thesis the breadth
expected at Stage II.

**7.1 Constructing the arbitrage-constraint index (Chapter 1)**

For each stock and each trading day, assemble a panel of constraint
proxies and reduce them to one index using principal-component analysis
(with a latent-factor model as a robustness alternative). Candidate
components:

-   Ban status (in-ban indicator) and length of the current ban spell.

-   MWPL utilisation --- open interest as a percentage of the stock's
    MWPL.

-   Futures-basis dispersion and magnitude (how far, and how variably,
    the basis strays from cost-of-carry).

-   Idiosyncratic volatility --- residual volatility from a factor
    model, the classic arbitrage-risk proxy.

-   Delivery percentage (from the MTO/full bhavcopy) as an inverse proxy
    for speculative, non-delivery trading.

-   Ownership breadth from quarterly shareholding filings ---
    investor-category shares and holder concentration.

-   Illiquidity (Amihud measure, bid-ask proxy) and SLB
    availability/cost where obtainable.

This chapter is deliberately designed to be a stand-alone deliverable: a
validated, reproducible measure of arbitrage-constraint intensity for
Indian equities, built entirely from public data, is publishable and
citable even if every later causal test comes back null.

**7.2 Measuring mispricing (Chapter 2)**

Three complementary, well-understood measures, so that no single noisy
measure drives the results: (i) deviation of the futures price from its
cost-of-carry fair value; (ii) put-call-parity deviations, restricted to
near-the-money options because settlement prices for thinly-traded
strikes are unreliable; and (iii) the magnitude of
post-earnings-announcement drift around scheduled results. Each is
computed at the stock-day (or stock-event) level so it can be matched to
the constraint index.

**7.3 Establishing causality (Chapter 3)**

The central threat is reverse causality: a stock enters the ban
precisely because speculative interest crowded into it, which is also
when mispricing is most likely. A naive "ban → wider basis" regression
would confuse the two. The identification strategy exploits the way the
ban threshold (95% of MWPL) is set. Before the reform MWPL was 20% of
free float (or 30× the prior month's average trading quantity); from 1
October 2025 it is the lower of 15% of free float or 65× the trailing
Average Daily Delivery Value (ADDV), floored at 10% of free float and
recomputed only once a quarter on a rolling three-month window. In both
regimes the denominator moves for reasons unconnected to today's
derivative trading --- free float changes with issuance and shareholding
shifts, and post-reform the binding term is a quarterly-reset
delivery-value figure --- so the same open interest can be in-ban or not
depending on stale, exogenous inputs. These denominator revisions give
variation in ban status that is plausibly orthogonal to current
mispricing, and serve as the instrument (the post-2025 ADDV rule, being
delivery-based and quarterly, is the cleaner instrument). A regression
discontinuity around the 95% threshold is reported as supporting
evidence, accompanied by a McCrary density test for
manipulation/bunching (the running variable is anticipated, so some
bunching is expected --- which is exactly why the RD is supporting, not
primary).

**7.4 The no-arbitrage band and the 2025 regime shifts (Chapter 4)**

Model price adjustment as a threshold process: little correction inside
the band, fast correction outside it. The workhorse estimator is a
three-regime threshold vector error-correction model (TVECM) with two
asymmetric thresholds and an unknown cointegrating vector (Ters and
Urban, 2020, extending Hansen and Seo, 2002), which recovers both the
no-arbitrage band and the implied overall arbitrage cost and is designed
for exactly this kind of pre/post-event analysis; a three-regime TAR
(following Aggarwal, 2015) and a smooth-transition (STAR) specification
are run as robustness. The band width is allowed to depend on the
constraint index from Chapter 1. The dated 2025 reforms then serve as
market-wide shifts in constraint intensity --- the FutEq (delta-based)
redefinition of open interest (in force by mid-2025), the new
delivery-value-linked MWPL and the delta-based ban-period rule (1
October 2025), and intraday MWPL monitoring (3 November 2025) ---
analysed with pre/post event windows and, where a cross-section of
treatment timing exists, staggered-treatment-robust
difference-in-differences estimators (Callaway--Sant'Anna,
Sun--Abraham).

**7.5 Cross-sectional asset-pricing test (Chapter 5)**

Using Fama--MacBeth regressions, test whether well-known return signals
earn higher returns among high-constraint stocks --- the direct
Stambaugh--Yu--Yuan test, which also reuses the existing 45-signal
long-short infrastructure. Because the derivatives universe is only
\~220 stocks, statistical power is limited; this chapter is reported as
secondary, corroborating evidence with honest power caveats, never as
the load-bearing result.

**7.6 Policy discussion (concluding chapter)**

The concluding chapter borrows the framing of the retail-participation
debate --- retail crowding is one reason stocks hit the position limit
in the first place --- and reads the results against SEBI's stated
trade-off between curbing speculation and preserving market quality.
This delivers the policy relevance of the alternative retail project
without depending on the firm-level retail-trading data that public
sources cannot provide.

**8. Data sources and access**

Every dataset is free and public, sourced from the exchange. This is a
deliberate design choice: it keeps the project fully reproducible and
removes any dependence on paid or proprietary feeds.

  -----------------------------------------------------------------------------------
  **Dataset (file)**     **Source**   **Key contents**                **Frequency**
  ---------------------- ------------ ------------------------------- ---------------
  Cash bhavcopy ---      NSE          OHLC, volume, and delivery      Daily
  sec_bhavdata_full                   quantity & % (delivery value →  
                                      Average Daily Delivery Value,   
                                      the post-2025 MWPL input)       

  Cash bhavcopy ---      NSE          ISIN-keyed OHLC (current file   Daily
  UDiFF                               format from 2024)               
  (BhavCopy_NSE_CM...)                                                

  F&O bhavcopy           NSE          Futures & options settlement    Daily
  (fo...bhav /                        prices, open interest, volume,  
  BhavCopy_NSE_FO...)                 contract specs                  

  Combined OI / MWPL     NSE          Per-stock MWPL, open interest   Daily
  file                                (notional and, post-2025,       
                                      FutEq/delta), and OI as % of    
                                      MWPL                            

  Securities in ban      NSE          List of stocks in F&O ban that  Daily
  period                              day                             

  Quarterly shareholding NSE/BSE      Ownership by category           Quarterly
  pattern                filings      (promoter, FII, DII,            
                                      individuals ≤₹2 lakh)           

  Corporate results /    NSE          Earnings dates & timestamps     Event
  announcements calendar              (for the PEAD measure)          

  India VIX              NSE          Implied-volatility index        Daily

  Index constituents &   NSE          Derivatives-universe membership Periodic
  F&O eligibility lists               over time                       
  -----------------------------------------------------------------------------------

Access is by direct download of the daily report files from NSE's
archives (with well-maintained open-source wrappers such as the R
package nser and Python scrapers available to automate bulk retrieval).
Archives extend comfortably past the proposed sample start of 2015. A
note on the mid-sample format change: NSE migrated its bhavcopy files to
the ISIN-keyed UDiFF format in 2024, so the data pipeline must handle
both the legacy and current layouts --- a routine but necessary cleaning
step.

**8.1 Sample and construction**

Proposed sample: 2015 to 2026, covering the roughly 220 stocks in the
F&O segment (with membership tracked over time, since the eligibility
list changes). Pre-2019 data can serve as a placebo/pre-retail-era
period. Construction proceeds from raw daily files to a cleaned
stock-day panel: merge cash and F&O records by symbol and date, compute
the basis and cost-of-carry fair value, attach ban status and MWPL
utilisation, join quarterly shareholding (forward-filled within
quarter), and flag earnings-event windows. Two construction points
follow from the reform: (i) MWPL must be reconstructed under both
regimes --- 20% of free float (or 30× prior-month volume) before the
change and, from 1 October 2025, the lower of 15% of free float or 65×
rolling-three-month ADDV with a 10%-free-float floor --- and switched at
the change date, which also yields the denominator revisions used as the
instrument; (ii) the post-2025 FutEq/delta open-interest measure
requires option deltas, computed from settlement-price-implied
volatilities. All cleaning steps are scripted and version-controlled so
the dataset is reproducible end-to-end.

**9. Expected results**

-   Mispricing measures widen and correct more slowly when the
    constraint index is high, with the effect strongest on days a stock
    is actually in the ban.

-   Post-earnings drift is larger in constrained stocks, since the
    trades that would close the gap are the ones being blocked.

-   The estimated no-arbitrage band is wider for smaller, less liquid,
    more retail-owned stocks.

-   The October and December 2025 relaxations show up as a narrowing of
    the band and shorter mispricing half-lives.

-   Return signals pay more in high-constraint stocks, supporting a
    mispricing rather than a risk interpretation.

**10. Deliverables and robustness to a null result**

The single most important design principle is that Chapter 1 --- the
validated, reproducible arbitrage-constraint measure --- is a
contribution in its own right. Theses fail when their entire value
hinges on the sign of one coefficient; this one is built so that even if
every causal test is insignificant, the constraint index, the cleaned
public-data panel, and the descriptive validation remain a usable,
citable asset. Concrete deliverables: (i) the reproducible stock-day
dataset and cleaning code; (ii) the constraint index and its
documentation; (iii) the causal and time-series results; and (iv) the
written thesis.

**11. Risks and mitigations**

  -----------------------------------------------------------------------
  **Risk**                          **Mitigation**
  --------------------------------- -------------------------------------
  Reverse causality --- bans are    Instrument ban status with
  triggered by the same crowding    MWPL-denominator revisions; treat the
  that causes mispricing.           RD as supporting evidence only.

  RD weakness --- the 95% running   Run the McCrary density test in the
  variable is anticipated and may   first month; lean on the instrument
  bunch.                            and dated reforms if bunching is
                                    severe.

  Low cross-sectional power ---     Report the Fama--MacBeth chapter as
  only \~220 F&O stocks.            secondary, with explicit power
                                    caveats.

  Unreliable option prices for thin Restrict put-call-parity tests to
  strikes.                          near-the-money contracts; rely on the
                                    futures basis as the primary
                                    mispricing measure.

  Mechanism changed mid-sample (Oct Split the sample at the change dates
  & Dec 2025).                      and treat each change as an
                                    additional, dated
                                    constraint-intensity shock.

  Bhavcopy format change (UDiFF,    Build the pipeline to parse both
  2024).                            legacy and current file layouts.
  -----------------------------------------------------------------------

**12. Indicative timeline**

**Stage I --- EC 495 (Semester 7)**

-   Weeks 1--3: literature review; finalise the mispricing measures and
    the constraint-index component list.

-   Weeks 4--8: build and clean the full stock-day dataset from NSE
    files.

-   Weeks 9--12: construct the constraint index; descriptive validation;
    run the McCrary test and an instrument-strength check to confirm the
    identification is viable.

-   End of semester: interim report with dataset, constraint measure,
    and preliminary findings.

**Stage II --- EC 497 (Semester 8)**

-   Weeks 1--5: main causal estimation (IV) and the 2025 rule-change
    analysis.

-   Weeks 6--9: threshold/smooth-transition band models and the
    cross-sectional Fama--MacBeth tests.

-   Weeks 10--12: robustness checks, policy chapter, and thesis writing.

**13. Indicative references**

1.  Aggarwal, N. (2015). Limits to Arbitrage: The Case of Single Stock
    Futures and Spot Prices. IGIDR Working Paper WP-2015-010.

2.  Barber, B. and Odean, T. Work on individual-investor trading and
    performance.

3.  De Long, J. B., Shleifer, A., Summers, L. and Waldmann, R. (1990).
    Noise Trader Risk in Financial Markets. Journal of Political
    Economy.

4.  Dwyer, G. P., Locke, P. and Yu, W. (1996). Index Arbitrage and
    Nonlinear Dynamics Between the S&P 500 Futures and Cash. Review of
    Financial Studies.

5.  Gromb, D. and Vayanos, D. (2010). Limits of Arbitrage: The State of
    the Theory. Annual Review of Financial Economics / NBER WP 15821.

6.  Hansen, B. E. and Seo, B. (2002). Testing for Two-Regime Threshold
    Cointegration in Vector Error-Correction Models. Journal of
    Econometrics.

7.  Kumar, A. (2009). Who Gambles in the Stock Market? Journal of
    Finance.

8.  Nandan, T., Agrawal, P. and Bhargava, S. (2014). Mispricing in CNX
    Nifty Futures: An Empirical Investigation.

9.  Ofek, E., Richardson, M. and Whitelaw, R. (2004). Limited Arbitrage
    and Short Sales Restrictions. Journal of Financial Economics.

10. Sehgal, S., Vasishth, V. and Deisting, F. (2024). Lottery Factor and
    Stock Returns: Evidence from India. Borsa Istanbul Review.

11. Shleifer, A. and Vishny, R. (1997). The Limits of Arbitrage. Journal
    of Finance.

12. Stambaugh, R., Yu, J. and Yuan, Y. (2015). Arbitrage Asymmetry and
    the Idiosyncratic Volatility Puzzle. Journal of Finance.

13. Ters, K. and Urban, J. (2020). Estimating Unknown Arbitrage Costs:
    Evidence from a 3-Regime Threshold Vector Error Correction Model.
    Journal of Financial Markets.

14. Tse, Y. (2001). Index Arbitrage with Heterogeneous Investors: A
    Smooth Transition Error Correction Analysis. Journal of Banking &
    Finance.

15. SEBI (2024). Measures to Strengthen Equity Index Derivatives
    Framework. Circular SEBI/HO/MRD/TPD-1/P/CIR/2024/132, 1 Oct 2024.

16. SEBI (2025). Measures for Enhancing Trading Convenience and
    Strengthening Risk Monitoring in Equity Derivatives. Circular
    SEBI/HO/MRD/TPD-1/P/CIR/2025/79, 29 May 2025.

17. SEBI (2024). Study on Profits and Losses of Individual Traders in
    the Equity F&O Segment (PR 22/2024).
