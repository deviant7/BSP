"""Build the stock-day MWPL / open-interest / ban panel from NSE combineoi and fo_secban files.

Treatment-side only (MWPL, OI, utilisation, ban status). No prices or mispricing outcomes.
Usage: python3 -I build_mwpl_panel.py RAW_DIR OUT_DIR
Outputs (OUT_DIR):
  mwpl_oi_panel.csv.gz   one row per (date, symbol): mwpl, oi, futeq_oi, util, util_futeq, limit_next_day, no_fresh_next_day
  ban_days.csv.gz        one row per (trade date, symbol) in the official securities-in-ban list
  build_report.txt       parsing counts and consistency checks
"""
import glob, io, os, re, sys, zipfile
import pandas as pd


def read_combineoi(path):
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        raw = z.read(name).decode("utf-8", "ignore")
    df = pd.read_csv(io.StringIO(raw), skipinitialspace=True, dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]
    ren = {"date": "date", "isin": "isin", "scrip name": "name", "nse symbol": "symbol", "mwpl": "mwpl",
           "open interest": "oi", "future equivalent open interest": "futeq_oi", "limit for next day": "limit_next_day"}
    df = df.rename(columns=ren)
    keep = [c for c in ren.values() if c in df.columns]
    df = df[keep].copy()
    for c in ["mwpl", "oi", "futeq_oi"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].str.replace(",", ""), errors="coerce")
    df["date"] = pd.to_datetime(df["date"].str.strip(), format="%d-%b-%Y", errors="coerce")
    df["symbol"] = df["symbol"].str.strip()
    df["no_fresh_next_day"] = df["limit_next_day"].str.contains("No Fresh", case=False, na=False)
    df["file"] = os.path.basename(path)
    return df


def read_secban(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Trade Date\s+(\d{2}-[A-Z]{3}-\d{4})", txt, re.I)
    if not m:
        return pd.DataFrame(columns=["date", "symbol"])
    date = pd.to_datetime(m.group(1).title(), format="%d-%b-%Y")
    syms = [ln.split(",", 1)[1].strip() for ln in txt.splitlines()[1:] if "," in ln and ln.split(",", 1)[1].strip()]
    return pd.DataFrame({"date": date, "symbol": syms})


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
    panel = panel.dropna(subset=["date", "symbol"]).drop_duplicates(["date", "symbol"]).sort_values(["date", "symbol"])
    panel["util"] = panel["oi"] / panel["mwpl"]
    if "futeq_oi" in panel.columns:
        panel["util_futeq"] = panel["futeq_oi"] / panel["mwpl"]
    rep.append(f"combineoi files: {len(files)}, unreadable: {len(bad)} {bad[:5]}")
    rep.append(f"panel rows: {len(panel)}, dates: {panel['date'].nunique()}, symbols: {panel['symbol'].nunique()}, "
               f"range: {panel['date'].min().date()} to {panel['date'].max().date()}")

    sb = [read_secban(f) for f in sorted(glob.glob(os.path.join(raw, "secban", "*.csv")))]
    ban = pd.concat(sb, ignore_index=True).drop_duplicates() if sb else pd.DataFrame(columns=["date", "symbol"])
    rep.append(f"secban files: {len(sb)}, ban stock-days: {len(ban)}")

    # consistency: stocks flagged 'No Fresh Positions' on day t should be in the ban list on the next trading day
    dates = sorted(panel["date"].unique())
    nxt = dict(zip(dates[:-1], dates[1:]))
    flag = panel.loc[panel["no_fresh_next_day"], ["date", "symbol"]].copy()
    flag["date"] = flag["date"].map(nxt)
    flag = flag.dropna()
    a = set(map(tuple, flag[["date", "symbol"]].astype(str).values))
    b = set(map(tuple, ban[ban["date"].isin(flag["date"].unique())][["date", "symbol"]].astype(str).values))
    inter = len(a & b)
    rep.append(f"flag(t) -> ban list(t+1): flagged {len(a)}, listed {len(b)}, both {inter}, "
               f"flag-only {len(a - b)}, list-only {len(b - a)}")

    panel.to_csv(os.path.join(out, "mwpl_oi_panel.csv.gz"), index=False, compression="gzip")
    ban.sort_values(["date", "symbol"]).to_csv(os.path.join(out, "ban_days.csv.gz"), index=False, compression="gzip")
    open(os.path.join(out, "build_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
