# Project Ed Feature Requests

Last reviewed: 2026-07-05
Status: Parking lot / extraction file

## Purpose

This file captures feature requests, future capabilities, candidate actions, and useful product ideas found in older Project Ed Google Docs or current Project Ed planning.

Google Docs are not treated as Project Ed canon. This file exists so useful feature ideas are not lost while old docs are archived or ignored.

Duplication is acceptable. Missing a real feature request is worse than capturing the same idea twice.

## Source handling rule

- Do not treat any source document here as current architecture by default.
- Extract feature requests only.
- Keep implementation decisions in the canon/build docs, not here.
- Keep sensitive values out of this file.

## Sources scanned in this pass

- Project Ed - Rebuild Brief
- Project Ed - Getting Started
- Project Ed - Auto Capture Log
- Ed Permission Broker v0 - code.gs
- PRNG OS - Ed + Airtable Design Plan
- Project Ed Onboarding Doc
- 2026-06-13 Project Abby

## Feature requests and candidate capabilities

### Capture and routing

- One assistant workflow where Ernie can dump work, thoughts, reminders, project notes, field notes, and process discoveries, and Ed routes items to the right place.
- Markdown capture path for Project Ed notes.
- Add a short local shell command such as `edcap "note here"` so Ernie can capture without typing the full Python caller path.
- Add process captures and field note candidates under a safe internal pass.
- Add non-public draft notes to internal docs under a safe internal pass.
- Create internal tasks from clear instructions once that action exists.
- Upload internal screenshots or artifacts to the correct Project Ed folder once that action exists.

### Future broker actions

Candidate broker actions after `captureNote` is stable:

- `captureTask`
- `appendToDontForget`
- `captureFieldNote`
- `uploadProjectArtifact`
- `appendBuildLog`

Each future broker action needs:

- explicit allowed destination
- explicit payload contract
- explicit failure modes
- permission-pass behavior
- human-approval boundary

### Caller layers and interfaces

Future caller layers to consider only after the local caller is boring and reliable:

- ChatGPT Action
- dashboard button
- Make scenario
- other controlled callers

Dashboard doctrine from source docs:

- Dashboard comes later.
- Dashboard is a view layer, not the system brain.
- Do not build dashboard before write/access plumbing is reliable.

### Status and work review

- ClickUp tasks should remain the active work source of truth.
- Review machinery such as status review and inbox processing should not become open loops themselves.
- A status review should avoid re-presenting tasks already reviewed in the same run.
- Ed may need a persistent or semi-persistent `reviewed_this_run` state.
- Candidate storage options mentioned elsewhere: ClickUp, lightweight local/session store, or transient daily review log.

### Conditional communications

- Add Conditional Comms as a base Ed feature.
- Pattern: draft a message now, park it, attach it to a task condition, and only release it if the condition remains true later.
- Related fields to consider:
  - recipient
  - draft reference
  - release condition
  - check date
  - resolution rule

### Intake and operational memory ideas

Potential operational-memory concepts found in planning docs:

- Every captured item should preserve source link, extracted text, classification, summary, confidence, status, and suggested route.
- Documents should be classifiable evidence linked back to Drive and related clients or workflows.
- Workflows may include Diane, AntiHub, payroll, A/R, A/P, monthly reports, cleanup, admin, and client follow-up.
- Human actions generated from intake or workflow state may sync to ClickUp instead of replacing ClickUp.
- Track people, clients, vendors, drivers, staff, partners, and contacts as entities when routing work.
- Track systems such as Google Drive, Gmail, Calendar, ClickUp, Make.com, Tally, Hubdoc, and related tools as routing/context entities.

### Permission and safety model

- The system should distinguish between suggested actions and authorized actions.
- Ed can classify, summarize, recommend, and draft.
- Automation can move records/files only when the destination and permission boundary are explicit.
- Sensitive, public, destructive, financial, permission-related, reputational, or ambiguous actions require explicit human review.

### AntiHub and document-support ideas

AntiHub-style support ideas that may become Ed-adjacent or PRNG OS features:

- receipt and document capture
- match candidates
- vendor identification
- category suggestions
- duplicate checks
- attachment routing
- review queues

### Abby-related requests

- Abby should be the technical documentation and analysis agent, not another Ed clone.
- Abby should be good at technical research, build analysis, documentation cleanup, and checking credible sources.
- Abby should save useful technical findings so they do not have to be researched from scratch every time.
- Project Abby exists separately at `punkrocknerdgirl/abby` and in ClickUp under Projects / Project Abby.

## Field-note candidates worth preserving

These are not exactly software features, but they capture product doctrine and may become site/field-note copy:

- The first job of the robot is to know where the notebooks are.
- The human should not have to label every thought; the robot should learn the labeler's handwriting.
- The build is the product.
- If the robot is supposed to act like it knows Ernie, the system needs real context, not just a prompt.
- The first key should be small enough to lose in a junk drawer and useful enough to miss when it is gone.

## Not included / intentionally excluded

- Sensitive values
- Current canon decisions
- Drive doc maintenance rules
- Old docs that only repeat already captured architecture without adding a feature request
