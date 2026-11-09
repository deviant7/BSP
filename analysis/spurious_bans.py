"""Spurious bans before and after the October 2025 reform (master plan §8; PAP §11.15 C18). Treatment side only.

(a) Pre-reform ban entries: is the crossing of 95% driven by open interest or by a fall in the MWPL?
(b) Post-reform counterfactual bans: a ban state machine (enter the next day when end-of-day utilisation > 0.95; leave
    after a day with utilisation <= 0.80), validated on actual data, applied to (i) gross OI / new MWPL, (ii) FutEq OI /
    old-formula limit, (iii) gross OI / old-formula limit.
Outputs analysis/output/spurious_bans.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import calendar, PROC, ROOT

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")


def load():
    days, pos = calendar()
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), parse_dates=["date"])
    P["i"] = P["date"].map(pos)
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["i"] = B["date"].map(pos)
    B["ban"] = True
    P = P.merge(B[["symbol", "i", "ban"]], on=["symbol", "i"], how="left")
    P["ban"] = P["ban"].fillna(False).astype(bool)
    return days, pos, P.sort_values(["symbol", "i"]).reset_index(drop=True)


def machine(df, ucol, init=None):
    """Simulated ban indicator for each row (stock-day) from end-of-day utilisation of the previous trading day.
    df sorted by symbol, i; consecutive trading days assumed within a stock (gaps reset the state)."""
    sim = np.zeros(len(df), bool)
    sym, i, u = df["symbol"].values, df["i"].values, df[ucol].values
    start = init if init is not None else np.zeros(len(df), bool)
    state = False
    for k in range(len(df)):
        if k == 0 or sym[k] != sym[k - 1] or i[k] != i[k - 1] + 1:
            state = bool(start[k])
            sim[k] = state
            continue
        prev_u = u[k - 1]
        if not np.isfinite(prev_u):
            sim[k] = state
            continue
        if state:
            state = not (prev_u <= 0.80)
        else:
            state = prev_u > 0.95
        sim[k] = state
    return sim


def summary(df, col):
    d = df[df[col]]
    s = df.sort_values(["symbol", "i"])
    st = s[col].values & ~np.r_[False, (s[col].values[:-1] & (s["symbol"].values[1:] == s["symbol"].values[:-1]) &
                                        (s["i"].values[1:] == s["i"].values[:-1] + 1))]
    return len(d), int(st.sum()), d["symbol"].nunique()


def main():
    days, pos, P = load()
    r = ["Spurious bans before and after the October 2025 reform (PAP §11.15 C18). Treatment side only.", ""]
    # (a) pre-reform entries
    sp = pd.read_csv(os.path.join(PROC, "ban_spells.csv.gz"), parse_dates=["start", "end"])
    sp = sp[(sp["start"] >= "2015-01-01") & (sp["start"] < REFORM)]
    sp["i0"] = sp["start"].map(pos)
    K = P.set_index(["symbol", "i"])
    rows = []
    for s, i0 in zip(sp["symbol"], sp["i0"]):
        try:
            a = K.loc[(s, i0 - 1)]; b = K.loc[(s, i0 - 2)]
        except KeyError:
            continue
        rows.append(dict(symbol=s, i0=i0, util1=a["util"], util0=b["util"], oi1=a["oi"], oi0=b["oi"], mw1=a["mwpl"], mw0=b["mwpl"],
                         mw_fell5=any(K.loc[(s, j), "mwpl"] < K.loc[(s, j - 1), "mwpl"] for j in range(i0 - 5, i0)
                                      if (s, j) in K.index and (s, j - 1) in K.index)))
    E = pd.DataFrame(rows)
    E["dl_util"] = np.log(E["util1"] / E["util0"])
    E["dl_oi"] = np.log(E["oi1"] / E["oi0"])
    E["dl_mw"] = -np.log(E["mw1"] / E["mw0"])
    E["mw_fell"] = E["mw1"] < E["mw0"]
    E["denom"] = E["mw_fell"] & (E["oi1"] / E["mw0"] <= 0.95)
    r += ["(a) Pre-reform ban entries (2015 to Sep 2025):",
          f"  entries analysed {len(E)} (of {len(sp)} spells); utilisation on the crossing day > 0.95: {(E['util1'] > 0.95).mean():.3f}",
          f"  MWPL fell on the crossing day: {int(E['mw_fell'].sum())} ({E['mw_fell'].mean():.3f}); denominator-driven "
          f"(would not have crossed at the old limit): {int(E['denom'].sum())} ({E['denom'].mean():.3f})",
          f"  MWPL fell at least once in the five days before entry: {E['mw_fell5'].mean():.3f}",
          f"  mean change in log utilisation on the crossing day (entries with positive OI on both days, n "
          f"{int(np.isfinite(E['dl_util']).sum())}): {E.loc[np.isfinite(E['dl_util']), 'dl_util'].mean():.4f}; from OI "
          f"{E.loc[np.isfinite(E['dl_util']), 'dl_oi'].mean():.4f}, from the MWPL {E.loc[np.isfinite(E['dl_util']), 'dl_mw'].mean():.4f}"]
    # (b) validation of the machine
    pre = P[(P["date"] >= "2015-01-01") & (P["date"] < REFORM)].copy()
    pre["sim"] = machine(pre, "util", init=pre["ban"].values)
    agree = (pre["sim"] == pre["ban"]).mean()
    tp = (pre["sim"] & pre["ban"]).sum(); fp = (pre["sim"] & ~pre["ban"]).sum(); fn = (~pre["sim"] & pre["ban"]).sum()
    r += ["", "(b) Ban state machine (enter after a day > 0.95; leave after a day <= 0.80):",
          f"  validation, pre-reform gross utilisation vs official list: agreement {agree:.4f}; actual ban days {int(pre['ban'].sum())}, "
          f"simulated {int(pre['sim'].sum())}, both {int(tp)}, simulated only {int(fp)}, actual only {int(fn)}"]
    po = P[P["date"] >= REFORM].copy()
    a = P[P["date"] == "2025-09-30"].set_index("symbol")["mwpl"]
    b = P[P["date"] == "2025-10-01"].set_index("symbol")["mwpl"]
    ratio = (a / b).dropna()
    po["ratio"] = po["symbol"].map(ratio)
    n_no = po.loc[po["ratio"].isna(), "symbol"].nunique()
    po = po[po["ratio"].notna()].copy()
    po["mw_old"] = po["mwpl"] * po["ratio"]
    po["u_fe_new"] = po["futeq_oi"] / po["mwpl"]
    po["u_gr_new"] = po["oi"] / po["mwpl"]
    po["u_fe_old"] = po["futeq_oi"] / po["mw_old"]
    po["u_gr_old"] = po["oi"] / po["mw_old"]
    init = po["ban"].values
    for c in ["u_fe_new", "u_gr_new", "u_fe_old", "u_gr_old"]:
        po["sim_" + c] = machine(po, c, init=init)
    agree2 = (po["sim_u_fe_new"] == po["ban"]).mean()
    r.append(f"  validation, post-reform FutEq / new MWPL vs official list: agreement {agree2:.4f} "
             f"(actual {int(po['ban'].sum())}, simulated {int(po['sim_u_fe_new'].sum())})")
    r += ["", f"  Post-reform counterfactuals, 1 Oct 2025 to {po['date'].max().date()} (stocks in F&O on 30 Sep and 1 Oct 2025; "
              f"{n_no} later entrants excluded). Ban stock-days / spells / stocks:"]
    lab = {"ban": "actual (official list)", "sim_u_fe_new": "simulated: FutEq OI, new MWPL (the new rule)",
           "sim_u_gr_new": "gross OI, new MWPL (old measure, new limit)", "sim_u_fe_old": "FutEq OI, old-formula limit",
           "sim_u_gr_old": "gross OI, old-formula limit (the old rule)"}
    for c, nm in lab.items():
        n, s_, k = summary(po, c)
        r.append(f"    {nm:48s} {n:6d} / {s_:4d} / {k:3d}")
    r += ["", "  Reading: the measure change (gross -> FutEq) lowers utilisation and removes bans; the formula change (old -> new",
          "  limit) raises it and adds bans; the new rule combines the two. Approximation: the old-formula limit freezes each",
          "  stock's old-to-new ratio of 1 Oct 2025."]
    # utilisation levels
    r.append("  median utilisation on post-reform days: " + ", ".join(f"{c} {po[c].median():.3f}" for c in ["u_fe_new", "u_gr_new", "u_fe_old", "u_gr_old"]))
    txt = "\n".join(r)
    open(os.path.join(OUT, "spurious_bans.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
