# 01. Project overview (the research design in full)

## 1.1 Identity

| Item | Value |
|---|---|
| Student | Prince Kumar, roll 23B3032, 4th-year BS Economics, IIT Bombay (2023 to 2027) |
| Course | BS Project: EC 495 Stage I (6 credits, semester 7, about July to November 2026) then EC 497 Stage II (12 credits, semester 8, about January to April 2027) |
| Guide | Prof. Aditi Chaubal, Department of Economics (non-linear time series). Spelling "Chaubal" confirmed by the user on 5 Nov 2026 (the user once voice-typed "Chawla") |
| Title | Limits to Arbitrage in the Indian Equity Market |
| Repository | `deviant7/bsp` on GitHub; working branch `claude/compassionate-rubin-s9gny2`; `main` has everything up to 28 Oct 2026 (PR #1 merged) |

## 1.2 Research question

Primary: **how strongly do limits to arbitrage bind in Indian equities, which kinds of limits matter, and how much
persistent mispricing do they explain?**

Mispricing measures:
1. **Futures-cash basis** of F&O stocks (main): m = ln F - ln(S - PV(D)) - r*tau, built from daily VWAPs.
2. **Post-earnings-announcement drift** (BHAR[+2,+64], surprise = announcement return EAR[-1,+1]; SUE from XBRL EPS as
   secondary).
3. **Price delay** (Hou and Moskowitz 2005) and variance ratios in the cash market.
4. Put-call parity: demoted to optional robustness (thin stock options).

## 1.3 Why India: a dated shock to almost every kind of limit

| Limit | Indian source of variation | Used for |
|---|---|---|
| Short-sale constraints | Only F&O-segment stocks are eligible for short selling (SLB also covers other liquid stocks since 2013; see 10); naked shorting banned; SLB thin, so the practical overnight short is the stock future. F&O entry/exit changes this permanently; the ban removes it temporarily | H6 (entry/exit), H7, H2 |
| Trading costs | Futures STT: 0.01% (1 Jun 2013), 0.0125% (1 Apr 2023), 0.02% (1 Oct 2024), 0.05% (1 Apr 2026) | H3 |
| Arbitrage capital | Arbitrage-fund AUM (AMFI, from mid-2018); 1 Apr 2023 debt-fund tax change; peak-margin phase-in Dec 2020 to Sep 2021 | H4 |
| Arbitrage risk | Basis volatility, idiosyncratic volatility | H1 |
| Position limits | MWPL; entity limits; ban (95%/80%); COVID MWPL halving (Mar to Nov 2020); new MWPL formula 1 Oct 2025; quarterly MWPL resets after Oct 2025 | H7, H8, H9, level effect, RD, hysteresis |

## 1.4 Contribution (as currently positioned)

- First study (as far as searches found) of the effects of India's F&O ban.
- Models the ban as it works: a **reduce-only rule for everyone**, giving **one-sided correction** and an
  **ambiguous-sign level effect** with an observable sign condition (composition of order flow).
- Shows the MWPL is **not** a valid instrument for ban status (an idea in the original project document).
- Covers many limits with dated shocks over 2015 to 2026 daily data (bans 2010 to 2026), plus the full cash market for
  F&O entry/exit.
- Pre-registered tests with falsifiers.
- Closest precedents: Aggarwal (2015, one-second bands, 141 stocks, 2013, no ban); Shankar, Sankar and Kiran Kumar (2015,
  SETAR bands on 5-minute data, 102 stocks, 2007 to 2009, no ban); Saurav, Srivastava and Agarwalla (2026, SSRN; stock
  futures basis around earnings and short-sale constraints; **not yet read in full**; the closest competitor for H2/H7).

## 1.5 Hypotheses (H1 to H9) and their status in the frozen plan

| H | Content | Status |
|---|---|---|
| H7 | In bans, correction becomes one-sided: rich futures (upper regime) revert less; cheap futures revert as fast or faster while inventory lasts, less after an expiry inside the ban | **Primary** |
| H8 | In bans, trading moves out of futures: dOI + volume ~ 0; futures volume down; cash volume and delivery share up | **Primary** (mechanism) |
| H3 | Costs set band edges: upper edge rises around each STT increase, ordered 2026 > 2024 > 2023 | **Primary** |
| H6 | F&O entry lowers bad-news drift and price delay; eligibility exit raises them (staggered DiD) | **Primary** |
| Level | Ban level effect sign follows pre-ban order-flow composition | Secondary |
| H9 | Upper basis quantile rises smoothly with utilisation before 95%; 1 Oct 2025 reform acts through predicted utilisation | Secondary |
| RD | Jump at 95%, after a density test | Secondary (supporting) |
| Hysteresis | In [0.80, 0.95): in-ban vs not-in-ban | Secondary |
| H2 | Bad-news drift larger on ban days; pre-announcement negative basis vanishes in bans | Secondary (low power: 180 events) |
| H1 | Friction index vs band width | Secondary |
| H4 | Arbitrage-fund flows vs upper basis quantile | Secondary |
| H5 | Overpricing-side anomalies stronger where shorting is costly | Secondary |

Primary family corrected with Holm at 5%.

## 1.6 Planned thesis structure (as planned in Oct 2026; the final structure is below)

1. Introduction and institutions. 2. Theory (+ simulation). 3. Data and measurement (mispricing measures; friction index).
4. Bands over time: costs, capital, reforms. 5. The F&O ban. 6. F&O eligibility and the cross-section. 7. Policy and
conclusion. Appendices: band-of-inaction derivation, pre-analysis plan, data construction, replication guide.

Final thesis structure (9 Nov 2026, `BSP_Thesis_Final_Nov2026.pdf`): 1 Introduction; 2 Related literature; 3 Institutional
setting; 4 Model; 5 Data and measurement (incl. constraint index); 6 The no-arbitrage band: costs, capital and position
limits (H3, H4, H9, H1, spurious bans, COVID restoration); 7 The F&O ban (H8, H7, level effect, 95% trigger, H2, placebos);
8 F&O eligibility and the cross-section (H6, H5); 9 Conclusion and policy. Appendices: A pre-analysis plan and log;
B data construction; C the model in full.

## 1.7 Chapter-to-test map (as planned)

| Chapter | Tests |
|---|---|
| 3 Measurement | Basis, implied repo, friction index (H1), data audit |
| 4 Bands over time | H3 (STT), H4 (capital), H9 (reform intensity), TVECM/ESTAR bands, state-dependent thresholds |
| 5 Ban | H7, H8, level effect, RD, hysteresis, H2 |
| 6 F&O eligibility and cross-section | H6, H5 |
| 7 Policy | Reading of results against SEBI's speculation versus market-quality trade-off; how many bans were "spurious" (denominator-driven) before and after Oct 2025; retail-loss framing from SEBI's study |

## 1.8 Data (one paragraph; full detail in 08)

All from free NSE archives/APIs plus FRED: combined open interest/MWPL file (daily, Feb 2010 to 27 Oct 2026), securities
in ban (daily), F&O bhavcopy (2015 to 2026; legacy format to 5 Jul 2024, UDiFF from 8 Jul 2024), cash bhavcopy, delivery
(MTO) file, corporate actions, results filings, "Financial Result Updates" announcements, board meetings, Nifty index
file, 3-month interbank rate (OECD via FRED). Processed sets: MWPL/OI/ban panel (752,037 stock-days), ban days and spells,
F&O membership and entry/exit events, announcements (94,071 events), basis panel (1,066,167 rows).

## 1.9 What "done" will look like (status 9 Nov 2026: all of it exists; the replication package is the repository itself)

- Theory document (done), test plan (frozen), data set (built, audited), estimates of every pre-specified test with
  nulls reported, a results page in `docs/`, thesis chapters in LaTeX, a final report/thesis PDF for the guide, a
  replication package (the repo).
