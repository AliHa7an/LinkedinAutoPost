"""Publish today's post (image + text) to Ali Hassan's personal LinkedIn profile.

Safety guarantees:
  * posts at most once per day (checks data/history.json)
  * refuses anything that fails validate_post()
  * only uses the w_member_social permission: it can create a post, nothing else
    (no likes, comments, connection requests or messages)

Usage:
  python scripts/post.py                 # today's post (PKT date)
  python scripts/post.py --date 2026-09-28
  python scripts/post.py --dry-run       # everything except publishing
Env:
  LINKEDIN_ACCESS_TOKEN   required unless --dry-run
  WAIT_FOR_POST_TIME=1    sleep until schedule.post_time_utc before publishing
  GITHUB_OUTPUT           (set by Actions) receives status / post_url
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

from common import (build_commentary, load_config, load_history, load_post, post_dir,
                    save_history, today_pkt, validate_post)
from render import render

API = "https://api.linkedin.com"
# Characters LinkedIn's "little text" format treats as markup. '#' is left alone so hashtags work.
RESERVED = set("\\|{}@[]()<>*_~")


class TokenExpired(Exception):
    pass


def output(**kw) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    for k, v in kw.items():
        print(f"{k}={v}")
        if path:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"{k}={v}\n")


def escape_little_text(s: str) -> str:
    return "".join("\\" + c if c in RESERVED else c for c in s)


def version_candidates(start: str, count: int = 8):
    y, m = int(start[:4]), int(start[4:])
    for _ in range(count):
        yield f"{y}{m:02d}"
        m -= 1
        if m == 0:
            y, m = y - 1, 12


class LinkedIn:
    def __init__(self, token: str, version: str):
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Bearer {token}"})
        self.version = version

    def _check(self, r: requests.Response, what: str) -> None:
        if r.status_code == 401:
            raise TokenExpired(f"{what}: 401 Unauthorized, the LinkedIn token is expired or revoked")
        if r.status_code >= 400:
            raise RuntimeError(f"{what} failed: HTTP {r.status_code} {r.text[:500]}")

    def rest(self, method: str, path: str, **kw) -> requests.Response:
        """Call a versioned /rest endpoint, stepping back a month if LinkedIn retired the version."""
        last = None
        for v in version_candidates(self.version):
            headers = {"LinkedIn-Version": v, "X-Restli-Protocol-Version": "2.0.0",
                       "Content-Type": "application/json"}
            r = self.s.request(method, API + path, headers=headers, timeout=60, **kw)
            body = r.text.upper()
            if r.status_code in (400, 426) and ("VERSION" in body and ("NONEXISTENT" in body or "NOT ACTIVE" in body or "DEPRECATED" in body)):
                last = r
                continue
            if v != self.version:
                print(f"note: LinkedIn-Version {self.version} is retired, used {v}. Update config.json.")
                self.version = v
            return r
        return last

    def person_urn(self) -> str:
        r = self.s.get(API + "/v2/userinfo", timeout=30)
        self._check(r, "userinfo")
        return f"urn:li:person:{r.json()['sub']}"

    def upload_image(self, owner: str, file: Path) -> str:
        r = self.rest("POST", "/rest/images?action=initializeUpload",
                      json={"initializeUploadRequest": {"owner": owner}})
        self._check(r, "image initializeUpload")
        v = r.json()["value"]
        with open(file, "rb") as f:
            up = self.s.put(v["uploadUrl"], data=f, timeout=180,
                            headers={"Content-Type": "application/octet-stream"})
        self._check(up, "image upload")
        return v["image"]

    def create_post(self, author: str, text: str, image_urn: str, alt: str, title: str) -> str:
        body = {
            "author": author,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                             "thirdPartyDistributionChannels": []},
            "content": {"media": {"id": image_urn, "altText": alt[:4086], "title": title[:200]}},
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        r = self.rest("POST", "/rest/posts", json=body)
        self._check(r, "create post")
        return r.headers.get("x-restli-id") or r.headers.get("x-linkedin-id") or ""


def wait_until(hhmm_utc: str, max_wait_s: int = 45 * 60) -> None:
    hh, mm = map(int, hhmm_utc.split(":"))
    now = datetime.now(timezone.utc)
    target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    delay = (target - now).total_seconds()
    if 0 < delay <= max_wait_s:
        print(f"waiting {int(delay)}s until {hhmm_utc} UTC (3:00 PM PKT)...")
        time.sleep(delay)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=today_pkt())
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    day = args.date
    cfg = load_config()
    history = load_history()

    if any(h["date"] == day for h in history):
        print(f"already posted for {day}; nothing to do (max 1 post per day)")
        output(status="already_posted")
        return 0
    if not (post_dir(day) / "post.json").exists():
        print(f"::warning::no post prepared for {day}; skipping today")
        output(status="missing")
        return 0

    problems = validate_post(day, cfg, history)
    if problems:
        print(f"::error::post for {day} failed checks, NOT publishing:")
        for p in problems:
            print(f"  - {p}")
        output(status="invalid")
        return 1

    post = load_post(day)
    image = Path(render(day))
    text = escape_little_text(build_commentary(post))
    print(f"rendered {image.name} ({image.stat().st_size // 1024} KB), text {len(text)} chars")

    if args.dry_run:
        print("dry run: validation and rendering passed, nothing published")
        output(status="dry_run")
        return 0

    token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    if not token:
        print("::error::LINKEDIN_ACCESS_TOKEN secret is missing")
        output(status="no_token")
        return 1

    if os.environ.get("WAIT_FOR_POST_TIME") == "1":
        wait_until(cfg["schedule"]["post_time_utc"])

    li = LinkedIn(token, cfg["linkedin"]["api_version"])
    try:
        me = li.person_urn()
        image_urn = li.upload_image(me, image)
        urn = li.create_post(me, text, image_urn, post["image"]["alt"], post["topic"])
    except TokenExpired as e:
        print(f"::error::{e}")
        output(status="token_expired")
        return 1

    url = f"https://www.linkedin.com/feed/update/{urn}/" if urn else ""
    history.append({"date": day, "category": post["category"], "topic": post["topic"],
                    "theme": post["theme"], "urn": urn, "url": url,
                    "posted_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    save_history(history)
    print(f"published: {url or urn}")
    output(status="posted", post_url=url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
