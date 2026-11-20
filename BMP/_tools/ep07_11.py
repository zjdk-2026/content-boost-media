import bmp_core as C
from bmp_core import qa
import asyncio, sys
from playwright.async_api import async_playwright
from PIL import Image
from ep_helpers import cover, end

EPS = {
 'EP07_DavidRyall': ('EP 07 · DAVID RYALL', [
  cover('07', '$250K IN DEBT.<br>3 WEEKS FROM CASH.', 'THEN HE GOT<br><span class="o">CONTROL OF IT.</span>', 'David Ryall', 'Helps business owners grow their net worth', 7, 'HIS'),
  qa(1, 'What was your breakthrough moment?', 'I got $250,000 in debt in the business with <span class="o">three weeks</span> before any cash was going to come in.', 58,
     note='His school photography business<br>had huge money in and huge money out.'),
  qa(2, 'What did you do differently?', 'Looking at every single expense<br><span class="o">extremely tightly.</span>', 74),
  qa(3, 'How did that change your finances?', 'When people are used to being in debt, even if they zero it out, they get back in debt <span class="o">pretty easily.</span>', 58,
     note='So he changed his set point.'),
  qa(4, 'What advice would you give someone<br>struggling right now?', 'If it\'s a revenue issue, my advice around that is to <span class="o">focus on the customer.</span>', 62),
  qa(5, 'If you could go back,<br>what would you change?', 'Just sorting out the money <span class="o">earlier.</span>', 62,
     note='He did no investing in 15 years<br>of running the business.'),
  qa(6, 'Will technology change<br>money management?', 'If you understand the fundamentals of your own money, you may use technology to <span class="o">augment it.</span>', 60),
  qa(7, 'What challenge would you give<br>the audience?', 'If your income was cut off,<br><span class="o">how long<br>do you last?</span>', 76,
     note='List every account and every debt<br>in one spreadsheet. Update it monthly.'),
  end('DAVID', 'RYALL')]),
 'EP08_MattCrowe': ('EP 08 · MATT CROWE', [
  cover('08', 'HE MADE MILLIONS.<br>HE LOST MILLIONS.', 'THEN HE<br><span class="o">REDEFINED WEALTH.</span>', 'Matt Crowe', 'Tech founder, angel investor and CEO coach', 7, 'HIS'),
  qa(1, 'What were your biggest<br>breakthrough moments?', 'It was a selfish act of me to not<br><span class="o">share my message.</span>', 74),
  qa(2, 'What did you realise<br>about yourself?', 'I\'m overworking or undercharging... from a place of <span class="o">lack of self-worth.</span>', 66),
  qa(3, 'What did success mean<br>to you back then?', 'The old definition was definitely around a <span class="o">money target.</span>', 74),
  qa(4, 'And what does it mean now?', 'Community and friendships. Time freedom, location freedom and <span class="o">mental freedom.</span>', 62,
     note='He used to work 100 hours a week.<br>Now his goal is to work till noon.'),
  qa(5, 'How will AI change<br>your industry?', 'AI will continue to <span class="o">eat everything.</span>', 88),
  qa(6, 'If you could go back,<br>what would you change?', 'I would have pursued more of the creative stuff without thinking about <span class="o">impressing<br>other people.</span>', 58),
  qa(7, 'What challenge would you give<br>the audience?', 'Turn around.<br>Look at them.<br><span class="o">Deal with it.</span>', 92,
     note='When the hard, scary things chase you,<br>stop running and face them.'),
  end('MATT', 'CROWE')]),
 'EP09_LeeBroders': ('EP 09 · LEE BRODERS', [
  cover('09', '6 MONTHS FOR HIS<br>FIRST CLIENT.', 'HE <span class="o">KEPT GOING.</span>', 'Lee Broders', 'British Army veteran and business mentor', 7, 'HIS'),
  qa(1, 'What were your breakthrough<br>moments?', 'Resilience.<br>It\'s a skill that<br><span class="o">you can learn.</span>', 88,
     note='Something he learned in the military.'),
  qa(2, 'How did the Army teach it?', 'Learning to be comfortable <span class="o">being uncomfortable.</span>', 58),
  qa(3, 'When did resilience pay off<br>for you?', 'It took me six months to get my <span class="o">first paying client.</span>', 74,
     note='After burnout he trained as a life coach.<br>At first, no one came.'),
  qa(4, 'If you could go back,<br>what would you change?', 'It\'s about enjoying the journey, not racing to the <span class="o">destination.</span>', 70,
     note='He would not change a thing.<br>He is happy with who he is.'),
  qa(5, 'How will AI change<br>your industry?', 'Use them as a tool and not as <span class="o">a crutch.</span>', 88),
  qa(6, 'What\'s your advice<br>for entrepreneurs?', 'Nothing\'s going to change until I take <span class="o">action on my knowledge.</span>', 74),
  qa(7, 'What challenge would you give<br>the audience?', 'That dream then becomes a <span class="o">goal.</span>', 88,
     note='Write down the biggest dream<br>you can think of.'),
  end('LEE', 'BRODERS')]),
 'EP10_MichaelMarcial': ('EP 10 · MICHAEL MARCIAL', [
  cover('10', 'HOMELESS.<br>SLEEPING IN HIS CAR.', 'THEN HIS DAUGHTER<br>ASKED <span class="o">ONE QUESTION.</span>', 'Michael Marcial', 'Founder, High Ticket Accelerator', 8, 'HIS'),
  qa(1, 'What were your breakthrough<br>moments?', 'That three-month period where I slept in my car was absolutely <span class="o">everything.</span>', 56),
  qa(2, 'How did you get out of<br>living in your car?', 'Why don\'t you just make<br><span class="o">more money?</span>', 86,
     note='What his two-year-old daughter asked him,<br>looking at him in the rear view mirror.'),
  qa(3, 'What happened after that?', 'That weekend was five yeses at <span class="o">$1,000.</span>', 84,
     note='A tenth of his biggest year<br>as an entrepreneur, in one weekend.'),
  qa(4, 'What advice do you have for people<br>on the brink?', 'The obstacle isn\'t really<br><span class="o">an obstacle.</span>', 84),
  qa(5, 'How has your mindset changed?', 'My bank account and my self-worth<br><span class="o">were equal.</span>', 74,
     note='Now more of his bandwidth goes<br>to his relationships.'),
  qa(6, 'How will AI change<br>your industry?', 'AI is going to help a lot of people that are <span class="o">scared to talk to people.</span>', 64),
  qa(7, 'What\'s your most important<br>message?', 'Nobody has it<br><span class="o">figured out.</span>', 96),
  qa(8, 'What challenge would you give<br>the audience?', 'Have your own<br><span class="o">rear view<br>mirror moment.</span>', 88,
     note='Look yourself in the mirror<br>and make that promise.'),
  end('MICHAEL', 'MARCIAL')]),
 'EP11_MarilenCrump': ('EP 11 · MARILEN CRUMP', [
  cover('11', 'SHE SOLD A DRAWING<br>FOR 50 CENTS.', '<span class="o">24 YEARS</span><br>IN BUSINESS SINCE.', 'Marilen Crump', 'Entrepreneur and expert dream catcher', 8, 'HER'),
  qa(1, 'What were your breakthrough<br>moments?', 'I got started over an <span class="o">ice cream sandwich</span> in middle school.', 70),
  qa(2, 'How did that shape your mindset?', 'You\'re okay if you want to live a <span class="o">different path.</span>', 74,
     note='She was a people pleaser who never<br>wanted to disappoint her parents.'),
  qa(3, 'And your biggest aha moment since?', '<span class="o">D</span>irection. <span class="o">R</span>elinquishing.<br><span class="o">E</span>fficiency. <span class="o">A</span>ction.<br><span class="o">M</span>omentum.', 70,
     note='Her DREAM system, worked out<br>while chasing a total eclipse.'),
  qa(4, 'What\'s your advice for entrepreneurs<br>seeking a breakthrough?', 'Perfection isn\'t real. Fail amongst <span class="o">people who love you.</span>', 74),
  qa(5, 'If you could go back,<br>what would you change?', 'Just get started.<br>Do it early.<br><span class="o">Fail early.</span>', 92),
  qa(6, 'How will AI change<br>your industry?', 'Building a community is even more pertinent <span class="o">right now.</span>', 72),
  qa(7, 'What\'s your most important<br>message?', 'How kind was I to somebody who may not be having a <span class="o">good day?</span>', 66),
  qa(8, 'What challenge would you give<br>the audience?', 'One day is the past. One day is what you\'re doing now. <span class="o">One day is the future.</span>', 60,
     note='Shut yourself off from the world for<br>three days and take a full assessment.'),
  end('MARILEN', 'CRUMP')]),
}

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
