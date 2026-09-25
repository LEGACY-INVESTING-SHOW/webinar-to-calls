"""Screenshot slides: python3 tools/shoot.py <deck-stem> <outdir> [slide numbers...]"""
import sys, pathlib, asyncio
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
async def main(stem, outdir, nums):
    out = pathlib.Path(outdir); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": 1320, "height": 760})
        url = (ROOT / "slides" / f"{stem}.html").as_uri()
        await pg.goto(url + "#1"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(800)
        total = await pg.evaluate("document.querySelectorAll('.slide').length")
        nums = nums or list(range(1, total + 1))
        overflow = []
        for n in nums:
            await pg.evaluate(f"window.deckShow({n-1})")
            await pg.wait_for_timeout(120)
            el = pg.locator(f'.slide[data-n="{n}"]')
            # overflow check on the unscaled slide content
            ov = await pg.evaluate(f"""(() => {{ const s=document.querySelector('.slide[data-n="{n}"]'); const c=s.querySelector('.content'); const f=s.querySelector('.foot');
                 if(!c) return 0; const cb=c.getBoundingClientRect(), sb=s.getBoundingClientRect(); let maxb=0;
                 c.querySelectorAll('*').forEach(e=>{{const r=e.getBoundingClientRect(); if(r.height>0) maxb=Math.max(maxb,r.bottom);}});
                 if(!f || getComputedStyle(f).display==='none') return 0; const fb = f.getBoundingClientRect().top; return Math.round((maxb - fb) ); }})()""")
            if ov > 0: overflow.append((n, ov))
            await el.screenshot(path=str(out / f"{stem}-{n:02d}.png"))
        await b.close()
        print(stem, "slides", total, "overflow(px past footer):", overflow)
stem, outdir, *nums = sys.argv[1:]
asyncio.run(main(stem, outdir, [int(x) for x in nums]))
