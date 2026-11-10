"""Deck-style (PNG) and Beamer-style (PDF) versions of the two Stage I figures made by bsp1_figures.py.
Imports the styling of analysis/deck_figures.py or analysis/beamer_figures.py and writes only into BSP1/.
Run:  python3 -I BSP1/scripts/bsp1_variants.py deck     (-> BSP1/deck/figs/*.png)
      python3 -I BSP1/scripts/bsp1_variants.py beamer   (-> BSP1/beamer/figs/*.pdf)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
sys.path.insert(0, HERE)
mode = sys.argv[1]
if mode == "deck":
    import deck_figures as S          # applies the deck palette and rcParams to the shared figure module
    out = os.path.join(ROOT, "BSP1", "deck", "figs")
    def save(fig, name):
        fig.savefig(os.path.join(out, name + ".png"), bbox_inches="tight", pad_inches=0.04, dpi=220, facecolor="white")
        S.plt.close(fig); print("  wrote", name)
    sizes = {"h1_bins": (8.6, 3.6), "rd_trading": (8.6, 3.6)}
    hset = lambda h: S.H_NOW.__setitem__("h", h)
else:
    import beamer_figures as S
    out = os.path.join(ROOT, "BSP1", "beamer", "figs")
    def save(fig, name):
        fig.savefig(os.path.join(out, name + ".pdf"), bbox_inches="tight", pad_inches=0.03)
        S.plt.close(fig); print("  wrote", name)
    sizes = {"h1_bins": (4.8, 2.3), "rd_trading": (4.8, 2.3)}
    hset = lambda h: S.H.__setitem__("h", h)
import bsp1_figures as B
B.save = save
os.makedirs(out, exist_ok=True)
for n, (w, h) in sizes.items():
    S.T.W1 = w; hset(h)
    getattr(B, n)()
