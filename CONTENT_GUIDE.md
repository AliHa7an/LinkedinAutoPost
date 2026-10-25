# Daily LinkedIn post playbook

One post per day, 3:00 PM PKT, on Ali Hassan's personal profile. Recruiters and hiring managers at
software companies read it: a skipped day beats a weak, wrong or AI-sounding post.

## Who is posting

Ali Hassan, Senior Full Stack Developer and AI Engineer, 7+ years: React, Next.js, React Native,
Node.js, NestJS, TypeScript, AWS/Azure, Supabase, OpenAI, Vapi voice AI. Write as him, first person.
Never invent stories, employers, clients, numbers or results; no first-person experience claims
("I've hit this", "I built", "my team"). Opinions and advice are fine ("I'd start with…", "my rule of
thumb: …"). The validator blocks common experience phrasings.

## Value: every post must pass all four

1. **Useful today:** a fact, technique, checklist or decision rule that saves time, prevents a bug or
   incident, or helps a career step.
2. **Makes them think:** a trade-off, a corrected misconception, or the "why".
3. **Shows senior judgment:** production thinking, failure modes, security, cost, maintainability.
   Lean towards Ali's stack.
4. **Specific and true:** real APIs, real numbers from real sources, working code.

**Model post:** "Deep copy or lossy copy?" (structuredClone vs JSON.parse(JSON.stringify())) got by far
the most reach: an everyday problem, a surprising verifiable fact, a one-line fix, instantly readable.

**Mix:** 4–5 everyday quick wins a week, plus 1–2 **deep dives** (how something works under the hood,
distributed-systems trade-offs, AI/LLM internals, a real public postmortem, a scaling decision),
explained simply: one core idea, a clear diagram, jargon explained in a line.

**Scope:** `"broad"` = a problem most full-stack devs, tech leads or hiring managers meet. `"niche"` = one
flag, option or minor feature; max one per 7 days (enforced), and it must open with the broad problem
it solves ("Two deploys at once can break production"), never the feature name.

## Make it real (premium, not generic)

Generic tips sound like AI. Every post needs at least one **real anchor**, verified in this run:
- a real incident or public postmortem (company, year, what broke, the lesson), or
- a real number from a named study, benchmark or official doc (Stack Overflow survey, DORA, OWASP,
  vendor engineering blogs, MDN, official docs), or
- an exact, real behaviour shown in code or output (a real error message, a real API result).
Then add **one line of Ali's judgment**: when he'd use it, when he wouldn't, or the trade-off he'd
weigh. That opinion is what makes the post feel written by a senior engineer, not summarised.
Prefer concrete nouns (real tools, real error text, real numbers) over adjectives. No textbook intros.

## LinkedIn rules

- No misinformation, no misleading hooks, no engagement bait ("like if", "comment YES", "tag someone",
  "repost if", "follow for more"). A genuine question is the only call to action.
- 3–5 relevant hashtags, no links in the text (except the official page in a verified job post).
- Credit sources by name, no copied passages, no attacks on people or companies, no politics.

## Topics

One category per day from `config.json > rules.categories`: not the neighbouring days', prefer ones
unused in the last 7 days (see the recent-posts summary).
- ai-agents, ai-chatbots, ai-evolution: how agents work, tool calling, memory, evals, failure modes.
- javascript, typescript, code-tips: one concrete gotcha or time-saver with a short snippet.
- security, app-maintenance: practical checks, common mistakes, upgrade and monitoring habits.
- architecture: a real design problem and its trade-offs.
- integrations-automation: Zapier, Make, n8n, GitHub Actions, webhooks; when to automate, when not.
- new-tools, text-to-video, future-tech: genuinely new, verified, no hype.
- prompt-writing: before/after prompt examples.
- code-with-emotions, team-management, career, roadmap: specific and honest, no motivational fluff.
- jobs: only real open roles at strong tech companies, verified on the careers page (that one link
  allowed); only when the target date is today.

## Facts

- Every release, tool, statistic, price, company or job claim is checked on the web in this run and
  listed in `sources`. Can't verify it → leave it out. Never estimate numbers or dates.
- Freshness: never "currently in beta" / "just launched" unless confirmed today on the official page
  (then `"status_verified_today": true`, only when the target date is today). Give older launches
  their year.
- No speculation as fact ("most teams…"). Don't strengthen a source's wording. Code must be correct.

## Text (`text`)

Hook (max 140 chars: a surprising verified fact, sharp opinion, common mistake, or question) → short
body (1–2 sentence paragraphs, a list of 3–5 points or a short code block) → Ali's judgment line →
a specific closing question that invites real experience (never "Thoughts?").
Aim for 600–1,100 characters, max 9 paragraphs of ≤280 characters, code ≤8 lines; the image carries
the detail. `validate.py` prints STYLE notes when over: fix them. Voice: plain, confident, human,
contractions, 0–2 emojis. Avoid `config.json > rules.banned_phrases`.

Hashtags: one broad + focused, e.g. `#AIAgents #AI #SoftwareEngineering`, `#TypeScript #NodeJS
#WebDevelopment`, `#SystemDesign #SoftwareArchitecture #Backend`, `#CyberSecurity #WebSecurity #DevOps`.

## The image

Every image uses `design/brand.css`: same author header and footer on every post (the signature) and
10 curated themes for variety. Copy the closest file from `design/examples/` and change the content and
the theme class: `"theme": "<name>"` and `<body class="t-<name>">` (+ ` gif` when animated). The theme
can't match either of the previous or next 2 posts (enforced).

| `theme` | Look | Good for |
|---|---|---|
| `classic` ★ | warm off-white, LinkedIn blue | anything |
| `classic-dark` ★ | near-black, soft blue | tables, code, infra |
| `sky` ★ | light sky grey, sky blue | anything |
| `paper` | editorial magazine, serif, burnt orange | career, lessons, deep dives |
| `salmon` | light FT-pink, teal + claret | studies, numbers |
| `swiss` | white, black rules, red highlight | bold claims, myth vs fact |
| `blueprint` | blue engineering grid, amber | architecture, flows |
| `midnight` | navy and gold | AI, security, deep dives |
| `forest` | deep green, cream, brass | leadership, best practices |
| `terminal` | dark editor, green, mono | code tips |
★ = Ali's favourites, about half of all posts.

**Layouts: vary them.** Don't default to two boxes every day.

| Example file | Layout | Use for | `visual_type` |
|---|---|---|---|
| `code-comparison.html` | before/after panels | code gotchas | `code-comparison` |
| `comparison-table.html` | table | X vs Y, settings | `comparison-table` |
| `flow-diagram.html` | SVG boxes + arrows | architecture | `flow-diagram` |
| `animated-flow.html` | SVG with moving dots | request/data/agent flows | `animated-flow` |
| `animated-reveal.html` | steps appearing | build-up, before→after | any, animated |
| `hero-stat.html` | one huge number + context | studies, benchmarks, incidents | `stat-chart` |
| `bento.html` | 4-card grid | checklists, "4 rules", practices | `checklist` |
| `timeline.html` | numbered vertical steps | how-it-works, roadmaps | `roadmap` |
| `insight.html` | one strong statement | principles, opinions | `concept-card` |

Rules: structure `header.author` (AH, name, title, one tag) → `h1` (6–10 words, key phrase in `<em>`)
→ optional `.sub` → `main` → optional `.takeaway` → `footer` (`alihexan.com` + source name). Use only
kit classes and variables; no custom colours, gradients, glows, neon or emoji art (rejected). Phone
readable: ≤40 words, code ≤8 lines, 3–4 diagram boxes.

**Animate wherever something moves or happens in steps** (`"animated": true`, GIF 800×1000): `.r0`–`.r4`
reveal steps, SVG `.dot` + `<animateMotion>` along `.edge`, `.flowline`, `.pulse`, `.grow .bar`. Calm:
2–4 moving things, readable when paused. Static (PNG, rendered 2× sharp) when nothing moves. The
renderer rejects overlapping text, text off canvas and text touching a box edge.

## post.json

```json
{
  "date": "2026-09-28", "category": "architecture", "scope": "broad", "theme": "blueprint",
  "topic": "Why webhook handlers must be idempotent",
  "text": "Hook...\n\nBody...\n\nAli's judgment.\n\nQuestion for readers?",
  "hashtags": ["#SystemDesign", "#Backend", "#Webhooks"],
  "image": {"file": "image.html", "visual_type": "animated-flow", "animated": true, "duration_ms": 4000,
            "alt": "Animated flow of a webhook event checked for duplicates, signed Ali Hassan, alihexan.com"},
  "sources": ["https://..."]
}
```
