#!/usr/bin/env bash
# Full reproduction run used in the project audit: rebuild the analysis caches from the processed data, rerun every
# analysis script in dependency order, and log each step. Usage (from the repo root): bash analysis/audit/rerun_all.sh LOGDIR
set -u
LOG=${1:-/tmp/rerun_logs}
mkdir -p "$LOG"
rm -f data/processed/cache/*.pkl
run() { echo "== $1 $(date +%T)"; python3 -I "$@" > "$LOG/$(basename "$1" .py).log" 2>&1; echo "   exit $? $(date +%T)"; }
run analysis/test_inference.py
run analysis/test_setar_simulated.py
run analysis/test_cs_att.py
run analysis/test_level_effect.py
run analysis/samples.py
run analysis/h8_trading.py
run analysis/h7_onesided.py
run analysis/h7_diagnostics.py
run analysis/h3_costs.py
run analysis/h6_outcomes.py
run analysis/h6_fno.py
run analysis/level_effect.py
run analysis/level_effect_buildup.py
run analysis/density_test.py
run analysis/rd_95.py
run analysis/hysteresis.py
run analysis/h9_regime.py
run analysis/h2_badnews.py
run analysis/h1_frictions.py
run analysis/h4_capital.py
run analysis/h5_anomalies.py
run analysis/h7_iv.py
run analysis/band_estimation.py
run analysis/band_exploratory.py
run analysis/band_costs.py
run analysis/constraint_index.py
run analysis/audit/index_size_check.py
run analysis/spurious_bans.py
run analysis/placebos.py
run analysis/covid_halving.py
run analysis/thesis_figures.py
echo "ALL DONE $(date +%T)"
