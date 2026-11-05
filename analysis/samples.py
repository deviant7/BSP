"""Shared analysis samples for the pre-registered tests (plan/pre_analysis_plan_v1.md, §2, §3 and §11 C1).

basis_sample(): one row per stock-day with the chosen futures contract, its basis m_t, the same contract's m_(t-1),
    validity filters, winsorised levels, the ban indicator for day t and utilisation omega_(t-1).
futures_activity(): one row per F&O stock-day with near+next futures volume and change in open interest (contracts),
    cash volume and delivery share, the ban indicator and omega_(t-1)  (for H8).

Usage (from the repo root):  python3 -I analysis/samples.py      -> builds both, caches them, writes a counts report.
Caches go to data/processed/cache/ (git-ignored).
"""
import glob, os, sys
import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROC = os.path.join(ROOT, "data", "processed")
RAW = os.path.join(ROOT, "data", "raw")
CACHE = os.path.join(PROC, "cache")
REFORM = pd.Timestamp("2025-10-01")


def calendar():
    d = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date"])["date"].unique()
    days = pd.DatetimeIndex(sorted(pd.to_datetime(d)))
    return days, pd.Series(np.arange(len(days)), index=days)


def treatment(days, pos):
    """Ban indicator for day t and omega_(t-1) from the previous trading day's file (C1 f)."""
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "util", "util_futeq"],
                    parse_dates=["date"])
    P["omega"] = np.where(P["date"] >= REFORM, P["util_futeq"], P["util"])
    P["i"] = P["date"].map(pos)
    lag = P[["symbol", "i", "omega"]].copy()
    lag["i"] = lag["i"] + 1                       # value of day i-1 attached to day i
    lag = lag.rename(columns={"omega": "omega_lag"})
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["ban"] = True
    B = B.rename(columns={"source": "ban_source"})
    return lag, B


def entry_window(pos):
    """Trading days 1-20 of a membership spell that starts with an F&O entry event (C1 c)."""
    E = pd.read_csv(os.path.join(PROC, "fno_events.csv"), parse_dates=["date"])
    E = E[E["type"] == "entry"]
    rows = []
    for d, s in zip(E["date"], E["symbol"]):
        if d in pos.index:
            i0 = pos[d]
            rows += [(s, i) for i in range(i0, i0 + 20)]
    return set(rows)


def basis_sample(rebuild=False):
    path = os.path.join(CACHE, "basis_sample.pkl")
    if os.path.exists(path) and not rebuild:
        return pd.read_pickle(path)
    days, pos = calendar()
    cols = ["date", "symbol", "expiry", "k", "tau", "F_vwap", "n_contracts", "pv", "event_in_life", "m_vwap", "m_close",
            "rel_repo", "r_filled", "theoretical_settle", "oi", "lot_used", "src"]
    X = pd.read_csv(os.path.join(PROC, "basis_panel.csv.gz"), usecols=cols, parse_dates=["date", "expiry"])
    X["i"] = X["date"].map(pos)
    X["i_exp"] = pos.reindex(X["expiry"]).values
    # expiry not a trading day in the calendar (should not happen): first trading day before it
    miss = X["i_exp"].isna()
    if miss.any():
        X.loc[miss, "i_exp"] = days.searchsorted(X.loc[miss, "expiry"], side="right") - 1
    X["d_exp"] = (X["i_exp"] - X["i"]).astype(int)            # trading days after t up to and including expiry
    win = entry_window(pos)
    X["entry20"] = [(s, i) in win for s, i in zip(X["symbol"], X["i"])]
    X["valid"] = ((X["n_contracts"] >= 5) & X["F_vwap"].notna() & X["m_vwap"].notna() & (X["pv"] == 0)
                  & ~X["event_in_life"].astype(bool) & ~X["entry20"])
    # chosen contract on day t: near if d > 3, else next (C1 a)
    near = X[X["k"] == 0][["symbol", "i", "expiry", "d_exp"]].rename(columns={"expiry": "near_exp", "d_exp": "near_d"})
    X = X.merge(near, on=["symbol", "i"], how="left")
    X["chosen"] = np.where(X["near_d"] > 3, X["k"] == 0, X["k"] == 1)
    # lag of the same contract on the previous trading day (C1 d)
    L = X[["symbol", "expiry", "i", "m_vwap", "m_close", "rel_repo", "valid"]].copy()
    L["i"] = L["i"] + 1
    L = L.rename(columns={"m_vwap": "m_lag_raw", "m_close": "mclose_lag_raw", "rel_repo": "repo_lag_raw",
                          "valid": "lag_valid"})
    S = X[X["chosen"]].merge(L, on=["symbol", "expiry", "i"], how="left")
    S["lag_valid"] = S["lag_valid"].fillna(False).astype(bool)
    S = S[S["valid"]].copy()
    # winsorise by calendar year on the chosen-contract sample (C1 e)
    S["year"] = S["date"].dt.year
    q = S.groupby("year")["m_vwap"].quantile([0.01, 0.99]).unstack()
    S["m"] = S["m_vwap"].clip(S["year"].map(q[0.01]), S["year"].map(q[0.99]))
    lag_year = days[(S["i"] - 1).clip(lower=0).values].year
    S["m_lag"] = S["m_lag_raw"].clip(pd.Series(lag_year, index=S.index).map(q[0.01]),
                                     pd.Series(lag_year, index=S.index).map(q[0.99]))
    S.loc[~S["lag_valid"], ["m_lag", "m_lag_raw", "mclose_lag_raw", "repo_lag_raw"]] = np.nan
    S["dm"] = S["m"] - S["m_lag"]
    S["dm_raw"] = S["m_vwap"] - S["m_lag_raw"]
    # robustness outcomes (close-based basis, relative implied repo), winsorised the same way
    for cur, lagc, out in [("m_close", "mclose_lag_raw", "mc"), ("rel_repo", "repo_lag_raw", "rr")]:
        qq = S.groupby("year")[cur].quantile([0.01, 0.99]).unstack()
        S[out] = S[cur].clip(S["year"].map(qq[0.01]), S["year"].map(qq[0.99]))
        ly = pd.Series(lag_year, index=S.index)
        S[out + "_lag"] = S[lagc].clip(ly.map(qq[0.01]), ly.map(qq[0.99]))
    lag, B = treatment(days, pos)
    S = S.merge(lag, on=["symbol", "i"], how="left")
    S = S.merge(B, on=["date", "symbol"], how="left")
    S["ban"] = S["ban"].fillna(False).astype(bool)
    S["post"] = S["date"] >= REFORM
    S = S.drop(columns=["valid", "chosen", "near_exp"])
    os.makedirs(CACHE, exist_ok=True)
    S.to_pickle(path)
    return S


