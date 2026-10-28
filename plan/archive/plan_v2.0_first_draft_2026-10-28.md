# BSP — Research Plan v2 (how to take the project forward)

*Drafted 28 Oct 2026. Builds on `BSP_Project_Document` (Sep 2026), which stays the statement of goals.
No calendar: phases are ordered by logical dependency only. Items marked [verify] must be checked
against an NSE/SEBI primary source before anything rests on them.*

---

## 0. The guiding idea

The project document's goals are good and stay: (1) a reproducible measure of how tightly arbitrage
constraints bind, (2) mispricing measures, (3) a causal estimate of the ban's effect, (4) the
no-arbitrage band and how the 2025 reforms moved it, (5) the cross-sectional asset-pricing test,
(6) a policy reading. What changes is the *order of reasoning* and the *discipline*:

> **theory → written predictions → blind data build → validation → tests → interpretation.**

Each chapter keeps its goal, but its hypothesis is now derived from one model, written down with its
sign *conditions* before outcomes are looked at, and tested with a design that can return a
surprise. The guide's request (theory first, against confirmation bias) is met by the model *plus*
the pre-analysis plan — the second is what actually ties our hands.

Status note: Prof. Chaubal has seen only the project document. Models A/B and the progress report
were never sent, so they can be replaced freely. The next thing she sees should be the corrected
theoretical framework (Phase 1) with a short note on how it revises the plan.

---

## 1. What the theory has to get right (and why A/B must be replaced, not polished)

### 1.1 The ban, described correctly
- Trigger: market-wide OI > 95% of MWPL (end of day; intraday checks from 3 Nov 2025).
  Exit: OI < 80% [verify]. In ban, **every participant** may only trade to *reduce* their position
  (post 1 Oct 2025: reduce end-of-day FutEq delta). This applies to futures *and* options on the stock.
- Consequence: in a ban, a trade can occur only between a closing long and a closing short, so OI can
  only fall. Rolling over into the next expiry is, in effect, a fresh position [verify how NSE treats rollovers].
- Who holds the OI? Every futures contract has a long and a short. In India the typical
  configuration in crowded stocks is: leveraged speculators long futures; cash-and-carry arbitrageurs
  (arbitrage mutual funds, prop desks) **long cash / short futures**. Reverse arbitrage (short cash /
  long futures) is rare because naked overnight cash shorting is barred and SLB is thin.

### 1.2 The mechanism the model should formalise (a hypothesis to be derived, not assumed)
1. **One-sided arbitrage in a ban.** Arbitrageurs cannot open new short-futures/long-cash positions,
   so a *rich* futures price (positive basis) is no longer corrected. They *can* unwind existing
   positions (buy back futures, sell cash), which corrects a *cheap* futures price (negative basis).
   ⇒ In a ban the upper band edge opens while the lower edge survives (or tightens): the effect on
   persistence is **asymmetric**, and its direction is set by the sign of pre-ban arbitrage inventory.
2. **Spillover to spot.** New speculative demand that cannot enter futures moves to the cash market
   (delivery or margin-funded), pushing spot relative to futures ⇒ a level effect on the basis that
   can be **negative**.
3. **Net effect on the basis level is ambiguous** (1 pushes up the upper tail, 2 pushes the mean down);
   the sign depends on observables: pre-ban basis sign, inventory proxy, how much demand migrates.
4. **Anticipation.** As utilisation approaches 95%, arbitrageurs who fear being locked in widen the
   price they need to open new positions ⇒ the band starts widening *before* the ban, and agents may
   avoid crossing (bunching below 95%). This predicts a *smaller* jump at 95% than a naive model —
   an honest prediction for the RD.
5. **Hysteresis.** With entry at 95% and exit at 80% [verify], two stocks at the same utilisation can be
   in different states, depending on their path.

This is a genuine result if it holds: a "reduce-only" rule converts two-sided arbitrage into
one-sided arbitrage. Nothing in the 21 papers derives it.

