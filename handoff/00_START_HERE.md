# HANDOFF: START HERE

You are taking over an ongoing research project. This folder is written so that a new chat or a new model, with no
memory of earlier work, can reach the same depth of context as the assistant that has worked on it so far. Read it fully
before doing anything. Last full update: **5 November 2026, end of session** (resume card: `16_resume_here.md`) (see `CHANGELOG.md` for every later change).

---------------------------------------------------------------------------------------------------------------------

## 1. The project in five sentences

1. This is **Prince Kumar's** (roll 23B3032, BS Economics, IIT Bombay, 2023 to 2027) Bachelor's thesis, EC 495 (Stage I,
   6 credits, semester 7) followed by EC 497 (Stage II, 12 credits, semester 8), guided by **Prof. Aditi Chaubal**
   (Economics; non-linear time series).
2. Title: **Limits to Arbitrage in the Indian Equity Market.** Question: how strongly do limits to arbitrage (trading
   costs, short-sale constraints, arbitrage capital, arbitrage risk, position limits) bind in Indian equities, and how much
   mispricing do they explain?
3. The sharpest lens is India's **F&O ban**: when market-wide open interest in a stock's derivatives exceeds 95% of its
   market-wide position limit (MWPL), every trader may only reduce positions until it falls to 80%. It is essentially
   unstudied. But the project is **broader than the ban** (user's explicit instruction).
4. Method order: **theory first** (the guide asked for it) → a **pre-analysis plan** frozen with a git tag before any
   outcome is related to any treatment → a **blind data build** from free NSE archives → tests → interpretation.
5. Status on 5 Nov 2026: theory done and verified; data built and audited; pre-analysis plan frozen (`pap-v1`);
   all four primary tests run and Holm-corrected (H8, H3, H6 rejected at 5%; H7 rejected its prediction with the
   opposite sign; see `04_current_state.md` §4.7 to 4.9 and `docs/14_results.md`); secondary tests next.

## 2. Reading order (do not skip)

| # | File | Why |
|---|---|---|
| 0 | **`16_resume_here.md`** | **Exactly where the last session stopped and the first actions for the next one (read right after this file)** |
| 1 | this file | Orientation, rules, bootstrap prompt |
| 2 | `01_project_overview.md` | The research design in full |
| 3 | `02_people_rules_and_working_style.md` | Who the user and guide are; every durable rule (several are strict) |
| 4 | `03_history_and_decisions.md` | Everything that happened, in order, and why each decision was taken |
| 5 | `04_current_state.md` | Exactly what exists now, what the guide has seen, what is pending |
| 6 | `05_next_steps.md` | The detailed work plan from here |
| 7 | `06_theory.md` | The model (all propositions, equations, numerical checks) |
| 8 | `07_test_plan.md` | The frozen pre-analysis plan, explained, with implementation notes |
| 9 | `08_data_pipeline.md` | Every script, every data set, every column, every data quirk and its fix |
| 10 | `09_key_numbers.md` | Every verified number, with its source file |
| 11 | `10_institutional_facts.md` | Every SEBI/NSE rule and date, with verification status |
| 12 | `11_literature.md` | What each paper says (verified from the PDFs), and positioning |
| 13 | `12_repo_map.md` | Every file in the repository and what it is |
| 14 | `13_environment_and_tooling.md` | How the cloud container, NSE access, git and LaTeX behave |
| 15 | `14_open_issues_and_risks.md` | Open threads, unresolved questions, risks, things to verify |
| 16 | `15_maintenance_protocol.md` | How to keep this folder and `memory/` current |
| 17 | `16_resume_here.md` | Resume card: where we stopped, rebuild list, next tests in order (update it at every session end) |

Deeper material, when needed: `docs/` (polished final-form documentation for outside readers), `memory/` (the
assistant's running notes, including the full session log `memory/05_session_log.md`), `plan/` (master plan, frozen test
plan, archive of all earlier plans and a register of everything removed), the PDFs at the repo root, and `references/`.

## 3. Non-negotiable rules (summary; full list in 02)

1. **Save continuity regularly.** After every meaningful step (decision, new document, finding, user correction): update
   `memory/` (append to `memory/05_session_log.md`) **and** the relevant files of this `handoff/` folder (and add a line
   to `handoff/CHANGELOG.md`), then commit and push to the working branch. The container is ephemeral.
2. **Work on branch `claude/compassionate-rubin-s9gny2`** of `deviant7/bsp`. Never push elsewhere without permission.
   No pull request unless the user asks. Commit trailers (exact):
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and
   `Claude-Session: https://claude.ai/code/session_01M6SKm82udXsHf6727aGMNw` (a new session will have its own session
   link; use the one your environment gives you). Never put model names or identifiers in repo files.
3. **The test plan is frozen.** Run tests exactly as `plan/pre_analysis_plan_v1.md` specifies. Any change goes in its §11
   "Deviations log" with date and reason, and results under the original specification are always reported.
4. **Honesty and rigour.** Read primary sources, not just notes. Flag errors plainly, including errors in earlier work by
   the assistant. Report nulls.
5. **No timelines.** The user said to ignore deadlines entirely; order work by logical dependency.
6. **Guide-facing documents** contain no internal references (no model letters A/B/C, no "audit", no memory or plan
   versions, no file paths, no past mistakes), no em dashes, no AI-sounding phrases; plain first-person academic language.
7. **Keep every past plan and every deletion** (`plan/archive/` and `plan/archive/REMOVED_ITEMS_REGISTER.md`).
8. **`docs/` describes only the final form** of the project (no history). Keep it current when something final changes.
9. The user's email (23b3032@iitb.ac.in) identifies the user only; never send it to any service.

## 4. Bootstrap prompt (the user can paste this into a new chat)

> You are continuing my BS thesis project in the repository `deviant7/bsp`, branch `claude/compassionate-rubin-s9gny2`.
> Before doing anything, read `CLAUDE.md`, then `handoff/16_resume_here.md`, then every file in `handoff/` in the order given in
> `handoff/00_START_HERE.md`, then skim `memory/05_session_log.md` and `plan/pre_analysis_plan_v1.md`. Do not rely on
> summaries alone where a primary file exists. When you have finished, (1) summarise where the project stands in about
> ten lines, (2) list the next three concrete steps from `handoff/05_next_steps.md`, (3) list anything in the handoff
> that looks inconsistent with the repository as you find it, and (4) wait for my go-ahead. Follow every rule in
> `handoff/02_people_rules_and_working_style.md`, and keep `memory/` and `handoff/` updated as you work.

## 5. Self-check: you are ready when you can answer these without looking

1. What does the F&O ban restrict, and for whom? (Everyone; only position-reducing trades; all expiries; futures and
   options of that stock; entry above 95% of MWPL at end of day, exit at 80%.)
2. Why is the MWPL not a valid instrument for ban status? (It moves the anticipation term pi(omega) and entity caps even
   when no ban occurs, so it violates exclusion.)
3. Why is the basis built from VWAPs and not settlement prices? (NSE sets a theoretical cost-of-carry settlement price
   when a future does not trade in the last half hour; bans thin trading, so a settlement basis would mechanically shrink.)
4. What are the four primary hypotheses? (H7 one-sided correction in bans; H8 trading moves out of futures; H3 costs set
   band edges around STT dates; H6 F&O entry/exit changes bad-news drift and price delay.)
5. What did the 5 Nov 2026 audit find about results dates? (The filing feed often carried late re-filing times and current
   symbols; 51.5% of F&O events were dated too late; rebuilt from "Financial Result Updates" announcements, board
   meetings and ISIN history.)
6. What has the guide seen? (The project document of September 2026 and the progress report PDF of October 2026, which
   she liked; she gave the go-ahead.)
7. Is the git tag `pap-v1` on GitHub? (Yes, since 5 Nov 2026: created by the user, pointing to commit 85dac3a. Cloud
   sessions cannot push tags through their git proxy.)
