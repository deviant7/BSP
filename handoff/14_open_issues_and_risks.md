# 14. Open issues, questions and risks

## 14.1 Waiting on the user
1. (Done 5 Nov 2026) `pap-v1` tag created on GitHub by the user at 85dac3a.
2. Optionally fetch library papers: Saurav-Srivastava-Agarwalla 2026 (priority), Gagnon 2018, Brennan-Schwartz 1990.
3. Go-ahead needed before fixing the errors in the project document (short-selling line; 30x leg; "relaxations";
   timeline) and in the literature review.
4. Whether the internship 45-signal library may be used (default: no; public anomalies only).
5. Any news from the guide (answers to the five questions he planned to ask her in person).

## 14.2 Open technical questions
| Issue | Why it matters | Plan |
|---|---|---|
| NSE `PREVCLOSE` not adjusted (resolved) | Returns | Adjusted in build_returns.py (99.6% factor check) |
| Market capitalisation before Jul 2017 | Back-cast from later AMFI share counts (82% within 10% at 3 years) | Optional: verify with CMIE Prowess (user has college access) |
| April 2021 combineoi vs bhavcopy OI gap (2 to 3%) | Utilisation precision that month | combineoi is NSE's own ban input; documented; could compare with NSE's "Combined Delta Equivalent OI" report |
| Dividend over-correction | Dividend contracts are excluded; announcement-aware adjustment would bring them back | Optional robustness using announcement dates from corporate actions |
| BSE-only listings lack results | 86 stock-quarters (MCX, Abbott, Nestle pre-2023) | Optional: BSE API |
| `theoretical_settle` only marks no-trade days | Close-based basis secondary only | Fine; VWAP basis is main |
| Closing auction from 3 Aug 2026 | Break in close-based measures for the last months | Note in results; VWAP measure less affected |
| Post-Oct 2025 delta rule | Delta OI = -V may fail by design | Report post-reform descriptively |
| Possible intraday-short practice for non-F&O stocks | Framing of cash-only stocks' short constraint | Broker-dependent; keep "formally only F&O securities are eligible" |
| NSE 60% utilisation alert | Could create a second anticipation threshold | Unverified; check if relevant |

## 14.3 Research risks (stated honestly)
- **H3 power is low**: STT changes are 0.25 to 3 bp per side against bands of tens of bp; three dates; one confounded.
- **Post-reform ban analyses are low-powered** (44 spells); H2 in bans has 180 events.
- **Selection into bans**: bans happen when speculative interest is high; H7 compares within the same stock and conditions
  on lagged deviations; the level effect uses near-miss controls; RD is supporting only.
- **Inventory is unobserved**: OI is a proxy for arbitrage inventory (it also contains speculators' positions).
- **Competitor paper** (Saurav et al. 2026) may cover part of H2/H7; read before writing.
- **The "unstudied" claim** must be re-checked before it is written as fact.
- **Data revisions at NSE** may change counts on rebuild; build reports allow line-by-line comparison.

## 14.4 Things not to do
- Do not relate outcomes to treatments outside the frozen specification without logging a deviation.
- Do not modify the model to fit results.
- Do not rebuild or resend the guide's PDF without the user asking.
- Do not delete superseded files or plans.
- Do not put internal labels or history into guide-facing documents or `docs/`.
- Do not push to any branch other than the working branch; do not open a PR unasked.

## 14.5 Interpretation questions raised by the primary results (5 Nov 2026)
- H7 rejected with the opposite sign; post-hoc reading (blocked new demand at ban start). The level-effect test (7 Nov) shows
  the basis falls at ban start, more after faster OI build-up, but for both long and short build-up, so the reading is only
  partial (14.6 below).
- H6 delay effect could be liquidity/attention or growth selection rather than short-sale access; drift contradicts the
  short-sale channel. Possible exploratory checks (log in §11.2 first): placebo cohorts of stocks that met size criteria
  but were not added; split by pre-entry disagreement (turnover/volatility).
- H3: report pre-specified p with the placebo calibration side by side.

## Added 7 Nov 2026 (secondary tests)
- **VWAP vs close basis on ban days disagree** (level effect -6.3 vs -0.7; hysteresis +0.4 vs +3.2; RD both about -12). Possible
  causes: intraday timing mismatch between futures and cash trades on thin ban days; stale futures closes. Daily data cannot
  resolve it; report both. Intraday data (NSE data shop) would settle it.
- **Composition cannot sign new longs vs shorts**; build-up split (OI x price) shows the in-ban fall for both; the "blocked new
  long demand" reading of H7 is only partial.
- **RD basis gap precedes the ban** (crossing-day basis already low); the RD supports the trading mechanism, not a level effect.
- **SLB eligibility wording in the sent documents**: the progress report (sent) and the model PDF say only F&O stocks are
  eligible for short selling *and stock lending*. SLB has covered other liquid stocks since July 2013 (SEBI), visible in the
  SLB data from 2018. Short-selling eligibility is correctly F&O-only. Correct this in the next guide-facing document
  (model tex lines on the short-sale table, the cash-only section and the F&O-inclusion test) and rebuild the model PDF then.

## 14.6 Risks and caveats from the secondary tests (7 Nov 2026)
- Ten secondary statistics, unadjusted: one or two p < 0.05 are expected by chance (stated in docs/14 §14.16).
- Level effect: matching imbalance (treated 10 bp lower on day -1); same-day-control version weak; closing group 30 events.
- H1 persistence measure fails at daily frequency (noise); H1 is cross-sectional only (no within-stock effect).
- H4: ~100 months, return-chasing flows; results depend on specification (levels vs differences, pre/post 2023).
- H5: constraint groups differ hugely in size (median mcap 43,513 / 11,402 / 770 cr); equal-weighted effects are symmetric.
- H9 B: the 1 Oct 2025 reform coincides with the FutEq numerator change and intraday monitoring (3 Nov); only one quarter
  each side before the first reset.
- SLB activity seems to measure borrowing demand, not ease of borrowing (wrong sign in H1).
- **Measurement noise in daily VWAP basis** (band chapter, exploratory IV): OLS reversion slopes are inflated toward -1.
  Implication to check: H7's regime slopes (OLS) on ban days, where trading is thinner, could be affected; the H7
  liquid-days diagnostic argues against noise, but an IV version (x_(t-2) as instrument) of H7 is a worthwhile exploratory
  robustness check (log in §11.2 if run).
