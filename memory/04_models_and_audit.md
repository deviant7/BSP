# 04 — Models A & B, and the audit (28 Oct 2026)

## Model A — Constrained arbitrage (models_src/ModelA_constrained_arbitrage.tex, 8 pp)
Basis m=F−F*. Outside demand u, fringe −φm, CARA arbitrageur α, basis risk σ_m², costs c|q| + c_s max(−q,0), cap |q|≤L=κ·MWPL.
Clearing u−φm−q=0. Prop1 band [−(c+c_s), c]; m(u) piecewise linear (slope 1/φ inside, ασ²/(1+ασ²φ) outside). Calibration c≈3 bp, c_s≈12 bp
(from Aggarwal). Prop2 W=2c+c_s comparative statics. Prop3 KKT λ, threshold ū=φc+(1+ασ²φ)L; capped m=(u−L)/φ; ban freezes q → slope 1/φ, edge +∞.
Prop4 ΔM=−θ(m−C)+ε, θ=ψ/[ασ²(1+ασ²φ)], half-life ln2/−ln(1−θ). Prop5 signal return ↑ in W. Prop6 ∂m/∂L=−1/φ, exclusion "by timing".

## Model B — Band of inaction (models_src/ModelB_band_of_inaction.tex, 7 pp)
dz=σdW; fixed intervention cost K (+K_s short side), running cost θz², discount ρ; QVI; V=A+e^{ηz}+A−e^{−ηz}+(θ/ρ)z²+θσ²/ρ², η=√(2ρ)/σ;
value matching + smooth pasting; small-cost leading order **b=(6Kσ²/θ)^{1/4}** (re-derived: correct). Ban via K_j g(ω), g→∞ at ω→0.95.
Prop "bridge": inner random walk + outer mean reversion = 3-regime TAR/TVECM. Proportional-cost variant b∝(cσ²/θ)^{1/3} (Dumas 1992).

## Audit findings (to fix before finalising theory)
1. **Ban mis-modelled (A & B)**: ban freezes fresh FutEq OI for *everyone* (outside traders too), not only the arbitrageur; demand
   migrates to the cash market (and is frozen in options too). A also conflates per-entity cap (10/20/30% of MWPL) with the market-wide 95% trigger.
   A correct ban model may give an *ambiguous or opposite* sign (e.g., speculative longs move to spot → basis falls).
2. **A Prop5 proof false**: Pr(u>φc) and net exceedance m−c=ασ²(u−φc)/(1+ασ²φ) both *decrease* in c.
3. **A Prop4 θ is ad hoc** (ψ asserted, cap effect asserted).
4. **B**: QVI obstacle sign flipped (should be V(0)+K_j−V(z)); asymmetric edges = symmetric formula with side costs (approximation only;
   edges jointly pinned by common V(0)); g(ω)→∞ assumed (encodes the conclusion); "exact bridge" overstated — impulse control resets z to 0,
   so outer regimes ~never populated; singular control reflects at edge (also no outer obs). Needs monitoring frictions/heterogeneity.
   Running cost θz² borne by "the arbitrageur" lacks micro-foundation (arbitrageurs profit from gaps).
5. **Identification (A, B, project doc)**: "Cov(L,u)=0 by timing" invalid if demand is persistent; ADDV tracks attention/speculation and
   directly affects spot liquidity → band (exclusion problem). Pre-Oct-2025 MWPL = 20% FF only → little variation (weak first stage);
   usable variation mostly from 1 Oct 2025 onward (~1 year of data).
6. Models were built to satisfy a checklist equal to H1–H6 → risk of reverse-engineering (the very bias the guide wanted to avoid).

## Audit of other documents
- Project doc: "no genuine short selling" (fix); "Oct and Dec 2025 relaxations" (Nov 3 is a tightening; Dec changes are index options + pre-open);
  unverified "30× volume" and "80% exit"; constraint index includes basis dispersion = outcome (circularity); data gaps: EPS for SUE and
  accounting data for 45 signals are not in free NSE files (Prowess/Ace via library?).
- Lit review: SYY≠Fama–MacBeth; PEAD definitions wrong; Roy–Chakraborty direction wrong; Sehgal MAX(L5)/IVOL reversal omitted;
  DSSW idiosyncratic caveat; GV's Loewenstein–Willard caveat omitted.
- Reference index: Nandan journal, Ters–Urban venue/year, lottery-India journal wrong.
- Batch-5 notes attribute 80%/30× rules to NSE html that does not contain them.
