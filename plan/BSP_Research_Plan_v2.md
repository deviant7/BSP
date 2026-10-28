# BSP — Research Plan v2 (revised 28 Oct 2026)

*Builds on `BSP_Project_Document` (Sep 2026), whose goals stand. No calendar: phases are ordered by
logical dependency only. [verify] = must be checked against a primary source; see
`memory/07_fact_check.md` for the verification log.*

---

## 0. Scope: limits to arbitrage in Indian equities — the ban is one lens, not the project

The question is the project document's: **how strongly do limits to arbitrage bind in Indian
equities, what kinds of limits matter, and how much mispricing do they explain?** The literature
(Shleifer–Vishny; Gromb–Vayanos) groups limits into a few kinds, and India gives a dated,
observable shock to almost every one of them:

| Kind of limit | Indian instrument / shock | Main use in the thesis |
|---|---|---|
| **Short-sale constraints** | Naked overnight cash shorting barred; SLB thin; the only practical overnight short is via single-stock futures/options, which exist only for F&O stocks. **F&O inclusion/exclusion** creates/removes the channel permanently; the **F&O ban** removes it temporarily. | Ch 5 (ban), Ch 6 (F&O eligibility, cross-section) |
| **Trading costs** | STT/stamp-duty changes on dated budget days (e.g., futures STT cut 2013, raised Oct 2024 [verify]) | Ch 4 (bands) |
| **Arbitrage capital & funding** | Arbitrage mutual-fund AUM (AMFI monthly) incl. tax-driven inflows; money-market rate shocks (Aggarwal: MIBOR drives bands); margin-rule changes (peak margin 2020–21 [verify]) | Ch 4 (bands over time) |
| **Arbitrage risk** | Idiosyncratic / basis risk (IVOL) | Ch 3 (index), Ch 6 |
| **Position limits** | MWPL, entity limits, 2025 reforms | Ch 4, Ch 5 |

So the ban is the sharpest *causal* lens on one constraint, but the thesis measures and tests all
of them. One model covers them all (each is a parameter), so every chapter's hypothesis comes from
the same theory.

Order of work: **theory → pre-analysis plan → blind data build → validation → tests → interpretation.**

Status: Prof. Chaubal has seen only the project document. Models A/B and the progress report were not
sent and can be replaced. The next thing she sees: the corrected framework + a one-page note.

---

## 1. Theory: one model of constrained arbitrage in India

### 1.1 Core (from Model A, kept because it is correct)
A risk-averse arbitrageur (risk-bearing capacity 1/α, i.e., capital), basis risk σ², trading cost c,
extra short-side cost c_s, outside demand u, fringe −φm; clearing gives the asymmetric band
[−(c+c_s), c] and comparative statics (Model A Props 1–2). Each Indian constraint is a parameter:
- costs (STT, fees) → c; short-side cost → c_s (SSF available: finite; cash-only stock: effectively ∞
  for overnight positions);
- capital/funding → α (and the financing rate);
- arbitrage risk → σ²;
- position limits → a cap, and the ban → a *reduce-only* rule (§1.2).

### 1.2 The ban, modelled correctly (replaces A Prop 3)
In a ban every participant (futures and options on that stock) may only reduce positions (post
1 Oct 2025: reduce end-of-day FutEq delta). Typical OI: speculators long futures, arbitrageurs long
cash/short futures. Results to *derive* (they are conjectures until derived):
1. **One-sided correction** — rich futures (positive basis) no longer corrected (no new short futures);
   cheap futures still corrected by unwinding.
2. **Spillover to cash** — new speculative demand moves to the cash market; basis *level* can fall.
   Net level effect ambiguous, with sign conditions on observables.
3. **Anticipation** near 95% — band widens before the ban; bunching below 95%; small RD jump.
4. **Hysteresis** — entry 95%, exit 80% [verify].

### 1.3 Cash-only stocks (for the F&O-eligibility chapter)
A short Miller (1977)-style extension: with dispersed beliefs and binding short constraints, prices
reflect optimists; giving a stock a short channel (F&O entry) lowers overpricing and speeds incorporation
of bad news (Diamond–Verrecchia 1987) [verify refs]. Exit does the reverse.

### 1.4 Dynamics and estimation lens
Heterogeneous arbitrageurs (cost distribution) turn the sharp band into a transition zone and populate
the outer regimes, which is what makes 3-regime TVECM / ESTAR the right estimators. Model B's
band-of-inaction derivation (QVI sign fixed; "exact bridge" claim dropped) goes to an appendix as the
interpretation of the threshold.

