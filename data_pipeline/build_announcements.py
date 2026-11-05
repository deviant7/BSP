"""Results-announcement events: one row per (symbol, quarter end) with the time the result first became public.

Usage: python3 -I build_announcements.py RAW_DIR OUT_DIR
Inputs (all NSE):
  RAW/results/{Quarterly,Annual,Integrated}_*.json   results filings (period end, broadcast time, XBRL links)
  RAW/resultupdates/ru_*.json                        corporate announcements, category 'Financial Result Updates'
                                                     (exchange dissemination time of each results filing)
  RAW/boardmeetings/bm_*.json                        board-meeting calendar (meeting date, purpose)
Output: announcements.csv.gz, announcements_report.txt

Why three sources (audit of 5 Nov 2026):
  * the results-filings feed misses some quarters (about 10% of F&O stock-quarters before 2024) and its broadcast time is
    often that of a later re-filing: in 2017-2018 most timestamps are days or weeks after the board meeting that approved
    the results (e.g. HINDUNILVR, June 2018 quarter: meeting and release on 16 Jul 2018, feed says 3 Aug 2018);
  * the 'Financial Result Updates' announcements carry the release on the meeting day, to the second;
  * listed companies must disclose results within 30 minutes of the end of the board meeting, so the meeting date bounds
    the release date.
Rules:
  1. release = earliest timed release across the announcement and the filing feeds for that (symbol, quarter end);
  2. if a board meeting on results is known and the only timed release (from the filing feed) is more than one calendar
     day after it, that time is a re-filing: the release is the meeting date, time unknown (an announcement time is kept,
     since a later announcement usually means the meeting was postponed);
  3. quarters known only from a board meeting: release = meeting date, time unknown;
  4. day 0 = release day if released before 15:30, else the next trading day; if the time is unknown, the next trading
     day after the release date (most results are released after the close; the EAR window [-1, +1] then contains the
     release day either way).
"""
import glob, json, os, re, sys
import pandas as pd

PERIOD_RE = re.compile(r"period\s+ended\s*(?:on\s*)?[:\-]?\s*"
                       r"([0-9]{1,2}(?:st|nd|rd|th)?[\s\-/.]*[A-Za-z]{3,9}[\s\-/.,]*[0-9]{2,4}"
                       r"|[A-Za-z]{3,9}\s*[0-9]{1,2}(?:st|nd|rd|th)?,?\s*[0-9]{4}"
                       r"|[0-9]{1,2}[\-/.][0-9]{1,2}[\-/.][0-9]{2,4})", re.I)


def quarter_before(ts):
    return ts.dt.to_period("Q").dt.start_time - pd.Timedelta(days=1)


def parse_period(text):
    m = PERIOD_RE.search(text or "")
    if not m:
        return pd.NaT
    s = re.sub(r"(?<=[0-9])(st|nd|rd|th)", "", m.group(1), flags=re.I)
    d = pd.to_datetime(s, dayfirst=True, errors="coerce", format="mixed")
    if pd.isna(d):
        return pd.NaT
    d = d + pd.offsets.MonthEnd(0)
    return d if d.month in (3, 6, 9, 12) else pd.NaT


