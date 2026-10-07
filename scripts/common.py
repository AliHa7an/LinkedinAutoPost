"""Shared helpers: config, dates, history and post validation."""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
HISTORY_FILE = ROOT / "data" / "history.json"
PKT = timezone(timedelta(hours=5))

URL_RE = re.compile(r"(https?://|www\.)\S+", re.I)
HASHTAG_RE = re.compile(r"^#[A-Za-z][A-Za-z0-9]{1,29}$")
# First-person experience claims we can't verify for Ali (opinions like "I'd" / "I think" stay allowed).
EXPERIENCE_RE = re.compile(
    r"\b(I've|I have (?:built|shipped|seen|worked|led|used|hit|run|spent|been)|I had|I built|I shipped|"
    r"I worked|I spent|I led|I once|I ran into|I hit|I learned|I learnt|my team|our team|we built|"
    r"we shipped|at my (?:last|previous|current|old) (?:job|company|role|team|employer)|"
    r"my (?:client|clients|employer|last project))\b",
    re.I,
)
STALE_RE = re.compile(r"\b(currently in (?:public |private )?beta|just (?:launched|released|shipped|announced)|"
                      r"brand[- ]new|this week|yesterday)\b", re.I)
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F02F\U0001F100-\U0001F1FF]"
)


def load_config() -> dict:
    return json.loads((ROOT / "config.json").read_text(encoding="utf-8"))


def today_pkt() -> str:
    return datetime.now(PKT).date().isoformat()


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))


