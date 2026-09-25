# Roadmap 2.0: Preston's 27 new deliverables

This folder is a standalone project. It holds the teaching content and slide decks for the 27 tracker rows marked **New** and assigned to **Preston** in the Airbnb Arbitrage Roadmap 2.0 Production Tracker: 7 Arbitrage Roadmap lessons, 17 STR Concierge lessons, and 3 shared resources. Sam's lessons and the rows marked Updated or Retained are not included.

## What's here

| Path | What it is |
|---|---|
| `roadmap-2-complete-new-content.md` | Step 1. The complete teaching content for all 27 items in one file. |
| `slides/index.html` | Step 2. Index of the 27 HTML decks. Open any deck in a browser. |
| `slides/<NN>-<CODE>.html` | One deck per lesson or resource. Arrow keys move, **N** shows speaker notes, **O** shows an overview, **P** prints slides with notes pages. |
| `slides/src/*.json` | The deck sources. Each slide's `ref` names the Markdown section it maps to. |
| `slides/assets/` | Shared stylesheet, viewer script, and bundled fonts (Newsreader, Instrument Sans; SIL Open Font License). |
| `reference/` | The production brief, the design guide, the writing guide, and the canonical recurring examples. |
| `tools/examples.py` | Computes every recurring-example number. `tools/render_examples.py` writes `reference/recurring-examples.md`. |
| `tools/build_decks.py` | Builds the HTML decks from `slides/src`. |
| `tools/qa_check.py` | Checks codes, slide-to-section mapping, voice rules, links, and canonical figures. |
| `tools/shoot.py`, `tools/contact.py` | Screenshots slides and builds contact sheets for visual review. |
| `parts/` | The per-lesson source files and research logs that were assembled into the complete Markdown file. |
| `qa/` | QA report, URL list, and unresolved facts. |

## Rebuild

```bash
python3 tools/render_examples.py      # only if you change an assumption in tools/examples.py
python3 tools/assemble.py             # parts/ -> roadmap-2-complete-new-content.md
python3 tools/build_decks.py          # slides/src -> slides/*.html
python3 tools/qa_check.py             # writes qa/qa-report-auto.md
```

Screenshots need Python Playwright and Pillow (`pip install playwright pillow`). The tools point Playwright at the preinstalled Chromium.

## Two recurring examples

- **Alder Street unit** (arbitrage): a hypothetical 2-bed apartment leased at $1,950 a month. Used in every Part One lesson.
- **Cedar Ridge house** (ownership): a hypothetical 3-bed lake-market house bought for $385,000 by Maya and Chris. Used in every STR Concierge lesson.

Every number in both examples is an assumption for teaching. See `reference/recurring-examples.md`.

Education only. Nothing here is legal, tax, lending, or insurance advice. Each lesson names the professional who has to confirm its examples before recording.
