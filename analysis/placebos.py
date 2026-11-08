"""Placebo checks from the master plan's safeguards (PAP §11.15 C19). Exploratory.

(a) Fake ban dates: actual pre-reform spells shifted 60 trading days later for the same stock (same length), kept if no
    actual ban day of the stock lies within the fake spell or 5 days either side. H7 (C2, pct thresholds) with the fake
    indicator (real ban days dropped); level-effect design (C7) with fake entries.
(b) Index-only reform dates (SEBI 2024/132) and (c) peak-margin dates: the H3 statistic (mean change in stock q80, 40
    trading days each side), ranked against the 30 H3 placebo dates.
Outputs analysis/output/placebos.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, calendar, PROC, ROOT
from h7_onesided import thresholds, design, estimate, fmt
from h3_costs import window_stats, EVENTS
import level_effect as le

OUT = os.path.join(ROOT, "analysis", "output")
REFORM = pd.Timestamp("2025-10-01")
SHIFT = 60


def fake_spells(pos, nT):
    sp = pd.read_csv(os.path.join(PROC, "ban_spells.csv.gz"), parse_dates=["start", "end"])
    sp = sp[(sp["start"] >= "2015-01-01") & (sp["start"] < REFORM)].copy()
    sp["i0"] = sp["start"].map(pos); sp["i1"] = sp["end"].map(pos)
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    B["i"] = B["date"].map(pos)
    real = B.groupby("symbol")["i"].apply(set).to_dict()
    rows = []
    for r in sp.itertuples():
        a, b = r.i0 + SHIFT, r.i1 + SHIFT
        if b >= nT:
            continue
        rs = real.get(r.symbol, set())
        if any(j in rs for j in range(a - 5, b + 6)):
            continue
        rows.append((r.symbol, a, b))
    return pd.DataFrame(rows, columns=["symbol", "i0", "i1"])


def main():
    days, pos = calendar()
    nT = len(days)
    S = basis_sample()
    F = fake_spells(pos, nT)
    fake = set((s, i) for s, a, b in F.itertuples(index=False) for i in range(a, b + 1))
    r = ["Placebo checks (PAP §11.15 C19). Exploratory.", "",
         f"(a) Fake ban spells: {len(F)} of the pre-reform spells shifted {SHIFT} trading days later without touching a real ban"]
    # H7 with fake bans
    S7 = S[(S["date"] < REFORM) & ~S["ban"]].copy()
    S7["ban"] = [(s, i) in fake for s, i in zip(S7["symbol"], S7["i"])]
    T = thresholds(S7, "m", "m_lag", "dm", "pct")
    r.append(fmt("  H7 specification with the fake ban indicator (real ban days dropped)", estimate(design(T, "m_lag", "dm"))))
    r.append("  Real H7 for comparison: delta_up -0.089 (0.037), delta_lo +0.081 (0.030).")
    # level effect with fake entries
    D = le.build()
    Cd = le.candidates(D, False)
    rows = []
    for s, a, b in F.itertuples(index=False):
        j = D["sid"].get(s)
        if j is None or a < 25:
            continue
        if D["BAN"][j, a - 5:a].any() or np.isnan(D["M"]["m"][j, a - 1]):
            continue
        w = le.omega_path(D, j, a)
        if w is None or np.isnan(w).any():
            continue
        vol = np.nansum(D["VOL"][j, a - 5:a]); doi = np.nansum(D["DOI"][j, a - 5:a])
        rows.append(dict(symbol=s, j=j, i0=a, L=b - a + 1, date=days[a], C=doi / vol if vol > 0 else np.nan,
                         x=np.r_[w, D["M"]["m"][j, a - 1]], imputed=False))
    E = pd.DataFrame(rows)
    Mi = le.match(E, Cd)
    ks, P = le.paths(D, E, Cd, Mi, "m")
    E["D"] = le.main_stat(E, ks, P)
    res, _ = le.analyse(E, "  Level-effect design with fake entries")
    r += res
    r.append("  Real level effect for comparison: mean D -6.3; C<=0 +8.4, C>0 -6.8; difference -15.2.")
    # (b), (c) dated placebos with the H3 statistic
    first, last = int(S["i"].min()) + 40, int(S["i"].max()) - 39
    true_i = [int(days.searchsorted(pd.Timestamp(d))) for d, _ in EVENTS.values()]
    pl = []
    for i0 in range(first, last + 1, 80):
        if any(abs(i0 - j) < 80 for j in true_i):
            continue
        w = window_stats(S, i0)
        if len(w) >= 50:
            pl.append(w["d80"].mean())
    pv = np.array(pl)
    r += ["", f"(b), (c) Dated placebos, H3 statistic (mean change in stock 80th percentile, bp); reference: {len(pv)} H3 placebo dates, "
              f"mean {pv.mean():+.2f}, sd {pv.std():.2f}"]
    dated = [("index reform: contract size, weekly expiries, ELM (20 Nov 2024)", "2024-11-20"),
             ("index reform: upfront premium, calendar spread (1 Feb 2025)", "2025-02-01"),
             ("index reform: intraday index position monitoring (1 Apr 2025)", "2025-04-01"),
             ("peak margin 25% (1 Dec 2020)", "2020-12-01"), ("peak margin 50% (1 Mar 2021)", "2021-03-01"),
             ("peak margin 75% (1 Jun 2021)", "2021-06-01"), ("peak margin 100% (1 Sep 2021)", "2021-09-01")]
    for lab, d in dated:
        i0 = int(days.searchsorted(pd.Timestamp(d)))
        w = window_stats(S, i0)
        v = w["d80"].mean()
        near = [k for k, (dd, _) in EVENTS.items() if abs(int(days.searchsorted(pd.Timestamp(dd))) - i0) < 80]
        r.append(f"  {lab:62s} (event day {days[i0].date()}): stocks {len(w)}, mean d80 {v:+.2f}, mean d20 {w['d20'].mean():+.2f}, "
                 f"median d50 {w['d50'].mean():+.2f}; share of placebos with |value| >= |this| {(np.abs(pv - pv.mean()) >= abs(v - pv.mean())).mean():.2f}"
                 + (f"; window overlaps STT event {near}" if near else ""))
    txt = "\n".join(r)
    open(os.path.join(OUT, "placebos.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
