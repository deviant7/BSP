# 05. Next steps (detailed work plan)

Order is by dependency, not by date (no timelines). Everything must follow the frozen plan
`plan/pre_analysis_plan_v1.md`; read `07_test_plan.md` for interpretation notes. Any departure, however small, is logged
in PAP §11 with date and reason before results are reported, and the original specification is always reported too.

## Step 0. Session start checks (every new session)

1. `git status`, `git log --oneline -5`, `git ls-remote --tags origin` (is `pap-v1` on GitHub? if not, remind the user:
   `git tag -a pap-v1 85dac3a -m "Pre-analysis plan v1 frozen" && git push origin pap-v1`, or create it on GitHub as a
   release tag targeting 85dac3a).
2. `ls data/raw data/processed`: if `data/raw` or `basis_panel.csv.gz` is missing, rebuild (`docs/12_reproducibility.md`;
   the price download takes about 2.5 hours and is resumable, so run it in the background).
3. `cd models_src/modelC && python3 verify_modelC.py` (ALL PASS) and `python3 -I analysis/test_setar_simulated.py`
   (known TAR -29.1/+15.2; model basis -10/0) as smoke tests.
4. Ask the user only what cannot be found in the repo (e.g. news from the guide).

## Step 1. Shared analysis infrastructure (before any test)

Create `analysis/samples.py` (build once, reuse everywhere) and write a counts report (`analysis/output/sample_report.txt`).

1. **Contract choice:** from `basis_panel.csv.gz`, for each stock-day take k = 0 unless the near contract has 3 or fewer
   **trading** days to expiry (count with the trading calendar = dates of `mwpl_oi_panel`), then take k = 1.
2. **Liquidity:** `n_contracts >= 5` (n_contracts is the number of contracts for both formats; UDiFF counts were moved from
   `qty` in the builder).
3. **Exclusions:** `pv > 0` (dividend within contract life), `event_in_life`, first 20 trading days after an F&O entry
   (`fno_events.csv`), `F_vwap` missing (lot failure). Keep `r_filled` rows but flag for a robustness drop.
4. **Changes:** Delta m_t = m_t - m_(t-1) only when both days are in the sample, consecutive trading days, and the **same
   expiry** (never across a roll). Lagged level m_(t-1) from the same contract.
5. **Winsorise** m at 1% and 99% within each calendar year for the main estimates; keep the raw value for robustness.
6. **Treatment merge (now allowed):** Ban_it = stock in `ban_days.csv.gz` on day t (any source; robustness: drop
   `source == imputed`). omega_(i,t-1) = `util` (before 1 Oct 2025) or `util_futeq` (from 1 Oct 2025) on day t-1.
   Spell variables from `ban_spells.csv.gz`: day of spell, spell length, and "an expiry date has passed since the spell
   start" (expiry dates from the basis panel).
7. **Inference helpers** (`analysis/inference.py`): two-way fixed effects (stock and date) by alternating demeaning;
   two-way clustered standard errors (Cameron, Gelbach and Miller: V = V_stock + V_date - V_stock-and-date);
   wild-cluster bootstrap (Rademacher or Webb weights) for event studies with few clusters; Holm correction.
   `pyfixest` is installable from PyPI in the container (checked 5 Nov 2026: pyfixest 0.60.0 downloads); cross-check the hand-written code against
   it on one regression. Write unit tests on simulated data with known coefficients.

## Step 2. Primary tests (order: H8, H7, H3, H6)

H8 first: it is the mechanical check that bans bind and that the ban timing is right; if it fails, the ban results need
re-thinking before anything else.

### H8: trading moves out of futures (pre-October 2025 bans)
- Unit: stock-day, F&O stocks, 2015 to 30 Sep 2025, excluding expiry days (open interest drops mechanically at expiry).
- Variables: near + next contracts: Delta OI and volume **in contracts**. Verified 5 Nov 2026: `oi` and `chg_oi` in
  the basis panel are in **shares** in both formats (oi / lot_used is an integer for 99.7% of legacy and 99.3% of UDiFF
  rows), so divide by `lot_used` to get contracts. Futures volume in contracts (`n_contracts`); cash volume `S_qty`; delivery share
  from `data/raw/prices/deliv` (deliverable / traded).
- Test 1: distribution of (Delta OI + volume) / volume on ban days; prediction about 0 (every trade closes for both sides).
- Test 2: within-stock comparison of ban days with the same stock's non-ban days in the same utilisation bin (e.g. bins of
  0.05 in omega_(t-1) from 0.80 to 1.00), regression of log futures volume, log cash volume, delivery share on Ban with
  stock-by-bin and date fixed effects; two-way clustered SE.
- Falsifier: (Delta OI + volume) not close to 0, or futures activity not lower.
- Report post-October 2025 bans separately and descriptively (delta-based rule allows cross-instrument offsets; the
  identity may fail by design).

### H7: one-sided correction
- Specification in `07_test_plan.md` and PAP §5. Regimes from the stock's own 20th/80th percentiles of m on non-ban days;
  mu_i = stock median on non-ban days; regressors (m_(t-1) - mu_i) x regime x {1, Ban}; stock and date FE; two-way SE.
- Prediction: delta_upper > 0, delta_lower <= 0; with the expiry-in-spell interaction, delta_lower moves toward 0 after an
  expiry inside the spell. Falsifier: delta_upper <= 0 or delta_upper = delta_lower (test the difference).
