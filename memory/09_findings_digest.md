# 09 — Findings digest (written 7 Nov 2026, end of the write-up stage)

One place with every result, its number, its caveat and how it was interpreted. Sources: `analysis/output/*.txt`,
`docs/14_results.md`, `docs/15_band_estimation.md`, `docs/16_constraint_index.md`. PAP = `plan/pre_analysis_plan_v1.md`
(frozen `pap-v1` 85dac3a; §11 log C1-C17 + §11.2 exploratory). All units bp unless stated.

## Primary family (Holm 5%)
| H | Pre-specified statistic | Result | Holm p | Notes |
|---|---|---|---|---|
| H8 trading | Ban coef. on log(1+fut contracts), [0.80,0.95), stock-bin + date FE | -2.00 (0.11); cash +0.073; delivery +0.041 | 7.4e-41 | Identity R=(dOI+V)/V: mean 0.42 (fails pooled). By enforcement: to 22 Mar 2020 median 0.871; 23 Mar 2020-Sep 2025 0.011; Oct-7 Dec 2025 0.193; from 8 Dec 2025 0.357. Futures effect -0.97 (EoD era) vs -2.72 (intraday era) |
| H3 costs | mean d q80, 2024+2026, stock-clustered | +6.96 (0.61), p 1.8e-24; 2023 -2.12, 2024 +6.42, 2026 +7.44 | 5.5e-24 | Placebo sd 7.4; ranks 0.10/0.067; width and q80-median not unusual → common level shift; Kolari-Pynnonen |
| H6 F&O entry/exit | Bonferroni of 4 | entry delay -0.109 (0.023) p 1.3e-6; entry drift -0.040 (opposite); exit delay +0.053 p 0.09; exit drift +0.014 | 1.0e-5 | SA -0.063; flat leads; selection on growth caveat |
| H7 one-sided | IU p | delta_up -0.089 (0.037), delta_lo +0.081 (0.030), p 1 | 1 | Opposite sign; liquid days stronger; EoD era up +0.016 lo +0.126; intraday era up -0.201 lo -0.120; first 0-4 calendar days of spell -0.163 vs -0.008 later; **IV (x_(t-2)) 7 Nov: up -0.190 (0.077), lo +0.088 (0.015) → not noise** |

Post-hoc reading (labelled): blocked new futures demand at ban start (model P5/B2) removes the pressure that made futures
rich. Build-up split shows the in-ban fall for both long and short build-up, so the reading is only partial.

## Secondary (unadjusted)
- **Level effect** (C7): 889 matched entries; mean -6.3 (median -7.8); C<=0 (30) +8.4 (10.9), C>0 -6.8 (1.8), diff -15.2,
  p 0.083; median split -5.8 p 0.025; slope -4.8 p 0.0014. Recovers ~day 7. Same-day controls: -4.0 (2.0), gradient n.s.
  Imbalance: treated 10 bp lower on day -1, dip on day -1. Exploratory: baseline -10..-2 → -11.3; gap-adjusted -9.2, slope
  -3.5. Build-up: long -7.9, short -5.5, closing +8.4 (n 30). Post-reform 19 events -2.8.
- **Density** (C8): transition population; CJM log ratio -0.05, p 0.86; robust; binned McCrary +0.31 is bandwidth bias
  (rises with h); cluster-boot se of CJM 0.29. Utilisation accelerates near 95%; crossing share 7% at 0.85 → ~50% at 0.93-0.95.
- **RD** (C9): sharp (99.7% vs 0.06%); futures -1.53, R -0.66, delivery +0.051, cash n.s.; basis -12.9 p 0.02 but crossing
  day already -11.3 (p 0.048), same-day change -2.8 n.s.; placebo 0.90 basis +24 at degenerate h.
- **Hysteresis** (C10): +0.4 (0.8) p 0.64 with 5 lags; -14.1 without lags; close-based +3.2 (VWAP vs close discrepancy).
- **H9** (C11): A: U share 0.20 → 0.27; slope +0.079 (0.038) p 0.019; step near 0.75; L and level flat with date FE. B:
  first stage +0.28; U +0.061 p 0.11; level +4.8; ban +0.023. C (resets): n.s.
