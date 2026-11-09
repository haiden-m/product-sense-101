#!/usr/bin/env python3
"""
Pull back CRM/marketing as the default lens without flattening scenarios.

Rule of thumb: name the product category once per example block; prefer
"your product" / "B2B SaaS" for framing; keep numbers, trade-offs, and jobs.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Applied to every lesson source file (not dist).
GLOBAL: list[tuple[str, str]] = [
    ("B2B CRM marketing platform", "B2B SaaS product"),
    ("Your B2B CRM marketing platform", "Your product team"),
    ("A B2B CRM marketing platform", "A growth-stage B2B SaaS company"),
    ("CRM marketing platform", "B2B SaaS product"),
    ("CRM platform", "B2B platform"),
    ("CRM/marketing-automation platforms", "B2B workflow-software market"),
    ("AI in marketing", "AI-assisted productivity"),
    ("CRM and marketing platforms", "B2B products with deep daily workflows"),
    ("In a CRM marketing platform,", "In complex B2B products,"),
]

# File-specific surgical edits (longer phrases first within each file).
PER_FILE: dict[str, list[tuple[str, str]]] = {
    "day01.html": [
        (
            "the <em>user</em> (the marketing manager working in the platform daily)",
            "the <em>user</em> (the practitioner working in the product daily)",
        ),
    ],
    "day06.html": [
        (
            '"AI writes your campaign copy"',
            '"AI drafts customer-facing content"',
        ),
        (
            '"one-click AI-personalized campaigns, at a third of your price, live in a week."',
            '"one-click automated workflows, at a third of your price, live in a week."',
        ),
        (
            "A marketing team using a spreadsheet, a generic email tool, and a BI dashboard stitched together instead of buying a CRM platform at all",
            "A team using a spreadsheet, a generic point tool, and a BI dashboard stitched together instead of buying your platform at all",
        ),
        ("Spreadsheets are a substitute for a CRM platform", "Spreadsheets are a substitute for the platform"),
    ],
    "day07.html": [
        (
            "for a B2B CRM marketing platform?",
            "for a B2B SaaS product with years of customer-specific configuration?",
        ),
        (
            "segmentation logic, journey builders, and BI integrations",
            "saved rules, automations, and BI integrations",
        ),
    ],
    "day08.html": [
        (
            "Sizing an AI message-generation add-on for CRM marketing",
            "Sizing an AI drafting add-on for a B2B workflow product",
        ),
        (
            "AI-assisted campaign-copy generator as a paid add-on to the core CRM marketing platform",
            "AI-assisted first-draft generator as a paid add-on to your core product",
        ),
        (
            "entering the gaming industry as a new vertical for your CRM marketing platform. He's seen a report saying \"player retention and CRM tools for gaming is a $6B market\"",
            "entering healthcare operations as a new vertical. He's seen a report saying \"operations software for mid-market healthcare is a $6B market\"",
        ),
    ],
    "day09.html": [
        ("<span class=\"ex-tag\">B2B SaaS / CRM Marketing</span>", "<span class=\"ex-tag\">B2B SaaS / Integrations</span>"),
        (
            "Consider a CRM marketing platform's integrations layer: connectors to ESPs, SMS gateways, push providers, and first-party data warehouses",
            "Consider a B2B platform's integrations layer: connectors to payment systems, identity providers, data warehouses, and communication channels",
        ),
        (
            "custom personalization algorithms and analytics widgets",
            "custom analytics modules and workflow widgets",
        ),
    ],
    "day10.html": [
        (
            "One CRM platform has PMF with enterprise retail CRM teams running lifecycle campaigns across channels.",
            "One product has PMF with enterprise retail ops teams running coordinated multi-channel programs.",
        ),
        (
            'ships a new "Predictive Journey Builder" module',
            'ships a new "Workflow Automation" module',
        ),
        (
            'if you could no longer use Predictive Journey Builder?',
            "if you could no longer use Workflow Automation?",
        ),
        (
            "real-time personalization add-on sold to existing CRM customers",
            "real-time insights add-on sold to existing customers",
        ),
        (
            "Marketing wants to put it in the keynote",
            "GTM wants to put it in the keynote",
        ),
        (
            "(e.g., enterprise retail CRM)",
            "(e.g., enterprise retail)",
        ),
        ("A CRM platform has strong PMF", "The product has strong PMF"),
    ],
    "day11.html": [
        ('unproven "AI Journey Orchestrator"', 'unproven "AI Workflow Orchestrator"'),
    ],
    "day12.html": [
        (
            "<b>Smart Send-Time Optimization</b> &#8212; a steady improvement worth roughly $25K/week in ongoing uplift once live, no deadline attached &#8212; and an <b>ESP migration</b>, forced because the long-deprecated email service provider your outbound campaigns run on is sunsetting its API in 12 weeks. After that date, every customer's outbound email campaigns stop sending, full stop.",
            "<b>Model accuracy improvements</b> &#8212; steady uplift worth roughly $25K/week once live, no hard deadline &#8212; and a <b>payment-provider API migration</b> forced because the processor your billing flow depends on is sunsetting its API in 12 weeks. After that date, renewals and upgrades stop processing, full stop.",
        ),
    ],
    "day14.html": [
        ("A CRM marketing platform ships two changes", "A B2B SaaS team ships two changes"),
    ],
    "day15.html": [
        ("A CRM platform's lifecycle-messaging team", "A platform team's messaging module"),
    ],
    "day16.html": [
        (
            "A CRM marketing platform's design review runs fifteen minutes on a new \"AI Suggested Segment\" button added to the campaign builder",
            "A design review runs fifteen minutes on a new \"AI Suggested Filter\" button added to the workflow editor",
        ),
    ],
    "day18.html": [
        (
            "your CRM platform's \"Predictive Audience Builder\"",
            "your analytics product's \"Predictive Audience Builder\"",
        ),
    ],
    "day19.html": [
        (
            "Your CRM marketing platform adopts <b>Weekly Active Campaigns</b> &mdash; automated journeys actually running and reaching a customer's end audience",
            "Your product adopts <b>Weekly Active Workflows</b> &mdash; automations actually running and delivering value to end users",
        ),
        (
            "auto-duplicates a client's existing campaign across every untouched audience segment",
            "auto-duplicates a client's existing workflow across every untouched account segment",
        ),
    ],
    "day26.html": [
        ("A CRM marketing platform's growth team", "A B2B SaaS growth team"),
    ],
    "day27.html": [
        (
            "A B2B CRM marketing platform is evaluating whether to reprice from its current model &mdash; three flat per-seat tiers &mdash; to a usage-based model metered on active contacts marketed to.",
            "A B2B SaaS company is evaluating whether to reprice from three flat per-seat tiers to usage-based pricing metered on monthly active API calls.",
        ),
    ],
    "day28.html": [
        (
            "In a CRM marketing platform, platform thinking shows up constantly and quietly. Customer data flows in from a dozen source systems; campaign triggers need to fire the moment a customer crosses a threshold",
            "In API-first B2B products, platform thinking shows up constantly. Customer data flows in from a dozen source systems; event triggers need to fire the moment a record crosses a threshold",
        ),
        (
            "If segment-change events are becoming table stakes in CRM marketing platforms",
            "If real-time event webhooks are becoming table stakes in B2B platforms",
        ),
    ],
    "day29.html": [
        (
            "In a CRM marketing platform, this shift is already underway and mostly invisible to the marketer using it. Predictive send-time models, AI-generated subject lines, and auto-drafted campaign briefs",
            "In many B2B products, this shift is already underway and mostly invisible to the user. Predictive scheduling, AI-generated summaries, and auto-drafted templates",
        ),
        ("the marketer can't tell", "the user can't tell"),
    ],
    "day30.html": [
        (
            "In a CRM marketing platform, the spine rarely runs in a tidy straight line",
            "On a mature B2B product, the spine rarely runs in a tidy straight line",
        ),
    ],
}


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    name = path.name
    pairs = list(GLOBAL)
    if name in PER_FILE:
        pairs = PER_FILE[name] + pairs
    for old, new in pairs:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(ROOT.glob("day*.html")):
        if path.parent.name == "dist":
            continue
        if process(path):
            changed += 1
    print(f"Updated {changed} file(s)")


if __name__ == "__main__":
    main()
