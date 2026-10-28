# Register of items removed, demoted or changed across plan versions

Purpose: nothing is lost. Every item cut from an earlier plan is listed here with *why* and *how to bring it back*.
Versions (full texts in this folder):
- **v1** = `plan_v1_project_document_Sep2026.md` (the BSP Project Document, Sep 2026 — the guide has seen this)
- **v2.0** = `plan_v2.0_first_draft_2026-10-28.md` (ban-centred re-plan)
- **v2.1** = `plan_v2.1_broadened_2026-10-28.md` (broadened to all limits to arbitrage, with trims)
- **current** = `../BSP_Research_Plan_v2.md` (v2.1 + fact-check refinements, 28 Oct 2026)

Status: **Dropped** (not in current plan) · **Demoted** (kept as optional/robustness) · **Changed** (replaced by a variant) ·
**Removed-factual** (removed because it was wrong).

## A. Measurement
| Item (version) | Status | Why | To reintroduce |
|---|---|---|---|
| Basis dispersion/magnitude as an input to the constraint index (v1 §7.1) | Changed | It is the outcome → circular index | Can be shown in a separate "outcome-augmented" index for descriptive use only |
| Ban status & spell length as index inputs (v1 §7.1) | Changed | It is the treatment → circular | Same as above |
| Delivery %, ownership breadth as constraint inputs (v1 §7.1) | Changed | Model treats them as *demand/crowding*, not frictions → separate crowding index | Merge back if the model is changed to treat crowding as a friction |
| Latent-factor version of the index (v1, v2.0) | Dropped (v2.1) | PCA + model-implied weights judged enough | Add as robustness; cheap once panel exists |
| Put–call-parity deviation as one of three core mispricing measures (v1 §7.2) | Demoted (v2.0 secondary → v2.1 optional) | Thin, non-synchronous stock-option prices; adds little beyond basis | Put–call–*futures* parity on traded near-ATM strikes, if option data quality turns out good |
| PEAD with SUE from paid Ace Equity data (v1) | Changed | Free data plan; EPS not in NSE files | EAR surprise always; SUE if EPS from NSE XBRL / Prowess |
| India VIX as a dataset (v1 §8) | Dropped silently in v2 | Not needed by any test as written | Natural control/transition variable in Ch 4 (STAR with VIX) |
| Pre-2019 data as "placebo / pre-retail-era period" (v1 §8.1) | Dropped silently in v2 | Not tied to a hypothesis | Use as placebo period for retail-crowding interpretations in Ch 7 |
| Full reconstruction of FutEq OI pre-2025 from option deltas (v2.0) | Demoted (conditional) | Only needed if NSE did not publish FutEq before the reform | Reinstate if NSE files lack FutEq pre-Oct 2025 |

## B. Identification
| Item | Status | Why | To reintroduce |
|---|---|---|---|
| MWPL-denominator revisions as the *primary* instrument in both regimes (v1 §7.3) | Changed | Pre-2025 MWPL = 20% FF only, FF changes are news-driven; ADDV not excludable | Pre-2025 FF changes kept as robustness; post-2025 mechanical variation (recalc dates, 1 Oct 2025 intensity) used instead |
| "Lower of 20% FF or 30× prior-month volume" MWPL (v1 §7.3, §8.1) | Removed-factual | That rule is from 2004 and was replaced in 2006 (see `memory/07_fact_check.md`) | Only relevant if the sample is extended to 2004–06 |
| "Cov(L,u)=0 by timing" exclusion (Model A Prop 6) | Removed-factual | Invalid with persistent demand | — |
| Callaway–Sant'Anna / Sun–Abraham for the 2025 reforms (v1 §7.4) | Changed | Single date, not staggered → continuous-intensity DiD | Still used for staggered F&O inclusion/exclusion (Ch 6) |
| Callaway–Sant'Anna for repeated ban events (v2.0) | Changed (v2.1) | Stacked DiD is simpler for repeated short events | Swap back if stacked design has problems |
| OSF registration of the PAP (v2.0) | Dropped (v2.1) | Git tag gives a timestamp | Register on OSF if the guide wants an external record |

