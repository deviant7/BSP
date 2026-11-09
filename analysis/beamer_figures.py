"""Charts for the academic (Beamer) presentation, written to beamer/figs/ as PDF.

Reuses the data code of thesis_figures_final.py and changes only the styling: a blue primary colour with red and other
contrasting colours, sizes for a 4:3 Beamer frame, and Liberation Sans to match the Helvetica text of the slides.
Run:  python3 -I analysis/beamer_figures.py [names...]
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import thesis_figures_final as T

OUT = os.path.join(T.ROOT, "beamer", "figs")
T.BLUE, T.RED, T.INK, T.MUTED, T.GREY, T.LIGHT, T.PALE = ("#1F4E9A", "#C0392B", "#1A1A1A", "#555555", "#8E9AA6",
                                                          "#C9D1D9", "#E6EDF7")
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 9, "axes.labelsize": 9, "legend.fontsize": 7.5,
    "axes.titlesize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8, "pdf.fonttype": 42,
})
_orig = plt.subplots
H = {"h": None}


def _subplots(*a, **k):
    if H["h"] and "figsize" in k:
        k["figsize"] = (k["figsize"][0], H["h"])
    return _orig(*a, **k)


plt.subplots = _subplots
T.plt.subplots = _subplots


def save_pdf(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("  wrote", name)


T.save = save_pdf
T.FIG = OUT

# width, height in inches (frame text width is about 4.6 in)
JOBS = {
    "timeline": (4.8, 2.4), "util_example": (4.6, 2.3), "ban_month": (4.6, 2.1), "mwpl_ratio": (4.4, 2.2),
    "basis_dist": (4.6, 2.2), "index_fig": (4.8, 2.3), "band_scatter": (4.4, 2.5), "band_years": (4.4, 2.2),
    "cost_band": (4.8, 2.5), "h3_placebo": (4.6, 2.3), "h4_flows": (4.6, 2.8), "h9_tails": (4.4, 2.4),
    "spurious": (4.6, 2.1), "covid": (4.4, 2.4), "ban_R": (4.6, 2.3), "h8_era": (4.8, 2.2), "h7_dots": (4.8, 2.2),
    "level_profile": (4.6, 2.6), "level_groups": (4.6, 2.3), "density": (4.4, 2.2), "rd_plot": (4.8, 2.2),
    "h6_es": (4.6, 2.4), "h5_legs": (4.6, 2.2), "arb_aum": (4.4, 2.1), "basis_expiry": (4.4, 2.0),
}

def model():
    """model_band, model_path, model_hist from the verified model script, resized for a Beamer frame."""
    src = open(os.path.join(T.ROOT, "models_src", "modelC", "verify_modelC.py")).read()
    src = src.replace('matplotlib.use("Agg")', "")
    for a, b in [('"figs/fig_path.pdf"', repr(os.path.join(OUT, "model_path.pdf"))),
                 ('"figs/fig_hist.pdf"', repr(os.path.join(OUT, "model_hist.pdf"))),
                 ('"figs/fig_band.pdf"', repr(os.path.join(OUT, "model_band.pdf"))),
                 ('"#1F3A5F"', repr(T.BLUE)), ('"#C9D6E8"', repr(T.PALE)), ('color="0.6"', 'color="#C0392B"'),
                 ('color="0.55"', 'color="#C0392B"'), ("figsize=(7.5, 5.2)", "figsize=(4.7, 3.1)"),
                 ("figsize=(6.2, 3.4)", "figsize=(4.6, 2.5)")]:
        src = src.replace(a, b)
    cwd = os.getcwd()
    os.chdir(os.path.join(T.ROOT, "models_src", "modelC"))
    try:
        exec(compile(src, "verify_modelC", "exec"), {"__name__": "__verify__"})
    finally:
        os.chdir(cwd)
    print("  wrote model_path, model_hist, model_band")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n in (sys.argv[1:] or list(JOBS) + ["model"]):
        print(n)
        if n == "model":
            H["h"] = None
            model()
            continue
        T.W1, H["h"] = JOBS[n]
        getattr(T, n)()
