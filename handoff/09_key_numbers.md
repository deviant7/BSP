# 09. Key numbers (current build, 5 Nov 2026)

Every number below reproduces from the build reports in `data/processed/`. If a rebuild changes a number, update it here,
in `docs/11_descriptive_facts.md` and wherever it is quoted. Numbers in the report the guide received (pre-audit) are in
`04_current_state.md` §4.3.

## Panel and universe
- MWPL/OI panel: 752,037 stock-days, 476 symbols, 4,120 trading days (1 Feb 2010 to 27 Oct 2026).
- 2015+: 534,892 panel stock-days; F&O membership 534,712 stock-days, 374 symbols, 2,917 trading days; panel vs membership
  agree on 534,538 (99.97%).
- F&O stocks per day: average 183 (2015 to 2026); 154 (2015), 172, 200 (2017), 206, 176, 140 (2020), 163, 196, 187, 185,
  216 (2025), 209 (2026).

## Bans
- 2015 to 2026: **1,788 spells, 9,416 ban stock-days, 141 stocks**; median spell 4 days (mean 5.3, max 31; 6.8% one-day);
  median stock 6 spells; most banned SAIL (76 spells).
- Pre-Oct 2025: 1,744 spells (median 4, mean 5.2). From Oct 2025: 44 spells (median 9, mean 9.3).
- 2010 to 2026: 2,181 spells, 11,765 ban stock-days.
- By year (spells / ban days / stocks): 2015 69/367/16; 2016 136/645/27; 2017 287/1,586/43; 2018 162/810/38; 2019 86/508/23;
  2020 178/756/40; 2021 162/789/26; 2022 100/457/23; 2023 193/942/41; 2024 289/1,656/49; 2025 93/558/37; 2026 33/342/10.
- Rule checks: utilisation > 95% the day before 99.4% of spells (median 1.006); <= 80% on the last ban day 99.7%
  (<= 82%: 99.9%). Flag vs list: 11,753 of 11,764 flags agree; 5 listed but not flagged.
- Non-ban stock-days with omega in (0.90, 0.95]: 2,439 pre-reform, 139 post; (0.95, 1.00]: 961 pre, 37 post.

## MWPL
- MWPL changes: 7,744 stock-day changes; by month Jan 238, Feb 1,485, Mar 134, Apr 229, May 1,612, Jun 100, Jul 258,
  Aug 1,558, Sep 87, Oct 457, Nov 1,529, Dec 57 (quarterly free-float updates).
- COVID halving: 61 stocks halved in files 20 Mar to 27 Mar 2020 (28 on 20 Mar, 13 on 23 Mar, 7, 5, 5, 2; plus 1 on
  29 Apr); 70 restored in the 26 Nov 2020 file.
- 1 Oct 2025: all 208 stocks' MWPL fell; ratio new/old p10 0.500, median 0.729, p90 0.750; 17% at the floor, 48% at 15% FF.
  Rebuild from pre-reform data exact for the 85 stocks at 15% FF; ADDV leg: actual about 6.5% above an NSE-only-delivery
  prediction (BSE deliveries).

## F&O events
- 239 entries, 171 exits (162 eligibility exits; 9 mergers/delistings); usable 233 / 158; 21 renames linked by ISIN.
- By year (entries/exits): 2015 20/3; 2016 16/3; 2017 41/5; 2018 0/11; 2019 0/56; 2020 6/13; 2021 60/0; 2022 2/8; 2023 0/8;
  2024 45/5; 2025 33/48; 2026 16/11.
- Largest batches: 29 Nov 2024 45 entries; 28 Jun 2019 34 exits; 28 Apr 2017 16 entries; 26 Feb 2021 16 entries;
  28 Feb 2025 16 exits; 31 Mar 2017 15 entries; 29 May 2015 14 entries; 27 Sep 2019 12 exits.

## Announcements
- 94,071 events (2014 to Oct 2026); release source: announcement 72,356, filing 17,525, board meeting 4,190.
- Timed release vs board meeting (88,185 with both): same day 90.2%, next day 6.5%, before 0.5%.
- Timing known 95.5% overall; 66.5% released at or after 15:30 (all events, timed); median 42 days after quarter end.
- F&O: 8,594 events on F&O days (timing known 99.0%; announcement 6,844, filing 1,661, board meeting 89); 180 on ban days;
  62% of timed F&O releases after close; median 4 per stock-year.
- Coverage of F&O stocks per quarter: min 97.8% (2023Q2), median 99.1%.
- Old build vs new: 51.5% of 7,910 old F&O events moved earlier (36% by >= 2 days).

## Basis
- Futures rows 1,652,524 (traded 1,450,297); VWAP inside [low, high] 99.77%; legacy lot snapped 2.01%; futures-cash match
  100%; near+next stock-futures rows 1,066,167.