### 1.3 What A and B contribute
- **Keep from A:** the static environment (CARA arbitrageur, fringe −φm, asymmetric costs c, c_s,
  clearing) and Prop 1 (asymmetric band) and Prop 2 (comparative statics). These are correct.
- **Replace in A:** Prop 3 (ban freezes only the arbitrageur; conflates the per-entity cap with the
  market-wide trigger), Prop 4 (θ asserted, not derived), Prop 5 (proof false), Prop 6 ("Cov(L,u)=0 by
  timing" invalid with persistent demand; ADDV not excludable).
- **Keep from B, demoted to the econometrics appendix:** the band-of-inaction logic as the *reading* of a
  threshold model. Fix the QVI sign (obstacle is V(0)+K_j−V(z)); state that with pure impulse control the
  outer regimes are empty, so the TAR/TVECM mapping needs heterogeneous arbitrageurs or monitoring
  frictions (which is also what motivates STAR). Drop g(ω)→∞ as an assumption.

### 1.4 Horizon and calibration
Our data are daily. Daily settlement prices of futures and the cash closing price are both last-30-minute
VWAPs [verify for each period], so the daily basis measures the *persistent* component that survives
intraday HFT arbitrage. The model's arbitrageur is therefore an overnight carrier (arbitrage fund / prop
desk) facing STT, stamp duty, exchange fees, funding spread, margins — not Aggarwal's 1-second trader.
Calibration should start from a **cost-implied band** built bottom-up (Slivka-style, ~2.5% in 2009 terms),
not from Aggarwal's 18 bp.

---

## 2. Revised hypotheses (derived, with sign conditions)

Each keeps the project document's number where possible; "⇐" gives the model result it rests on.

| # | Hypothesis (revised) | Changes vs project doc |
|---|---|---|
| H1 | Mispricing magnitude and persistence rise with *ex-ante friction* (costs, basis risk, capacity, short-side cost). ⇐ static band + comparative statics | Index now excludes outcomes and the ban (see §4.3); association, not causal |
| H2 | Earnings drift is larger where the short channel is constrained; **in a ban, drift after bad news rises, after good news not** (only futures give overnight short exposure; long side can still buy cash). | Sign made asymmetric; conditional on EPS/surprise data |
| H3 | Band width rises with cost/illiquidity/volatility; the estimated band is close to the cost-implied band. ⇐ band formula | Adds a non-circular validation (estimated vs cost-implied) |
| H4 | The 1 Oct 2025 package (lower MWPL denominator, FutEq numerator, delta-reduction rule) has **heterogeneous** effects whose sign per stock follows from predicted Δutilisation; the 3 Nov 2025 intraday monitoring is a *tightening*; the Oct 2024 STT increase on F&O [verify] is a cost shock that widens bands. | "Relaxations" framing dropped; no assumed sign for the package |
| H5 | Anomaly returns are larger where arbitrage is constrained. Stated two-sided for IVOL because in India high-IVOL stocks outperform (Sehgal et al. 2024). | Two-sided; signal set rebuilt from public data |
| H6 | Ban effects survive when ban status is driven by mechanical variation (recalculation dates, reform intensity, hysteresis), not only by crowding. | Instrument redesigned (§5) |
| H7 *(new)* | In a ban, correction becomes one-sided: positive-basis deviations persist, negative-basis deviations still revert (given short-futures arbitrage inventory). | The model's sharpest, most falsifiable prediction |
| H8 *(new)* | In a ban, trading migrates to the cash market: cash volume, delivery %, and spot volatility move; futures volume and OI fall. | Mechanism check; outcomes not used in H1–H7 |

What would *falsify* the model: no asymmetry in H7; bans with no change in futures activity (H8); the
estimated band far from any plausible cost (H3).

---

## 3. Phase plan (ordered by dependency, no dates)

### Phase 0 — Facts and housekeeping
1. Verify from NSE/SEBI circulars: 80% ban exit; history of the MWPL formula before 2025 (was there a
   "30× average daily volume" leg, and until when?); rollover treatment during a ban; physical settlement
   of stock derivatives (phased from 2018) [verify]; closing/settlement-price methodology by period;
   STT/stamp duty history (incl. 1 Oct 2024 F&O STT rise) [verify]; F&O eligibility criteria changes
   (2018 revision, 2024 revision) [verify]; T+1 cash settlement transition (2023).
