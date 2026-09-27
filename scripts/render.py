"""Render posts/<date>/image.html to image.png (or image.gif when animated).

Usage: python scripts/render.py 2026-09-28
"""
from __future__ import annotations

import io
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

from common import load_config, load_post, post_dir

# Pause every CSS/Web animation and SVG SMIL clock, then jump all of them to time t (ms).
SEEK_JS = """
(t) => {
  for (const a of document.getAnimations()) { a.pause(); a.currentTime = t; }
  for (const s of document.querySelectorAll('svg')) {
    if (s.pauseAnimations) { s.pauseAnimations(); s.setCurrentTime(t / 1000); }
  }
}
"""


def seek_all(page, t_ms: float) -> None:
    page.evaluate(SEEK_JS, t_ms)


# Finds text that overlaps other text or spills outside the canvas.
LAYOUT_JS = """
() => {
  const W = innerWidth, H = innerHeight, boxes = [], problems = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode, el = n.parentElement;
    if (!n.textContent.trim() || !el) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.05) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) {
      if (b.width < 2 || b.height < 2) continue;
      boxes.push({t: n.textContent.trim().slice(0, 40), el, l: b.left, r: b.right, top: b.top, bot: b.bottom});
    }
  }
  for (const b of boxes) {
    if (b.l < 0 || b.top < 0 || b.r > W + 1 || b.bot > H + 1) problems.push(`text off canvas: "${b.t}"`);
  }
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const a = boxes[i], b = boxes[j];
    if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el)) continue;
    const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l), oy = Math.min(a.bot, b.bot) - Math.max(a.top, b.top);
    if (ox > 4 && oy > 4) problems.push(`text overlaps: "${a.t}" / "${b.t}"`);
  }
  return [...new Set(problems)];
}
"""


def check_layout(page) -> list[str]:
    return page.evaluate(LAYOUT_JS)


class LayoutError(Exception):
    pass


def render(day: str) -> str:
    cfg = load_config()["image"]
    post = load_post(day)
    img = post["image"]
    folder = post_dir(day)
    html = (folder / img.get("file", "image.html")).resolve()
    animated = bool(img.get("animated"))

    w, h = (cfg["gif_width"], cfg["gif_height"]) if animated else (cfg["width"], cfg["height"])
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        page.goto(html.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(400)

        if not animated:
            problems = check_layout(page)
            if problems:
                browser.close()
                raise LayoutError("image layout problems:\n  - " + "\n  - ".join(problems))
            out = folder / "image.png"
            page.screenshot(path=str(out), full_page=False)
            browser.close()
            return str(out)

        duration = int(img.get("duration_ms", 4000))
        n = int(img.get("frames", cfg["gif_frames"]))
        frames, problems = [], set()
        for i in range(n):
            seek_all(page, duration * i / n)
            page.wait_for_timeout(30)
            if i % 4 == 0:
                problems.update(check_layout(page))
            frames.append(Image.open(io.BytesIO(page.screenshot())).convert("RGB"))
        browser.close()
        if problems:
            raise LayoutError("image layout problems:\n  - " + "\n  - ".join(sorted(problems)))

    out = folder / "image.gif"
    colors = 256
    while True:
        # One shared palette for all frames: smaller file and no colour flicker.
        base = frames[0].quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
        pal = [base] + [f.quantize(palette=base, dither=Image.Dither.NONE) for f in frames[1:]]
        buf = io.BytesIO()
        pal[0].save(buf, format="GIF", save_all=True, append_images=pal[1:],
                    duration=max(40, duration // n), loop=0, optimize=True, disposal=1)
        if buf.tell() <= cfg["gif_max_bytes"] or colors <= 32:
            break
        colors //= 2
    out.write_bytes(buf.getvalue())
    return str(out)


if __name__ == "__main__":
    print(render(sys.argv[1]))
