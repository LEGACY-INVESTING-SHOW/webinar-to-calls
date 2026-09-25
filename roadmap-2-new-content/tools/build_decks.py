"""Build HTML lesson decks from slides/src/*.json.

    python3 tools/build_decks.py          # builds every deck + slides/index.html
    python3 tools/build_decks.py 01-1.3   # builds one deck

Spec format: see slides/src/README.md.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "slides" / "src"
OUT = ROOT / "slides"
MD = "roadmap-2-complete-new-content.md"
# Minimal mode (Preston feedback, 2026-09-25): no labels, eyebrows, subheadlines, captions, assumption tags,
# box labels, footers, cover meta, or sources slides. Slides show the point and nothing else.
MINIMAL = True
FONTS = ""  # fonts are bundled in slides/assets/fonts and imported by deck.css


def inline(s):
    """Escape, then allow **bold**, *italic*, [text](url)."""
    s = html.escape(str(s), quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def paras(s):
    return "".join(f"<p>{inline(p.strip())}</p>" for p in re.split(r"\n\s*\n", str(s)) if p.strip())


NUMERIC = re.compile(r"^[\s(+\-−]*[$]?[\d,]+(\.\d+)?\s*(%|x|/month|/mo|/year|/yr| months| nights)?\)?$")


def is_num(c):
    return bool(NUMERIC.match(str(c).strip())) if str(c).strip() else False


def box(b):
    if not b:
        return ""
    kind = b.get("kind", "info")
    cls = {"info": "box", "warn": "box warn", "gold": "box gold"}[kind]
    lab = b.get("label", {"info": "Worked example", "warn": "This fails if", "gold": "How to use this"}[kind])
    labhtml = "" if MINIMAL else f'<div class="lab">{inline(lab)}</div>'
    return f'<div class="{cls}">{labhtml}{paras(b["text"])}</div>'


def table(cols, rows, compact=False, total_last=False, ws=False):
    numcols = set()
    for j in range(len(cols)):
        vals = [r[j] for r in rows if j < len(r) and str(r[j]).strip()]
        if j > 0 and vals and sum(is_num(v) for v in vals) >= max(1, len(vals) * 0.6):
            numcols.add(j)
    cls = "t" + (" compact" if compact else "") + (" ws" if ws else "")
    h = [f'<table class="{cls}"><thead><tr>']
    for j, c in enumerate(cols):
        h.append(f'<th class="{"n" if j in numcols else ""}">{inline(c)}</th>')
    h.append("</tr></thead><tbody>")
    for k, r in enumerate(rows):
        tr = ' class="total"' if total_last and k == len(rows) - 1 else ""
        h.append(f"<tr{tr}>")
        for j, c in enumerate(r):
            c = str(c)
            if ws and (c.strip() == "" or set(c.strip()) == {"_"}):
                h.append('<td class="fill">&nbsp;</td>')
            else:
                h.append(f'<td class="{"n" if j in numcols else ""}">{inline(c)}</td>')
        h.append("</tr>")
    h.append("</tbody></table>")
    return "".join(h)


def glyph(nn):
    # 27 squares, one per new deliverable; this deck's square is filled gold.
    out = ['<svg class="glyph" width="186" height="186" viewBox="0 0 186 186" aria-hidden="true">']
    for k in range(27):
        r, c = divmod(k, 6) if k < 24 else (4, k - 24)
        x, y = 4 + c * 30, 4 + r * 30
        on = (k + 1) == nn
        fill = "#D9A93D" if on else "none"
        stroke = "#D9A93D" if on else "rgba(234,240,234,.45)"
        out.append(f'<rect x="{x}" y="{y}" width="22" height="22" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    out.append("</svg>")
    return "".join(out)


def render_slide(d, s, n, total):
    t = s["type"]
    head = ""
    if t not in ("cover", "statement"):
        eb = "" if MINIMAL else s.get("eyebrow", "")
        head = (f'<div class="eyebrow">{inline(eb)}</div>' if eb else "") + f'<h2>{inline(s["title"])}</h2>'
        if s.get("keyline") and not MINIMAL:
            head += f'<div class="keyline">{inline(s["keyline"])}</div>'
        head += '<div class="rule"></div>'
    tag = '<div class="assume">All figures on this slide are assumptions</div>' if s.get("assumption") and not MINIMAL else ""
    body = ""
    if t == "cover":
        meta = "".join(f"<div><span>{inline(a)}</span>{inline(b)}</div>" for a, b in s.get("meta", []))
        if MINIMAL:
            body = f'<h1>{inline(s["title"])}</h1><div class="goldrule"></div>'
        else:
          body = (glyph(d["nn"]) + f'<div class="eyebrow">{inline(s.get("eyebrow", "PRESTON · ROADMAP 2.0"))}</div>'
                f'<div class="kicker">{inline(s.get("kicker", ""))}</div><h1>{inline(s["title"])}</h1>'
                f'<div class="goldrule"></div><p class="sub">{inline(s.get("subtitle", ""))}</p><div class="meta">{meta}</div>')
    elif t == "statement":
        eb = "" if MINIMAL else s.get("eyebrow", "")
        body = ((f'<div class="eyebrow">{inline(eb)}</div>' if eb else "") +
                f'<div class="big"><p>{inline(s["text"])}</p>' +
                (f'<div class="support">{inline(s["support"])}</div>' if s.get("support") and not MINIMAL else "") + "</div>")
    elif t == "bullets":
        tagn = "ol" if s.get("ordered") else "ul"
        cls = "steps" if s.get("ordered") else "pts"
        body = f'<{tagn} class="{cls}">' + "".join(f"<li>{inline(x)}</li>" for x in s["items"]) + f"</{tagn}>"
    elif t in ("table", "worksheet"):
        body = table(s["columns"], s["rows"], s.get("compact"), s.get("total_last"), ws=(t == "worksheet"))
        if s.get("caption") and not MINIMAL:
            body += f'<div class="cap">{inline(s["caption"])}</div>'
    elif t == "two":
        cols = []
        for side in (s["left"], s["right"]):
            c = f'<div><h3>{inline(side["head"])}</h3>'
            if side.get("note") and not MINIMAL:
                c += f'<div class="colnote">{inline(side["note"])}</div>'
            c += '<ul class="pts">' + "".join(f"<li>{inline(x)}</li>" for x in side["items"]) + "</ul></div>"
            cols.append(c)
        body = '<div class="two">' + "".join(cols) + "</div>"
    elif t == "flow":
        parts = []
        for k, nd in enumerate(s["nodes"]):
            if k:
                parts.append('<div class="arrow">&rarr;</div>')
            khtml = "" if MINIMAL else f'<div class="k">{inline(nd.get("k", ""))}</div>'
            parts.append(f'<div class="node {nd.get("kind", "")}">{khtml}'
                         f'<div class="h">{inline(nd["h"])}</div><div class="d">{inline(nd.get("d", ""))}</div></div>')
        body = '<div class="flow">' + "".join(parts) + "</div>"
    elif t == "gates":
        g = []
        for k, x in enumerate(s["gates"]):
            sub = f'<small>{inline(x["sub"])}</small>' if x.get("sub") and not MINIMAL else ""
            g.append(f'<div class="gate"><div class="num">{k + 1:02d}</div><div class="q">{inline(x["q"])}{sub}</div>'
                     f'<div class="no">{inline(x["no"])}</div></div>')
        end = f'<div class="end">{inline(s["end"])}</div>' if s.get("end") else ""
        body = '<div class="gates">' + "".join(g) + end + "</div>"
    elif t == "calc":
        ln = []
        for x in s["lines"]:
            ln.append(f'<div class="ln"><span><span class="op">{inline(x.get("op", ""))}</span>{inline(x["label"])}</span>'
                      f'<span class="v">{inline(x["v"])}</span></div>')
        r = s["result"]
        ln.append(f'<div class="ln res"><span><span class="op">=</span>{inline(r["label"])}</span><span class="v">{inline(r["v"])}</span></div>')
        side = ""
        if s.get("side"):
            side = f'<div class="side body small">{paras(s["side"])}</div>'
        if s.get("side_box"):
            side += box(s["side_box"])
        body = f'<div class="calc"><div class="lines">{"".join(ln)}</div><div class="side">{side}</div></div>'
    elif t == "bars":
        mx = max(abs(float(x["value"])) for x in s["items"]) or 1
        rows = []
        for x in s["items"]:
            v = float(x["value"])
            w = abs(v) / mx * 100
            kind = x.get("kind", "neg" if v < 0 else "pos")
            cls = "bar " + kind + (" hot" if x.get("hot") else "")
            disp = x.get("display") or (("-$" if v < 0 else "$") + f"{abs(v):,.0f}")
            rows.append(f'<div class="{cls}"><div class="lbl">{inline(x["label"])}</div><div class="trk"><div class="fill" style="left:0;width:{w:.1f}%"></div></div>'
                        f'<div class="val">{inline(disp)}</div></div>')
        body = '<div class="bars">' + "".join(rows) + "</div>"
        if s.get("caption") and not MINIMAL:
            body += f'<div class="cap">{inline(s["caption"])}</div>'
    elif t == "checklist":
        cls = "check cols2" if s.get("cols2") else "check"
        body = f'<ul class="{cls}">' + "".join(f"<li>{inline(x)}</li>" for x in s["items"]) + "</ul>"
    elif t == "scorecard":
        body = table(s["columns"], s["rows"], compact=True)
        bands = "".join(f'<div class="band {b.get("kind", "")}"><div class="h">{inline(b["h"])}</div><div class="d">{inline(b["d"])}</div></div>'
                        for b in s["bands"])
        body += f'<div class="bands">{bands}</div>'
    elif t == "dothis":
        items = "".join(f"<li>{inline(x)}</li>" for x in s["items"])
        lab = "" if MINIMAL else f'<div class="lab">{inline(s.get("label", "Do this week"))}</div>'
        body = f'<div class="do">{lab}<ul>{items}</ul></div>'
        if s.get("next"):
            body += f'<div class="next">{inline(s["next"])}</div>'
    elif t == "sources":
        items = "".join(f'<li><a href="{html.escape(x["url"])}" target="_blank" rel="noopener">{inline(x["title"])}</a>'
                        f'{(" · " + inline(x["note"])) if x.get("note") else ""}</li>' for x in s["items"])
        body = f'<ul class="src">{items}</ul>'
    elif t == "text":
        body = f'<div class="body">{paras(s["text"])}</div>'
    else:
        raise ValueError(f"unknown slide type {t}")
    if t not in ("cover", "table", "worksheet") and s.get("text") and t not in ("statement", "text"):
        body = f'<div class="body">{paras(s["text"])}</div>' + body
    if t in ("table", "worksheet") and s.get("text"):
        body = f'<div class="body small">{paras(s["text"])}</div>' + body
    body += box(s.get("box"))
    ref = s.get("ref", "")
    foot = "" if MINIMAL else (f'<div class="foot"><span>{inline(d["code"])} · {inline(d.get("short", d["title"]))}</span>'
            f'<span class="ref">{("§ " + inline(ref)) if ref else ""}</span><span>{n} / {total}</span></div>')
    cls = "slide s-" + t
    return (f'<section class="{cls}" data-n="{n}">{head}<div class="content">{tag}{body}</div>{foot}</section>'
            f'<div class="notes-src" data-ref="{MD} § {html.escape(ref)}"><div class="nh">Slide {n} · {html.escape(s.get("title", ""))}</div>'
            f'<div class="nb">{paras(s.get("notes", ""))}<p class="small">Maps to {MD} § {inline(ref)}</p></div></div>')


def build(path):
    d = json.loads(path.read_text())
    if MINIMAL:
        d["slides"] = [s for s in d["slides"] if s["type"] != "sources"]
    total = len(d["slides"])
    slides = "".join(render_slide(d, s, k + 1, total) for k, s in enumerate(d["slides"]))
    title = f'{d["code"]} {d["title"]}'
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(d["code"])} · {html.escape(d.get("short", d["title"]))}</title>
<meta name="description" content="{html.escape(title)}. Roadmap 2.0 lesson deck. Keys: arrows to move, N for speaker notes, O for overview, P to print with notes.">
{FONTS}
<link rel="stylesheet" href="assets/deck.css"></head>
<body>
<div class="hud"><span class="count"></span><a href="#" class="tn">Notes (N)</a><a href="#" class="to">Overview (O)</a><a href="index.html">All decks</a></div>
<main class="stage">{slides}</main>
<aside class="notes-panel"><div class="nh"><span>Speaker notes</span><span class="nref"></span></div><div class="nbody"></div></aside>
<script src="assets/deck.js"></script>
</body></html>"""
    out = OUT / f'{path.stem}.html'
    out.write_text(doc)
    return d, total, out