2. Data-availability check (no outcomes computed): archive depth for combined-OI/MWPL files, ban lists,
   F&O bhavcopy (options too), cash bhavcopy with delivery, corporate actions (dividends, splits), SLB
   bhavcopy, NSE XBRL financial results (free EPS?), Prowess/CMIE access via IITB library.
3. Fix the project document's errors (short-selling line; "relaxations"; unverified rules) and the
   literature review / notes errors listed in `memory/04_models_and_audit.md`.

### Phase 1 — Theory (one model, "the ban as a reduce-only market-wide freeze")
- Environment from A (§1.3) + inventory state + outside futures speculators whose futures demand is also
  frozen in a ban + cash-market spillover share s + anticipation via probability of entering a ban.
- Results to derive: (i) normal-times band; (ii) ban band — one-sided, with conditions; (iii) basis
  level under ban — sign conditions; (iv) pre-ban widening and bunching; (v) MWPL change → ban
  probability → basis (what an instrument would and would not identify, with the exclusion problem
  stated); (vi) PEAD asymmetry; (vii) heterogeneous arbitrageurs → smooth transition (STAR) and
  populated outer regimes (TVECM).
- **Simulation:** simulate the model, then run every planned estimator (event study, RD, TVECM) on
  simulated data. This checks that the estimators recover the effects, shows how anticipation biases the
  RD, and gives power calculations — all before seeing real outcomes.
- Deliverables: full model (LaTeX, ~10–15 pp) + 3-page plain-language version for the guide + a one-page
  note mapping each result to a hypothesis and test.

### Phase 2 — Pre-analysis plan (PAP)
- Fix: sample filters; outcome definitions (§4.2); treatment definitions; each specification; expected
  sign *and the condition under which it reverses*; inference (clustering, bootstrap); multiple-testing
  treatment (primary vs secondary outcomes); what counts as a falsification.
- Timestamp it with a git tag (optionally OSF). Deviations later are allowed but must be reported.
- Guide signs off on Phase 1 + Phase 2 before outcome analysis.

### Phase 3 — Data pipeline (blind to outcome–treatment relationships)
- Build the stock-day panel 2015–2026 (and the event files). Allowed while blind: data-quality reports,
  treatment-side descriptives (number/length of bans, utilisation paths, MWPL changes at 1 Oct 2025 and
  at each quarterly recalculation), outcome *distributions* on their own. Not allowed: any table/plot of
  outcomes by treatment.
- **Pipeline validation on a non-test object:** compute the Nifty index futures basis and replicate
  Nandan et al. (2014) (mean −₹8.19, 71% negative days, 2003–12). If our code matches, the stock-level
  basis code is trusted.
- Reconstruct FutEq (delta-based) OI pre-2025 from option settle prices (Black-76 on the futures price)
  and check it against NSE's published FutEq after the change.

### Phase 4 — Measurement chapter (project doc Ch 1 + Ch 2)
See §4. Validation of the index is done against the band estimates from Phase 5 and against the
cost-implied band — both computed independently.

### Phase 5 — Causal and dynamic chapters (project doc Ch 3 + Ch 4)
See §5 and §6.

### Phase 6 — Cross-section (project doc Ch 5)
See §7.

### Phase 7 — Policy chapter, writing, replication package
- Policy: read the estimates against SEBI's speculation-control vs market-quality trade-off; quantify
  "spurious" bans (bans driven by the denominator, not by crowding) before vs after 1 Oct 2025.
- Replication package: code + derived measures. Check NSE terms before redistributing raw files.

---

## 4. Measurement (Chapters on data, mispricing, constraint index)

### 4.1 Panel
Stock-day, F&O universe with time-varying membership (~180–220 stocks), 2015–2026; near-month and
next-month futures; options near the money; ban status, utilisation, MWPL; cash OHLC, volume,
delivery; corporate actions; shareholding (quarterly, forward-filled). Known breaks to handle:
physical settlement, T+1, UDiFF format (2024), COVID 2020, lot-size changes, eligibility revisions.

