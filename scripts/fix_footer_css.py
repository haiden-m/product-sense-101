#!/usr/bin/env python3
"""Move lesson-footer CSS from Vercel wrapper into each lesson's main <style>."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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

WRAPPER_FOOTER_RE = re.compile(
    r"(<style>:root\{color-scheme:light[^<]*?</style>)",
    re.DOTALL,
)

# Wrong insertion: footer rules inside first mini style block after <body> line 1
MINI_STYLE_FOOTER_RE = re.compile(
    r"(<style>:root\{color-scheme:light[^"]*?\})\s*"
    r"/\* — Footer — \*/\s*"
    r"\.lesson-footer\s*\{[^}]*\}\s*"
    r"\.footer-left\s*\{[^}]*\}\s*"
    r"\.footer-next\s*\{[^}]*\}\s*"
    r"\.footer-next a\s*\{[^}]*\}\s*"
    r"\.footer-next a:hover\s*\{[^}]*\}\s*"
    r"</style>",
    re.DOTALL,
)


def remove_wrapper_footer(text: str) -> str:
    """Strip footer CSS accidentally added to the first-line wrapper <style>."""
    def repl(m: re.Match[str]) -> str:
        block = m.group(0)
        if ".lesson-footer" not in block:
            return block
        # Keep only the one-line/minimal wrapper rules up to img rule
        start = block.find("<style>")
        inner = block[start + 7 : block.rfind("</style>")]
        # Remove footer section from inner
        inner = re.sub(
            r"\s*/\* — Footer — \*/\s*"
            r"\.lesson-footer\s*\{[^}]*\}\s*"
            r"\.footer-left\s*\{[^}]*\}\s*"
            r"\.footer-next\s*\{[^}]*\}\s*"
            r"\.footer-next a\s*\{[^}]*\}\s*"
            r"\.footer-next a:hover\s*\{[^}]*\}\s*",
            "",
            inner,
            flags=re.DOTALL,
        )
        return f"<style>{inner}</style>"

    # First </style> in file is the wrapper
    idx = text.find("</style>")
    if idx == -1:
        return text
    # Only patch if lesson-footer appears before first </style>
    head = text[: idx + len("</style>")]
    if ".lesson-footer" not in head:
        return text
    head = repl(head)
    return head + text[idx + len("</style>") :]


def ensure_main_footer_css(text: str) -> str:
    if re.search(r"(?<!</style>.*)\.lesson-footer", text):
        # Check if main block has lesson-footer (not only in wrapper)
        pass
    # Count .lesson-footer occurrences
    if len(re.findall(r"\.lesson-footer\s*\{", text)) >= 2:
        text = remove_wrapper_footer(text)

    if re.search(r"<style>[\s\S]*\.lesson-footer", text):
        # Might only be wrapper — find main style: second <style> or large block
        styles = list(re.finditer(r"<style>", text))
        if len(styles) < 2:
            # single main style in body
            if ".lesson-footer" in text.split("</style>", 1)[-1]:
                return text
        main_start = styles[1].start() if len(styles) > 1 else styles[0].start()
        main_end = text.find("</style>", main_start)
        main_block = text[main_start:main_end]
        if ".lesson-footer" in main_block:
            return remove_wrapper_footer(text)

    # Insert before last </style> before <div class="page"> or wrap
    anchor = re.search(r"<div class=\"(?:page|wrap)\">", text)
    if not anchor:
        return text
    before = text[: anchor.start()]
    last_style_end = before.rfind("</style>")
    if last_style_end == -1:
        return text
    text = (
        text[:last_style_end]
        + FOOTER_CSS
        + "\n"
        + text[last_style_end:]
    )
    return remove_wrapper_footer(text)


def cleanup_orphans(text: str) -> str:
    text = re.sub(r"footer\s*\.next\s+strong\s*\{[^}]*\}\s*", "", text)
    return text


def main() -> None:
    for day in range(1, 31):
        path = ROOT / f"day{day:02d}.html"
        text = path.read_text(encoding="utf-8")
        text = ensure_main_footer_css(text)
        text = cleanup_orphans(text)
        path.write_text(text, encoding="utf-8")
        n = len(re.findall(r"\.lesson-footer\s*\{", text))
        print(f"{path.name}: {n} footer rule block(s)")


if __name__ == "__main__":
    main()
