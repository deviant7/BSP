"""Daily total returns for every NSE cash-market stock (EQ/BE/BZ), adjusted for splits, bonuses and dividends.

Usage: python3 -I build_returns.py RAW_DIR OUT_DIR
Inputs: RAW/prices/cash/YYYYMMDD.csv, RAW/corpactions/ca_YYYYMM.json
Output: OUT/returns_daily.csv.gz (git-ignored; rebuild), OUT/returns_report.txt

Why: NSE's PREVCLOSE is NOT adjusted for corporate actions (TATASTEEL 1:10 split on 28 Jul 2022: prevclose 959.4,
close 100.35; RELIANCE 1:1 bonus on 28 Oct 2024: prevclose 2655.70, close 1334.35).
Rules:
  ret = (close * k + D) / prevclose - 1 on an ex-date, where k = shares received per share held (split from face value a
  to b: k = a/b; bonus x:y: k = (x + y)/y; both: product) and D = cash dividend per pre-event share; ret = close/prevclose - 1
  otherwise. Ex-dates of rights issues, demergers and schemes of arrangement: ret = NaN with flag (their price effect needs
  issue prices or values that the subject text does not give reliably).
  Every split/bonus factor is checked against the price jump on the ex-date; a factor that does not match is reported.
  Days with |log return| > log(1.5) and no corporate action are flagged ('jump') and kept (reported for inspection).
"""
import glob, json, os, re, sys
import numpy as np
import pandas as pd

DIV_RE = re.compile(r"dividend[^0-9]{0,25}?(?:rs|re|inr)\.?\s*([0-9]+(?:\.[0-9]+)?)", re.I)
SPLIT_RE = re.compile(r"split[^0-9]*?(?:from\s*)?(?:rs|re)\.?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:/-)?(?:\s*per\s*share)?\s*to\s*(?:rs|re)\.?\s*([0-9]+(?:\.[0-9]+)?)", re.I)
BONUS_RE = re.compile(r"bonus\s*(?:issue)?\s*([0-9]+)\s*:\s*([0-9]+)", re.I)
OTHER_RE = re.compile(r"rights|demerger|arrangement|amalgamation|reduction|consolidat|spin", re.I)


def corporate_actions(raw):
    rows = []
    for f in sorted(glob.glob(os.path.join(raw, "corpactions", "*.json"))):
        for r in json.load(open(f)):
            if r.get("series") not in (None, "EQ", "BE", "BZ") or r.get("exDate") in (None, "-"):
                continue
            sub = r.get("subject", "") or ""
            k = 1.0
            for a, b in SPLIT_RE.findall(sub):
                if float(b) > 0:
                    k *= float(a) / float(b)
            if "bonus" in sub.lower() and "debenture" not in sub.lower() and "ncrps" not in sub.lower() and "preference" not in sub.lower():
                for x, y in BONUS_RE.findall(sub):
                    if float(y) > 0:
                        k *= (float(x) + float(y)) / float(y)
            div = sum(float(a) for a in DIV_RE.findall(sub))
            other = bool(OTHER_RE.search(sub))
            rows.append((r["symbol"].strip(), pd.to_datetime(r["exDate"], format="%d-%b-%Y"), k, div, other, sub))
    C = pd.DataFrame(rows, columns=["symbol", "date", "k", "div", "other", "subject"])
    C["norm"] = C["subject"].str.lower().str.replace(r"\s+", "", regex=True)
    C = C.drop_duplicates(["symbol", "date", "norm"])
    # a split and a bonus on the same ex-date are listed as separate records: multiply their factors; the same dividend
    # listed twice ("purpose revised"): take the maximum
    g = C.groupby(["symbol", "date"]).agg(k=("k", "prod"), div=("div", "max"), other=("other", "max"),
                                         subject=("subject", " | ".join)).reset_index()
    return g


