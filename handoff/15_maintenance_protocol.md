# 15. Maintenance protocol (how continuity is kept)

The user wants two layers of continuity (5 Nov 2026):

| Layer | Folder | Purpose | Style |
|---|---|---|---|
| 1. Assistant's own memory | `memory/` + `CLAUDE.md` | Running working notes for the assistant in later sessions; the session log is the detailed chronological record | Terse, append-only log; topic files updated in place |
| 2. Handoff brief | `handoff/` | A complete, self-contained brief that any new chat or model can be pointed to and reach full context | Curated, structured, current-state first; history kept in 03 |

Both are committed to the repository; nothing important may live only in a chat or a container.

## 15.1 When to update
After every meaningful step: a decision, a user instruction or correction, a new document, a new data set or rebuild, a
finding (including a found error), a test result, a guide interaction, a git event (merge, tag). At minimum at the end of
every session and before any long-running job.

## 15.2 What to update
| Event | memory/ | handoff/ | docs/ |
|---|---|---|---|
| Any step | append to `05_session_log.md` | `CHANGELOG.md` line; `04_current_state.md` | |
| New user rule or preference | `06_user_working_style.md` | `02_people_rules_and_working_style.md` | |
| Decision or plan change | session log; plan files + `REMOVED_ITEMS_REGISTER.md` | `03_history_and_decisions.md`, `05_next_steps.md` | if it changes the final form |
| Data change or rebuild | session log | `08_data_pipeline.md`, `09_key_numbers.md` | `06`, `07`, `10`, `11`, `12` as needed |
| New fact verified or corrected | `03`/`07` in memory | `10_institutional_facts.md` | `03_institutional_setting.md` |
| Literature read | `02_literature_digest.md`, references notes | `11_literature.md` | `13_references.md` |
| Test results | session log | `04`, `05`, `09` | new `docs/14_results.md` |
| Deviation from the PAP | PAP §11 + session log | `07_test_plan.md` | `09_empirical_design.md` |
| New file or folder | | `12_repo_map.md` | `12_reproducibility.md` if part of the final form |
| Environment discovery | session log | `13_environment_and_tooling.md` | |
| New open question or risk | session log open threads | `14_open_issues_and_risks.md` | |

Then commit and push to `claude/compassionate-rubin-s9gny2`.

## 15.3 Consistency rules
- Numbers are copied from build reports, never typed from memory; when a number changes, search the repo for the old
  value (`grep -rn "old value" handoff docs memory plan`) and update every occurrence except historical records (the
  session log, the sent PDF, archived plans).
- The handoff states the **current** truth; history goes only in `03_history_and_decisions.md` and `CHANGELOG.md`.
- If the handoff and the repository disagree, the repository wins; fix the handoff and note it in the changelog.
- `memory/08_handoff_next_session.md` is the older handoff; `handoff/` supersedes it. Keep it, with a pointer.

## 15.4 How a new chat should start
Use the bootstrap prompt in `00_START_HERE.md` §4. The new chat reads `CLAUDE.md`, all of `handoff/` in order, then the
session log and the PAP, reports the state, lists inconsistencies, and waits for the user's go-ahead.

## 15.5 At the end of every session
Rewrite `16_resume_here.md` (where we stopped, last message to the user, first actions, rebuild list of git-ignored files,
next work in order, lessons that must not be lost), append the session-end entry to `memory/05_session_log.md`, update
`04_current_state.md`, `CHANGELOG.md` and `CLAUDE.md`'s state paragraph, then commit and push and confirm the tree is clean.
