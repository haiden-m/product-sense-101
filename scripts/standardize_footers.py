#!/usr/bin/env python3
"""Standardize lesson-footer across day01–day30.html."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Next lesson targets from index.html (day N → link, label)
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

FOOTER_CSS = """
  /* — Footer — */
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
    font-size: 0.8rem;
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


def footer_html(day: int) -> str:
    href, label = NEXT[day]
    if day == 30:
        left = "Day 30 complete — course complete"
        right = f'<a href="{href}">{label}</a>'
    else:
        left = f"Day {day} complete"
        right = f'<a href="{href}">Next lesson → {label}</a>'
    return (
        "  <!-- Footer -->\n"
        "  <div class=\"lesson-footer\">\n"
        f"    <div class=\"footer-left\">{left}</div>\n"
        f"    <div class=\"footer-next\">{right}</div>\n"
        "  </div>"
    )


def strip_footer_css(text: str) -> str:
    """Remove legacy footer rules and any existing lesson-footer block."""
    text = re.sub(
        r"/\*[^\n]*Footer[^\n]*\*/\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    # Multi-line .lesson-footer block through .footer-next a:hover
    text = re.sub(
        r"\.lesson-footer\s*\{[^}]*\}\s*"
        r"(?:\.footer-left\s*\{[^}]*\}\s*)?"
        r"(?:\.footer-next\s*\{[^}]*\}\s*)?"
        r"(?:\.footer-next a\s*\{[^}]*\}\s*)?"
        r"(?:\.footer-next a:hover\s*\{[^}]*\}\s*)?",
        "",
        text,
        flags=re.DOTALL,
    )
    # footer { ... } and footer .child rules
    while True:
        new = re.sub(r"footer\s*\.[\w-]+\s*\{[^}]*\}\s*", "", text)
        new = re.sub(r"footer\s*\{[^}]*\}\s*", "", new)
        if new == text:
            break
        text = new
    text = re.sub(r"\.foot-note\s*\{[^}]*\}\s*", "", text)
    text = re.sub(r"\.foot-brand\s*\{[^}]*\}\s*", "", text)
    text = re.sub(r"\.foot-brand\s+strong\s*\{[^}]*\}\s*", "", text)
    # media queries that only tweak footer padding
    text = re.sub(
        r"@media[^{]+\{[^}]*footer\s*\{[^}]*\}[^}]*\}",
        "",
        text,
        flags=re.DOTALL,
    )
    return text


def insert_footer_css(text: str) -> str:
    if ".lesson-footer" in text:
        return text
    return text.replace("</style>", FOOTER_CSS + "\n</style>", 1)


def replace_footer_html(text: str, day: int) -> str:
    block = footer_html(day)
    # Existing lesson-footer
    if re.search(r'<div class="lesson-footer">', text):
        text = re.sub(
            r"<!-- Footer -->\s*<div class=\"lesson-footer\">[\s\S]*?</div>",
            block.strip(),
            text,
            count=1,
        )
        # fallback without comment
        text = re.sub(
            r"<div class=\"lesson-footer\">[\s\S]*?</div>\s*(?=</div>\s*\n<script)",
            block.strip() + "\n",
            text,
            count=1,
        )
        return text

    # <footer>...</footer> inside wrap (day 5–27, 9)
    if re.search(r"<footer>", text):
        text = re.sub(r"\s*<footer>[\s\S]*?</footer>", "\n\n" + block + "\n", text, count=1)
        return text

    # day 6–8: footer after closing wrap — move inside
    m = re.search(
        r"(</div>\s*\n)(<footer>[\s\S]*?</footer>)",
        text,
    )
    if m:
        text = text[: m.start(1)] + "\n\n" + block + "\n" + m.group(1) + text[m.end(2) :]
        return text

    raise RuntimeError("Could not locate footer to replace")


def process(path: Path, day: int) -> None:
    text = path.read_text(encoding="utf-8")
    text = strip_footer_css(text)
    text = insert_footer_css(text)
    text = replace_footer_html(text, day)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for day in range(1, 31):
        path = ROOT / f"day{day:02d}.html"
        process(path, day)
        print(f"OK {path.name}")


if __name__ == "__main__":
    main()