### 1.5 Horizon
Data are daily → the arbitrageur is an *overnight carrier* (arbitrage fund / prop desk). Calibrate from a
bottom-up cost band (STT, stamp duty, fees, funding, margins), not from Aggarwal's 1-second 18 bp band.

### 1.6 Simulation
Simulate the model; run every planned estimator on simulated data (power, bias, how anticipation
affects the RD) before touching real outcomes.

### What is dropped from A/B
A Prop 3 (ban freezes only the arbitrageur; per-entity cap conflated with market-wide trigger), Prop 4's
asserted θ, Prop 5 (false proof), Prop 6 ("Cov(L,u)=0 by timing"); B's g(ω)→∞ assumption.

---

## 2. Hypotheses (derived, with the condition under which each would reverse)

| # | Hypothesis | Constraint |
|---|---|---|
| H1 | Mispricing size and persistence rise with ex-ante frictions (index built from frictions only). Association. | all |
| H2 | Earnings drift is larger where shorting is hard: in cash-only vs F&O stocks, and in a ban — **after bad news, not good news**. | short-sale |
| H3 | Band width rises with costs, illiquidity, volatility; estimated band ≈ cost-implied band; STT changes move the band by roughly the cost change. | costs |
| H4 | Bands widen when arbitrage capital is scarce (low/falling arbitrage-fund AUM, higher funding rates, tighter margins). | capital |
| H5 | Anomaly returns are larger where arbitrage is constrained (two-sided for IVOL: high-IVOL stocks outperform in India). | risk, short-sale |
| H6 | F&O inclusion lowers overpricing / drift / price delay; exclusion raises them. | short-sale |
| H7 | In a ban, correction becomes one-sided (positive-basis deviations persist). | short-sale / limits |
| H8 | In a ban, trading migrates to the cash market (cash volume, delivery %, spot volatility up; futures OI down). | limits (mechanism check) |
| H9 | The 1 Oct 2025 package has heterogeneous effects whose per-stock sign follows predicted Δutilisation; 3 Nov 2025 is a tightening. | limits |

Falsifiers written in advance: no asymmetry in H7; no futures-activity change in bans (H8); estimated
band far from any plausible cost (H3); no effect of F&O entry (H6).

---

## 3. Phases

**Phase 0 — Facts and feasibility.** Verify every rule, date and citation (see `memory/07_fact_check.md`).
Check data availability (no outcomes computed): archives of combined OI/MWPL, ban lists, F&O and cash
bhavcopies (with delivery), corporate actions, F&O eligibility lists over time, AMFI arbitrage-fund AUM,
NSE XBRL results (EPS), Prowess access via the library. Fix project-document and literature-review errors.

**Phase 1 — Theory + simulation** (§1). Deliverables: full model (LaTeX), 3-page guide version, one-page
result→hypothesis→test map.

**Phase 2 — Pre-analysis plan.** Samples, outcomes, treatments, specifications, expected signs + reversal
conditions, inference, primary vs secondary outcomes, falsifiers. Git-tagged. Guide signs off on 1 + 2.

**Phase 3 — Blind data build.** Panel 2015–2026 for all listed stocks (cash) and F&O stocks (futures,
options, OI, ban). While blind: data-quality reports, treatment-side descriptives, outcome distributions
alone; no outcome-by-treatment output. Pipeline validated by replicating Nandan et al. (2014) Nifty
futures basis.

**Phase 4 — Measurement (Ch 3).** **Phase 5 — Bands over time (Ch 4).** **Phase 6 — Ban (Ch 5).**
**Phase 7 — F&O eligibility and cross-section (Ch 6).** **Phase 8 — Policy, writing, replication package.**

---

## 4. Measurement (Ch 3; project doc Ch 1–2)

**Mispricing measures**
1. *Futures basis* (F&O stocks; primary): m = ln(F/F*), F* = (S − PV(div))·e^{r(T−t)}; r = MIBOR and
   T-bill as sensitivity; plus **relative implied repo** (stock's implied rate minus the day's
   cross-sectional median) to remove common-rate error. Drop final days before expiry.
2. *Earnings drift* (all stocks): surprise = earnings-announcement return (prices only); SUE (Harshita
   et al.) if EPS is obtainable. Drift = BHAR[+2,+64].
3. *Price efficiency* (all stocks): price delay (Hou–Moskowitz 2005) and variance ratios [verify refs].
4. *Put–call parity* — **optional robustness only** (thin, non-synchronous stock-option prices).

