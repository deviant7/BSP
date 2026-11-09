"""Audit helper: find decimal numbers quoted in the write-ups (thesis chapters, first-results report, docs results pages)
that do not match, after rounding, any number in the analysis outputs or data reports. Flags are candidates for a manual
check, not errors (rounded figures, derived figures and institutional facts also appear).
Usage: python3 -I analysis/audit/check_numbers.py
"""
import glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = sorted(glob.glob(os.path.join(ROOT, "thesis", "ch*.tex")) + [os.path.join(ROOT, "progress_report_src", "first_results_nov2026.tex")]
             + [os.path.join(ROOT, "docs", f) for f in ("14_results.md", "15_band_estimation.md", "16_constraint_index.md", "README.md")])
REF = glob.glob(os.path.join(ROOT, "analysis", "output", "*.txt")) + glob.glob(os.path.join(ROOT, "analysis", "output", "*.csv")) + \
      glob.glob(os.path.join(ROOT, "data", "processed", "*.txt"))

num = re.compile(r"(?<![\w.])[-+−]?\d{1,3}(?:,\d{3})*(?:\.\d+)?|(?<![\w.])[-+]?\d+\.\d+")


def values(text):
    out = set()
    for m in num.findall(text):
        m = m.replace(",", "").replace("−", "-")
        try:
            out.add(float(m))
        except ValueError:
            pass
    return out


ref = set()
for f in REF:
    ref |= values(open(f, errors="ignore").read())
ref_abs = sorted(abs(v) for v in ref)


def matched(x, dec):
    tol = 0.5 * 10 ** (-dec) + 1e-9
    import bisect
    a = abs(x)
    k = bisect.bisect_left(ref_abs, a - tol)
    return k < len(ref_abs) and ref_abs[k] <= a + tol + 1e-12


flags = []
for f in SRC:
    for ln, line in enumerate(open(f), 1):
        for m in re.findall(r"(?<![\w.])[-+]?\d+\.\d+", line.replace("$-", "-").replace("$+", "+")):
            dec = len(m.split(".")[1])
            x = float(m)
            if not matched(x, dec) and not matched(x * 100, max(dec - 2, 0)) and not matched(x / 100, dec + 2):
                flags.append((os.path.relpath(f, ROOT), ln, m))
print(f"numbers not matched in outputs: {len(flags)}")
for f, ln, m in flags:
    print(f"  {f}:{ln}  {m}")
