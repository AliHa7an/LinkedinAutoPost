# Manual content requests

Pushing a change to `requests/run.json` starts the "Generate content" workflow (same as clicking
**Run workflow** in the Actions tab).

```json
{ "date": "2026-09-29", "note": "optional extra instructions, e.g. 'make it about TypeScript generics'" }
```

`date` is optional (default: today in Asia/Karachi). If that day's post already exists or is
already published, the run does nothing. If the run finishes after 3 PM PKT on that same day, it
publishes straight away; otherwise the 3 PM workflow publishes it.
