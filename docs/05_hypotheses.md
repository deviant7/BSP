# 5. Hypotheses and falsifiers

Every hypothesis below is derived from the model in [04_theoretical_framework.md](04_theoretical_framework.md). Each comes
with the result that would contradict it, written before any outcome was related to any treatment. How each is tested is
in [09_empirical_design.md](09_empirical_design.md); the frozen test plan is `plan/pre_analysis_plan_v1.md`
(git tag `pap-v1`).

## 5.1 Primary hypotheses

These four form the primary family. Their p-values are corrected jointly for multiple testing (Holm, 5%).

| # | Hypothesis (plain language) | Model source | Contradicted if |
|---|---|---|---|
| **H7** | **Bans make correction one-sided.** In a ban, positive deviations of the basis (rich futures) revert more slowly; negative deviations (cheap futures) revert as fast or faster while arbitrage inventory lasts, and less so after an expiry has occurred inside the ban. | One-sided correction (4.6, result 2) | Upward deviations do not revert more slowly in bans, or upward and downward deviations change in the same way |
| **H8** | **Bans move trading out of futures** (mechanism). On ban days the change in futures open interest is about minus futures volume; futures volume falls; cash volume and the delivery share rise, relative to the same stock's non-ban days at similar utilisation. | Trading in a ban (4.6, result 5) | Change in OI plus volume is not close to zero, or futures activity does not fall |
| **H3** | **Costs set the band edges.** Around each STT increase (1 April 2023, 1 October 2024, 1 April 2026) the upper edge of the basis distribution rises, by more for larger cost changes (2026 > 2024 > 2023). | Costs set the edges (4.4, point 1) | No shift, or shifts unrelated to the size of the cost change |
| **H6** | **Short-sale access lowers overpricing and speeds up bad news.** After a stock enters the F&O segment, drift after bad news and price delay fall; after an eligibility exit they rise. | Miller and bad-news results (4.9) | No change, or changes of the opposite sign |

## 5.2 Secondary hypotheses (reported, labelled exploratory)

| # | Hypothesis | Model source | Contradicted if |
|---|---|---|---|
| Level | The ban's effect on the **level** of the basis follows the composition of trading before the ban: positive when open interest was falling (closing trades), negative when it was rising (new exposure). | Level effect (4.6, result 4) | Sign unrelated to composition |
| H9 | **Position-limit regime and anticipation.** On non-ban days the upper part of the basis distribution rises smoothly as utilisation approaches 95%; the 1 October 2025 reform acts through the predicted change in each stock's utilisation. | Anticipation; MWPL not an instrument (4.7, 4.8) | A jump only at 95% with no gradient before it; no effect of predicted utilisation |
| RD | A local jump in outcomes at 95% utilisation, after a density test. Supporting evidence only. | 4.7, 4.8 | (descriptive) |
| Hysteresis | Between 80% and 95% utilisation, stocks in a ban behave differently from stocks not in a ban. | Hysteresis (4.7) | No difference at equal utilisation and past path |
| H2 | **Bad news in bans.** Drift after bad news is larger on ban days; the negative pre-announcement basis seen outside bans disappears in bans. Few events (stated in advance). | Bad news in a ban (4.9) | Symmetric response to good and bad news |
| H1 | **Frictions and mispricing.** Band width and persistence rise with an index of ex-ante frictions (spread proxy, illiquidity, idiosyncratic volatility, utilisation headroom, lending availability). | Band and inventory results (4.4, 4.5) | No relation |
| H4 | **Arbitrage capital.** Flows into arbitrage funds lower the upper quantile of the cross-sectional basis. | Capital and location (4.4, points 2 and 4) | No relation after separating the 1 April 2023 STT change |
| H5 | **Anomalies and constraints.** Overpricing-side anomaly returns are stronger where shorting is costly; the underpricing side is unaffected. | Miller (4.9) | Symmetric effects |

## 5.3 What is deliberately not a one-sided hypothesis

The model does **not** predict that bans "widen mispricing". It predicts one-sided correction (H7) and a level effect whose
sign depends on the composition of trading. The empirical test of the level effect is whether its sign follows that
composition, not whether it has a particular sign.

## 5.4 Falsifiers in one list

- No upper/lower asymmetry in reversion during bans (H7).
- No change in futures activity during bans (H8).
- Band edges unrelated to dated cost changes (H3).
- No effect of F&O entry or exit on price delay or bad-news drift (H6).