### 4.2 Mispricing measures
1. **Futures basis (primary).** m = ln(F/F*), F* = (S − PV(dividends within life))·e^{r(T−t)}; r =
   MIBOR/T-bill (sensitivity to both). Also the **relative implied repo**: each stock's implied financing
   rate minus the cross-sectional median that day, which removes errors in r common to all stocks. Exclude
   the last few days before expiry; also report the next-month contract.
2. **Put–call–futures parity (secondary).** C − P = e^{−r(T−t)}(F − K) for near-ATM, actually traded
   strikes. Stock options are European [verify date], and using F instead of S removes dividends and the
   stock-shorting leg, so it isolates the options–futures link. Restrict to volume-filtered strikes;
   non-synchronous closing prices are the main risk.
3. **Earnings drift (conditional on data).** Surprise = SUE (seasonal random walk, Harshita et al.:
   (EPS_q − EPS_{q−4})/price) if EPS is available (NSE XBRL results or Prowess), and in any case the
   **earnings-announcement return (EAR)** surprise, which needs only prices. Drift = BHAR[+2,+64].
4. **Cash-market efficiency (for §7):** variance ratios, price delay (Hou–Moskowitz), which exist for
   non-F&O stocks too.

### 4.3 Constraint index (keeps the project doc goal, removes circularity)
- Build it **only from ex-ante friction inputs** that the model says set the band: trading cost
  (bid–ask proxy, Amihud, NSE impact cost if available), short-side cost (SLB availability/fee), basis
  risk / IVOL, capacity (headroom 1 − OI/MWPL, lagged), funding (rate spread).
- **Exclude** basis dispersion (an outcome) and ban status (the treatment). Report demand-pressure
  variables (delivery %, retail ownership share, turnover) as a *separate* crowding index — the model
  treats demand u and frictions as different objects.
- Weights: (a) PCA, as in the project doc; (b) a model-implied index (weights from the band formula);
  (c) robustness with a latent-factor model. Validation: does the index predict out-of-sample the
  band width estimated in §6 and the cost-implied band? This makes Chapter 1 the stand-alone,
  citable deliverable the project document wanted — now with a non-circular validation.

---

## 5. Causal effects of the ban (project doc Ch 3), several designs, none relied on alone

1. **Ban-entry event study with near-miss controls.** Treated: stock-days entering a ban. Controls:
   stocks whose utilisation reached, say, 85–94.9% in the same window without crossing, matched on the
   utilisation path and on the basis before the event. Stacked DiD / Callaway–Sant'Anna for repeated
   events. Outcomes: H7 (asymmetric reversion), basis level, H8 (spot spillover).
2. **RD at 95%** with McCrary. Supporting only; the model predicts anticipation and bunching, so a small
   jump is not evidence against the mechanism — this is written in the PAP in advance.
3. **Hysteresis design** (if 80% exit is confirmed). Among stock-days with utilisation in [80, 95), compare
   in-ban vs not-in-ban, conditional on the current level and trend of utilisation.
4. **Mechanical denominator variation.**
   - *Quarterly MWPL recalculation dates (post Oct 2025):* MWPL changes discretely on a known date while
     OI is continuous ⇒ a jump in utilisation, and hence in ban probability. Compare stocks whose MWPL
     fell vs rose around each recalculation.
   - *1 Oct 2025 formula change as continuous treatment:* for each stock, predicted Δln(utilisation) =
     Δln(OI measure: notional → FutEq, from the pre-reform options share) − Δln(MWPL: 20% FF →
     min(15% FF, 65×ADDV), floor 10% FF), all from pre-reform data. Use it as treatment intensity
     (DiD with stock and date fixed effects) and as an instrument for ban days.
   - *Pre-2025:* free-float changes are often news (OFS, QIPs, promoter sales), so they are a weak and
     possibly invalid instrument; use only as robustness, and only if the volume leg (if any) adds
     variation.
   - The exclusion restriction is argued, not assumed: ADDV can affect spot liquidity directly, so
     specifications control for ADDV/turnover levels and use the *formula-induced* part of the change.