def futures_activity(rebuild=False):
    path = os.path.join(CACHE, "futures_activity.pkl")
    if os.path.exists(path) and not rebuild:
        return pd.read_pickle(path)
    days, pos = calendar()
    X = pd.read_csv(os.path.join(PROC, "basis_panel.csv.gz"),
                    usecols=["date", "symbol", "expiry", "k", "n_contracts", "chg_oi", "oi", "lot_used", "S_qty"],
                    parse_dates=["date", "expiry"])
    X["d_oi"] = X["chg_oi"] / X["lot_used"]
    X["oi_c"] = X["oi"] / X["lot_used"]
    near = X[X["k"] == 0][["date", "symbol", "expiry", "S_qty"]].rename(columns={"expiry": "near_exp"})
    agg = X.groupby(["date", "symbol"]).agg(vol=("n_contracts", "sum"), d_oi=("d_oi", "sum"), oi_c=("oi_c", "sum"),
                                             n_rows=("k", "size")).reset_index()
    A = agg.merge(near, on=["date", "symbol"], how="left")
    A["expiry_day"] = A["date"] == A["near_exp"]
    A["R"] = np.where(A["vol"] > 0, (A["d_oi"] + A["vol"]) / A["vol"].where(A["vol"] > 0), np.nan)
    # delivery share, EQ series
    D = []
    for f in sorted(glob.glob(os.path.join(RAW, "prices", "deliv", "*.csv"))):
        if os.path.getsize(f) == 0:
            continue
        d = pd.read_csv(f)
        D.append(d[d["series"] == "EQ"][["date", "symbol", "qty_traded", "deliv_qty"]])
    D = pd.concat(D, ignore_index=True)
    D["date"] = pd.to_datetime(D["date"])
    D["deliv_share"] = D["deliv_qty"] / D["qty_traded"].where(D["qty_traded"] > 0)
    A = A.merge(D[["date", "symbol", "deliv_share"]], on=["date", "symbol"], how="left")
    A["i"] = A["date"].map(pos)
    lag, B = treatment(days, pos)
    A = A.merge(lag, on=["symbol", "i"], how="left").merge(B, on=["date", "symbol"], how="left")
    A["ban"] = A["ban"].fillna(False).astype(bool)
    A["post"] = A["date"] >= REFORM
    os.makedirs(CACHE, exist_ok=True)
    A.to_pickle(path)
    return A


def report(S, A):
    r = []
    r.append(f"basis sample (chosen contract, valid): {len(S)} stock-days, {S['symbol'].nunique()} stocks, "
             f"{S['date'].min().date()} to {S['date'].max().date()}")
    r.append(f"  chosen = next contract (near has <= 3 trading days left): {(S['k'] == 1).mean():.3f}")
    r.append(f"  with a valid same-contract lag (Delta m defined): {S['dm'].notna().sum()}")
    r.append(f"  ban days: {int(S['ban'].sum())} (with Delta m: {int((S['ban'] & S['dm'].notna()).sum())}); "
             f"imputed ban days: {int((S['ban_source'] == 'imputed').sum())}")
    r.append(f"  post 1 Oct 2025: {int(S['post'].sum())} stock-days, ban {int((S['ban'] & S['post']).sum())}")
    r.append(f"  r_filled rows: {int(S['r_filled'].sum())}; omega_lag missing: {int(S['omega_lag'].isna().sum())}")
    r.append(f"futures activity: {len(A)} stock-days; expiry days {int(A['expiry_day'].sum())}; ban days {int(A['ban'].sum())}; "
             f"delivery share present {A['deliv_share'].notna().mean():.3f}")
    return "\n".join(r)


if __name__ == "__main__":
    S = basis_sample(rebuild=True)
    A = futures_activity(rebuild=True)
    txt = report(S, A)
    os.makedirs(os.path.join(ROOT, "analysis", "output"), exist_ok=True)
    open(os.path.join(ROOT, "analysis", "output", "sample_report.txt"), "w").write(txt + "\n")
    print(txt)