def save_history(items: list[dict]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def post_dir(day: str) -> Path:
    return POSTS_DIR / day


def load_post(day: str) -> dict:
    return json.loads((post_dir(day) / "post.json").read_text(encoding="utf-8"))


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def build_commentary(post: dict) -> str:
    """Final text exactly as it will appear on LinkedIn (hashtags appended)."""
    return post["text"].rstrip() + "\n\n" + " ".join(post["hashtags"])


def style_warnings(post: dict, rules: dict) -> list[str]:
    """Non-blocking guidance: the post is still published, but the writer should aim for these."""
    text = post.get("text", "")
    warns = []
    n = len(text)
    if not rules["text_min_chars"] <= n <= rules["text_max_chars"]:
        warns.append(f"length {n} chars; aim for {rules['text_min_chars']}-{rules['text_max_chars']} (concise)")
    paras = [x for x in re.split(r"\n\s*\n", text.strip()) if x.strip()]
    if len(paras) > rules["max_paragraphs"]:
        warns.append(f"{len(paras)} paragraphs; aim for {rules['max_paragraphs']} or fewer")
    for x in paras:
        codeish = sum(1 for ln in x.splitlines() if re.search(r"[;{}()=<>]|^\s{2,}", ln)) >= 2
        if not codeish and len(x) > rules["paragraph_max_chars"]:
            warns.append(f"long paragraph ({len(x)} chars, aim <= {rules['paragraph_max_chars']}): '{x[:50]}...'")
        if codeish and len(x.splitlines()) > 8:
            warns.append("code block longer than 8 lines; keep only the lines that make the point")
    return warns


def validate_post(day: str, cfg: dict | None = None, history: list[dict] | None = None) -> list[str]:
    """Return a list of problems. Empty list = safe to publish."""
    cfg = cfg or load_config()
    rules = cfg["rules"]
    history = load_history() if history is None else history
    errors: list[str] = []
    folder = post_dir(day)

    try:
        post = load_post(day)
    except FileNotFoundError:
        return [f"posts/{day}/post.json not found"]
    except json.JSONDecodeError as e:
        return [f"post.json is not valid JSON: {e}"]

    for key in ("date", "category", "topic", "theme", "text", "hashtags", "image", "sources"):
        if key not in post:
            errors.append(f"missing field: {key}")
    if errors:
        return errors

    if post["date"] != day[:10]:
        errors.append(f"date field {post['date']} does not match folder {day}")

    cat = post["category"]
    if cat not in rules["categories"]:
        errors.append(f"unknown category '{cat}'")

    text: str = post["text"]
    hook = text.strip().split("\n", 1)[0]
    if len(hook) > rules["hook_max_chars"]:
        errors.append(f"first line (hook) is {len(hook)} chars; keep it <= {rules['hook_max_chars']}")

    if "#" in text:
        errors.append("put hashtags only in the 'hashtags' list, not inside text")

    urls = URL_RE.findall(text)
    if cat == "jobs":
        if len(urls) > 1:
            errors.append("job posts may contain at most one link")
    elif urls:
        errors.append("no links in the post text (hurts reach); keep sources in 'sources'")

    low = text.lower()
    for phrase in rules["banned_phrases"]:
        if phrase in low:
            errors.append(f"AI-sounding phrase not allowed: '{phrase}'")

    for m in EXPERIENCE_RE.finditer(text):
        errors.append(f"unverifiable first-person experience claim: '{m.group(0)}' (use advice/opinion instead)")
    if post.get("status_verified_today") is not True:
        for m in STALE_RE.finditer(text):
            errors.append(f"time-sensitive wording '{m.group(0)}': confirm on current official docs today and set "
                          f"\"status_verified_today\": true, or reword")

    emojis = len(EMOJI_RE.findall(text))
    if emojis > rules["max_emojis"]:
        errors.append(f"{emojis} emojis; max {rules['max_emojis']}")

    paragraphs = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    last = paragraphs[-1] if paragraphs else ""
    q = [s for s in re.split(r"(?<=[?])\s", last) if s.strip().endswith("?")]
    if not q or len(q[-1].split()) < 6:
        errors.append("last paragraph must ask readers a real question (6+ words) to invite comments")

    tags = post["hashtags"]
    if not isinstance(tags, list) or not rules["hashtags_min"] <= len(tags) <= rules["hashtags_max"]:
        errors.append(f"need {rules['hashtags_min']}-{rules['hashtags_max']} hashtags")
    else:
        for t in tags:
            if not HASHTAG_RE.match(t):
                errors.append(f"bad hashtag '{t}' (use #Word, letters/numbers only)")
        if len({t.lower() for t in tags}) != len(tags):
            errors.append("duplicate hashtags")

    if len(build_commentary(post)) > 3000:
        errors.append("text + hashtags exceed LinkedIn's 3000 character limit")

    sources = post["sources"]
    if not isinstance(sources, list):
        errors.append("sources must be a list of URLs")
    elif cat in rules["categories_needing_sources"] and not sources:
        errors.append(f"category '{cat}' is factual/news: add at least one source URL")

    img = post["image"]
    html = folder / img.get("file", "image.html")
    if not html.exists():
        errors.append(f"image file {html.name} not found")
    else:
        src = html.read_text(encoding="utf-8")
        brand = cfg["brand"]
        if brand["site"].lower() not in src.lower():
            errors.append(f"image must show {brand['site']}")
        if brand["name"].lower() not in src.lower():
            errors.append(f"image must show the name {brand['name']}")
        if re.search(r"<(script|link)[^>]+(src|href)=[\"']https?://", src, re.I) and "fonts.googleapis.com" not in src:
            errors.append("image.html may only load external Google Fonts (keep everything else inline)")
        # Brand kit: one recognisable look, no AI-style colour effects.
        if "design/brand.css" not in src:
            errors.append('image.html must use the brand kit: <link rel="stylesheet" href="../../design/brand.css">')
        if 'class="author"' not in src or "<footer" not in src:
            errors.append("image.html must keep the brand header (header.author) and footer, see design/examples/")
        if re.search(r"gradient\(|text-shadow|filter:\s*(drop-shadow|blur)|backdrop-filter|0 0 \d+px", src, re.I):
            errors.append("no gradients, glows, blurs or neon effects in the image (brand kit only)")
        if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", src):
            errors.append("no custom colours in image.html; use the brand variables (var(--accent) etc.) and classes")
    if post.get("theme") not in rules["themes"]:
        errors.append(f"theme must be one of {', '.join(rules['themes'])} (brand kit variants)")
    if post.get("scope") not in ("broad", "niche"):
        errors.append('add "scope": "broad" or "niche" (niche = one flag/option/minor feature)')
    elif post["scope"] == "niche":
        d0 = date.fromisoformat(day[:10])
        recent_niche = [h for h in history if h.get("scope") == "niche" and h.get("slot", h["date"]) != day
                        and 0 <= (d0 - date.fromisoformat(h["date"])).days <= 7]
        if len(recent_niche) >= rules["niche_max_per_7_days"]:
            errors.append("a niche topic was already posted in the last 7 days; pick a broad, widely relevant topic")
    vt = img.get("visual_type")
    if vt not in rules["visual_types"]:
        errors.append(f"image.visual_type must be one of {', '.join(rules['visual_types'])}")
    elif (vt == "animated-flow") != bool(img.get("animated")):
        errors.append("visual_type 'animated-flow' must have \"animated\": true, and only it may be animated")
    if not img.get("alt") or len(img["alt"]) < 20:
        errors.append("image.alt needs a real description (20+ chars) for accessibility")

    # Repetition checks against what was already published.
    d = date.fromisoformat(day[:10])
    topic_n, theme_n = _norm(post["topic"]), _norm(post["theme"])
    for h in history:
        if h.get("slot", h.get("date")) == day:
            continue
        age = (d - date.fromisoformat(h["date"])).days
        if 0 <= age <= rules["topic_repeat_days"] and _norm(h.get("topic", "")) == topic_n:
            errors.append(f"same topic already posted on {h['date']}")
        if rules["theme_repeat_days"] and 0 <= age <= rules["theme_repeat_days"] and _norm(h.get("theme", "")) == theme_n:
            errors.append(f"image theme '{post['theme']}' used on {h['date']}; pick a different look")
        if age == 1 and h.get("category") == cat and cat != "jobs":
            errors.append(f"category '{cat}' was also yesterday's; rotate topics")
    return errors
