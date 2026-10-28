"""Extra treatment-side figures for the progress report (no outcomes): MWPL ratio at the 1 Oct 2025 formula change."""
import os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

proc, figdir = sys.argv[1], sys.argv[2]
P = pd.read_csv(os.path.join(proc, "mwpl_oi_panel.csv.gz"), parse_dates=["date"]).sort_values(["symbol", "date"])
P["ratio"] = P.groupby("symbol")["mwpl"].pct_change() + 1
r = P.loc[P["date"] == "2025-10-01", "ratio"].dropna()
fig, ax = plt.subplots(figsize=(5.5, 2.8))
ax.hist(r, bins=np.arange(0.45, 0.80, 0.0125), color="#1F3A5F")
ax.set_xlabel("new MWPL / old MWPL on 1 Oct 2025"); ax.set_ylabel("stocks")
fig.tight_layout(); fig.savefig(os.path.join(figdir, "mwpl_ratio_oct2025.pdf")); plt.close(fig)
print(len(r), r.describe().round(3).to_dict())
