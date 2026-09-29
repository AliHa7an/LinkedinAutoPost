# LinkedIn Auto Post

One professional post (text + image) per day on Ali Hassan's personal LinkedIn profile, at
**3:00 PM PKT**, fully automatic and free.

```
"Generate content" (GitHub Actions, ~8:20 AM PKT)   "Daily LinkedIn post" (GitHub Actions, 3:00 PM PKT)
  Claude Code (CLAUDE_CODE_OAUTH_TOKEN)               validates the post again
  researches + verifies facts                         renders image.html -> PNG / animated GIF
  writes posts/<date>/post.json + image.html  ---->   publishes to LinkedIn (official API)
  validates, renders, looks at the image              records it in data/history.json
  commits the post
```

Everything runs on GitHub: no computer needs to be on and nothing waits for approval.

GitHub's scheduler can start runs hours late, so both workflows try many times a day:
"Generate content" every hour 8:20 AM–8:20 PM PKT, "Daily LinkedIn post" at 2:40 PM (waits until
3:00) and every hour 3:05–11:05 PM PKT. Every run checks `data/history.json` first and finishes in
seconds, without using Claude, if today's post already exists or is already published, so there is
never more than one post per day. Scheduled runs never publish before 3 PM. If generation finishes
after 3 PM, it publishes immediately. If a prepared post was never published (GitHub too late), the
next day's run reuses it instead of writing a new one (not for job posts or time-sensitive news).

Start a run manually: Actions > Generate content > Run workflow (optional date + note), or push
`requests/run.json` (see `requests/README.md`). The Claude instructions are in
`.github/prompts/daily.md` and `CONTENT_GUIDE.md`.

## Safety

- Official LinkedIn API only, with the `w_member_social` permission. The code can create a post
  and nothing else: no likes, comments, connection requests or messages.
- Hard limit of 1 post per day (`data/history.json`).
- `scripts/common.py > validate_post` blocks publishing when: the topic was posted in the last 45
  days, the image theme in the last 14 days, the category was yesterday's, the text has links
  (except verified job posts), hashtags are outside 3–5, AI-cliché phrases appear, there is no real
  question for readers, factual categories have no sources, or the image lacks "Ali Hassan" /
  "alihexan.com".
- Anything wrong means **nothing is posted** and a GitHub issue is opened (you get an email).
- Instant off switch: LinkedIn > Settings > Data privacy > Permitted services > remove
  "Posting Automatically", or disable the workflow in the Actions tab.

## Setup (done once)

1. LinkedIn app "Posting Automatically" with products *Share on LinkedIn* and *Sign In with
   LinkedIn using OpenID Connect*.
2. Repo secrets: `LINKEDIN_ACCESS_TOKEN` (scopes `openid profile w_member_social`) and
   `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`, same as FBAutoPoster).
3. Settings > Actions > General > Workflow permissions: **Read and write**.

## Every 60 days: renew the token (2 minutes)

LinkedIn tokens for self-serve apps expire after 60 days and cannot be refreshed automatically.
A reminder issue opens 10 days before `config.json > token.expires_on`.

1. https://www.linkedin.com/developers/tools/oauth/token-generator, app *Posting Automatically*,
   scopes `openid`, `profile`, `w_member_social`, Request access token, Allow.
2. Update the `LINKEDIN_ACCESS_TOKEN` secret.
3. Set `token.expires_on` in `config.json` to today + 60 days.

## Manual controls

- **Test without posting:** Actions > Daily LinkedIn post > Run workflow (dry run is on by default).
  The rendered image is attached to the run as an artifact.
- **Skip a day:** delete that day's folder in `posts/`.
- **Edit a post before 3 PM:** edit `posts/<date>/post.json` or `image.html` on GitHub; the
  "Check new posts" workflow validates it.
- **Write your own post:** add a folder following `CONTENT_GUIDE.md`.

## Local

```bash
pip install -r requirements.txt && python -m playwright install chromium
cd scripts
python validate.py 2026-09-28
python render.py 2026-09-28
python post.py --date 2026-09-28 --dry-run
```

## Troubleshooting

| Issue title | Meaning | Fix |
| --- | --- | --- |
| token expired or missing | 401 from LinkedIn | Renew the token (above) |
| failed safety checks | the prepared post broke a rule | Read the run log, fix or delete the post |
| content generation failed | the Claude run errored (often an expired `CLAUDE_CODE_OAUTH_TOKEN`) | Open the run; renew the token with `claude setup-token` if needed; re-run Generate content |
| No post was prepared | no post existed by 6 PM PKT | Check the Generate content runs |
| auto-post failed | API or network error | Re-run the workflow with dry run off |
