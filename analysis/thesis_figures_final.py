"""Figures for the final thesis, in the thesis design (written to thesis/figs/).

Every figure is drawn from the project's data or from numbers in analysis/output/ (quoted where hard-coded).
Run all:   python3 -I analysis/thesis_figures_final.py
Run some:  python3 -I analysis/thesis_figures_final.py timeline spurious ...
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
sys.path.insert(0, os.path.dirname(__file__))
from samples import basis_sample, futures_activity, calendar, ROOT, PROC

FIG = os.path.join(ROOT, "thesis", "figs")
BLUE, RED, INK, MUTED, GREY, LIGHT, PALE = "#1F4E9A", "#C0504D", "#1A1A1A", "#6B6B6B", "#9A9A9A", "#D0D0D0", "#E8EDF5"
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8.5, "axes.titlesize": 8.5, "axes.labelsize": 8.5,
    "axes.edgecolor": GREY, "axes.linewidth": 0.6, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 3, "ytick.major.size": 0,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": "#E6E6E6", "grid.linewidth": 0.6,
    "legend.frameon": False, "legend.fontsize": 8, "lines.linewidth": 1.8, "pdf.fonttype": 42,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.titlecolor": INK,
})
W1, W2 = 6.3, 3.0          # full text width (inches) and default height
BP = 1e4


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + ".pdf"), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("  wrote", name)


def label_bars(ax, bars, fmt="{:,.0f}", inside=False, color=INK, dx=0.01):
    xmax = ax.get_xlim()[1]
    for b in bars:
        v = b.get_width()
        ax.text(v + dx * xmax, b.get_y() + b.get_height() / 2, fmt.format(v), va="center", ha="left",
                fontsize=8, color=color, fontweight="bold")


# ------------------------------------------------------------------------------------------------ institutions
def timeline():
    fig, ax = plt.subplots(figsize=(W1, 2.9))
    D = pd.Timestamp
    lanes = ["Futures STT", "Ban enforcement", "Position limit", "Arbitrage capital"]
    y = {k: len(lanes) - i for i, k in enumerate(lanes)}
    h = 0.5

    def seg(lane, a, b, col, txt, tcol="white"):
        a, b = D(a), D(b)
        ax.barh(y[lane], (b - a).days, left=a, height=h, color=col, edgecolor="white", linewidth=1.5)
        ax.text(a + (b - a) / 2, y[lane], txt, ha="center", va="center", fontsize=7, color=tcol, fontweight="bold")

    seg("Futures STT", "2015-01-01", "2023-04-01", LIGHT, "0.01%", INK)
    seg("Futures STT", "2023-04-01", "2024-10-01", GREY, "0.0125%")
    seg("Futures STT", "2024-10-01", "2026-04-01", MUTED, "0.02%")
    seg("Futures STT", "2026-04-01", "2026-11-01", INK, "")
    ax.text(D("2026-12-10"), y["Futures STT"], "0.05%", va="center", fontsize=7, color=INK, fontweight="bold")
    seg("Ban enforcement", "2015-01-01", "2020-03-23", LIGHT, "end-of-day positions", INK)
    seg("Ban enforcement", "2020-03-23", "2025-10-01", BLUE, "peak intraday positions")
    seg("Ban enforcement", "2025-10-01", "2026-11-01", RED, "delta", "white")
    seg("Position limit", "2015-01-01", "2025-10-01", LIGHT, "20% of free float, gross open interest", INK)
    seg("Position limit", "2025-10-01", "2026-11-01", RED, "new", "white")
    ax.barh(y["Position limit"] + 0.36, (D("2020-11-27") - D("2020-03-23")).days, left=D("2020-03-23"), height=0.16,
            color=BLUE, edgecolor="white")
    ax.text(D("2020-11-27") + pd.Timedelta(days=40), y["Position limit"] + 0.36, "halved for volatile stocks",
            va="center", fontsize=6.5, color=BLUE)
    seg("Arbitrage capital", "2015-01-01", "2020-12-01", LIGHT, "", INK)
    seg("Arbitrage capital", "2020-12-01", "2021-09-01", BLUE, "")
    ax.text(D("2021-01-15"), y["Arbitrage capital"] + 0.38, "peak margins phased in", fontsize=6.5, color=BLUE)
    seg("Arbitrage capital", "2021-09-01", "2026-11-01", LIGHT, "", INK)
    ax.plot([D("2023-04-01")] * 2, [y["Arbitrage capital"] - h / 2, y["Arbitrage capital"] + h / 2], color=RED, lw=2.2)
    ax.text(D("2023-04-20"), y["Arbitrage capital"] - 0.02, "debt-fund tax change", fontsize=6.5, color=RED, va="center")
    ax.set_yticks([y[k] for k in lanes]); ax.set_yticklabels(lanes, color=INK)
    ax.set_xlim(D("2015-01-01"), D("2027-06-30"))
    ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(False); ax.tick_params(axis="y", length=0)
    ax.set_ylim(0.4, len(lanes) + 0.75)
    save(fig, "fig_timeline")


def util_example():
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "util"], parse_dates=["date"])
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    s = "SAIL"
    p = P[(P["symbol"] == s) & (P["date"] >= "2024-01-01") & (P["date"] <= "2024-06-30")].sort_values("date")
    b = set(B.loc[B["symbol"] == s, "date"])
    fig, ax = plt.subplots(figsize=(W1, 2.6))
    inb = p["date"].isin(b).values
    for d, flag in zip(p["date"], inb):
        if flag:
            ax.axvspan(d - pd.Timedelta(hours=12), d + pd.Timedelta(hours=12), color=PALE, lw=0)
    ax.plot(p["date"], p["util"] * 100, color=BLUE, lw=1.5)
    for lvl, txt in [(95, "95%: ban from the next day"), (80, "80%: ban ends")]:
        ax.axhline(lvl, color=RED if lvl == 95 else MUTED, lw=0.9, ls="--")
        ax.text(p["date"].iloc[-1] + pd.Timedelta(days=2), lvl, txt, fontsize=7, va="center",
                color=RED if lvl == 95 else MUTED)
    ax.set_ylabel("Utilisation of the MWPL (%)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("2024 (shaded: days in the ban)")
    ax.set_ylim(min(30, p["util"].min() * 100 - 3), 106)
    save(fig, "fig_util_example")


def arb_aum():
    A = pd.read_csv(os.path.join(PROC, "amfi_arbitrage_monthly.csv"))
    A["m"] = pd.PeriodIndex(A["month"], freq="M").to_timestamp()
    fig, ax = plt.subplots(figsize=(W1, 2.4))
    ax.plot(A["m"], A["aum"] / 1e5, color=BLUE)
    ax.axvline(pd.Timestamp("2023-04-01"), color=RED, lw=0.9, ls="--")
    ax.text(pd.Timestamp("2023-05-01"), 2.6, "1 April 2023: debt funds\nlose their tax advantage", fontsize=7, color=RED)
    ax.set_ylabel("Net assets (Rs lakh crore)")
    ax.set_ylim(0, 3.3)
    save(fig, "fig_arb_aum")


# ------------------------------------------------------------------------------------------------ data
def ban_month():
    B = pd.read_csv(os.path.join(PROC, "ban_days.csv.gz"), parse_dates=["date"])
    m = B.groupby(B["date"].dt.to_period("M")).size()
    idx = pd.period_range("2010-02", "2026-10", freq="M")
    m = m.reindex(idx, fill_value=0)
    fig, ax = plt.subplots(figsize=(W1, 2.4))
    ax.bar(idx.to_timestamp(), m.values, width=25, color=BLUE, lw=0)
    ax.axvline(pd.Timestamp("2025-10-01"), color=RED, lw=0.9, ls="--")
    ax.text(pd.Timestamp("2025-09-01"), m.max() * 0.92, "new rule\n1 Oct 2025", ha="right", fontsize=7, color=RED)
    ax.set_ylabel("Ban stock-days per month")
    save(fig, "fig_ban_month")


def mwpl_ratio():
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl"], parse_dates=["date"])
    a = P[P["date"] == "2025-09-30"].set_index("symbol")["mwpl"]
    b = P[P["date"] == "2025-10-01"].set_index("symbol")["mwpl"]
    r = (b / a).dropna()
    fig, ax = plt.subplots(figsize=(W1, 2.3))
    ax.hist(r, bins=np.arange(0.45, 0.80, 0.0125), color=BLUE, edgecolor="white", lw=0.8)
    ax.set_xlabel("New MWPL divided by old MWPL, 1 October 2025")
    ax.set_ylabel("Stocks")
    top = ax.get_ylim()[1]
    ax.annotate("floor: 10% of free float\n(half the old limit)", (0.5, 21), xytext=(0.53, top * 0.55), fontsize=7,
                color=MUTED, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    ax.annotate("15% of free float\n(three quarters of the old limit)", (0.745, top * 0.9), xytext=(0.60, top * 0.85),
                fontsize=7, color=MUTED, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.6))
    print("    stocks", len(r), "median", round(r.median(), 3))
    save(fig, "fig_mwpl_ratio")


def basis_dist():
    S = basis_sample()
    m = S["m"].dropna() * BP
    q = np.percentile(m, [10, 50, 90])
    out = (m < -100) | (m > 100)
    fig, ax = plt.subplots(figsize=(W1, 2.4))
    ax.hist(m[~out], bins=np.arange(-100, 101, 2.5), color=BLUE, edgecolor="white", lw=0.4)
    for v, t in zip(q, ["10th percentile", "median", "90th percentile"]):
        ax.axvline(v, color=INK if t == "median" else RED, lw=0.9, ls="--")
        ax.text(v + 1.5, ax.get_ylim()[1] * 0.97, f"{t}\n{v:+.1f} bp", fontsize=7, va="top", color=MUTED)
    ax.set_xlabel("Basis (bp)")
    ax.set_ylabel("Stock-days")
    txt = (f"Analysis sample: {len(m)} stock-days; median {q[1]:+.1f} bp, 10th percentile {q[0]:+.1f}, "
           f"90th percentile {q[2]:+.1f}; share beyond 100 bp from zero {out.mean():.3f}")
    open(os.path.join(ROOT, "analysis", "output", "thesis_figures_stats.txt"), "w").write(txt + "\n")
    print("   ", txt)
    save(fig, "fig_basis_dist")


def basis_expiry():
    S = basis_sample()
    S = S[S["k"] == 0]
    S = S.assign(dte=S["d_exp"])
    g = S[(S["dte"] >= 0) & (S["dte"] <= 24)].groupby("dte")["m"].apply(lambda x: np.median(np.abs(x)) * BP)
    fig, ax = plt.subplots(figsize=(W1, 2.2))
    ax.bar(g.index, g.values, color=BLUE, width=0.75, lw=0)
    ax.set_xlabel("Trading days to expiry (near-month contract)")
    ax.set_ylabel("Median absolute basis (bp)")
    ax.invert_xaxis()
    save(fig, "fig_basis_expiry")


def index_fig():
    # loadings and validation from analysis/output/constraint_index.txt and index_size_check.txt
    comp = ["No short channel", "SLB scarcity", "Spread", "Illiquidity", "Idiosyncratic volatility"]
    load = [0.494, 0.448, 0.428, 0.489, 0.365]
    fig, axs = plt.subplots(1, 2, figsize=(W1, 2.3), gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axs[0]
    bars = ax.barh(comp[::-1], load[::-1], color=BLUE, height=0.6)
    ax.set_xlim(0, 0.62); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    label_bars(ax, bars, "{:.2f}")
    ax.set_title("Loadings on the first component", fontsize=8)
    ax.tick_params(axis="y", length=0)
    ax = axs[1]
    rows = ["Price delay", "Price delay,\nwithin stock", "Absolute drift", "Drift after\nbad news"]
    raw = [(0.058, 0.003), (0.032, 0.005), (0.023, 0.001), (-0.008, 0.001)]
    siz = [(0.036, 0.004), (0.028, 0.006), (0.015, 0.001), (-0.001, 0.002)]
    yy = np.arange(len(rows))[::-1]
    for off, data, col, lab in [(0.15, raw, GREY, "no size control"), (-0.15, siz, BLUE, "with size control")]:
        b = np.array([d[0] for d in data]); s = np.array([d[1] for d in data])
        ax.errorbar(b, yy + off, xerr=1.96 * s, fmt="o", color=col, ms=5, elinewidth=1.2, capsize=0, label=lab)
    ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_yticks(yy); ax.set_yticklabels(rows); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    ax.set_title("Coefficient per s.d. of the index (95% interval)", fontsize=8)
    ax.legend(loc="lower right", fontsize=7)
    fig.tight_layout(w_pad=2)
    save(fig, "fig_index")


# ------------------------------------------------------------------------------------------------ band chapter
def band_scatter():
    from band_estimation import load
    S = load()
    x, d = S["x"].values, S["d"].values
    bins = np.arange(-90, 61, 5)
    c = pd.cut(x, bins)
    g = pd.DataFrame({"c": c, "d": d}).groupby("c", observed=True)["d"].agg(["mean", "count"])
    mids = np.array([iv.mid for iv in g.index])
    fig, ax = plt.subplots(figsize=(W1, 2.7))
    ax.axvspan(-34.5, 23.9, color=PALE, lw=0)
    ax.scatter(mids, g["mean"], s=18, color=BLUE, zorder=3)
    ax.axhline(0, color=MUTED, lw=0.7)
    for v, t in [(-34.5, "lower threshold\n-34.5 bp"), (23.9, "upper threshold\n+23.9 bp")]:
        ax.axvline(v, color=RED, lw=0.9, ls="--")
        ax.text(v, ax.get_ylim()[1] * 0.9, t, fontsize=7, color=RED, ha="center", va="top",
                bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlabel("Yesterday's basis relative to the stock's median (bp)")
    ax.set_ylabel("Mean change in the basis today (bp)")
    save(fig, "fig_band_scatter")


def band_years():
    B = pd.read_csv(os.path.join(ROOT, "analysis", "output", "band_by_year.csv"))
    B = B[B["year"] <= 2025]
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.fill_between(B["year"], B["gL"], B["gU"], color=PALE, lw=0)
    ax.plot(B["year"], B["gU"], color=RED, marker="o", ms=4, label="Upper threshold")
    ax.plot(B["year"], B["gL"], color=BLUE, marker="s", ms=4, label="Lower threshold")
    ax.axhline(0, color=MUTED, lw=0.7)
    for _, r in B.iterrows():
        pass
    ax.set_ylabel("Basis relative to the\nstock's median (bp)")
    ax.legend(loc="lower right", ncol=2)
    ax.set_xticks(B["year"])
    save(fig, "fig_band_years")


def cost_band():
    # components of the open-and-hold round trip (bp), as in analysis/band_costs.py; edges from band_costs.txt
    periods = ["to Mar 2023", "Apr 2023 to Sep 2024", "Oct 2024 to Mar 2026", "from Apr 2026"]
    fstt = [1.0, 1.25, 2.0, 5.0]
    exc = [(0.00322, 0.00188), (0.00322, 0.00188), (0.00297, 0.00173), (0.00297, 0.00173)]
    brk, sebi, gst = 0.01, 0.0001, 0.18
    comps = {"STT on cash purchase": [], "STT on delivery": [], "STT on futures sale": [], "Stamp duty": [],
             "Fees, brokerage, GST": []}
    for f, (ec, ef) in zip(fstt, exc):
        comps["STT on cash purchase"].append(10.0)
        comps["STT on delivery"].append(10.0)
        comps["STT on futures sale"].append(f)
        comps["Stamp duty"].append(1.5)
        comps["Fees, brokerage, GST"].append(((ec + sebi + brk) * 2 + (ef + sebi + brk)) * (1 + gst) * 100)
    tot = np.sum([comps[k] for k in comps], axis=0)
    gU = [27.5, 23.6, 21.5, 24.1]; p90 = [27.5, 24.7, 24.2, 29.7]
    cols = [BLUE, "#5B7FBF", RED, GREY, LIGHT]
    fig, ax = plt.subplots(figsize=(W1, 2.6))
    yy = np.arange(len(periods))[::-1]
    left = np.zeros(len(periods))
    for (k, v), c in zip(comps.items(), cols):
        ax.barh(yy, v, left=left, color=c, height=0.55, edgecolor="white", lw=1.5, label=k)
        left += np.array(v)
    for i in range(len(periods)):
        ax.text(tot[i] + 0.6, yy[i], f"{tot[i]:.1f}", va="center", fontsize=8, fontweight="bold")
    ax.scatter(gU, yy + 0.34, marker="v", color=INK, s=28, zorder=4, label="Estimated upper threshold (level)")
    ax.set_yticks(yy); ax.set_yticklabels(periods); ax.tick_params(axis="y", length=0)
    ax.set_xlabel("bp of notional"); ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 36)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.22), ncol=3, fontsize=7)
    print("    totals", np.round(tot, 1))
    save(fig, "fig_cost_band")


def h3_placebo():
    from h3_costs import window_stats, EVENTS
    S = basis_sample()
    days, pos = calendar()
    ev = {k: int(days.searchsorted(pd.Timestamp(d))) for k, (d, dc) in EVENTS.items()}
    true = {k: window_stats(S, i0)["d80"].mean() for k, i0 in ev.items()}
    first, last = int(S["i"].min()) + 40, int(S["i"].max()) - 39
    pl = []
    for i0 in range(first, last + 1, 80):
        if any(abs(i0 - j) < 80 for j in ev.values()):
            continue
        w = window_stats(S, i0)
        if len(w) >= 50:
            pl.append((days[i0], w["d80"].mean()))
    P = pd.DataFrame(pl, columns=["date", "v"])
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.scatter(P["date"], P["v"], s=22, color=LIGHT, edgecolor=GREY, lw=0.6, label="Placebo dates", zorder=3)
    for k, i0 in ev.items():
        ax.scatter(days[i0], true[k], s=46, color=BLUE if k != "2023" else GREY, zorder=4)
        ax.annotate(f"STT {k}\n{true[k]:+.1f}", (days[i0], true[k]), xytext=(6, 4), textcoords="offset points",
                    fontsize=7, color=BLUE if k != "2023" else MUTED)
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.set_ylabel("Mean change in stocks'\n80th percentile (bp)")
    ax.legend(loc="lower left", fontsize=7)
    print("    placebo n", len(P), "sd", round(P["v"].std(ddof=0), 2))
    save(fig, "fig_h3_placebo")


def h4_flows():
    S = basis_sample()
    nb = S[~S["ban"]].copy()
    nb["month"] = nb["date"].dt.to_period("M")
    q = nb.groupby("month")["m"].quantile(0.8) * BP
    A = pd.read_csv(os.path.join(PROC, "amfi_arbitrage_monthly.csv"))
    A["month"] = pd.PeriodIndex(A["month"], freq="M")
    A = A.set_index("month").sort_index()
    flow = A["net_inflow"] / A["aum"].shift(1) * 100
    q = q[q.index >= pd.Period("2018-05", "M")]
    fig, axs = plt.subplots(2, 1, figsize=(W1, 3.6), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
    axs[0].plot(q.index.to_timestamp(), q.values, color=BLUE, lw=1.4)
    axs[0].set_ylabel("80th percentile\nof the basis (bp)")
    f = flow[flow.index >= pd.Period("2018-05", "M")]
    axs[1].bar(f.index.to_timestamp(), f.values, width=25, color=[BLUE if v >= 0 else RED for v in f.values], lw=0)
    axs[1].set_ylabel("Net inflow\n(% of assets)")
    axs[1].set_ylim(-45, 40)
    for a in axs:
        a.axvline(pd.Timestamp("2023-04-01"), color=MUTED, lw=0.8, ls="--")
    fig.tight_layout(h_pad=0.6)
    save(fig, "fig_h4_flows")


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
    labels = ["< 0.60"] + [f"{a:.2f} to {b:.2f}" for a, b in zip(edges[1:-1], edges[2:])]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.plot(x, U.values, color=RED, marker="o", ms=5, label="Upper tail (rich futures)")
    ax.plot(x, L.values, color=BLUE, marker="s", ms=5, label="Lower tail (cheap futures)")
    ax.axhline(0.2, color=MUTED, lw=0.7, ls=":")
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_xlabel("Utilisation of the position limit the day before")
    ax.set_ylabel("Share of days")
    ax.legend(loc="upper left")
    save(fig, "fig_h9_tails")


def spurious():
    rules = ["Old rule: gross open interest,\nold-formula limit", "Actual rule: delta-adjusted open\ninterest, new limit",
             "Gross open interest,\nnew limit", "Delta-adjusted open interest,\nold-formula limit"]
    vals = [1505, 412, 6256, 1]
    cols = [GREY, BLUE, LIGHT, LIGHT]
    fig, ax = plt.subplots(figsize=(W1, 2.3))
    yy = np.arange(len(rules))[::-1]
    bars = ax.barh(yy, vals, color=cols, height=0.58)
    ax.set_xlim(0, 7300)
    label_bars(ax, bars)
    ax.set_yticks(yy); ax.set_yticklabels(rules); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Ban stock-days, 1 October 2025 to 27 October 2026")
    save(fig, "fig_spurious")


def covid():
    P = pd.read_csv(os.path.join(PROC, "mwpl_oi_panel.csv.gz"), usecols=["date", "symbol", "mwpl", "util"], parse_dates=["date"])
    P = P.sort_values(["symbol", "date"])
    P["r"] = P.groupby("symbol")["mwpl"].pct_change() + 1
    rest = set(P[(P["date"] == "2020-11-26") & P["r"].between(1.8, 2.2)]["symbol"])
    days = np.sort(P["date"].unique())
    i0 = int(np.searchsorted(days, np.datetime64("2020-11-27")))
    win = days[i0 - 40:i0 + 41]
    Q = P[P["date"].isin(win)].copy()
    Q["g"] = np.where(Q["symbol"].isin(rest), "restored", "other")
    Q["k"] = Q["date"].map({d: j - 40 for j, d in enumerate(win)})
    # utilisation measured at the end of day t-1 applies to day t: plot the file-date utilisation against file day
    m = Q.groupby(["k", "g"])["util"].mean().unstack() * 100
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.plot(m.index, m["restored"], color=BLUE, label=f"Stocks whose limit was restored ({len(rest)})")
    ax.plot(m.index, m["other"], color=GREY, label="Other F&O stocks")
    ax.axvline(-0.5, color=RED, lw=0.9, ls="--")
    ax.text(0.5, ax.get_ylim()[1] * 0.96, "limit restored, 27 Nov 2020", color=RED, fontsize=7, va="top")
    ax.set_xlabel("Trading days relative to the restoration")
    ax.set_ylabel("Mean utilisation of the MWPL (%)")
    ax.legend(loc="lower left", fontsize=7)
    save(fig, "fig_covid")


# ------------------------------------------------------------------------------------------------ ban chapter
def ban_R():
    A = futures_activity()
    b = A[A["ban"] & ~A["expiry_day"] & A["R"].notna()].copy()
    b["month"] = b["date"].dt.to_period("M").dt.to_timestamp()
    m = b.groupby("month")["R"].median()
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.axvspan(pd.Timestamp("2020-03-23"), pd.Timestamp("2025-10-01"), color=PALE, lw=0)
    ax.plot(m.index, m.values, color=BLUE, lw=1.2, marker="o", ms=2.5)
    ax.text(pd.Timestamp("2022-09-01"), 1.08, "peak intraday checks", color=BLUE, fontsize=7, ha="center")
    ax.text(pd.Timestamp("2017-08-01"), 1.08, "end-of-day checks", color=MUTED, fontsize=7, ha="center")
    ax.set_ylim(-0.08, 1.2)
    ax.set_ylabel("Median on ban days of\n(change in OI + volume) / volume")
    save(fig, "fig_ban_R")


def h8_era():
    # analysis/output/h8_results.txt and docs/14 §14.2
    fig, axs = plt.subplots(1, 2, figsize=(W1, 2.2))
    eras = ["End-of-day\nchecks", "Peak intraday\nchecks"]
    ax = axs[0]
    bars = ax.bar(eras, [-0.97, -2.72], color=[GREY, BLUE], width=0.55)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() - 0.12, f"{b.get_height():.2f}", ha="center",
                va="top", fontsize=8, fontweight="bold", color=INK)
    ax.set_ylim(-3.2, 0.2); ax.axhline(0, color=MUTED, lw=0.7)
    ax.set_title("Effect of a ban on log futures contracts", fontsize=8)
    ax = axs[1]
    lab = ["End-of-day\nchecks", "Peak intraday\nchecks", "Delta rule\n(from Dec 2025)"]
    bars = ax.bar(lab, [0.871, 0.011, 0.357], color=[GREY, BLUE, RED], width=0.55)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.02, f"{b.get_height():.2f}", ha="center",
                fontsize=8, fontweight="bold")
    ax.set_ylim(0, 1.05)
    ax.set_title("Median R on ban days (0 = every trade closes)", fontsize=8)
    fig.tight_layout(w_pad=2.5)
    save(fig, "fig_h8_era")


def h7_dots():
    # h7_results.txt, h7_iv.txt, placebos.txt
    rows = [("Pre-specified", -0.089, 0.037, 0.081, 0.030), ("Noise-corrected (IV)", -0.190, 0.077, 0.088, 0.015),
            ("False ban dates", 0.037, 0.047, -0.028, 0.038)]
    fig, axs = plt.subplots(1, 2, figsize=(W1, 2.2), sharey=True)
    yy = np.arange(len(rows))[::-1]
    for ax, j, ttl in [(axs[0], 1, "Upper regime (rich futures)"), (axs[1], 3, "Lower regime (cheap futures)")]:
        for k, r in enumerate(rows):
            col = GREY if r[0].startswith("False") else BLUE
            ax.errorbar(r[j], yy[k], xerr=1.96 * r[j + 1], fmt="o", color=col, ms=6, elinewidth=1.4, capsize=0)
            ax.text(r[j], yy[k] + 0.22, f"{r[j]:+.3f}", ha="center", fontsize=7, color=MUTED)
        ax.axvline(0, color=MUTED, lw=0.7)
        ax.set_title(ttl, fontsize=8)
        ax.grid(axis="x"); ax.grid(axis="y", visible=False)
        ax.set_ylim(-0.6, len(rows) - 0.4)
    axs[0].set_yticks(yy); axs[0].set_yticklabels([r[0] for r in rows]); axs[0].tick_params(axis="y", length=0)
    axs[0].annotate("model predicts > 0", (0.98, 0.04), xycoords="axes fraction", ha="right", fontsize=7, color=RED)
    axs[1].annotate("model predicts ≤ 0", (0.98, 0.04), xycoords="axes fraction", ha="right", fontsize=7, color=RED)
    fig.text(0.5, -0.04, "Change in the reversion slope on ban days (95% interval)", ha="center", fontsize=8.5)
    fig.tight_layout(w_pad=1.5)
    save(fig, "fig_h7_dots")


def level_profile():
    import level_effect as le
    D = le.build()
    E, _ = le.events(D, False)
    Cd = le.candidates(D, False)
    Mi = le.match(E, Cd)
    ks, P = le.paths(D, E, Cd, Mi, "m")
    hi = (E["C"] > E["C"].median()).values
    fig, ax = plt.subplots(figsize=(W1, 2.7))
    ax.axvspan(-0.5, 4.5, color=PALE, lw=0)
    with np.errstate(all="ignore"):
        ax.plot(ks, np.nanmean(P[hi], axis=0), color=RED, lw=1.5, label="Fast open-interest build-up (above median)")
        ax.plot(ks, np.nanmean(P[~hi], axis=0), color=GREY, lw=1.5, label="Slow build-up (below median)")
        ax.plot(ks, np.nanmean(P, axis=0), color=BLUE, lw=2.0, label="All entries")
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.text(2, ax.get_ylim()[1] * 0.92, "first five days", ha="center", fontsize=7, color=MUTED)
    ax.set_xlabel("Trading days relative to the first ban day")
    ax.set_ylabel("Change in the basis from day -1,\ntreated minus controls (bp)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=7)
    save(fig, "fig_level_profile")


def level_groups():
    # level_effect_results.txt, level_effect_buildup.txt, placebos.txt (means and standard errors, bp)
    rows = [("All entries, at mean composition (889)", -6.41, 1.84), ("Falling open interest before (30)", 8.4, 10.9),
            ("Rising open interest before (859)", -6.8, 1.8), ("Long build-up (453)", -7.9, 2.7),
            ("Short build-up (406)", -5.5, 2.2), ("False entries (510)", 0.98, 1.46)]
    fig, ax = plt.subplots(figsize=(W1, 2.6))
    yy = np.arange(len(rows))[::-1]
    for k, r in enumerate(rows):
        col = GREY if r[0].startswith("False") else (RED if "Falling" in r[0] else BLUE)
        ax.errorbar(r[1], yy[k], xerr=1.96 * r[2], fmt="o", color=col, ms=6, elinewidth=1.4, capsize=0)
        ax.text(r[1], yy[k] + 0.25, f"{r[1]:+.1f}", ha="center", fontsize=7, color=MUTED)
    ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows]); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Change in the basis over the first ban days, treated minus controls (bp, 95% interval)")
    save(fig, "fig_level_groups")


def density():
    import density_test as dt
    P = dt.panel()
    pre = P[(P["date"] >= "2015-01-01") & (P["date"] < dt.REFORM)]
    main_pop = pre[~pre["ban_prev"].fillna(True).astype(bool) & ~pre["ban"] & (pre["omega_prev"] < dt.C)]
    x = main_pop["omega"].values
    x = x[(x >= 0.80) & (x < 1.10)]
    fig, ax = plt.subplots(figsize=(W1, 2.4))
    ax.hist(x, bins=np.arange(0.80, 1.10001, 0.005), color=BLUE, edgecolor="white", lw=0.4)
    ax.axvline(0.95, color=RED, lw=0.9, ls="--")
    ax.text(0.953, ax.get_ylim()[1] * 0.92, "95% trigger", color=RED, fontsize=7)
    ax.set_xlabel("Utilisation of the MWPL at the end of the day (stocks below 95% the day before)")
    ax.set_ylabel("Stock-days per bin")
    save(fig, "fig_density")


def rd_plot():
    import rd_95
    F = rd_95.frame()
    F = F[(F["date"] < "2025-10-01") & (F["x"] >= 0.80) & (F["x"] < 1.10)]
    bins = np.arange(0.80, 1.1001, 0.01)
    F["b"] = pd.cut(F["x"], bins)
    g = F.groupby("b", observed=True).agg(x=("x", "mean"), fut=("ly_fut", "mean"), m=("m", "mean"))
    fig, axs = plt.subplots(1, 2, figsize=(W1, 2.4))
    for ax, col, ttl in [(axs[0], "fut", "log(1 + futures contracts) on day t"), (axs[1], "m", "Basis on day t (bp)")]:
        lo, hi = g[g["x"] < 0.95], g[g["x"] >= 0.95]
        ax.scatter(lo["x"], lo[col], s=14, color=GREY)
        ax.scatter(hi["x"], hi[col], s=14, color=BLUE)
        for part, c in [(lo, GREY), (hi, BLUE)]:
            p = np.polyfit(part["x"], part[col], 1)
            xs = np.linspace(part["x"].min(), part["x"].max(), 10)
            ax.plot(xs, np.polyval(p, xs), color=c, lw=1.3)
        ax.axvline(0.95, color=RED, lw=0.9, ls="--")
        ax.set_title(ttl, fontsize=8)
        ax.set_xlabel("Utilisation at the end of day t-1")
    fig.tight_layout(w_pad=2)
    save(fig, "fig_rd")


# ------------------------------------------------------------------------------------------------ eligibility chapter
def h6_es():
    # event-time profile of the Callaway-Sant'Anna delay estimates, analysis/output/h6_results.txt (cells with n >= 19)
    ent = {-7: -0.036, -6: -0.057, -5: -0.018, -4: 0.013, -3: 0.009, 0: -0.090, 1: -0.218, 2: -0.097, 3: -0.093,
           4: -0.065, 5: -0.079, 6: -0.014}
    ext = {-6: 0.022, -5: -0.019, -4: -0.012, -3: 0.010, 0: 0.034, 1: 0.128, 2: 0.021, 3: 0.053, 4: 0.027, 5: -0.006}
    fig, ax = plt.subplots(figsize=(W1, 2.5))
    ax.axvspan(-2.5, -0.5, color=PALE, lw=0)
    for d, col, lab, mk in [(ent, BLUE, "Entry into the F&O segment", "o"), (ext, RED, "Eligibility exit", "s")]:
        k = sorted(d)
        pre = [e for e in k if e < 0]; post = [e for e in k if e >= 0]
        ax.plot(pre, [d[e] for e in pre], color=col, marker=mk, ms=5, lw=1.4, label=lab)
        ax.plot(post, [d[e] for e in post], color=col, marker=mk, ms=5, lw=1.4)
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.text(-1.5, -0.20, "base and\nevent years", ha="center", fontsize=7, color=MUTED, va="bottom")
    ax.set_xlabel("Years relative to the first full year after the event")
    ax.set_ylabel("Change in price delay")
    ax.legend(loc="upper left", fontsize=7)
    save(fig, "fig_h6_es")


def h5_legs():
    # h5_results.txt: G3 minus G1 legs (% a month, Newey-West s.e.)
    rows = [("Short leg, value-weighted", 0.04, 0.20), ("Long leg, value-weighted", -0.03, 0.14),
            ("Short leg, equal-weighted", -0.49, 0.16), ("Long leg, equal-weighted", 0.46, 0.15),
            ("Momentum short leg, value-weighted", -0.51, 0.22)]
    fig, ax = plt.subplots(figsize=(W1, 2.3))
    yy = np.arange(len(rows))[::-1]
    for k, r in enumerate(rows):
        col = BLUE if "value" in r[0] else GREY
        ax.errorbar(r[1], yy[k], xerr=1.96 * r[2], fmt="o", color=col, ms=6, elinewidth=1.4, capsize=0)
        ax.text(r[1], yy[k] + 0.25, f"{r[1]:+.2f}", ha="center", fontsize=7, color=MUTED)
    ax.axvline(0, color=MUTED, lw=0.7)
    ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows]); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Cash-only stocks without SLB trades minus F&O stocks (% a month, 95% interval)")
    save(fig, "fig_h5_legs")


# ------------------------------------------------------------------------------------------------ model figures
def model():
    src = open(os.path.join(ROOT, "models_src", "modelC", "verify_modelC.py")).read()
    src = src.replace('matplotlib.use("Agg")', "")
    for a, b in [('"figs/fig_path.pdf"', repr(os.path.join(FIG, "model_path.pdf"))),
                 ('"figs/fig_hist.pdf"', repr(os.path.join(FIG, "model_hist.pdf"))),
                 ('"figs/fig_band.pdf"', repr(os.path.join(FIG, "model_band.pdf"))),
                 ('"#1F3A5F"', repr(BLUE)), ('"#C9D6E8"', repr(PALE)), ('color="0.6"', f'color="{GREY}"'),
                 ('color="0.55"', f'color="{GREY}"'), ("figsize=(7.5, 5.2)", "figsize=(6.3, 4.0)"),
                 ("figsize=(6.2, 3.4)", "figsize=(6.3, 2.8)")]:
        src = src.replace(a, b)
    cwd = os.getcwd()
    os.chdir(os.path.join(ROOT, "models_src", "modelC"))
    try:
        exec(compile(src, "verify_modelC", "exec"), {"__name__": "__verify__"})
    finally:
        os.chdir(cwd)
    print("  wrote model_path, model_hist, model_band")


ALL = ["timeline", "util_example", "arb_aum", "ban_month", "mwpl_ratio", "basis_dist", "basis_expiry", "index_fig",
       "band_scatter", "band_years", "cost_band", "h3_placebo", "h4_flows", "h9_tails", "spurious", "covid", "ban_R",
       "h8_era", "h7_dots", "level_profile", "level_groups", "density", "rd_plot", "h6_es", "h5_legs", "model"]

if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    for w in (sys.argv[1:] or ALL):
        print(w)
        globals()[w]()
