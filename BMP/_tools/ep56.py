import bmp_core as C
from bmp_core import qa, O, INK, GREY
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

def cover(ep, l1, l2, name, role, n, pron):
    return f'''<div style="font-size:28px;font-weight:800;letter-spacing:5px;color:{GREY}">EPISODE {ep}</div>
<div style="margin-top:36px;font-size:74px;line-height:1.1;font-weight:900">{l1}</div>
<div style="margin-top:24px;font-size:74px;line-height:1.1;font-weight:900">{l2}</div>
<p style="margin-top:50px;font-size:42px;line-height:1.3;font-weight:700;color:{GREY}">My conversation with<br><span style="color:{INK};font-weight:800">{name}</span></p>
<p style="margin-top:10px;font-size:32px;font-weight:600;color:{GREY}">{role}</p>
<div style="margin-top:40px;display:inline-block;border:3px solid {O};border-radius:50px;padding:16px 34px;font-size:30px;font-weight:800;letter-spacing:2px">{n} QUESTIONS. {pron} BEST ANSWERS.</div>'''

def end(first, last):
    return f'''<div style="font-size:40px;font-weight:700;color:{GREY}">Watch the full episode with</div>
<div style="margin-top:14px;font-size:84px;line-height:1.05;font-weight:900">{first}<br>{last}</div>
<div style="margin-top:60px;background:{O};color:{INK};border-radius:60px;padding:30px 54px;font-size:46px;font-weight:900">COMMENT “YOUTUBE”</div>
<p style="margin-top:30px;font-size:38px;font-weight:700;color:{GREY}">and I’ll send you the link.</p>'''

EPS = {
 'EP05_JeromeLamarque': ('EP 05 · JEROME LAMARQUE', [
  cover('05', 'HE KEPT CHANGING<br>WHAT HE DID.', 'THEN HE FOUND<br><span class="o">HIS GIFT.</span>', 'Jerome Lamarque', 'High performance and leadership coach', 7, 'HIS'),
  qa(1, 'What was your biggest breakthrough moment?', 'There is no such thing as <span class="o">common sense.</span> There\'s only things that are common to people\'s senses.', 62),
  qa(2, 'How did that change your business?', 'I don\'t actually think I\'ve got a business. I just think I\'m a <span class="o">teacher.</span>', 72),
  qa(3, 'How can someone start aligning<br>to their purpose?', 'If you do what you do for money, you\'re probably not <span class="o">sharing your gift</span> with the world.', 66),
  qa(4, 'What\'s the future of your industry?', 'No one wants to be controlled. Everyone wants to be <span class="o">inspired.</span>', 76),
  qa(5, 'If you went back in time,<br>what would you change?', 'Never give your children advice <span class="o">unless they ask for it.</span>', 64,
     note='The one thing he would change:<br>the way he parented.'),
  qa(6, 'What advice would you give<br>entrepreneurs today?', 'Find out <span class="o">why you were born,</span> as quick as possible.', 76),
  qa(7, 'What\'s your next big breakthrough?', 'Our external world is only a reflection of our <span class="o">internal world.</span>', 70),
  end('JEROME', 'LAMARQUE')]),
 'EP06_YvetteSalvaris': ('EP 06 · YVETTE SALVARIS', [
  cover('06', 'NO ONE\'S COMING<br>TO SAVE YOU.', '<span class="o">9 YEARS</span> RUNNING<br>HER OWN BUSINESS.', 'Yvette Salvaris', 'Owner, Ethical Training Solutions', 8, 'HER'),
  qa(1, 'What was your breakthrough moment?', 'I can really make a <span class="o">difference</span> to the care industry.', 80),
  qa(2, 'Any other breakthrough moments?', 'This is working.<br><span class="o">I can do this.</span>', 96,
     note='When her first class of child care<br>students graduated.'),
  qa(3, 'Did it change your mindset<br>on business?', 'I knew I could do it,<br>but it took me a while<br>to <span class="o">understand<br>that I could.</span>', 60),
  qa(4, 'Any advice for anyone<br>in your position?', 'Don\'t listen to people. Do what you feel is <span class="o">right.</span>', 80,
     note='A lot of people did not take her<br>seriously when she started.'),
  qa(5, 'What\'s been your big mindset shift?', '<span class="o">No one\'s coming to save you</span> when you run your own business.', 74),
  qa(6, 'What\'s your message to people<br>in the care industry?', 'Do it because<br>you <span class="o">love it.</span>', 96),
  qa(7, 'What\'s one action to take today?', 'Just get off your butt.<br><span class="o">Try it out.</span>', 88),
  qa(8, 'If you started again,<br>what would you change?', 'I wouldn\'t<br><span class="o">change a thing.</span>', 96,
     note='Her mistakes taught her something new.'),
  end('YVETTE', 'SALVARIS')]),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for tag, (foot, S) in EPS.items():
            C.FOOT = foot
            for i, body in enumerate(S, 1):
                f = f'./{tag}_{i:02d}.html'; open(f, 'w').write(C.shell(i, len(S), body))
                await pg.goto('file://' + f); await pg.wait_for_timeout(250)
                h = await pg.evaluate('document.body.scrollHeight')
                if h > 1350: print(tag, i, 'overflow', h)
                await pg.screenshot(path=f'./BMP_{tag}_QA_{i:02d}.png')
            ims = [Image.open(f'./BMP_{tag}_QA_{i:02d}.png') for i in range(1, len(S) + 1)]
            s = Image.new('RGB', (5 * 324, 2 * 405), (250, 249, 247))
            for i, m in enumerate(ims): s.paste(m.resize((324, 405)), (324 * (i % 5), 405 * (i // 5)))
            s.save(f'./Preview_{tag}.png')
        await b.close()
asyncio.run(main()); print('done')
