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

Voice: plain, confident, human; contractions; varied sentence length; 0–2 emojis (max 5). No hashtags
or links in the text. 900–1,800 characters ideal (limits 400–2,600). Avoid
`config.json > rules.banned_phrases` and anything that sounds like a press release.

## Hashtags (`hashtags`)

3–5, most relevant first, one broad + focused ones, e.g. `#AIAgents #AI #SoftwareEngineering`,
`#TypeScript #NodeJS #WebDevelopment`, `#SystemDesign #SoftwareArchitecture #Backend`,
`#CyberSecurity #WebSecurity #DevOps`, `#Automation #NoCode #Zapier`,
`#CareerGrowth #TechCareers #SoftwareDevelopers`, `#PromptEngineering #GenerativeAI #LLM`.

## The image: pick the visual that explains the topic best

Set `image.visual_type` to one of these (the validator checks it):

| Topic | `visual_type` | Output |
|---|---|---|
| A process with moving parts: request lifecycle, agent loop, pipeline, webhook/queue/integration, auth flow | `animated-flow` | animated GIF (`"animated": true`) |
| Static architecture or system layout | `flow-diagram` | PNG |
| Code tip or gotcha | `code-comparison` (before/after) or `code-snippet` | PNG |
| Security or maintenance practice | `checklist` | PNG |
| X vs Y, trade-offs | `comparison-table` | PNG |
| Study, report or benchmark numbers | `stat-chart` | PNG |
| Career path or learning plan | `roadmap` | PNG |
| One idea or principle | `concept-card` | PNG |

PNG keeps text and lines sharp (better than JPG for diagrams and code). GIF is for motion: use it
whenever the topic is a flow, and only then. LinkedIn accepts JPG, PNG and GIF (GIF up to 250 frames).

- Self-contained `image.html`: 1080×1350 for PNG, 800×1000 for GIF. Inline CSS/SVG only; Google Fonts
  is the only external resource.
- A clearly different look every day, named in `theme` (e.g. "blueprint grid", "terminal", "hand-drawn
  notebook", "retro poster", "glassmorphism dark", "newspaper", "pastel isometric", "chalkboard",
  "Swiss minimal", "neon synthwave", "paper cut-out", "code editor window", "sticky notes", "subway
  map", "comic panel"). No theme repeats within 14 days.
- Large readable text (28px+ PNG, 24px+ GIF), max ~40 words, lay out with flex/grid (not per-line
  absolute positions), keep 16px+ padding inside every box. "Ali Hassan" and "alihexan.com" in a
  footer or corner. The renderer rejects overlapping text, text off the canvas, and text touching a
  box edge.
- Animation: CSS `@keyframes` or SVG `<animate>`, looping cleanly within `duration_ms` (e.g. 4000),
  no JavaScript timers, a few moving elements (packets along arrows, highlighted steps).

## Files to write

`posts/YYYY-MM-DD/post.json`:

```json
{
  "date": "2026-09-28",
  "category": "architecture",
  "topic": "Why webhook handlers must be idempotent",
  "theme": "blueprint grid",
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
