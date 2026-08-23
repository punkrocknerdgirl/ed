# 2026-08-23 — ED — Board rebuilt on tags, rail reworked, Listener wired

## Purpose

Rebuild the quest board so ClickUp **tags** decide what renders, replacing a
structure that read lists and folders — most of which no longer exist. Then
rework the rail layout across several passes, and wire the Listener crystal to
something real for the first time.

Third session of the day. Follows the Abby decommission checkpoint.

## Verified state

**Verified — checked directly this session:**

- ClickUp now carries the taxonomy as tags: **1 `campaign`, 11 `main`, 4 `life`,
  15 `side`** — 31 tagged tasks spread across **both spaces and 8 lists**. The
  tag works as the seam regardless of where a task lives; confirmed by pulling
  the same set filtered on tags alone.
- `PRNG Creative` holds **no folders at all** any more, only two lists. This is
  what killed the old `major` column, which read folders.
- The board renders **campaign 1 / main 11 / life 4 / side 15**, verified in a
  headless browser at 1600px and 1100px. No JS errors, no horizontal overflow at
  either width.
- **Aging is intact.** A positive control with hand-backdated stamps hits
  wear 1.0 / 2.0 / 3.0 exactly on each column's thresholds. Live data reads 0
  everywhere because the bulk re-tag touched every task today — correct, not
  broken.
- **The Listener lamp is wired and passes three controls**: negative (empty
  Inbox → dark), positive (a real night's record → lit), and a **decoy** (an
  open Inbox task that is not a record → stays dark). The decoy is what proves
  it means "a record is waiting" and not "something is in your inbox."
- Lit vs dark measured on the crystal image itself: **3.08x mean, 2.98x in the
  highlights.**
- `Drop it` produces the correct clipboard payload with the date stamped from
  the browser, clears the box, updates the button, and rings `claude://`.
  Tested end to end with a real clipboard read.
- Ed's scroll **removes itself** when his line is empty — no empty bubble.
- Origin tip is `e63fe27`, read from a fresh anonymous clone in a cloud
  container. Local is **not behind**.
- A `.env` in the Drive copy of the retired local runner was **trashed**, with
  permissions confirmed owner-only first and a control search proving the
  deletion check worked.

**Reported, not independently verified:**

- **Nothing in this session was committed or pushed.** All changes are saved to
  the local working copy only.
- The Listener **agent** is still unverified live. The lamp reads the Inbox
  correctly; nothing proves the agent is running and carving records.
- The `life` aging thresholds (3 / 7 / 14 days) are Claude's pick and were
  **never tuned with Ernie**. Marked PROVISIONAL in the source.
- Rendering was verified headless in a Linux container, not in Ernie's own
  browser.

## What changed this session

**`fill_board.py` — rebuilt around tags**

- Reads a flat `tasks` list and sorts each into exactly one column by tag,
  resolved `campaign > main > life > side`. Untagged tasks never render, so the
  board cannot show something that was not deliberately put on it.
- **The live gate was inverted.** Was `LIVE = {in progress, next, recurring}`;
  is now *everything tagged except* `done / closed / complete / parked`. The old
  rule was written when lists carried the taxonomy — run the tags through it and
  **14 of 15 side quests and 3 urgent main quests vanish.**
- `campaign` drives the big parchment at the top and is not a note.
- The Listener lamp is computed from open Inbox tasks instead of hardcoded.
- Retired: `major` (read folders), `daily` and `rep` (needed tags that never
  existed; `rep`'s fallback to the `recurring` *status* would have
  double-rendered six `main` tasks).

**`clickup_dump.json` — new flat shape**, one `tasks` array plus `inbox`.

**Layout, four passes.** Landed on: full-width sign; campaign below it spanning
the left block only; main beside side; life spanning under both; rail carrying
Vault → Listener → Ed and his bell. Default rail widened **272 → 340px** with
the narrower breakpoints moved to match.

**The Vault now targets the Journal doc.** `Drop it` copies an append-only
instruction naming the doc, with today's date stamped in Ernie's browser, and
rings the bell. The doc is named, never ID'd, because this file is public.

**Ed is silent.** `BOARD.ed` is `""` and the scroll removes itself. `ed_line()`
is kept, not deleted — one word restores him.

**The placeholder `BOARD` literal was rebuilt** with synthetic entries carrying
no client name, replacing entries that named real projects with invented
statuses.

## What was NOT changed

