"""Compact summary of recent posts, so the daily run doesn't need to read every file.

Usage: python scripts/recent.py [target-date]
"""
import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from common import POSTS_DIR, load_config, load_history, today_pkt

target = date.fromisoformat((sys.argv[1] if len(sys.argv) > 1 else today_pkt())[:10])
rules = load_config()["rules"]
items = {h.get("slot", h["date"]): h for h in load_history()}
for folder in sorted(POSTS_DIR.iterdir()):  # also include prepared, not yet published posts
    f = folder / "post.json"
    if f.exists() and folder.name not in items:
        p = json.loads(f.read_text(encoding="utf-8"))
        items[folder.name] = {"date": p["date"], "category": p["category"], "topic": p["topic"],
                              "theme": p["theme"], "pending": True}

window = rules["topic_repeat_days"]
recent = sorted((v for v in items.values()
                 if 0 <= (target - date.fromisoformat(v["date"])).days <= window), key=lambda v: v["date"])
print(f"Posts in the last {window} days (don't repeat topics; themes blocked for {rules['theme_repeat_days']} days):")
for v in recent:
    print(f"- {v['date']} | {v['category']} | theme: {v['theme']} | {v['topic']}{' (pending)' if v.get('pending') else ''}")

yday = (target - timedelta(days=1)).isoformat()
blocked = sorted({v["category"] for v in items.values() if v["date"] == yday})
last7 = Counter(v["category"] for v in items.values()
                if 0 < (target - date.fromisoformat(v["date"])).days <= 7)
unused = [c for c in rules["categories"] if c not in last7 and c not in blocked]
themes = sorted({v["theme"] for v in items.values()
                 if 0 <= (target - date.fromisoformat(v["date"])).days <= rules["theme_repeat_days"]})
print(f"\nNot allowed today (yesterday's category): {', '.join(blocked) or 'none'}")
print(f"Unused in the last 7 days (prefer these): {', '.join(unused)}")
if rules["theme_repeat_days"]:
    print(f"Themes you can't use: {', '.join(themes) or 'none'}")
niche = [v for v in items.values() if v.get("scope") == "niche" and 0 <= (target - date.fromisoformat(v["date"])).days <= 7]
print(f"Niche posts in the last 7 days: {len(niche)} (max {rules['niche_max_per_7_days']}; otherwise pick a broad topic)")
