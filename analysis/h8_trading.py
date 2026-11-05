"""H8 (primary): in a ban, trading moves out of futures. Specification: PAP §5 and §11 C3.

Outputs analysis/output/h8_results.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from samples import futures_activity, ROOT
from inference import feols, coef_table

rng = np.random.default_rng(8)
OUT = os.path.join(ROOT, "analysis", "output")


def boot_mean(df, col, B=999):
    """Stock-clustered bootstrap CI for the mean and median of col."""
    g = {s: v[col].values for s, v in df.groupby("symbol")}
    keys = list(g)
    means, meds = [], []
    for _ in range(B):
        x = np.concatenate([g[k] for k in rng.choice(keys, len(keys))])
        means.append(x.mean()); meds.append(np.median(x))
    return np.percentile(means, [2.5, 97.5]), np.percentile(meds, [2.5, 97.5])


def main():
    A = futures_activity()
    r = ["H8: trading moves out of futures in a ban (PAP §5, §11 C3)", ""]
    pre = A[(A["date"] >= "2015-01-01") & (A["date"] < "2025-10-01") & ~A["expiry_day"]].copy()
    r.append(f"pre-reform non-expiry F&O stock-days: {len(pre)}; ban days {int(pre['ban'].sum())}")

    # identity test
    b = pre[pre["ban"] & pre["R"].notna()]
    c = pre[~pre["ban"] & pre["omega_lag"].between(0.80, 0.95, inclusive="left") & pre["R"].notna()]
    ci_m, ci_md = boot_mean(b, "R")
    r += ["", "Identity test: R = (Delta OI + volume) / volume, near + next contracts",
          f"  ban days (n={len(b)}, stocks {b['symbol'].nunique()}): mean {b['R'].mean():.4f} [95% CI {ci_m[0]:.4f}, {ci_m[1]:.4f}], "
          f"median {b['R'].median():.4f} [{ci_md[0]:.4f}, {ci_md[1]:.4f}]",
          f"    quantiles p10/p25/p75/p90: " + "/".join(f"{b['R'].quantile(q):.3f}" for q in (.1, .25, .75, .9)),
          f"    share of ban days with R <= 0.01: {(b['R'] <= 0.01).mean():.3f}; R <= 0.05: {(b['R'] <= 0.05).mean():.3f}",
          f"  comparison non-ban days, omega_(t-1) in [0.80, 0.95) (n={len(c)}): mean {c['R'].mean():.4f}, median {c['R'].median():.4f}",
          f"  all non-ban days: mean {pre.loc[~pre['ban'], 'R'].mean():.4f}, median {pre.loc[~pre['ban'], 'R'].median():.4f}"]
    holds = (b["R"].mean() < 0.10) and (b["R"].mean() < c["R"].mean() / 10)
    r.append(f"  pre-set reading (mean < 0.10 and < 1/10 of comparison mean): identity {'HOLDS' if holds else 'DOES NOT HOLD'}")
    bb = b.copy(); bb["omega_bin"] = pd.cut(bb["omega_lag"], [0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 9], right=False)
    r.append("  ban-day R by omega_(t-1) bin: " + "; ".join(f"{k}: mean {v.mean():.3f} (n={len(v)})"
                                                      for k, v in bb.groupby("omega_bin", observed=True)["R"]))
    bb["day_of_spell"] = np.nan

    # regressions in the common-support zone
    Z = pre[pre["omega_lag"].between(0.80, 0.95, inclusive="left")].copy()
    Z["bin"] = pd.cut(Z["omega_lag"], [0.80, 0.85, 0.90, 0.95], right=False, labels=["a", "b", "c"]).astype(str)
    Z["stock_bin"] = Z["symbol"] + "_" + Z["bin"]
    Z["ban_i"] = Z["ban"].astype(int)
    Z["ly_fut"] = np.log1p(Z["vol"])
    Z["ly_cash"] = np.log1p(Z["S_qty"])
    r += ["", f"Regressions, omega_(t-1) in [0.80, 0.95): n={len(Z)}, ban days {int(Z['ban'].sum())}, stocks {Z['symbol'].nunique()}",
          "  y = a + b*Ban + stock-by-bin FE + date FE; SE two-way clustered (stock, date)"]
    res = {}
    for y, lab in [("ly_fut", "log(1 + futures contracts)"), ("ly_cash", "log(1 + cash shares traded)"),
                   ("deliv_share", "delivery share"), ("R", "R")]:
        d = Z.dropna(subset=[y])
        t = coef_table(feols(d, f"{y} ~ ban_i | stock_bin + date"))
        res[y] = t.loc["ban_i"]
        r.append(f"  {lab:32s} b = {t.loc['ban_i','b']:+.4f}  se {t.loc['ban_i','se']:.4f}  t {t.loc['ban_i','t']:+.2f}  "
                 f"n={len(d)}  (non-ban mean of y {d.loc[~d['ban'], y].mean():.4f})")
    t = res["ly_fut"]
    p_one = t["p_two"] / 2 if t["b"] < 0 else 1 - t["p_two"] / 2
    r += ["", f"Family test statistic (§11 C3 f): one-sided p that the Ban coefficient on log futures contracts < 0: p_H8 = {p_one:.3g}"]
    r.append("Prediction: futures volume falls, cash volume and delivery share rise, R close to 0 in bans.")

    # post-reform, descriptive
    po = A[(A["date"] >= "2025-10-01") & ~A["expiry_day"]]
    pb = po[po["ban"] & po["R"].notna()]
    pc = po[~po["ban"] & po["omega_lag"].between(0.80, 0.95, inclusive="left") & po["R"].notna()]
    r += ["", "Post-1 Oct 2025 (delta-based rule; descriptive only):",
          f"  ban days n={len(pb)}: mean R {pb['R'].mean():.4f}, median {pb['R'].median():.4f}; "
          f"comparison non-ban [0.80,0.95) n={len(pc)}: mean {pc['R'].mean():.4f}, median {pc['R'].median():.4f}"]
    # robustness: drop imputed ban days
    rb = b[b["ban_source"] != "imputed"]
    r.append(f"Robustness: excluding imputed ban days: n={len(rb)}, mean R {rb['R'].mean():.4f}")

    # EXPLORATORY (not pre-specified; added after seeing the identity result, 5 Nov 2026): the ban-day R distribution
    # has a break between 6 and 24 March 2020 (non-ban days show none; chg_oi equals the change in OI levels)
    r += ["", "EXPLORATORY (added after the pre-specified result was seen): split at 15 Mar 2020"]
    BRK = pd.Timestamp("2020-03-15")
    for lab, msk in [("before 15 Mar 2020", b["date"] < BRK), ("15 Mar 2020 to Sep 2025", b["date"] >= BRK)]:
        x = b[msk]
        r.append(f"  ban days {lab}: n={len(x)}, mean R {x['R'].mean():.4f}, median {x['R'].median():.4f}, "
                 f"share R <= 0.01 {(x['R'] <= 0.01).mean():.3f}")
    for lab, msk in [("before", Z["date"] < BRK), ("after", Z["date"] >= BRK)]:
        d = Z[msk]
        t = coef_table(feols(d, "ly_fut ~ ban_i | stock_bin + date"))
        r.append(f"  log futures contracts, {lab} 15 Mar 2020: b = {t.loc['ban_i','b']:+.4f} (se {t.loc['ban_i','se']:.4f}), n={len(d)}")
    txt = "\n".join(r)
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "h8_results.txt"), "w").write(txt + "\n")
    print(txt)
    return p_one


if __name__ == "__main__":
    main()
