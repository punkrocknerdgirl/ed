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