---

## 6. Bands and reforms (project doc Ch 4) — the non-linear time-series core

- **Per-stock and pooled threshold models.** Ters–Urban 3-regime TVECM as the workhorse (test β = 1
  rather than leaving β fully free, since theory pins it), Aggarwal-style 3-regime TAR and Tse-style
  ESTAR as robustness. With ~2,700 daily observations per stock over the full sample but only ~250 after
  Oct 2025, pre/post comparisons use pooled/panel threshold models (stock fixed effects, common
  thresholds scaled by stock cost) or groups of similar stocks.
- **Ban-dependent regimes (direct test of H7):** a threshold model whose upper/lower adjustment speeds
  are allowed to differ in ban vs non-ban states — observed regime (ban) × unobserved regime (threshold).
- **Estimated vs cost-implied band (H3):** Ters–Urban's precisely estimated θ + β0 is directly comparable
  to the bottom-up cost band.
- **Reforms:** 1 Oct 2024 STT change (cost shock, common), 1 Oct 2025 package (heterogeneous intensity,
  §5.4), 3 Nov 2025 intraday monitoring (tightening), 6 Dec 2025 pre-open session. The 2024 index-only
  measures are placebos for single-stock bands (they should not move them, except through spillover).

---

## 7. Cross-section (project doc Ch 5), made more powerful

- **SYY-style test, done as SYY did it:** double sorts (constraint × anomaly) with value-weighted
  portfolios, plus Fama–MacBeth as a complement. Anomalies rebuilt from public data (momentum,
  short-term reversal, MAX, IVOL, illiquidity, turnover, delivery-based, and accounting anomalies if
  XBRL/Prowess works). Do not rely on the internship's 45-signal library unless its use is cleared under
  the internship agreement.
- **Power fix — F&O eligibility events.** Inclusion in the F&O segment *creates* an overnight short channel
  (single-stock futures); exclusion removes it. Inclusions/exclusions happen in batches over 2015–2026
  (including large eligibility revisions [verify]), across a universe of ~2,000 listed stocks. Staggered
  DiD (Callaway–Sant'Anna / Sun–Abraham) on anomaly returns, PEAD and price delay around these events is
  a direct "limits to arbitrage in Indian equities" test with far more power than 220 stocks. It also
  connects the ban (a temporary loss of the channel) to entry/exit (a permanent gain/loss).

---

## 8. Safeguards against confirmation bias (in addition to theory)

1. PAP with sign *conditions* and falsification criteria (Phase 2), git-tagged.
2. Blind pipeline: no outcome-by-treatment output until the PAP is tagged.
3. Simulated-data runs of every estimator (Phase 1) — power and bias known in advance.
4. Placebos: index-only reforms for single-stock bands; fake ban dates; non-F&O stocks for ban effects.
5. Primary vs secondary outcomes fixed in advance; report all pre-specified tests, including nulls.
6. "Expected results" section replaced by "predictions and what would contradict them".

---

## 9. Proposed thesis structure

1. Introduction and institutions (short selling, SLB, F&O, MWPL, ban, 2024–26 reforms).
2. Theory: the ban as a reduce-only freeze (model + simulations).
3. Data and measurement: panel, mispricing measures, constraint index and its validation (Ch 1–2 of the doc).
4. Causal effects of the ban (Ch 3 of the doc).
5. Bands and regime shifts (Ch 4 of the doc).
6. Cross-section and F&O eligibility (Ch 5 of the doc).
7. Policy and conclusion (Ch 6 of the doc).
Appendices: band-of-inaction derivation (fixed Model B), PAP, data construction, replication guide.

---

## 10. Immediate next steps
1. Phase 0 fact checks (rules and data availability) — no outcome computed.
2. Write the corrected model (Phase 1) and simulate it.
3. Send Prof. Chaubal: the model (3-pp version + full), a one-page note on how it revises the plan, and
   ask for her view on the PAP idea and on building the data pipeline blind in parallel.
