"""Daily market capitalisation for every NSE cash-market stock, from AMFI half-yearly average market caps.

Usage: python3 -I build_mcap.py OUT_DIR       (needs OUT/returns_daily.csv.gz and OUT/amfi_mcap.csv.gz)
Output: OUT/mcap_daily.csv.gz (git-ignored): date, symbol, mcap_cr, src ('amfi' = share count from the same half-year,
        'backcast' = before the stock's first AMFI half-year, 'forward' = after its last); OUT/mcap_report.txt.
Method: an adjusted price A_t = close_t x K_t, where K_t is the cumulative product of share-count factors (splits,
bonuses, and the inferred ratio of likely-missing corporate actions) up to t, so A_t is comparable across splits. For
each AMFI half-year h, the share count in base units is S_h = average market cap_h / mean(A_t over h). Market cap on day
t = A_t x S_h(t), with h(t) the half-year containing t; before the first and after the last AMFI half-year of a stock
the nearest S_h is used (this ignores new issues and buybacks; the error is measured by a back-cast test inside the
AMFI window and reported).
AMFI rows are matched to stocks by ISIN within the half-year, else by the NSE symbol printed in the row.
"""
import os, sys
import numpy as np
import pandas as pd


def half(d):
    return np.where(d.dt.month <= 6, d.dt.year.astype(str) + "-06-30", d.dt.year.astype(str) + "-12-31")


def main(out):
    rep = []
    R = pd.read_csv(os.path.join(out, "returns_daily.csv.gz"), usecols=["date", "symbol", "isin", "close", "k_used"],
                    parse_dates=["date"]).sort_values(["symbol", "date"])
    R["K"] = R.groupby("symbol")["k_used"].cumprod()
    R["A"] = R["close"] * R["K"]
    R["per"] = half(R["date"])
    A = pd.read_csv(os.path.join(out, "amfi_mcap.csv.gz"))
    A["symbols"] = A["symbols"].fillna("")
    # match AMFI rows to symbols within each half-year: ISIN first, then NSE symbol token
    pairs = R[["per", "isin", "symbol"]].drop_duplicates()
    m1 = pairs.merge(A[["period_end", "isin", "avg_mcap_cr"]], left_on=["per", "isin"], right_on=["period_end", "isin"])
    m1 = m1.groupby(["per", "symbol"])["avg_mcap_cr"].max().reset_index()
    tok = A.assign(tok=A["symbols"].str.split()).explode("tok")[["period_end", "isin", "tok", "avg_mcap_cr"]].dropna()
    tok = tok.drop_duplicates(["period_end", "isin", "tok"])             # BSE and NSE symbols are often the same
    tok = tok.drop_duplicates(["period_end", "tok"], keep=False)          # a token naming two companies is dropped
    m2 = pairs.merge(tok, left_on=["per", "symbol"], right_on=["period_end", "tok"])[["per", "symbol", "avg_mcap_cr"]]
    m2 = m2.drop_duplicates(["per", "symbol"])
    M = pd.concat([m1.assign(how="isin"), m2.assign(how="symbol")]).drop_duplicates(["per", "symbol"], keep="first")
    rep.append(f"AMFI half-year x stock matches: {len(M)} (by ISIN {int((M['how']=='isin').sum())}, by symbol {int((M['how']=='symbol').sum())})")
    avgA = R.groupby(["per", "symbol"])["A"].mean().rename("avgA").reset_index()
    M = M.merge(avgA, on=["per", "symbol"])
    M["S"] = M["avg_mcap_cr"] / M["avgA"]                 # crore per unit of adjusted price
    # back-cast test inside the AMFI window: predict each half-year from the S of 6 half-years (3 years) later
    M = M.sort_values(["symbol", "per"])
    M["S_fwd3"] = M.groupby("symbol")["S"].shift(-6)
    err = np.log(M["S_fwd3"] / M["S"]).dropna()
    rep.append(f"back-cast test (share count taken from 3 years later): n={len(err)}, median |log error| {err.abs().median():.3f}, "
               f"p75 {err.abs().quantile(.75):.3f}, p90 {err.abs().quantile(.9):.3f}, share within 10% {(err.abs() < np.log(1.1)).mean():.3f}")
    M["S_fwd1"] = M.groupby("symbol")["S"].shift(-1)
    e1 = np.log(M["S_fwd1"] / M["S"]).dropna()
    rep.append(f"  (from the next half-year: median |log error| {e1.abs().median():.3f}, within 10% {(e1.abs() < np.log(1.1)).mean():.3f})")
    # assign S to every day: same half-year if available, else nearest half-year of the same stock
    R = R.merge(M[["per", "symbol", "S"]], on=["per", "symbol"], how="left")
    R["src"] = np.where(R["S"].notna(), "amfi", "")
    first = M.groupby("symbol")["per"].min(); last = M.groupby("symbol")["per"].max()
    Sfirst = M.sort_values("per").groupby("symbol")["S"].first(); Slast = M.sort_values("per").groupby("symbol")["S"].last()
    pre = R["S"].isna() & (R["per"] < R["symbol"].map(first))
    post = R["S"].isna() & (R["per"] > R["symbol"].map(last))
    R.loc[pre, "S"] = R.loc[pre, "symbol"].map(Sfirst); R.loc[pre, "src"] = "backcast"
    R.loc[post, "S"] = R.loc[post, "symbol"].map(Slast); R.loc[post, "src"] = "forward"
    gap = R["S"].isna() & R["symbol"].isin(first.index)
    R["S"] = R.groupby("symbol")["S"].transform(lambda s: s.ffill().bfill())
    R.loc[gap & R["S"].notna(), "src"] = "interpolated"
    R["mcap_cr"] = R["A"] * R["S"]
    have = R["mcap_cr"].notna()
    rep.append(f"stock-days with a market cap: {have.mean():.3f}; by source: " +
               R.loc[have, "src"].value_counts(normalize=True).round(3).to_dict().__repr__())
    yr = R.groupby(R["date"].dt.year).apply(lambda d: pd.Series({"stocks": d["symbol"].nunique(),
                                                                  "share_with_mcap": d["mcap_cr"].notna().mean()}))
    rep.append("by year:\n" + yr.round(3).to_string())
    R.loc[have, ["date", "symbol", "mcap_cr", "src"]].to_csv(os.path.join(out, "mcap_daily.csv.gz"), index=False,
                                                             compression="gzip", float_format="%.6g")
    open(os.path.join(out, "mcap_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1])
