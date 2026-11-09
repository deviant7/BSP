"""Charts for the presentation deck (written to deck/figs/ as PNG), in the deck's chart style.

Reuses the data code of thesis_figures_final.py and only changes the styling (palette, bar outlines, sizes), so every
chart rests on the same numbers as the thesis.
Run:  python3 -I analysis/deck_figures.py [names...]
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import thesis_figures_final as T

OUT = os.path.join(T.ROOT, "deck", "figs")
# deck palette: bright blue (main series), navy-black (contrast / benchmark), mid blue, steel, greys
T.BLUE, T.RED, T.INK, T.MUTED, T.GREY, T.LIGHT, T.PALE = ("#00A3E8", "#0B1F33", "#1A1A1A", "#4D4D4D", "#6A93B0",
                                                          "#C9D3DC", "#E3F4FC")
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9,
    "axes.edgecolor": "#1A1A1A", "axes.linewidth": 0.8, "axes.spines.left": True, "axes.grid": False,
    "xtick.color": "#1A1A1A", "ytick.color": "#1A1A1A", "ytick.major.size": 3, "xtick.major.size": 3,
    "patch.force_edgecolor": True, "patch.edgecolor": "#1A1A1A", "patch.linewidth": 0.6,
    "legend.frameon": True, "legend.edgecolor": "#1A1A1A", "legend.fancybox": False, "legend.fontsize": 7.5,
    "savefig.dpi": 220,
})


def save_png(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), bbox_inches="tight", pad_inches=0.04, dpi=220, facecolor="white")
    plt.close(fig)
    print("  wrote", name)


T.save = save_png
import matplotlib.axes
matplotlib.axes.Axes.grid = lambda self, *a, **k: None   # the deck's charts carry no gridlines
T.FIG = OUT

# figure heights for the deck (inches): taller than in the thesis so charts fill their panels
_orig_subplots = plt.subplots
H_NOW = {"h": None}


def _subplots(*a, **k):
    if H_NOW["h"] and "figsize" in k:
        k["figsize"] = (k["figsize"][0], H_NOW["h"])
    return _orig_subplots(*a, **k)


plt.subplots = _subplots
T.plt.subplots = _subplots
HEIGHT = {4.3: 3.3, 5.6: 3.9, 5.4: 3.6, 8.6: 3.7}

# (function, output name, width in inches): half panel 4.3", full width 8.6"
JOBS = {
    "timeline": 8.6, "util_example": 5.6, "ban_month": 8.6, "mwpl_ratio": 4.3, "basis_dist": 4.3,
    "index_fig": 8.6, "band_scatter": 4.3, "band_years": 4.3, "cost_band": 5.4, "h3_placebo": 4.3, "h4_flows": 4.3,
    "h9_tails": 4.3, "spurious": 5.6, "covid": 4.3, "ban_R": 5.6, "h8_era": 8.6, "h7_dots": 5.6,
    "level_profile": 4.3, "level_groups": 4.3, "density": 4.3, "rd_plot": 4.3, "h6_es": 5.6, "h5_legs": 5.6,
    "arb_aum": 4.3, "basis_expiry": 4.3,
}


def model_band():
    import importlib.util
    us = np.linspace(-150, 150, 400)
    PHI, G, CP, CM = 1.0, 1.0, 15.0, 60.0

    def m(u):
        if u > PHI * CP:
            return (G * u + CP) / (G * PHI + 1)
        if u < -PHI * CM:
            return (G * u - CM) / (G * PHI + 1)
        return u / PHI
    fig, ax = plt.subplots(figsize=(4.3, 2.8))
    ax.axhspan(-CM, CP, color=T.PALE, lw=0)
    ax.plot(us, us, color=T.GREY, ls="--", lw=1.2, label="no arbitrage")
    ax.plot(us, [m(u) for u in us], color=T.BLUE, lw=2.2, label="with arbitrage")
    ax.text(-145, 8, "band: no trade", fontsize=7.5, color=T.MUTED)
    ax.set_xlabel("Demand pressure toward futures, u")
    ax.set_ylabel("Basis, m (bp)")
    ax.legend(loc="upper left")
    save_png(fig, "model_band")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(JOBS) + ["model_band"]
    for n in names:
        print(n)
        if n == "model_band":
            model_band()
            continue
        T.W1 = JOBS[n]
        H_NOW["h"] = HEIGHT[JOBS[n]] if n != "timeline" else 3.3
        getattr(T, n)()
