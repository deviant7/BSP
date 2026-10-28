"""Treatment-side descriptive facts on F&O bans, MWPL and utilisation (no price/mispricing outcomes).

Usage: python3 -I describe_bans.py PROCESSED_DIR FIG_DIR
Reads mwpl_oi_panel.csv.gz and ban_days.csv.gz; writes ban_spells.csv.gz, descriptives.txt and figures.
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACC = "#1F3A5F"
REFORMS = {"2020-03-23": "MWPL halving\n(COVID)", "2025-10-01": "new MWPL\nformula"}


def spells(ban, tdays):
    """Group consecutive trading days in the ban list into spells per symbol."""
    pos = {d: i for i, d in enumerate(tdays)}
    b = ban.copy()
    b["k"] = b["date"].map(pos)
    b = b.dropna(subset=["k"]).sort_values(["symbol", "k"])
    b["new"] = b.groupby("symbol")["k"].diff().ne(1)
    b["spell"] = b.groupby("symbol")["new"].cumsum()
    g = b.groupby(["symbol", "spell"])
    sp = g.agg(start=("date", "min"), end=("date", "max"), days=("date", "size")).reset_index()
    return sp


def main(proc, figdir):
    os.makedirs(figdir, exist_ok=True)
    P = pd.read_csv(os.path.join(proc, "mwpl_oi_panel.csv.gz"), parse_dates=["date"])
    B = pd.read_csv(os.path.join(proc, "ban_days.csv.gz"), parse_dates=["date"])
    tdays = sorted(P["date"].unique())
    out = []
    w = out.append

    w(f"Panel: {P['date'].min().date()} to {P['date'].max().date()}, {len(tdays)} trading days, "
      f"{P['symbol'].nunique()} distinct symbols")
    uni = P.groupby(P["date"].dt.year)["symbol"].nunique()
    per_day = P.groupby("date")["symbol"].size().groupby(pd.Index(pd.to_datetime(tdays)).year).mean()

    B = B[B["date"].isin(tdays)]
    sp = spells(B, tdays)
    sp.to_csv(os.path.join(proc, "ban_spells.csv.gz"), index=False, compression="gzip")
    yr = pd.DataFrame({
        "fo_stocks_per_day": per_day.round(0),
        "ban_stock_days": B.groupby(B["date"].dt.year).size(),
        "stocks_banned": B.groupby(B["date"].dt.year)["symbol"].nunique(),
        "spells_started": sp.groupby(sp["start"].dt.year).size(),
        "median_spell_days": sp.groupby(sp["start"].dt.year)["days"].median(),
        "mean_spell_days": sp.groupby(sp["start"].dt.year)["days"].mean().round(1),
        "p90_spell_days": sp.groupby(sp["start"].dt.year)["days"].quantile(0.9),
    }).fillna(0)
    yr["share_stocks_banned"] = (yr["stocks_banned"] / uni).round(3)
    w("\nBy year:\n" + yr.to_string())
    w(f"\nAll spells: {len(sp)}; median length {sp['days'].median():.0f} days; mean {sp['days'].mean():.1f}; "
      f"max {sp['days'].max()}; share of spells of 1 day {np.mean(sp['days']==1):.2f}")

    # rule checks: entry when util(t-1) > 0.95; exit when util(last ban day) <= 0.80
    P = P.sort_values(["symbol", "date"])
    reform = pd.Timestamp("2025-10-01")
    P["u_rule"] = np.where((P["date"] >= reform) & P.get("util_futeq").notna() if "util_futeq" in P else False,
                           P.get("util_futeq"), P["util"])
    idx = {d: i for i, d in enumerate(tdays)}
    prevday = {tdays[i]: tdays[i - 1] for i in range(1, len(tdays))}
    key = P.set_index(["date", "symbol"])["u_rule"]
    ent = sp.assign(prev=sp["start"].map(prevday)).dropna(subset=["prev"])
    eu = np.array([key.get((d, s), np.nan) for d, s in zip(ent["prev"], ent["symbol"])])
    xu = np.array([key.get((d, s), np.nan) for d, s in zip(sp["end"], sp["symbol"])])
    w(f"\nRule check (entry): util on day before spell start > 0.95 in {np.nanmean(eu > 0.95):.3f} of {np.isfinite(eu).sum()} spells "
      f"(median {np.nanmedian(eu):.3f})")
    w(f"Rule check (exit): util on last ban day <= 0.80 in {np.nanmean(xu <= 0.80):.3f} of {np.isfinite(xu).sum()} spells "
      f"(median {np.nanmedian(xu):.3f}); <= 0.82 in {np.nanmean(xu <= 0.82):.3f}")

    # MWPL changes
    P["mwpl_ratio"] = P.groupby("symbol")["mwpl"].pct_change() + 1
    chg = P[(P["mwpl_ratio"] - 1).abs() > 1e-9]
    w(f"\nMWPL changes: {len(chg)} stock-day changes; by month of year: "
      + ", ".join(f"{m}:{n}" for m, n in chg.groupby(chg['date'].dt.month).size().items()))
    for d, lab in REFORMS.items():
        d = pd.Timestamp(d)
        if d in idx:
            r = P.loc[P["date"] == d, "mwpl_ratio"].dropna()
            w(f"MWPL ratio on {d.date()} ({lab.replace(chr(10), ' ')}): n={len(r)}, "
              f"quantiles 10/50/90 = {r.quantile(.1):.3f}/{r.median():.3f}/{r.quantile(.9):.3f}; share < 1: {np.mean(r < 0.999):.2f}")

    # utilisation near the threshold, days not in ban (running variable for an RD)
    inban = set(map(tuple, B[["date", "symbol"]].astype(str).values))
    P["in_ban_today"] = [(str(d), s) in inban for d, s in zip(P["date"].astype(str), P["symbol"])]
    for lab, m in [("pre-Oct-2025 (gross OI)", P["date"] < reform), ("post-Oct-2025 (FutEq)", P["date"] >= reform)]:
        x = P.loc[m & ~P["in_ban_today"], "u_rule"].dropna()
        lo = ((x > 0.90) & (x <= 0.95)).sum(); hi = ((x > 0.95) & (x <= 1.00)).sum()
        w(f"Utilisation counts, not-in-ban stock-days, {lab}: (0.90,0.95] {lo}, (0.95,1.00] {hi}")

    open(os.path.join(proc, "descriptives.txt"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))

    # figures
    m = B.groupby(B["date"].dt.to_period("M")).size()
    m.index = m.index.to_timestamp()
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    ax.bar(m.index, m.values, width=25, color=ACC)
    for d, lab in REFORMS.items():
        ax.axvline(pd.Timestamp(d), color="0.4", lw=0.8, ls="--")
        ax.text(pd.Timestamp(d), ax.get_ylim()[1] * 0.95, lab, fontsize=7, ha="right", va="top")
    ax.set_ylabel("stock-days in ban per month"); fig.tight_layout()
    fig.savefig(os.path.join(figdir, "ban_days_per_month.pdf")); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.hist(sp["days"].clip(upper=40), bins=np.arange(0.5, 41.5, 1), color=ACC)
    ax.set_xlabel("ban spell length (trading days; 40 = 40 or more)"); ax.set_ylabel("spells")
    fig.tight_layout(); fig.savefig(os.path.join(figdir, "spell_lengths.pdf")); plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.0), sharey=False)
    for ax, (lab, mk) in zip(axs, [("before 1 Oct 2025 (gross OI / MWPL)", P["date"] < reform),
                                   ("from 1 Oct 2025 (FutEq OI / MWPL)", P["date"] >= reform)]):
        x = P.loc[mk & ~P["in_ban_today"], "u_rule"].dropna()
        ax.hist(x[(x > 0.6) & (x < 1.1)], bins=np.arange(0.6, 1.1001, 0.01), color=ACC)
        ax.axvline(0.95, color="0.3", ls="--", lw=0.8); ax.axvline(0.80, color="0.6", ls=":", lw=0.8)
        ax.set_title(lab, fontsize=8); ax.set_xlabel("utilisation, stock-days not in ban")
    fig.tight_layout(); fig.savefig(os.path.join(figdir, "utilisation_near_threshold.pdf")); plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
