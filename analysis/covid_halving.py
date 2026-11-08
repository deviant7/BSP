"""COVID MWPL halving (March 2020) and restoration (27 Nov 2020) as mechanical shocks to the position limit
(master plan §6.4; PAP §11.15 C20). Exploratory.

DiD: y_it = b * Post_it x Treated_i + stock FE + date FE, 40 trading days either side, two-way clustered SE.
Outcomes: utilisation the day before (first stage), in a ban, log(1 + futures contracts), upper/lower exceedance U, L and
level m - q50 (thresholds as PAP C11 a). Restoration is the main design (calm market, announced date); the halving
coincided with the March 2020 crash and selected stocks on volatility and utilisation.
Outputs analysis/output/covid_halving.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, calendar, treatment, PROC, ROOT
from inference import feols, coef_table
from h9_regime import thresholds, outcomes

OUT = os.path.join(ROOT, "analysis", "output")


def panel():
    days, pos = calendar()
    S = basis_sample()
    q = thresholds(S)
    S = outcomes(S.copy(), q)
    A = futures_activity()
    A["i"] = A["date"].map(pos)
    A["ly_fut"] = np.log1p(A["vol"])
    lag, B = treatment(days, pos)
    T = A[["symbol", "i", "date", "ly_fut", "ban", "omega_lag", "expiry_day"]].copy()
    T["ban"] = T["ban"].astype(float)
    T.loc[T["expiry_day"].fillna(False).astype(bool), "ly_fut"] = np.nan
    return days, pos, S, T


def treated_sets(pos):
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl"], parse_dates=["date"])
    P = P.sort_values(["symbol", "date"])
    P["r"] = P.groupby("symbol")["mwpl"].pct_change() + 1
    h = P[(P["date"] >= "2020-03-19") & (P["date"] <= "2020-03-31") & P["r"].between(0.45, 0.55)]
    halved = {s: pos[d] + 1 for s, d in zip(h["symbol"], h["date"])}          # effective next trading day
    rr = P[(P["date"] == "2020-11-26") & P["r"].between(1.8, 2.2)]
    restored = set(rr["symbol"])
    return halved, restored


def did(df, y, lab):
    d = df.dropna(subset=[y]).copy()
    if d["tp"].sum() < 30:
        return f"  {lab:34s} too few treated post observations"
    t = coef_table(feols(d, f"{y} ~ tp | symbol + date"))
    return (f"  {lab:34s} Post x Treated {t.loc['tp', 'b']:+.4f} (se {t.loc['tp', 'se']:.4f}, t {t.loc['tp', 't']:+.2f}); "
            f"n {len(d)}, treated stocks {d.loc[d['treated'] == 1, 'symbol'].nunique()}")


def block(S, T, days, i_event, treated_post, W, lab, ctrl_filter=None):
    r = [lab]
    lo, hi = i_event - W, i_event + W - 1
    for df, ys in ((T, [("omega_lag", "utilisation (first stage)"), ("ban", "in a ban"), ("ly_fut", "log(1 + futures contracts)")]),
                   (S, [("U", "upper exceedance U"), ("L", "lower exceedance L"), ("lev", "level m - q50 (bp)")])):
        d = df[(df["i"] >= lo) & (df["i"] <= hi)].copy()
        d["treated"], d["tp"] = treated_post(d)
        if ctrl_filter is not None:
            d = d[ctrl_filter(d)]
        for y, nm in ys:
            r.append(did(d, y, nm))
    return r


def main():
    days, pos, S, T = panel()
    halved, restored = treated_sets(pos)
    i_rest = pos[pd.Timestamp("2020-11-27")]
    r = ["COVID MWPL halving and restoration (PAP §11.15 C20). Exploratory. Stock and date FE; SE two-way clustered.",
         f"Halved stocks (files 20-27 Mar 2020): {len(halved)}; restored stocks (file 26 Nov 2020, effective 27 Nov): {len(restored)}", ""]

    def tp_rest(d):
        tr = d["symbol"].isin(restored).astype(int)
        return tr, tr * (d["i"] >= i_rest).astype(int)
    r += block(S, T, days, i_rest, tp_rest, 40, "(a) RESTORATION, 40 trading days either side of 27 Nov 2020")
    # robustness: controls with pre-window utilisation above 0.20
    pre = T[(T["i"] >= i_rest - 40) & (T["i"] < i_rest)].groupby("symbol")["omega_lag"].mean()
    hi_util = set(pre[pre > 0.20].index) | restored
    r += block(S, T, days, i_rest, tp_rest, 40, "  robustness: controls with pre-window mean utilisation > 0.20",
               ctrl_filter=lambda d: d["symbol"].isin(hi_util))
    r += block(S, T, days, i_rest, tp_rest, 20, "  robustness: 20 trading days either side")
    # pre-trend: placebo restoration date 20 days earlier, pre-window only
    i_fake = i_rest - 20
    def tp_fake(d):
        tr = d["symbol"].isin(restored).astype(int)
        return tr, tr * (d["i"] >= i_fake).astype(int)
    Sp, Tp = S[S["i"] < i_rest], T[T["i"] < i_rest]
    r += block(Sp, Tp, days, i_fake, tp_fake, 20, "  placebo: fake restoration 20 days earlier (data before the true date only)")
    # (b) halving (staggered by stock within one week)
    i_half = pos[pd.Timestamp("2020-03-23")]
    def tp_half(d):
        eff = d["symbol"].map(halved)
        tr = eff.notna().astype(int)
        return tr, (tr * (d["i"] >= eff.fillna(10 ** 9))).astype(int)
    r += [""] + block(S, T, days, i_half, tp_half, 40, "(b) HALVING, 40 trading days either side of 23 Mar 2020 (crash period; selected stocks)")
    txt = "\n".join(r)
    open(os.path.join(OUT, "covid_halving.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
