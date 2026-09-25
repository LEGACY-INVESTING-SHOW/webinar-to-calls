# Prep Kit PDF Design Guidelines

Use this guide for every PDF we make for Legacy Investing Show: prep kit guides, bonuses, workbooks, cheat sheets. The goal is one family of documents that look related, read easily, and print well.

Reference builds: `anti-inflation-pack.html` and `tax-playbook.html` in this folder. Copy their structure. The shared stylesheet is `style.css`. Build with `build.py`.

---

## 1. The feel in one line

A calm field guide on cream paper. Forest green ink. One thin gold accent. Big serif headings, plain sans body, and a dark green "Do this week" box at the end of every chapter.

If a page looks like a slide deck, a SaaS dashboard, or a bank brochure, it is wrong.

---

## 2. Page setup

| Item | Value |
|---|---|
| Page size | US Letter, 8.5 x 11 in, portrait |
| Margins | Top 0.85 in, sides 1 in, bottom 0.95 in |
| Cover | Full bleed, no margins, rendered on its own |
| Footer | Running title left, page number right, 7.5 px small caps, muted gray |
| Body column | Full width inside the margins. No sidebars. |
| Page color | Cream on every page, including the margins |

Body pages start numbering at 1 after the cover.

---

## 3. Color

Use these tokens. Do not invent new colors.

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#FBF8F1` | Page background |
| `--ivory` | `#F3EDDF` | Soft panels, table zebra if needed |
| `--line` | `#DDD4BE` | Hairlines, table rows |
| `--ink` | `#1F2A24` | Body text |
| `--ink-soft` | `#4A5850` | Secondary text, captions in tables |
| `--ink-faint` | `#7D877F` | Captions, footers, labels |
| `--forest` | `#16352A` | Headings, cover background, "Do this week" box |
| `--emerald` | `#2F7D5B` | Key lines, part numbers, list markers, small labels |
| `--emerald-tint` | `#E4EFE5` | Info callout background |
| `--gold` | `#D9A93D` | Thin rules, table header underline, checkbox borders on dark |
| `--gold-ink` | `#8A6510` | Strategy tags, gold callout label |
| `--gold-tint` | `#F6ECD3` | "How to read this" and "If you only do four things" callouts |
| `--rose` | `#B0503C` | Warning label |
| `--rose-tint` | `#F6E4DD` | Warning callout background |

Rules:

- Green is the main color. Gold is an accent. Rose is only for warnings.
- Never use pure black or pure white.
- Never use gradients, glows, drop shadows, or rounded cards.
- Text on the dark green box is `#EAF0EA`. Bold text on it is `#FBF8F1`. Labels on it are gold.

---

## 4. Type

Two fonts. Load from Google Fonts.

| Role | Font | Weights |
|---|---|---|
| Display (titles, part names, big statements, strategy names) | **Newsreader** | 500, 600, 700, plus 500 italic |
| Body (everything else) | **Instrument Sans** | 400, 500, 600, 700, plus 400 italic |

Newsreader replaced Fraunces. Fraunces had swash-style f and j glyphs that read as odd. Do not use Fraunces. Do not use Inter, Roboto, Arial, Open Sans, or system fonts.

Size scale, in points:

| Element | Font | Size | Weight | Notes |
|---|---|---|---|---|
| Cover title | Newsreader | 54 | 600 | Line height 1.0, cream on forest |
| Cover subtitle | Newsreader italic | 17 | 500 | |
| Part title | Newsreader | 28 | 600 | Forest |
| Part number | Newsreader | 56 | 500 | Emerald, in the left column |
| Key line under a part title | Instrument Sans | 13 | 500 | Emerald |
| Section head (h3) | Instrument Sans | 13.5 | 700 | Forest |
| Strategy name | Newsreader | 18 | 600 | Forest |
| Small head (h4) | Instrument Sans | 11 | 700 | |
| Big statement | Newsreader | 17 | 500 | Forest, gold rule above |
| Body | Instrument Sans | 10.5 | 400 | Line height 1.5 |
| Table text | Instrument Sans | 9.5 | 400 | |
| Captions | Instrument Sans | 8.5 | 400 | Faint ink |
| Labels (PART, DO THIS WEEK, PLAIN WORDS) | Instrument Sans | 8 | 600–700 | Uppercase, letter-spacing 0.18–0.22 em |

Bold in body text is weight 600 in forest green. That is how key phrases stand out without a highlighter.

---

## 5. Page anatomy

Every guide has these pages, in this order.

1. **Cover.** Full-bleed forest green. Eyebrow "PRESTON SEO · PREP KIT" in gold. A small kicker line. The title. A 64 pt gold rule. An italic subtitle. A two-line blurb. A three-column meta row at the bottom: edition or author, format or tax year, use. One small graphic in the top right that means something about the guide. Four bars for four buckets. A grid of 27 squares for 27 strategies. Do not use stock images, icons, or photos.
2. **Read this first.** One page. Who it is for. What it is not. Where the numbers come from. A line about talking to a licensed adviser.
3. **Contents.** Its own page. Part numbers in emerald, titles, hairline between rows. A gold callout box under the list that says how to read the guide.
4. **Parts.** Each part starts on a new page. See section 6.
5. **Your one-page plan** or **Your first 30 days.** A fill-in table the reader signs, plus a printable checklist.
6. **Notes and sources.** Where each number came from. Which old claims were dropped and why. A short disclaimer at the end.

