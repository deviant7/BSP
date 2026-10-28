"""Download and compact NSE daily price files: F&O bhavcopy (futures rows + options summary), cash bhavcopy (EQ series),
and the security-wise delivery file (MTO). Handles the legacy formats and the UDiFF format (mid-2024 onward).

Usage: python3 -I download_nse_prices.py OUT_DIR START END [workers]
Writes one compact CSV per day and kind under OUT_DIR/{fut,optsum,cash,deliv}/YYYYMMDD.csv; raw zips are not kept.
Building these files is part of the blind data build: nothing here relates prices to bans.
"""
import datetime as dt, io, os, sys, threading, time, urllib.request, urllib.error, zipfile
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
A = "https://nsearchives.nseindia.com/"
MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def get(url, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 ** (k + 1))
        except Exception:
            time.sleep(2 ** (k + 1))
    raise RuntimeError("failed " + url)


def unzip_csv(b):
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        n = [x for x in z.namelist() if x.lower().endswith(".csv")][0]
        return pd.read_csv(io.BytesIO(z.read(n)), dtype=str, skipinitialspace=True)


def fo(d):
    legacy = f"{A}content/historical/DERIVATIVES/{d.year}/{MON[d.month-1]}/fo{d:%d}{MON[d.month-1]}{d.year}bhav.csv.zip"
    udiff = f"{A}content/fo/BhavCopy_NSE_FO_0_0_0_{d:%Y%m%d}_F_0000.csv.zip"
    b = get(legacy)
    if b is not None:
        x = unzip_csv(b); x.columns = [c.strip() for c in x.columns]
        num = ["STRIKE_PR", "OPEN", "HIGH", "LOW", "CLOSE", "SETTLE_PR", "CONTRACTS", "VAL_INLAKH", "OPEN_INT", "CHG_IN_OI"]
        for c in num: x[c] = pd.to_numeric(x[c], errors="coerce")
        fut = x[x["INSTRUMENT"].isin(["FUTSTK", "FUTIDX"])].copy()
        fut = pd.DataFrame({"date": d.isoformat(), "inst": fut["INSTRUMENT"].map({"FUTSTK": "STF", "FUTIDX": "IDF"}),
                            "symbol": fut["SYMBOL"].str.strip(), "expiry": pd.to_datetime(fut["EXPIRY_DT"], format="%d-%b-%Y").dt.date,
                            "open": fut["OPEN"], "high": fut["HIGH"], "low": fut["LOW"], "close": fut["CLOSE"], "last": None,
                            "settle": fut["SETTLE_PR"], "underlying": None, "contracts": fut["CONTRACTS"],
                            "value_rs": fut["VAL_INLAKH"] * 1e5, "qty": None, "trades": None, "oi": fut["OPEN_INT"],
                            "chg_oi": fut["CHG_IN_OI"], "lot": None, "src": "legacy"})
        opt = x[x["INSTRUMENT"].isin(["OPTSTK", "OPTIDX"])]
        osum = opt.groupby(["INSTRUMENT", "SYMBOL"]).agg(contracts=("CONTRACTS", "sum"), value_rs=("VAL_INLAKH", "sum"),
                                                         oi=("OPEN_INT", "sum")).reset_index()
        osum["value_rs"] *= 1e5; osum["date"] = d.isoformat(); osum["src"] = "legacy"
        osum = osum.rename(columns={"INSTRUMENT": "inst", "SYMBOL": "symbol"})
        return fut, osum
    b = get(udiff)
    if b is None:
        return None, None
    x = unzip_csv(b)
    num = ["StrkPric", "OpnPric", "HghPric", "LwPric", "ClsPric", "LastPric", "SttlmPric", "UndrlygPric", "OpnIntrst",
           "ChngInOpnIntrst", "TtlTradgVol", "TtlTrfVal", "TtlNbOfTxsExctd", "NewBrdLotQty"]
    for c in num: x[c] = pd.to_numeric(x[c], errors="coerce")
    fut = x[x["FinInstrmTp"].isin(["STF", "IDF"])]
    fut = pd.DataFrame({"date": d.isoformat(), "inst": fut["FinInstrmTp"], "symbol": fut["TckrSymb"].str.strip(),
                        "expiry": pd.to_datetime(fut["XpryDt"]).dt.date, "open": fut["OpnPric"], "high": fut["HghPric"],
                        "low": fut["LwPric"], "close": fut["ClsPric"], "last": fut["LastPric"], "settle": fut["SttlmPric"],
                        "underlying": fut["UndrlygPric"], "contracts": None, "value_rs": fut["TtlTrfVal"],
                        "qty": fut["TtlTradgVol"], "trades": fut["TtlNbOfTxsExctd"], "oi": fut["OpnIntrst"],
                        "chg_oi": fut["ChngInOpnIntrst"], "lot": fut["NewBrdLotQty"], "src": "udiff"})
    opt = x[x["FinInstrmTp"].isin(["STO", "IDO"])]
    osum = opt.groupby(["FinInstrmTp", "TckrSymb"]).agg(qty=("TtlTradgVol", "sum"), value_rs=("TtlTrfVal", "sum"),
                                                        oi=("OpnIntrst", "sum")).reset_index()
    osum = osum.rename(columns={"FinInstrmTp": "inst", "TckrSymb": "symbol"}); osum["date"] = d.isoformat(); osum["src"] = "udiff"
    return fut, osum


