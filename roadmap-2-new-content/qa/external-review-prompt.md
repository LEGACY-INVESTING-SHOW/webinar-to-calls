# Prompt for an independent AI review of the Roadmap 2.0 package

Copy everything below the line into the reviewing AI, and attach `roadmap-2-new-content.zip` (or give it the folder).

---

You are reviewing a finished piece of online-course production work. Be independent and critical. Your job is to find what is wrong, weak, unclear, inconsistent, or risky, and to say exactly how to fix it. Don't praise. Don't rewrite the whole course. Report findings.

## 1. What this project is

Legacy Investing Show runs two courses taught by **Preston**:

- **Airbnb Arbitrage Roadmap 2.0 (Part One):** leasing a property from a landlord and running it as a short-term rental (STR).
- **STR Concierge (Part Two):** buying and operating an STR you own.
- **Shared resources (Part Three):** templates used across both.

A production tracker (Google Sheet) lists every lesson, marked New, Updated, or Retained, and assigns each one to Preston or to **Sam**. This package covers only the **27 rows marked New and assigned to Preston**:

- **7 Arbitrage lessons:** 1.3, 3.1, 3.3, 3.4, 3.5, 5.7, 6.5
- **17 STR Concierge lessons:** 0.1, 0.2, 0.3, PA.1, PA.6, PA.7, PA.8, PA.9, PA.10, PA.11, PA.12, OP.6, OP.7, OP.8, OP.9, OP.11, OP.12
- **3 shared resources:** SR.1 (regulatory compliance checklist), SR.3 (cost segregation and tax-impact estimator), SR.5 (tool comparison guide)

Sam records live demos (for example 3.2 regulation research, 4.1 to 4.5 market research, PA.2 to PA.5 market, sourcing, underwriting and cost segregation, OP.1 to OP.5 listings, pricing and software, OP.10 performance review). Preston's lessons must teach the decisions around those demos and hand off to Sam by code. They must not re-teach Sam's demos. Lessons marked Updated or Retained are out of scope.

The original production brief is `reference/brief.md`. Read it first. It lists the required description and topics for every one of the 27 items, and the production checks.

## 2. The two deliverables

**Step 1: `roadmap-2-complete-new-content.md`.** This is the complete teaching content for all 27 items in one Markdown file, about 130,000 words. It is written for Preston to teach from. Every lesson is required to have:

- a learning outcome;
- a full teaching narrative in numbered sections (for example `PA.6.3`);
- worked examples with visible calculations;
- a practical exercise or decision tool;
- a "Who confirms what" section naming the attorney, CPA, lender, insurer, or local office that must confirm the example;
- a transition to the next lesson;
- sources, linked beside the claims they support.

The three resources contain usable templates: fields, instructions, decision rules, and formulas. The file also contains a tracker check, the full numbers of the two recurring examples, and an appendix of unresolved facts. The per-lesson source files are in `parts/`, with research logs in `parts/sources-*.md`.

**Step 2: 27 HTML slide decks, one per item, 374 slides in total.**

- `dist/<NN>-<CODE>.html`: each deck as a single self-contained file. Easiest to open.
- `slides/<NN>-<CODE>.html`: the same decks, using the shared files in `slides/assets/`. The index is `slides/index.html`.
- `slides/src/<NN>-<CODE>.json`: the editable source of each deck.

## 3. Where the script (speaking notes) lives

Each slide's script is what Preston says on camera while that slide shows. It is stored in three places, all with the same text:

1. **Inside the HTML itself.** In each deck file, every `<section class="slide" data-n="N">` is followed by a `<div class="notes-src" data-ref="roadmap-2-complete-new-content.md § X.Y">` element. That element holds the script for slide N and the Markdown section it maps to. In a browser, press **N** to show the script panel under the current slide. Use the arrow keys to move between slides and **O** for an overview. The notes element is hidden on screen, so read the HTML source or press N.
2. **In the JSON source**, as the `notes` field of each slide in `slides/src/*.json`. The `ref` field names the Markdown section.
3. **In one table:** `qa/slide-scripts-and-timing.md` lists every slide with its title, full script, word count, and run time at 180 words per minute. The total is about 264 minutes. Most lessons run 8 to 11 minutes, and OP.7 runs about 16.

