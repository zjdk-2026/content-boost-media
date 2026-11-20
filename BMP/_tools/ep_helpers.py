from bmp_core import O, INK, GREY
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

