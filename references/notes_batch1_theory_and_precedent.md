# Reading Notes — Batch 1: Theory spine + closest precedent

Covers references 1–5 (Tiers 1–2). For each: the argument, the mechanism, the evidence/method, and **what we take for our project**. Where a full PDF isn't in the folder yet, notes are built from the verified abstract plus the canonical content; mark such papers for a verbatim re-read once you drop the journal PDF in `references/`.

---

## 1. Shleifer & Vishny (1997), "The Limits of Arbitrage," *Journal of Finance*

**The claim.** Textbook arbitrage assumes many small, well-capitalised traders who each take tiny positions against a mispricing. Real arbitrage is done by a *few specialised professionals* trading largely with *other people's money* (client capital). This separation of brains and capital is the whole story.

**The mechanism (performance-based arbitrage, "PBA").** Investors judge arbitrageurs by recent returns and pull capital after losses. So when a mispricing *widens* — the position moves against the arbitrageur before it converges — clients withdraw funds precisely when the opportunity is most attractive. The arbitrageur may be forced to *liquidate* into the mispricing, amplifying it rather than correcting it. Result: arbitrage is least effective exactly when it is most needed, and mispricings can be large and persistent.

**Key implications we use.**
- Arbitrage capacity is finite and *state-dependent* (shrinks in bad states). This is the conceptual basis for treating the F&O ban as a sharp, exogenous contraction in that capacity.
- "Prices can get worse before they get better" → mispricing has a *time dimension* (half-life), not just a level. Motivates modelling correction *speed* (our Ch 2/4), not only magnitude.
- Anomalies concentrate where arbitrage is hardest → sets up the cross-sectional test (Ch 5).