def main(raw, out):
    rep = []
    fs = [f for f in sorted(glob.glob(os.path.join(raw, "prices", "cash", "*.csv"))) if os.path.getsize(f) > 0]
    X = pd.concat([pd.read_csv(f, usecols=["date", "symbol", "series", "isin", "close", "prevclose", "qty", "value_rs"])
                   for f in fs], ignore_index=True)
    X["date"] = pd.to_datetime(X["date"])
    X["pri"] = X["series"].map({"EQ": 0, "BE": 1, "BZ": 2})
    X = X.sort_values("pri").drop_duplicates(["date", "symbol"]).drop(columns="pri").sort_values(["symbol", "date"])
    n_re = X["symbol"].str.contains(r"-RE\d*$", regex=True).sum()
    X = X[~X["symbol"].str.contains(r"-RE\d*$", regex=True)]          # rights entitlements are not shares
    etf = X["symbol"].str.contains(r"ETF|BEES$|IETF$", regex=True)
    rep.append(f"ETF-like symbols dropped (ETF/BEES in the symbol): {X.loc[etf, 'symbol'].nunique()}")
    X = X[~etf]
    rep.append(f"rights-entitlement rows ('-RE' symbols) dropped: {int(n_re)}")
    rep.append(f"cash stock-days {len(X)}, symbols {X['symbol'].nunique()}, {X['date'].min().date()} to {X['date'].max().date()}")
    C = corporate_actions(raw)
    X = X.merge(C, on=["symbol", "date"], how="left")
    X["k"] = X["k"].fillna(1.0); X["div"] = X["div"].fillna(0.0); X["other"] = X["other"].fillna(False).astype(bool)
    ok = (X["prevclose"] > 0) & (X["close"] > 0)
    X["ret"] = np.where(ok, (X["close"] * X["k"] + X["div"]) / X["prevclose"] - 1, np.nan)
    X["flag"] = ""
    X.loc[X["other"], "flag"] = "other_ca"
    X.loc[X["other"], "ret"] = np.nan
    # first trading day of a symbol after the sample start (new listing, relisting, demerged entity): prevclose is a base
    # price, not a market close
    fd = (X["date"] == X.groupby("symbol")["date"].transform("min")) & (X["date"] > X["date"].min())
    X.loc[fd, "flag"] = "first_day"; X.loc[fd, "ret"] = np.nan
    rep.append(f"first trading days after sample start (return set to NaN): {int(fd.sum())}")
    # validate split/bonus factors against the price jump
    ev = X[(X["k"] != 1) & ok]
    implied = X.loc[ev.index, "prevclose"] / X.loc[ev.index, "close"]
    good = (np.log(implied / ev["k"]).abs() < np.log(1.25))
    X.loc[ev.index[~good], "flag"] = "factor_mismatch"
    rep.append(f"split/bonus ex-dates matched to a price row: {len(ev)}; factor consistent with the price jump "
               f"(within 25%): {good.mean():.3f}")
    if (~good).any():
        bad = ev[~good].assign(implied=implied[~good])[["date", "symbol", "k", "implied", "subject"]]
        rep.append("  mismatches (first 15):\n" + bad.head(15).to_string(index=False))
    lr = np.log1p(X["ret"])
    jump = (lr.abs() > np.log(1.5)) & (X["k"] == 1) & ~X["other"] & (X["flag"] == "")
    # a jump whose price ratio is a standard split/bonus ratio is almost surely a corporate action missing from the feed
    ratio = X["prevclose"] / X["close"]
    nice = np.array([1.25, 4 / 3, 1.5, 2, 2.5, 3, 4, 5, 10, 20])
    near = np.min(np.abs(np.log(ratio.values[:, None] / nice[None, :])), axis=1) < np.log(1.03)
    miss_ca = jump & pd.Series(near, index=X.index) & (X["ret"] < 0)
    X.loc[jump, "flag"] = "jump"
    X.loc[miss_ca, "flag"] = "likely_missing_ca"
    X.loc[miss_ca, "ret"] = np.nan
    # share-count factor including the inferred ratio of likely missing corporate actions (used for market cap)
    nr = nice[np.argmin(np.abs(np.log(ratio.values[:, None] / nice[None, :])), axis=1)]
    X["k_used"] = np.where(miss_ca, nr, X["k"])
    rep.append(f"jumps whose price ratio is a standard split/bonus ratio (likely missing corporate action; return NaN): "
               f"{int(miss_ca.sum())}")
    jump = jump & ~miss_ca
    rep.append(f"rights/demerger/scheme ex-dates set to NaN: {int(X['other'].sum())}")
    rep.append(f"unexplained jumps |log return| > log 1.5 (kept, flagged): {int(jump.sum())} "
               f"({jump.mean()*1e4:.2f} per 10,000 stock-days)")
    if jump.any():
        rep.append("  examples:\n" + X.loc[jump, ["date", "symbol", "series", "prevclose", "close", "ret"]].head(12).to_string(index=False))
    rep.append(f"dividend ex-dates with a price row: {int((X['div'] > 0).sum())}")
    rep.append("daily return quantiles p0.1/p1/p50/p99/p99.9: " + "/".join(f"{X['ret'].quantile(q):.4f}" for q in (.001, .01, .5, .99, .999)))
    cols = ["date", "symbol", "isin", "series", "close", "prevclose", "qty", "value_rs", "k", "k_used", "div", "ret", "flag"]
    X[cols].to_csv(os.path.join(out, "returns_daily.csv.gz"), index=False, compression="gzip", float_format="%.8g")
    open(os.path.join(out, "returns_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
