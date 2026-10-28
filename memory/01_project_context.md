# 01 — Project context (design, plan, history)

## Who / what
- Student: Prince Kumar (23B3032), 4th-year BS Economics, IIT Bombay. Background: quant research intern at a trading firm
  (mid-frequency desk; F&O long-short pipeline, iron condors, merger arb, WorldQuant alphas; a ~45-signal long-short library).
  Works on Indian markets.
- Course: BSP = EC 495 (Stage I, 6 cr, Sem 7, ~Jul–Nov 2026) + EC 497 (Stage II, 12 cr, Sem 8, ~Jan–Apr 2027).
- Guide: Prof. Aditi Chaubal (approved Project 1). Other possible faculty mentioned early: Radeef Chundakkadan, Puja Padhi, Tara Shankar Shaw.

## How the topic was chosen (Very old conversation)
- Seven ideas → user wanted a multi-chapter research *program*, public data. Two programs evaluated:
  - **Program A (chosen): Limits to arbitrage** — F&O ban/MWPL as constraint shock. Literature gap: ban essentially unstudied.
  - **Program B (dropped): Retail transformation** — fatal measurement problem: participant-wise OI is market-level only,
    shareholding measures ownership not trading; 2024–26 reforms are index-level (N≈1–2, no DiD); welfare already estimated by SEBI.
    Survives only as the concluding policy chapter.
- Key advice then: make Chapter 1 (the constraint measure) a deliverable that survives a null; run McCrary early.

## The study plan (BSP_Project_Document, Sep 2026) — the user's master plan
Primary Q: how strongly do arbitrage constraints bind in Indian equities, and how much persistent mispricing do they explain?
Chapters / methods:
1. **Constraint index** (stock-day, PCA; latent factor robustness): ban dummy & spell length, %MWPL utilisation, futures-basis
   dispersion/magnitude, IVOL, delivery %, ownership breadth (quarterly shareholding), Amihud/bid-ask, SLB where available.
2. **Mispricing measures**: (i) futures basis vs cost-of-carry, (ii) near-ATM put-call-parity deviation, (iii) PEAD.
3. **Causality**: instrument ban status with MWPL-denominator revisions (pre-reform 20% FF [doc also says "or 30× prior-month
   volume" — unverified]; post 1 Oct 2025 min(15% FF, 65×ADDV), floor 10% FF, quarterly); RD at 95% as supporting, with McCrary.
4. **No-arbitrage band + 2025 regime shifts**: Ters–Urban 3-regime TVECM (workhorse), TAR (Aggarwal) & STAR (Tse) robustness;
   band allowed to depend on index; reforms as dated intensity shocks; Callaway–Sant'Anna/Sun–Abraham if staggered.
5. **Cross-section**: Fama–MacBeth; signals earn more in high-constraint stocks (SYY); secondary, power caveats (~220 stocks).
6. **Policy chapter**: retail crowding (SEBI loss study, Kumar, lottery) read against SEBI's speculation-vs-quality trade-off.
Hypotheses H1–H6: H1 mispricing ↑ with index; H2 PEAD larger for constrained, largest in ban; H3 band wider for small/illiquid/
retail-owned; H4 Oct & Dec 2025 changes narrow band & shorten half-lives; H5 signals pay more in high-constraint; H6 mispricing
responds to denominator-induced ban status.
Data (all free NSE): sec_bhavdata_full (OHLC, delivery qty/%), UDiFF bhavcopy (2024+ format change), F&O bhavcopy (settle, OI),
combined OI/MWPL file, securities-in-ban list, quarterly shareholding, results calendar, India VIX, F&O eligibility lists.
Timeline in doc: Stage I wk1–3 lit review, wk4–8 dataset, wk9–12 index + McCrary + first stage, interim report; Stage II causal,
bands, FM, robustness, writing.

## The pivot (guide's suggestion, ~Sep 2026)
- Prof. Chaubal: before empirical work, build a theoretical/mathematical model of what the project will show, so the
  conclusions are theory-derived (guards against confirmation bias/overfitting).
- Response so far: deep literature review (29 pp, math), then two candidate models (A: constrained arbitrage with MWPL cap, KKT;
  B: impulse-control band of inaction, b=(6Kσ²/θ)^{1/4}, "bridge" to TAR/TVECM). Both "deliver" six requirements = H1–H6.
  Final model choice deferred to guide. Progress report + 3-pp guide versions written Sep 28.
- No data downloaded, no empirical work yet.

## Corrections already folded into review/models (but NOT into the Word doc)
- Short selling: intraday cash shorting allowed; naked overnight shorting barred; SLB thin → SSF is the practical channel.
  The project doc §1 still says "no genuine short selling in the cash market" (fix pending).
- MWPL formula is 65× ADDV (delivery VALUE), floor 10% FF, quarterly (doc already corrected).
- Timeline in doc still lacks the theory stage (pending).

## Current status (28 Oct 2026)
- See `05_session_log.md` for the latest decisions and open threads.
