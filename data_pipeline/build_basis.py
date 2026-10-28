"""Build the stock-day futures-cash basis panel (outcome side). Nothing here uses ban status or utilisation.

Usage: python3 -I build_basis.py RAW_DIR OUT_DIR
Inputs: RAW/prices/{fut,cash}/YYYYMMDD.csv, RAW/corpactions/ca_YYYYMM.json, RAW/rates/INDIR3TIB01STM.csv
Main measure (pre-registered): basis from daily VWAPs,
    m = ln F_vwap - ln(S_vwap - PV(D)) - r * tau,
with D = cash dividends going ex in (t, expiry], r = 3-month interbank rate (monthly, OECD), tau = calendar days / 365.
Also: close-based basis (secondary; NSE uses a theoretical settlement price when a contract does not trade in the last half
hour, flagged via zero contracts/trades) and the relative implied repo rate (stock's implied rate minus the day's median).
"""
import glob, json, math, os, re, sys
from functools import reduce
from math import gcd
import numpy as np
import pandas as pd

DIV_RE = re.compile(r"dividend[^0-9]{0,25}?(?:rs|re|inr)\.?\s*([0-9]+(?:\.[0-9]+)?)", re.I)


def load_dir(path, usecols=None):
    fs = sorted(glob.glob(os.path.join(path, "*.csv")))
    frames = [pd.read_csv(f, usecols=usecols) for f in fs if os.path.getsize(f) > 0]
    return pd.concat(frames, ignore_index=True)


def dividends(raw):
    rows = []
    for f in sorted(glob.glob(os.path.join(raw, "corpactions", "*.json"))):
        for r in json.load(open(f)):
            if r.get("series") not in (None, "EQ", "BE", "BZ"):
                continue
            amts = [float(a) for a in DIV_RE.findall(r.get("subject", ""))]
            if amts and r.get("exDate") not in (None, "-"):
                rows.append((r["symbol"].strip(), pd.to_datetime(r["exDate"], format="%d-%b-%Y"), sum(amts)))
    d = pd.DataFrame(rows, columns=["symbol", "ex", "div"]).drop_duplicates()
    return d.groupby(["symbol", "ex"], as_index=False)["div"].max()   # same event listed twice (e.g. 'purpose revised')


EVENT_RE = re.compile(r"bonus|split|sub-division|rights|debenture|demerger|scheme|capital reduction|buy ?back|"
                      r"distribution|amalgamation|merger|reduction", re.I)


def other_events(raw):
    """Non-dividend corporate events that change what the stock holder receives (bonus debentures, splits, rights, ...)."""
    rows = []
    for f in sorted(glob.glob(os.path.join(raw, "corpactions", "*.json"))):
        for r in json.load(open(f)):
            if EVENT_RE.search(r.get("subject", "")) and r.get("exDate") not in (None, "-"):
                rows.append((r["symbol"].strip(), pd.to_datetime(r["exDate"], format="%d-%b-%Y")))
    return pd.DataFrame(rows, columns=["symbol", "ex"]).drop_duplicates()


def lot_sizes(fut):
    """Legacy files lack lot size: OI and change in OI are whole multiples of the lot, so take their gcd per contract."""
    leg = fut[fut["src"] == "legacy"]
    vals = pd.concat([leg[["symbol", "expiry", "oi"]].rename(columns={"oi": "v"}),
                      leg[["symbol", "expiry", "chg_oi"]].rename(columns={"chg_oi": "v"})])
    vals = vals[vals["v"].notna() & (vals["v"] != 0)]
    vals["v"] = vals["v"].abs().round().astype("int64")
    g = vals.groupby(["symbol", "expiry"])["v"].apply(lambda s: reduce(gcd, s.tolist())).rename("lot_gcd")
    return g.reset_index()


