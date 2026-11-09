"""Figures for the thesis chapters and the first-results report (written to reports/figs/).

fig_level_profile.pdf  : level effect, event-time path of treated minus matched controls (bp), by median composition
fig_h9_tails.pdf       : share of non-ban days in the stock's upper and lower tail, by utilisation the day before
fig_band_years.pdf     : pooled threshold-model band edges by calendar year (stock-demeaned basis)
fig_ban_R.pdf          : monthly median of (change in OI + volume) / volume on ban days, with enforcement-regime dates
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, ROOT

FIG = os.path.join(ROOT, "reports", "figs")
INK, MUTED, BLUE, RED = "#222222", "#6b6b6b", "#3a5f86", "#b5473a"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})


def level_profile():
    import level_effect as le
    D = le.build()
    E, _ = le.events(D, False)
    Cd = le.candidates(D, False)
    Mi = le.match(E, Cd)
    ks, P = le.paths(D, E, Cd, Mi, "m")
    hi = (E["C"] > E["C"].median()).values
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    for msk, lab, col, ls in [(np.ones(len(E), bool), "All entries", INK, "-"), (hi, "Fast OI build-up (above median)", RED, "--"),
                              (~hi, "Slow OI build-up (below median)", BLUE, ":")]:
        with np.errstate(all="ignore"):
            ax.plot(ks, np.nanmean(P[msk], axis=0), color=col, lw=1.6, ls=ls, label=lab)
    ax.axvline(-0.5, color=MUTED, lw=0.8)
    ax.axhline(0, color=MUTED, lw=0.6)
    ax.set_xlabel("Trading days relative to the first ban day")
    ax.set_ylabel("Basis change from day -1,\ntreated minus controls (bp)")
    ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)
    ax.grid(axis="y", color="#e6e6e6", lw=0.6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_level_profile.pdf")); plt.close(fig)


def h9_tails():
    S = basis_sample()
    nb = S[(S["date"] < "2025-10-01") & ~S["ban"]]
    low = nb[nb["omega_lag"] < 0.60]
    cnt = low.groupby("symbol").size()
    q = low[low["symbol"].isin(cnt[cnt >= 100].index)].groupby("symbol")["m"].quantile([0.2, 0.8]).unstack()
    A = nb.merge(q, left_on="symbol", right_index=True)
    A = A[A["omega_lag"] < 0.95]
    edges = [0, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    A["bin"] = pd.cut(A["omega_lag"], edges, right=False)
    U = A.groupby("bin", observed=True).apply(lambda g: (g["m"] > g[0.8]).mean())
    L = A.groupby("bin", observed=True).apply(lambda g: (g["m"] < g[0.2]).mean())
    labels = ["< 0.60"] + [f"{a:.2f}-{b:.2f}" for a, b in zip(edges[1:-1], edges[2:])]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.plot(x, U.values, color=RED, lw=1.6, marker="o", ms=4, label="Upper tail (rich futures)")
    ax.plot(x, L.values, color=BLUE, lw=1.6, marker="s", ms=4, label="Lower tail (cheap futures)")
    ax.axhline(0.2, color=MUTED, lw=0.6, ls=":")
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_xlabel("Utilisation of the position limit the day before")
    ax.set_ylabel("Share of days")
    ax.legend(frameon=False, fontsize=7)
    ax.grid(axis="y", color="#e6e6e6", lw=0.6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_h9_tails.pdf")); plt.close(fig)


def band_years():
    B = pd.read_csv(os.path.join(ROOT, "analysis", "output", "band_by_year.csv"))
    B = B[B["year"] <= 2025]
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.fill_between(B["year"], B["gL"], B["gU"], color="#dfe7ef", lw=0)
    ax.plot(B["year"], B["gU"], color=RED, lw=1.6, marker="o", ms=3.5, label="Upper threshold")
    ax.plot(B["year"], B["gL"], color=BLUE, lw=1.6, marker="s", ms=3.5, label="Lower threshold")
    ax.axhline(0, color=MUTED, lw=0.6)
    ax.set_xlabel("Year"); ax.set_ylabel("Basis relative to the\nstock's median (bp)")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    ax.grid(axis="y", color="#e6e6e6", lw=0.6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_band_years.pdf")); plt.close(fig)


def ban_R():
    A = futures_activity()
    b = A[A["ban"] & ~A["expiry_day"] & A["R"].notna()].copy()
    b["month"] = b["date"].dt.to_period("M").dt.to_timestamp()
    m = b.groupby("month")["R"].median()
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.plot(m.index, m.values, color=INK, lw=1.2, marker="o", ms=2)
    for d, lab, ha in [("2020-03-23", " intraday checks", "left"), ("2025-10-01", "delta-based rule ", "right")]:
        ax.axvline(pd.Timestamp(d), color=RED, lw=0.9, ls="--")
        ax.text(pd.Timestamp(d), 1.05, lab, color=RED, fontsize=7, va="bottom", ha=ha)
    ax.set_ylim(-0.05, 1.2)
    ax.set_ylabel("Median on ban days of\n(change in OI + volume) / volume")
    ax.set_xlabel("Month")
    ax.grid(axis="y", color="#e6e6e6", lw=0.6)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig_ban_R.pdf")); plt.close(fig)


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    which = sys.argv[1:] or ["ban_R", "band_years", "h9_tails", "level_profile"]
    for w in which:
        globals()[w]()
    print("figures written")