Review the slides and the script together. The slide shows the point, and the script carries the explanation.

## 4. Rules the work was supposed to follow

**Design** (`reference/DESIGN.md`, adapted from a PDF guide to slides):

- cream paper, forest green, one gold accent;
- Newsreader for headings and Instrument Sans for body text;
- no gradients, shadows, icons, emoji, or stock images.

**Preston's own feedback on the decks, which overrides earlier guidance.** In his words: "Too much content, too many labels and extra disclaimers. Get rid of the helper text, label text, extra disclaimers, subheadlines, and just directly say what you want to say with a more minimal approach. Don't overexplain, don't overjustify the calculations, keep things simple." And: "Nobody cares about the sources" on slides. The resulting rules are in `reference/deck-minimal-rules.md`:

- a cover with the title only;
- one point per slide;
- up to 4 short bullets, or one small table, calc, flow, or checklist;
- no labels, captions, disclaimers, footers, or sources slides;
- a final "do this week" slide;
- scripts of 60 to 150 words per slide.

The Markdown file keeps its sources and professional-confirmation notes. Those were removed only from the slides.

**Voice** (`reference/writing-guide.md`):

- first person as Preston, plain and conversational;
- no em or en dashes;
- no hype words ("delve", "unlock", "game-changer", and so on);
- sentences under 25 words;
- no invented Preston stories, client results, guarantees, program benefits, or "algorithm" rules;
- illustrative numbers marked "(assumption)".

Preston also asked for his humanize-ai-writing skill (a nine-source anti-AI-slop review) to be applied to all content. See the limitations below.

**Accuracy:**

- Legal, tax, lending, and platform rules must link to primary sources: official government pages, the IRS, CFPB, Fannie Mae, lenders' published pages, or platform help centers.
- Rules must be written as conditional on the address, the borrower, the tax year, or the product.

**Course-wide terms** are in `reference/course-terms.md`. For example: "course example" instead of "canonical", ADR as "average nightly rate", "the $10,000 buffer", and "pass rule" used only in PA.1's sense.

## 5. The recurring examples

The full numbers are in `reference/recurring-examples.md` and are computed by `tools/examples.py`. Every number is an assumption.

- **Alder Street unit (arbitrage):**
  - a hypothetical two-bedroom apartment in an unnamed city, leased at $1,950 a month;
  - at a $205 average nightly rate and 70% occupancy, it grosses $61,625 and nets $12,218 a year ($1,018 a month) under Airbnb's 15.5% host-only fee;
  - break-even occupancy is 49.9%;
  - the stress case nets $1,548 a year;
  - setup payback is 11.8 months on a 24-month lease;
  - lessons test it against the official New York City and Los Angeles rules.
- **Cedar Ridge house (ownership):**
  - a hypothetical three-bedroom lake-market house bought by **Maya and Chris** for $385,000 with 25% down;
  - they compare a DSCR quote (7.25%, 1 point) with a conventional quote (6.875%);
  - net operating income is $29,209;
  - DSCR base cash flow is $5,572 before diligence, and $5,172 after PA.9 adds a $400 yearly permit renewal. The weak case is -$5,875;
  - cash to close is $110,688;
  - the story continues through the offer (walk-away price $393,000), diligence, closing, launch, refinance, and exit.
  - Savings rise from $210,000 in 0.3 to $231,000 by the offer in PA.8, after six months of saving, while they keep a $51,000 emergency fund.

## 6. Checks already done (verify them, don't trust them)

- **Tracker:** titles and ownership were checked against the live tracker. The tracker has typos: PA.7 reads "Heal" for "Deal", and Module 6 reads "Hream".
- **Calculation audit:** see `qa/calc-audit.md`, then the consistency fixes in `qa/consistency-fixes.md`.
- **No-context reviews:** every deck was reviewed and then fixed. See `qa/reviews/*-review.md` and `*-changes.md`.
- **Automated QA:** `python3 tools/qa_check.py` passes. All 27 codes appear in the Markdown and in the decks, every slide ref maps to a heading, there are no dashes, and no banned words. See `qa/qa-report-auto.md`.
- **Overflow:** every deck passed a screenshot overflow check.
- **Summary:** `qa/final-report.md`.

