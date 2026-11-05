# 4. Theoretical framework

The full model, with proofs, is in `BSP_Model_C_Constrained_Arbitrage_India.pdf` (LaTeX source and a numerical check
of every closed form in `models_src/modelC/`; run `python3 verify_modelC.py` there, all checks pass). This page explains
it step by step for a reader without a finance background. Notation is listed at the end.

## 4.1 Why a model first

The model is written before any outcome is examined, so that each hypothesis is **derived**, not fitted to the data, and
each comes with a result that would contradict it. Where the model says an effect could go either way, it also says what
observable condition decides the sign; the empirical work then tests that condition rather than a one-sided claim.

Three design rules:

1. **Institutions as they are.** The ban, short-selling rules, settlement prices and costs follow the primary sources
   ([03_institutional_setting.md](03_institutional_setting.md)).
2. **Predictions that can fail.**
3. **Daily horizon.** The arbitrageur holds positions overnight (arbitrage funds, proprietary desks), because the data
   are daily.

## 4.2 Set-up

**Prices.** A stock has price S and a future maturing at T. The cost-of-carry value of the future is
F* = (S - PV(D)) exp(r (T - t)). The basis is m = ln F - ln F*. Write s and f for how far the spot and futures prices
are from fundamental value; then m is approximately f - s.

**Outside traders.** Everyone who is not an arbitrageur (retail traders, hedgers, investors) is summarised by simple
demand curves:

- in the cash market, net demand D_S - psi_S * s;
- in the futures market, net long demand D_F - psi_F * f.

psi_S and psi_F measure the **depth** of each market (how much the price must move to absorb an order). D_S and D_F
shift with news and sentiment.

**Arbitrage sector.** Arbitrageurs together hold a units of the cash-and-carry trade: long a shares and short a futures
(a negative a means reverse arbitrage).

**Market clearing.** Both markets must clear:

    D_S - psi_S * s + a = 0        and        D_F - psi_F * f - a = 0.

Subtracting one from the other gives the key equation

    m = (u - a) / Phi,     where  1/Phi = 1/psi_F + 1/psi_S  and  u = Phi * (D_F/psi_F - D_S/psi_S).

u is the **relative demand pressure toward futures**. It is positive when outside traders want long exposure through
futures more than through cash (for example leveraged speculative longs), and negative when they want short exposure
through futures (hedgers, or pessimists who can only short through futures). Without arbitrage (a = 0) the basis is
u / Phi. Arbitrage lowers it by a / Phi, because buying the stock raises s and selling the future lowers f.

## 4.3 What arbitrageurs want

Arbitrageurs choose a to maximise

    Pi(a) = a*m - (gamma/2)*a^2 - c_plus * max(a, 0) - c_minus * max(-a, 0),     gamma = alpha * sigma^2.

- a*m is the gain if the basis converges to zero at expiry.
- (gamma/2) a^2 is the cost of risk: alpha is risk aversion per unit of capital (higher when capital is scarce) and
  sigma^2 the risk borne before convergence (margin calls, the risk of unwinding early at a loss).
- c_plus is the cost of a cash-and-carry position; c_minus the cost of a reverse position. Each is a round-trip
  transaction cost plus a financing term:

      c_plus  = tau_plus  + (r_A - r_b) * (T - t)
      c_minus = tau_minus + (l_s + r_b - r_L) * (T - t)

  with tau the trading costs (STT, stamp duty, fees, brokerage, impact), r_A the return arbitrage capital requires,
  r_b the benchmark rate, l_s the stock-lending fee and r_L the rebate earned on short-sale proceeds.

**How each Indian limit enters:**

| Limit | Indian institution | Parameter |
|---|---|---|
| Trading costs | STT on futures (four dated levels); cash STT; fees | tau_plus, tau_minus |
| Short-sale cost | No naked shorting; only F&O stocks eligible; SLB thin | c_minus (effectively infinite for cash-only stocks) |
| Arbitrage capital | Arbitrage-fund assets; funding rates; peak-margin rules | alpha (so gamma), r_A |
| Arbitrage risk | Basis volatility, idiosyncratic volatility | sigma^2 (so gamma) |
| Position limits | Entity limits, MWPL, F&O ban | caps on a; the reduce-only rule |
| Market depth | Liquidity of outside traders | psi_S, psi_F (so Phi) |

