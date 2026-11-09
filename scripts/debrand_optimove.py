#!/usr/bin/env python3
"""Remove Optimove-specific names from lesson HTML (source files)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters: longer / more specific phrases first.
REPLACEMENTS: list[tuple[str, str]] = [
    ("Optimove-style platform, ", "Your B2B CRM marketing platform, "),
    ("(Optimove-style)", ""),
    ("Optimove-style", "B2B CRM marketing"),
    ("(think: Optimove's category) ", ""),
    ("Optimove's connector and partner ecosystem", "A connector and partner ecosystem"),
    ("Consider Optimove's integrations layer", "Consider a CRM marketing platform's integrations layer"),
    ("plus AI capabilities like OptiGenie that recommend next-best-actions", "plus built-in AI that recommends next-best-actions"),
    ("makes Optimove more valuable", "makes the platform more valuable"),
    ("adopts Optimove makes", "adopts the platform makes"),
    ("runs through Optimove generates", "runs through the platform generates"),
    ("without Optimove building", "without your team building"),
    ("Optimove leadership", "Your leadership team"),
    ("you (Optimove) build", "your team builds"),
    (
        "If Optimove's core platform doesn't yet have strong, sticky usage among brands",
        "If your core platform doesn't yet have strong, sticky usage among customers",
    ),
    ("Optimove has PMF", "One CRM platform has PMF"),
    (
        'Do we have PMF on Overlay yet? Marketing wants to put it in the keynote next quarter."',
        'Do we have PMF on the add-on yet? Marketing wants to put it in the keynote next quarter."',
    ),
    (
        'new "Overlay"-style real-time personalization layer sold as an add-on to existing CRM customers',
        "real-time personalization add-on sold to existing CRM customers",
    ),
    (
        "mid-market iGaming operator who wants bonus-engine orchestration first and lifecycle second",
        "mid-market subscription business that wants onboarding automation first and lifecycle orchestration second",
    ),
    ("mid-market iGaming operators", "mid-market businesses in a new vertical"),
    ("mid-market iGaming", "mid-market subscription businesses"),
    ("Optimove", "the platform"),
    ("OptiGenie", "built-in AI recommendations"),
]


def scrub(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # tidy spacing from removed parentheticals
    text = text.replace("A CRM marketing platform  ", "A B2B CRM marketing platform ")
    text = text.replace("A CRM marketing platform is", "A B2B CRM marketing platform is")
    return text


def main() -> None:
    hits = 0
    for path in sorted(ROOT.glob("day*.html")):
        if "dist" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = scrub(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            hits += 1
        left = updated.lower().count("optimove") + updated.lower().count("optigenie")
        if left:
            print(f"WARN {path.name}: {left} brand mentions remain")

    # index / other
    for name in ("index.html",):
        path = ROOT / name
        if path.exists():
            original = path.read_text(encoding="utf-8")
            updated = scrub(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")

    print(f"Updated {hits} lesson file(s)")


if __name__ == "__main__":
    main()
