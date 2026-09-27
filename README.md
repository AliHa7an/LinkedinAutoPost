# LinkedIn Auto Post

One professional post (text + image) per day on Ali Hassan's personal LinkedIn profile, at
**3:00 PM PKT**, fully automatic and free.

```
Claude scheduled task (daily, ~11 AM PKT)          GitHub Actions (daily, 3:00 PM PKT)
  researches + verifies facts                          validates the post again
  writes posts/<date>/post.json                        renders image.html -> PNG / animated GIF
  designs posts/<date>/image.html        --push-->     publishes to LinkedIn (official API)
  runs validate.py + render.py                         records it in data/history.json
```

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
2. Repo secret `LINKEDIN_ACCESS_TOKEN` (scopes `openid profile w_member_social`).
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
| No post was prepared | the Claude task didn't push one | Nothing posted today; check the scheduled task |
| auto-post failed | API or network error | Re-run the workflow with dry run off |