## 7. Known limitations (confirm, and flag anything worse)

- **Sources were not opened directly.** Direct fetches of official sites (airbnb.com, irs.gov, consumerfinance.gov, fanniemae.com, nyc.gov, lacity.gov, and others) were blocked. Every rule was checked only through web-search summaries restricted to the official domain, and the search budget ran out near the end. `qa/unresolved.md`, also the appendix of the Markdown, lists open facts and who must confirm them. If you can open the official pages, check the claims against them. That is the most valuable thing you can do.
- **The humanize pass is incomplete.** It finished for SR.1, SR.3, and SR.5. The other 24 items got only 1 to 4 of the nine rounds before the run was stopped. The logs are in `qa/humanize/<deck>/log.md`.
- **OP.7 is long:** 18 slides, above the 9 to 14 target.
- **Consistency after edits:** some cross-lesson figures were edited late, so check that the Cedar Ridge money thread still agrees end to end.

## 8. What to review

Work through the whole package. For each item, look at the Markdown lesson, the deck, and its script.

1. **Brief coverage.** Does each of the 27 items cover the brief's description and every "topics to include" bullet? List any missing topic. Are Sam's demos handed off rather than re-taught?
2. **Accuracy and sourcing.** Find claims about law, tax, lending, insurance, or platforms that are wrong, stated too absolutely, out of date, or unsupported by their cited source. Check dates and figures: 1031 exchange deadlines, the post-January 19, 2025 bonus depreciation rule, Fannie Mae's short-term rental income rule, NYC Local Law 18, LA Home-Sharing, and Airbnb fees and features. Flag any invented rule, result, or guarantee.
3. **Math.** Recompute worked examples, especially the Cedar Ridge thread across 0.2 to OP.12 and the Alder Street figures. List every mismatch between lessons, and between the Markdown and the slides or script.
4. **Teaching quality.** Could a beginner follow it? Look for undefined jargon, skipped steps, confusing order, exercises a student couldn't start, and weak transitions.
5. **Slides.** Do the decks follow Preston's minimal rules? Flag slides that are still crowded, carry labels or disclaimers, repeat the script, or say nothing useful. Also flag slides that are now so bare they lose the point. Check readability in the rendered HTML.
6. **Script.** Read the notes as spoken delivery. Does it sound like one natural person? Flag AI patterns: staged setups, "it's not X, it's Y" contrasts, stacked rhetorical questions, filler, hype, repeated sentence shapes, and summary endings. Flag scripts that just read the slide, that are too long for the slide, or that contradict the Markdown. Say whether the timing per lesson (about 8 to 11 minutes) suits mid-course videos.
7. **Consistency.** Check terms, names, the recurring figures, cross-references (for example "see PA.8.3"), and pronouns (Maya and Chris are "they").
8. **Risk.** Flag anything that could mislead a student into a costly or illegal action, overstate returns, or read as legal, tax, or lending advice without the needed conditions.

## 9. Output

Write one Markdown file, `review-report.md`, with these sections:

1. **Verdict:** 5 to 8 sentences. Is this ready to record? What are the three biggest problems?
2. **Critical issues:** anything factually wrong, risky, or breaking the brief. For each: item code, file, and location (section number or slide number), what's wrong, evidence (a quote, a recomputed figure, or the correct source), and the exact fix.
3. **Per-item review:** one subsection per code, in tracker order. Cover brief coverage (met or missing), accuracy, math, teaching, slides, and script. Use a short table of findings with a severity (High, Medium, or Low) and a fix for each.
4. **Cross-course issues:** consistency, terms, the Cedar Ridge and Alder Street threads, and repeated patterns.
5. **Script and timing notes:** lessons that should be shortened or lengthened, and scripts that need rewriting, with examples.
6. **Unresolved facts:** which items in `qa/unresolved.md` you could confirm or refute, with the source. List what still needs a professional.
7. **Prioritized fix list:** a numbered list, most important first, each small enough to act on.

Quote exact text when you criticize wording. Recompute numbers with a tool rather than estimating. If you can't verify something, say so instead of guessing.
