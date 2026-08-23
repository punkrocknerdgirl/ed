# Checkpoint config

- **Display name:** Project Ed
- **Slug:** ed
- **Expected origin:** punkrocknerdgirl/ed
- **Expected checkout:** /Users/erniehathaway/Projects/ed
- **Log directory:** docs/build-logs/
- **Filename prefix:** ED-
- **Glossary:** none — this repo has never kept one, do not create one
- **Bugs log:** docs/build-logs/ed-bugs.md (create on first entry)

## Where the rules actually live

The durable rulebook for this project is **`claude/how-we-build-things.md`, a
Claude Project doc — not a file in this repo.** Read Part 3 rule 10 (how to talk
to Ernie) and Part 5 (what Ed may do without asking) before touching anything.

This repo used to carry `docs/ED_CANON.md` and `docs/ed_standing-authority.md`,
which cited each other as current and pointed cold sessions at retired rules.
Both were deleted 2026-08-23 in `e9934d8`. If a copy turns up anywhere, it is
stale — do not restore it.

## Standing guardrails

- **Never run git through the desktop/device bridge.** Every git command there
  leaves a `.git/index.lock` the bridge cannot delete, and Ernie's next commit
  fails with "another git process seems to be running." Read repo state by
  cloning to a cloud container instead, or ask.
- **A cloud container cannot push to `ed`** — the git proxy refuses to inject a
  credential for it. Prepare the commit, hand Ernie the exact commands, then
  verify from origin afterwards.
- **The quest board is practice-internal and must never be deployed.** It
  carries client names. See Part 1 of how-we-build-things.
- `docs/interface/board-data.js`, `clickup_dump.json`, and
  `quest-board-live.html` are generated and gitignored. Never commit them.
- Any HTML handed to Ernie must be the **baked** standalone that `fill_board.py`
  emits. The source version points at `assets/` and `board-data.js`, so it opens
  broken from Downloads and reads as a bug in the work.
- Never hand Ernie a `.md` attachment — they cannot be downloaded on her end.
  Deliverables go to Google Drive under `My Drive/10 PRNG Projects/04 Project
  Ed` with a link, or inline in a code block.
- One ask at a time, and wait for the answer. Rule 10. The checkpoint process
  itself is the exception — it runs straight through.
- QuickBooks Online is read-only for Ed. Gmail is draft-only; sending needs an
  explicit instruction from Ernie and is never inferred from context.
- Never address Ernie by a campaign name. Daphne / Silvertone / Andromeda are
  her character, not her.
- Do not claim code was committed, pushed, deployed, tested, or verified unless
  it actually occurred. Verified and reported-but-unverified are different
  categories and the build log must distinguish them.
- Local checkout and GitHub main stay in sync — the local folder is the working
  copy, GitHub is the record. Build logs are written locally first, then pushed,
  never edited directly on GitHub.
