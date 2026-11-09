"""Download AMFI monthly reports (Excel), April 2018 onward, and extract the arbitrage-fund category row.

Source: https://portal.amfiindia.com/spages/am{mon}{yyyy}repo.xls (Dec 2021 and Jan 2022: ...reporevised.xls).
Output: data/raw/amfi_monthly/*.xls and data/processed/amfi_arbitrage_monthly.csv (month, schemes, folios, funds
mobilised, redemptions, net inflow, net AUM, average AUM; INR crore).
Usage: python3 -I data_pipeline/download_amfi_monthly.py data/raw/amfi_monthly data/processed
"""
import os, sys, time, urllib.request
import numpy as np
import pandas as pd

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def fetch(url, fn):
    if os.path.exists(fn) and os.path.getsize(fn) > 1000:
        return True
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                data = r.read()
            if len(data) < 1000 or data[:5].lower() in (b"<!doc", b"<html"):
                return False
            open(fn, "wb").write(data)
            return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            time.sleep(2 ** k)
        except Exception:
            time.sleep(2 ** k)
    return False


def read_any(fn):
    for eng in ("xlrd", "openpyxl"):
        try:
            return pd.read_excel(fn, sheet_name=None, header=None, engine=eng)
        except Exception:
            continue
    return {}


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return np.nan


def extract(fn):
    """Return dict of arbitrage-fund figures, trying the post-2018 layout (row 'Arbitrage Fund' with 7 numeric columns
    after the name) and the April-2018-style layout (sheet 'red+assets')."""
    sheets = read_any(fn)
    if "red+assets" in sheets:
        # April 2018 to March 2019 layout: Table 3 (redemptions, net inflow) and Table 4 (net assets) on one sheet
        d = sheets["red+assets"]
        idx = [i for i in range(len(d)) if str(d.iloc[i, 0]).strip().lower().startswith("arbitrage fund")]
        if len(idx) >= 2:
            red, net, aum = num(d.iloc[idx[0], 4]), num(d.iloc[idx[0], 5]), num(d.iloc[idx[1], 4])
            return dict(schemes=np.nan, folios=np.nan, mobilised=red + net, redeemed=red, net_inflow=net, aum=aum,
                        aaum=np.nan, layout="table3_4", sheet="red+assets")
    for name, d in sheets.items():
        txt = d.astype(str)
        for i in range(len(d)):
            row = list(d.iloc[i])
            labels = [str(x).strip() for x in row]
            for j, lab in enumerate(labels):
                if lab.lower().startswith("arbitrage fund") and "of fund" not in lab.lower():
                    vals = [num(v) for v in row[j + 1:]]
                    vals = [v for v in vals if np.isfinite(v)]
                    if len(vals) >= 7:
                        return dict(schemes=vals[0], folios=vals[1], mobilised=vals[2], redeemed=vals[3],
                                    net_inflow=vals[4], aum=vals[5], aaum=vals[6], layout="row7", sheet=name)
    return None


def main(raw, out):
    os.makedirs(raw, exist_ok=True)
    rows, missing = [], []
    for y in range(2018, 2027):
        for mi, m in enumerate(MON):
            per = pd.Period(f"{y}-{mi + 1:02d}", "M")
            if per < pd.Period("2018-04", "M") or per > pd.Period("2026-09", "M"):
                continue
            fn = os.path.join(raw, f"am{m}{y}repo.xls")
            ok = fetch(f"https://portal.amfiindia.com/spages/am{m}{y}repo.xls", fn)
            if not ok:
                ok = fetch(f"https://portal.amfiindia.com/spages/am{m}{y}reporevised.xls", fn)
            if not ok:
                missing.append(str(per)); continue
            e = extract(fn)
            if e is None:
                missing.append(str(per) + " (no row)"); continue
            e["month"] = str(per)
            rows.append(e)
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(out, "amfi_arbitrage_monthly.csv"), index=False)
    print(f"months parsed {len(D)}; missing/unparsed: {missing}")
    print(D[["month", "schemes", "net_inflow", "aum", "aaum"]].to_string())


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