- **H2** (C12): ban x bad +0.7% (3.4) p 0.59; pre-EA basis outside bans bad - good -2.0 (1.1) p 0.04 (Saurav et al.
  direction); cash-only vs F&O: bad -0.67%, good +2.40% (under-reaction both ways).
- **H1** (C13): F&O index +3.5 bp/sd on band width (p 0.002), size +2.5; persistence wrong sign (noise); no within-stock
  effect; SLB scarcity wrong sign (SLB activity = borrowing demand).
- **H4** (C14): lagged flow -17.5 (14.2) p 0.11; FD -20.6 (6.8); pre-2023 -26.0; post +17.1; same-month +4.5 (chasing).
- **H5** (C15): VW short leg G3-G1 +0.04% p 0.57; EW short -0.49%, long +0.46% (symmetric small-stock); momentum short
  -0.51% (0.22) fits.

## Band chapter (C16)
Pooled SETAR (473,110 non-ban obs): gL -34.5 [-37.2, -32.2], gU +23.9 [+20.3, +26.1]; slopes -0.084/-0.468/-0.809;
linearity sup-F 7,471 (boot crit 30.7). BIC: SETAR 3,005,493 < LSTAR 3,005,545 < ESTAR 3,008,092 < linear 3,034,394.
**Noise**: IV slopes -0.121/-0.192/-0.141 → daily reversion mostly noise; asymmetry in speeds not robust. Period-demeaned
thresholds: -39.1/+23.8, -30.9/+18.9, -31.5/+23.1, -31.5/+28.9; slope above upper edge -0.77, -0.55, -0.20, -0.15. States:
lower edge wider far from expiry (-40 vs -28); high utilisation gU 19.8 vs 25.9. STR: omega +0.225 (0.053), days to expiry
+0.221 above 7 days, AUM -0.077. Per-stock (258): median -26.4/+16.5, width 40.9; unrelated to friction index. Cost band:
open+hold 27.1/27.3/28.0/31.0 (25-38 with brokerage range); roll 4.0/4.3/5.0/8.0; level gU +27.5/+23.6/+21.5/+24.1; p90
+27.5/+24.7/+24.2/+29.7.

## Constraint index (C17)
All NSE stocks, 80,042 stock-quarters (3,310 stocks); loadings no_short .49, slb .45, cs .43, lamihud .49, ivol .37; 53%;
stable by year; persistence 0.90. Delay +0.058 (t 20.8), within stock +0.032; |BHAR| +0.023; bad -0.008, good +0.001; F&O
band width -6.4 (opposite → use H1 F&O index for bands). File `data/processed/constraint_index_q.csv.gz`.

## Facts verified on 7 Nov (primary sources)
In-ban rule from 1 Oct 2025 looser (SEBI 2025/79 Table 2); package not a relaxation. Short selling: F&O securities only
(SEBI 5 Jan 2024, references/25). SLB: also liquid non-F&O since Jul 2013 (secondary + SLB data). ADDV in quantity.
Pre-2025 MWPL 20% FF (data reproduce 85 stocks). Cost components: STT physical settlement 0.1% (NSE 1/2018), stamp duty
Jul 2020, NSE charges Oct 2024.

## Interpretation in one paragraph (as written in the thesis)
Position limits bind hard on trading; their price effect is not the reduce-only arbitrage channel but appears at ban start
(blocked new demand) and fades within a week; enforcement matters (intraday checks). Short-sale access speeds price
adjustment (F&O entry, constraint index) but evidence on overpricing/bad-news drift is mixed. Costs shape a wide asymmetric
band; edges do not move one-for-one with STT; new-entry cost in the outer tail, roll cost small. Capital: weak traces in
the predicted direction. Ten secondary tests unadjusted: read as a pattern.

## Write-ups (7 Nov)
- `thesis/` (main.tex + ch1-ch8 + appA plan + appB data + model PDF appendix + references) → `BSP_Thesis_Draft_Nov2026.pdf`
  (52 pp). Internal draft, guide-style language.
- `progress_report_src/first_results_nov2026.tex` → `BSP_First_Results_Nov2026.pdf` (5 pp, guide-facing, NOT SENT): corrects
  the October report's SLB wording and counts (results dated from first dissemination); asks two questions (extend model for
  blocked new demand? take observed-state STR further?).
- Figures: `analysis/thesis_figures.py` → reports/figs/fig_level_profile, fig_h9_tails, fig_band_years, fig_ban_R.
