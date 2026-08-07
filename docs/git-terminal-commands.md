{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # Git & Terminal Commands \'97 Working Reference\
\
Commands relearned while building Diane 2.0. Plain text, one command at a time.\
Format: command \uc0\u8594  what it does \u8594  (why, when relevant)\
\
---\
\
## Navigation\
\
`cd /Users/erniehathaway/Projects/diane`\
Moves Terminal into the Diane repository folder.\
\
`pwd`\
Prints the full path of the folder you are currently in.\
\
---\
\
## Status & Comparison\
\
`git status`\
Shows the current branch, modified files, untracked files, staged files, and whether local and remote history differ.\
\
`git branch --show-current`\
Prints the name of the branch currently checked out.\
\
`git log --oneline --left-right --graph HEAD...origin/main`\
Compares local `main` with `origin/main`. `<` marks local-only commits and `>` marks remote-only commits.\
\
`git diff --stat`\
Shows a compact summary of changed files and line counts.\
\
`git diff --check`\
Checks the current diff for whitespace errors and conflict-marker problems. No output means it passed.\
\
`git diff -- <file>`\
Shows uncommitted changes in one file compared with the current local commit.\
\
`git diff origin/main -- <file>`\
Compares the current working copy of one file directly with GitHub's `origin/main` version.\
\
---\
\
## Inspecting Commits\
\
`git show --stat --oneline <commit>`\
Shows a commit summary and which files changed, without dumping the full patch.\
\
`git show --format= --no-ext-diff --unified=8 <commit> -- <file>`\
Shows the actual diff for one file in one commit, with eight lines of surrounding context.\
\
---\
\
## Searching\
\
`grep -nE "pattern1|pattern2" <file>`\
Searches a file for either pattern and prints matching line numbers.\
\
---\
\
## Safety & Backup\
\
`git branch backup/pre-reconcile-2026-08-06`\
Creates a safety branch pointing at the current commit without switching branches.\
\
`git stash push -u -m "message"`\
Temporarily stores tracked and untracked local work. `-u` includes untracked files and folders; `-m` adds a readable label.\
\
`git stash list`\
Lists saved stashes.\
\
`git stash apply`\
Reapplies the newest stash but keeps the stash saved until you confirm the files restored correctly.\
\
---\
\
## Rewriting / Applying History\
\
`git reset --hard origin/main`\
Moves local `main` to exactly match `origin/main`. Only use after protecting local work with a backup branch and stash.\
\
`git cherry-pick <commit>`\
Copies one specific commit onto the current branch.}

---

## Divergent History / First-Time Setup

`git push --set-upstream origin main`
Links your local `main` branch to `origin/main` on GitHub so future `git push` (no flags) knows where to send commits. Needed once per branch, typically the first time you push a locally-created repo, or after a fresh `git init` that was never cloned from the remote.

`git pull origin main --no-rebase --allow-unrelated-histories`
Merges two branches that don't share a common commit ancestor — happens when a local folder was `git init`'d fresh (not cloned) but points at a GitHub repo that already has its own separate commit history. `--no-rebase` forces a true merge commit instead of rewriting history (safer to reason about than rebase). `--allow-unrelated-histories` overrides git's default refusal to merge two trees with no shared starting point.

**If this opens Vim for a merge commit message:**
Press `Esc`, type `:wq`, press `Enter`. This saves the default message and exits — you are not expected to write a custom message here.

**If it instead reports `error: untracked working tree files would be overwritten by merge`:**
This means files exist locally at the same path as files in the incoming history, but were never `git add`'d. Back them up first (`cp` to a folder outside the repo), delete the local untracked copies, then retry the pull. Do not delete without backing up first if the local copies might contain content the remote doesn't have — check with `git diff origin/main -- <file>` before deleting.