def index(decks):
    rows = []
    for d, total, out in decks:
        rows.append(f'<tr><td>{html.escape(d["code"])}</td><td><a href="{out.name}">{html.escape(d["title"])}</a></td>'
                    f'<td>{html.escape(d.get("section", ""))}</td><td class="n">{total}</td></tr>')
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Roadmap 2.0 Decks</title>{FONTS}<link rel="stylesheet" href="assets/deck.css">
<style>body{{background:var(--paper);padding:56px 16px}} .wrap{{max-width:1040px;margin:0 auto}} h1{{font:600 40px/1.1 var(--display);color:var(--forest);margin:0 0 8px}}
p{{font:400 17px/1.5 var(--body);color:var(--ink-soft);max-width:760px}} .wrap table.t{{font-size:16px}} @media(max-width:640px){{.wrap table.t td:nth-child(3),.wrap table.t th:nth-child(3){{display:none}}}}</style></head>
<body><div class="wrap"><div class="eyebrow">Preston · Roadmap 2.0 · New deliverables</div><h1>27 lesson and resource decks</h1>
<p>One deck per tracker item. Open a deck, use the arrow keys to move, press N for speaker notes and O for an overview. Every slide maps to a numbered section of {MD}.</p>
<table class="t"><thead><tr><th>Code</th><th>Deck</th><th>Section</th><th class="n">Slides</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div></body></html>"""
    (OUT / "index.html").write_text(doc)


if __name__ == "__main__":
    files = sorted(SRC.glob("*.json"))
    if len(sys.argv) > 1:
        files = [SRC / f"{a}.json" for a in sys.argv[1:]]
    built = [build(f) for f in files]
    if len(sys.argv) == 1:
        index(built)
    for d, total, out in built:
        print(f"{d['code']:6} {total:3} slides -> {out.relative_to(ROOT)}")
