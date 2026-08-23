#!/usr/bin/env python3
"""
fill_board.py -- the seam, filled. TAG-DRIVEN as of 2026-08-23.

Reads a ClickUp dump and writes board-data.js, which defines window.BOARD_DATA.
quest-board-v1.html loads that file if it is there, and falls back to its own
placeholder BOARD if it is not. Nothing else on the page changes.

WHAT DECIDES WHERE A TASK GOES (rebuilt with Ernie, 2026-08-23)

  THE TAG. Not the list, not the folder, not the space. A task tagged `main`
  renders as a main quest whether it lives in a client list, the Quest Log, or
  anywhere else that exists later. This replaces the old structure, which read
  ClickUp FOLDERS in PRNG Creative -- folders that no longer exist.

    campaign   ONE quest, the standing one, rendered as the big parchment at
               the top. Not a note; it has no column.
    main       Main Quests. The work that pays.
    life       Life Quests. Personal. Sits directly under main, deliberately
               its own panel rather than mixed in -- Ernie tagged them apart,
               so the board keeps them apart.
    side       Side Quests.

  A task carrying more than one of these lands in exactly one column, resolved
  campaign > main > life > side. Untagged tasks do not render at all -- which means the
  board can never show something Ernie did not deliberately put on it.

  RETIRED THIS REBUILD: `major` (read folders, which are gone), `daily` and
  `rep` (needed tags that never existed, and `rep`'s fallback to the `recurring`
  STATUS double-rendered six main-tagged tasks).

WHAT EARNS A SPOT (changed 2026-08-23 -- read this before "fixing" it)

  Everything tagged, unless it has been PUT AWAY: done, closed, complete,
  parked. `pending` and `waiting` are ordinary live work and DO render.

  The old rule was the reverse -- LIVE = {in progress, next, recurring} -- and it
  was written when lists carried the taxonomy. Run the tags through it and 14 of
  15 side quests vanish, along with three urgent main quests. The tag now says
  whether a thing belongs on the board; the status only says whether it has been
  shelved.

WHAT THE DUMP MUST CARRY

  A flat `tasks` list. Every task needs `date_updated` -- ClickUp's
  epoch-millisecond last-touched stamp. It is what aging runs on, and WITHOUT IT
  EVERY NOTE RENDERS BRAND NEW.

  It cannot come from the same call as the rest. `clickup_filter_tasks` does not
  return the field at all -- verified 2026-08-23, not assumed -- while
  `clickup_get_task` on the very same task returns it. So building the dump costs
  one extra per-task fetch for anything that will render. An MCP gap, not a
  design gap.

  A task with no `date_updated` ages to nothing rather than guessing.
"""
import json, html, sys, os, base64, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DUMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "clickup_dump.json")
OUT  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "board-data.js")

d = json.load(open(DUMP))
TODAY = datetime.date.fromisoformat(d["fetched"])

PRIO = {"urgent": 0, "high": 1, "normal": 2, "low": 3, None: 4}
SHELVED = {"done", "closed", "complete", "parked"}

# Columns, in resolution order. A task takes the first one it carries.
COLUMNS = ["campaign", "main", "life", "side"]

# -- Aging -- the only signal this board may give that time has passed --------
# Rule 5 forbids overdue, red, and counting; the brief allows exactly one thing:
# "an old quest just looks old." It renders as wear -- yellowing and a lifting
# corner -- and is never printed, never counted, never turned back into a date.
#
# The clock runs PER COLUMN. Ernie's thresholds from 2026-08-23, carried forward
# unchanged through the tag rebuild: a flat rate inverts the signal, because the
# same four days means something different on a payroll run than on a blog post.
#
# Days untouched at which a note reaches wear level 1 / 2 / 3.
AGE_STEPS = {
    "main": (2, 5, 10),    # the work that pays. Sitting is the worst kind.
    "life": (3, 7, 14),    # PROVISIONAL -- Claude's pick, never tuned with
                           # Ernie. An errand rots faster than a blog post but
                           # slower than a payroll run. Change it on sight.
    "side": (7, 14, 30),
}

