# 2026-08-23 — ED — Project Abby decommissioned, board rebuilt on live data

## Purpose

Find and remove everything that could still hand work to Project Abby, a project
that never got off the ground, and then rebuild the quest board so it stops
rendering a workspace that no longer exists.

The session opened by asking what the latest build docs said. That question
turned out to have two different answers, which is finding one.

## Verified state

**Verified — checked directly this session:**

- `origin/main` is **`5f5bff4`**. Pushed by Ernie in Terminal; receipt read
  `9f3607a..5f5bff4  main -> main`. Confirmed from a **fresh anonymous clone**
  in a cloud container, not from local cache.
- At that tip: no `Kwisatz`, no `Abby`, no `High Life`. A positive control
  (a term known present) returned hits in the same run, so the zeros mean
  something.
- `board-data.js`, `clickup_dump.json`, `quest-board-live.html` are **not
  tracked** at `5f5bff4`. Confirmed against the fresh clone.
- ClickUp holds **no** Abby folder, list, task, or doc. Search returned 0 for
  `Abby`, `Agent Directory`, and `PRNG HQ`; a control search returned 3 hits in
  the same minute. The whole PRNG HQ doc is gone, Agent Directory included.
- `~/Projects` contains no file or folder named for Abby, and no reference to
  the retired project alias or its ClickUp list ID.
- Full-history sweeps of every **public** repo (31, 32, 12, 12 commits): two
  files in `ed` history mention Abby, both deleted at the tip; one line at the
  tip of `prngcreative` names it as a June sibling folder. No client data, no
  credentials, in any of it.
- The board regenerated from a live pull: main 1, major 2, side 6, daily 3,
  rep 1. Aging renders a real spread (0.14 through 2.12), which is the first
  time wear has been seen varying on genuinely current data.

**Reported, not independently verified:**

- That the deleted ClickUp folders were removed deliberately. Ernie said so
  mid-session; nothing was checked against an audit trail.
- The contents of `Claude_data.zip` in Google Drive. It matched a full-text
  search for the retired project name; the archive was never opened.
- Private repo history (`diane`, `prngclients`, `prngbooks`). Anonymous clone is
  refused and git may not be run through the device bridge, so **their working
  trees were swept and are clean, but their history was not swept at all.**

## What changed this session

**Decommissioned — the things that could actually dispatch to the project:**

- Google Drive `workspaces.json` — carried an alias map pointing the retired
  project name at a ClickUp list ID. **Trashed** (recoverable 30 days).
- Google Drive `runner.py` — a CLI whose `--project` flag accepted that alias.
  **Trashed.**
- Both belonged to the **retired ed local runner**, whose broker was archived
  earlier the same day. Neither file exists anywhere in `~/Projects`; nothing on
  disk read them. They were orphans describing a dead system pointed at a
  workspace structure that no longer exists.

**Removed from the repo:**

- The placeholder `major` entry naming a decommissioned project in
  `docs/interface/quest-board-v1.html`. It never rendered —
  `Object.assign(BOARD, window.BOARD_DATA)` replaces the whole quest list — but
  it sat in a tracked file in a public repo asserting a status for a real
  project. Committed as `5f5bff4`, pushed, verified from outside.

**Rebuilt:**

- `clickup_dump.json` regenerated from a live ClickUp pull, then `fill_board.py`
  run to emit `board-data.js` and the baked `quest-board-live.html`.
- The dump now reflects a workspace with **three** folders in PRNG Creative,
  down from six. Three project folders and two lists were deleted by Ernie
  during the session.

**Housekeeping:**

- `~/Projects/diane/skills/` — held nothing but a `.DS_Store`. Moved to
  `~/Projects/_to_delete/diane-skills/` and emptied by Ernie. This closes the
  open item from the previous checkpoint, which flagged it as unexamined.

## What was NOT changed

- **`ed` git history.** Two deleted files still mention the retired project in
  31 commits of a public repo. Removing them means force-pushing over the whole
  history for prose describing an internal agent role — no client data, no
  credential. The history purge was investigated and deliberately closed earlier
  the same day; **this was not sufficient reason to reopen it.**
- **The `prngcreative` tip line.** It is a dated June build log describing what
  the folder tree looked like in June, when that was true. Editing it would not
  be a fix, it would be falsifying a record.
- **The remaining three placeholder `major` entries** in the board template.
  They name real projects and assert invented text and statuses. Flagged, left
  alone — see the bugs log.
- **`STARTER_DAILIES`.** Still three hardcoded placeholders. No `daily` tag
  exists in ClickUp, so the fallback still stands. Unchanged and still open.
- **`.env` in Google Drive** from the retired local runner. Owner-only, not
  shared, and the secret it holds was already retired when the broker deployment
  was archived. Surfaced, deliberately not acted on this session.

## Guardrails

**New, learned this session:**

- **A backup file made beside a gitignored file is not itself gitignored.**
  A `clickup_dump.json.bak` was created next to the gitignored dump in this
  **public** repo. `.gitignore` covers the dump, not the `.bak`, so it showed up
  as untracked-and-unignored carrying client names. The README's push loop
  recommends `git add -A` on the grounds that gitignore covers the generated
  files — that assumption was one stray suffix from being false. **Name files
  explicitly on `git add` in this repo, whatever the README says.** The `.bak`
  was removed before staging.
- **A zero result is not evidence until a control proves the search works.**
  Used deliberately this session: every sweep ran a positive control (a term
  known to be present) alongside it. The ClickUp "Abby is gone" finding is only
  trustworthy because a control search returned hits in the same minute.
- **Distinguish an operational reference from an inert mention.** When retiring a
  project, what matters is what can *dispatch* to it — alias maps, config, CLI
  flags, folder IDs. Prose, history and dated logs merely *name* it and cannot
  commingle anything. Conflating the two turns a ten-minute cleanup into a
  history rewrite.
- **The Claude Project docs and this repo's build logs are two different record
  sets.** Checkpoint summaries live in the Project; build logs live in
  `docs/build-logs/`. This session opened by reading only the Project and
  reporting the "latest" state while two newer logs sat on disk unread.
  **Always say which record set a claim comes from, and check both.**
- **Project doc timestamps come back in UTC.** A doc stamped `19:50` was
  reported as "yesterday evening" when it was in fact 2:50pm the same afternoon.
  Convert to America/Chicago before saying a word about when something happened.

**Carried forward from the previous checkpoint:**

- A skill with more than one file cannot be updated by pasting `SKILL.md` — zip
  the folder and upload that.
- All skills live account-wide at `~/.claude/skills/`. No repo-local skill
  folders.
- There is no single folder covering all three surfaces; the disk is the master
  and the uploaded copy goes stale silently.
- A skill's description is a trigger, not documentation.
- Verified and reported-but-unverified are different categories, always stated
  in plain words.
- Never run git through the device bridge.
- A cloud container cannot push to `ed` — prepare, hand over, verify after.
- Client data and credentials never reach a public repo or an unnecessary chat.
  A build log about client-adjacent work is itself client-adjacent: sweep the
  log, not only the tree it describes.
- Write the log for someone with no memory of the session.

## Next step

**Trash the `.env` in Google Drive** left behind by the retired ed local runner.
One action. It is owner-only and the secret inside was retired when the broker
deployment was archived, so this is hygiene rather than exposure — but it is a
credential file sitting outside the gitignored home it was designed to live in,
and the lesson from earlier the same day was that the file nobody thinks of as
code is the one that leaks.

Immediately behind it, and the larger of the two: **Project Ed no longer appears
on its own board.** See the bugs log.
