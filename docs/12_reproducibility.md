# 12. Reproducibility

Every number in the project can be rebuilt from public sources with the scripts in this repository. This page lists the
files that make up the project, the software needed and the exact sequence of commands.

## 12.1 Repository layout (final-form files)

| Path | Content |
|---|---|
| `docs/` | This documentation |
| `BSP_Model_C_Constrained_Arbitrage_India.pdf`, `models_src/modelC/` | Theoretical framework (PDF, LaTeX source, `verify_modelC.py` numerical checks and their output, figures) |
| `plan/pre_analysis_plan_v1.md` | The frozen test plan (git tag `pap-v1`) |
| `data_pipeline/` | Download and build scripts (one per data set), with a README |
| `data/raw/` | Raw downloads (not committed; about 1.2 GB; rebuilt by the download scripts) |
| `data/processed/` | Processed data sets and build reports (committed, except the basis panel, which is rebuilt) |
| `analysis/` | Estimators (`setar.py`), their test on simulated data (`test_setar_simulated.py`), data audit scripts (`audit/`) |
| `reports/figs/`, `reports/tables/` | Treatment-side figures and tables generated from the processed data |
| `references/` | PDFs of the papers and regulatory documents cited, with an index |

## 12.2 Software

- Python 3 with `numpy`, `pandas`, `scipy`, `matplotlib`, `openpyxl`, `pyfixest` (`pip install numpy pandas scipy matplotlib openpyxl pyfixest`).
- `pdftotext` (poppler) for the AMFI lists.
- `curl` (the FRED download falls back to it).
- LaTeX for the PDFs: `texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`.
- Network access to `nsearchives.nseindia.com`, `www.nseindia.com` and `fred.stlouisfed.org`.

All scripts are run with `python3 -I` (isolated mode), from the repository root.

## 12.3 Rebuild sequence

```bash
# 1. downloads (raw data; each step is resumable and skips files already present)
python3 -I data_pipeline/download_nse_mwpl.py data/raw 2010-01-01 2026-10-27
python3 -I data_pipeline/download_nse_prices.py data/raw/prices 2015-01-01 2026-10-27 3
python3 -I data_pipeline/download_rates_corpactions.py data/raw 2014 2026
python3 -I data_pipeline/download_results_filings.py data/raw 2014 2026
python3 -I data_pipeline/download_results_filings.py data/raw 2025 2026 integrated
python3 -I data_pipeline/download_results_filings.py data/raw 2014 2026 boardmeetings
python3 -I data_pipeline/download_results_filings.py data/raw 2014 2026 resultupdates
python3 -I data_pipeline/download_index_close.py data/raw/indices/nifty50_daily.csv 2015-01-01 2026-10-27

# 2. builds (order matters: announcements need the panel and the membership file)
python3 -I data_pipeline/build_mwpl_panel.py data/raw data/processed
python3 -I data_pipeline/describe_bans.py data/processed reports/figs
python3 -I data_pipeline/build_fno_events.py data/raw data/processed
python3 -I data_pipeline/build_announcements.py data/raw data/processed
python3 -I data_pipeline/build_basis.py data/raw data/processed
python3 -I data_pipeline/build_returns.py data/raw data/processed
python3 -I data_pipeline/build_amfi_mcap.py data/raw data/processed
python3 -I data_pipeline/build_mcap.py data/processed
python3 -I data_pipeline/report_figs.py data/processed reports/figs
python3 -I data_pipeline/report_tables.py data/processed reports/tables

# 3. tests (frozen plan) and their checks
python3 -I analysis/test_inference.py
python3 -I analysis/samples.py
python3 -I analysis/h8_trading.py
python3 -I analysis/h7_onesided.py
python3 -I analysis/h7_diagnostics.py
python3 -I analysis/h3_costs.py
python3 -I analysis/h6_outcomes.py
python3 -I analysis/h6_fno.py

# 4. other checks
python3 -I analysis/test_setar_simulated.py
python3 -I analysis/audit/audit_coverage.py data/raw
python3 -I analysis/audit/audit_prices.py data/raw
python3 -I analysis/audit/audit_oi_alignment.py data/raw
(cd models_src/modelC && python3 verify_modelC.py)
```

Approximate run times on one machine: the open-interest and ban files about 40 minutes; the price files about
2.5 hours; each event-list download 10 to 30 minutes; each build a few minutes.

## 12.4 Outputs and their reports

| Output | Rows (current build) | Report |
|---|---|---|
| `mwpl_oi_panel.csv.gz` | 752,037 stock-days, 476 symbols, 4,120 trading days | `build_report.txt` |
| `ban_days.csv.gz` | 11,765 stock-days (2010 to 2026) | `build_report.txt` |
| `ban_spells.csv.gz` | 2,181 spells (2010 to 2026) | `descriptives.txt` |
| `fno_membership.csv.gz` | 534,712 stock-days, 374 symbols | `fno_events_report.txt` |
| `fno_events.csv` | 239 entries, 171 exits | `fno_events_report.txt` |
| `announcements.csv.gz` | one row per stock and quarter | `announcements_report.txt` |
| `basis_panel.csv.gz` | 1,066,167 stock-day-contract rows | `basis_report.txt` |
| `nifty_futures.csv.gz`, `nifty50_daily.csv` | validation series | `basis_report.txt` |
| `returns_daily.csv.gz` (not committed) | 5,331,373 stock-days, 3,723 stocks | `returns_report.txt` |
| `amfi_mcap.csv.gz` | 18 half-years, about 3,400 to 5,400 companies each | `amfi_mcap_report.txt` |
| `mcap_daily.csv.gz` (not committed) | daily market cap, 94.7% of cash stock-days | `mcap_report.txt` |

## 12.5 Things that change if the data are rebuilt later

- NSE occasionally revises or removes archive files and changes its web endpoints. The build reports record the counts
  of the current build, so a rebuild can be compared line by line.
- The interest-rate series is extended monthly; a later rebuild replaces the carried-forward rate for October 2026 with
  the published value (`r_filled` becomes False).
- Event lists (corporate actions, results, board meetings) can gain late filings.