def cash(d):
    legacy = f"{A}content/historical/EQUITIES/{d.year}/{MON[d.month-1]}/cm{d:%d}{MON[d.month-1]}{d.year}bhav.csv.zip"
    udiff = f"{A}content/cm/BhavCopy_NSE_CM_0_0_0_{d:%Y%m%d}_F_0000.csv.zip"
    b = get(legacy)
    if b is not None:
        x = unzip_csv(b); x.columns = [c.strip() for c in x.columns]
        x = x[x["SERIES"].str.strip().isin(["EQ", "BE", "BZ"])]
        out = pd.DataFrame({"date": d.isoformat(), "symbol": x["SYMBOL"].str.strip(), "series": x["SERIES"].str.strip(),
                            "isin": x["ISIN"], "open": x["OPEN"], "high": x["HIGH"], "low": x["LOW"], "close": x["CLOSE"],
                            "last": x["LAST"], "prevclose": x["PREVCLOSE"], "qty": x["TOTTRDQTY"], "value_rs": x["TOTTRDVAL"],
                            "trades": x["TOTALTRADES"], "src": "legacy"})
        return out
    b = get(udiff)
    if b is None:
        return None
    x = unzip_csv(b)
    x = x[x["SctySrs"].str.strip().isin(["EQ", "BE", "BZ"])]
    return pd.DataFrame({"date": d.isoformat(), "symbol": x["TckrSymb"].str.strip(), "series": x["SctySrs"].str.strip(),
                         "isin": x["ISIN"], "open": x["OpnPric"], "high": x["HghPric"], "low": x["LwPric"], "close": x["ClsPric"],
                         "last": x["LastPric"], "prevclose": x["PrvsClsgPric"], "qty": x["TtlTradgVol"],
                         "value_rs": x["TtlTrfVal"], "trades": x["TtlNbOfTxsExctd"], "src": "udiff"})


def deliv(d):
    b = get(f"{A}archives/equities/mto/MTO_{d:%d%m%Y}.DAT")
    if b is None:
        return None
    rows = []
    for ln in b.decode("utf-8", "ignore").splitlines():
        p = [q.strip() for q in ln.split(",")]
        if len(p) >= 7 and p[0] == "20":
            rows.append((d.isoformat(), p[2], p[3], p[4], p[5], p[6]))
    return pd.DataFrame(rows, columns=["date", "symbol", "series", "qty_traded", "deliv_qty", "deliv_pct"])


def main(out, start, end, workers=4):
    for k in ["fut", "optsum", "cash", "deliv"]:
        os.makedirs(os.path.join(out, k), exist_ok=True)
    log = open(os.path.join(out, "price_download_log.tsv"), "a"); lock = threading.Lock()
    days = []
    d, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    while d <= e:
        if d.weekday() < 5 and not os.path.exists(os.path.join(out, "deliv", f"{d:%Y%m%d}.csv")):
            days.append(d)
        d += dt.timedelta(days=1)

    def run(d):
        status = []
        try:
            f, o = fo(d)
            if f is not None:
                f.to_csv(os.path.join(out, "fut", f"{d:%Y%m%d}.csv"), index=False)
                o.to_csv(os.path.join(out, "optsum", f"{d:%Y%m%d}.csv"), index=False)
            status.append("fo:" + ("ok" if f is not None else "404"))
            c = cash(d)
            if c is not None:
                c.to_csv(os.path.join(out, "cash", f"{d:%Y%m%d}.csv"), index=False)
            status.append("cash:" + ("ok" if c is not None else "404"))
            v = deliv(d)
            if v is not None:
                v.to_csv(os.path.join(out, "deliv", f"{d:%Y%m%d}.csv"), index=False)
            else:  # write empty marker so holidays are not retried
                open(os.path.join(out, "deliv", f"{d:%Y%m%d}.csv"), "w").close()
            status.append("deliv:" + ("ok" if v is not None else "404"))
        except Exception as ex:
            status.append("ERR:" + str(ex)[:80])
        with lock:
            log.write(f"{d}\t{' '.join(status)}\n"); log.flush()
        time.sleep(0.3)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(run, days))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4)
