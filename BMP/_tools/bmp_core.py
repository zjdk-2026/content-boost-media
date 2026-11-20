O='#FF9200'; INK='#111111'; GREY='#8A8A8A'; BG='#FAF9F7'
FOOT=''
def shell(page,total,body):
    bars=''.join(f'<div style="flex:1;height:7px;border-radius:4px;background:{O if i<page else "rgba(17,17,17,0.10)"}"></div>' for i in range(total))
    swipe='' if page==total else f'<div style="display:flex;align-items:center;gap:12px;font-size:24px;font-weight:800;letter-spacing:3px;color:{INK}">SWIPE <svg width="32" height="18" viewBox="0 0 34 20" fill="none"><path d="M2 10h28M22 2l8 8-8 8" stroke="{O}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
    top='<img src="logo_black.png" style="height:132px">' if page==1 else ''
    foot='' if page==1 else '<img src="logo_black.png" style="height:104px">'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:M;src:url(Montserrat.ttf);font-weight:100 900}}
body{{margin:0}} p{{margin:0}} .o{{color:{O}}}
</style></head><body>
<div style="width:1080px;height:1350px;box-sizing:border-box;position:relative;overflow:hidden;background:{BG};font-family:M,sans-serif;color:{INK};padding:64px 96px 60px;display:flex;flex-direction:column;align-items:center;text-align:center">
{top}
<div style="flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;width:100%">{body}</div>
<div style="width:100%;display:flex;flex-direction:column;gap:22px">
<div style="display:flex;justify-content:space-between;align-items:center"><div style="display:flex;align-items:center;gap:20px">{foot}<div style="font-size:24px;font-weight:800;letter-spacing:3px;color:{GREY}">{FOOT}</div></div>{swipe}</div>
<div style="display:flex;gap:8px">{bars}</div></div></div></body></html>'''
def qa(num,q,a,size=76,note=None,quote=True):
    n=f'<p style="margin-top:34px;font-size:32px;font-weight:600;color:{GREY}">{note}</p>' if note else ''
    mark=f'<div style="margin-top:40px;font-size:200px;line-height:.55;font-weight:900;color:{O};height:80px">&#8220;</div>' if quote else '<div style="height:44px"></div>'
    return f'''<div style="display:inline-flex;align-items:center;gap:14px;font-size:24px;font-weight:800;letter-spacing:4px;color:#fff;background:{INK};padding:10px 24px 10px 10px;border-radius:30px"><span style="background:{O};color:{INK};border-radius:50%;width:38px;height:38px;display:inline-flex;align-items:center;justify-content:center;letter-spacing:0;font-size:22px">{num}</span>ZAC ASKED</div>
<p style="margin-top:26px;font-size:38px;line-height:1.3;font-weight:600;color:{GREY}">{q}</p>
{mark}
<div style="margin-top:22px;font-size:{size}px;line-height:1.13;font-weight:800;text-transform:uppercase">{a}</div>
<div style="margin-top:40px;width:90px;height:8px;background:{O};border-radius:4px"></div>{n}'''