## 4.4 Result 1: the no-arbitrage band

Solving the arbitrageurs' problem together with market clearing gives a unique equilibrium:

- If -c_minus <= u/Phi <= c_plus, arbitrageurs do nothing (a = 0) and **m = u/Phi**: the basis moves one-for-one with
  demand pressure.
- If demand pushes the basis above c_plus, arbitrageurs sell futures and buy stock:
  **m = (gamma*u + c_plus) / (gamma*Phi + 1)**.
- If demand pushes it below -c_minus, they do the reverse: **m = (gamma*u - c_minus) / (gamma*Phi + 1)**.

So there is a **band [-c_minus, c_plus]** inside which the basis is left alone, and outside which arbitrage absorbs part
of each shock. The response of the basis to demand falls from 1/Phi inside the band to gamma/(gamma*Phi + 1) outside.

**Comparative statics:**

1. **Costs set the edges.** The edges are c_plus and -c_minus. They do not depend on capital or risk. A change in trading
   costs (e.g. an STT change) moves the corresponding edge one-for-one.
2. **Capital and risk set how far the basis travels beyond an edge.** Beyond an edge the slope gamma/(gamma*Phi + 1) rises
   with gamma = alpha*sigma^2: scarcer capital or riskier convergence lets the basis go further out.
3. **Maturity.** Both edges are linear in the time to expiry and shrink to the pure trading costs at expiry.
4. **Location.** The band is centred at (c_plus - c_minus)/2, **below zero** when shorting costs more than carrying, as
   it does in India. The upper edge itself can be negative if cash-and-carry capital accepts a return below the benchmark
   rate. Earlier Indian studies find a band centred below zero, for example mean thresholds of -39 and -10 bp for 102 NSE
   stock futures in Shankar, Sankar and Kiran Kumar (2015). The model reproduces this.

## 4.5 Result 2: inventory moves the no-trade region

The ban acts on positions already held, so the model tracks arbitrage **inventory**. Days are discrete. The sector enters
day t holding a_(t-1) >= 0, pays c_plus per unit added and c_u per unit unwound, and chooses a_t to maximise

    a_t*m_t - (gamma/2)*a_t^2 - c_plus*(a_t - a_(t-1))^+ - c_u*(a_(t-1) - a_t)^+.

(Reverse arbitrage is set aside here; the ability of stock holders to sell cash and buy futures is part of cash-market
depth.) The sector trades only when the basis leaves

    [ gamma*a_(t-1) - c_u ,  gamma*a_(t-1) + c_plus ].

**Meaning:** the thresholds are not constants. A large existing cash-and-carry book raises both the level at which new
arbitrage starts and the level at which unwinding starts. Threshold models estimated on data should therefore allow the
thresholds to depend on lagged open interest; fixed thresholds estimate an average.

## 4.6 Result 3: the F&O ban as a reduce-only rule

In a ban the model imposes two restrictions:

- **(B1) Reduce-only arbitrage:** 0 <= a_t <= a_(t-1). Arbitrageurs can unwind but not add.
- **(B2) Blocked new exposure:** outside traders' demand changes have two parts, demand to **close** positions
  (long liquidation, short covering), which can still be executed, and demand for **new** futures exposure, which cannot.
  A share chi of the blocked new demand moves to the cash market (a trader who cannot buy the future buys the stock on
  margin); the rest is withdrawn. In the clearing equation this turns a new-demand shock e into -lambda*e, with
  lambda = chi * psi_F / psi_S >= 0.

Consequences (each proved in the model document):

1. **The basis in a ban is at least as high as outside a ban** for the same demand and inventory, because the ban only
   removes the option to add, which is used only to push the basis down.
2. **One-sided correction.** With inventory a_(t-1) > 0 at the start of a ban:
   - *No ceiling:* when demand pressure rises, every increase passes through fully (slope 1/Phi instead of
     gamma/(gamma*Phi + 1)). **Rich futures are not corrected.**
   - *A floor while inventory lasts:* when pressure falls, the sector unwinds and the basis is held at
     m_t = gamma*a_t - c_u. **Cheap futures are still corrected**, at a level that rises with remaining inventory.
   - *The floor wears out:* once inventory reaches zero, the floor disappears. Positions cannot be rolled, so an
     **expiry inside a ban** removes the expiring part of the inventory for the rest of the ban.
