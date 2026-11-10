"""Two figures for the Stage I report that the thesis did not have, in the thesis figure style.

fig_h1_bins: band width and mean absolute basis by decile of the F&O friction index (previous quarter).
fig_rd_trading: futures contracts and R = (dOI + V)/V around the 95% trigger (trading only).
Writes PDFs to BSP1/paper/figs/ (and, with --png, PNGs to BSP1/deck/figs/ in the deck style is not needed).
Run:  python3 -I BSP1/scripts/bsp1_figures.py
"""
import os, sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import thesis_figures_final as T
plt = T.plt
OUT = os.path.join(ROOT, "BSP1", "paper", "figs")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("  wrote", name)


def h1_bins():
    import h1_frictions as H
    M = pd.read_csv(os.path.join(H.PROC, "fno_membership.csv.gz"))
    Fq = pd.read_pickle(os.path.join(H.CACHE, "frictions_q.pkl"))
    O = H.outcomes()
    Z, v, share = H.build_index(Fq, H.FR)
    Z["q"] = Z["q"] + 1
    D = O.merge(Z, on=["symbol", "q"], how="inner")
    D = D[(D["q"] >= pd.Period("2015Q2")) & (D["q"] <= pd.Period("2025Q3"))].dropna(subset=["W", "A"])
    for c in ["W", "A"]:
        D[c + "_d"] = D[c] - D.groupby("q")[c].transform("mean") + D[c].mean()
    D["dec"] = D.groupby("q")["index"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False)) + 1
    g = D.groupby("dec").agg(W=("W_d", "mean"), A=("A_d", "mean"), n=("W", "size"))
    print(g.round(2).to_string())
    fig, axs = plt.subplots(1, 2, figsize=(T.W1, 2.4))
    for ax, col, ttl in [(axs[0], "W", "Band width: 80th minus 20th percentile (bp)"),
                         (axs[1], "A", "Mean absolute basis (bp)")]:
        bars = ax.bar(g.index, g[col], color=T.BLUE,
                      width=0.7)
        ax.set_title(ttl, fontsize=8)
        ax.set_xticks(range(1, 11))
        ax.set_xlabel("Decile of the friction index, previous quarter")
        lo = g[col].min()
        ax.set_ylim(lo * 0.8, g[col].max() * 1.06)
    fig.tight_layout(w_pad=2)
    save(fig, "fig_h1_bins")


def rd_trading():
    import rd_95
    F = rd_95.frame()
    F = F[(F["date"] < "2025-10-01") & (F["x"] >= 0.80) & (F["x"] < 1.10)]
    if "expiry_day" in F.columns:
        F = F[~F["expiry_day"].astype(bool)]
    bins = np.arange(0.80, 1.1001, 0.01)
    F["b"] = pd.cut(F["x"], bins)
    g = F.groupby("b", observed=True).agg(x=("x", "mean"), fut=("ly_fut", "mean"), R=("R", "mean"))
    fig, axs = plt.subplots(1, 2, figsize=(T.W1, 2.4))
    for ax, col, ttl in [(axs[0], "fut", "log(1 + futures contracts) on day t"),
                         (axs[1], "R", "R = (change in OI + volume) / volume, day t")]:
        lo, hi = g[g["x"] < 0.95], g[g["x"] >= 0.95]
        ax.scatter(lo["x"], lo[col], s=14, color=T.GREY)
        ax.scatter(hi["x"], hi[col], s=14, color=T.BLUE)
        for part, c in [(lo, T.GREY), (hi, T.BLUE)]:
            p = np.polyfit(part["x"], part[col], 1)
            xs = np.linspace(part["x"].min(), part["x"].max(), 10)
            ax.plot(xs, np.polyval(p, xs), color=c, lw=1.3)
        ax.axvline(0.95, color=T.RED, lw=0.9, ls="--")
        ax.set_title(ttl, fontsize=8)
        ax.set_xlabel("Utilisation at the end of day t-1")
    fig.tight_layout(w_pad=2)
    save(fig, "fig_rd_trading")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or ["h1_bins", "rd_trading"]):
        print(n); globals()[n]()