def symbol_mapper(raw, rep):
    """NSE's event feeds label old records with the company's CURRENT symbol and ISIN (audit of 5 Nov 2026: e.g. the
    filings of CADILAHC appear under ZYDUSLIFE). Map each record to the symbol that traded on the event date, using the
    daily (symbol, ISIN) pairs of the cash bhavcopy: a rename keeps the ISIN; a face-value change keeps the symbol and
    gives a new ISIN. ISINs that follow each other under one symbol (gap <= 15 days) are linked into one company."""
    fs = [f for f in sorted(glob.glob(os.path.join(raw, "prices", "cash", "*.csv"))) if os.path.getsize(f) > 0]
    C = pd.concat([pd.read_csv(f, usecols=["date", "symbol", "isin"]) for f in fs], ignore_index=True).dropna()
    C["date"] = pd.to_datetime(C["date"])
    sp = C.groupby(["isin", "symbol"])["date"].agg(["min", "max"]).reset_index()
    parent = {}
    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x
    for _, g in sp.sort_values("min").groupby("symbol"):
        g = g.reset_index(drop=True)
        for i in range(1, len(g)):
            if (g.loc[i, "min"] - g.loc[i - 1, "max"]).days <= 15 and g.loc[i, "isin"] != g.loc[i - 1, "isin"]:
                a, b = find(g.loc[i - 1, "isin"]), find(g.loc[i, "isin"])
                if a != b:
                    parent[b] = a
    sp["company"] = sp["isin"].map(find)
    by_company = {k: g.sort_values("min")[["symbol", "min", "max"]].values.tolist() for k, g in sp.groupby("company")}
    isin_company = dict(zip(sp["isin"], sp["company"]))
    last_isin = C.sort_values("date").groupby("symbol")["isin"].last().to_dict()
    lo = C["date"].min()

    def one(sym, isin, d):
        isin = isin if isinstance(isin, str) and isin in isin_company else last_isin.get(sym)
        if isin is None or pd.isna(d):
            return sym
        spans = by_company[isin_company[isin]]
        if d < lo:
            return spans[0][0]
        best = min(spans, key=lambda r: 0 if r[1] <= d <= r[2] else min(abs((d - r[1]).days), abs((d - r[2]).days)))
        return best[0]

    cache = {}
    def smap(sym, isin, when):
        out = []
        for a, b, c in zip(sym.astype(str).str.strip(), isin, pd.to_datetime(when).dt.normalize()):
            k = (a, b, c)
            if k not in cache:
                cache[k] = one(a, b, c)
            out.append(cache[k])
        res = pd.Series(out, index=sym.index)
        rep.append(f"  symbol mapping: {int((res != sym.astype(str).str.strip()).sum())} of {len(res)} records relabelled "
                   "to the symbol trading on the event date")
        return res
    return smap


