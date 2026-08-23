# Interfaces

Surfaces Ernie actually looks at. **Practice-internal — never deploy any of these
to a web host.** They carry client names; see Part 1 of `how-we-build-things.md`
in the Project Ed docs.

| File | What | State |
|---|---|---|
| `ed-console-v0.html` | Ed Console v0.1 — capture surface. Panels, columns, activity log, dropzone. | Earlier concept, 2026-07 |
| `quest-board-v1.html` | The quest board — status surface. Main quest, five quest-log panels, shield, Listener, bell. | Current, 2026-08-22 |

These are siblings, not replacements: the console is about *getting things in*,
the board is about *seeing where things stand*. Whether they converge is open.

## quest-board-v1.html

Open it directly in a browser — no build step, no server, no dependencies.
Images live in `assets/`. Google Fonts load when online and fall back cleanly
when not.

**The seam.** All quest text is placeholder, held in one `BOARD` object at the
top of the `<script>`. That object is what ClickUp and Airtable fill in; nothing
else on the page changes when they do.

| Field | Notes |
|---|---|
| `mainQuest` | Title and `daysRemaining`. The only number on the board that counts anything. |
| `ed` | One line, first person, one instruction. Never a list. |
| `shield` | `active` + `daysLeft`. Earned quiet, not a second clock. |
| `listener` | `waiting` + `line`. Lit means a record is waiting. |
| `quests[]` | `type` (main / major / side / daily / rep), `text`, optional `status`, optional `thread` (major only), and `sat`. |

`sat` is how long a quest has sat there. It drives wear only — **never printed,
never counted, never turned into a date.**

`MAJOR_SHOWN` caps how many projects show. The overflow link carries no number,
deliberately.

**The bell** is `<a href="claude://">` — a bare deep link, verified to bring the
Claude desktop app forward *without* touching the open conversation. No
`claude://.../new` link appears anywhere on this page: the app has one window, so
a `/new` link would end whatever conversation Ernie was in, and nothing on the
board gets to make that call. The link beneath it only touches the clipboard.

Design rules this page is built to, all in `quest-board-brief.md`: nothing marked
overdue, no counters or progress bars, no failure state, one voice, one ask,
aging as the only signal that time has passed, and separation carried by
structure rather than by dimming anything out.
