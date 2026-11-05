"""Results-announcement events from NSE filings (legacy results API to Mar 2025; Integrated Filing - Financials after).

Usage: python3 -I build_announcements.py RAW_DIR OUT_DIR
Output: announcements.csv.gz with one row per (symbol, period end): first public release time across standalone and
consolidated filings, the event day (day 0 = release day if released before the 15:30 close, else the next trading day),
and the XBRL links (for earnings per share later).
Gaps: the legacy results API lacks some filings (e.g. 52 of 198 F&O stocks have no June-2022-quarter filing there).
(symbol, quarter) pairs missing from the filings are filled from the NSE board-meeting calendar (purpose 'Financial
results'; the period is the last quarter end before the meeting). Those events have a date but no release time:
timing_known = False, day 0 = the meeting day (next trading day if it is a holiday). The EAR window [-1, +1] and the
drift window from day +2 do not depend on the release time to within one day.
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
    ev["timing_known"] = True

    # board meetings on financial results (fills gaps in the filings data)
    bm = []
    for f in glob.glob(os.path.join(raw, "boardmeetings", "bm_*.json")):
        for r in json.load(open(f)):
            if "financial result" in str(r.get("bm_purpose", "")).lower():
                bm.append((str(r.get("bm_symbol", "")).strip(), r.get("bm_date"), r.get("bm_timestamp")))
    B = pd.DataFrame(bm, columns=["symbol", "meeting", "intimated"])
    B["meeting"] = pd.to_datetime(B["meeting"], format="%d-%b-%Y", errors="coerce")
    B["intimated"] = pd.to_datetime(B["intimated"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    B = B.dropna(subset=["symbol", "meeting"])
    B["period_end"] = B["meeting"].dt.to_period("Q").dt.start_time - pd.Timedelta(days=1)   # quarter before the meeting
    B["period_end"] = B["period_end"].dt.normalize()
    # the latest intimation for a (symbol, quarter) carries the final meeting date (meetings get rescheduled)
    B = B.sort_values("intimated").groupby(["symbol", "period_end"], as_index=False).last()
    key_ev = set(zip(ev["symbol"], ev["period_end"]))
    both = B[[k in key_ev for k in zip(B["symbol"], B["period_end"])]].merge(ev[["symbol", "period_end", "released"]],
                                                                            on=["symbol", "period_end"])
    agree = (both["released"].dt.normalize() == both["meeting"]).mean() if len(both) else float("nan")
    add = B[[k not in key_ev for k in zip(B["symbol"], B["period_end"])]].copy()
    add = add.assign(released=add["meeting"], n_filings=0, xbrl_standalone=None, xbrl_consolidated=None,
                     src="board_meeting", timing_known=False)
    add = add[add["meeting"] >= pd.Timestamp("2014-01-01")]
    ev = pd.concat([ev, add[ev.columns]], ignore_index=True)

    # trading calendar: all NSE trading days 2010 onward (from the open-interest panel) plus the price-file days
    cal = set(pd.read_csv(os.path.join(out, "mwpl_oi_panel.csv.gz"), usecols=["date"])["date"].unique())
    cal |= {f"{os.path.basename(f)[:4]}-{os.path.basename(f)[4:6]}-{os.path.basename(f)[6:8]}"
            for f in glob.glob(os.path.join(raw, "prices", "cash", "*.csv")) if os.path.getsize(f) > 0}
    days = pd.Series(sorted(pd.to_datetime(list(cal))))
    rel_day = ev["released"].dt.normalize()
    after_close = (ev["released"].dt.hour * 60 + ev["released"].dt.minute >= 15 * 60 + 30) & ev["timing_known"]
    target = rel_day + pd.to_timedelta(after_close.astype(int), unit="D")
    idx = days.searchsorted(target)       # first trading day on or after target (handles weekends/holidays)
    ev["event_day"] = [days.iloc[i] if i < len(days) else pd.NaT for i in idx]
    ev["after_close"] = after_close
    ev["lag_days"] = (ev["released"] - ev["period_end"]).dt.days
    ev = ev[(ev["lag_days"] >= 0) & (ev["lag_days"] <= 200)]
    ev.to_csv(os.path.join(out, "announcements.csv.gz"), index=False, compression="gzip")
    rep = [f"filing rows {n0}; events (symbol x period end) {len(ev)}; symbols {ev['symbol'].nunique()}",
           f"board meetings on results: {len(B)} (symbol x quarter); also in filings: {len(both)}, of which meeting day = "
           f"release day: {agree:.3f}; added from board meetings: {int((ev['src'] == 'board_meeting').sum())}",
           f"released after close (timing known): {ev.loc[ev['timing_known'], 'after_close'].mean():.3f}; median days from period end to release: {ev['lag_days'].median():.0f}",
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
