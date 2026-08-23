# Build logs

Dated build notes for Project Ed. One file per checkpoint session.

- **Naming:** `YYYY-MM-DD-ED-<short-slug>.md`
- **Config:** `.claude/checkpoint-config.md` at the repo root sets the log
  directory and prefix, and carries this repo's standing guardrails. Read it
  before writing a log.
- **The rulebook is not in this repo.** It is `claude/how-we-build-things.md`,
  a Claude Project doc. Part 3 rule 10 governs how to talk to Ernie; Part 5
  governs what may be done without asking.

Logs are written locally first, then pushed. Never edit them directly on GitHub.

Each log should record what was verified, what changed, **and what was
deliberately not changed** — the last one is what makes a log useful three
weeks later.

Before committing a log, sweep it for client names. A build log about
client-adjacent work is itself client-adjacent, and this repo is public.

## Pushing changes

The loop, for when you have edited, moved, renamed, or deleted files locally:

```bash
cd ~/Projects/ed
git status
git add -A
git commit -m "what changed and why"
git push origin main
```

`git add -A` stages everything at once — edits, new files, deletions, and
renames. It is safe in this repo because `.gitignore` covers the generated
board files and `.env`, but read `git status` first anyway. In a checkout that
carries unrelated stray files, name the files explicitly instead.

Renames need nothing special: Git detects them by comparing content.

**`git status` does not prove a push worked.** It compares your branch to a
cached copy of origin, not to GitHub. The push output is the receipt — a line
like `0d177a2..6b9f72e  main -> main` means it landed. To check later, run
`git fetch origin` **first**, then `git status`.

Full command reference, including what to do when a push is rejected:
`~/Projects/diane/docs/build-logs/terminal-and-git-glossary.md`
