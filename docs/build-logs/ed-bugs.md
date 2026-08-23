# Project Ed — bugs and known issues

One entry per issue. Resolved entries are never deleted: the history is the
value. Add the date and a one-line note on the fix instead.

Started 2026-08-23.

---

## OPEN — Project Ed no longer appears on its own board

**Shows up as:** the Major Quest column renders two lines. Project Ed is not one
of them, and there is no overflow marker to say it was dropped.

**Where:** `docs/interface/fill_board.py`, `MULTISTEP = 2` (line 58).

A major quest line must be a ClickUp folder holding at least two tasks — the
rule that says "a folder with one lone task is a task somebody filed in a
folder." On 2026-08-23 the `Build Log` and `PRNG OS` lists were deleted from the
Project Ed folder, leaving it with **zero** tasks. It now falls below the
threshold and is filtered out silently.

Not a defect in the rule; the rule fired correctly. The issue is that **the
board that tracks this build no longer shows this build**, and nothing on the
page says so. Three ways out, none chosen yet: put tasks back in the folder,
lower `MULTISTEP`, or special-case the folder the board itself belongs to.

Opened 2026-08-23.

## OPEN — the drift blind spot is dormant, not fixed

**Shows up as:** it does not, currently.

**Where:** `docs/interface/quest-board-v1.html`, `MAJOR_SHOWN = 3` (line 450);
sort order set in `fill_board.py`.

Major lines are sorted most-alive-first and capped at three, so a *stalled*
project sinks below the cut and lands in "the rest are in the ledger" — the
column built to catch drift hides the worst drift. Raised as the top board item
by the 2026-08-23 checkpoint, using a project that has since been deleted as its
example.

With only two major lines left, nothing is being hidden today. **The mechanism is
untouched and will bite again the moment a fourth project folder exists.**

Opened 2026-08-23.

## OPEN — placeholder board asserts invented statuses for real projects

**Shows up as:** never renders. `Object.assign(BOARD, window.BOARD_DATA)`
replaces the whole quest list whenever `board-data.js` is present.

**Where:** `docs/interface/quest-board-v1.html`, the placeholder `BOARD` literal
around lines 419–441.

Three `major` entries name real projects and give them invented task text and
statuses. Harmless while data loads, misleading to anyone reading the source
cold — and the page is designed to fall back to exactly this content when
`board-data.js` is missing, which is the situation a new reader is most likely
to be in.

A fourth entry naming a decommissioned project was removed 2026-08-23 (`5f5bff4`).
The remaining three were left deliberately.

Opened 2026-08-23.

## OPEN — dailies are still hardcoded placeholders

**Shows up as:** the Dailies column always renders the same three notes, always
at zero wear, regardless of anything in ClickUp.

**Where:** `docs/interface/fill_board.py`, `STARTER_DAILIES`.

No `daily` tag exists anywhere in the ClickUp workspace, so the fallback stands.
When the real dailies are named and tagged, the constant goes away and the
`daily` branch takes over on its own — no code change needed beyond deleting it.

Carried from the 2026-08-23 seam checkpoint. Still open.

## OPEN — interface README lists a file that was deleted

**Shows up as:** `docs/interface/README.md` line 9 documents
`ed-console-v0.html` as if it were present. The file was deleted in the
2026-08-23 doc cleanup (`e9934d8`).

Verified still present 2026-08-23. One-line fix, not yet made.

## OPEN — quest-board.md at the repo root is the v1 brief only

**Shows up as:** a cold session reading the root brief gets superseded design
rules — it still specifies dailies as "deliberately low-contrast," which V3
overturned with "separation is structural, not tonal."

The current brief with V2–V5 lives at `claude/quest-board-brief.md`, a Claude
Project doc. The repo copy has no pointer to it.

Carried from the 2026-08-23 doc cleanup. Still open.

## OPEN — `.env` from the retired local runner sits in Google Drive

**Shows up as:** a 64-byte `.env` in the Drive copy of the retired
`project-ed-local-caller` tree, alongside `config/`, `actions/`, `logs/` and
`__pycache__`.

Permissions checked 2026-08-23: **owner only, not shared with anyone.** The
secret it carries was retired the same day when the broker's Apps Script
deployment was archived — the endpoint returns 404, verified externally. So this
is hygiene, not exposure.

Recorded because the standing lesson is that the file nobody thinks of as code
is the one that leaks. Two sibling files from the same dead tree were trashed
2026-08-23; this one was left pending Ernie's call.

## OPEN — private repo history never swept

**Shows up as:** it cannot be seen from here at all.

`diane`, `prngclients` and `prngbooks` refuse anonymous clone, and git may not
be run through the device bridge. Their **working trees** were swept clean
2026-08-23; their **history** was not swept, for anything.

Needs either credentialed access from a session, or commands handed to Ernie to
run locally.

## OPEN — `Claude_data.zip` in Drive, contents unknown

A 934 KB archive dated June 2026 that matched a Drive full-text search for a
decommissioned project name. Never opened. Low priority; recorded so the next
sweep does not rediscover it as if it were new.

---

## RESOLVED

### 2026-08-23 — placeholder named a decommissioned project in a public repo

A `major` placeholder entry in `docs/interface/quest-board-v1.html` named a
project that no longer exists in ClickUp and assigned it a status. Never
rendered, but sat in a tracked file in a public repo.

Removed and pushed as `5f5bff4`. Verified gone from a fresh anonymous clone of
origin, with a positive control confirming the sweep was working.

### 2026-08-23 — `~/Projects/diane/skills/` was an unexamined folder

Flagged by the previous checkpoint as possibly holding real skills in a location
Claude Code does not read. Inspected: it contained a single `.DS_Store` and
nothing else. Moved out of the repo and deleted. No skills were lost.