3. **Sign reversal of new demand.** Outside a ban, new long demand for futures raises the basis. In a ban the same shock
   **lowers** it (slope -lambda/Phi), because the blocked demand moves to the cash market and raises the stock price
   instead. The reversal is strict if chi > 0.
4. **The level effect is ambiguous.** Compare the same shocks with and without a ban. The difference
   (ban minus no ban) is falling in the amount of new-exposure demand, is non-negative when there is none, and becomes
   negative when new demand is large enough. **A ban raises the basis when pressure comes mainly from closing trades and
   lowers it when new speculative demand keeps arriving.** The observable sign condition is the composition of trading
   before and during the ban (rising open interest means new positions; falling means closing).
5. **Trading and measurement in a ban.**
   - If the rule binds contract by contract, every futures trade in a ban closes a long and a short, so
     **change in OI = - volume** outside expiry days. From October 2025, trades that offset across instruments (allowed
     under the delta test) break this identity, and the gap measures such offsetting.
   - Futures volume falls and spreads widen, because a trade needs a long and a short who both want to reduce.
   - On days with no trade in the last half hour, NSE's theoretical settlement price makes a settlement-price basis zero
     by construction. **Bans thin out trading, so a settlement-price basis would show the basis "closing" during bans for
     purely mechanical reasons.** The data work therefore uses traded prices and flags theoretical settlements.

## 4.7 Result 4: anticipation and hysteresis

If exiting a position during a ban is costlier (by l > 0, because only traders who also want to reduce can be
counterparties), and a position opened at utilisation omega meets a ban before it is closed with probability pi(omega)
(rising in omega), then outside a ban the effective cost of opening cash-and-carry is c_plus + pi(omega)*l.

- **Anticipation:** the upper edge of the no-trade region rises **smoothly** as utilisation approaches 95%, and new
  arbitrage slows before any ban. The jump at exactly 95% contains only the reduce-only effects of 4.6.
- **What a density test can show:** arbitrageurs holding back thins the density of utilisation just below 95%;
  speculators rushing in before an expected ban does the opposite. The model does not sign a density test; the test
  shows which force dominates.
- **Hysteresis:** for utilisation between 80% and 95% a stock may be in a ban (it crossed 95% earlier) or not. Comparing
  the two at the same utilisation measures the reduce-only state against the anticipation state.

## 4.8 Result 5: what this implies for identification

**The MWPL is not a valid instrument for ban status.** The MWPL affects the basis through three channels: the ban state,
the anticipation term pi(omega), and entity limits proportional to the MWPL. A change in the MWPL therefore moves the
basis even when no ban occurs, which violates the exclusion restriction. Changes in the MWPL identify the **total**
effect of the position-limit regime (ban plus anticipation plus caps), not the effect of the ban alone.

What each design identifies under the model:

| Design | Identifies |
|---|---|
| Regression discontinuity at 95% | The local jump in the reduce-only effects, provided utilisation cannot be placed precisely on one side |
| Hysteresis comparison (80% to 95%) | Reduce-only state versus anticipation state at equal utilisation, controlling for past paths |
| Ban-entry event study with near-miss controls | The dynamic effects of 4.6 against stocks with similar paths that stayed below 95% |
| 1 October 2025 reform and quarterly MWPL resets | Reduced-form, total-regime effects of predicted changes in utilisation |

## 4.9 Result 6: short-sale constraints beyond the basis

**Bad news in a ban.** Suppose an announcement reveals news of size delta and trading on the day impounds a share k of
it. For bad news, a share rho of informed selling runs through short futures (the only overnight short in an F&O stock).
In a ban that capacity is gone, so the share impounded falls to k(1 - rho) and the drift after bad news rises from
(1 - k)*delta to (1 - k + k*rho)*delta. Good news is unaffected, because optimists can still buy the stock.

**Cash-only stocks and F&O entry (Miller 1977).** Investors' valuations are spread uniformly over [v - delta, v + delta];
each long investor demands k(v_i - p); shorting costs c_s per unit; supply is Q > 0.

- The price p rises with the cost of shorting c_s.
- With free shorting, p = v - Q/k. With no shorting (and delta >= Q/k), p = v + delta - 2*sqrt(delta*Q/k), so the
  **overpricing is (sqrt(delta) - sqrt(Q/k))^2**, which rises with disagreement delta.

