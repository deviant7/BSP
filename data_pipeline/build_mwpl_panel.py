"""Build the stock-day MWPL / open-interest / ban panel from NSE combineoi and fo_secban files.

Treatment-side only (MWPL, OI, utilisation, ban status). No prices or mispricing outcomes.
Usage: python3 -I build_mwpl_panel.py RAW_DIR OUT_DIR
Outputs (OUT_DIR):
  mwpl_oi_panel.csv.gz   one row per (date, symbol): mwpl, oi, futeq_oi, util, util_futeq, limit_next_day, no_fresh_next_day
  ban_days.csv.gz        one row per (trade date, symbol) in the official securities-in-ban list
  build_report.txt       parsing counts and consistency checks
"""
import glob, io, os, re, struct, sys, zipfile, zlib
import pandas as pd


def parse_date(x):
    """NSE files use DD-MON-YYYY and (in some years) DD-Mon-YY."""
    x = str(x).strip()
    for fmt in ("%d-%b-%Y", "%d-%b-%y"):
        try:
            return pd.to_datetime(x, format=fmt)
        except Exception:
            pass
    return pd.NaT


def zip_members(path):
    """Return [(member_name, text)] for every CSV in the zip. NSE sometimes bundles earlier days' files into one zip
    (e.g. 1-2 Jul 2025). If the central directory is damaged (stray leading bytes), scan local file headers instead."""
    try:
        with zipfile.ZipFile(path) as z:
            return [(n, z.read(n).decode("utf-8", "ignore")) for n in z.namelist() if n.lower().endswith(".csv")], "ok"
    except Exception:
        b = open(path, "rb").read()
        out, i = [], b.find(b"PK\x03\x04")
        while i >= 0:
            method, csize = struct.unpack("<H", b[i+8:i+10])[0], struct.unpack("<I", b[i+18:i+22])[0]
            nlen, xlen = struct.unpack("<HH", b[i+26:i+30])
            name = b[i+30:i+30+nlen].decode("utf-8", "ignore")
            start = i + 30 + nlen + xlen
            if name.lower().endswith(".csv"):
                try:
                    data = b[start:start+csize]
                    txt = zlib.decompressobj(-15).decompress(data) if method == 8 else data
                    out.append((name, txt.decode("utf-8", "ignore")))
                except Exception:
                    pass
            i = b.find(b"PK\x03\x04", i + 4)
        if not out:
            raise ValueError("no readable csv member")
        return out, "recovered"


def file_date(path):
    m = re.search(r"(\d{8})", os.path.basename(path))
    return pd.to_datetime(m.group(1), format="%d%m%Y")


