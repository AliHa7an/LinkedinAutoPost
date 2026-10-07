# Daily LinkedIn post playbook

Brief for the daily Claude run. One post per day, 3:00 PM PKT, on Ali Hassan's personal profile.
Recruiters and hiring managers at software companies read this profile, so a skipped day is always
better than a weak, wrong or AI-sounding post.

## Who is posting

Ali Hassan, Senior Full Stack Developer and AI Engineer, 7+ years: React, Next.js, React Native,
Node.js, NestJS, TypeScript, AWS/Azure, Supabase, OpenAI and Vapi voice AI. Portfolio: alihexan.com.
Write as him, first person, as a working engineer. Never invent stories, employers, clients, numbers
or results. No first-person experience claims ("I've hit this…", "I built…", "my team…"); opinions
and advice are fine ("I'd start with…", "my rule of thumb: …"). The validator blocks common
experience phrasings.

## Audience and the value test

Readers: software engineers, tech leads, founders, recruiters and HR at software companies.
Every post must pass all four before you write it:

1. **Useful today:** the reader leaves with a fact, technique, checklist or decision rule that saves
   time, prevents a bug or incident, or helps a decision or a career step.
2. **Makes them think:** a trade-off, a common misconception corrected, or a "why", not just a "what".
3. **Shows senior judgment** (what recruiters notice): production thinking, trade-offs, failure
   modes, security, cost, maintainability, clear explanation. Lean towards Ali's stack when the
   topic allows it.
4. **Specific and true:** real APIs, real numbers from real sources, working code.

Formats to rotate: before/after code, myth vs fact, mistake → fix, trade-off comparison, checklist,
step-by-step flow, "what a study/report found and what to do with it", roadmap, mini case study from
a public postmortem or official engineering blog.

## LinkedIn rules (Professional Community Policies)

- No misinformation or unverifiable claims; no misleading hooks (hook must match the content).
- No engagement bait: never "like if…", "comment YES", "tag someone", "repost if", "follow for more",
  "react with…". A genuine question that needs a thoughtful answer is the only call to action.
- No spam: 3–5 relevant hashtags, no link in the text (except the official page in a verified job
  post), no repeated content.
- Respect others: credit sources by name, no copied passages, no attacks on people or companies, no
  politics or religion, no confidential or private information.

## What works best (from Ali's own results)

Model post: "Deep copy or lossy copy?" (2026-09-30, structuredClone vs JSON.parse(JSON.stringify())).
It got far more impressions than the rest because it was:
1. **An everyday problem** most developers have hit (copying an object), not a rare setting.
2. **A surprising, verifiable fact** (the common way silently breaks Dates, Sets, circular refs).
3. **A fix they can use today**, in one line.
4. **Instantly readable**: a clear before/after visual and a short text.
Before writing, ask: "Would most of Ali's network meet this problem this month, and will they learn
something true and useful in 30 seconds?" If not, pick another topic.

## Reach: pick topics many people care about

Low-reach posts were narrow one-flag tips (a TypeScript utility type, a CI concurrency key, a git
flag, a Dependabot setting). Set `"scope"` in post.json:
- `"broad"`: a problem most full-stack developers, tech leads or hiring managers meet: system design
  decisions, AI agents/LLM apps in production, performance, security fundamentals, debugging and
  reliability lessons (public postmortems), React/Next.js/Node patterns, code review, careers,
  interviews, working in teams.
