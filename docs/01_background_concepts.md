# 1. Background concepts

This page explains, from the ground up, every idea the rest of the documentation relies on. A reader who already knows
derivatives markets can skip to [02_research_question.md](02_research_question.md).

## 1.1 Stocks, the cash market and the derivatives market

- A **stock** (or share) is a unit of ownership in a company. Buying and selling stocks for immediate settlement happens
  in the **cash market** (also called the spot or equity market). In India, cash trades settle one trading day after the
  trade (T+1).
- A **derivative** is a contract whose value depends on another asset, the **underlying**. On the National Stock Exchange
  of India (NSE), derivatives on individual stocks and on indices trade in the **F&O segment** (futures and options).
- Only about 200 of the roughly 2,000 stocks listed on NSE have derivatives at any time. These are the **F&O stocks**.
  Which stocks qualify is set by rules of the market regulator, the Securities and Exchange Board of India (**SEBI**),
  based on size and liquidity. Stocks enter and leave the segment over time (see
  [03_institutional_setting.md](03_institutional_setting.md)).

## 1.2 Futures

- A **single-stock future** is an agreement to buy (long) or sell (short) a fixed number of shares of one stock on a
  future date, the **expiry**, at a price agreed today, the **futures price** F.
- Futures trade in **lots** (contract sizes) fixed by the exchange, for example 500 shares per contract.
- At any time NSE lists three monthly contracts per stock: the **near month** (expiring this month), the **next month**
  and the **far month**. Most trading is in the near month.
- Indian stock futures are **physically settled**: a position held to expiry ends with delivery of the shares.
- Profits and losses on futures are settled every day (mark to market), and traders post **margin** as collateral.

## 1.3 Options

- A **call option** gives the right, not the obligation, to buy the underlying at a set strike price; a **put option**
  gives the right to sell. Options on F&O stocks also trade on NSE.
- The **delta** of an option is how much its price moves when the stock price moves by one rupee. Delta lets a position
  in options be expressed as an equivalent number of shares (its **futures-equivalent** size). This matters for the
  position limits described below.

## 1.4 Open interest and volume

- **Volume** is the number of contracts (or shares) traded during a day.
- **Open interest (OI)** is the number of contracts outstanding at the end of the day: every open contract has one long
  side and one short side, and OI counts each contract once.
- If a trade opens a new position for both sides, OI rises by the size of the trade. If it closes positions for both
  sides, OI falls by that size. If one side opens and the other closes, OI is unchanged.
- **Market-wide OI** in a stock adds up OI over all its futures and options contracts, measured in shares.

## 1.5 The cost-of-carry price and the basis

Suppose a stock costs S today and pays no dividend before the future expires. An investor can get the stock at expiry in
two ways: buy it today and hold it (paying interest on the money used), or buy the future. If the two routes cost
different amounts, there is a riskless profit. So in a frictionless market the futures price must equal the
**cost-of-carry price**

    F* = (S - PV(D)) * exp(r * tau)

where r is the interest rate, tau is the time to expiry in years, and PV(D) is the present value of any dividends the stock
holder receives before expiry (the futures holder does not get them).

The **basis** (the project's main measure of mispricing) is the percentage gap between the actual futures price and this
value:

    m = ln F - ln F*

It is quoted in **basis points (bp)**: 1 bp = 0.01%. A basis of +20 bp means the future is 0.20% more expensive than
cost of carry ("rich"); a basis of -20 bp means it is 0.20% cheaper ("cheap").

## 1.6 Arbitrage

**Arbitrage** is trading that profits from a price gap between two things that should cost the same, and in doing so
closes the gap.

- **Cash-and-carry arbitrage** (used when the future is rich, m > 0): buy the stock, sell the future. At expiry the
  stock is delivered against the future and the trader earns the gap. Indian *arbitrage mutual funds* run this trade on a
  large scale.
- **Reverse arbitrage** (used when the future is cheap, m < 0): sell the stock, buy the future. This needs the trader to
  sell shares they do not own overnight, which in India requires borrowing the shares (see 1.8). So reverse arbitrage is
  much harder than cash-and-carry. Existing holders of the stock can do a version of it (sell their shares, buy the
  future), and arbitrageurs who already hold cash-and-carry positions can **unwind** them (sell the stock, buy back the
  future), which also pushes a cheap future back up.

## 1.7 Limits to arbitrage

In textbooks arbitrage is free and instant, so prices never deviate from fair value. In practice arbitrage is limited by:

| Limit | What it means |
|---|---|
| **Trading costs** | Taxes, fees, brokerage and price impact. A gap smaller than the round-trip cost is not worth trading. |
| **Short-sale constraints** | Rules or costs that make it hard to sell what you do not own. |
| **Capital** | Arbitrageurs have limited money and face margin calls; when capital is scarce, they cannot take every trade. |
| **Arbitrage risk** | The gap can widen before it closes, causing losses before convergence. |
| **Position limits** | Rules capping how large positions can be. |

The **limits-to-arbitrage** literature (Shleifer and Vishny 1997; Gromb and Vayanos 2010) argues that these limits let
mispricing persist. This project measures how strongly each limit binds in Indian equities.

## 1.8 Short selling in India

**Short selling** is selling shares you do not own, hoping to buy them back cheaper. In India:

- **Naked** short selling (selling without arranging to deliver the shares) is prohibited.
- Only **F&O-segment stocks** are eligible for short selling and for the formal stock-lending scheme (**SLB**, securities
  lending and borrowing). SLB trading is thin.
- Retail investors can short within a single day, but an **overnight** short position in practice means a short
  single-stock future (or options). This channel exists only for F&O stocks.

So for most Indian stocks there is no practical way to bet against the price overnight, and for F&O stocks the main way
is the futures market. This is why the F&O segment and the rules that restrict it matter for mispricing.

## 1.9 The market-wide position limit (MWPL) and the F&O ban

- The **MWPL** is a cap set by the exchange on the total open interest that all traders together may hold in a stock's
  derivatives. It is expressed in shares and is tied to the stock's **free float** (the shares not held by promoters,
  that is, by the founding or controlling group).
