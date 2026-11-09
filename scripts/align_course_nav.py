#!/usr/bin/env python3
"""Align course-home nav with index.html margins (900px + 20px padding)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_HTML = (
    '<nav class="course-nav" aria-label="Course">'
    '<a class="course-home" href="index.html">← Course home</a>'
    "</nav>\n\n"
)

NAV_RE = re.compile(
    r"\s*<nav class=\"course-nav\"[^>]*>.*?</nav>\s*",
    re.DOTALL,
)

COURSE_NAV_CSS = """  .course-nav {
    width: 100%;
    max-width: 900px;
    margin: 0 auto 1.25rem;
    padding: calc(40px + env(safe-area-inset-top, 0px)) 20px 0;
    box-sizing: border-box;
  }"""

COURSE_NAV_CSS_RE = re.compile(r"\.course-nav\s*\{[^}]*\}", re.DOTALL)

INSERT_BEFORE_RE = re.compile(
    r"<div class=\"page\">|<div class=\"wrap\">|<header class=\"top\">",
)


def move_and_style(text: str) -> str:
    text = NAV_RE.sub("\n", text, count=1)
    if 'class="course-nav"' in text:
        # remove any duplicate nav left inside containers
        text = NAV_RE.sub("\n", text)

    m = INSERT_BEFORE_RE.search(text)
    if not m:
        raise RuntimeError("No insertion point for course nav")
    if text[max(0, m.start() - 200) : m.start()].find("course-nav") == -1:
        text = text[: m.start()] + NAV_HTML + text[m.start() :]

    text = COURSE_NAV_CSS_RE.sub(COURSE_NAV_CSS, text, count=1)
    return text


def main() -> None:
    for day in range(1, 31):
        path = ROOT / f"day{day:02d}.html"
        text = path.read_text(encoding="utf-8")
        text = move_and_style(text)
        path.write_text(text, encoding="utf-8")
        print(f"OK {path.name}")


if __name__ == "__main__":
    main()
