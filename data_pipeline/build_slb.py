"""Parse NSE SLBS bhavcopies into one table (see download_slb.py for the file layout).

Output data/processed/slb_daily.csv.gz: one row per trade date x symbol x series (tenure) with the closing lending fee
(Rs per share), quantity (shares), value (Rs), trades and the SLB contract's expiry date.
Usage: python3 -I data_pipeline/build_slb.py data/raw/slb data/processed
"""
import glob, os, sys
import pandas as pd


def parse(fn):
    rows = []
    for line in open(fn, encoding="latin-1"):
        p = [x.strip() for x in line.split(",")]
        if len(p) < 17 or not p[1]:
            continue
        try:
            rows.append(dict(symbol=p[1], series=p[2], expiry=p[3], fee_open=float(p[6]), fee_high=float(p[7]),
                             fee_low=float(p[8]), fee_close=float(p[9]), qty=float(p[11]), value=float(p[12]),
                             date=p[15], trades=float(p[16])))
        except ValueError:
            continue
    return rows


def main(raw, out):
    files = sorted(glob.glob(os.path.join(raw, "*.dat")))
    rows = []
    for f in files:
        r = parse(f)
        d = pd.Timestamp(os.path.basename(f)[:8])
        for x in r:
            x["file_date"] = d
        rows += r
    D = pd.DataFrame(rows)
    D["date"] = pd.to_datetime(D["date"], format="%d-%b-%Y", errors="coerce")
    D["expiry"] = pd.to_datetime(D["expiry"], format="%d-%b-%Y", errors="coerce")
    bad = (D["date"] != D["file_date"]).sum()
    D["date"] = D["file_date"]
    D = D.drop(columns="file_date")
    D = D[D["qty"] > 0]
    D.to_csv(os.path.join(out, "slb_daily.csv.gz"), index=False)
    rep = [f"SLB bhavcopies parsed: {len(files)} files; rows with trades {len(D)}; symbols {D['symbol'].nunique()}; "
           f"{D['date'].min().date()} to {D['date'].max().date()}; inner trade date differs from file date: {bad}",
           "rows per year: " + ", ".join(f"{k} {v}" for k, v in D.groupby(D['date'].dt.year).size().items()),
           "stocks with any trade per year: " + ", ".join(f"{k} {v}" for k, v in D.groupby(D['date'].dt.year)['symbol'].nunique().items())]
    open(os.path.join(out, "slb_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
