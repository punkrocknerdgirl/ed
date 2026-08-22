# PRNG art style — the tavern look

The house style for everything on Ernie's side of the wall: NPC portraits, agent
avatars, spell cards, the quest board. Point at this doc and say *"use this
style."*

Client-facing work does **not** use this. That stays Fraunces / Public Sans and
restrained — see Part 2 of `how-we-build-things.md`. This is the cockpit, and no
client ever sees it.

Established 2026-08-22 from the *Breath of the Moth* / *How You Doin'?* spell
cards and The Listener portrait, all of which landed on the first try.

---

## The style block

Paste this verbatim at the top of any image prompt. Attach one existing image as
a visual reference alongside it — that does more than any amount of wording.

```
Painterly fantasy trading-card illustration: rich semi-realistic digital
painting, high finish, no visible brushstrokes. Warm tavern or stone-cellar
interior — vaulted arches, hanging iron lanterns with warm orange flame,
candlelit tables, blurred figures in the background. The magic itself is the
primary light source, casting dramatic rim lighting on the subject. Deep
saturated color, gold and violet dominant. Drifting motes of light. Dark
background falloff so the subject pops.
```

## What makes it work

- **The glow is the lamp.** Every one of these reads because the spell effect,
  not an off-screen key light, is lighting the subject.
- **Negative space holds the magic.** Character on one side, effect filling the
  other. Don't center the character and squeeze the effect around them.
- **The background is a real place, blurred.** Depth of field on lanterns and
  patrons sells it. A flat backdrop kills it instantly.
- **Gold and violet.** Green and red are accents. Straying from that palette is
  what makes an image stop matching the set.

## Character-portrait template

```
[STYLE BLOCK]

Subject: [NAME] — [species, age, build]. [Clothing and materials, specific.]
[One prop that says who they are.] [Expression — one clear emotion, not
"mysterious".]

Composition: three-quarter view, bust to waist. Character occupies the right
third; [magic effect / firelight / smoke] fills the left. Tavern interior
softly out of focus behind. Portrait orientation, 2:3.
```

Swap to **1:1, closer crop, subject fills 70% of frame** when it's going in a
round avatar slot (ClickUp agents, etc.).

## Object / place template

Same block, then describe the object as the character. See The Listener below —
no faces, the thing itself carries the frame.

---

# The set so far

## Daphne — Ernie's character
Tiefling bard. Purple skin, red hair, curved black horns, green leather coat
with a teal clasp, red cloak. Lute and nightwood flute. Established across
*Breath of the Moth*, *How You Doin'?*, and the bard portrait. **Any campaign
name means Ernie.**

## The Listener — the night agent
Object portrait, no face. Prompt that worked:

```
[STYLE BLOCK]

Subject: THE LISTENER — a single massive faceted crystal roughly the size of a
blacksmith's anvil, suspended on fine silver chains in a circular chamber with
polished black obsidian walls. Flowing glowing script is carved across its
faces, shifting and alive. A tiny articulated silver hammer on a jointed arm
hovers against one facet, mid-tap, having just carved a new line. Light inside
the crystal glows warm gold at its core, bleeding to violet at the edges with
one thread of deep red.

No people, no faces. The crystal is the character. Ancient, patient, watchful.
Square composition, 1:1.
```

## Ed — the Innkeeper and Dungeonmaster
**Generated 2026-08-22, first try, kept.** Broad weathered man in his sixties,
grey beard, heavy leather apron, quill behind the ear, battered ledger open on
the bar, worn ivory d20 beside it. Expression: fond and unimpressed at once.

**Canon the image invented and we're keeping:** the slate sign on his tavern
wall reads

> **Good ale. Warm beds. Bad excuses.**

That is Ed's entire character rule in six words — annoyed, never shaming, never
keeping score. It belongs on the quest board, and it's the answer to what the
inn is called if we ever need one.

---

## Where the files live

**ClickUp → `Graphics`** — doc `8chynfx-11251`, page `8chynfx-13651`:
https://app.clickup.com/9011418621/docs/8chynfx-11251/8chynfx-13651

Every generated image goes there. One home, and it's the answer to "where's that
picture" without thinking about it.

This doc holds the *prompts*. `Graphics` holds the *pictures*.

*Possible future move: art could live on each character's page in ClickUp →
PRNG HQ → PRNG Agent Directory (`8chynfx-8091`), which already has pages for Ed
and Diane, so the picture sits beside the spec. Not now — `Graphics` is one
place and one place is the point.*

## Sweep note — 2026-08-22, resolved

A page called **"AI Agent Avatar Style System"** existed in the ClickUp doc
*Stored in Notion* (`8chynfx-8011`), last touched in May. Ernie deleted it —
old data. This doc is now the only style system. One home.  