"""EXPLORATORY (added 7 Nov 2026 AFTER the level-effect and RD results were seen; logged in PAP §11.2).

Why: the composition ratio C (change in OI over volume, days -5..-1) cannot tell whether the new positions that push
utilisation over 95% are new longs or new shorts, but the model's sign depends on it (new long demand blocked -> basis
lower in a ban; new short demand blocked -> basis higher). The RD showed the basis is already low on the crossing day.
Indian market practice classifies OI changes with the price change over the same days:
  long build-up  = OI up, price up      (new longs dominate)
  short build-up = OI up, price down    (new shorts dominate)
  short covering = OI down, price up    (closing shorts)
  long unwinding = OI down, price down  (closing longs)
Price change = log change of the cash VWAP from day -6 to day -1. Same events, controls and outcome D as PAP §11.4 C7.
Outputs analysis/output/level_effect_buildup.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
import level_effect as le
from samples import PROC, ROOT
from inference import lincomb


def cash_matrix(D):
    X = pd.read_csv(os.path.join(PROC, "basis_panel.csv.gz"), usecols=["date", "symbol", "k", "S_vwap"], parse_dates=["date"])
    X = X[X["k"] == 0]
    X["i"] = X["date"].map(D["pos"])
    X = X[X["symbol"].isin(D["sid"])]
    S = np.full(D["OM"].shape, np.nan)
    S[X["symbol"].map(D["sid"]).values, X["i"].values] = X["S_vwap"].values
    return S


def main():
    D = le.build()
    E, _ = le.events(D, False)
    Cd = le.candidates(D, False)
    Mi = le.match(E, Cd)
    ks, P = le.paths(D, E, Cd, Mi, "m")
    E["D"] = le.main_stat(E, ks, P)
    S = cash_matrix(D)
    E["ret5"] = [np.log(S[j, i - 1] / S[j, i - 6]) if i >= 6 else np.nan for j, i in zip(E["j"], E["i0"])]
    up = E["ret5"] > 0
    E["grp"] = np.select([(E["C"] > 0) & up, (E["C"] > 0) & ~up, (E["C"] <= 0) & up, (E["C"] <= 0) & ~up],
                         ["long build-up", "short build-up", "short covering", "long unwinding"], "none")
    E.loc[E["ret5"].isna() | E["C"].isna(), "grp"] = "none"
    r = ["EXPLORATORY: level effect by build-up type (OI change x price change over days -5..-1). Units bp.",
         "Model reading: new long demand blocked -> lower basis in a ban; new short demand blocked -> higher; closing",
         "pressure -> higher (no new arbitrage). D as in PAP §11.4 C7 (in-ban days k=0..min(4,L-1)).", ""]
    d = E[(E["grp"] != "none") & E["D"].notna()].copy()
    tab = d.groupby("grp")["D"].agg(["size", "mean", "median"])
    tab["mean ret5 (%)"] = d.groupby("grp")["ret5"].mean() * 100
    tab["mean C"] = d.groupby("grp")["C"].mean()
    r += [tab.round(3).to_string(), ""]
    for g, c in [("short build-up", "sb"), ("short covering", "sc"), ("long unwinding", "lu")]:
        d[c] = (d["grp"] == g).astype(int)
    fit, t, dd = le.regress(d, ["sb", "sc", "lu"])
    r.append(f"Regression D ~ group (base = long build-up), two-way clustered (stock, event date), n = {len(dd)}:")
    r.append(f"  long build-up (intercept): {le.fmt_b(t, 'Intercept')}")
    for c, nm in [("sb", "short build-up"), ("sc", "short covering"), ("lu", "long unwinding")]:
        b, se = lincomb(fit, {"Intercept": 1.0, c: 1.0})
        r.append(f"  {nm}: level {b:+.2f} (se {se:.2f}); difference from long build-up {le.fmt_b(t, c)}")
    # event-time paths by group
    sel = [-10, -5, -2, -1, 0, 1, 2, 3, 4, 7, 10]
    r += ["", "Mean D_k by group (relative to day -1):"]
    for g in ["long build-up", "short build-up", "short covering", "long unwinding"]:
        msk = (E["grp"] == g).values
        with np.errstate(all="ignore"):
            r.append(f"  {g:15s} (n={int(msk.sum())}): " + "; ".join(f"{k:+d}: {np.nanmean(P[msk, list(ks).index(k)]):+.1f}" for k in sel))
    # same-day controls version of the main contrast
    Ms = le.match(E, Cd, same_day=True)
    _, Ps = le.paths(D, E, Cd, Ms, "m")
    E2 = E.copy(); E2["D"] = le.main_stat(E2, ks, Ps)
    d2 = E2[(E2["grp"] != "none") & E2["D"].notna()].copy()
    d2["sb"] = (d2["grp"] == "short build-up").astype(int)
    d2 = d2[d2["grp"].isin(["long build-up", "short build-up"])]
    _, t2, n2 = le.regress(d2, ["sb"])
    r += ["", f"Same-day controls, long vs short build-up only (n = {len(n2)}): long build-up {le.fmt_b(t2, 'Intercept')}; "
              f"short minus long {le.fmt_b(t2, 'sb')}"]
    txt = "\n".join(r)
    open(os.path.join(ROOT, "analysis", "output", "level_effect_buildup.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