## C. Estimation (bands)
| Item | Status | Why | To reintroduce |
|---|---|---|---|
| Aggarwal-style 3-regime TAR per stock per day (v1 robustness) | Dropped (v2.1) | Needs intraday data; daily data give ~1 obs/day | Possible if intraday data (NSE data shop / tick) are obtained |
| Plain 3-regime TAR as robustness (v1, v2.0) | Dropped (v2.1) | TVECM + ESTAR judged sufficient | Cheap to add back as a third spec |
| Unknown cointegrating vector β (Ters–Urban default) | Changed | Theory pins β=1; test it instead of leaving it free | Free β as robustness |

## D. Cross-section
| Item | Status | Why | To reintroduce |
|---|---|---|---|
| Fama–MacBeth on the internship 45-signal library as its own chapter (v1 Ch 5) | Changed | IP/NDA risk; accounting data not free; SYY used sorts not FM | Re-add if the internship agreement allows and data exist |
| H5 one-sided (signals pay more in high-constraint stocks) (v1) | Changed | India IVOL premium is positive (Sehgal et al.) → stated two-sided | — |

## E. Hypotheses and framing
| Item | Status | Why | To reintroduce |
|---|---|---|---|
| H3 "band wider for … more retail-owned stocks" (v1) | Changed | Current H3 is costs/illiquidity/volatility; retail ownership moved to crowding index | Add "retail-ownership" interaction to H3 or H1 as a secondary test |
| H4 "Oct & Dec 2025 *relaxations* narrow the band" (v1) | Removed-factual / Changed | 3 Nov 2025 is a tightening; package has heterogeneous effects → now H9 | — |
| H6 v1 (mispricing responds to denominator-induced ban) | Changed | Folded into the ban chapter's designs (v2.1 has no separate H for it) | Restore as an explicit hypothesis in the PAP |
| v2.0 H4 (2025 package + Oct 2024 STT) | Split in v2.1 | STT → H3 (costs); 2025 package → H9 | — |
| "Expected results" section (v1 §9) | Changed | All confirmatory → replaced by predictions + falsifiers | — |
| "Position limits studied in Korea and Taiwan" (v1 §6) | Removed-factual | No supporting study found | Only with a real citation |
| "No genuine short selling in the cash market" (v1 §1) | Removed-factual | Intraday shorting allowed; naked short selling barred | — |
| Ban-centred scope (v2.0) | Changed (v2.1) | User: project is limits to arbitrage broadly | — |

## F. Process
| Item | Status | Why | To reintroduce |
|---|---|---|---|
| Stage I/II week-by-week timeline (v1 §12) | Dropped | User: ignore timelines entirely | Rebuild if a deadline is imposed |
| Models A & B as two competing candidates | Changed | Replaced by one corrected model (A's static core; B as appendix) | Full A/B sources remain in `models_src/` |

## Changelog of the current plan (additions; nothing removed)
- 28 Oct 2026 (after fact-check pass 2): added short-selling eligibility (F&O securities only) to §0; Indian stylised facts the
  model must reproduce (band centred below zero; asymmetric volatility effect) and Brennan–Schwartz early-exit option to §1;
  model-free percentile bounds as threshold robustness and positioning vs Shankar et al. (2015/2019) and Saurav et al. (2026) to §5;
  Gagnon (2018) precedent and "three channels opened by F&O inclusion" to §7; FutEq OI already published pre-reform (§6.4);
  Phase 0 to-do list updated.
- 28 Oct 2026 (data start): pre-sample 2010–2014 MWPL/ban data downloaded for robustness/power (addition, not in v1/v2);
  primary basis measure defined on daily VWAPs (futures vs cash) instead of settlement/close prices, because NSE uses a theoretical
  settlement price on no-trade days (close/settlement basis kept as secondary).
