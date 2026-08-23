#!/usr/bin/env python3
"""
fill_board.py — the seam, filled.

Reads a ClickUp dump and writes board-data.js, which defines window.BOARD_DATA.
quest-board-v1.html loads that file if it is there, and falls back to its own
placeholder BOARD if it is not. Nothing else on the page changes.

WHAT EACH COLUMN ANSWERS (decided with Ernie, 2026-08-23)

  Main quest line   The quest itself never changes -- reports out by the 15th,
                    and she knows it by heart. So the column does not list the
                    steps. It shows ONE note: the next immediate thing that
                    moves it forward.
  Major quest lines One note per project: its next available quest, plus a
                    tally of how far that line has come. A project with nothing
                    live still shows, because a stalled build is exactly the
                    drift this column exists to catch.
  Side quests       Admin, live only.
  Dailies           Admin tagged `daily` -- NO SUCH TAG EXISTS IN CLICKUP YET,
  Repeatables       Admin tagged `repeat` -- so repeatables fall back to the
                    `recurring` STATUS and dailies come up empty. Open question.

WHAT EARNS A SPOT: only live work. `pending` is backlog, `parked` is shelved;
both stay in ClickUp. The statuses already carry this, so nothing new to keep up.
"""
import json, html, sys, os, base64, re, datetime
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DUMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "clickup_dump.json")
OUT  = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "board-data.js")

d = json.load(open(DUMP))
TODAY = datetime.date.fromisoformat(d["fetched"])

PRIO = {"urgent": 0, "high": 1, "normal": 2, "low": 3, None: 4}
LIVE = {"in progress", "next", "recurring"}
DONE = {"complete", "closed", "done"}
# A major quest line is a ClickUp FOLDER in PRNG Creative that is genuinely
# multi-step. A folder holding one lone task is a task someone filed in a
# folder, not a project, and it does not belong in this column. Raise or lower.
MULTISTEP = 2
# where a build currently stands, most-alive first
STATUS_RANK = {"in progress": 0, "next": 1, "recurring": 2, "waiting": 3,
               "pending": 4, "parked": 5}

esc = lambda s: html.escape(s, quote=False)
nice = lambda s: " ".join(w.capitalize() for w in s.split())

def due_key(t):
    dd = t.get("due_date")
    return (0, int(dd)) if dd else (1, 0)

def due_date(t):
    return datetime.date.fromtimestamp(int(t["due_date"]) / 1000) if t.get("due_date") else None

# ── Main quest line ── one note: the next immediate step ─────────────────────
# Client work plus the Books list, which is where the reports themselves live.
feeds_main = [t for t in d["clients"] if t["status"] in LIVE] + \
             [t for t in d["admin"] if t["status"] in LIVE and t["list"] == "Books"]
feeds_main.sort(key=lambda t: (due_key(t), PRIO[t.get("priority")]))
step = feeds_main[0] if feeds_main else None
main_q = ([{"type": "main", "text": esc(step["name"]),
            "status": nice(step["status"]), "sat": 0}] if step else [])

# ── Major quest lines ── next available quest per project, plus a tally ──────
tally = Counter()
total = Counter()
for t in d["creative_all"]:
    total[t["folder"]] += 1
    if t["status"] in DONE:
        tally[t["folder"]] += 1

open_by_folder = {}
for t in d["creative"]:
    open_by_folder.setdefault(t["folder"], []).append(t)

major_q = []
for folder in total:
    if total[folder] < MULTISTEP:
        continue
    tasks = sorted(open_by_folder.get(folder, []),
                   key=lambda t: STATUS_RANK.get(t["status"], 9))
    lead = tasks[0] if tasks else None
    major_q.append({
        "type": "major",
        "thread": folder.replace("Project ", ""),
        "text": esc(lead["name"]) if lead else "Nothing queued.",
        "status": nice(lead["status"]) if lead else "Clear",
        "tally": "%d of %d" % (tally[folder], total[folder]),
        "sat": 0,
        "_rank": STATUS_RANK.get(lead["status"], 9) if lead else 99,
    })
# lines that are actually moving come first; finished ones fall to the ledger
major_q.sort(key=lambda q: q.pop("_rank"))

# ── Admin ── side quests, dailies, repeatables ───────────────────────────────
# Starter dailies. Placeholders until the real ones are named and tagged in
# ClickUp -- at which point this list goes away and the `daily` branch below
# takes over on its own.
STARTER_DAILIES = ["Check email", "Check messages", "Check for new transactions"]

rep_q, daily_q, side_q = [], [], []
for t in d["admin"]:
    if t["status"] not in LIVE:
        continue
    if step and t["id"] == step["id"]:
        continue                      # already standing as the main quest step
    tags = [x.lower() for x in t.get("tags", [])]
    note = {"text": esc(t["name"]), "status": nice(t["status"]), "sat": 0}
    if "daily" in tags:
        daily_q.append({"type": "daily", **note})
    elif "repeat" in tags or t["status"] == "recurring":
        rep_q.append({"type": "rep", **note})
    else:
        side_q.append({"type": "side", **note})

if not daily_q:
    daily_q = [{"type": "daily", "text": esc(t), "sat": 0} for t in STARTER_DAILIES]

# ── The parts ClickUp does not own ───────────────────────────────────────────
y, m = TODAY.year, TODAY.month
target = datetime.date(y, m, 15) if TODAY.day <= 15 else \
         datetime.date(y + (m == 12), 1 if m == 12 else m + 1, 15)
days_left = (target - TODAY).days

# Ed does not repeat the note beside him, and he NEVER carries a count --
# rule 7: a number on the board is a scoreboard, and a scoreboard is a stick.
def ed_line(step, days_left):
    if not step:
        return "Board's clear. Pick the thing you keep walking past."
    dd = due_date(step)
    if dd and dd < TODAY:
        return "That one's already late. Do it before you open anything else."
    if dd and dd == TODAY:
        return "That's today's. Everything else can wait an hour."
    return "%d days to the 15th. One thing at a time." % days_left

BOARD = {
    "mainQuest": {"title": "Reports Out by the 15th", "daysRemaining": days_left},
    "ed": ed_line(step, days_left),
    "shield": {"active": False, "daysLeft": 0},
    "listener": {"waiting": False, "line": "Nothing waiting to be triaged."},
    "quests": main_q + major_q + side_q + daily_q + rep_q,
}

with open(OUT, "w") as f:
    f.write("/* Generated by fill_board.py from ClickUp — %s. Do not edit by hand.\n"
            "   Practice-internal: carries client names. Never commit, never deploy. */\n"
            % d["fetched"])
    f.write("window.BOARD_DATA = " + json.dumps(BOARD, indent=2, ensure_ascii=False) + ";\n")

# ── Bake a standalone copy ───────────────────────────────────────────────────
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
for k, v in [("main", main_q), ("major", major_q), ("side", side_q),
             ("daily", daily_q), ("rep", rep_q)]:
    print("  %-6s %2d" % (k, len(v)))
