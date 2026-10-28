# BSP — Research Plan v2 (revised 28 Oct 2026)

*Earlier versions and everything cut or changed are kept in `plan/archive/` — see
`plan/archive/REMOVED_ITEMS_REGISTER.md` before reintroducing anything.*

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
| **Short-sale constraints** | Naked short selling barred; SEBI's framework makes only *F&O-segment securities* eligible for short selling and SLB; SLB thin; the practical overnight short is via single-stock futures/options, which exist only for F&O stocks. **F&O inclusion/exclusion** creates/removes the channel permanently; the **F&O ban** removes it temporarily. | Ch 5 (ban), Ch 6 (F&O eligibility, cross-section) |
| **Trading costs** | Futures STT (sell side): 0.017→0.01% on 1 Jun 2013; 0.0125→0.02% on 1 Oct 2024; 0.02→0.05% on 1 Apr 2026 (options also raised) | Ch 4 (bands) |
| **Arbitrage capital & funding** | Arbitrage mutual-fund AUM (AMFI monthly), incl. inflows after the 1 Apr 2023 debt-fund tax change (≈₹71k cr Apr 2023 → ≈₹1.99 lakh cr Oct 2024); money-market rate shocks (Aggarwal: MIBOR drives bands); peak-margin phase-in (25% Dec 2020 → 100% Sep 2021) | Ch 4 (bands over time) |
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
4. **Hysteresis** — entry 95%, exit 80% (confirmed: NSE Clearing circ. 119/2025). Rollovers are not
   allowed in a ban, so expiries inside a ban force OI down.

Facts the model must be able to reproduce (from Indian evidence): the band is centred *below* zero
(Shankar et al. 2015: κ_L ≈ −39 bp, κ_H ≈ −10 bp at 5-min frequency; median mispricing negative also in
Aggarwal 2015 and Nandan et al. 2014) — consistent with abundant cash-and-carry capacity and blocked reverse
arbitrage; and volatility widens the lower bound about twice as much as the upper. The early-exit (early
unwinding) option of Brennan–Schwartz (1990) should enter the ban analysis: in a ban, exit stays open while
entry closes.

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

**Phase 0 — Facts and feasibility.** Verify every rule, date and citation (done 28 Oct 2026, see
`memory/07_fact_check.md` incl. §I; papers #20–21 read, `references/notes_batch6_new_india_ssf_papers.md`).
Still to do: read Saurav–Srivastava–Agarwalla (2026, SSRN) and position H2/H7 against it; Gagnon (2018);
Brennan–Schwartz (1990, early-exit option — feeds the ban model); confirm intraday-shorting practice for
non-F&O stocks; check NSE archives for FutEq OI history (published daily before the reform) and monthly NPH
(free-float) files.
Check data availability (no outcomes computed): archives of combined OI/MWPL, ban lists, F&O and cash
bhavcopies (with delivery), corporate actions, F&O eligibility lists over time, AMFI arbitrage-fund AUM,
NSE XBRL results (EPS), Prowess access via the library. Fix project-document and literature-review errors.

**Phase 1 — Theory + simulation** (§1). Deliverables: full model (LaTeX), 3-page guide version, one-page
result→hypothesis→test map. *Status 28 Oct 2026:* full Model C drafted (`BSP_Model_C_Constrained_Arbitrage_India.pdf`,
source + numerical checks in `models_src/modelC/`), with the hypothesis map inside (§11). Pending: user review, 3-page guide
version, full estimator-on-simulated-data exercise (TVECM/RD/event study), and reading Brennan–Schwartz, Saurav et al., Gagnon.
New design point from the model: MWPL is not a valid excluded instrument for ban status (Prop. 9); measured basis must use
trade-based prices because NSE uses a theoretical settlement price on no-trade days (Prop. 7).

**Phase 2 — Pre-analysis plan.** *(v1 complete: `plan/pre_analysis_plan_v1.md`; tag `pap-v1` after user OK; v0 in archive.)* Samples, outcomes, treatments, specifications, expected signs + reversal
conditions, inference, primary vs secondary outcomes, falsifiers. Git-tagged. Guide signs off on 1 + 2.

**Phase 3 — Blind data build.** *(Started 28 Oct 2026: `data_pipeline/`, sources in its README.)* Panel 2015–2026 for all listed stocks (cash) and F&O stocks (futures,
options, OI, ban). While blind: data-quality reports, treatment-side descriptives, outcome distributions
alone; no outcome-by-treatment output. Pipeline validated by replicating Nandan et al. (2014) Nifty
futures basis. Known breaks to handle: physical settlement of stock derivatives (some stocks from Jul 2018;
all from the Oct 2019 expiry); T+1 (25 Feb 2022 → 27 Jan 2023); UDiFF files (old CM bhavcopy dropped
8 Jul 2024); COVID 2020; lot-size changes; eligibility revisions (2018; 30 Aug 2024); and the **closing
auction for F&O stocks from 3 Aug 2026** (spot close no longer a 30-min VWAP → measurement break in the
basis; futures daily settle = last half-hour weighted average price).

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
- **Robustness for thresholds:** model-free percentile bounds (as in Shankar et al. 2015) alongside TVECM/ESTAR.
- **Positioning:** Shankar et al. (2015/2019) estimate SETAR bands for ~100 NSE SSF on 5-min data, 2007–09, and relate
  them to liquidity and volatility; our contribution is daily, 2015–2026, the full set of dated shocks (costs, capital,
  limits, ban) and causal designs. Saurav–Srivastava–Agarwalla (2026) study the basis around earnings — Ch 5/6 must
  be positioned against it once read.
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
   Δutilisation (numerator: notional → FutEq, from pre-reform options share — NSE already published
   market-level FutEq OI daily before the reform (NSE Clearing FAQ, Oct 2025), so reconstruct only if the archive is short; denominator: 20% FF → min(15% FF, 65×ADDV in shares), floor 10%,
   quarterly windows per NSE Clearing SOP). Pre-2025 MWPL was 20% FF only (the old "30× volume" leg ended
   in 2006), so pre-2025 free-float changes are robustness only (often news-driven).
   *COVID MWPL halving (23 Mar–26 Nov 2020):* MWPL cut to 50% for stocks with ≥15% avg high–low range or
   ≥40% avg utilisation over 5 sessions — a rule-based, dated shock to the limit (criteria partly endogenous,
   so use near-threshold comparisons).

## 7. F&O eligibility and the cross-section (Ch 6)

- **F&O inclusion/exclusion as staggered events (H6, H2):** ~2,000 listed stocks; Callaway–Sant'Anna /
  Sun–Abraham DiD on drift, price delay, overpricing proxies; matched non-F&O controls. Eligibility is
  rule-based, which also allows an RD on the criteria: 2018 framework (top 500 by mcap and traded value;
  MQSOS ≥ ₹25 lakh; MWPL ≥ ₹500 cr; ADDV ≥ ₹10 cr) and SEBI circ. 2024/116 of 30 Aug 2024 (₹75 lakh;
  ₹1,500 cr; ₹35 cr; exit after 3 consecutive months failing). Quarterly entries/exits continue (e.g., 8 added
  1 Apr 2026, 6 added 28 Oct 2026). Precedent: Danielsen–Sorescu (2001), option introductions relax short
  constraints; Gagnon (2018), SSF listings on OneChicago lowered lending-market utilisation and fees. In India,
  F&O inclusion opens three channels at once (SSF/options, formal short-selling eligibility, SLB eligibility) —
  the design measures their joint effect.
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
