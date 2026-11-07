# 2. Research question, scope and contribution

## 2.1 The question

**How strongly do limits to arbitrage bind in the Indian equity market, which kinds of limits matter, and how much
mispricing do they explain?**

"Mispricing" is measured in three ways (defined in [08_variables_and_measures.md](08_variables_and_measures.md)):

1. the **futures-cash basis** of F&O stocks: the gap between a stock future's price and its cost-of-carry value (main
   measure);
2. **post-earnings-announcement drift**: how slowly prices absorb news in quarterly results;
3. **price delay**: how slowly a stock's price responds to market-wide news.

## 2.2 Why India

India offers a dated, observable change to almost every kind of limit to arbitrage, which lets the project study them
side by side within one market and one data source.

| Kind of limit | Indian source of variation |
|---|---|
| Short-sale constraints | Only F&O-segment stocks are eligible for short selling (stock lending also covers other liquid stocks, but is thin), and the practical overnight short is the single-stock future. **Entry into and exit from the F&O segment** changes this permanently for a stock. The **F&O ban** removes it temporarily. |
| Trading costs | The securities transaction tax (STT) on futures sales was changed on fixed dates: 0.01% from 1 June 2013, 0.0125% from 1 April 2023, 0.02% from 1 October 2024 and 0.05% from 1 April 2026. |
| Arbitrage capital and funding | Assets of arbitrage mutual funds (large inflows after the 1 April 2023 change in the taxation of debt funds); money-market rates; the peak-margin rules phased in from December 2020 to September 2021. |
| Arbitrage risk | Basis volatility and idiosyncratic (stock-specific) volatility. |
| Position limits | The MWPL, entity-level limits, the ban rule, the halving of the MWPL for volatile stocks in March 2020, and the new MWPL formula of 1 October 2025. |

## 2.3 The F&O ban as a focus

The F&O ban is the sharpest of these sources of variation, and it has essentially not been studied. When a stock's
derivatives open interest crosses 95% of its limit, every trader in that stock's futures and options is restricted to
reducing positions until open interest falls to 80%. Between 2015 and October 2026 this happened 1,788 times, to 141
different stocks. The ban is one lens on the wider question, not the whole project.

## 2.4 Approach

The project proceeds in a fixed order:

1. **Theory first.** One model of constrained arbitrage covers all the limits listed above; each limit is a parameter.
   Every hypothesis is derived from the model, together with the result that would contradict it
   ([04_theoretical_framework.md](04_theoretical_framework.md), [05_hypotheses.md](05_hypotheses.md)).
2. **Tests written down before data are examined.** A pre-analysis plan fixes samples, variables, specifications and
   falsifiers, and is frozen with a git tag before any outcome is related to any treatment
   ([09_empirical_design.md](09_empirical_design.md)).
3. **A data set built from primary sources**, every step scripted and checked against the exchange's own rules
   ([06_data_sources.md](06_data_sources.md), [07_data_construction.md](07_data_construction.md),
   [10_data_quality_audit.md](10_data_quality_audit.md)).
4. **Estimators tested on simulated data** from the model before they are applied to real data.
5. **Tests, then interpretation**, reporting every pre-specified test, including nulls.

## 2.5 Contribution

Relative to existing work, the project:

- **Studies the F&O ban.** No study we are aware of estimates its effects. The closest Indian work estimates
  no-arbitrage bands for stock futures without the ban: Aggarwal (2015), 141 stocks with one-second data over six months
  of 2013; Shankar, Sankar and Kiran Kumar (2015, published 2019), 102 stocks with five-minute data for 2007 to 2009. A
  recent working paper by Saurav, Srivastava and Agarwalla (2026) studies the stock-futures basis around earnings
  announcements and short-sale constraints.
- **Models the ban as it actually works.** The ban restricts every participant to reducing positions, not only
  arbitrageurs. The model shows that this makes correction of the basis **one-sided** and makes the ban's effect on the
  level of the basis **ambiguous in sign**, with an observable condition that sets the sign.
- **Corrects an identification idea.** Changes in the MWPL cannot serve as an instrument for ban status, because they
  also change the chance of future bans, which traders respond to even when no ban occurs.
- **Covers many limits with dated shocks** over a long daily sample (2015 to 2026, about 200 F&O stocks at a time, plus
  the full cash market for the F&O entry and exit tests).
- **Pre-registers its tests** with falsifiers derived from theory.

## 2.6 Scope and what is not claimed

- The unit of analysis is a stock on a trading day. Data are end-of-day; intraday dynamics are outside scope.
- The arbitrageur in the model is an overnight carrier (an arbitrage fund or a proprietary desk), not an intraday market
  maker, because the data are daily.
- Results for the period after the 1 October 2025 reform rest on 44 ban spells and are reported as low-powered.
- The welfare of retail traders is not re-estimated; SEBI's own studies are used for the policy discussion.
