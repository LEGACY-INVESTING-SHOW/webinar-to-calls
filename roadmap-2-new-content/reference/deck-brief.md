# Deck brief (shared by all deck agents)

Project folder: /home/user/webinar-to-calls/roadmap-2-new-content (a standalone project; ignore the rest of the repo).

You turn finished lesson content into one HTML slide deck per lesson or resource. The Markdown in `parts/<NN>-<CODE>.md` is the source of truth. Slides teach from it; they never add new facts, numbers, or sources that are not in the Markdown.

Read first:
1. `slides/src/README.md` — the JSON spec format, slide types, and fit rules.
2. `reference/DESIGN.md` — the visual and writing rules (cream paper, forest green, one gold accent, short sentences, no em dashes, no hype, no icons or emoji). The decks already use this design; you only write the JSON.
3. `reference/writing-guide.md` — voice rules. They apply to slide text and speaking notes.
4. Your lessons' Markdown files in `parts/`.

Write `slides/src/<NN>-<CODE>.json` for each assigned item (same NN and CODE as the part file, e.g. `slides/src/12-PA.6.json`). Set `nn` to the NN number, `code`, `title` (exact tracker title as in the Markdown H2, except PA.7 which uses "Deal"), `short` (a footer title under ~40 characters), and `section` (e.g. "Part Two · Phase 1 - Property Acquisition").

Deck requirements:
- 14 to 20 slides per lesson deck; resource decks can run 14 to 22.
- Slide 1 is a `cover`. Its title is the lesson's main teaching point as a claim, not the lesson name. The subtitle carries "Lesson CODE. <tracker title>" (or "Resource CODE. ..."). Meta: [["Teacher","Preston"],["Example","Alder Street unit (hypothetical)" or "Cedar Ridge house (hypothetical)"],["Use","Education only. Not legal, tax, lending, or insurance advice."]] (adjust the Use line to fit the lesson).
- Every other slide title teaches a point: a full claim a student could write down ("Break-even sits near 50% occupancy, so the cushion is 20 points"), never a topic label ("Break-even"), and never the lesson name.
- Cover the Markdown's sections in order. Every slide's `ref` must be an existing Markdown heading number from the lesson (for example "PA.6.3"), or "CODE sources" for the sources slide. Check each ref against the file with grep.
- Include the recurring example as visible math: `calc`, `bars`, or `table` slides with the exact figures from the Markdown. Set `assumption: true` on any slide showing example figures.
- Include at least one decision tool the student uses: `gates`, `flow`, `scorecard`, `worksheet`, or `checklist`, taken from the lesson's exercise.
- Include a "Who confirms what" slide (table or two) naming the professional and what they confirm.
- Second-to-last slide: `dothis`, with 3 or 4 concrete actions under an hour each, plus a `next` line naming the next lesson by code and title (from the Markdown's Next lesson section).
- Last slide: `sources`, with the key primary sources from the lesson's source list (up to 10), each with a short note on what it supports.
- Resource decks (SR.x) must teach how to use the template: what it is for, walk through each section of the template, the decision rules and formulas, a filled example, common mistakes, and how to hand it to the professional.
- Where Sam's demo sits next to the lesson, one slide (or a line in notes) says what to bring back from Sam's lesson by code. Don't re-teach the demo.

Speaking notes (`notes`) on every slide: 80 to 200 words of what Preston actually says, in the first person, conversational, following the voice rules. Notes expand the slide; they don't read it aloud. Numbers in notes must match the Markdown. Never invent Preston's experiences or client results.

Fit: follow the fit rules in the README. After writing each spec, build and screenshot it:

```bash
cd /home/user/webinar-to-calls/roadmap-2-new-content
python3 tools/build_decks.py <NN>-<CODE>
python3 tools/shoot.py <NN>-<CODE> /tmp/claude-0/-home-user-webinar-to-calls/d99ede6b-dd10-56b0-832f-64707167293b/scratchpad/decks/<NN>-<CODE>
python3 tools/contact.py /tmp/claude-0/-home-user-webinar-to-calls/d99ede6b-dd10-56b0-832f-64707167293b/scratchpad/decks/<NN>-<CODE>/sheet.png /tmp/claude-0/-home-user-webinar-to-calls/d99ede6b-dd10-56b0-832f-64707167293b/scratchpad/decks/<NN>-<CODE>/*-[0-9][0-9].png
```

`shoot.py` prints any slide whose content runs past the footer. The list must be empty. Then Read the contact sheet image and look at it: fix crowded, clipped, or near-empty slides (a slide with one short line and nothing else should be merged or given a diagram). Rebuild until clean.

Rules: no em or en dashes anywhere in the JSON (grep for them); no banned words from the writing guide; valid JSON. Only write `slides/src/<your files>.json` and the built `slides/<your files>.html`. Don't edit tools, CSS, parts, or other agents' files. If the builder lacks something you need, work within the existing slide types and mention it in your report.

When done, report: the files, slide counts, the overflow result for each deck, and anything in the Markdown you think is wrong or inconsistent (don't fix the Markdown yourself).
