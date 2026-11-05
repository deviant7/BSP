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
| How NSE's `PREVCLOSE` handles splits/bonuses | Returns for H6, H5, EAR, BHAR | Check known splits before building returns |
| Market capitalisation for the cash universe | Size matching for H6 controls; size-matched BHAR | Find a free source (NSE market-cap files, XBRL shares outstanding, historic NPH files for F&O stocks) |
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
