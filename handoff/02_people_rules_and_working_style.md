# 02. People, rules and working style

## 2.1 The user (Prince Kumar)

- 4th-year BS Economics student at IIT Bombay (minor not relevant to the project).
- Background: quantitative research intern at a trading firm (mid-frequency desk). Built an F&O long-short pipeline, iron
  condor strategies, merger arbitrage work, WorldQuant-style alphas, a library of about 45 long-short signals. Works on
  Indian markets. Knows markets well; wants academic rigour on top.
- Uses voice typing; messages may contain transcription slips (e.g. "Chawla" for Chaubal). Interpret charitably and
  confirm names before putting them into documents.
- Earlier sessions ran on his Windows folder `D:\BSP` through a desktop bridge (Claude desktop with a project library).
  Since 28 Oct 2026 the GitHub repository is the single store; work happens in Claude Code cloud sessions.
- The internship signal library may be under an agreement (NDA/IP); it is **not** used unless he confirms it is cleared.

## 2.2 The guide (Prof. Aditi Chaubal)

- Economics faculty, IIT Bombay; works on non-linear time series (relevant: threshold and smooth-transition models).
- Approved the project (the "limits to arbitrage" programme) from the original proposal.
- Her key instruction (about September 2026): **build a theoretical, mathematical model of what the project will show
  before any empirical work**, so conclusions are derived from theory and the risk of confirmation bias and overfitting is
  lower.
- What she has seen: the original proposal (`BSP Proposal.docx`, not in the repo), the project document (September 2026;
  `BSP_Project_Document.docx/.pdf`), and the progress report `BSP_Progress_Report_Oct2026.pdf` (26 pages, with the full
  model as an appendix). **She liked the report and gave the go-ahead for further work** (user, 5 Nov 2026).
- She has **not** seen: the earlier Models A and B, the 28 Sep 2026 progress note, the literature review PDF, the test plan
  as a separate document, or any internal notes.
- Questions the user said he would raise with her personally (removed from the report at his request, text kept in
  `progress_report_src/removed_guidance_questions.tex`): (1) is the wider framing acceptable; (2) is the theory at the
  right depth; (3) threshold models versus smooth-transition models, and state-dependent thresholds; (4) access to a
  database with EPS and shareholding (e.g. CMIE Prowess); (5) does she want the test plan before the main estimates. His
  report of her reaction (5 Nov): she liked it and approved continuing. No specific answers to these were relayed.

## 2.3 Durable rules from the user (all still in force)

| # | Rule | Given |
|---|---|---|
| 1 | **Save to memory regularly**: after any meaningful step update `memory/`, append to `memory/05_session_log.md`, and commit and push. Now also: keep `handoff/` current (see 15) | 28 Oct 2026; extended 5 Nov 2026 |
| 2 | Thorough, unbiased, academically rigorous work; read primary sources line by line, not just notes or abstracts; flag errors honestly, including the assistant's own earlier errors | from the start |
| 3 | **Ignore timelines entirely**; no time pressure; order work by logic, never by Stage I/II weeks | 28 Oct 2026 |
| 4 | The project is **limits to arbitrage in Indian equities broadly**; the F&O ban is an important focus, not the whole project | 28 Oct 2026 |
| 5 | Keep the project document's goals (he likes them), while correcting its errors | 28 Oct 2026 |
| 6 | **Keep every past plan and every deletion**: archive plan versions in `plan/archive/`, log every removed or changed item in `REMOVED_ITEMS_REGISTER.md` with why and how to reintroduce | 28 Oct 2026 |
| 7 | **Guide-facing documents: no internal references** (no Model A/B/C labels, "audit", memory files, plan versions, phases, file paths, reading-status notes, past mistakes). Self-contained academic writing. **No em dashes, no AI-sounding phrases**, plain first-person language, jargon only when needed. One PDF to the guide at a time | 28 Oct 2026 |
| 8 | Keep the existing model; no further theory unless the data demand it; "mostly data from now on" (answer to his question "can we work with data without modelling?") | 28 Oct 2026 |
| 9 | Wait for the guide before freezing the test plan (done: she gave the go-ahead; plan frozen 5 Nov 2026) | 28 Oct 2026 |
| 10 | **`docs/` = documentation of the final project form only**, for readers without domain knowledge; very thorough; only finalised items; separate Markdown files | 5 Nov 2026 |
| 11 | **`handoff/` = everything a new chat/model needs**, as extensive as possible: everything done, everything planned, all context | 5 Nov 2026 |

## 2.4 Working style the user expects

- Opens a new session by asking for "full and extensive context": read the conversations, memory, artefacts, every file;
  then give a brief summary of where things stand, and only then act.
- Wants deep, honest assessments rather than reassurance; prefers clean identification over descriptive work; the thesis
  may become a working paper.
- Likes deliverables as compiled LaTeX PDFs with sources saved, and plain-language short versions for the guide.
- Wants to be told plainly when something earlier was wrong (e.g. the audit of Models A/B, the results-date problem).
- Gives short go-ahead messages ("yes go ahead"); expects the assistant to carry a task through and save state.
- Asks questions mid-way ("do we really need X?"): answer directly with a recommendation.

## 2.5 Git and repository rules

- Branch: `claude/compassionate-rubin-s9gny2`. Push with `git push -u origin claude/compassionate-rubin-s9gny2`; retry on
  network errors with backoff (2, 4, 8, 16 s).
- If the branch's PR has been merged, restart the branch from the latest `main` for new work (that happened once: PR #1
  merged 28 Oct 2026, merge commit 65ef0e3).
- No pull request unless the user asks. If one is created, mirror any PR template.
- Commit messages: clear and descriptive, ending with the two trailer lines given in 00 (section 3).
- Never put model names or identifiers in commits, code, docs or any repo file.
- Raw data (`data/raw/`) and `data/processed/basis_panel.csv.gz` are git-ignored (too large); everything else is committed.
- `__pycache__/` is ignored (it was committed once by mistake and removed).

## 2.6 Writing style for guide-facing text (checklist)

- First person ("I built", "I find"), plain sentences, short paragraphs.
- No em dashes (use commas, colons or parentheses). No "delve", "crucially", "it is worth noting", "in conclusion" and the
  like.
- No mention of how the work was produced, of internal files, model versions, audits, or earlier mistakes.
- Numbers must come from the current data build; regenerate tables rather than typing numbers by hand.
- Build PDFs from LaTeX (`pdflatex` twice); keep sources; never hand-edit PDFs.
