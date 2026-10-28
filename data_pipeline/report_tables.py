"""Write LaTeX tables of treatment-side ban facts (2015 onward) for the progress report."""
import os, sys
import pandas as pd

proc, tabdir = sys.argv[1], sys.argv[2]
P = pd.read_csv(os.path.join(proc, "mwpl_oi_panel.csv.gz"), parse_dates=["date"], usecols=["date", "symbol"])
B = pd.read_csv(os.path.join(proc, "ban_days.csv.gz"), parse_dates=["date"])
S = pd.read_csv(os.path.join(proc, "ban_spells.csv.gz"), parse_dates=["start", "end"])
P, B, S = P[P.date >= "2015-01-01"], B[B.date >= "2015-01-01"], S[S.start >= "2015-01-01"]
y = pd.DataFrame({
    "F\\&O stocks (avg/day)": P.groupby("date").size().groupby(lambda d: d.year).mean().round(0).astype(int),
    "Stocks banned": B.groupby(B.date.dt.year).symbol.nunique(),
    "Ban spells": S.groupby(S.start.dt.year).size(),
    "Ban stock-days": B.groupby(B.date.dt.year).size(),
    "Median spell (days)": S.groupby(S.start.dt.year).days.median(),
    "Longest spell (days)": S.groupby(S.start.dt.year).days.max(),
}).fillna(0).astype(int)
y.index.name = "Year"
heads = ["F\\&O stocks\\\\(avg per day)", "Stocks\\\\banned", "Ban\\\\spells", "Ban\\\\stock-days",
         "Median spell\\\\(days)", "Longest spell\\\\(days)"]
lines = ["\\begin{tabular}{l" + "r" * y.shape[1] + "}", "\\toprule",
         "Year & " + " & ".join("\\shortstack[r]{" + h + "}" for h in heads) + " \\\\", "\\midrule"]
for yr, row in y.iterrows():
    lab = f"{yr}" + ("$^{a}$" if yr == 2026 else "")
    lines.append(lab + " & " + " & ".join(str(v) for v in row.values) + " \\\\")
tot = [str(int(P.groupby('date').size().mean())), str(B.symbol.nunique()), str(len(S)), str(len(B)), str(int(S.days.median())), str(S.days.max())]
lines += ["\\midrule", "2015 to 2026 & " + " & ".join(tot) + " \\\\", "\\bottomrule", "\\end{tabular}"]
open(os.path.join(tabdir, "ban_by_year.tex"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
