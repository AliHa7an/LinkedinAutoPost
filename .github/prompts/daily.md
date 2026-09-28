# Daily LinkedIn content run (GitHub Actions)

You are running inside a GitHub Actions job on a fresh copy of the AliHa7an/LinkedinAutoPost repo
(current directory). Python dependencies and Chromium (Playwright) are already installed. There is
no human to answer questions: make reasonable decisions and finish the job.

## What to do

Create exactly ONE LinkedIn post (text + image) for the **target date** given at the end of this
prompt (it can carry a suffix like `2026-09-28-extra` for an extra post: then the folder is
`posts/2026-09-28-extra/` and the `date` field inside post.json is just `2026-09-28`; the post must
also differ in topic, category and image theme from any post already published that day), following `CONTENT_GUIDE.md` exactly, together with `config.json` and `data/history.json`.

1. Read `CONTENT_GUIDE.md`, `config.json` and `data/history.json` in full. Also list `posts/` and
   read the `topic`, `category` and `theme` of every existing post so you don't repeat any of them.
2. If `posts/<target date>/post.json` already exists, or `data/history.json` already has the target
   date: run `cd scripts && python validate.py <target date>`. If it passes, stop and only write the
   summary. Otherwise fix that post.
3. Pick the category (not yesterday's; prefer ones unused in the last 7 days), then research with
   WebSearch/WebFetch. Every factual claim must come from an official or reputable source you
   opened in this run, and every source URL goes in `sources`. No hypothetical, speculative or
   invented statements, numbers, quotes or stories. If you can't verify a topic, choose another.
   Job posts only for real, currently open roles verified on the company's own careers page.
4. Write `posts/<target date>/post.json` and `posts/<target date>/image.html` (new visual theme,
   "Ali Hassan" and "alihexan.com" on the image).
5. From `scripts/` run `python validate.py <target date>` and `python render.py <target date> --preview /tmp/work`.
   Then LOOK at the preview PNGs in `/tmp/work` with the Read tool (for an animated post these are
   frames from the start, middle and end). Fix anything cut off, overlapping, cramped, misspelled,
   low-contrast or generic-looking, and repeat until both commands pass and the image looks like a
   designer made it.
6. Re-read the text once as a senior engineer and once as a recruiter: correct, specific, useful,
   human, no hype, ends with a genuine question for readers.

## Do NOT

- Do not run `git commit` or `git push`, and do not run `scripts/post.py`. The workflow validates,
  commits and publishes after you finish.
- Do not edit anything outside `posts/<target date>/`.
- Do not print environment variables or look for tokens.
- Keep temporary files in `/tmp/work/`, never inside the repo.

## Finish

Write a short Markdown summary to `/tmp/run-summary.md`: date, category, topic, theme, whether the
image is animated, the hook line, the hashtags, the source URLs you used, and anything you skipped
and why.
