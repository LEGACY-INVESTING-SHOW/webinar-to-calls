# Deck spec format

One JSON file per deck: `slides/src/<NN>-<CODE>.json`. Build with `python3 tools/build_decks.py`.

```json
{
  "nn": 1,                        // 1-27, order in the tracker set (drives the cover glyph)
  "code": "1.3",
  "title": "Exact tracker title",
  "short": "Short running title for the footer (max ~40 chars)",
  "section": "Part One · Module 1",
  "slides": [ {slide}, ... ]
}
```

Every slide takes: `type`, `title` (a teaching point, a full claim, never the lesson name), optional `eyebrow`, `keyline`, `text` (paragraphs above the main element), `box` ({kind: info|warn|gold, label, text}), `assumption` (true adds "All figures on this slide are assumptions"), `ref` (the Markdown section number it maps to, e.g. "1.3.4"), and `notes` (full speaking notes, paragraphs separated by a blank line).

Inline markup allowed in strings: `**bold**`, `*italic*`, `[text](https://url)`.

| type | fields |
|---|---|
| cover | kicker, title, subtitle, meta: [[label, text] x3] |
| statement | text (one sentence), support |
| bullets | items [], ordered (bool) |
| table | columns [], rows [[]], total_last (bool), compact (bool), caption |
| worksheet | columns [], rows [[]] (empty string = blank fill-in cell), caption |
| two | left {head, note, items []}, right {same} |
| flow | nodes [{k, h, d, kind: ""/"stop"/"go"}] (3-5 nodes) |
| gates | gates [{q, sub, no}], end |
| calc | lines [{op, label, v}], result {label, v}, side (text), side_box (box) |
| bars | items [{label, value (number, negative for costs), kind: pos/neg/total, hot (bool), display}], caption |
| checklist | items [], cols2 (bool) |
| scorecard | columns [], rows [[]], bands [{kind: r/i/"", h, d}] (3 bands) |
| dothis | items [] (3-4 actions), next (transition line), label |
| sources | items [{title, url, note}] |
| text | text |

Fit rules for a 1280x720 slide: title up to ~80 characters (two lines); bullets max 6 items of up to ~110 characters; tables max 8 rows (use compact for 9-11); flow max 5 nodes; gates max 5; checklist max 8 (cols2 up to 14 short items); bars max 8; a box adds ~110px, so pair it with shorter content.
