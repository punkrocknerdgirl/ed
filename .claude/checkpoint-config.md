# Checkpoint config

- **Display name:** Project Ed
- **Slug:** ed
- **Log prefix:** ED
- **Expected origin:** punkrocknerdgirl/ed
- **Expected checkout:** /Users/erniehathaway/Projects/ed

## Standing guardrails

- Work one exact step at a time when interacting with Ernie during the build.
  The checkpoint itself is the exception — it runs straight through.
- Never run git through the device bridge. Reading `.git/refs/*` and
  `.git/logs/HEAD` with `cat` is safe. Any `git` subcommand is not, including
  read-only ones — they leave `.git/index.lock`, the bridge cannot unlink it,
  and Ernie's next commit dies.
- Read, analyze and draft are free. Ask first before anything that deletes,
  publishes, changes permissions, moves money, sends, commits Ernie to another
  human, alters a live automation, or rewrites git history.
- Never type a credential, an email at a login wall, or a one-time code into a
  form. Ernie authenticates.
- Verified and reported-but-unverified are different categories and the log must
  distinguish them in plain words. Proposed, saved, committed, pushed, deployed
  and verified are six different states.
- One container, one sensitivity level. The level is a property of the data, not
  the folder. Practice-internal never touches a web host.
- Verify from outside, logged out, in a browser that has never authenticated to
  that host. Check the content, not the status code. Every check needs a positive
  control or a silent zero looks exactly like a real one. When two probes
  disagree, believe the pessimistic one.
- Client dashboard and reporting work is built local. Nothing new goes online
  without Ernie's explicit say-so. The dads and bcr quote pages, already live
  behind their Cloudflare gate, are the only exceptions.
- A skill may carry real client names only while it is local-only. Once a skill
  goes account-wide the master is the shipped thing and there is no boundary left
  to scrub at.
- When a scan or a log has to be shown, return counts and exit codes, not
  content. Redaction by eye fails.
- Verify the destination exists before deleting the source.
- Deliverables go to Google Drive with the link in the reply. Never hand Ernie a
  `.md` attachment — she cannot download them.
- Never emit a `claude://.../new` link. The app has one window and it will eat
  whatever she is in.
