# 13. Environment and tooling

## 13.1 Where work happens
- Claude Code cloud sessions (claude.ai/code), repository `deviant7/bsp` cloned at `/home/user/BSP`. The container is
  ephemeral: anything not committed and pushed is lost when it is reclaimed. A later session may or may not get the same
  container (on 5 Nov 2026 the old container, with `data/raw`, was still there).
- Earlier (before 28 Oct 2026): Claude desktop with a bridge to the user's Windows folder `D:\BSP` and a project library.
  The desktop era could not save PDFs to disk and hit .docx upload errors; the repo replaced it.
- GitHub access is through MCP tools (`mcp__github__*`), not the `gh` CLI. Repository scope: `deviant7/bsp`.

## 13.2 Git through the session proxy
- Pushing the working branch works: `git push -u origin claude/compassionate-rubin-s9gny2`.
- **Pushing tags failed** (HTTP 403, 5 Nov 2026), including `git push origin refs/tags/pap-v1`. Tags must be created by the
  user (or on GitHub). Do not retry endlessly.
- No PR without the user's request. PR #1 (branch → main) was merged by the user on 28 Oct 2026.

## 13.3 Software
- Python 3.13 with numpy, pandas (version 3-era warnings about `concat` sorting appear; harmless), matplotlib, openpyxl.
  `pyfixest` installable from PyPI.
- LaTeX: `apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended lmodern`
  (was installed in the 28 Oct container). Build with `pdflatex` twice.
- `pdftotext` for most PDFs; OCR for `references/1_shleifer_vishny_limits.pdf`: `apt-get install -y tesseract-ocr`,
  `pdftoppm -r 200 -gray`, `tesseract`.
- `pandoc` reads the .docx.
- Chromium and Playwright are preinstalled (not used so far).

## 13.4 Network
- Outbound HTTPS goes through an agent proxy (CA bundle `/root/.ccr/ca-bundle.crt`); see `/root/.ccr/README.md` if a tool
  fails TLS or gets 403/407.
- NSE archives (`nsearchives.nseindia.com`) and APIs (`www.nseindia.com/api/...`) are reachable with a browser
  User-Agent, `Accept: application/json` and a page `Referer`; fetching the NSE homepage returns 403, so skip cookies.
- FRED: Python connections drop; use `curl -sS -L`.
- SSRN, Wiley, JSTOR: 403 (that is why the three library papers are missing).
- niftyindices.com API refused (no Nifty total-return index).

## 13.5 Running long jobs
- Background Bash jobs are allowed; foreground `sleep` is blocked; to wait, run an `until ...; do sleep 10; done` loop in
  the background and get notified when it ends.
- The price download takes about 2.5 hours, more than a 2-hour background limit: it is resumable, so restart it.
- Downloads write into `data/raw/`; put any downloaded third-party files in their own new directory and run Python with
  `-I` (isolated mode) so nothing in a data folder can be imported as code.
- Use the scratchpad directory (given in the session's system prompt) for temporary files, not `/tmp`.

## 13.6 Disk and memory
- The writable disk is a per-session allowance; `df` can mislead. Raw data ~1.2 GB; basis panel 74 MB compressed; the basis
  builder needs several GB of RAM.

## 13.7 Commit conventions
- Descriptive message, then the trailers given in `00_START_HERE.md` §3 (use your own session link).
- Never include model names or identifiers in commits or files.
