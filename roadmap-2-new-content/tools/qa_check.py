"""QA checks for the Roadmap 2.0 new-content package.

    python3 tools/qa_check.py            # prints a report, writes qa/qa-report-auto.md

Checks:
1. All 27 tracker codes appear as lesson headings in the Markdown and as decks.
2. Every deck slide has a ref that resolves to a heading in the Markdown, and speaking notes.
3. No em/en dashes and no banned words in the Markdown or deck text.
4. Every URL in the Markdown and decks is listed; URLs cited in decks also appear in the Markdown.
5. Canonical example figures appear unchanged (spot list).
"""
import json, re, pathlib, collections, subprocess, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
MD = ROOT / "roadmap-2-complete-new-content.md"
SRC = ROOT / "slides" / "src"

CODES = ["1.3", "3.1", "3.3", "3.4", "3.5", "5.7", "6.5", "0.1", "0.2", "0.3", "PA.1", "PA.6", "PA.7", "PA.8",
         "PA.9", "PA.10", "PA.11", "PA.12", "OP.6", "OP.7", "OP.8", "OP.9", "OP.11", "OP.12", "SR.1", "SR.3", "SR.5"]
BANNED = ["delve", "crucial", "robust", "seamless", "game-changer", "game changer", "unlock", "supercharge", "elevate",
          "empower", "tapestry", "testament", "pivotal", "realm", "holistic", "synergy", "cutting-edge", "let's dive",
          "dive in", "here's the thing", "it's worth noting", "let that sink in", "at the end of the day",
          "in today's landscape", "non-negotiable", "you're done", "guaranteed", "financial freedom",
          "crush it", "navigate the landscape", "the power of"]
CANON = {"Alder base gross": "$61,625", "Alder base net": "$12,218", "Alder monthly net": "$1,018",
         "Alder stress net": "$1,548", "Alder break-even": "49.9%", "Alder sunk setup": "$12,050",
         "Cedar gross": "$74,275", "Cedar NOI": "$29,209", "DSCR cash flow": "$5,572", "DSCR PITIA": "$2,557",
         "Cash to close DSCR": "$110,688", "Refi cash out": "$15,725", "Sale net before tax": "$142,560"}


def headings(md):
    return re.findall(r"^(#{2,4})\s+(\S+)\s+(.*)$", md, re.M)


def main():
    md = MD.read_text()
    out = []
    w = out.append
    ok = True
    # 1 codes
    h2 = {m[1] for m in headings(md) if m[0] == "##"}
    decks = {json.loads(p.read_text())["code"]: p for p in SRC.glob("[0-9][0-9]-*.json")}
    missing_md = [c for c in CODES if c not in h2]
    missing_deck = [c for c in CODES if c not in decks]
    html_missing = [c for c, p in decks.items() if not (ROOT / "slides" / f"{p.stem}.html").exists()]
    w(f"## 1. Tracker codes\n\n- Codes expected: {len(CODES)}\n- Lesson headings found in Markdown: {len([c for c in CODES if c in h2])}\n"
      f"- Deck specs found: {len([c for c in CODES if c in decks])}\n- Missing in Markdown: {missing_md or 'none'}\n"
      f"- Missing decks: {missing_deck or 'none'}\n- Specs without built HTML: {html_missing or 'none'}\n")
    ok &= not (missing_md or missing_deck or html_missing)
    # 2 refs
    heads = {m[1].rstrip(".") for m in headings(md)}
    bad_refs, no_notes, counts = [], [], {}
    all_deck_text = []
    for code, p in sorted(decks.items(), key=lambda kv: kv[1].name):
        d = json.loads(p.read_text())
        counts[code] = len(d["slides"])
        for k, s in enumerate(d["slides"], 1):
            ref = str(s.get("ref", "")).strip()
            base = ref.split()[0] if ref else ""
            if ref.endswith("sources"):
                base = ref  # "1.3 sources" maps to the lesson's sources heading
                if f"{code} sources" not in md:
                    bad_refs.append((code, k, ref))
            elif base not in heads:
                bad_refs.append((code, k, ref))
            if len(str(s.get("notes", "")).split()) < 25:
                no_notes.append((code, k))
        all_deck_text.append(p.read_text())
    w(f"## 2. Slide-to-Markdown mapping\n\n- Slides total: {sum(counts.values())} across {len(counts)} decks\n"
      f"- Slides whose ref does not match a Markdown heading: {bad_refs or 'none'}\n- Slides with fewer than 25 words of notes: {no_notes or 'none'}\n")
    ok &= not bad_refs
    # 3 voice
    deck_text = "\n".join(all_deck_text)
    dash_md = [(i + 1, l[:90]) for i, l in enumerate(md.splitlines()) if "—" in l or "–" in l]
    dash_deck = deck_text.count("—") + deck_text.count("–")
    bans = collections.Counter()
    for b in BANNED:
        pat = re.compile(r"\b" + re.escape(b) + r"\b", re.I)
        bans[b] = len(pat.findall(md)) + len(pat.findall(deck_text))
    bans = {k: v for k, v in bans.items() if v}
    w(f"## 3. Voice checks\n\n- Em/en dashes in Markdown: {len(dash_md)} {dash_md[:5] if dash_md else ''}\n- Em/en dashes in deck specs: {dash_deck}\n"
      f"- Banned words/phrases found (count): {bans or 'none'}\n")
    # 4 urls
    url_re = re.compile(r"https?://[^\s)\]\"'<>]+")
    md_urls = sorted(set(u.rstrip(".,;") for u in url_re.findall(md)))
    deck_urls = sorted(set(u.rstrip(".,;") for u in url_re.findall(deck_text)))
    not_in_md = [u for u in deck_urls if u not in md_urls]
    doms = collections.Counter(re.sub(r"^https?://([^/]+).*", r"\1", u) for u in md_urls)
    w(f"## 4. Links\n\n- Unique URLs in Markdown: {len(md_urls)}\n- Unique URLs in decks: {len(deck_urls)}\n"
      f"- Deck URLs not cited in the Markdown: {not_in_md or 'none'}\n- Domains: " + ", ".join(f"{d} ({n})" for d, n in doms.most_common()) + "\n")
    (ROOT / "qa" / "url-list.txt").write_text("\n".join(md_urls) + "\n")
    # 5 canon
    miss = {k: v for k, v in CANON.items() if v not in md}
    w(f"## 5. Canonical figures\n\n- Spot figures checked: {len(CANON)}\n- Not found in Markdown: {miss or 'none'}\n")
    words = len(re.findall(r"\w+", md))
    w(f"## Totals\n\n- Markdown words: {words:,}\n- Slide counts: " + ", ".join(f"{c} {n}" for c, n in counts.items()) + "\n")
    rep = "# Automated QA report\n\n" + "\n".join(out)
    (ROOT / "qa" / "qa-report-auto.md").write_text(rep)
    print(rep)
    print("RESULT:", "PASS" if ok else "CHECK FAILURES ABOVE")


if __name__ == "__main__":
    main()
