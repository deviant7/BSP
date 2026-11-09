"""Audit robustness check (8 Nov 2026; exploratory, logged in PAP §11.2): do the constraint index's relations to
post-announcement drift and price delay survive a size control? Same regressions as constraint_index.py validation (ii), adding
market-cap decile fixed effects (decile of the previous month-end market cap within the cash universe).
Outputs analysis/output/index_size_check.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from samples import PROC, CACHE, ROOT
from inference import feols, coef_table


def main():
    Z = pd.read_csv(os.path.join(PROC, "constraint_index_q.csv.gz"))
    Z["q"] = pd.PeriodIndex(Z["q"], freq="Q")
    E = pd.read_pickle(os.path.join(CACHE, "event_outcomes.pkl"))
    E["q0"] = E["event_day"].dt.to_period("Q") - 1
    E = E.merge(Z[["symbol", "q", "index"]].rename(columns={"q": "q0", "index": "index_prev"}), on=["symbol", "q0"], how="inner")
    M = pd.read_csv(os.path.join(PROC, "mcap_daily.csv.gz"), parse_dates=["date"])
    M["ym"] = M["date"].dt.to_period("M")
    me = M.sort_values("date").groupby(["symbol", "ym"]).tail(1).copy()
    me["dec"] = me.groupby("ym")["mcap_cr"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    me["ym"] = me["ym"] + 1
    E["ym"] = E["event_day"].dt.to_period("M")
    E = E.merge(me[["symbol", "ym", "dec"]], on=["symbol", "ym"], how="left").dropna(subset=["bhar_w", "dec"])
    E["abs_bhar"] = E["bhar_w"].abs()
    E["qs"] = E["q"].astype(str); E["date_c"] = E["event_day"].astype(str); E["decs"] = E["dec"].astype(int).astype(str)
    r = ["Constraint index and drift with and without a size control (exploratory audit check). Two-way clustered SE.", ""]
    for lab, d in [("all events, |BHAR|", E), ("bad news, BHAR", E[E["bad"] == True]), ("good news, BHAR", E[E["good"] == True])]:
        y = "abs_bhar" if "|" in lab else "bhar_w"
        a = coef_table(feols(d, f"{y} ~ index_prev | qs", cluster="symbol+date_c"))
        b = coef_table(feols(d, f"{y} ~ index_prev | qs + decs", cluster="symbol+date_c"))
        r.append(f"  {lab:20s} quarter FE: {a.loc['index_prev', 'b']:+.4f} ({a.loc['index_prev', 'se']:.4f});  "
                 f"+ size-decile FE: {b.loc['index_prev', 'b']:+.4f} ({b.loc['index_prev', 'se']:.4f}); n {len(d)}")
    D = pd.read_pickle(os.path.join(CACHE, "delay_panel.pkl"))
    Zy = Z.assign(year=Z["q"].dt.year + 1).groupby(["symbol", "year"])["index"].mean().rename("index_prev").reset_index()
    Dv = D.merge(Zy, on=["symbol", "year"]).dropna(subset=["delay", "log_mcap"])
    Dv["ys"] = Dv["year"].astype(str)
    r.append("")
    for rhs, fe in [("index_prev", "ys"), ("index_prev + log_mcap", "ys"), ("index_prev + log_mcap", "ys + symbol")]:
        t = coef_table(feols(Dv, f"delay ~ {rhs} | {fe}", cluster="symbol"))
        r.append(f"  price delay ~ {rhs:22s} | {fe:12s}: index {t.loc['index_prev', 'b']:+.4f} ({t.loc['index_prev', 'se']:.4f}); n {len(Dv)}")
    txt = "\n".join(r)
    open(os.path.join(ROOT, "analysis", "output", "index_size_check.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
