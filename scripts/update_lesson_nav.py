#!/usr/bin/env python3
"""Fix footer CSS placement, add course home nav + footer home link on all lessons."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEXT: dict[int, tuple[str, str]] = {
    1: ("day02.html", "First Principles Thinking"),
    2: ("day03.html", "Jobs-to-be-Done"),
    3: ("day04.html", "Customer Segmentation &amp; ICPs"),
    4: ("day05.html", "Problem Space vs Solution Space"),
    5: ("day06.html", "Porter's Five Forces for SaaS"),
    6: ("day07.html", "Competitive Moats"),
    7: ("day08.html", "Market Sizing (TAM/SAM/SOM)"),
    8: ("day09.html", "Platform Thinking &amp; Network Effects"),
    9: ("day10.html", "Product&ndash;Market Fit"),
    10: ("day11.html", "RICE, ICE &amp; MoSCoW"),
    11: ("day12.html", "Opportunity Sizing &amp; Cost of Delay"),
    12: ("day13.html", "The Kano Model"),
    13: ("day14.html", "One-Way vs Two-Way Doors"),
    14: ("day15.html", "Technical Debt as Product Strategy"),
    15: ("day16.html", "Product Critique"),
    16: ("day17.html", "UX Principles for PMs"),
    17: ("day18.html", "Data-Informed vs Data-Driven"),
    18: ("day19.html", "North Star Metrics"),
    19: ("day20.html", "The Art of Saying No"),
    20: ("day21.html", "The Pyramid Principle"),
    21: ("day22.html", "Asking Sharper Questions"),
    22: ("day23.html", "Stakeholder Management"),
    23: ("day24.html", "Writing Crisp PRDs"),
    24: ("day25.html", "Presenting Roadmaps"),
    25: ("day26.html", "Growth Loops &amp; Retention"),
    26: ("day27.html", "B2B SaaS Pricing Strategy"),
    27: ("day28.html", "API &amp; Platform PM"),
    28: ("day29.html", "AI-Era Product Thinking"),
    29: ("day30.html", "The Decision Spine (Capstone)"),
    30: ("index.html", "Back to course home"),
}

NAV_FOOTER_CSS = """
  /* — Course nav & footer — */
  .course-nav {
    width: 100%;
    max-width: 900px;
    margin: 0 auto 1.25rem;
    padding: calc(40px + env(safe-area-inset-top, 0px)) 20px 0;
    box-sizing: border-box;
  }
  .course-home,
  .footer-home {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--teal);
    text-decoration: none;
  }
  .course-home:hover,
  .footer-home:hover {
    text-decoration: underline;
  }
  .lesson-footer {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--chalk);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .footer-left {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem 1rem;
    font-size: 0.8rem;
    color: var(--stone);
  }
  .footer-day {
    color: var(--stone);
  }
  .footer-next {
    margin-left: auto;
    text-align: right;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--teal);
  }
  .footer-next a {
    color: inherit;
    font-weight: inherit;
    text-decoration: none;
  }
  .footer-next a:hover {
    text-decoration: underline;
  }
"""

NAV_HTML = (
    '  <nav class="course-nav" aria-label="Course">'
    '<a class="course-home" href="index.html">← Course home</a>'
    "</nav>\n\n"
)

FOOTER_BLOCK_RE = re.compile(
    r"\s*/\* — (?:Footer|Course nav & footer) — \*/\s*"
    r"(?:\.course-nav\s*\{[^}]*\}\s*)?"
    r"(?:\.course-home[^{]*\{[^}]*\}\s*)?"
    r"(?:\.footer-home[^{]*\{[^}]*\}\s*)?"
    r"\.lesson-footer\s*\{[^}]*\}\s*"
    r"(?:\.footer-left\s*\{[^}]*\}\s*)?"
    r"(?:\.footer-day\s*\{[^}]*\}\s*)?"
    r"\.footer-next\s*\{[^}]*\}\s*"
    r"(?:\.footer-next a\s*\{[^}]*\}\s*)?"
    r"(?:\.footer-next a:hover\s*\{[^}]*\}\s*)?",
    re.DOTALL,
)

WRAPPER_FOOTER_RE = re.compile(
    r"(\s*/\* — (?:Footer|Course nav & footer) — \*/\s*"
    r"\.lesson-footer\s*\{[^}]*\}\s*"
    r"(?:\.footer-left\s*\{[^}]*\}\s*)?"
    r"\.footer-next\s*\{[^}]*\}\s*"
    r"(?:\.footer-next a\s*\{[^}]*\}\s*)?"
    r"(?:\.footer-next a:hover\s*\{[^}]*\}\s*)?)",
    re.DOTALL,
)


def strip_wrapper_css(text: str) -> str:
    first_end = text.find("</style>")
    if first_end == -1 or ".lesson-footer" not in text[: first_end + 8]:
        return text
    return WRAPPER_FOOTER_RE.sub("", text, count=1)


def main_style_insert_at(text: str) -> int:
    m = re.search(r'<div class="(?:page|wrap)">|<header class="top">', text)
    if not m:
        return text.rfind("</style>")
    return text.rfind("</style>", 0, m.start())


def upsert_css(text: str) -> str:
    text = FOOTER_BLOCK_RE.sub("", text)
    pos = main_style_insert_at(text)
    if pos == -1:
        return text
    snippet = text[max(0, pos - 2500) : pos]
    if ".lesson-footer" in snippet and ".course-nav" in snippet:
        return text
    return text[:pos] + NAV_FOOTER_CSS + "\n" + text[pos:]


def add_top_nav(text: str) -> str:
    if 'class="course-nav"' in text:
        return text
    return re.sub(
        r"(<div class=\"(?:page|wrap)\">)\s*\n?",
        r"\1\n" + NAV_HTML,
        text,
        count=1,
    )


def footer_html(day: int) -> str:
    href, label = NEXT[day]
    if day == 30:
        day_note = "Day 30 complete — course complete"
        right = f'<a href="{href}">{label}</a>'
    else:
        day_note = f"Day {day} complete"
        right = f'<a href="{href}">Next lesson → {label}</a>'
    return (
        "  <!-- Footer -->\n"
        "  <div class=\"lesson-footer\">\n"
        "    <div class=\"footer-left\">\n"
        '      <a class="footer-home" href="index.html">← Course home</a>\n'
        f'      <span class="footer-day">{day_note}</span>\n'
        "    </div>\n"
        f'    <div class="footer-next">{right}</div>\n'
        "  </div>"
    )


def upsert_footer(text: str, day: int) -> str:
    block = footer_html(day)
    text = re.sub(r"<!-- Footer -->\s*<!-- Footer -->\s*", "<!-- Footer -->\n  ", text)
    if re.search(r'<div class="lesson-footer">', text):
        text = re.sub(
            r"<!-- Footer -->\s*<div class=\"lesson-footer\">[\s\S]*?</div>",
            block,
            text,
            count=1,
        )
        text = re.sub(
            r"<div class=\"lesson-footer\">[\s\S]*?</div>\s*(?=</div>\s*\n<script)",
            block.strip() + "\n",
            text,
            count=1,
        )
    return text


def process(day: int) -> None:
    path = ROOT / f"day{day:02d}.html"
    text = path.read_text(encoding="utf-8")
    text = strip_wrapper_css(text)
    text = upsert_css(text)
    text = add_top_nav(text)
    text = upsert_footer(text, day)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for day in range(1, 31):
        process(day)
        print(f"OK day{day:02d}.html")


if __name__ == "__main__":
    main()