- Robustness (all pre-specified): thresholds from a per-stock 3-regime threshold model on non-ban days; fixed +/-25 bp
  around the median; state-dependent thresholds (thresholds depending on lagged OI/MWPL); unwinsorised; drop imputed ban
  days; drop `r_filled`; close-based basis; relative implied repo.
- Report pre- and post-October 2025 separately as well as pooled (post has 44 spells: low power, stated in advance).

### H3: costs set the band edges
- Dates: 1 Apr 2023, 1 Oct 2024, 1 Apr 2026. Windows +/-40 trading days. All F&O stocks.
- Outcome per stock and window: 80th and 20th percentiles of m (clean sample), and threshold-model edges.
- Prediction: upper edge rises after each date; ordering of the rises 2026 > 2024 > 2023 (cost changes: +0.03, +0.0075,
  +0.0025 percentage points of STT on the futures sale; plus whatever share of the round trip this represents; compute the
  implied change in c_plus in bp: 0.0025% = 0.25 bp, 0.0075% = 0.75 bp, 0.03% = 3 bp per side).
- **Important:** these cost changes are small (0.25 to 3 bp) relative to band widths of tens of bp; power will be low;
  the 2023 date is confounded with the debt-fund tax change (reported, not claimed). State this when reporting.
- Inference: paired stock-level differences, clustered by stock; wild bootstrap; placebo dates (e.g. index-only reform
  dates of 20 Nov 2024 and 1 Feb 2025, and random dates).

### H6: short-sale access (F&O entry and eligibility exit)
Needs inputs not yet built:
- **Daily returns for the cash universe** (all EQ/BE/BZ stocks): from `data/raw/prices/cash` close and previous close.
  Verify how NSE's `PREVCLOSE` treats splits and bonuses on ex-dates (if adjusted, return = close / prevclose - 1 is
  clean; otherwise adjust with corporate actions). Check a known split (e.g. a 1:5 split) before using.
- **Market capitalisation** for size matching and size portfolios: not in the bhavcopy. Options: NSE market-cap archive
  files, or shares outstanding from the XBRL filings, or free float = MWPL/0.20 for F&O stocks only (not enough for
  controls). Find a source first; if none is free, match on traded value and price level and log the deviation.
- **Market return** for price delay: equal-weighted cash-universe return, or Nifty 50 / a broad index file.
- Outcomes: price delay (weekly returns, 52-week windows), VR(5), BHAR[+2,+64] after bad news (EAR in bottom tercile or
  quintile; pre-specify which in §11 before running if the PAP is silent).
- Design: Callaway and Sant'Anna staggered DiD for entries; separately for eligibility exits (158 usable); controls
  not-yet-treated and never-treated cash stocks matched on size, turnover, volatility over the 6 months before. Python
  options: `csdid` / `differences` packages, or implement group-time ATTs directly. Sun and Abraham as a check.
- Batches (45 entries on 29 Nov 2024; 34 exits on 28 Jun 2019) dominate; report with and without them.

### Multiple testing
Holm across the four primary tests at 5% (one p-value per hypothesis; decide in §11 before running which statistic is
the hypothesis's p-value where several exist, e.g. delta_upper - delta_lower for H7, the mean (Delta OI + volume) / volume
or the futures-volume coefficient for H8).

## Step 3. Secondary tests (labelled exploratory)

Level effect (stacked ban-entry event study with near-miss controls, split by pre-ban Delta OI / volume); H9 (basis
quantiles by utilisation bins; 1 Oct 2025 intensity DiD); RD at 95% after the Cattaneo-Jansson-Ma density test (density
test is treatment-side and can be done at any time); hysteresis; H2 (180 ban-day announcements); H1 (friction index);
H4 (needs AMFI); H5 (anomaly double sorts; needs returns and characteristics).

## Step 4. Inputs still to collect (blind-safe, can run in parallel)

| Input | Use | Notes |
|---|---|---|
| AMFI monthly arbitrage-fund AUM and net flows (mid-2018 on) | H4 | amfiindia.com monthly reports; categorised from 2018 |
| EPS from XBRL filings | SUE (secondary surprise) | links in `announcements.csv.gz` (`xbrl_standalone`, `xbrl_consolidated`); legacy XML to Mar 2025, Integrated Filing XML after |
| SLB bhavcopy | Friction index (H1) | NSE SLB segment archives |
| Market capitalisation / shares outstanding | H6 matching, size portfolios, H5 | source to be found |
| Index dividends | Sharper Nifty validation | optional |
| BSE results for BSE-only listings (MCX, Abbott, Nestle before 2023) | Close the last 1% gap in announcements | optional |
| Announcement-date-aware dividend adjustment | Lets dividend contracts back into the sample | optional robustness |

## Step 5. Writing and reporting

1. `docs/14_results.md` (final-form results page): every pre-specified test, original specification first, nulls
   included.
2. Thesis chapters in LaTeX (structure in 01). The literature-review PDF needs its known errors fixed before reuse.
3. Next guide deliverable: one PDF (guide-facing rules), probably "first results". Ask the user before sending anything.
4. With the user's go-ahead only: correct the project document's known errors (short-selling line, 30x leg,
   "relaxations", timeline).

## Step 6. Keep continuity

After each step: update `memory/05_session_log.md`, the relevant `handoff/` files (at least 04, 05, 09, CHANGELOG),
`docs/` if something final changed, commit, push.
