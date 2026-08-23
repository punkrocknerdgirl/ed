# 2026-08-23 — ED — The checkpoint skill became `/longrest`

## Purpose

"Checkpoint" collided with an actual Anthropic feature, so the session-closing
skill needed a new name. Renaming it turned into the larger question of where
skills live at all, and that turned out to be the more valuable half.

## Verified state

**Verified — checked directly:**

- `~/.claude/skills/` holds five skills: `longrest`, `css-color-theme`,
  `scale-ticket-processor`, `ticket-pipeline`, `wc-driver-pay`.
- The folder was renamed `checkpoint` → `longrest`; `SKILL.md` frontmatter now
  reads `name: longrest`, confirmed with `head -4`.
- The skill contains four files, not one: `SKILL.md`,
  `examples/diane-CHECKPOINT.md`, `references/log-template.md`,
  `references/project-config.md`. Confirmed with `ls -R` before anything was
  deleted anywhere.
- `~/Downloads/longrest.zip` contains all four; the `zip` output listed each.
- Ernie confirmed `/longrest` appears in Claude Code, claude.ai, and Cowork.

**Reported, not independently verified:**

- That the claude.ai upload carried all four files through. Ernie confirmed the
  skill shows up; nobody opened it afterward to confirm the references and
  examples came along.

## What changed this session

- `~/.claude/skills/checkpoint/` → `~/.claude/skills/longrest/`.
- `name: checkpoint` → `name: longrest` in the frontmatter. The folder name does
  not register the command; the frontmatter does.
- Fixed `whenErnie` → `when Ernie` in the description. That sentence is what
  Claude reads to decide whether to fire the skill, so a mangled word in it is a
  coin flip.
- Removed the old `checkpoint` skill from claude.ai and uploaded `longrest.zip`
  in its place.

## What was NOT changed

- **The body of the skill.** Every step, every standing rule, the whole process
  is untouched. Only the name moved.
- **Per-repo `.claude/checkpoint-config.md` files.** `ed`, `diane` and
  `prngclients` each have one and they still work — the config was never keyed to
  the skill's name. Renaming them is cosmetic and was deliberately skipped.
- **`~/Projects/diane/skills/`.** Seen in VS Code, left alone. See next step.
- **Nothing was committed or pushed.** This session touched no repo.

## Guardrails

Carried forward from the previous checkpoint, plus new ones from today.

**New, learned today:**

- **A skill with more than one file cannot be updated by pasting `SKILL.md`.**
  Paste or single-file Replace silently drops `references/` and `examples/`. Zip
  the whole folder and upload that. The claude.ai panel shows a file count next
  to the skill — read it before touching anything.
- **All skills live account-wide at `~/.claude/skills/`. No repo-local skill
  folders.** Ernie's call, and the reasoning holds: an unused skill is inert, it
  only fires when its description matches, so breadth costs nothing. A skill that
  lives in one repo is a skill you can't reach from the others.
- **`~/.claude/skills/` sits above `~/Projects`, so it covers every repo
  automatically.** No per-project setup, no config.
- **There is no single folder covering all three surfaces.** Claude Code reads
  the Mac; claude.ai and Cowork read Anthropic's copy. The disk is the master,
  the uploaded zip is the mirror, and the mirror goes stale silently.
- **A skill's description is a trigger, not documentation.** Bare common words in
  it — "rest", "check", "review" — invite accidental firing during ordinary
  conversation. Slash invocation is unambiguous; natural language is not.

**Carried forward:**

- Verified and reported-but-unverified are different categories, always stated in
  plain words.
- Never run git through the device bridge (Rule 5a).
- Client data and credentials never reach a public repo or an unnecessary chat.
- Write the log for someone with no memory of the session.

## Known issue opened

`~/Projects/diane/skills/` exists as a plain folder inside the `diane` repo. It is
**not** `.claude/skills/`, which is the name Claude Code looks under — so its
contents may be doing nothing at all. Unexamined. Open.

## Next step

Look inside `~/Projects/diane/skills/`. If it holds real skills, move them to
`~/.claude/skills/`; if it's dead weight, delete it. Either way the repo stops
holding skills, per today's rule.