- **Utilisation** is market-wide OI divided by the MWPL, written omega (ω).
- When utilisation exceeds **95%** at the end of a day, the stock enters the **F&O ban** from the next trading day.
  During the ban **every** trader may only **reduce** existing positions in that stock's derivatives. Opening new
  positions or rolling a position into the next expiry is not allowed, and increases are penalised.
- The ban ends when utilisation falls to **80%** or below. The gap between 95% (entry) and 80% (exit) is a form of
  **hysteresis**: at the same utilisation, say 88%, a stock may be in a ban (it crossed 95% earlier) or not.

The exact rules and their history are in [03_institutional_setting.md](03_institutional_setting.md).

## 1.10 The no-arbitrage band

Because arbitrage is costly, small deviations of the basis are left alone: the cost of trading would exceed the gain. Only
when the basis moves outside a range does arbitrage start. This range is the **no-arbitrage band**:

- Upper edge c+ : the cost of a cash-and-carry trade.
- Lower edge -c- : minus the cost of a reverse trade (larger in India, because shorting is hard).

Inside the band the basis wanders with demand; outside it, arbitrage pushes it back. Section
[04_theoretical_framework.md](04_theoretical_framework.md) derives this formally.

## 1.11 Statistical tools used (plain descriptions)

| Tool | What it does here |
|---|---|
| **Threshold autoregression (TAR / SETAR)** | A time-series model in which the speed at which the basis reverts depends on which "regime" it is in: inside the band (little reversion) or outside it (strong reversion). The regime boundaries (thresholds) are estimated. |
| **Threshold vector error-correction model (TVECM)** | The same idea written for the futures price and the stock price jointly (Ters and Urban 2020). |
| **Smooth-transition models (ESTAR)** | Like TAR, but the reversion speed changes gradually with the size of the deviation (Tse 2001). |
| **Event study** | Compare an outcome before and after a dated event (e.g. a stock entering a ban) with a control group that did not experience the event. |
| **Difference-in-differences (DiD)** | Compare the change in an outcome for treated units with the change for untreated units over the same period. **Staggered DiD** (Callaway and Sant'Anna 2021) handles events that happen at different dates for different stocks. |
| **Regression discontinuity (RD)** | Compare outcomes just above and just below a rule's cut-off (here 95% utilisation), where units are otherwise similar. A **density test** (Cattaneo, Jansson and Ma 2020) checks that units do not bunch on one side. |
| **Clustered standard errors** | Measures of uncertainty that allow observations of the same stock, or the same day, to be correlated. |
| **Holm correction** | Adjusts significance thresholds when several main hypotheses are tested together, so that the chance of at least one false positive stays at 5%. |

## 1.12 Other terms

| Term | Meaning |
|---|---|
| **Bhavcopy** | NSE's daily file of prices, volumes and open interest for every traded instrument. |
| **UDiFF** | The newer, standardised NSE file format used from July 2024. |
| **VWAP** | Volume-weighted average price: total traded value divided by total traded quantity over the day. |
| **Settlement price** | The price NSE uses to mark futures to market each day. When a contract does not trade in the last half hour, NSE sets it to a theoretical cost-of-carry value (see [08_variables_and_measures.md](08_variables_and_measures.md)). |
| **Ex-date** | The first day a stock trades without the right to an announced dividend. |
| **STT** | Securities transaction tax, a tax on the value of trades, set in the Union Budget. |
| **ISIN** | International Securities Identification Number, a fixed code for a security that survives name and symbol changes. |
| **Free float** | Shares not held by promoters. |
| **ADDV** | Average daily delivery value (or quantity): how many shares change hands for delivery, as opposed to intraday trades. |
| **Earnings announcement** | A company's release of quarterly financial results. **Post-earnings-announcement drift** is the tendency of prices to keep moving in the direction of the news for weeks afterwards. |
| **Pre-analysis plan (PAP)** | A document fixing the tests before any outcome is related to any treatment (see [09_empirical_design.md](09_empirical_design.md)). |