def sat(kind, updated_ms):
    """Wear as a CONTINUOUS number 0-3, not three steps. Piecewise-linear
    through the column's own thresholds, so they still mean exactly what they
    meant -- the value hits 1.0, 2.0 and 3.0 on the nose at a, b and c -- while
    a note at nine days no longer renders identical to one at fourteen.

    Unknown or missing stamp ages to 0: a note never invents age it cannot show
    its work for."""
    if not updated_ms or kind not in AGE_STEPS:
        return 0
    days = (TODAY - datetime.date.fromtimestamp(int(updated_ms) / 1000)).days
    a, b, c = AGE_STEPS[kind]
    if days <= 0:  return 0
    if days < a:   return round(days / a, 2)
    if days < b:   return round(1 + (days - a) / (b - a), 2)
    if days < c:   return round(2 + (days - b) / (c - b), 2)
    return 3

esc = lambda s: html.escape(s, quote=False)
nice = lambda s: " ".join(w.capitalize() for w in s.split())

def due_key(t):
    dd = t.get("due_date")
    return (0, int(dd)) if dd else (1, 0)

def due_date(t):
    return datetime.date.fromtimestamp(int(t["due_date"]) / 1000) if t.get("due_date") else None

# -- Sort every task into exactly one column by its tag -----------------------
buckets = {c: [] for c in COLUMNS}
skipped_shelved = 0
skipped_untagged = 0

for t in d["tasks"]:
    if (t.get("status") or "").lower() in SHELVED:
        skipped_shelved += 1
        continue
    tags = [x.lower() for x in t.get("tags", [])]
    for c in COLUMNS:
        if c in tags:
            buckets[c].append(t)
            break
    else:
        skipped_untagged += 1

# Soonest due first, then priority. A task with no due date sorts after ones
# that have them -- a date is a commitment, a priority is only an opinion.
for c in COLUMNS:
    buckets[c].sort(key=lambda t: (due_key(t), PRIO.get(t.get("priority"), 4)))

def note(t, kind):
    return {"type": kind,
            "text": esc(t["name"]),
            "status": nice(t.get("status") or ""),
            "sat": sat(kind, t.get("date_updated"))}

main_q = [note(t, "main") for t in buckets["main"]]
life_q = [note(t, "life") for t in buckets["life"]]
side_q = [note(t, "side") for t in buckets["side"]]

# -- The campaign quest -- the standing one, top of the board -----------------
# It is not a note and has no column. If nothing is tagged `campaign` the board
# says so plainly rather than inventing one or leaving a blank parchment.
camp = buckets["campaign"][0] if buckets["campaign"] else None
camp_title = esc(camp["name"]) if camp else "No campaign set.\nTag one in ClickUp."

# -- The parts ClickUp does not own -------------------------------------------
y, m = TODAY.year, TODAY.month
target = datetime.date(y, m, 15) if TODAY.day <= 15 else \
         datetime.date(y + (m == 12), 1 if m == 12 else m + 1, 15)
days_left = (target - TODAY).days

# Ed points at ONE thing: the soonest main quest. He does not repeat the
# campaign beside him, and he NEVER carries a count -- rule 7: a number on the
# board is a scoreboard, and a scoreboard is a stick.
step = buckets["main"][0] if buckets["main"] else None

def ed_line(step, days_left):
    if not step:
        return "Board's clear. Pick the thing you keep walking past."
    dd = due_date(step)
    if dd and dd < TODAY:
        return "That one's already late. Do it before you open anything else."
    if dd and dd == TODAY:
        return "That's today's. Everything else can wait an hour."
    return "%d days to the 15th. One thing at a time." % days_left

