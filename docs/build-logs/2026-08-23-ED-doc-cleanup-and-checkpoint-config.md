# Project Ed Checkpoint: Repo Doc Cleanup and Checkpoint Config Added

**Date:** 2026-08-23
**Repo/checkout:** `/Users/erniehathaway/Projects/ed` (branch `main`)

## Purpose

Reconcile the local checkout against `origin/main`, remove ChatGPT-era
documentation that was actively misdirecting fresh AI sessions, and give this
repo the same checkpoint config that `diane` and `prngclients` already carry —
so build logs land in a known place from here on.

## Verified state

- **`origin/main` is now `e9934d8`** (was `18c65f3`). Verified by cloning origin
  fresh into a cloud container and listing the tree: 14 tracked files.
- A client-name sweep of the entire tracked tree at `e9934d8` returns **no
  matches**. The repo is still client-data-free. (The sweep pattern itself is a
  list of client names and is therefore practice-internal — it is not recorded
  here. See Part 1.)
- `docs/interface/` local files were compared to origin by md5 **before** the
  cleanup commit — `quest-board-v1.html`, `fill_board.py`, `README.md`, and all
  three PNGs were byte-identical. Nothing needed merging or overwriting in
  either direction.
- The three generated files (`board-data.js`, `clickup_dump.json`,
  `quest-board-live.html`) are present locally and correctly gitignored. They
  carry client names and were confirmed absent from the tracked tree.
- `project-ed-local-caller/.env` holds `ED_BROKER_URL` and `ED_BROKER_SECRET`
  and is correctly gitignored. Values were not read or echoed.

## What changed this session

Twelve files removed from the repo, committed by Ernie in Terminal and pushed as
`e9934d8`. She had already deleted all of them from the working tree
deliberately; this commit told git about it.

**The citation ring — the reason this was urgent.** Three files each vouched for
the others as current, and none of them mentioned `how-we-build-things.md`:

- `docs/ED_CANON.md` — declared itself "the current main Ed document" and gave a
  ranked authority ladder placing itself second only to a live instruction from
  Ernie. A cold session following the repo's own instructions would bootstrap the
  retired rulebook.
- `docs/ed_standing-authority.md` — "docs/ED_CANON.md remains the current main
  Project Ed source of truth," and ED_CANON pointed straight back at it.
- `docs/build-notes/2026-07-05-doc-homes.md` — named ED_CANON as the main restart
  document, under a heading reading "Current rule."

A grep confirmed the string `how-we-build-things` appeared in exactly two repo
files, both written 2026-08-22 or later. Everything older was a self-consistent
ChatGPT-era world model with no forward pointer out of it.

**Also removed:**

- `docs/daphne campaign.md` — 12KB of "Daphne (she/her)" with no header saying
  Daphne is a character. The project copy `claude/campaign-glimmerhold.md` keeps
  that guard; this copy had it stripped, creating a live path to breaking the one
  hard rule about how Ernie is addressed.
- `docs/git-terminal-commands.md` — first ~60% raw RTF pasted into a `.md`,
  actually a Diane reference doc living in `ed`, carrying `git reset --hard` and
  `git stash` recipes with no guardrail. The one file entirely about running git
  was also the only one omitting the rule that makes running it dangerous.
- `docs/ed_build-log.md`, `docs/ed_feature-requests.md`, `docs/README.md`,
  `README.md`, `build-log/2026-08-07-chatgpt-codex-auth-checkpoint.md` — Ernie's
  call, deleted deliberately.
- `docs/interface/ed-console-v0.html` — the earlier capture surface, superseded
  by the quest board.
- `ed-broker-test.json` — unreferenced anywhere except its own line in
  `.gitignore`, yet still tracked and public, since gitignore does not untrack
  what is already committed. `ed_capture.py` reads the broker URL and secret from
  environment variables, not from this file. Its only value was the placeholder
  string `REPLACE_WITH_LOCAL_SECRET`, so nothing leaked.

**Added this session (uncommitted at time of writing):**

- `.claude/checkpoint-config.md` — matches the shape `diane` and `prngclients`
  already use. Log directory `docs/build-logs/`, filename prefix `ED-`.
- `docs/build-logs/` and this file.

**Removed in a follow-up commit the same session:**

- `artstyle.md` — byte-for-byte identical to the project doc
  `claude/art-style.md`. Two live copies with no canonical one named, while the
  file's own closing line read "This doc is now the only style system. One
  home." The project doc is the home; the repo copy is gone.
- `project-ed-local-caller/ed_caller.rtf` — RTF pasted into a code folder,
  referenced by nothing. `ed_capture.py` does not read it.

## What was NOT changed

- No file in `docs/interface/` was edited. The quest board, `fill_board.py`, and
  the assets are untouched at the versions pushed in `18c65f3`.
- `quest-board.md` at the repo root was left in place. It is the **v1 brief only**
  — it still specifies dailies as "deliberately low-contrast," which V3 overturned
  ("separation is structural, not tonal"), and still asks for a first-draft mockup
  that has been built. The full brief with V2–V5 lives at
  `claude/quest-board-brief.md`. Flagged, not acted on.
