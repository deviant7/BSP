# Reading Notes — Batch 3: Indian market evidence (calibration tier)

Covers references 8–11. These calibrate *what mispricing looks like in India* and give us magnitude benchmarks and the specifically-Indian short-sale-asymmetry fact. Read from the PDFs (Roy-Chakraborty extraction was partly garbled by two-column layout; characterised from the readable portions).

---

## 8. Nandan, Agrawal & Bhargava (2014) — CNX Nifty futures mispricing, 2003–2012

**Setup.** Cost-of-carry fair value F0 = S0·e^{(r−q)T} (r = 30-day MIBOR, q = dividend yield), vs observed near-month Nifty futures, **daily closing**, Jan 2003–Dec 2012, 2,382 obs (expiry days filtered). Non-parametric tests (KS for non-normality; Mann-Whitney across basis sign; Kruskal-Wallis + Dunn across days-to-expiry).

**Findings we use as benchmarks.**
- **Persistent net underpricing**: overall mean mispricing **−₹8.19**; **71% of observations are negative** (futures underpriced) vs 29% positive — the classic **short-sale-constraint signature** (you can't easily do reverse-cash-and-carry, so negative mispricing isn't arbitraged away). Magnitude also larger on the negative side (−₹13.99 vs +₹6.04).
- **Mispricing rises with days-to-expiry** (mean −₹14.9 at >21 days vs −₹0.46 at 1–7 days) — convergence as expiry nears.
- **Efficiency improved over the decade**: mean underpricing fell from −₹24.3 (2007) toward ≈ −₹0.23 (2012); 2012 even flipped to more positive than negative signals. So the Indian basis anomaly is real but *attenuating over time* — important for our sample: the pre-2015 period behaves differently from the reform era, supporting a regime-aware design.

**Relevance.** Confirms the futures-basis measure (our Ch 2 measure #1) is meaningful in India and that the negative-side asymmetry is a robust Indian stylised fact. Also flags that time-trend/regime matters — reinforces our staggered/regime-shift framing. Caveat they share with us: daily closing prices → non-synchronous-trading noise; they ignore transaction costs (we won't).

## 9. Roy & Chakraborty (2023), *Global Business Review* — efficiency & price discovery in NSE single-stock futures

**What it does.** Examines the dynamic linkage / lead-lag and market efficiency between single-stock futures and their underlying spot at NSE, using Johansen cointegration and AR-order/causality testing. Confirms the long-run cointegration (law-of-one-price holds in the long run) with short-run deviations and a price-discovery role for the futures segment.

**Relevance.** A more recent Indian efficiency reference to cite for (a) the cointegration foundation our TVECM assumes (spot and futures are cointegrated; the basis is the error-correction term) and (b) the price-discovery angle if we add a lead-lag/information-share sub-section. Lower-priority: it's background/positioning, not method we replicate. (Full-text re-read optional — the PDF's two-column layout garbles cleanly extracted text.)

## 10. Harshita, Singh & Yadav (2018) — PEAD anomaly in India, 2002–2017

**Setup.** Standardized Unexpected Earnings (SUE) → post-earnings-announcement drift; **cross-sectional Fama-MacBeth regressions** + paired t-tests, 2002–2017.

**Findings we use.**
- **Statistically significant PEAD exists in India**, robust to sub-periods and after controlling for **beta, market cap, P/B, illiquidity, and idiosyncratic volatility**. Prices under-react to earnings surprises and drift in the surprise direction — a semi-strong-form inefficiency.

**Relevance (Ch 2 measure #3 + Ch 5 method).** This is our warrant that PEAD is a usable mispricing measure in India, and it hands us (a) the SUE construction and (b) a working **Fama-MacBeth** template on Indian data — the same estimator as our cross-sectional chapter. Our extension: interact PEAD magnitude with the arbitrage-constraint index / ban status (H2 — drift should be *deeper* where the trades that would close it are blocked). Note the authors already include idiosyncratic volatility as a control — our constraint index generalises that into a richer measure.

## 11. Slivka, Shah & Wu (2011), NYU-Poly working paper — practitioner view of Indian SSF-vs-futures arbitrage

**The one killer fact.** Using recent single-stock-futures data, the **zero-arbitrage band width in India is "typically at least twice that occurring in mature global markets."** That is a direct, quotable magnitude benchmark for our band estimates: we should *expect* Indian bands roughly 2× developed-market width, and the reforms' job is to narrow them.

**Why the band is wide (their diagnosis).** High brokerage + government/exchange/regulatory fees + STT, an **underdeveloped SLB market** that throttles short selling, and (secondarily) execution speed. Consequently, real arbitrage in India is **confined almost entirely to intraday single-stock-vs-futures** trades; NIFTY index-basket-vs-futures arbitrage is "notably absent" (basket execution too hard/costly).

**Relevance.** (a) Corroborates Aggarwal's wide, asymmetric bands from the practitioner side and gives a clean "2× mature markets" headline. (b) Justifies our focus on **single-stock** futures basis rather than index-basket arbitrage. (c) Its cost taxonomy (fees, SLB, execution) maps directly onto components of our constraint index. Practitioner paper (not peer-reviewed) — cite for institutional colour and the 2× benchmark, not for identification.

---

## What Batch 3 adds to the project
The Indian evidence tells us three things we can bank on: (1) the futures basis in India is **persistently negative and asymmetric** because the short side is constrained (Nandan; Aggarwal) — so our sign predictions are grounded; (2) **PEAD is present and Fama-MacBeth works on Indian data** (Harshita et al.) — our Ch 2/Ch 5 measures are viable; (3) Indian no-arbitrage bands are **~2× developed-market width** (Slivka) — a concrete magnitude to validate our estimates against, and a reminder that the *level* of frictions is high, so the *variation* we exploit (ban on/off, reform dates) sits on top of an already-wide band. Also: efficiency was **improving pre-2015** (Nandan), so the retail-era + reform sample is the right window and a regime-aware design is warranted.

---
**Progress:** Batches 1–3 done (theory spine, methods, India evidence). **Remaining:** Batch 4 — retail/behavioural (12 SEBI loss study, 13 Kumar, 14 lottery-India, 15a/b Barber-Odean) for the policy chapter; Batch 5 — primary regulatory sources (16, 17 SEBI circulars, 18 NSE MWPL rules), read for exact rules/dates; plus an OCR pass on #1 Shleifer-Vishny to upgrade Batch-1 from the actual text.