- `"niche"`: one specific option, flag or minor language feature. At most one per 7 days (enforced).
Even a niche tip must open with the broad problem it solves ("Two deploys at once can break
production"), not the feature name ("Actions concurrency").

## Topic rotation

One category per day from `config.json > rules.categories`: not yesterday's, prefer ones unused in
the last 7 days (`python scripts/recent.py` shows this).

- ai-agents, ai-chatbots, ai-evolution: how agents/bots work, tool calling, memory, evals, failure modes.
- javascript, typescript, code-tips: one concrete tip with a short snippet, a gotcha, a time-saver.
- security, app-maintenance: practical checklists, common mistakes, upgrade and monitoring habits.
- architecture: a real design problem and its trade-offs (queues, caching, idempotency, multi-tenant…).
- integrations-automation: Zapier, Make, n8n, GitHub Actions, webhooks; when to automate, when not.
- new-tools, text-to-video, future-tech: genuinely new releases, verified, no hype.
- prompt-writing: better prompts with a before/after example.
- code-with-emotions, team-management, career, roadmap: growing, getting hired, leading, learning;
  honest and specific, no motivational fluff.
- jobs: only real open roles at strong tech companies, verified today on the company's careers page
  (one link allowed: that page). Name company, role, remote/location, stack. Otherwise pick another.

## Facts and recent studies

- Every release, tool, statistic, price, law, company or job claim is checked on the web in this run
  and listed in `sources`. Can't verify it → leave it out. Never estimate numbers or dates.
- Good sources for "recent studies": official docs and changelogs, engineering blogs of the company
  involved, Stack Overflow Developer Survey, GitHub Octoverse, Google DORA / State of DevOps, OWASP,
  NIST, Verizon DBIR, peer-reviewed papers, reputable tech press. Name the source in the text.
- Freshness: don't call something new or current ("currently in beta", "just launched") unless you
  confirmed its status today on the official page; then add `"status_verified_today": true`. Frame
  older launches with their year. Prefer the last 30 days for news posts.
- No speculation presented as fact ("most teams…", "90% of developers…"). Every sentence is either
  from a checked source or a well-established engineering principle. Don't strengthen a source's
  wording ("occasionally" never becomes "always").
- Code must be correct for the stated language version.

## Writing the text (`text`)

1. Hook (max 140 chars): a surprising verified fact, a sharp opinion, a common mistake, or a question.
2. Body: short paragraphs (1–3 lines), blank lines between; a numbered list, short code block,
   before/after, or 3–5 practical points.
3. One clear takeaway line.
4. Last paragraph: a specific question that invites real experience ("What's the one check you'd add
   before shipping an agent to production?"), never "Thoughts?".

**Concise:** readable in under a minute. Aim for 600–1,100 characters (stay within 350–1,300).
One idea per post; the image carries the detail. Paragraphs of 1–2 short sentences (max 280
characters), at most 9 paragraphs, lists of 3–5 items, code blocks of 8 lines or fewer. Cut every
sentence that doesn't add a fact, a step or the takeaway. `validate.py` prints STYLE notes when a
post goes over these targets: fix them. They don't block publishing, but aim to have none.

Voice: plain, confident, human; contractions; varied sentence length; 0–2 emojis (max 5). No hashtags
or links in the text. Avoid `config.json > rules.banned_phrases` and anything that sounds like a
press release.

## Hashtags (`hashtags`)

3–5, most relevant first, one broad + focused ones, e.g. `#AIAgents #AI #SoftwareEngineering`,
`#TypeScript #NodeJS #WebDevelopment`, `#SystemDesign #SoftwareArchitecture #Backend`,
`#CyberSecurity #WebSecurity #DevOps`, `#Automation #NoCode #Zapier`,
`#CareerGrowth #TechCareers #SoftwareDevelopers`, `#PromptEngineering #GenerativeAI #LLM`.

## The image: brand kit, not a new theme every day

Every image uses **`design/brand.css`**, so the feed looks like one recognisable author. Only the
content changes. Start from the closest file in `design/examples/` (`code-comparison.html`,
`comparison-table.html`, `flow-diagram.html`) and change the text, code and diagram.

- `<link rel="stylesheet" href="../../design/brand.css">`, `<body class="light">` or
  `<body class="dark">` (`"theme"` in post.json is `"light"` or `"dark"`; mostly light, dark for
  code-heavy posts). For an animated GIF add `gif`: `<body class="light gif">`.
- Fixed structure: `header.author` (avatar "AH", name, title, one topic tag) → `h1` (6–10 words, one
  key phrase in `<em>`) → optional `.sub` → `main` (the visual) → optional `.takeaway` → `footer`
  (`alihexan.com` + source name).
- Use only the kit's classes and variables (`.panel`, `.panel.good/.bad`, `pre`, `table`, `.stats`,
  `ul.check`, SVG `.node/.edge/.nlabel/.nsmall/.dot`, `var(--accent)`). No custom colours, gradients,
  glows, blur, neon, emoji art, stickers, paper or retro effects: the validator rejects them.
- Readable on a phone: max ~40 words on the image, code max 8 lines, 3–4 diagram boxes.

Pick `image.visual_type` for the topic (validator checks it):

| Topic | `visual_type` |
|---|---|
| A process with moving parts (request, pipeline, agent loop, queue, auth flow) | `animated-flow` (GIF, `"animated": true`; animate a `.dot` along `.edge` with SVG `<animateMotion>`) |
| Architecture or system layout | `flow-diagram` |
| Code tip or gotcha | `code-comparison` (before/after) or `code-snippet` |
| Security or maintenance practice | `checklist` |
| X vs Y, trade-offs | `comparison-table` |
| Study, report or benchmark numbers | `stat-chart` |
| Career path or learning plan | `roadmap` |
| One idea or principle | `concept-card` |

Use GIF only for real flows, PNG for everything else. LinkedIn accepts JPG, PNG and GIF (≤250 frames).
The renderer rejects overlapping text, text off the canvas and text touching a box edge.

## Files to write

`posts/YYYY-MM-DD/post.json`:

```json
{
  "date": "2026-09-28",
  "category": "architecture",
  "topic": "Why webhook handlers must be idempotent",
  "theme": "light",
  "scope": "broad",
  "text": "Hook...\n\nBody...\n\nQuestion for readers?",
  "hashtags": ["#SystemDesign", "#Backend", "#Webhooks"],
  "image": {
    "file": "image.html",
    "visual_type": "animated-flow",
    "alt": "Animated flow of a webhook event checked for duplicates, signed Ali Hassan, alihexan.com",
    "animated": true,
    "duration_ms": 4000
  },
  "sources": ["https://..."]
}
```

and `posts/YYYY-MM-DD/image.html`. Then from `scripts/`: `python validate.py <date>` and
`python render.py <date> --preview /tmp/work`, look at the previews, fix, repeat until both pass.
The workflow commits and publishes; rendered images are never committed.
