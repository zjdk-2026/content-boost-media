import bmp_core as C
from bmp_core import qa
import asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image
from ep_helpers import cover, end

from eps12_16 import EPS

async def main(only=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for tag, (foot, S) in EPS.items():
            if only and only not in tag: continue
            C.FOOT = foot
            for i, body in enumerate(S, 1):
                f = f'/home/claude/bmp/work/{tag}_{i:02d}.html'; open(f, 'w').write(C.shell(i, len(S), body).replace('<style>','<style>div,p{text-wrap:balance}'))
                await pg.goto('file://' + f); await pg.wait_for_timeout(250)
                h = await pg.evaluate('document.body.scrollHeight')
                if h > 1350: print(tag, i, 'overflow', h)
                # orphan check: last line of the answer block
                orphan = await pg.evaluate('''() => {const d=[...document.querySelectorAll('div')].find(x=>x.style.textTransform==='uppercase'); if(!d) return null;
                  const r=document.createRange(); const words=[]; const w=document.createTreeWalker(d,NodeFilter.SHOW_TEXT);
                  let n; while(n=w.nextNode()){const re=/\\S+/g; let m; while(m=re.exec(n.data)){r.setStart(n,m.index); r.setEnd(n,m.index+m[0].length); words.push(r.getBoundingClientRect().top)}}
                  if(words.length<2) return null; const last=words[words.length-1]; return words.filter(t=>Math.abs(t-last)<5).length}''')
                if orphan == 1: print(tag, i, 'ORPHAN last word')
                await pg.screenshot(path=f'/home/claude/bmp/work/BMP_{tag}_QA_{i:02d}.png')
            ims = [Image.open(f'/home/claude/bmp/work/BMP_{tag}_QA_{i:02d}.png') for i in range(1, len(S) + 1)]
            s = Image.new('RGB', (5 * 324, 2 * 405), (250, 249, 247))
            for i, m in enumerate(ims): s.paste(m.resize((324, 405)), (324 * (i % 5), 405 * (i // 5)))
            s.save(f'/home/claude/bmp/work/Preview_{tag}.png')
        await b.close()
asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None)); print('done')