**For our project.** This is the theory our whole design operationalises. The MWPL ban is a clean, dated, mechanical instance of "arbitrage capacity suddenly removed." H1 (mispricing widens and persists under tight constraints) is the direct empirical translation of PBA. *(Read the JF/NBER-w5167 PDF line-by-line for the model's exact setup and the noise-trader "resiliency" condition.)*

---

## 2. Gromb & Vayanos (2010), "Limits of Arbitrage: The State of the Theory," NBER WP 15821

**What it is.** The field map. Nests every friction into one framework, so you can locate any specific mechanism (ours = position/capital limits) within the theory.

**The four costs faced by arbitrageurs (verified from abstract):**
1. **Risk** — fundamental *and* non-fundamental (noise-trader) risk.
2. **Short-selling costs** — borrowing fees, availability, outright bans.
3. **Leverage & margin constraints** — financing limits on how big a position can be.
4. **Constraints on equity capital** — the PBA/withdrawal channel from Shleifer-Vishny.

**Direction of the field (verified):** moving toward the role of *financial institutions and agency frictions* in asset prices; the authors frame this as able to "explain market anomalies and inform welfare and policy debates."

**For our project.** India stacks *all four* costs unusually high: no cash short-selling + thin SLB (cost 2), hard MWPL position caps + margin regime (cost 3), and a small pool of specialised arbitrage capital (cost 4). The MWPL ban is essentially a *hard leverage/position constraint that binds discretely*. Read the survey's simple nesting model to borrow its comparative statics: how each cost widens the price gap and how they interact — this is the theoretical scaffolding for the constraint index (Ch 1) and directly supports the "welfare/policy" framing of our concluding chapter.

---

## 3. De Long, Shleifer, Summers & Waldmann (1990), "Noise Trader Risk in Financial Markets," *JPE*

**The claim.** Even with no fundamental risk, the *unpredictability of noise traders' beliefs* is itself a risk that deters arbitrage. Arbitrageurs with short horizons fear that mispricing will get worse (noise traders become more pessimistic/optimistic) before it corrects, so they don't fully trade against it. Mispricing survives *in equilibrium*, and noise traders can even earn higher returns by bearing the risk they create.

**Why it matters here.**
- Provides the second leg of "why mispricing survives" (Shleifer-Vishny is the capital leg; DSSW is the risk leg). Together they justify a *no-arbitrage band* of finite width rather than instantaneous correction.
- The retail boom in India is, in this language, an increase in noise-trader presence → wider bands, more short-horizon reversal. This is exactly the bridge to our concluding policy chapter (retail crowding is *why* stocks hit the position limit).

**For our project.** Grounds H3 (band width larger for more retail-owned stocks) and the policy-chapter logic. Read for the horizon argument and the "create-your-own-space" risk that keeps arbitrageurs out.

---

## 4. Aggarwal, N. (2015), "Limits to Arbitrage: The Case of Single Stock Futures and Spot Prices," IGIDR WP-2015-010 ⭐ closest precedent

**Verified abstract/keywords.** "Market frictions such as transactions costs, funding constraints and short selling constraints limit arbitrage, but these frictions affect different stocks differently." Uses **intraday data** on liquid single-stock futures and their spot markets; constructs **no-arbitrage bands** to measure arbitrage efficiency per security. JEL G13, G14.

**Three findings we build on:**
1. **Large cross-sectional variation** in both the *width* and the *asymmetry* of no-arbitrage bands across stocks — frictions bite unevenly.
2. **Limited commonality**: only ~**17%** of the variation in band sizes is a common factor; most is stock-specific. (Tells us a constraint index must be largely *stock-level*, not just a market factor.)
3. **Funding liquidity** is the key driver of the *common* component — links band variation to Gromb-Vayanos cost (3)/(4).

**The gap = our contribution.** Aggarwal *measures* the bands and correlates them with funding liquidity. She does **not** use the F&O ban / MWPL mechanism, and she does **not** establish causality from a constraint shock to band width. Our project = her band-measurement method **+** the MWPL ban/denominator revisions as the identifying shock **+** the 2025 reforms as constraint-intensity shifts. So her methodology is our Chapter-1/Chapter-4 starting point and her result is the benchmark we extend.

**To do on the full PDF (get it into the folder):** copy her *exact* band-construction formulas (how transaction costs, financing, and the SSF-spot basis define the band edges), her filtering/cleaning of intraday data, and her PCA/common-component setup — we will replicate and then augment these. This is the single most important paper to read line-by-line.

---

## 5. Stambaugh, Yu & Yuan (2015), "Arbitrage Asymmetry and the Idiosyncratic Volatility Puzzle," *JF*

**Verified abstract (core).** Short selling faces greater risks/impediments than buying — "arbitrage asymmetry." Combined with mispricing, this explains the negative IVOL–return relation. The IVOL effect is **negative among overpriced** stocks but **positive among underpriced** stocks (mispricing measured by combining **11 return anomalies**); the negative side is stronger because shorting overpricing is harder. Aggregating gives the negative "puzzle." The IVOL effect also moves with **investor sentiment**, strongest among overpriced stocks.

**Method template we reuse:**
- Build a composite mispricing score from a *library* of anomalies (they use 11; we have ~45 signals) and sort stocks.
- Use **idiosyncratic volatility as the arbitrage-cost proxy**, and test whether anomaly/mispricing effects are stronger where arbitrage is harder.
- The *asymmetry* prediction (overpriced vs underpriced behave differently) is important for India: with **no cash short-selling**, the overpriced side should be *even more* constrained than in the US. That is a sharp, testable prediction our setting is unusually suited to.

**For our project.** This is the blueprint for Chapter 5 (H5): do our signals pay more in high-constraint stocks? And the asymmetry angle gives a distinctively-Indian twist — the short-side constraint is near-absolute here, so we predict a *stronger* overpricing-persistence than the US baseline. Idiosyncratic volatility also becomes one component of our constraint index (Ch 1). *(Read the JF/NBER-w18560 PDF for the anomaly list, the mispricing-score construction, and the sentiment interaction.)*

---

## Synthesis so far — the through-line for the thesis
Shleifer-Vishny (capital limits) + DSSW (noise-trader risk) explain **why a no-arbitrage band exists and persists**. Gromb-Vayanos **catalogues the frictions** that set its width. Aggarwal **measures that band in India** and ties it to funding liquidity — but stops short of a causal constraint shock. Stambaugh-Yu-Yuan turns the same logic into a **cross-sectional asset-pricing test**. Our project threads these together: *use India's mechanical MWPL ban (and its 2025 rule changes) as the missing causal shock to arbitrage capacity, measure its effect on the no-arbitrage band and on mispricing persistence, and check the cross-sectional signature — in a market where the short-side constraint is near-absolute.*

**Next batch:** Ofek-Richardson-Whitelaw (PCP method), the threshold/STAR band econometrics cluster, and the SEBI/NSE primary sources. Drop the `[lib]` PDFs (esp. Aggarwal full text, Stambaugh, Ofek et al.) into `references/` and I'll re-read them verbatim and tighten these notes with exact formulas and figures.
