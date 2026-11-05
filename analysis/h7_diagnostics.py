"""EXPLORATORY diagnostics for H7 (added 5 Nov 2026 AFTER the pre-specified H7 result was seen; not part of the frozen plan).
Purpose: understand why, in bans, upward deviations of the basis revert faster and downward deviations slower (the
opposite of the model's one-sided-correction prediction). Candidate explanations examined:
  (1) measurement noise from thin trading (errors-in-variables makes reversion look stronger);
  (2) which leg moves: futures (e.g. liquidation of long futures) or cash (e.g. spillover of demand to the stock);
  (3) differences across the three enforcement regimes of the ban rule (end-of-day checks before 23 Mar 2020; peak
      intraday checks 23 Mar 2020 to Sep 2025; end-of-day FutEq checks from 1 Oct 2025).
Outputs analysis/output/h7_diagnostics.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, PROC, ROOT
from h7_onesided import thresholds, design, estimate, fmt, add_postexp, BP

OUT = os.path.join(ROOT, "analysis", "output")


def legs(S):
    """Same-contract daily log changes of the futures VWAP and the cash VWAP (net of dividends: none in the sample)."""
    days, pos = calendar()
    X = pd.read_csv(os.path.join(PROC, "basis_panel.csv.gz"), usecols=["date", "symbol", "expiry", "F_vwap", "S_vwap",
                                                                         "n_contracts"], parse_dates=["date", "expiry"])
    X["i"] = X["date"].map(pos)
    L = X.copy(); L["i"] += 1
    L = L.rename(columns={"F_vwap": "F_lag", "S_vwap": "S_lag", "n_contracts": "n_lag"})[["symbol", "expiry", "i", "F_lag", "S_lag", "n_lag"]]
    X = X.merge(L, on=["symbol", "expiry", "i"], how="left")
    X["dlnF"] = np.log(X["F_vwap"] / X["F_lag"]) * BP
    X["dlnS"] = np.log(X["S_vwap"] / X["S_lag"]) * BP
    return S.merge(X[["symbol", "expiry", "i", "dlnF", "dlnS", "n_lag"]], on=["symbol", "expiry", "i"], how="left")


def main():
    S = add_postexp(basis_sample())
    S = legs(S)
    T = thresholds(S, "m", "m_lag", "dm", "pct")
    r = ["EXPLORATORY diagnostics for H7 (not pre-specified). Units bp.", ""]

    # (1) thin trading: restrict to observations where the chosen contract traded at least N contracts on t and t-1
    for N in (50, 200, 1000):
        Tm = T[(T["n_contracts"] >= N) & (T["n_lag"] >= N)]
        r.append(fmt(f"(1) both days >= {N} contracts", estimate(design(Tm, "m_lag", "dm"))))
    # (3) enforcement regimes
    for lab, a, z in [("(3a) end-of-day checks, to 22 Mar 2020", "2015-01-01", "2020-03-23"),
                      ("(3b) peak-intraday checks, 23 Mar 2020 to 30 Sep 2025", "2020-03-23", "2025-10-01")]:
        Tm = T[(T["date"] >= a) & (T["date"] < z)]
        r.append(fmt(lab, estimate(design(Tm, "m_lag", "dm"))))

    # (2) which leg moves: regress each leg's daily change on the same regime regressors
    D = design(T, "m_lag", "dm")
    D = D.dropna(subset=["dlnF", "dlnS"])
    for leg in ("dlnF", "dlnS"):
        D2 = D.copy(); D2["y"] = D2[leg]
        r.append(fmt(f"(2) dependent variable = {leg} (same regressors; sum of the two legs' coefficients = the dm coefficient)",
                     estimate(D2)))
    # (2b) average leg moves on ban days by regime of m_(t-1), against non-ban days in the same regime
    reg = np.where(D["x_up"] != 0, "up", np.where(D["x_lo"] != 0, "lo", "mid"))
    D["regime"] = reg
    tab = D.groupby(["regime", "ban"]).agg(n=("y", "size"), dm=("y", "mean"), dlnF=("dlnF", "mean"), dlnS=("dlnS", "mean"),
                                           x=("x_up", lambda s: np.nan)).drop(columns="x")
    r += ["", "(2b) mean daily changes by regime of m_(t-1) and ban status (bp):", tab.round(2).to_string()]
    # (4) day of spell
    sp = pd.read_csv(os.path.join(PROC, "ban_spells.csv.gz"), parse_dates=["start", "end"])
    b = D[D["ban"]][["symbol", "date"]].reset_index().merge(sp, on="symbol")
    b = b[(b["date"] >= b["start"]) & (b["date"] <= b["end"])]
    D["dos"] = np.nan
    D.loc[b["index"].values, "dos"] = (b["date"] - b["start"]).dt.days.values
    D["first3"] = D["ban"] & (D["dos"] <= 4)
    r.append("\n(4) ban observations by calendar days since spell start: <=4 days " + str(int(D["first3"].sum())) +
             ", later " + str(int((D["ban"] & ~D["first3"]).sum())))
    for lab, msk in (("first days of spell (<=4 calendar days)", ~(D["ban"] & ~D["first3"])),
                     ("later days of spell", ~D["first3"])):
        r.append(fmt(f"(4) ban days restricted to {lab}", estimate(D[msk])))
    txt = "\n".join(r)
    open(os.path.join(OUT, "h7_diagnostics.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