- **Nothing was committed or pushed.** Commands are handed over below.
- **`main` and `side` aging thresholds** — carried forward untouched.
- **The Listener agent's instructions.** Its spec still describes the old job:
  carve one triage task and go silent. Ernie has since asked for something
  different. Deliberately left for the next session.
- **`ed_line()`** — preserved rather than deleted.
- **No credential was added anywhere.** Weighed and rejected: making the Vault
  write directly needs a token, and the only place to put one is inside a file
  designed to open from anywhere — the exact shape of the credential that sat in
  a public repo for two months. The board stays dumb on purpose.
- **The `life` column's existence** was Claude's reading of "under main" and was
  confirmed by Ernie mid-flight, not assumed silently.

## Guardrails

**New, learned this session:**

- **A filter written for one taxonomy silently strangles the next.** The live
  gate was correct under lists and near-fatal under tags, with no error — just a
  nearly empty column. **When the thing that decides membership changes, re-derive
  every filter that ran on the old one.** The tag now says whether something
  belongs on the board; the status only says whether it has been shelved.
- **A new note type inherits the wrong styling in silence.** `.note.life` was
  missing from the badge selector and fell through to a rule built for dark
  notes that no longer exist — a grey box with effectively invisible text on
  cream. It rendered; it just could not be read. **Add a new type to every
  type-keyed selector, or it inherits whatever the base rule was built for.**
- **A measuring probe needs its own control.** The lamp measured 1.30x and
  "too subtle" — because the probe averaged the whole panel, most of which is
  background that does not change. Measured on the crystal itself: 3.08x. Second
  time this exact mistake has been made; the first was a pixel probe landing on
  a glyph.
- **`clickup_search` returns `dateUpdated` in bulk.** This retires the documented
  per-task-fetch workaround — **31 stamps in one call instead of 31 calls.**
  `clickup_filter_tasks` still does not return the field.
- **A bulk re-tag resets `date_updated` on every task it touches**, so the wear
  signal reads zero across the whole board afterwards and rebuilds from that
  moment. Correct behaviour, alarming on sight.
- **A control that cannot fail is not a control**, applied to a *lamp*: a
  hardcoded `waiting: False` read as information for as long as it existed. **An
  indicator that cannot turn on is worse than no indicator.**
- **A client-name sweep fails in BOTH directions, and today it did both.**
  Written without `-i` it reported clean on a file it had not really searched —
  the exact bug this project already had a rule about, reproduced within an hour
  of reading that rule. Written with `-i` but no word boundaries it then flagged
  a hit that turned out to be `ArrowRight` matching a client surname as a
  substring. **A sweep needs `-i`, word boundaries, and a human read of every
  hit** — plus both controls: a seeded positive that must be found, and a decoy
  that must be ignored. One control only proves one direction.
- **A CSS default cannot beat a saved `localStorage` value.** Changing the rail
  default does nothing for anyone who has dragged the grip; the saved width
  wins until the grip is double-clicked. Say so when changing a default that
  has a remembered override.

**Carried forward from the previous checkpoint:**

- A backup file made beside a gitignored file is **not** itself gitignored. Name
  files explicitly on `git add` in this repo, whatever the README says.
- A zero result is not evidence until a control proves the search works.
- Distinguish an operational reference from an inert mention.
- The Claude Project docs and this repo's build logs are two different record
  sets. Always say which one a claim comes from, and check both.
- Project doc timestamps come back in **UTC** — convert before saying when.
- A skill with more than one file cannot be updated by pasting `SKILL.md`.
- All skills live account-wide at `~/.claude/skills/`.
- A skill's description is a trigger, not documentation.
- Verified and reported-but-unverified are different categories, always stated
  in plain words.
- **Never run git through the device bridge.**
- A cloud container cannot push to `ed` — prepare, hand over, verify after.
- Client data and credentials never reach a public repo. **A build log about
  client-adjacent work is itself client-adjacent: sweep the log, not only the
  tree it describes.**
- Write the log for someone with no memory of the session.

## Next step

**Rewrite the Listener agent's instructions to match the job Ernie actually
described**: read the Journal doc, parse it, and go over the items *with* her —
rather than carving one triage task and going silent. Everything else queued
behind it (a `Listen` button, a 12-hour autorun) is built off that spec, and
building either first would encode the wrong job.

Both are credential-free: the button is the same copy-and-ring-the-bell trick
the Vault now uses, and the autorun is a scheduled task whose fresh session
already has the ClickUp MCP.
