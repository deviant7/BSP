# Pre-analysis plan — DRAFT v0 (28 Oct 2026; internal)

Status: drafted while the data are being built. **No outcome has been related to any treatment.** The final version will
be git-tagged (`pap-v1`) before any such analysis; every later deviation is logged in §10 with its reason.
Numbers marked [TBD] are filled from treatment-side descriptives (allowed while blind).

## 1. Samples
- **Main:** NSE single-stock F&O universe, 1 Jan 2015 – 27 Oct 2026, with time-varying membership (from combineoi files).
  Pre-sample 2010–2014 available for robustness only.
- **Cash universe (Ch 6):** all NSE EQ-series stocks, same period.
- **Contract choice:** near-month future; switch to next month when ≤ 3 trading days remain (expiry-week effects).
- **Exclusions (fixed now):** stock-days with < 5 futures trades or zero futures volume (no trade-based price); ex-dividend
  and corporate-action windows (ex-date −1 to +1) unless dividends are explicitly adjusted; first 20 trading days after F&O
  entry; last 3 trading days before expiry (main spec).

## 2. Outcomes (definitions fixed)
- **O1 basis (primary):** m_it = ln F̄_it − ln S̄_it − (r_t − q_it)·τ_it, with F̄ = futures daily VWAP (traded value /
  traded quantity), S̄ = cash daily VWAP, r = 91-day T-bill (main) / MIBOR (robustness), q from known dividends,
  τ = calendar days to expiry / 365. Secondary: close/settlement-based basis with NSE theoretical-settlement days flagged.
- **O2 relative implied repo:** implied rate from F̄/S̄ minus the cross-sectional median that day.
- **O3 reversion:** daily Δm_it on m_{i,t−1}, by regime (above/below thresholds).
- **O4 trading:** futures volume, ΔOI, ΔOI + volume (identity check), cash volume, delivery %.
- **O5 drift:** BHAR[+2,+64] after results announcements; surprise = earnings-announcement return [−1,+1].
- **O6 efficiency (cash universe):** Hou–Moskowitz price delay (weekly), variance ratio VR(5).

## 3. Treatments
- **Ban:** official securities-in-ban list (fo_secban); utilisation ω = OI/MWPL (gross OI before 1 Oct 2025; FutEq after).
- **MWPL shocks:** 1 Oct 2025 formula (predicted Δln ω from pre-reform free float, ADDV and options share of OI);
  quarterly recalculations after 1 Oct 2025; COVID halving 23 Mar – 26 Nov 2020.
- **Cost shocks:** futures STT 1 Apr 2023, 1 Oct 2024, 1 Apr 2026.
- **Capital:** monthly arbitrage-fund AUM and flows (AMFI, from mid-2018); 1 Apr 2023 debt-fund tax change (confounded with
  the STT change on the same day — both reported, neither claimed separately unless identified by cross-section).
- **Short channel:** F&O inclusion/exclusion dates (2015–2026), incl. the 2018 and 30 Aug 2024 criteria revisions.

## 4. Primary hypotheses, specifications, signs and reversal conditions
| H | Spec | Prediction (sign) | Reverses / fails if |
|---|---|---|---|
| H7 (primary) | Δm_it = Σ_r [β_r + δ_r·Ban_it]·m_{i,t−1}·1{regime r} + α_i + λ_t + e; regimes: m above upper threshold, below lower threshold (thresholds from pre-period TVECM per stock group) | δ_up > 0 (upper reversion weakens); δ_down ≤ 0 while inventory proxy high; δ_down → 0 after an in-ban expiry | δ_up ≤ 0, or δ_up = δ_down |
| H8 (mechanism) | Ban-day regressions of ΔOI + volume (futures, contracts) and futures volume | ΔOI + V ≈ 0 before 1 Oct 2025; volume ↓; cash volume/delivery ↑ | ΔOI + V ≠ 0 systematically; no activity change |
| H3 (primary) | Event windows ±20 days around STT dates; threshold/edge estimates and \|m\| | upper edge ↑ by ≈ ΔSTT (+ physical-delivery effect) | no shift, or shift unrelated to size of cost change |
| H6 (primary) | Staggered DiD (Callaway–Sant'Anna) of F&O inclusion on O5, O6; matched non-F&O controls; RD on eligibility criteria where usable | delay ↓, bad-news drift ↓ after inclusion; reverse at exclusion | no change or opposite |
| H9 | DiD with continuous predicted Δln ω (1 Oct 2025); ω-binned event study pre-ban | upper edge rises smoothly with ω before 95%; reform effects follow predicted Δω | jump only at 95%; no ω gradient |
| Level (Prop. 6) | Ban-entry stacked event study, split by order-flow composition (ΔOI/volume pre-ban as closing-vs-new proxy) | sign follows composition | sign unrelated to composition |

Secondary: H1 (friction index ↔ band), H2 (bad-news drift in bans; pre-EA basis vanishes in bans), H4 (AUM flows ↔ upper
edge), H5 (anomaly asymmetry).

## 5. Designs (detail)
- **Ban-entry event study:** stacked; treated = first ban day; controls = stock-days with ω ∈ [0.85, 0.95) in the same week
  that do not enter, matched on ω path (5 days) and basis level; window −20…+20.
- **RD:** running variable ω on day t−1, cutoff 0.95, local linear, MSE-optimal bandwidth, McCrary/Cattaneo–Jansson–Ma
  density test reported first; anticipation means the RD is *supporting* only.
- **Hysteresis:** ω ∈ [0.80, 0.95): in-ban vs not-in-ban, controlling for ω, Δω, lagged m (5 lags).
- **Reform intensity:** stock FE + date FE; predicted Δln ω from data up to 15 Sep 2025 only.

## 6. Inference and multiple testing
Two-way clustered SEs (stock, date); wild-cluster bootstrap where events are few. Primary family {H7, H3, H6, H8}:
Holm correction; secondary hypotheses reported unadjusted and labelled exploratory.

## 7. Power (to fill from descriptives)
Ban spells 2015–2026: 1,789 (1,745 before Oct 2025; 44 after); ban stock-days 9,414; stocks ever banned: 141;
not-in-ban stock-days with utilisation in (0.90, 0.95]: 2,441 pre-reform, 139 post; F&O inclusions/exclusions: [TBD].
Post-reform ban events are few (44 spells) → reform-period ban analyses are low-powered; state this in advance.

## 8. Falsifiers (from the model)
No upper/lower asymmetry in bans; no change in futures activity during bans; band unrelated to dated cost shocks; F&O inclusion
without effect on delay/drift.

## 8b. Data decisions from the build (28 Oct 2026)
- Main sample excludes stock-days with a dividend or other corporate event (bonus, split, rights, debentures, demerger, scheme,
  buyback) going ex in the contract life (flags `pv>0`, `event_in_life`); robustness adds dividend days with an
  announcement-date-aware adjustment.
- Outliers (|m| > 200 bp, 0.65% of clean days) are kept; main estimates use winsorisation at 1/99% within year, robustness without.
- Rate: monthly 3-month interbank (OECD); relative implied repo removes common rate error.

## 9. Data gaps to resolve before tagging
Dividend/corporate-action source for q; MIBOR vs T-bill series (RBI DBIE); results-announcement dates; free-float history
(monthly NPH files, discontinued Oct 2025); F&O inclusion/exclusion list; AMFI monthly arbitrage AUM.

## 10. Deviations log
(empty)