Entry into the F&O segment lowers c_s. It should therefore lower the prices of high-disagreement stocks at entry and
reduce their later underperformance; exit should do the reverse. Diamond and Verrecchia (1987) add that short constraints
slow the incorporation of bad news even without a level bias.

## 4.10 Heterogeneous arbitrageurs and the estimation lens

With a single cost the band has sharp edges. If costs differ across arbitrageurs, aggregate arbitrage rises smoothly
with the size of the deviation. In daily data the basis then follows an error-correction process whose speed of
reversion rises smoothly with the distance from the band's centre (a smooth-transition model, Tse 2001), well
approximated by a three-regime threshold model whose thresholds are quantiles of the cost distribution (Dwyer, Locke and
Yu 1996; Ters and Urban 2020). The inventory result adds that the thresholds move with inventory; the ban result adds
that in a ban the upper regime's reversion falls toward zero while the lower regime's remains.

## 4.11 Calibration and horizon

For an overnight carrier the round-trip cost of a cash-and-carry trade includes STT on the stock purchase and sale (0.1%
each), STT on the futures sale (0.01% to 0.05% depending on the period) or 0.1% on physical delivery, stamp duty, fees,
brokerage and impact: tens of basis points. This is far wider than bands of a few basis points estimated from one-second
data, which describe intraday market makers. Funds that roll positions rather than take delivery spread these costs over
several expiries. The simulations use round illustrative numbers (c_plus = 15 bp, c_u = 10 bp, c_minus = 60 bp); they
are not estimates.

## 4.12 Simulation and numerical checks

A script solves each equilibrium numerically (bisection on the best-response fixed point) and compares it with the closed
forms: the static band, the inventory step with and without a ban, the floor gamma*a_t - c_u, the full passthrough above
it, the "at least as high" lemma, the monotonicity and sign change of the level effect, and the Miller closed forms. All
pass.

A simulation (Phi = gamma = 1; c_plus = 15, c_u = 10 bp; demand pressure AR(1) with persistence 0.9 around 25 bp; daily
shock standard deviation 6 bp per component; lambda = 0.5; 300 paired paths with and without a 40-day ban) shows:

- **Asymmetric reversion:** the slope of the daily change in the basis on its lagged level above the 80th percentile
  weakens from -0.18 (no ban) to -0.13 (ban); below the 20th percentile it strengthens from -0.12 to -0.16.
- **Level effect:** with no extra new demand during the ban the mean basis is 4.9 bp higher; with a steady inflow of 1, 2
  and 4 bp per day of new demand it is 3.1, 10.8 and 26.0 bp lower.

These simulated data are also used to test the estimators before they touch real data
([09_empirical_design.md](09_empirical_design.md), section 9.6).

## 4.13 Limitations

1. Partial equilibrium, linear outside demand, a myopic mean-variance arbitrage sector; the option to unwind early
   enters only through the inventory structure.
2. The split of outside demand into closing and new-exposure parts drives the sign-reversal and level results. Its
   empirical counterpart (order flow that opens versus closes positions) is only partly observable in public data
   (changes in open interest against volume).
3. Reverse arbitrage by stock holders is folded into cash-market depth.
4. Anticipation rests on exit being costlier in a ban, which is itself testable (futures activity in bans).
5. The news and Miller results fix directions, not magnitudes.

## Notation

| Symbol | Meaning |
|---|---|
| S, F, F* | Stock price, futures price, cost-of-carry futures value |
| m | Basis, ln F - ln F* |
| u | Relative demand pressure toward futures |
| psi_S, psi_F, Phi | Depth of the cash and futures markets; combined depth |
| a | Arbitrage position (units of cash-and-carry) |
| alpha, sigma^2, gamma | Risk aversion per unit of capital; basis risk; gamma = alpha*sigma^2 |
| c_plus, c_minus, c_u | Cost of a cash-and-carry position, of a reverse position, of unwinding |
| omega | Utilisation, open interest / MWPL |
| pi(omega), l | Probability of meeting a ban; extra cost of exiting in a ban |
| chi, lambda | Share of blocked new demand that moves to cash; lambda = chi*psi_F/psi_S |
| delta, k, rho | News size; share impounded on the day; share of informed selling via futures |
