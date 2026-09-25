"""Assemble parts/*.md into roadmap-2-complete-new-content.md."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = ROOT / "parts"

TRACKER = [
    # nn, code, title, part, module
    (1, "1.3", "Is Arbitrage Still Viable in 2026? A Market Reality Check", "Part One", "Module 1 - Foundations & the 2026 Market Reality"),
    (2, "3.1", "How STR Regulation Actually Works: Licensing, Zoning & Primary-Residence Rules", "Part One", "Module 3 - STR Regulations & Compliance"),
    (3, "3.3", "Occupancy Taxes & Platform-Verified Registration", "Part One", "Module 3 - STR Regulations & Compliance"),
    (4, "3.4", "Red Flags: Markets, Cities & Leases to Avoid in 2026", "Part One", "Module 3 - STR Regulations & Compliance"),
    (5, "3.5", "Sublease Legality & Landlord Disclosure Best Practices", "Part One", "Module 3 - STR Regulations & Compliance"),
    (6, "5.7", "The 2026 Landlord Pitch: Handling Regulation & Liability Objections", "Part One", "Module 5 - Landlord Outreach System"),
    (7, "6.5", "When to Bring In a Local Property Manager", "Part One", "Module 6 - Building Your Dream Team"),
    (8, "0.1", "Welcome to STR Concierge: What's Different About Owning", "Part Two", "Module 0 - Ownership vs. Arbitrage"),
    (9, "0.2", "Why Ownership Wins: Cash Flow + Tax Savings + Equity", "Part Two", "Module 0 - Ownership vs. Arbitrage"),
    (10, "0.3", "Is Ownership Right for You? A Capital & Readiness Checklist", "Part Two", "Module 0 - Ownership vs. Arbitrage"),
    (11, "PA.1", "Discovery: Defining Your Buy Box (Market, Property Type, Price Range, Goals)", "Part Two", "Phase 1 - Property Acquisition"),
    (12, "PA.6", "DSCR Loans 101: How They Qualify the Property, Not You", "Part Two", "Phase 1 - Property Acquisition"),
    (13, "PA.7", "DSCR vs. Conventional Financing: Which Path Fits Your Deal", "Part Two", "Phase 1 - Property Acquisition"),
    (14, "PA.8", "Offer Strategy & Negotiation for Investment Property", "Part Two", "Phase 1 - Property Acquisition"),
    (15, "PA.9", "Due Diligence: STR-Specific Inspections, Appraisal & Title Review", "Part Two", "Phase 1 - Property Acquisition"),
    (16, "PA.10", "Entity & Tax Structure Setup: LLC, S-Corp or Holding Company", "Part Two", "Phase 1 - Property Acquisition"),
    (17, "PA.11", "Closing Day: Documents, Wire Fraud Prevention & Possession", "Part Two", "Phase 1 - Property Acquisition"),
    (18, "PA.12", "Your Post-Close Checklist: Insurance, Utilities & Handoff to Operations", "Part Two", "Phase 1 - Property Acquisition"),
    (19, "OP.6", "Furnishing & Interior Optimization for an Owned Property", "Part Two", "Phase 2 - Operations Launch"),
    (20, "OP.7", "Building Your Ops Team: Cleaner, Co-Host, or Property Manager", "Part Two", "Phase 2 - Operations Launch"),
    (21, "OP.8", "SOPs: Cleaning, Guest Communication & Emergency Response", "Part Two", "Phase 2 - Operations Launch"),
    (22, "OP.9", "Guest Experience & Review Strategy in the AI Ranking Era", "Part Two", "Phase 2 - Operations Launch"),
    (23, "OP.11", "Scaling Your Portfolio: Refinancing, HELOCs & Property #2", "Part Two", "Phase 2 - Operations Launch"),
    (24, "OP.12", "Exit Strategy: Hold, Refinance, Sell, or 1031 Exchange", "Part Two", "Phase 2 - Operations Launch"),
    (25, "SR.1", "Regulatory compliance checklist, by state and city", "Part Three", "Shared Resource Library"),
    (26, "SR.3", "Cost segregation & tax-impact estimator", "Part Three", "Shared Resource Library"),
    (27, "SR.5", "Tool comparison guide (PMS, dynamic pricing, AI guest-messaging)", "Part Three", "Shared Resource Library"),
]
PART_NAMES = {"Part One": "Part One: Airbnb Arbitrage Roadmap 2.0", "Part Two": "Part Two: STR Concierge", "Part Three": "Part Three: Shared Resources"}


def anchor(text):
    return re.search(r'<a id="([^"]+)"></a>', text).group(1)


def main():
    files = {int(p.name[:2]): p for p in PARTS.glob("[0-9][0-9]-*.md")}
    L = []
    w = L.append
    w("# Airbnb Arbitrage Roadmap 2.0: Preston's 27 New Lessons and Resources\n")
    w("Complete teaching content. Prepared 25 September 2026 from the Roadmap 2.0 new-creation brief and the live production tracker.\n")
    w("This file holds the material Preston teaches from: learning outcomes, full narrative, worked examples, exercises, decision tools, and templates. The slide decks in `slides/` are built from it, and every slide names the section here that it maps to.\n")
    w("Education only. Nothing here is legal, tax, lending, or insurance advice. Rules for short-term rentals depend on the exact address. Tax treatment depends on the taxpayer and tax year. Loan terms depend on the borrower, the property, and the lender's current product. Each lesson ends with a **Who confirms what** section naming the professional who must review its examples before recording.\n")
    w("## How to use this file\n")
    w("- Lessons appear in tracker order within each part. Headings carry the tracker code, so `PA.6.3` is the third section of lesson PA.6.")
    w("- Two hypothetical examples recur throughout: the **Alder Street unit** (arbitrage) and the **Cedar Ridge house** (ownership). Their full numbers are in the next section. Every figure in them is an assumption.")
    w("- Links sit beside the claims they support. Each lesson ends with its source list and the date checked.")
    w("- Sam's demo lessons are referenced by code, never re-taught. Each Preston lesson says what to bring back from Sam's demo.")
    w("- The appendix lists facts that are still unresolved and who has to confirm them.\n")
    w("## Tracker check\n")
    w("Verified against the live tracker (Production Tracker tab) on 25 September 2026. All 27 rows read *New*, *Preston*, *Not Started*.\n")
    w("| # | Code | Tracker title | Part | Module / phase |\n|---:|---|---|---|---|")
    for nn, code, title, part, mod in TRACKER:
        p = files.get(nn)
        link = f"[{title}](#{anchor(p.read_text())})" if p else title
        w(f"| {nn} | {code} | {link} | {part} | {mod} |")
    w("\nTracker spelling notes: the tracker spells PA.7 as \"Which Path Fits Your Heal\" and Module 6 as \"Building Your Hream Team\". Both are read here as typos for \"Deal\" and \"Dream\". PA.1's full tracker title includes the parenthetical \"(Market, Property Type, Price Range, Goals)\".\n")
    ex = (ROOT / "reference" / "recurring-examples.md").read_text()
    ex = ex.replace("# Recurring examples (canonical numbers)", "## The two recurring examples", 1)
    ex = re.sub(r"^## Example", "### Example", ex, flags=re.M)
    ex = re.sub(r"^### (A\d|B\d)", r"#### \1", ex, flags=re.M)
    ex = ex.replace("generated by `tools/examples.py`. Do not change a number in a lesson without changing it here and re-running the script.",
                    "computed by `tools/examples.py`. Lessons quote these figures unchanged.")
    w(ex + "\n")
    current = None
    for nn, code, title, part, mod in TRACKER:
        if part != current:
            w(f"\n---\n\n# {PART_NAMES[part]}\n")
            current = part
        p = files.get(nn)
        if not p:
            w(f"## {code}  {title}\n\n**MISSING**\n")
            continue
        w(p.read_text().strip() + "\n\n---\n")
    unresolved = ROOT / "qa" / "unresolved.md"
    if unresolved.exists():
        w("\n# Appendix: unresolved facts and professional review\n")
        body = unresolved.read_text()
        body = re.sub(r"^# .*\n", "", body, count=1)
        w(body)
    out = ROOT / "roadmap-2-complete-new-content.md"
    out.write_text("\n".join(L).replace("\n\n\n", "\n\n"))
    print(out, len(out.read_text().split()), "words;", len(files), "parts")


if __name__ == "__main__":
    main()
