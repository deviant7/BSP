"""F&O segment membership and entry/exit events, 2015 onward, from the futures bhavcopy.

Membership: a stock is in the F&O segment on day t if stock futures (STF) on it are listed in that day's F&O bhavcopy.
(The combined-OI file lists stocks one day earlier at entry, because its limits apply to the next day; checked separately.)
Symbol renames are linked through ISINs from the cash bhavcopy so that a rename is not counted as an exit plus an entry.
Usage: python3 -I build_fno_events.py RAW_DIR OUT_DIR
Outputs: fno_membership.csv.gz (date, symbol, isin), fno_events.csv (event list), fno_events_report.txt
"""
import glob, os, sys
import pandas as pd


def main(raw, out):
    rep = []
    F = pd.concat([pd.read_csv(f, usecols=["date", "inst", "symbol"]) for f in sorted(glob.glob(os.path.join(raw, "prices", "fut", "*.csv")))])
    F = F[(F["inst"] == "STF") & (F["symbol"] != "NSETEST")].drop_duplicates(["date", "symbol"])[["date", "symbol"]]
    C = pd.concat([pd.read_csv(f, usecols=["date", "symbol", "series", "isin"]) for f in sorted(glob.glob(os.path.join(raw, "prices", "cash", "*.csv")))
                   if os.path.getsize(f) > 0])
    C = C.sort_values("series").drop_duplicates(["date", "symbol"])
    # consecutive days are counted over days that HAVE an F&O file, so a missing file (30 Mar 2021) is not a gap
    days = sorted(set(F["date"]))
    missing = sorted(set(C["date"]) - set(F["date"]))
    rep.append(f"cash trading days without an F&O file (bridged): {missing}")
    pos = {d: i for i, d in enumerate(days)}
    M = F.merge(C[["date", "symbol", "isin"]], on=["date", "symbol"], how="left")
    rep.append(f"F&O stock-days {len(M)}, symbols {M['symbol'].nunique()}, ISIN matched {M['isin'].notna().mean():.4f}")

    M["k"] = M["date"].map(pos)
    M = M.sort_values(["symbol", "k"])
    M["new"] = M.groupby("symbol")["k"].diff().ne(1)
    M["spell"] = M.groupby("symbol")["new"].cumsum()
    sp = M.groupby(["symbol", "spell"]).agg(first=("date", "min"), last=("date", "max"), kf=("k", "min"), kl=("k", "max"),
                                            isin_first=("isin", "first"), isin_last=("isin", "last")).reset_index()
    # link renames: a spell ending at k and another symbol's spell starting at k+1 with the same ISIN
    starts = sp.set_index(["isin_first", "kf"])
    sp["renamed_to"] = [starts.loc[(i, k + 1), "symbol"] if (i, k + 1) in starts.index else None
                        for i, k in zip(sp["isin_last"], sp["kl"])]
    ends = sp.set_index(["isin_last", "kl"])
    sp["renamed_from"] = [ends.loc[(i, k - 1), "symbol"] if (i, k - 1) in ends.index else None
                          for i, k in zip(sp["isin_first"], sp["kf"])]
    last_day, first_day = days[-1], days[0]
    cash_days = C.groupby("symbol")["date"].apply(set)
    ev = []
    for _, r in sp.iterrows():
        if r["first"] != first_day and pd.isna(r["renamed_from"]):
            prior_cash = sum(1 for d in cash_days.get(r["symbol"], set()) if d < r["first"])
            ev.append((r["first"], r["symbol"], "entry", r["isin_first"], prior_cash))
        if r["last"] != last_day and pd.isna(r["renamed_to"]):
            nxt = days[r["kl"] + 1] if r["kl"] + 1 < len(days) else None
            later_cash = sum(1 for d in cash_days.get(r["symbol"], set()) if d > r["last"])
            ev.append((nxt, r["symbol"], "exit", r["isin_last"], later_cash))
    E = pd.DataFrame(ev, columns=["date", "symbol", "type", "isin", "cash_days_before_or_after"])
    E["note"] = ""
    E.loc[(E["type"] == "entry") & (E["cash_days_before_or_after"] < 60), "note"] = "recent listing (<60 cash days before entry)"
    E.loc[(E["type"] == "exit") & (E["cash_days_before_or_after"] < 5), "note"] = "no cash trading after exit (merger/delisting/symbol change)"
    E = E.sort_values(["date", "type", "symbol"])
    renames = sp.dropna(subset=["renamed_to"])[["symbol", "renamed_to", "last"]]
    rep.append(f"symbol renames linked by ISIN: {len(renames)}: " + ", ".join(f"{a}->{b} ({str(d)})" for a, b, d in renames.values[:30]))
    rep.append(f"events: entries {sum(E['type']=='entry')}, exits {sum(E['type']=='exit')}; "
               f"eligibility-type exits (cash trading continues) {sum((E['type']=='exit') & (E['note']==''))}; "
               f"entries of established stocks {sum((E['type']=='entry') & (E['note']==''))}")
    by = E.assign(y=E["date"].str[:4]).groupby(["y", "type"]).size().unstack(fill_value=0)
    rep.append("by year:\n" + by.to_string())
    bd = E.groupby(["date", "type"]).size().reset_index(name="n").sort_values("n", ascending=False)
    rep.append("largest batches:\n" + bd.head(12).to_string(index=False))
    M[["date", "symbol", "isin"]].to_csv(os.path.join(out, "fno_membership.csv.gz"), index=False, compression="gzip")
    E.to_csv(os.path.join(out, "fno_events.csv"), index=False)
    open(os.path.join(out, "fno_events_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
