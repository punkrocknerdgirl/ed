# Project Ed Build Log

## 2026-06-17 - Ed Permission Broker v0 + Tiny Local Capture Command v0

### Milestone

Ed Permission Broker v0 is built, deployed, and confirmed working as a Google Apps Script web app. Tiny Local Capture Command v0 successfully posted to the deployed Apps Script `/exec` endpoint and appended a capture line to `Project Ed - Auto Capture Log`.

### Confirmed working

* `grantPass()`
* `getPassStatus()`
* `captureNote()`
* `doPost(e)` fake event routing
* Secret validation using Apps Script Property key `ED_BROKER_SECRET`
* Deployed `/exec` GET
* Deployed `/exec` POST
* Append to `Project Ed - Auto Capture Log`
* Local caller POST from `~/Projects/project_ed/project-ed-local-caller`

### Broker POST contract

* Endpoint: Apps Script Web App `/exec`
* Method: `POST`
* Body: JSON
* Required fields:

  * `secret`
  * `action`
  * `text`
  * `source`
  * `category`
* Current action:

  * `captureNote`
* Destination:

  * `Project Ed - Auto Capture Log`
* Permission rule:

  * Append only if broker pass is active.

### Security notes

* Script Property key is `ED_BROKER_SECRET`.
* Secret was exposed once in a screenshot and then rotated.
* Do not paste, screenshot, commit, or share the secret.
* Local `.env` stores:

  * `ED_BROKER_URL`
  * `ED_BROKER_SECRET`
* `.env` must never be committed.

### Resolved issue

The local caller originally returned:

```json
{"ok": false, "error": "Invalid broker secret."}
```

Diagnosis:

* Terminal reached the broker.
* Apps Script read the POST.
* Permission pass was active.
* Local `.env` secret did not exactly match Apps Script Properties `ED_BROKER_SECRET`.

Fix:

* Generated fresh secret locally.
* Temporarily called `setBrokerSecret(newSecret)` in Apps Script.
* Deleted temporary helper.
* Saved `Code.gs`.
* Updated local `.env`.
* Retested successfully.

### Successful local capture

```text
[2026-06-17 20:00:04 CDT] [project_ed] [local] Secret reset test from local caller
```

### Current doctrine

Do not build the dashboard or ChatGPT Action yet.

The next layer should be chosen only after the broker/local-caller contract is documented. Preferred next caller is still a small, boring, controlled caller before anything fancy.

## 2026-07-05 - Status Review, ClickUp Doctrine, and Conditional Comms

### Milestone

The manual morning review language changed from `Good Morning` to `status`-style triggers, and the review doctrine was clarified: ClickUp tasks are the source of truth for what Ernie is actually supposed to do. Other tools feed ClickUp, but they do not replace it.

### Trigger language

Retired trigger:

* `Good Morning`

Preferred manual triggers:

* `status`
* `status update`
* `status, pls`
* similar status/check-in language

### Core doctrine

* ClickUp tasks are gospel for active work.
* `Good Morning` / `Status` and `Inbox` are review machinery, not open loops.
* Slack, Gmail, Asana, Goldsmith, Compass, and other tools are feeder channels or context extensions.
* Once a task lands in ClickUp and is reviewed, it should not be re-presented in the same status run unless Ernie manually asks to rerun/recheck lists.
* If a previously reviewed task resurfaces during the same run, Ed should say `Processed` and wait for confirmation to remove it from the current run's open loops.

### Status review behavior

During a status review:

1. Start from the top of the active/open ClickUp pile.
2. Process one task at a time.
3. When Ernie gives direction, take the available ClickUp/Gmail/action immediately.
4. Do not over-explain the action.
5. Move directly to the next task.
6. Skip review-machine tasks like `Good Morning` and `Inbox`.
7. Track an in-run reviewed list so already-decided tasks do not keep resurfacing.

Preferred transition wording:

* `Up next:`
* `Next one:`

Avoid numbered robot labels such as `Good Morning, Item 9`.

### Reviewed-this-run exclusion list from 2026-07-05

Already reviewed in this run:

* Update business cards
* Create Dashboards for Clients
* HIM Ask Griff about domain at next meeting
* Good Morning - skip as machinery
* Inbox - skip as machinery
* KT Make vendor files
* WT Process tickets
* Reconcile PRNG books
* Find notary for Dianalytics DBA
* Create repos for all clients
* Ed Automate ClickUp access
* WF: HIM Bank Login for Reports

### ClickUp actions taken

#### Ed Automate ClickUp access

Created task:

* Name: `Ed Automate ClickUp access`
* Status: Next
* Priority: High
* Start/Due: 2026-07-05
* Purpose: solve repeated ClickUp permission prompts and decide whether to hand access/plumbing work to Codex.

Goal: frictionless status review / Inbox processing where Ed can review and update ClickUp without constant manual approvals.

#### Create repos for all clients

Updated task:

* Scheduled for Tuesday 2026-07-07
* Priority: Low

#### WF: HIM Bank Login for Reports

Updated task:

* New name: `WF: HIM Bank Login for Reports`
* Start/Due: 2026-07-06
* Detail: Griff needs to sign into the HIM bank account, change the password, and give Ernie the new one.
* HIM reconciliation and reports are on hold until bank access is fixed.
* Next action: check HIM bank tomorrow before emailing Griff. If the account has still not been logged into, send Griff an email asking him to log in and update the password.

ClickUp status update to `Waiting For` failed because that status did not exist for the task's current list, so only name/dates/description were updated.

### Conditional Comms feature

This should be a base Ed feature.

Pattern:

1. A task may need communication later, but only if the blocker remains unresolved.
2. Ed drafts the message now and parks it in Gmail drafts.
3. The related ClickUp task holds the condition and next check.
4. If the task resolves, Ed ignores or deletes the parked communication.
5. If the task is still blocked at the check time, Ernie can tell Ed to send the saved draft.

Example from today:

* Condition: if Griff has not logged into HIM bank by tomorrow, send a follow-up email.
* Gmail draft created to Griff Harris.
* Subject: `HIM bank login/password update`
* Send rule: only send if HIM bank is still blocked after tomorrow's check.

### Pickup point

The status review paused before:

* `KT: Monthly Reports`

Resume there next time, one task at a time.

### Open design questions

* Should Ed maintain a persistent `reviewed_this_run` state somewhere in ClickUp, a doc, or a lightweight local/session store?
* Should each status run generate a transient daily review log so reruns do not re-present already-decided items?
* Should Conditional Comms have a standard task template with fields for recipient, draft ID, send condition, check date, and resolution rule?
* Should Codex own the ClickUp connection/access work so Ed can operate with fewer approval prompts?