def main(raw, out):
    os.makedirs(out, exist_ok=True)
    rep = []
    fut = load_dir(os.path.join(raw, "prices", "fut"))
    fut["date"] = pd.to_datetime(fut["date"]); fut["expiry"] = pd.to_datetime(fut["expiry"])
    lots = lot_sizes(fut)
    fut = fut.merge(lots, on=["symbol", "expiry"], how="left")
    contracts = np.where(fut["src"] == "udiff", fut["qty"], fut["contracts"])
    fut["n_contracts"] = contracts
    # the true lot is a multiple of the gcd; when the lot changes within a contract's life (splits, lot revisions) the gcd
    # falls below it, so snap a daily estimate (value / (contracts x mid price)) to the nearest multiple of the gcd
    mid = (fut["low"] + fut["high"]) / 2
    est = fut["value_rs"] / (fut["n_contracts"] * mid.where(mid > 0))
    mult = np.maximum(np.round(est / fut["lot_gcd"]), 1)
    lot_legacy = np.where(np.isfinite(mult), fut["lot_gcd"] * mult, fut["lot_gcd"])
    fut["lot_used"] = np.where(fut["src"] == "udiff", fut["lot"], lot_legacy)
    fut["lot_snapped"] = (fut["src"] == "legacy") & np.isfinite(mult) & (mult != 1)
    rep.append(f"legacy rows whose lot was snapped above the gcd (range check not independent for these): "
               f"{fut.loc[fut['src'] == 'legacy', 'lot_snapped'].mean():.4f}")
    fut["F_vwap"] = fut["value_rs"] / (fut["n_contracts"] * fut["lot_used"])
    fut.loc[fut["n_contracts"] <= 0, "F_vwap"] = np.nan
    inr = (fut["F_vwap"] >= fut["low"] * 0.995) & (fut["F_vwap"] <= fut["high"] * 1.005)
    traded = fut["F_vwap"].notna()
    rep.append(f"futures rows {len(fut)}; with trades {traded.sum()}; F_vwap inside [low, high] (±0.5%): "
               f"{inr[traded].mean():.4f}")
    fut.loc[traded & ~inr, "F_vwap"] = np.nan          # lot-size failures (e.g. mid-contract lot revisions) dropped

    # near / next contract per day
    fut = fut.sort_values(["date", "symbol", "expiry"])
    fut["k"] = fut.groupby(["date", "symbol", "inst"]).cumcount()
    fut = fut[fut["k"] <= 1]

    cash = load_dir(os.path.join(raw, "prices", "cash"), usecols=["date", "symbol", "series", "close", "qty", "value_rs", "trades"])
    cash["date"] = pd.to_datetime(cash["date"])
    cash["pri"] = cash["series"].map({"EQ": 0, "BE": 1, "BZ": 2})
    cash = cash.sort_values("pri").drop_duplicates(["date", "symbol"]).drop(columns="pri")
    cash["S_vwap"] = cash["value_rs"] / cash["qty"]
    cash = cash.rename(columns={"close": "S_close", "qty": "S_qty", "value_rs": "S_value", "trades": "S_trades"})

    stf = fut[fut["inst"] == "STF"].merge(cash, on=["date", "symbol"], how="left")
    rep.append(f"stock-futures rows (near+next) {len(stf)}; matched to cash {stf['S_vwap'].notna().mean():.4f}")

    # rate: monthly 3-month interbank (% p.a.), applied to all days of the month
    rt = pd.read_csv(os.path.join(raw, "rates", "INDIR3TIB01STM.csv"))
    rt.columns = ["month", "r"]; rt["month"] = pd.to_datetime(rt["month"]).dt.to_period("M")
    rt["r"] = pd.to_numeric(rt["r"], errors="coerce") / 100
    stf["month"] = stf["date"].dt.to_period("M")
    stf = stf.merge(rt, on="month", how="left")
    stf["tau"] = (stf["expiry"] - stf["date"]).dt.days / 365.0

    # dividends going ex in (t, expiry]
    dv = dividends(raw)
    rep.append(f"dividend events parsed: {len(dv)}")
    m = stf[["date", "symbol", "expiry", "r"]].merge(dv, on="symbol", how="inner")
    m = m[(m["ex"] > m["date"]) & (m["ex"] <= m["expiry"])]
    m["pv"] = m["div"] * np.exp(-m["r"] * (m["ex"] - m["date"]).dt.days / 365.0)
    pv = m.groupby(["date", "symbol", "expiry"], as_index=False)["pv"].sum()
    stf = stf.merge(pv, on=["date", "symbol", "expiry"], how="left")
    stf["pv"] = stf["pv"].fillna(0.0)
    stf["div_yield_in_life"] = stf["pv"] / stf["S_vwap"]
    ev = other_events(raw)
    e = stf[["date", "symbol", "expiry"]].merge(ev, on="symbol", how="inner")
    e = e[(e["ex"] > e["date"]) & (e["ex"] <= e["expiry"])].drop_duplicates(["date", "symbol", "expiry"])
    e["event_in_life"] = True
    stf = stf.merge(e[["date", "symbol", "expiry", "event_in_life"]], on=["date", "symbol", "expiry"], how="left")
    stf["event_in_life"] = stf["event_in_life"].fillna(False).astype(bool)
    rep.append(f"non-dividend corporate events parsed: {len(ev)}; stock-futures rows with such an event in the contract life: "
               f"{stf['event_in_life'].mean():.4f}")

    stf["m_vwap"] = np.log(stf["F_vwap"]) - np.log(stf["S_vwap"] - stf["pv"]) - stf["r"] * stf["tau"]
    theo = np.where(stf["src"] == "udiff", stf["trades"].fillna(0) == 0, stf["n_contracts"].fillna(0) == 0)
    stf["theoretical_settle"] = theo
    stf["m_close"] = np.log(stf["close"]) - np.log(stf["S_close"] - stf["pv"]) - stf["r"] * stf["tau"]
    stf["r_implied"] = (np.log(stf["F_vwap"]) - np.log(stf["S_vwap"] - stf["pv"])) / stf["tau"].where(stf["tau"] > 0)
    ok = stf["tau"] >= 7 / 365
    med = stf[ok].groupby(["date", "k"])["r_implied"].median().rename("r_med").reset_index()
    stf = stf.merge(med, on=["date", "k"], how="left")
    stf["rel_repo"] = stf["r_implied"] - stf["r_med"]

    keep = ["date", "symbol", "expiry", "k", "tau", "F_vwap", "S_vwap", "close", "S_close", "n_contracts", "lot_used",
            "value_rs", "oi", "chg_oi", "S_qty", "S_value", "S_trades", "r", "pv", "div_yield_in_life", "m_vwap", "m_close",
            "theoretical_settle", "r_implied", "rel_repo", "lot_snapped", "event_in_life", "src"]
    stf[keep].to_csv(os.path.join(out, "basis_panel.csv.gz"), index=False, compression="gzip", float_format="%.8g")

    # index futures (NIFTY) implied rate for validation against the interbank rate
    nif = fut[(fut["inst"] == "IDF") & (fut["symbol"] == "NIFTY") & (fut["k"] == 0)][["date", "expiry", "F_vwap", "close", "underlying", "n_contracts"]]
    nif.to_csv(os.path.join(out, "nifty_futures.csv.gz"), index=False, compression="gzip")

    # outcome-only validation (no treatment variables)
    v = stf[(stf["k"] == 0) & stf["m_vwap"].notna() & (stf["n_contracts"] >= 5)]
    rep.append(f"near-month usable stock-days (>=5 contracts): {len(v)}")
    c = v[~v["event_in_life"] & (v["pv"] == 0)]
    rep.append(f"CLEAN near-month sample (no dividend or other corporate event in contract life): n={len(c)}, "
               f"median {c['m_vwap'].median()*1e4:.1f} bp, p10 {c['m_vwap'].quantile(.1)*1e4:.1f}, "
               f"p90 {c['m_vwap'].quantile(.9)*1e4:.1f}, share |m|>200bp {(c['m_vwap'].abs() > 0.02).mean():.4f}")
    q = v.groupby(v["date"].dt.year)["m_vwap"].describe(percentiles=[.1, .5, .9])[["count", "10%", "50%", "90%"]] * [1, 1e4, 1e4, 1e4]
    rep.append("basis m_vwap by year (bp):\n" + q.round(1).to_string())
    bins = pd.cut(v["tau"] * 365, [0, 3, 7, 14, 21, 35, 70], right=True)
    conv = v.groupby(bins, observed=True)["m_vwap"].agg(["count", "median", lambda s: s.abs().median()]) * [1, 1e4, 1e4]
    conv.columns = ["count", "median_bp", "median_abs_bp"]
    rep.append("convergence by calendar days to expiry (bp):\n" + conv.round(1).to_string())
    rep.append(f"share of near-month rows with theoretical settlement flag: {stf.loc[stf['k']==0,'theoretical_settle'].mean():.4f}")
    open(os.path.join(out, "basis_report.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
