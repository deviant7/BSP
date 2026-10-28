# Reading Notes — Batch 5: Regulatory primary sources (institutional-detail tier)

Covers references 16–18, read directly from the SEBI circulars. These give the **exact rules and dates** our identification depends on. Everything below is quotable primary-source fact.

---

## 16. SEBI Circular 2024/132 (1 Oct 2024) — "Measures to Strengthen Equity Index Derivatives Framework"

Six measures, with exact effective dates (from the circular's own applicability table):

| Measure | Effective |
|---|---|
| Contract size for index derivatives raised to ₹15–20 lakh (was ₹5–10 lakh, last set 2015) — new contracts | **20 Nov 2024** |
| Rationalisation of weekly index products → only **one benchmark index weekly expiry per exchange** | **20 Nov 2024** |
| Additional **2% ELM** on short options on expiry day | **20 Nov 2024** |
| **Upfront collection of option premium** from buyers | **1 Feb 2025** |
| **Removal of calendar-spread margin benefit** on expiry day | **1 Feb 2025** |
| **Intraday monitoring of index position limits** (≥4 random snapshots/day) | **1 Apr 2025** |

Stated rationale: heightened retail participation + expiry-day speculation (holding periods "in minutes"). Four of six measures target expiry-day option activity; one (contract size) restores suitability; one (upfront premium) is risk hygiene.

**For our project.** These are dated, market-wide shocks that mostly hit *index* derivatives and retail speculation — i.e., they're the Project-2-style shocks we treat as *background/policy context*, not our core single-stock identification. But they matter as (a) the retail-purge backdrop and (b) potential confounders to date around in the 2024–25 window.

## 17. SEBI Circular 2025/79 (29 May 2025) — "Enhancing Trading Convenience & Strengthening Risk Monitoring" ⭐⭐ (our identification source)

Stated objectives include, explicitly, **"reduce instances of spurious F&O ban periods in single stocks"** — i.e., SEBI is directly reforming the mechanism our thesis studies. Key provisions:

**(a) FutEq Open Interest (5.1) — already implemented by May 2025.** OI now measured at **portfolio level as net delta-adjusted open positions** across futures + options per underlying (long future = +1×notional; option delta 0..±1). Market-wide FutEq OI = gross sum of net FutEq across all UCCs. → OI is now a *delta-weighted* quantity, not raw notional.

**(b) New MWPL definition (5.2) — effective 1 Oct 2025. THE identification variable.**
- Old (per Dec 2024 Master Circular): MWPL = **20% of free-float** shares.
- New: **MWPL = lower of {15% of free float, 65 × Average Daily Delivery Value (ADDV) across CCs}, with a floor of 10% of free float.**
- **Recalculated every 3 months on rolling 3-month ADDV.**
- Ban trigger unchanged in spirit: market-wide **FutEq OI > 95% of MWPL** (tested EOD; plus intraday checks from Nov 2025).
- SEBI's stated reason: "tying MWPL to cash-market delivery volume will **reduce potential manipulation and better align derivatives risk with underlying cash-market liquidity.**"

**(c) Ban-period rule (5.3) — 1 Oct 2025.** After a scrip enters the ban, any trading must **reduce end-of-day FutEq delta** (toward 0); passive increases from price moves are not breaches; a sign flip is not acceptable "reduction." (This is the "risk-reducing trades allowed" relaxation, made precise in delta terms.)

**(d) Other dated shocks:** intraday MWPL monitoring for single stocks **3 Nov 2025**; index-futures position limits **1 Jul 2025**; index-options limits glide path 1 Jul–5 Dec 2025, normal from **6 Dec 2025**; pre-open session for derivatives **6 Dec 2025**; non-benchmark index eligibility (≥14 constituents, top weight ≤20%, top-3 ≤45%) **3 Nov 2025**; individual entity single-stock limits recalibrated to new MWPL (Client 10%, Pro 20%, Pro+Client/FPI-I/MF 30%) **1 Oct 2025**.

**Why this is the crux of our identification (updates the proposal — read carefully):**
1. **The denominator instrument is now delivery-value-linked and quarterly.** From 1 Oct 2025, whether a stock is in-ban depends on **65× rolling 3-month ADDV** (when that binds below 15% free float). ADDV is *trailing cash-market delivery* — it moves for reasons unrelated to *today's* derivative speculation, and it's **reset only quarterly**. That is a cleaner, more defensible instrument for ban status than the old pure-free-float rule. (Note: our earlier note/proposal said "65× cash *volume*"; the precise term is **65× Average Daily Delivery *Value* (ADDV)** — delivery, not turnover — and there is a **10%-free-float floor**. Update the project doc's identification + data sections accordingly.)
2. **Three dated, mechanical regime shifts in constraint intensity:** the OI *measure* changed (notional → FutEq delta, pre-Oct 2025), the MWPL *formula* changed (1 Oct 2025), and the ban *rule* relaxed (1 Oct 2025) — a clean pre/post design, tailor-made for the Ters-Urban TVECM event-study.
3. **A data-construction consequence:** to reconstruct MWPL utilisation across the whole sample we must compute both the old (20% free float) and new (min{15% FF, 65×ADDV}, floor 10% FF) formulas, and switch at 1 Oct 2025 — and we now need **ADDV** (from the delivery/MTO files) and **FutEq/delta** (needs option deltas → implied vols from settlement prices) for the post-period. Flag for the Stage-I pipeline.

## 18. NSE — MWPL / F&O ban methodology (exchange rules)
Supplementary to the SEBI circulars: NSE operationalises the ban (95% entry; **release when OI falls below 80%**), publishes the **daily securities-in-ban list** and per-stock **MWPL / %-utilisation** files, and specifies the historical MWPL computation (20% free float, or 30× prior-month average trading quantity, pre-reform). Use NSE as the source for the *daily observable* ban/MWPL panel; use the SEBI circulars for the *rules and dates*. (Fully readable; extract exact file formats during the Stage-I data build.)

---

## What Batch 5 locks in
We now have the exact, dated, mechanical variation our causal design runs on: the ban trigger (95% of MWPL, release <80%), the pre-reform MWPL (20% free float or 30× prior-month volume), and the post-1-Oct-2025 MWPL (min{15% FF, 65×ADDV}, floor 10% FF, quarterly reset), plus the FutEq/delta OI redefinition and the ban-period delta-reduction rule. The single most important upgrade vs. the proposal: the denominator instrument is **delivery-value-based and quarterly-reset**, which is *stronger* than the free-float-only story — and the precise term is **ADDV**, with a 10%-floor. Recommend updating the project document's §2.4 (identification) and §2.5 (data) to reflect ADDV, the floor, the quarterly reset, and the FutEq redefinition.

---
## Literature review — COMPLETE (Batches 1–5)
All 21 references read: theory spine (1–3), methods (4, 6, 7a–c), India evidence (8–11), retail/behavioural (12–15), primary sources (16–18). Shleifer-Vishny (#1) recovered via OCR and confirms the Batch-1 note. Next natural step: fold the ADDV/FutEq refinements into the project document, and turn these notes into the thesis's Literature Review + Institutional Background chapters.
