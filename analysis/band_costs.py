"""Band chapter, C16 (g): bottom-up round-trip cost of an overnight cash-and-carry position (long cash, short stock future),
by STT period, compared with the estimated upper edge of the basis in levels (bp of the stock price).

Components (sources in docs/15_band_estimation.md):
  STT on cash delivery purchase 0.1%; STT on futures sale 0.01% (Jun 2013), 0.0125% (Apr 2023), 0.02% (Oct 2024),
  0.05% (Apr 2026); STT on physically settled stock derivatives 0.1% (NSE circular 1/2018; all stock derivatives physically
  settled from the Oct 2019 expiry); closing instead by selling cash also costs 0.1% STT.
  Stamp duty (buyer only, from 1 Jul 2020): delivery 0.015%, futures 0.002% (before: state rates, about 0.01% delivery).
  NSE transaction charges: cash 0.00322% -> 0.00297% (1 Oct 2024); futures 0.00188% -> 0.00173% (1 Oct 2024); SEBI fee
  0.0001%; GST 18% on exchange charges, SEBI fee and brokerage. Brokerage at an institutional rate: 0.01% per leg (range
  0.005% to 0.03% shown as a sensitivity).
Scenarios: (A) open and hold to expiry (buy cash, sell future, deliver at expiry); (B) roll an existing position for one
more month (buy back the expiring future, sell the next one): the marginal cost of keeping cash-and-carry capital in place.
Outputs analysis/output/band_costs.txt.
"""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from band_estimation import load, SortedData, setar_fit, QGRID, STT
from samples import ROOT

OUT = os.path.join(ROOT, "analysis", "output")
PERIODS = [  # label, futures STT %, exchange cash %, exchange futures %
    ("to Mar 2023", 0.01, 0.00322, 0.00188),
    ("Apr 2023 - Sep 2024", 0.0125, 0.00322, 0.00188),
    ("Oct 2024 - Mar 2026", 0.02, 0.00297, 0.00173),
    ("from Apr 2026", 0.05, 0.00297, 0.00173),
]


def cost(fut_stt, ex_c, ex_f, brk=0.01, stamp_d=0.015, stamp_f=0.002, sebi=0.0001, gst=0.18):
    """Returns (A, B) in bp of notional."""
    fees = lambda ex: (ex + sebi + brk) * (1 + gst)
    A = (0.1 + stamp_d + fees(ex_c)          # buy cash
         + fut_stt + fees(ex_f)              # sell future
         + 0.1 + fees(ex_c))                 # delivery at expiry (STT 0.1% on physical settlement; charges as a cash leg)
    B = (stamp_f + fees(ex_f)                # buy back expiring future
         + fut_stt + fees(ex_f))             # sell next-month future
    return A * 100, B * 100


def main():
    S = load()
    r = ["Bottom-up cost band for overnight cash-and-carry (bp of notional) and estimated upper edges (bp, levels).", "",
         "Period               | A: open + hold to expiry | B: roll one month | sensitivity A (brokerage 0.005%-0.03%/leg)"]
    for lab, fs, ec, ef in PERIODS:
        a, b = cost(fs, ec, ef)
        a_lo, _ = cost(fs, ec, ef, brk=0.005); a_hi, _ = cost(fs, ec, ef, brk=0.03)
        r.append(f"{lab:21s}|        {a:6.1f}            |      {b:5.1f}        | {a_lo:5.1f} to {a_hi:5.1f}")
    a0, _ = cost(0.01, 0.00322, 0.00188, stamp_d=0.01, stamp_f=0.002)
    r.append(f"(before July 2020 with a state stamp duty of about 0.01% on delivery: A {a0:.1f})")
    r += ["", "Estimated edges in levels (pooled threshold model on m, not demeaned; and the 80th/90th percentiles of m), non-ban days:"]
    S["m_bp"] = S["m_lag"] * 1e4
    for lab, a, b in STT:
        g = S
        if a: g = g[g["date"] >= a]
        if b: g = g[g["date"] < b]
        x, d = g["m_bp"].values, g["d"].values
        o = setar_fit(SortedData(x, np.unique(np.quantile(x, QGRID))), d)
        r.append(f"  {lab:21s} threshold model: gL {o['gL']:+6.1f}, gU {o['gU']:+6.1f}; median {np.median(x):+5.1f}; "
                 f"p80 {np.percentile(x, 80):+5.1f}; p90 {np.percentile(x, 90):+5.1f}; p95 {np.percentile(x, 95):+5.1f}")
    r += ["", "Reading: the full round trip (A, 27 to 31 bp at a 0.01% brokerage per leg) lies above the estimated upper",
          "threshold in levels (+22 to +28 bp) and the 80th percentile, and between the 90th and 95th percentiles; the",
          "marginal cost of rolling an existing position (B) is 4 to 8 bp. A band set by the cost of new entry would sit near",
          "A; a band set by funds that keep capital in place and roll would sit much lower. STT raised A by about 4 bp from",
          "the first to the last period; the estimated upper threshold did not rise in step, while the 90th percentile",
          "rose by about 2 bp in the last period. The basis is measured net of the 3-month interbank rate, so a fund whose",
          "required return differs from that rate shifts the whole band (model P2 iv)."]
    txt = "\n".join(r)
    open(os.path.join(OUT, "band_costs.txt"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