**Constraint index** (keeps the doc's stand-alone deliverable, minus circularity)
- Inputs: frictions only — bid–ask proxy/Amihud/impact cost, SLB availability, IVOL/basis risk,
  lagged MWPL headroom, F&O status. **Excluded:** basis dispersion (outcome), ban status (treatment).
- Crowding variables (delivery %, retail ownership, turnover) form a separate index.
- Weights: PCA (as in the doc) and model-implied weights. Validated against the estimated bands (Ch 4).

---

## 5. Bands over time — costs and capital (Ch 4; the non-linear time-series core)

- 3-regime TVECM (Ters–Urban; test β = 1) as workhorse; ESTAR (Tse) as robustness. Pooled/panel
  threshold models for sub-periods with few daily observations.
- **Costs (H3):** compare estimated θ+β0 with the bottom-up cost band; event windows around STT changes.
- **Capital (H4):** let thresholds/adjustment speeds depend on arbitrage-fund AUM, funding rates, and
  margin regimes (smooth-transition with an observed transition variable — Prof. Chaubal's area).
- **Reforms (H9):** 1 Oct 2025 package (heterogeneous intensity), 3 Nov 2025 tightening; the 2024
  index-only measures as placebos for single-stock bands.
- Cross-sectional variation in bands feeds H1 and the index validation.

## 6. The F&O ban (Ch 5)

1. Ban-entry event study vs near-miss controls (85–94.9% utilisation, matched on path); stacked DiD.
   Outcomes: H7 asymmetry, basis level, H8 spillover, H2 (bad-news drift in ban) if enough events.
2. RD at 95% with McCrary — supporting; anticipation predicted in advance.
3. Hysteresis design in [80, 95) — only if the 80% exit is confirmed.
4. Mechanical variation: quarterly MWPL recalculation dates (post Oct 2025); 1 Oct 2025 predicted
   Δutilisation (numerator: notional → FutEq, from pre-reform options share — use NSE's published FutEq
   if available, else reconstruct; denominator: 20% FF → min(15% FF, 65×ADDV), floor 10%). Pre-2025
   free-float changes only as robustness (often news-driven).

## 7. F&O eligibility and the cross-section (Ch 6)

- **F&O inclusion/exclusion as staggered events (H6, H2):** ~2,000 listed stocks; Callaway–Sant'Anna /
  Sun–Abraham DiD on drift, price delay, overpricing proxies; matched non-F&O controls. Eligibility is
  rule-based (market cap, turnover, MWPL criteria) [verify], which also allows an RD on the criteria.
- **SYY-style test (H5):** double sorts constraint × anomaly (VW), FM as complement; anomalies rebuilt from
  public data (momentum, reversal, MAX, IVOL, illiquidity, turnover; accounting ones only if EPS/XBRL works).
  The internship 45-signal library only if its use is cleared under the internship agreement.

## 8. Policy and conclusion (Ch 7)
Read results against SEBI's speculation-vs-market-quality trade-off: which limits matter most, how many
bans were "spurious" (denominator-driven) before vs after 1 Oct 2025, what F&O eligibility rules imply.
Retail-crowding framing from the SEBI loss study, kept short.

---

## 9. Safeguards against confirmation bias
PAP with reversal conditions and falsifiers (git-tagged); blind build; estimators tested on simulated data;
placebos (index-only reforms; fake ban dates; non-F&O stocks for ban effects); all pre-specified tests
reported, nulls included; "Expected results" replaced by "predictions and what would contradict them".

## 10. Trimmed from the project document / earlier plan, and why
- **Put–call parity as a core measure** → optional robustness (data quality; little beyond the basis).
- **Aggarwal-style per-stock-per-day TAR** → not feasible on daily data; 3-regime TVECM + ESTAR suffice.
- **Latent-factor version of the index** → PCA + model-implied weights are enough.
- **45-signal Fama–MacBeth as a chapter** → folded into a public-anomaly SYY test inside Ch 6.
- **Full pre-2025 FutEq reconstruction** → only if NSE did not publish FutEq before the reform.
- **Callaway–Sant'Anna for 2025 reforms** → not staggered (one date); continuous-intensity DiD instead.
- **OSF registration** → git tag suffices.
- **Pre-2025 free-float "instrument" as primary** → robustness only.

## 11. Thesis structure
1. Introduction and institutions. 2. Theory (+ simulation). 3. Data and measurement (mispricing,
constraint index). 4. Bands over time: costs, capital, reforms. 5. The F&O ban. 6. F&O eligibility and
the cross-section. 7. Policy and conclusion. Appendices: band-of-inaction derivation, PAP, data
construction, replication guide.

## 12. Next steps
1. Phase 0 verification (in progress: `memory/07_fact_check.md`) and data-availability checks.
2. Corrected model + simulation.
3. Send Prof. Chaubal the model (full + 3-page) and a one-page note on how it revises the plan.
