# Minimal slide rules (Preston's feedback, 25 September 2026)

These rules replace the slide-writing parts of `deck-brief.md`. The decks are mid-course videos. A slide shows the point and nothing else. Preston says the rest.

Preston's words: "Too much content, too many labels and extra disclaimers. Get rid of the helper text, label text, extra disclaimers, subheadlines, and just directly say what you want to say with a more minimal approach. Don't overexplain things, don't overjustify the calculations, keep things simple." And: "Nobody cares about the sources. Get rid of that."

## What the builder already hides

`tools/build_decks.py` runs in minimal mode. It no longer shows cover kicker, subtitle, eyebrow, or meta row; slide eyebrows; keylines (subheadlines); "All figures are assumptions" tags; box labels; table and chart captions; flow-node labels; gate sub-lines; column notes; footers; or `sources` slides. Delete those fields from the JSON anyway, so the source matches what people see.

## Rules for every deck

1. **Cover:** the title only. One plain sentence with the lesson's point, ideally under 9 words. No lesson code, module name, or teacher line.
2. **Slide count:** 9 to 14 slides for a lesson, 10 to 15 for a resource. Merge slides that say the same thing. Cut slides that state the obvious.
3. **Titles:** say the point in plain words, 10 words or fewer where possible, never more than two lines. No colons stacking two ideas.
4. **Body:** one element per slide. Pick one of:
   - up to 4 bullets of up to 8 words each;
   - a table of up to 5 rows and 4 columns, numbers only where possible;
   - a calc of up to 5 lines plus the result;
   - a flow or gates of up to 4 steps with short labels (drop the `d` text or keep it under 5 words);
   - a bars chart of up to 6 bars;
   - a checklist of up to 6 short items.
   The `text` field above the element is only for a sentence the slide can't work without, under 15 words. Use a `box` only if it carries the key takeaway, under 15 words.
5. **Cut from every deck:**
   - the `sources` slide;
   - "Who confirms what" slides (keep one plain sentence in the speaking notes where a pro must check something);
   - disclaimer boxes and "education only" lines;
   - "assumption" labels on slides (the Markdown keeps them);
   - recap slides and slides that repeat the title in the body;
   - explanations of how a number was calculated, unless the calculation IS the lesson. Then show inputs and the result, not every step.
6. **Math:** show the answer and the two to four inputs that drive it. Round to what a viewer can hold: "$1,018 a month", not "$1,018.17". Keep figures identical to the Markdown.
7. **Last slide:** a `dothis` slide with 3 actions of up to 8 words each and a short `next` line such as "Next: 3.2, Sam's live regulation search."
8. **Speaking notes:** keep them, because they are what Preston says. Trim each to 60 to 150 words. Conversational, first person, no reading of sources or URLs aloud, no stacked disclaimers. One sentence naming who confirms something is fine where it matters.
9. **Refs:** every slide keeps a `ref` that matches a heading in the lesson Markdown.
10. **Voice:** no em or en dashes; the writing-guide banned words; no invented Preston stories or results.
