"""Secondary: hysteresis comparison in the 80-95% utilisation zone (model Cor. hysteresis). Specification: PAP §11.7 C10.

m_t = b Ban_t + g1 omega_(t-1) + g2 d omega + sum_l r_l m_(t-l) + stock FE + date FE, omega_(t-1) in [0.80, 0.95).
Outputs analysis/output/hysteresis.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, calendar, treatment, ROOT
from inference import feols, coef_table, lincomb
from h7_onesided import add_postexp

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
INTRADAY = pd.Timestamp("2020-03-23")
BP = 1e4


def data():
    days, pos = calendar()
    S = add_postexp(basis_sample())
    for c in ["m", "dm", "mc", "rr"]:
        S[c] = S[c] * BP
    lag, _ = treatment(days, pos)
    # omega_(t-2) = omega_lag attached to day t-1; max omega over t-10..t-1
    W = lag.pivot_table(index="i", columns="symbol", values="omega_lag")
    W = W.reindex(range(len(days) + 1))
    om2 = W.shift(1).stack().rename("omega_lag2").reset_index()
    mx = W.rolling(10, min_periods=5).max().stack().rename("omega_max10").reset_index()  # omega_lag over days t-9..t = omega t-10..t-1
    S = S.merge(om2, on=["i", "symbol"], how="left").merge(mx, on=["i", "symbol"], how="left")
    M = S[["symbol", "i", "m"]]
    for l in range(1, 6):
        L = M.copy(); L["i"] += l
        S = S.merge(L.rename(columns={"m": f"m_l{l}"}), on=["symbol", "i"], how="left")
    A = futures_activity()
    A["i"] = A["date"].map(pos)
    A["ly_fut"] = np.log1p(A["vol"])
    A = A[["symbol", "i", "ly_fut", "R", "deliv_share", "expiry_day"]]
    S = S.merge(A, on=["symbol", "i"], how="left")
    for c in ["ly_fut", "R", "deliv_share"]:
        S.loc[S["expiry_day"].fillna(False).astype(bool), c] = np.nan
    S["d_omega"] = S["omega_lag"] - S["omega_lag2"]
    S["ban_i"] = S["ban"].astype(int)
    S["bin"] = pd.cut(S["omega_lag"], [0.80, 0.85, 0.90, 0.95], right=False, labels=["a", "b", "c"]).astype(str)
    return S


LAGS = " + ".join(f"m_l{l}" for l in range(1, 6))


def est(d, y, rhs, fe="symbol + date", name="ban_i"):
    cols = [y] + [c.strip() for c in rhs.replace("C(bin)", "bin").split("+")]
    dd = d.dropna(subset=[c for c in cols if c in d.columns])
    fit = feols(dd, f"{y} ~ {rhs} | {fe}")
    t = coef_table(fit)
    return fit, t, dd


def fmt(t, name, dd):
    b, se, p = t.loc[name, "b"], t.loc[name, "se"], t.loc[name, "p_two"]
    p1 = p / 2 if b > 0 else 1 - p / 2
    return (f"{b:+8.3f} (se {se:.3f}, t {b / se:+.2f}); two-sided p = {p:.3g}; one-sided p(b > 0) = {p1:.3g}; "
            f"n = {len(dd)}, ban days {int(dd['ban_i'].sum())}, stocks {dd['symbol'].nunique()}")


def main():
    S = data()
    Z = S[(S["date"] < REFORM) & S["omega_lag"].between(0.80, 0.95, inclusive="left")].copy()
    base = f"ban_i + omega_lag + d_omega + {LAGS}"
    r = ["Hysteresis comparison, omega_(t-1) in [0.80, 0.95) (PAP §11.7 C10). Units bp. Stock and date FE; SE two-way "
         "clustered (stock, date).", f"Zone stock-days 2015 to Sep 2025: {len(Z)}, of which in a ban {int(Z['ban'].sum())}", ""]
    fit, t, dd = est(Z, "m", base)
    r.append("MAIN: m_t on Ban_t, omega_(t-1), d omega, 5 lags of m:")
    r.append("  Ban: " + fmt(t, "ban_i", dd))
    r.append("  other coefficients: " + "; ".join(f"{k} {t.loc[k, 'b']:+.3f}" for k in ["omega_lag", "d_omega", "m_l1", "m_l2", "m_l5"]))
    r += ["", "Secondary outcomes (same specification):"]
    for y, nm in [("dm", "Delta m_t, same contract"), ("mc", "close-based basis"), ("rr", "relative implied repo (annual rate)"),
                  ("ly_fut", "log(1 + futures contracts)"), ("R", "R = (dOI + V)/V"), ("deliv_share", "delivery share")]:
        _, t2, d2 = est(Z, y, base)
        r.append(f"  {nm:36s} " + fmt(t2, "ban_i", d2))
    r += ["", "Robustness (outcome m_t):"]
    variants = [("utilisation bins instead of linear", f"ban_i + C(bin) + d_omega + {LAGS}", Z),
                ("without lagged basis", "ban_i + omega_lag + d_omega", Z),
                ("adding max omega over t-10..t-1", base + " + omega_max10", Z),
                ("excluding imputed ban days", base, Z[Z["ban_source"] != "imputed"]),
                ("end-of-day enforcement (to 22 Mar 2020)", base, Z[Z["date"] < INTRADAY]),
                ("peak-intraday enforcement (from 23 Mar 2020)", base, Z[Z["date"] >= INTRADAY])]
    for nm, rhs, d in variants:
        _, t3, d3 = est(d, "m", rhs)
        r.append(f"  {nm:44s} " + fmt(t3, "ban_i", d3))
    Z["ban_pre"] = (Z["ban"] & (Z["postexp"] == 0)).astype(int)
    Z["ban_post"] = (Z["ban"] & (Z["postexp"] == 1)).astype(int)
    rhs = f"ban_pre + ban_post + omega_lag + d_omega + {LAGS}"
    dd = Z.dropna(subset=["m", "omega_lag", "d_omega"] + [f"m_l{l}" for l in range(1, 6)])
    fit4 = feols(dd, f"m ~ {rhs} | symbol + date")
    t4 = coef_table(fit4)
    r.append(f"  in-ban days before an expiry in the spell: {t4.loc['ban_pre', 'b']:+.3f} (se {t4.loc['ban_pre', 'se']:.3f}, "
             f"n ban {int(dd['ban_pre'].sum())}); after: {t4.loc['ban_post', 'b']:+.3f} (se {t4.loc['ban_post', 'se']:.3f}, "
             f"n ban {int(dd['ban_post'].sum())})")
    P = S[(S["date"] >= REFORM) & S["omega_lag"].between(0.80, 0.95, inclusive="left")]
    r += ["", f"After 1 Oct 2025 (FutEq utilisation; descriptive): zone stock-days {len(P)}, in a ban {int(P['ban'].sum())}"]
    if P["ban"].sum() >= 20:
        _, t5, d5 = est(P, "m", base)
        r.append("  Ban: " + fmt(t5, "ban_i", d5))
    txt = "\n".join(r)
    open(os.path.join(OUT, "hysteresis.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