def read_combineoi(path):
    members, how = zip_members(path)
    frames = []
    for name, raw in members:
        df = pd.read_csv(io.StringIO(raw), skipinitialspace=True, dtype=str)
        df = df.loc[:, [c for c in df.columns if not str(c).startswith("Unnamed")]]
        df.columns = [c.strip().lower() for c in df.columns]
        ren = {"date": "inner_date", "isin": "isin", "scrip name": "name", "nse symbol": "symbol", "mwpl": "mwpl",
               "open interest": "oi", "future equivalent open interest": "futeq_oi", "limit for next day": "limit_next_day"}
        df = df.rename(columns=ren)
        df = df[[c for c in ren.values() if c in df.columns]].copy()
        for c in ["mwpl", "oi", "futeq_oi"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
        df["date"] = file_date(name) if re.search(r"\d{8}", name) else file_date(path)
        df["inner_date"] = df["inner_date"].map(parse_date)
        df["symbol"] = df["symbol"].astype(str).str.strip()
        df["no_fresh_next_day"] = df["limit_next_day"].astype(str).str.contains("No Fresh", case=False, na=False)
        df["file"] = os.path.basename(path) + ":" + name
        df["zip_status"] = how
        df["own_member"] = file_date(name) == file_date(path) if re.search(r"\d{8}", name) else True
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def read_secban(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Trade Date\s+(\d{1,2}-[A-Za-z]{3}-\d{2,4})", txt)
    inner = parse_date(m.group(1)) if m else pd.NaT
    syms = [ln.split(",")[1].strip() for ln in txt.splitlines()[1:] if "," in ln and ln.split(",")[1].strip()]
    return pd.DataFrame({"date": file_date(path), "inner_date": inner, "symbol": syms})


def main(raw, out):
    os.makedirs(out, exist_ok=True)
    rep = []
    files = sorted(glob.glob(os.path.join(raw, "combineoi", "*.zip")))
    frames, bad = [], []
    for f in files:
        try:
            frames.append(read_combineoi(f))
        except Exception as e:
            bad.append((os.path.basename(f), str(e)[:80]))
    panel = pd.concat(frames, ignore_index=True)
    rec = panel.loc[panel["zip_status"] == "recovered", "file"].nunique()
    mis = panel.loc[panel["inner_date"].notna() & (panel["inner_date"] != panel["date"]), ["file", "inner_date"]].drop_duplicates()
    # misdated files: reassign to the inner date if no other file covers it, otherwise drop
    covered = set(panel.loc[panel["inner_date"].isna() | (panel["inner_date"] == panel["date"]), "date"])
    actions = []
    for f, idate in mis.itertuples(index=False):
        if idate not in covered:
            panel.loc[panel["file"] == f, "date"] = idate; covered.add(idate); actions.append((f, str(idate.date()), "reassigned"))
        else:
            panel = panel[panel["file"] != f]; actions.append((f, str(idate.date()), "dropped"))
    rep.append(f"recovered damaged zips: {rec}; misdated files: {actions}")
    nodate = panel.loc[panel["inner_date"].isna(), "file"].nunique()
    rep.append(f"files with unparseable inner date (kept, file-name date used): {nodate}")
    bundled = panel.loc[~panel["own_member"], "file"].unique().tolist()
    rep.append(f"bundled extra members read: {bundled}")
    panel = panel.sort_values("own_member", ascending=False)
    panel = panel.dropna(subset=["date", "symbol"]).drop_duplicates(["date", "symbol"]).sort_values(["date", "symbol"])
    panel = panel.drop(columns=["own_member"])
    # NSE sometimes prints "Not available in NSE-F&O" in the symbol field; restore the symbol from the same ISIN on the
    # nearest date where it is given
    ph = panel["symbol"].str.contains("Not available", case=False, na=False)
    good = panel.loc[~ph & panel["isin"].notna(), ["isin", "date", "symbol"]].sort_values("date")
    fixed = 0
    if ph.any():
        rows = panel.loc[ph, ["isin", "date"]].sort_values("date").reset_index()
        back = pd.merge_asof(rows, good.rename(columns={"symbol": "sym_b"}), on="date", by="isin", direction="backward")
        fwd = pd.merge_asof(rows, good.rename(columns={"symbol": "sym_f"}), on="date", by="isin", direction="forward")
        sym = back["sym_b"].fillna(fwd["sym_f"])
        panel.loc[rows["index"].values, "symbol"] = sym.fillna("UNMAPPED:" + rows["isin"].astype(str)).values
        fixed = int(sym.notna().sum())
    rep.append(f"placeholder symbols ('Not available in NSE-F&O'): {int(ph.sum())}; restored from ISIN: {fixed}")
    panel["_restored"] = ph.values
    n0 = len(panel)
    panel = panel.sort_values("_restored").drop_duplicates(["date", "symbol"]).drop(columns="_restored")
    rep.append(f"restored rows dropped because the symbol already appears that day (old ISIN on an ISIN-change day): {n0 - len(panel)}")
    panel = panel.sort_values(["date", "symbol"])
    panel = panel.drop(columns=["inner_date"])
    panel["util"] = panel["oi"] / panel["mwpl"]
    if "futeq_oi" in panel.columns:
        panel["util_futeq"] = panel["futeq_oi"] / panel["mwpl"]
    rep.append(f"combineoi files: {len(files)}, unreadable: {len(bad)} {bad[:5]}")
    rep.append(f"panel rows: {len(panel)}, dates: {panel['date'].nunique()}, symbols: {panel['symbol'].nunique()}, "
               f"range: {panel['date'].min().date()} to {panel['date'].max().date()}")

    sb = [read_secban(f) for f in sorted(glob.glob(os.path.join(raw, "secban", "*.csv")))]
    ban = pd.concat(sb, ignore_index=True) if sb else pd.DataFrame(columns=["date", "inner_date", "symbol"])
    bmis = ban.loc[ban["inner_date"].notna() & (ban["inner_date"] != ban["date"]), ["date", "inner_date"]].drop_duplicates()
    okb = ban["inner_date"].isna() | (ban["inner_date"] == ban["date"])
    bcovered = set(ban.loc[okb, "date"])
    bact = []
    for fd, idt in bmis.itertuples(index=False):
        m = (ban["date"] == fd) & (ban["inner_date"] == idt)
        if idt not in bcovered:
            ban.loc[m, "date"] = idt; okb[m] = True; bcovered.add(idt); bact.append((str(fd.date()), str(idt.date()), "reassigned"))
        else:
            bact.append((str(fd.date()), str(idt.date()), "dropped"))
    rep.append(f"secban files: {len(sb)}; misdated: {bact}")
    ban = ban[okb][["date", "symbol"]].drop_duplicates()
    ban = ban[ban["date"].isin(panel["date"].unique())]
    rep.append(f"ban stock-days on panel trading days: {len(ban)}")

    # consistency: stocks flagged 'No Fresh Positions' on day t should be in the ban list on the next trading day
    dates = sorted(pd.to_datetime(panel["date"].unique()))
    nxt = {d: n for d, n in zip(dates[:-1], dates[1:])}
    flag = panel.loc[panel["no_fresh_next_day"], ["date", "symbol"]].copy()
    flag["date"] = pd.to_datetime(flag["date"]).map(nxt)
    flag = flag.dropna()
    key = lambda df: set(zip(pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d"), df["symbol"]))
    a = key(flag)
    b = key(ban[ban["date"].isin(flag["date"].unique())])
    rep.append(f"flag(t) -> ban list(t+1): flagged {len(a)}, listed {len(b)}, both {len(a & b)}, "
               f"flag-only {len(a - b)}, list-only {len(b - a)}")
    if a - b:
        rep.append(f"  examples flag-only: {sorted(a - b)[:8]}")
    if b - a:
        rep.append(f"  examples list-only: {sorted(b - a)[:8]}")

    cols = [c for c in ["date", "symbol", "isin", "mwpl", "oi", "futeq_oi", "util", "util_futeq", "no_fresh_next_day"] if c in panel]
    outp = panel[cols].copy()
    for c in ["util", "util_futeq"]:
        if c in outp:
            outp[c] = outp[c].round(6)
    for c in ["mwpl", "oi"]:
        outp[c] = outp[c].round(0).astype("Int64")
    if "futeq_oi" in outp:
        outp["futeq_oi"] = outp["futeq_oi"].round(2)
    outp.to_csv(os.path.join(out, "mwpl_oi_panel.csv.gz"), index=False, compression="gzip")
    panel.drop_duplicates("symbol", keep="last")[["symbol", "isin", "name"]].to_csv(
        os.path.join(out, "symbols.csv"), index=False)
    ban.sort_values(["date", "symbol"]).to_csv(os.path.join(out, "ban_days.csv.gz"), index=False, compression="gzip")
    open(os.path.join(out, "build_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
