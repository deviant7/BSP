# 05 — Session log (append newest at bottom)

## Before this repo (from the two conversation logs)
- Project selection (Very old conversation): Program A (limits to arbitrage / F&O ban) chosen over Program B (retail transformation).
- Project document written (Sep 2026). Guide asked for a theoretical framework first.
- Recent conversation: literature collected (21 PDFs), notes batches 1–5, 29-pp literature review (LaTeX), Models A & B (full + 3-pp guide
  versions), progress report to guide (Sep 28 2026) asking which model to lead with. No data work yet.

## Session 28 Oct 2026 (cloud session, branch claude/compassionate-rubin-s9gny2)
- Read both conversation logs, the project doc (docx = pdf), all 21 references in full (Shleifer–Vishny via OCR), notes, lit review,
  models, progress report. Built the audit in `04_models_and_audit.md` and the verified digest in `02_literature_digest.md`.
- User instruction: save memory regularly → created `CLAUDE.md` + `memory/` (this folder).
- User question: is the project-doc plan right, and is the pivot to modelling right? Advice given (summary):
  1. Guide's principle (theory before data) is right *for the core mechanism*, especially because the ban's effect on the basis has
     no obvious sign. But Models A/B were built to deliver H1–H6, so they rationalise the plan rather than discipline it; and they
     mis-model the ban (it freezes fresh OI for everyone). As built, they don't give the protection the guide wanted.
  2. Real guard against confirmation bias = a short corrected model whose predictions can come out either way + a written,
     git-timestamped pre-analysis plan (outcomes, specs, signs, tests) before looking at outcome–treatment relationships.
  3. Project-doc plan is too broad for the time left (6 chapters, 3 mispricing measures, 4 frameworks), has data gaps (EPS, accounting
     data), a circular constraint index, weak pre-2025 instrument, and all-confirmatory "expected results".
  4. Recommended core: (a) one model of the ban as a market-wide freeze of fresh futures OI, with daily-horizon arbitrageurs;
     (b) data pipeline built in parallel, blind to outcomes (treatment-side descriptives allowed); (c) identification: ban-entry
     event study vs near-miss controls, RD at 95% with McCrary, and the 1 Oct 2025 MWPL formula change as a continuous-treatment
     DiD using predicted ΔMWPL from pre-reform FF & ADDV; (d) TVECM bands pre/post as the dynamics lens.
     Demote: constraint index → descriptive; PCP → robustness if option data adequate; PEAD → only if EPS via Prowess/library;
     45-signal FM → drop/appendix (also check internship NDA/IP on the signal library). Policy chapter short.
  5. Timeline risk: Stage I ends ~Nov 2026; aim by then for corrected model + PAP + dataset + descriptives.

## Open threads
- Guide's response on model choice / the re-scoped plan.
- Fix project doc (short-selling line, "relaxations", timeline with theory stage).
- Fix lit-review / notes / reference-index errors (listed in 04) — awaiting user go-ahead.
- Verify 80% ban-exit rule and historical 30× volume MWPL leg from NSE circulars.
- Data feasibility: ban list archive depth, combined OI files back to 2015, option settle-price quality, EPS source.