# -- The Listener -- a one-bit lamp, and now actually wired -------------------
# It is NOT a display. It answers one question: is there a night's record sitting
# in Admin > Inbox that Ernie has not triaged yet. Lit = yes, dark = no.
#
# Until 2026-08-23 this was hardcoded False, so it said "nothing waiting"
# forever whether or not anything was -- a lamp with the wire cut, and worse than
# no lamp, because a lamp that cannot turn on still reads as information.
#
# It matches on the TITLE the Listener agent is specified to carve, not on "any
# open Inbox task" -- the Inbox holds other things, and lighting the crystal for
# those would make it mean something other than what it says.
TRIAGE = "triage the night's record"
waiting = [t for t in d.get("inbox", [])
           if (t.get("status") or "").lower() not in SHELVED
           and t.get("name", "").strip().lower().startswith(TRIAGE)]

# No count in the line. Rule 7: a number on the board is a scoreboard, and a
# scoreboard is a stick. The crystal says whether, never how many.
BOARD = {
    "mainQuest": {"title": camp_title, "daysRemaining": days_left},
    # Ed is QUIET, Ernie's call 2026-08-23. The board carries the information
    # now, so a line from him was a second voice saying what the notes already
    # say. ed_line() is kept, not deleted -- the capability is still here and
    # this is a one-word change back. Return "" and the scroll hides itself.
    "ed": "",
    "listener": {"waiting": bool(waiting),
                 "line": "A record is waiting to be triaged." if waiting
                         else "Nothing waiting to be triaged."},
    "quests": main_q + life_q + side_q,
}

with open(OUT, "w") as f:
    f.write("/* Generated by fill_board.py from ClickUp -- %s. Do not edit by hand.\n"
            "   Practice-internal: carries client names. Never commit, never deploy. */\n"
            % d["fetched"])
    f.write("window.BOARD_DATA = " + json.dumps(BOARD, indent=2, ensure_ascii=False) + ";\n")

# -- Bake a standalone copy ---------------------------------------------------
# quest-board-v1.html is the SOURCE: it points at assets/ and board-data.js, which
# keeps the repo clean and diffable. But a file that only works from one folder
# gets opened from Downloads and looks broken. So we also emit one self-contained
# file with the images and the data inlined -- that is the one to actually open,
# and it can live anywhere. It carries client names, so it is gitignored too.
TEMPLATE   = os.path.join(HERE, "quest-board-v1.html")
STANDALONE = os.path.join(HERE, "quest-board-live.html")

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp"}

def inline_asset(m):
    rel = m.group(1)
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        print("  ! missing asset, left as a link: %s" % rel)
        return m.group(0)
    ext = os.path.splitext(path)[1].lower()
    blob = base64.b64encode(open(path, "rb").read()).decode()
    return 'src="data:%s;base64,%s"' % (MIME.get(ext, "application/octet-stream"), blob)

if os.path.exists(TEMPLATE):
    page = open(TEMPLATE).read()
    page = page.replace('<script src="board-data.js"></script>',
                        "<script>window.BOARD_DATA = "
                        + json.dumps(BOARD, ensure_ascii=False) + ";</script>", 1)
    page = re.sub(r'src="(assets/[^"]+)"', inline_asset, page)
    open(STANDALONE, "w").write(page)
    print("wrote %s  (%.0f KB, opens from anywhere)"
          % (STANDALONE, os.path.getsize(STANDALONE) / 1024))

print("wrote %s" % OUT)
print("  campaign  %s" % (esc(camp["name"]) if camp else "-- none tagged --"))
print("  main    %2d" % len(main_q))
print("  life    %2d" % len(life_q))
print("  side    %2d" % len(side_q))
print("  listener %s" % ("LIT -- record waiting" if waiting else "dark -- nothing waiting"))
print("  shelved %2d skipped (done/closed/parked)" % skipped_shelved)
print("  untagged%2d skipped" % skipped_untagged)
