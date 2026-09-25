# Writing guide for Roadmap 2.0 new content

## Who is talking
Preston teaches every lesson in the first person ("I", "you"). It sounds like a person explaining a deal across a table: direct, plain, a bit dry, never hyped.

**Never invent Preston's history.** No "when I launched my first unit", no client stories, no results, no "my students average". If a personal story would help, leave a one-line bracket for the recording: `[Recording note: Preston can add a real example here if he has one.]` Use at most one per lesson.

## Voice rules (drawn from the stop-slop / humanizer / anti-slop skills)
- No em dashes or en dashes used as dashes. Use a period, comma, colon, or parentheses. (Number ranges like 45-180 use a plain hyphen.)
- Short sentences, mostly 8 to 20 words. Nothing over 25 words. Mix lengths.
- Plain words first, then the real term: "a paper write-off for wear on the building (depreciation)".
- Active voice with a real subject. "The city issues the permit," not "the permit is issued".
- Name the specific thing. Not "there are several factors"; say which factors.
- Use two items or four when that is what's true. Don't reach for three by reflex.
- Contractions are fine (you'll, it's, don't).
- No throat-clearing: skip "Let's dive in", "In this lesson we will explore", "Here's the thing", "It's worth noting", "Let that sink in", "At the end of the day", "In today's landscape".
- No hype or filler words: delve, crucial, robust, leverage (as a verb meaning use), seamless, game-changer, unlock, supercharge, navigate the landscape, journey (outside a guest journey), elevate, empower, tapestry, testament, pivotal, realm, holistic, synergy, cutting-edge, "the power of".
- No "It's not X, it's Y" / "This isn't about X. It's about Y." constructions. No "Not only... but also".
- No stacked rhetorical questions. One real question is fine when you answer it.
- No emoji. No exclamation marks.
- Don't end sections with a moral or a recap line that repeats the section. End on the next action or the fact.
- Avoid bolded-label bullet lists everywhere ("**Speed:** blah"). Use them only in reference tables or templates.
- No sales language: "non-negotiable", "you're done", "guaranteed", "passive income", "financial freedom", "crush it".
- Say "may", "can", "in some cities" where the rule depends on the address, borrower, tax year, or product. But don't hedge plain facts.

## Accuracy rules
- Every legal, tax, financing, or platform claim gets a link to its primary source right beside the claim: official government page, IRS, CFPB, Fannie Mae, the lender's own published page, or the platform's help center. Third-party blogs are not sources for rules.
- Treat rules as conditional on the address, borrower, tax year, or product. Say which.
- Never invent program benefits, lender terms, "algorithm" rules, guarantees, client results, or statistics.
- Illustrative numbers are always marked. Use the tag **(assumption)** after a made-up number the first time it appears in a section, or put the numbers in a table captioned "All figures are assumptions."
- Use the canonical numbers in `reference/recurring-examples.md`. Do not change them. If a lesson needs a new number (for example a lender reserve requirement), label it as an assumption and keep it consistent with the canonical example.
- Mark where a professional must confirm: use a line that starts `**Confirm with:**` naming attorney, CPA, insurer, lender, or local licensing office and what they must confirm.
- Research method in this environment: direct fetches of airbnb.com, irs.gov, consumerfinance.gov, fanniemae.com and most official sites are blocked by the network proxy. Use WebSearch with `allowed_domains` set to the official domain to confirm what the official page says (the search tool returns summaries of the page). Log each check in your sources log with how you verified it. If you cannot confirm a claim, write it conditionally and add it to the log under "Unresolved".

## Keep Sam's lessons separate
Sam records the live demos. Preston's lessons teach the decisions and failure points around them. Do not re-teach a Sam demo. Point to it by code and title and say what the student should bring back from it.

Sam's lessons referenced by Preston's content:
- 3.2 How to Research Regulations Before You Sign Anything (live regulation search)
- 4.1 How to Find a Money-Making Market - 2026 Method; 4.2 Market Analysis: Supply vs. Revenue & Oversupply Screening; 4.3 AirDNA Tutorial (2026); 4.4 How to Find a Profitable Property; 4.5 How to Easily Find Apartments for Arbitrage
- 5.6 Skip Tracing Tutorial; 9.1 Posting Your Listing; 9.10 Revenue Management Fundamentals; 9.11 Building Your Direct Booking Channel (Use Guesty); 9.12 Guesty for Hosts Tutorial; 9.13 PriceLabs Tutorial; 11.4 AI Tools for Hosts in 2026
- PA.2 Choosing a Market for Ownership: Regulatory-Safe, Cash-Flowing Areas; PA.3 Deal Sourcing: Building a Pipeline of 5-10 Qualified Properties; PA.4 Reading a Full Underwriting Package: Revenue, Expenses, Cap Rate & Cash-on-Cash Return; PA.5 Cost Segregation & Year-One Depreciation, Explained
- OP.1 Listing Creation Across Airbnb, VRBO & Booking.com; OP.2 2026 Listing Optimization: Structured Data & the Algorithm; OP.3 Building Your Direct Booking Website; OP.4 Tech Stack Architecture: PMS, Pricing, Messaging & Ops as One Workflow; OP.5 Dynamic Pricing & Revenue Management for Owners; OP.10 The 30-Day and 90-Day Performance Review

Other lessons that are Updated or Retained (not ours; you may point to them, never write them): 1.4 Mindset & My Personal Journey (retained), 1.5 The Math to Quit Your Job - Rebuilt Around the 2.5x Rule (updated), 2.4 Insurance & Liability Protection for Arbitrage Operators (updated), 5.1 Landlord Script Overview, 5.2 Landlord Role Play, 5.3 Sublease Addendum Deep Dive (updated), 5.4 Negotiating Free Rent, 6.1 Cleaners, 6.2 Handyman, 6.3 Neighbors, 6.4 Stagers & Interior Designers, 7.1 Why Design Matters, 9.3 Dealing With Damages, 9.4 How to Avoid Parties & Smoking, 9.8 Bookkeeping, 9.9 Taxes & Working With a CPA, 10.6 Home Equity to Scale, 12.x Co-Hosting Masterclass, SR.2 Underwriting spreadsheet (updated), SR.4 Top STR Markets Ranked (updated). Don't define the "2.5x rule"; lesson 1.5 owns it.

## Tracker order (for transitions)
Part One: ... 1.3 → 1.4 Mindset (retained) → 1.5 ... ; 3.1 → 3.2 (Sam) → 3.3 → 3.4 → 3.5 → Module 4 (Sam 4.1) ; 5.6 (Sam) → 5.7 → Module 6 (6.1 Cleaners) ; 6.4 → 6.5 → Module 7.
Part Two: 0.1 → 0.2 → 0.3 → PA.1 → PA.2 (Sam) → PA.3 (Sam) → PA.4 (Sam) → PA.5 (Sam) → PA.6 → PA.7 → PA.8 → PA.9 → PA.10 → PA.11 → PA.12 → OP.1 (Sam) ... OP.5 (Sam) → OP.6 → OP.7 → OP.8 → OP.9 → OP.10 (Sam) → OP.11 → OP.12.
Part Three: SR.1 (backs Module 3 and PA.2), SR.3 (supports PA.5), SR.5 (supports Module 9 tool tutorials and OP.4/OP.5).
The transition should name the next lesson that moves the student's decision forward. When the next lesson in order is a Sam demo, say what to watch for there and which Preston lesson picks up after.

## Required shape of every lesson section (Markdown)

```
<a id="lesson-CODE-SLUG"></a>
## CODE  Exact tracker title

| Tracker | Detail |
|---|---|
| Part / module | ... |
| Code | CODE |
| Production type / owner | New / Preston |
| Connects to | Sam's ... ; resource ... |

### CODE.0 Learning outcome
One short paragraph: what the student can decide or produce after this lesson.

### CODE.1 ... (teaching narrative, several numbered subsections, full prose, not bullets-only)
...
### CODE.n Worked example: Alder Street / Cedar Ridge
(calculations shown step by step; numbers from the canonical file; assumptions marked)
### CODE.n Exercise / decision tool
(a worksheet table, scorecard, checklist, or decision flow the student fills in for a real address or deal)
### CODE.n Who confirms what
(**Confirm with:** lines)
### CODE.n Next lesson
(one short paragraph transition)
### CODE sources
(bulleted list: [title](url), what it supports, "checked 2026-09-25 via ...")
```
Headings use the code with a dot suffix, e.g. `### PA.6.3 How a lender reads projected STR income`. For code 1.3 use `### 1.3.1`, etc. For resources, replace "Learning outcome" with "What this resource does" and include the full template (fields table with columns such as Field / What to enter / Source or formula / Status), instructions, decision rules, and formulas.

Length target: 2,500 to 4,000 words per lesson; resources can be longer because of the templates. Real teaching narrative, not an outline.
