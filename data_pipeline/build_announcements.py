"""Results-announcement events from NSE filings (legacy results API to Mar 2025; Integrated Filing - Financials after).

Usage: python3 -I build_announcements.py RAW_DIR OUT_DIR
Output: announcements.csv.gz with one row per (symbol, period end): first public release time across standalone and
consolidated filings, the event day (day 0 = release day if released before the 15:30 close, else the next trading day),
and the XBRL links (for earnings per share later).
"""
import glob, json, os, sys
import pandas as pd


def main(raw, out):
    rows = []
    for f in glob.glob(os.path.join(raw, "results", "Quarterly_*.json")) + glob.glob(os.path.join(raw, "results", "Annual_*.json")):
        for r in json.load(open(f)):
            rows.append((r.get("symbol"), r.get("isin"), r.get("toDate"), r.get("broadCastDate") or r.get("filingDate"),
                         r.get("consolidated"), r.get("audited"), r.get("xbrl"), "legacy"))
    for f in glob.glob(os.path.join(raw, "results", "Integrated_*.json")):
        for r in json.load(open(f)):
            rows.append((r.get("symbol"), None, r.get("qe_Date"), r.get("broadcast_Date"), r.get("consolidated"),
                         r.get("audited"), r.get("xbrl"), "integrated"))
    A = pd.DataFrame(rows, columns=["symbol", "isin", "period_end", "released", "consolidation", "audited", "xbrl", "src"])
    A["period_end"] = pd.to_datetime(A["period_end"], format="mixed", dayfirst=True, errors="coerce")
    A["released"] = pd.to_datetime(A["released"], format="mixed", dayfirst=True, errors="coerce")
    n0 = len(A)
    A = A.dropna(subset=["symbol", "period_end", "released"])
    A["consolidated"] = A["consolidation"].str.contains("^Consolidated", case=False, na=False)
    ev = (A.sort_values("released").groupby(["symbol", "period_end"])
          .agg(released=("released", "first"), n_filings=("released", "size"),
               xbrl_standalone=("xbrl", lambda s: next((x for x, c in zip(s, A.loc[s.index, "consolidated"]) if not c and x), None)),
               xbrl_consolidated=("xbrl", lambda s: next((x for x, c in zip(s, A.loc[s.index, "consolidated"]) if c and x), None)),
               src=("src", "first")).reset_index())
    # trading calendar: all NSE trading days 2010 onward (from the open-interest panel) plus the price-file days
    cal = set(pd.read_csv(os.path.join(out, "mwpl_oi_panel.csv.gz"), usecols=["date"])["date"].unique())
    cal |= {f"{os.path.basename(f)[:4]}-{os.path.basename(f)[4:6]}-{os.path.basename(f)[6:8]}"
            for f in glob.glob(os.path.join(raw, "prices", "cash", "*.csv")) if os.path.getsize(f) > 0}
    days = pd.Series(sorted(pd.to_datetime(list(cal))))
    rel_day = ev["released"].dt.normalize()
    after_close = ev["released"].dt.hour * 60 + ev["released"].dt.minute >= 15 * 60 + 30
    target = rel_day + pd.to_timedelta(after_close.astype(int), unit="D")
    idx = days.searchsorted(target)       # first trading day on or after target (handles weekends/holidays)
    ev["event_day"] = [days.iloc[i] if i < len(days) else pd.NaT for i in idx]
    ev["after_close"] = after_close
    ev["lag_days"] = (ev["released"] - ev["period_end"]).dt.days
    ev = ev[(ev["lag_days"] >= 0) & (ev["lag_days"] <= 200)]
    ev.to_csv(os.path.join(out, "announcements.csv.gz"), index=False, compression="gzip")
    rep = [f"filing rows {n0}; events (symbol x period end) {len(ev)}; symbols {ev['symbol'].nunique()}",
           f"released after close: {ev['after_close'].mean():.3f}; median days from period end to release: {ev['lag_days'].median():.0f}",
           "events per year:\n" + ev.groupby(ev["event_day"].dt.year).size().to_string()]
    fno = pd.read_csv(os.path.join(out, "fno_membership.csv.gz"))
    fs = set(fno["symbol"])
    e2 = ev[ev["symbol"].isin(fs)]
    rep.append(f"events for symbols ever in F&O: {len(e2)}; per symbol-year median "
               f"{e2.groupby(['symbol', e2['event_day'].dt.year]).size().median():.0f}")
    open(os.path.join(out, "announcements_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
