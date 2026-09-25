"""Bundle a built deck into one self-contained HTML file (CSS, fonts, and script inlined).

    python3 tools/bundle_deck.py 01-1.3 [02-3.1 ...]   -> dist/<stem>.html
"""
import base64, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "slides" / "assets"

def inline_css():
    fonts = (ASSETS / "fonts" / "fonts.css").read_text()
    def emb(m):
        data = base64.b64encode((ASSETS / "fonts" / m.group(1)).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"
    fonts = re.sub(r"url\(([^)]+\.woff2)\)", emb, fonts)
    css = (ASSETS / "deck.css").read_text().replace('@import url("fonts/fonts.css");', "")
    return fonts + "\n" + css

def bundle(stem):
    html = (ROOT / "slides" / f"{stem}.html").read_text()
    html = html.replace('<link rel="stylesheet" href="assets/deck.css">', f"<style>{inline_css()}</style>")
    html = html.replace('<script src="assets/deck.js"></script>', f"<script>{(ASSETS / 'deck.js').read_text()}</script>")
    html = html.replace('<a href="index.html">All decks</a>', "")
    out = ROOT / "dist" / f"{stem}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html)
    return out

for s in sys.argv[1:]:
    p = bundle(s)
    print(p, f"{p.stat().st_size/1024:.0f} KB")
