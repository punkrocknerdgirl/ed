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
    daily      Dailies. NOT a tag -- see below.

  DAILIES COME FROM THE STATUS, NOT A TAG (Ernie, 2026-08-24). Any tagged task
  whose ClickUp STATUS is `recurring` moves to Dailies instead of the column its
  tag names. It MOVES, it does not duplicate -- status is resolved before tag, so
  a `main` + `recurring` task appears once, in Dailies.

  This is the same wiring that misfired in the 2026-08-23 rebuild, and the
  difference is the word INSTEAD. Back then `rep` fell back to the `recurring`
  status while its tag ALSO placed it, so six tasks rendered twice. Resolve
  status first and that cannot happen. If Dailies is ever wrong, check that
  ordering before anything else.

  A task carrying more than one tag lands in exactly one column, resolved
  campaign > (recurring -> daily) > main > life > side. Untagged tasks do not
  render at all -- the board can never show something Ernie did not deliberately
  put on it.

  `life` is retained but EMPTY as of 2026-08-24 -- Ernie retagged those to side.
  It costs nothing to keep and its panel hides itself when empty, so re-tagging
  one `life` brings the column straight back.

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

THE SEVEN-DAY WINDOW (Ernie, 2026-08-24)

  The board answers exactly one question: WHAT DOES ERNIE NEED TO KNOW RIGHT NOW.
  So it renders only what is due inside the next seven days, plus anything
  already past due -- which still simply appears, never flagged.

  A TASK WITH NO DUE DATE DOES NOT RENDER. Ernie's call, and it is not an
  oversight to be "fixed" later: an undated task is ClickUp's problem, not this
  board's. If it matters this week it gets a date in ClickUp.

AGING IS GONE (Ernie, 2026-08-24)

  Wear, `sat`, per-column thresholds and the `date_updated` fetch are all
  removed. Aging entered as a CONSTRAINT in the v1 brief -- "an old quest just
  looks old ... that is the only aging signal permitted" -- a ceiling on what the
  renderer was allowed to do INSTEAD of overdue flags. It was later written up as
  the board's purpose. It never was. Do not rebuild it without Ernie saying so.

  Brightness now means URGENT, not old. It reads `priority` straight from
  ClickUp.

WHAT THE DUMP MUST CARRY

  A flat `tasks` list. Each task needs: `name`, `status`, `status_color`,
  `tags`, `due_date` (epoch ms), `priority`.

  `status_color` is ClickUp's own hex for that status, so the board matches what
  Ernie already sees in ClickUp instead of inventing a second palette.

  `date_updated` is no longer read. Nothing here needs a per-task fetch.
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

# Statuses that mean "this comes round again" and belong in Dailies. Ernie's
# call 2026-08-24: use the status she is already setting rather than making her
# maintain a second tag for the same fact.
RECURRING = {"recurring"}

# -- The window -- how far ahead the board looks ------------------------------
# Seven days. Anything dated further out is ClickUp's business, not the board's.
# Overdue is NOT excluded: it is still today's problem, and rule 1 says it simply
# appears rather than being marked.
WINDOW_DAYS = 7

esc = lambda s: html.escape(s, quote=False)
nice = lambda s: " ".join(w.capitalize() for w in s.split())

def due_key(t):
    dd = t.get("due_date")
    return (0, int(dd)) if dd else (1, 0)

def due_date(t):
    return datetime.date.fromtimestamp(int(t["due_date"]) / 1000) if t.get("due_date") else None

# -- Sort every task into exactly one column by its tag -----------------------
buckets = {c: [] for c in COLUMNS + ["daily"]}
skipped_shelved = 0
skipped_untagged = 0

HORIZON = TODAY + datetime.timedelta(days=WINDOW_DAYS)
skipped_undated = 0
skipped_far = 0

for t in d["tasks"]:
    if (t.get("status") or "").lower() in SHELVED:
        skipped_shelved += 1
        continue
    tags = [x.lower() for x in t.get("tags", [])]
    # THE CAMPAIGN IS EXEMPT from the window. Brief rule 1: it is "pinned at the
    # top, always present, never scrolls away." A standing quest that vanishes
    # because it is dated eight days out is the one thing this board may not do.
    if "campaign" not in tags:
        # No date, no note. An undated task is ClickUp's problem.
        dd = due_date(t)
        if dd is None:
            skipped_undated += 1
            continue
        # Past due still renders -- exactly what she needs to know right now.
        if dd > HORIZON:
            skipped_far += 1
            continue
    # Resolution order matters and is the whole reason this does not double-render.
    # 1. campaign wins outright -- it is the standing quest, recurring or not.
    if "campaign" in tags:
        buckets["campaign"].append(t)
        continue
    # 2. a recurring STATUS moves the task to Dailies, instead of its tag column.
    #    It must still carry a board tag, or it was never meant to be here.
    if (t.get("status") or "").lower() in RECURRING and any(c in tags for c in COLUMNS):
        buckets["daily"].append(t)
        continue
    # 3. otherwise the tag decides.
    for c in COLUMNS:
        if c in tags:
            buckets[c].append(t)
            break
    else:
        skipped_untagged += 1

# Soonest due first, then priority. A task with no due date sorts after ones
# that have them -- a date is a commitment, a priority is only an opinion.
for c in buckets:
    buckets[c].sort(key=lambda t: (due_key(t), PRIO.get(t.get("priority"), 4)))

# A note now carries: what it is, what it says, when it is due, what colour
# ClickUp paints its status, and whether it is urgent.
#
#   due          a short human string. Inside a seven-day window the weekday is
#                what actually orients you, so "Wed 26" beats "2026-08-26".
#   statusColor  ClickUp's own hex. The board does not invent a palette.
#   urgent       priority == urgent. This is the ONLY thing brightness means.
def due_label(dd):
    delta = (dd - TODAY).days
    if delta == 0:  return "Today"
    if delta == 1:  return "Tomorrow"
    if delta == -1: return "Yesterday"
    return dd.strftime("%a %-d %b")

def note(t, kind):
    dd = due_date(t)
    return {"type": kind,
            "text": esc(t["name"]),
            "status": nice(t.get("status") or ""),
            "statusColor": t.get("status_color") or "",
            "due": due_label(dd) if dd else "",
            "urgent": (t.get("priority") or "").lower() == "urgent"}

main_q = [note(t, "main") for t in buckets["main"]]
life_q = [note(t, "life") for t in buckets["life"]]
side_q = [note(t, "side") for t in buckets["side"]]
daily_q = [note(t, "daily") for t in buckets["daily"]]

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
    "quests": main_q + life_q + side_q + daily_q,
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
print("  daily   %2d  (status recurring)" % len(daily_q))
print("  urgent  %2d" % sum(1 for q in (main_q + life_q + side_q + daily_q) if q["urgent"]))
print("  window   next %d days (through %s)" % (WINDOW_DAYS, HORIZON))
print("  shelved %2d skipped (done/closed/parked)" % skipped_shelved)
print("  undated %2d skipped (no due date in ClickUp)" % skipped_undated)
print("  beyond  %2d skipped (due after the window)" % skipped_far)
print("  untagged%2d skipped" % skipped_untagged)
