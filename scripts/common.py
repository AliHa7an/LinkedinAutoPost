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

    if post["date"] != day:
        errors.append(f"date field {post['date']} does not match folder {day}")

    cat = post["category"]
    if cat not in rules["categories"]:
        errors.append(f"unknown category '{cat}'")

    text: str = post["text"]
    n = len(text)
    if not rules["text_min_chars"] <= n <= rules["text_max_chars"]:
        errors.append(f"text length {n} outside {rules['text_min_chars']}-{rules['text_max_chars']}")

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
    if not img.get("alt") or len(img["alt"]) < 20:
        errors.append("image.alt needs a real description (20+ chars) for accessibility")

    # Repetition checks against what was already published.
    d = date.fromisoformat(day)
    topic_n, theme_n = _norm(post["topic"]), _norm(post["theme"])
    for h in history:
        if h.get("date") == day:
            continue
        age = (d - date.fromisoformat(h["date"])).days
        if 0 < age <= rules["topic_repeat_days"] and _norm(h.get("topic", "")) == topic_n:
            errors.append(f"same topic already posted on {h['date']}")
        if 0 < age <= rules["theme_repeat_days"] and _norm(h.get("theme", "")) == theme_n:
            errors.append(f"image theme '{post['theme']}' used on {h['date']}; pick a different look")
        if age == 1 and h.get("category") == cat and cat != "jobs":
            errors.append(f"category '{cat}' was also yesterday's; rotate topics")
    return errors
