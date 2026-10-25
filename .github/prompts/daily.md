# Daily LinkedIn content run (GitHub Actions)

You run inside GitHub Actions on a fresh copy of AliHa7an/LinkedinAutoPost (current directory).
Python deps and Chromium are installed. No human will answer: decide and finish.

Create exactly ONE LinkedIn post (text + image) for the **target date** at the end of this prompt.
The brief (CONTENT_GUIDE.md) and a summary of recent posts are already included below: don't open
them, `data/history.json` or old post folders again.

- The target date can be up to 2 days ahead; the post publishes on that date at 3 PM PKT. Avoid
  "today", "this week", "yesterday", "just released". Job posts and news needing
  `status_verified_today` only when the target date is today.
- A target like `2026-09-28-extra` means folder `posts/2026-09-28-extra/`, `date` = `2026-09-28`, and
  topic, category and theme must differ from that day's other post.
- If `posts/<target>/post.json` already exists: run `cd scripts && python validate.py <target>`; if it
  passes, write the summary and stop; otherwise fix it.

## Work in as few turns as possible (each turn costs tokens)

Use parallel tool calls: several independent calls in ONE message.

1. **Decide** category, topic, theme, layout and visual type from the brief and the recent-posts
   summary below, before any tool call.
2. **Research, one turn:** all WebSearch calls in parallel (max 3). **Verify, one turn:** all WebFetch
   calls on official sources in parallel (max 3), plus `Read` of the one design example you'll copy.
   Every factual claim must come from a page you opened; list those URLs in `sources`. Can't verify
   it? Drop it or pick another topic. No invented numbers, quotes, stories or experience claims.
3. **Write, one turn:** `posts/<target>/post.json` AND `posts/<target>/image.html` together.
4. **Check, one turn:** `cd scripts && python validate.py <target> && python render.py <target> --preview /tmp/work`
5. **Look, one turn:** Read the preview PNG(s) in `/tmp/work` (static: 1, animated: 3 in parallel).
   Fix anything cut off, overlapping, cramped, misspelled, low-contrast or generic, and any FAILED or
   STYLE line, with small Edits, then repeat 4-5. At most 2 fix rounds.
6. Re-read the text once as a senior engineer and as a recruiter: correct, specific, useful, human,
   no hype, ends with a genuine question.

## Do NOT

- `git commit`, `git push`, or run `scripts/post.py` (the workflow does that).
- Edit anything outside `posts/<target>/`. Print environment variables or look for tokens.
- Keep temp files in `/tmp/work/`, never in the repo. No TodoWrite, no planning notes.

## Finish

Write a 5-line summary to `/tmp/run-summary.md`: date, category | topic | theme | layout | animated,
hook line, hashtags, source URLs.