- `project-ed-local-caller/docs/README.md` (zero bytes since June) was flagged
  and left alone.
- Aging on the quest board is still not wired. Every `sat` value is 0, so no note
  shows wear. Unchanged from the 2026-08-22 checkpoint and still the highest-value
  open item on the board itself.
- No checkpoint *skill* was created or edited. Skill files are not reachable from
  this session; only the per-repo configs they read.

## Correction to the working model

There are not three checkpoint skills, one per surface. There is **one skill plus
a per-repo `.claude/checkpoint-config.md`.** The config is what varies by project,
not by whether the session runs in Claude Code, Cowork, or claude.ai. `ed` was
missing its config — that was the entire gap.

## Housekeeping outside this repo

`~/Projects` had three stale folders removed: `_client_work_holding` (an older
draft of one client's reports, superseded by the copies in `prngclients`, and
loose client-confidential data sitting outside any repo) and two
`.git_parent_backup*` bare object stores. The device bridge cannot delete, so they
were moved to `~/Projects/_to_delete/` and Ernie emptied it.

Also noted, not acted on: `antihub` is the only repo whose local `main` differs
from its last-known `origin/main`, and it has not fetched since 2026-07-06.

## Guardrails

- Never run git through the desktop/device bridge — it leaves an `index.lock`
  the bridge cannot delete.
- A cloud container cannot push to `ed`; prepare the commit, hand over the
  commands, verify from origin after.
- The quest board is practice-internal and must never be deployed.
- Do not claim code was committed, pushed, deployed, tested, or verified unless
  it actually occurred.
- Local checkout is the working copy, GitHub is the record. Build logs are
  written locally first, then pushed, never edited directly on GitHub.

## Incident: client names committed to this public repo, then removed

**This was Claude's error, introduced by the first draft of this very file.**

The draft recorded the cleanup sweep by quoting the grep pattern used to run it
— a pipe-delimited list of seven client names — and separately named one client
in the housekeeping section. Both were pushed to `ed`, which is public
(confirmed: an anonymous clone succeeds from a container the git proxy refuses
to issue credentials for). Ernie was told to push it.

Caught on the verification pass after `1b412f4`, by the same sweep run against
the fresh clone.

- **Severity:** client *names* only. No financial figures, quotes, or
  diagnostics. Materially smaller than the 2026-08-22 exposure, but it broke the
  one property that made this repo useful — the Map's entry for `ed` read
  "**None** — verified."
- **Fix:** the two offending commits (`83c9b98`, `1b412f4`) were the tip and
  nothing depended on them, so they were squashed back to the last verified
  clean commit `e9934d8` and replaced via
  `git reset --soft` + `git push --force-with-lease`. Verified from a fresh
  clone: both SHAs are unreachable, and a full sweep across all 27 commits in
  history is clean apart from one pre-existing item below.
- **Residue, pre-existing and accepted:** one partner name appears in a list of
  feeder channels in `docs/ed_build-log.md`, in commits from June. That file is
  deleted at the tip. Not financial detail, not from this session; filed
  alongside the `prngclients` / `prngbooks` history items as a someday.
- **Guardrail added** to `.claude/checkpoint-config.md`: a build log about
  client-adjacent work is itself client-adjacent. Sweep the log you just wrote,
  not only the tree it describes, and never paste a client-name search pattern
  into a tracked file.

The general shape is worth keeping: **the artifact that proves cleanliness can
be the thing that breaks it.** Rule 5 says verify from outside — this is the
case where the verification output itself needed verifying.

## Terminal reference written

Ernie asked what commands keep the local folder and GitHub mirrored, and whether
`git status` confirms a push. It does not: it compares the branch to a *cached*
copy of origin, so a rejected push can still read as "up to date." That is the
2026-08-22 failure shape exactly — a local cache being mistaken for the remote.

- `diane/docs/build-logs/terminal-and-git-glossary.md` gained a workflow section
  at the end, plus a missing `git rm <file>` entry inserted in alphabetical
  order per that file's stated convention. **Note the conflict that was
  resolved rather than papered over:** the glossary's `git add <file>` entry
  explicitly warns against `git add -A` because the Diane checkout carries stray
  files. The new section keeps explicit naming as the default and scopes
  `git add -A` to checkouts where `git status` has just been read and is clean.
  A section arguing with its own file 300 lines up is the failure this session
  spent its morning removing.
- `ed/docs/build-logs/README.md` — what the folder is, the naming convention,
  the push loop, the `git status` caveat, and a pointer to the glossary as the
  full reference. Deliberately a pointer and not a copy.

## Next step

Wire aging on the quest board. Every `sat` is 0, so no note shows wear, which
means the board cannot show drift — and catching drift is most of why it exists.
`date_updated` drives it; the ClickUp MCP's task filter omits that field but a
per-task fetch returns it. An MCP gap, not a design gap.

Also still open, both flagged this session and deliberately untouched:
`quest-board.md` at the repo root is the v1 brief only and contradicts V3 on
dailies; `antihub` is the one repo whose local `main` differs from its
last-known `origin/main`, unfetched since 2026-07-06.
