# Reading Notes — Batch 4: Retail & behavioural (policy-chapter tier)

Covers references 12–15. These feed the concluding **policy chapter** (retail crowding as the demand-side reason stocks hit the position limit) and the noise-trader leg of "why mispricing survives." Not identification — supporting/framing.

---

## 12. SEBI (Sep 2024), PR 22/2024 — individual F&O trader losses ⭐ (the policy anchor)

Authoritative regulator study, FY22–FY24 (follow-up to Jan 2023 study). Key findings, verbatim-grade:
- **93%** of >1 crore individual F&O traders lost money over FY22–24; **average loss ≈ ₹2 lakh/trader** (incl. costs). **Only 1%** earned >₹1 lakh.
- Top 3.5% of loss-makers (~4 lakh traders) lost **₹28 lakh each** on average.
- **FY24 class split:** proprietary traders +₹33,000 cr, FPIs +₹28,000 cr (gross); **individuals −₹61,000 cr**. **96–97% of Pro/FPI profits came from algorithmic trading.**
- Costs: individuals spent ~₹26,000 each on F&O costs in FY24; ~₹50,000 cr over three years (51% brokerage, 20% exchange fees).
- Demographics: young (<30) traders 31%→43% (FY23→FY24); **72% from B30 cities**; **>75% declared income <₹5 lakh**; **>75% of loss-makers kept trading**.

**For our project.** This is the *authoritative welfare number* — the reason we DON'T re-estimate retail welfare from public aggregates (we'd lose the comparison). It's the demand-side backdrop for the whole thesis: this is who crowds into the speculative positions that push a stock's OI toward the 95% MWPL trigger. The wealth transfer (individuals → algo-driven Pro/FPI) is exactly the "noise traders subsidise sophisticated traders" story of DSSW, made concrete. Use it to frame the policy chapter and to motivate *why* SEBI is tightening the constraints we study.

## 13. Kumar (2009), "Who Gambles in the Stock Market?", *JF*

Canonical. Individuals' propensity to gamble correlates with their investing: retail investors **prefer lottery-type stocks** (low price, high idiosyncratic volatility, high idiosyncratic skewness). Lottery demand rises in downturns and with socioeconomic traits associated with lottery-buying (poorer, younger, less educated, certain regions/religions). Lottery stocks subsequently **underperform** (over-demand → lower future returns).

**For our project.** Defines the lottery-stock proxy (low-price, high-IVOL, high-skew) and the *type* of stock retail crowds into — plausibly the same names that hit MWPL bans. Bridges to H3 (wider bands in high-retail names) and to the constraint index (IVOL/skew as inputs). Foundational for the India lottery paper (#14) below.

## 14. Sehgal, Vasishth & Deisting (2024), "Lottery factor and stock returns: Evidence from India," *Borsa Istanbul Review*

Indian implementation of Kumar/Bali-et-al., Dec 2001–Mar 2021. Lottery characteristics = **MAX (max daily return), skewness, tail risk, idiosyncratic volatility**; builds a **lottery factor** and augments Fama-French 5-factor → a **6-factor behavioural model**. Finds MAX predicts returns beyond other risk measures; **lottery behaviour is mainly retail-driven** and tied to probability mis-weighting / overreaction to attention-grabbing events.

**For our project.** (a) Confirms the lottery/retail-overreaction channel operates in India — the demand-side counterpart to our supply-side (arbitrage-constraint) story. (b) Its factor toolkit (MAX, skew, tail risk, IVOL) overlaps our constraint-index inputs and Stambaugh's IVOL proxy. (c) Already-published for India → we **cite, not re-do** (crowdedness point from the feasibility memo). Use in the policy chapter to argue retail crowding + binding constraints jointly produce persistent mispricing.

## 15. Barber & Odean — 15a "Trading Is Hazardous to Your Wealth" (*JF* 2000); 15b "The Behavior of Individual Investors" (2013 handbook)

Canonical retail-underperformance evidence. 15a: 66,465 discount-brokerage households, 1991–96 — those who **trade most underperform most** (net ~11.4% vs market ~17.9% for the highest-turnover quintile); overconfidence → overtrading → costs destroy returns. 15b: survey of the field — retail investors **underperform, hold under-diversified portfolios, exhibit the disposition effect, chase attention-grabbing/past-return stocks, and are net noise**.

**For our project.** The behavioural micro-foundation for treating heavy retail activity as *noise* (DSSW/Tse's heterogeneous, less-informed traders). Supports the policy chapter's premise and the interpretation that reforms curbing retail speculation could, in principle, tighten bands — an empirical question our Ch 4 answers. Cite for framing; not Indian data.

---

## What Batch 4 gives the thesis
A complete demand-side narrative for the concluding chapter: Indian retail investors gamble on lottery-type stocks (Kumar; Sehgal et al.), overtrade and lose at scale (Barber-Odean; SEBI's ₹1.8-lakh-cr number), and their crowding is plausibly what drives single-stock OI to the 95% MWPL trigger in the first place. This closes the loop with Project-1's supply-side (limits-to-arbitrage) core: **retail crowding creates the mispricing pressure; binding arbitrage constraints prevent its correction.** And it justifies borrowing the retail-policy framing *without* needing the firm-level retail-trading data that killed Project 2.
