"""Check a post against the safety/quality rules.

Usage: python scripts/validate.py 2026-09-28   (exit code 1 if anything fails)
"""
import sys

from common import build_commentary, load_post, validate_post

if __name__ == "__main__":
    day = sys.argv[1]
    problems = validate_post(day)
    if problems:
        print(f"FAILED posts/{day}:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    text = build_commentary(load_post(day))
    print(f"OK posts/{day}  ({len(text)} chars)\n" + "-" * 60 + f"\n{text}\n" + "-" * 60)