def main(raw, out):
    rep = []
    smap = symbol_mapper(raw, rep)
    # ---- results filings (period end, broadcast time, XBRL links)
    rows = []
    for f in glob.glob(os.path.join(raw, "results", "Quarterly_*.json")) + glob.glob(os.path.join(raw, "results", "Annual_*.json")):
        for r in json.load(open(f)):
            rows.append((r.get("symbol"), r.get("isin"), r.get("toDate"), r.get("broadCastDate") or r.get("filingDate"),
                         r.get("consolidated"), r.get("xbrl"), "legacy"))
    for f in glob.glob(os.path.join(raw, "results", "Integrated_*.json")):
        for r in json.load(open(f)):
            rows.append((r.get("symbol"), r.get("isin"), r.get("qe_Date"), r.get("broadcast_Date"), r.get("consolidated"),
                         r.get("xbrl"), "integrated"))
    A = pd.DataFrame(rows, columns=["symbol", "isin", "period_end", "released", "consolidation", "xbrl", "src"])
    A["symbol"] = A["symbol"].astype(str).str.strip()
    A["period_end"] = pd.to_datetime(A["period_end"], format="mixed", dayfirst=True, errors="coerce").dt.normalize()
    A["released"] = pd.to_datetime(A["released"], format="mixed", dayfirst=True, errors="coerce")
    n0 = len(A)
    A = A.dropna(subset=["period_end", "released"])
    A = A[A["symbol"].ne("") & A["symbol"].ne("None")]
    A["consolidated"] = A["consolidation"].str.contains("^Consolidated", case=False, na=False)
    A["symbol"] = smap(A["symbol"], A["isin"], A["released"])
    fil = (A.sort_values("released").groupby(["symbol", "period_end"])
           .agg(filing_released=("released", "first"), n_filings=("released", "size"),
                xbrl_standalone=("xbrl", lambda s: next((x for x, c in zip(s, A.loc[s.index, "consolidated"]) if not c and x), None)),
                xbrl_consolidated=("xbrl", lambda s: next((x for x, c in zip(s, A.loc[s.index, "consolidated"]) if c and x), None)),
                filing_src=("src", "first")).reset_index())
    rep.append(f"results filings: {n0} rows -> {len(fil)} (symbol, quarter end)")

    # ---- 'Financial Result Updates' announcements (dissemination time)
    rows = []
    for f in glob.glob(os.path.join(raw, "resultupdates", "ru_*.json")):
        for r in json.load(open(f)):
            rows.append((str(r.get("symbol") or "").strip(), r.get("sm_isin"), r.get("an_dt"), r.get("attchmntText") or ""))
    U = pd.DataFrame(rows, columns=["symbol", "isin", "an_dt", "text"]).drop_duplicates()
    U["announced"] = pd.to_datetime(U["an_dt"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    U = U.dropna(subset=["announced"])
    U = U[U["symbol"].ne("")]
    U["symbol"] = smap(U["symbol"], U["isin"], U["announced"])
    U["period_end"] = U["text"].map(parse_period)
    parsed = U["period_end"].notna().mean()
    lag = (U["announced"].dt.normalize() - U["period_end"]).dt.days
    bad = U["period_end"].isna() | (lag < 0) | (lag > 200)
    U.loc[bad, "period_end"] = quarter_before(U.loc[bad, "announced"])
    U["period_end"] = U["period_end"].dt.normalize()
    ann = U.groupby(["symbol", "period_end"], as_index=False).agg(ann_released=("announced", "min"),
                                                                  n_announcements=("announced", "size"))
    rep.append(f"result-update announcements: {len(U)}; period parsed from text {parsed:.3f} "
               f"(fallback: quarter before the announcement for {bad.mean():.3f}); -> {len(ann)} (symbol, quarter end)")

    # ---- board meetings on results
    rows = []
    for f in glob.glob(os.path.join(raw, "boardmeetings", "bm_*.json")):
        for r in json.load(open(f)):
            p = str(r.get("bm_purpose", "")).lower()
            if "result" in p and not re.search(r"postpon|reschedul|adjourn|cancel", p):
                rows.append((str(r.get("bm_symbol", "")).strip(), r.get("sm_isin"), r.get("bm_date"), r.get("bm_timestamp")))
    B = pd.DataFrame(rows, columns=["symbol", "isin", "meeting", "intimated"])
    B["meeting"] = pd.to_datetime(B["meeting"], format="%d-%b-%Y", errors="coerce")
    B["intimated"] = pd.to_datetime(B["intimated"], format="%d-%b-%Y %H:%M:%S", errors="coerce")
    B = B.dropna(subset=["meeting"])
    B["symbol"] = smap(B["symbol"], B["isin"], B["meeting"])
    B["period_end"] = quarter_before(B["meeting"]).dt.normalize()
    B = B.sort_values("intimated").groupby(["symbol", "period_end"], as_index=False).last()   # latest intimation
    rep.append(f"board meetings on results: {len(B)} (symbol, quarter end)")

    # ---- combine
    ev = fil.merge(ann, on=["symbol", "period_end"], how="outer").merge(
        B[["symbol", "period_end", "meeting"]], on=["symbol", "period_end"], how="outer")
    ev["released"] = ev[["filing_released", "ann_released"]].min(axis=1)
    ev["release_src"] = pd.Series(pd.NA, index=ev.index, dtype="object")
    ev.loc[ev["released"].notna(), "release_src"] = "filing"
    ev.loc[ev["ann_released"].notna() & (ev["ann_released"] <= ev["filing_released"].fillna(pd.Timestamp.max)),
           "release_src"] = "announcement"
    ev["timing_known"] = ev["released"].notna()
    gap = (ev["released"].dt.normalize() - ev["meeting"]).dt.days
    late_any = ev["meeting"].notna() & (gap > 1)
    # only the filing feed carries re-filing times; an announcement more than a day after the meeting usually means the
    # meeting was postponed without a new intimation, so the announcement time is kept
    late = late_any & (ev["release_src"] == "filing")
    rep.append(f"timed release more than 1 day after the board meeting: {int(late_any.sum())}; from the filing feed only "
               f"(treated as re-filing, release = meeting date): {int(late.sum())}; announcement-based (kept): "
               f"{int((late_any & ~late).sum())}")
    only_bm = ev["released"].isna() & ev["meeting"].notna()
    ev.loc[late | only_bm, "released"] = ev.loc[late | only_bm, "meeting"]
    ev.loc[late | only_bm, "timing_known"] = False
    ev.loc[late | only_bm, "release_src"] = "board_meeting"
    ev = ev.dropna(subset=["released"])
    ev["lag_days"] = (ev["released"].dt.normalize() - ev["period_end"]).dt.days
    ev = ev[(ev["lag_days"] >= 0) & (ev["lag_days"] <= 200) & (ev["released"] >= pd.Timestamp("2014-01-01"))]

    # ---- event day
    cal = set(pd.read_csv(os.path.join(out, "mwpl_oi_panel.csv.gz"), usecols=["date"])["date"].unique())
    cal |= {f"{os.path.basename(f)[:4]}-{os.path.basename(f)[4:6]}-{os.path.basename(f)[6:8]}"
            for f in glob.glob(os.path.join(raw, "prices", "cash", "*.csv")) if os.path.getsize(f) > 0}
    days = pd.Series(sorted(pd.to_datetime(list(cal))))
    after_close = (ev["released"].dt.hour * 60 + ev["released"].dt.minute >= 15 * 60 + 30) | ~ev["timing_known"]
    target = ev["released"].dt.normalize() + pd.to_timedelta(after_close.astype(int), unit="D")
    idx = days.searchsorted(target)       # first trading day on or after target (handles weekends and holidays)
    ev["event_day"] = [days.iloc[i] if i < len(days) else pd.NaT for i in idx]
    ev["after_close"] = after_close.where(ev["timing_known"])
    ev = ev.sort_values(["event_day", "symbol"])
    cols = ["symbol", "period_end", "released", "timing_known", "release_src", "after_close", "event_day", "lag_days",
            "meeting", "filing_released", "ann_released", "n_filings", "n_announcements", "xbrl_standalone",
            "xbrl_consolidated", "filing_src"]
    ev[cols].to_csv(os.path.join(out, "announcements.csv.gz"), index=False, compression="gzip")

    # ---- report
    tk = ev["timing_known"]
    agree = ev[tk & ev["meeting"].notna()]
    d = (agree["released"].dt.normalize() - agree["meeting"]).dt.days
    rep += [f"events (symbol, quarter end): {len(ev)}; symbols {ev['symbol'].nunique()}",
            "release source: " + ev["release_src"].value_counts().to_string().replace("\n", "; "),
            f"timed release vs board-meeting day (where both exist, n={len(agree)}): same day {(d == 0).mean():.3f}, "
            f"next day {(d == 1).mean():.3f}, before {(d < 0).mean():.3f}",
            f"timing known: {tk.mean():.3f}; released at or after 15:30 (timing known): {ev.loc[tk, 'after_close'].mean():.3f}; "
            f"median days from quarter end to release: {ev['lag_days'].median():.0f}",
            "events per year:\n" + ev.groupby(ev["event_day"].dt.year).size().to_string()]
    fno = pd.read_csv(os.path.join(out, "fno_membership.csv.gz"), parse_dates=["date"])
    fk = set(zip(fno["date"], fno["symbol"]))
    infno = pd.Series([(a, b) in fk for a, b in zip(ev["event_day"], ev["symbol"])], index=ev.index)
    rep.append(f"events on days the stock is in the F&O segment: {int(infno.sum())}; timing known {ev.loc[infno, 'timing_known'].mean():.3f}; "
               "source: " + ev.loc[infno, "release_src"].value_counts().to_string().replace("\n", "; "))
    qe = fno.groupby(fno["date"].dt.to_period("Q"))["symbol"].apply(lambda s: set(s[fno.loc[s.index, "date"] == fno.loc[s.index, "date"].max()]))
    have = ev.groupby(ev["period_end"].dt.to_period("Q"))["symbol"].apply(set)
    cov = {str(q): round(len(s & have.get(q, set())) / len(s), 3) for q, s in qe.items() if str(q) < "2026Q3"}
    rep.append(f"coverage: share of F&O stocks (at quarter end) with an event for that quarter: min {min(cov.values()):.3f} "
               f"({min(cov, key=cov.get)}), median {pd.Series(cov).median():.3f}")
    rep.append("coverage by quarter: " + ", ".join(f"{k} {v:.2f}" for k, v in cov.items()))
    open(os.path.join(out, "announcements_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