- Dividend events parsed 16,320; non-dividend events 1,991 (0.91% of rows with one in the contract life).
- Near-month usable (>= 5 contracts) 534,628; **clean 503,170: median +1.2 bp, p10 -33.0, p90 +26.2, |m| > 200 bp 0.65%**.
- Yearly (usable near-month) p10/median/p90 bp: 2015 -41.7/-1.3/25.7; 2016 -36.3/1.9/26.9; 2017 -26.7/4.0/26.7;
  2018 -37.4/-1.8/24.0; 2019 -45.7/0.6/26.9; 2020 -45.2/2.1/29.5; 2021 -18.0/9.2/34.4; 2022 -34.3/1.4/29.1;
  2023 -29.1/1.0/24.9; 2024 -28.7/-0.2/24.6; 2025 -29.4/1.0/24.4; 2026 -32.6/0.8/28.5.
- Convergence (median abs basis by days to expiry): (21,35] 16.6; (14,21] 14.7; (7,14] 14.1; (3,7] 13.1; (0,3] 12.8 bp.
- Rows with carried-forward rate: 7,225 (Oct 2026).
- Dividend days: adjusted +9.7 bp vs clean +1.1 bp (unadjusted -48.8): over-correction.

## Theory and estimator checks
- verify_modelC: ALL PASS. Simulated reversion slopes (normal → ban): above p80 -0.182 → -0.130; below p20 -0.116 → -0.163.
  Level effect +4.93 / -3.09 / -10.83 / -26.03 bp for 0 / 1 / 2 / 4 bp/day new demand.
- SETAR: known TAR -30/+15 → -29.1/+15.2; model basis → -10/0.

## Literature numbers often quoted
- Aggarwal (2015): bands +3 / -15 bp (one-second data, 141 stocks, Mar to Aug 2013); MIBOR explains ~18% of PC1.
- Shankar et al. (2015): kappa_L -39 bp, kappa_H -10 bp, band 28 bp (102 stocks, 5-minute, 2007 to 2009).
- Slivka et al. (2011): cost band ~2.47% for JSWSTEEL.
- SEBI (2024): 93% of individual F&O traders lost money FY22 to FY24; over Rs 1.8 lakh crore.
- Arbitrage-fund AUM about Rs 71,106 crore (Apr 2023) → Rs 1,98,981 crore (Oct 2024) (press, from AMFI; to confirm).

## Primary test results (5 Nov 2026; analysis/output/)
- Analysis sample: 486,040 chosen-contract stock-days, 371 stocks; next contract 18.5%; Delta m defined 482,443; ban days
  8,851 (Delta m 8,756); post-reform 49,903 (ban 400).
- H8 (zone omega_(t-1) in [0.80, 0.95), n = 16,270, 5,441 ban days, 167 stocks): log futures contracts -2.0036 (0.1106,
  t -18.11); log cash shares +0.0726 (0.0266); delivery share +0.0410 (0.0045); R -0.573 (0.044). Ban-day R mean 0.424
  (CI 0.340-0.520), median 0.305; non-ban comparison mean 1.019. Before/after 15 Mar 2020 futures effect -0.972 / -2.722.
- H7 main (n 481,772, 360 stocks, 8,662 ban obs): normal slopes up -0.712, mid -0.393, lo -0.204; deltas up -0.089
  (0.037), mid +0.099 (0.062), lo +0.081 (0.030); diff -0.170 (0.046); p_H7 = 1. Spec 2: delta_lo + interaction -0.827 (0.089).
- H3: mean d80 2023 -2.12 (181 stocks), 2024 +6.42 (172), 2026 +7.44 (192); pooled 2024+2026 +6.962 (0.613), p 1.84e-24;
  placebo sd 7.40 (30 dates); ranks 0.667 / 0.100 / 0.067.

## Added 5 Nov 2026
- Returns: 5,331,373 stock-days, 3,723 stocks; factor check 99.6% of 769 ex-dates; 424 inferred missing CAs; 448 jumps.
- AMFI: 18 half-years, ~3,400 (2017H2) to ~5,370 companies; NSE coverage 89–97% by count, 95–99.8% by value.
- Market cap: 94.7% of stock-days; back-cast 3-year test median error 0.3%, 82% within 10%.
- Delay panel: 17,715 stock-years (price >= Rs 5), median D1 0.243; by size quintile 0.364 → 0.189.
- Events with EAR 75,233, BHAR 72,972; winsorised mean BHAR bad −2.7%, good +1.5%.
- H6: entry delay ATT −0.109 (0.023); SA −0.063; entry drift −0.040 (0.018); exit delay +0.053 (0.040); exit drift +0.014.
- Holm: H8 7.4e-41, H3 5.5e-24, H6 1.0e-5, H7 1.
- H8 ban-day R by enforcement regime: median 0.871 / 0.011 / 0.193 / 0.357.
- H7 diagnostics: liquid days δ_up −0.154, δ_lo +0.130; EOD era δ_up +0.016, δ_lo +0.126; intraday era −0.201 / −0.120;
  0 to 4 calendar days after spell start δ_up −0.163, later −0.008.
- H3 placebo pairs: d80 4.6%, width 23.4%, q80−median 27.4%.