---

## 6. Part opener

Every part opens the same way:

```
PART              Part title in Newsreader 28 pt
01                Key line in emerald, one sentence
------------------------------------------------ (2 px forest rule)
```

The number sits in a 1.05 in left column. The title and key line sit to the right. The key line is the one thing a reader should remember from the part.

Then the body flows at full width. No left column after the opener.

---

## 7. Components

Use only these. If you need a new one, add it to `style.css` and to this file.

**Do this week (`.do`).** Dark forest box, gold label, three or four items, each with a hollow gold checkbox. Ends every part. Actions only. No theory. Each item should take under an hour.

**Plain words (`.words`).** Hairline above and below. Emerald label. A two-column term and definition list. Use it the first time a piece of jargon appears. Keep each definition to one line.

**Info callout (`.box`).** Emerald tint, emerald uppercase label, square corners, no border. For worked examples and short explanations.

**Warning callout (`.box.warn`).** Rose tint, rose label. For "this fails if" and "do not do this."

**Gold callout (`.box.gold`).** Gold tint, gold label. For reading instructions and the "minimum viable" summary.

**Big statement (`.big`).** A 36 pt gold rule, then one sentence in Newsreader 17 pt. One per part at most. It is the sentence you would put on a wall.

**Strategy block (`.strategy`).** Small gold tag "STRATEGY 5 OF 27", the name in Newsreader 18 pt, then one line in small text that says "I use this." or "I have studied this." Use for numbered items in a playbook.

**Tables.** Uppercase 8.5 pt headers with a 2 px gold underline. Hairline between rows. No vertical lines. No fills unless zebra helps a long table. Right-align numbers. Bold the first column when it is a label. A `.cap` caption under the table for sources and notes.

**Worksheet tables (`.ws`).** Same table, with dotted bottom borders on the cells the reader fills in.

**Checklist (`.check`).** Hollow forest checkboxes, one item per line, hairline between lines. For printable checklists.

**Bucket or job cards (`.jobs`).** A 2 x 2 grid, ivory background, 2 px emerald top border, small label, Newsreader name, one-line description. Use once, for a four-part idea. Do not use card grids anywhere else.

**Two columns (`.two`).** Only for short "ignore / watch" style lists or a glossary.

---

## 8. Spacing and rhythm

- Space is uneven on purpose. Tight inside a group. Generous between groups.
- Part opener bottom margin: 18 pt. Section head top margin: 16 pt. Paragraph gap: 9 pt.
- Callouts and boxes never break across pages. Tables never break across pages.
- No page should end with only a "Do this week" box or one or two lines on it. If that happens, trim the part by a few sentences until the box fits on the previous page. Do not shrink the font to fix it.
- A part can end with a partial page. That is normal for a book.

---

## 9. Writing rules

These matter as much as the design. The look only works if the words are short.

- **Grade 4 to 5 reading level.** Score with the reading-level script before you build. Target Flesch-Kincaid grade under 5.0. The inflation guide scored 2.9. The tax guide scored 4.6.
- **Short sentences.** Aim for 8 to 15 words. One idea per sentence.
- **Plain words first.** Say "a paper write-off for wear on a building" before you say "depreciation." Then use the real word, because the reader will meet it elsewhere.
- **Keep the numbers.** Dollar limits, dates, percentages, and sources stay exact. Simple does not mean vague.
- **Say what you did and did not do.** "I use this." "I have studied this." "I did not have this audited." Readers trust it.
- **Every part ends in action.** Three or four "Do this week" items.
- **Cut sales language.** No "non-negotiable," no "you're done," no promised results. Say what the old version got wrong and fix it.
- **No em-dashes.** Use a period or a comma.
- **Educational disclaimer** on the cover meta row, in "Read this first," and in the closing note. Never in the middle of the content.

---

## 10. Build workflow

1. Copy one of the reference HTML files. Keep the `<link rel="stylesheet" href="style.css">` line.
2. Write the content in the components above.
3. Add the guide's name and running title to the `GUIDES` dict in `build.py`.
4. Run:

   ```bash
   cd guides && python3 build.py your-guide-name
   ```

   This renders the cover full bleed, renders the body with footers, stamps a cream background under every body page so the margins match, merges it all with pypdf, and drops page previews in `preview/`.

5. Build a contact sheet from `preview/` and look at every page at thumbnail size. Fix stray pages (section 8).
6. Open two or three pages at full size. Check tables, boxes, and headings.
7. Score the reading level one more time.
8. Delete `preview/` before you commit. Commit the HTML, CSS, and the PDF in `pdf/`.

Requirements: Python 3 with `playwright` (Chromium installed), `pypdf`, and `pdftoppm` from poppler for previews.

---

## 11. Don'ts

- No icons above headings. No emoji.
- No photos, stock art, or AI images.
- No gradients, glass, shadows, or rounded cards.
- No hero numbers with tiny labels under them.
- No centered body text. Left align everything except table numbers.
- No more than one accent color on a page besides green.
- No font other than Newsreader and Instrument Sans.
- No page that is only a callout box.
- No sentence over 25 words.
