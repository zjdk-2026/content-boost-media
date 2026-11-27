// Content Boost in-browser reel renderer (Chrome). Renders 720x1280 branded reel from a 9:16 source blob.
window.CB = window.CB || {};
CB.W = 720; CB.H = 1280;
CB.BR = {
  delel: {dark: '#133433', light: '#DDDEDA', box: '#133433', boxText: '#FFFFFF', display: '600 60px "CBCorm"', dispFam: 'CBCorm', dispW: 600, label: 'CBInter', labelW: 600, cap: 'CBArimo', capW: 700, capSize: 44, upperHook: false, dot: false, grid: false},
  bmp: {dark: '#0C0C0C', light: '#FF9200', box: '#FF9200', boxText: '#0C0C0C', dispFam: 'CBMont', dispW: 800, label: 'CBMontS', labelW: 600, cap: 'CBMont', capW: 800, capSize: 42, upperHook: true, dot: true, grid: true},
};
CB.loadFonts = async () => {
  const J = 'https://cdn.jsdelivr.net/npm/@fontsource/';
  const F = [['CBArimo', 'arimo/files/arimo-latin-700-normal.woff2', 700], ['CBCorm', 'cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2', 600],
    ['CBInter', 'inter/files/inter-latin-600-normal.woff2', 600], ['CBMont', 'montserrat/files/montserrat-latin-800-normal.woff2', 800],
    ['CBMontS', 'montserrat/files/montserrat-latin-600-normal.woff2', 600]];
  for (const [n, p, w] of F) {
    const buf = await (await fetch(J + p.replace('/files', '@5/files'))).arrayBuffer();
    const ff = new FontFace(n, buf, {weight: String(w)}); await ff.load(); document.fonts.add(ff);
  }
  return [...document.fonts].map(f => f.family + ':' + f.status);
};
CB.ease = x => { x = Math.max(0, Math.min(1, x)); return 1 - Math.pow(1 - x, 3); };
CB.font = (fam, w, s) => `${w} ${s}px "${fam}"`;
CB.textC = (ctx, txt, y, font, fill, opts = {}) => {
  ctx.font = font; ctx.textBaseline = 'alphabetic';
  const sp = opts.sp || 0;
  if (sp) { ctx.letterSpacing = sp + 'px'; } else { ctx.letterSpacing = '0px'; }
  const w = ctx.measureText(txt).width - (sp ? sp : 0);
  const x = (CB.W - w) / 2;
  if (opts.stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = opts.stroke; ctx.strokeStyle = opts.strokeCol || 'rgba(0,0,0,0.85)'; ctx.strokeText(txt, x, y); }
  if (opts.shadow) { ctx.shadowColor = 'rgba(0,0,0,0.6)'; ctx.shadowBlur = 12; }
  ctx.fillStyle = fill; ctx.fillText(txt, x, y);
  ctx.shadowBlur = 0; ctx.letterSpacing = '0px';
  return w;
};
CB.drawFrame = (ctx, vid, t, c) => {
  const W = CB.W, H = CB.H;
  const k = (c.joins || []).filter(j => j <= t).length;
  const z = k % 2 ? (c.flip || 1.08) : 1.0;
  const vw = vid.videoWidth, vh = vid.videoHeight;
  if (c.hook && t < c.hook.until) { // hook layout: brand panel on top, speaker window below
    const top = c.hook.win || 430; ctx.fillStyle = CB.BR[c.brand].dark; ctx.fillRect(0, 0, W, top);
    const sh = (H - top) * vw / W; const sy0 = Math.max(0, Math.min(vh - sh, vh * 0.30 - sh * 0.30));
    ctx.drawImage(vid, 0, sy0, vw, sh, 0, top, W, H - top); return;
  }
  const cw = vw / z, ch = vh / z, fy = c.faceY || 0.40;
  const sx = (vw - cw) / 2, sy = Math.max(0, Math.min(vh - ch, vh * fy - ch * fy));
  ctx.drawImage(vid, sx, sy, cw, ch, 0, 0, W, H);
};
CB.hook = (ctx, t, c, B) => {
  const hk = c.hook; if (!hk || t >= hk.until) return;
  const a = CB.ease(t / 0.25);
  ctx.globalAlpha = a;
  let y = hk.y || 170;
  if (hk.kicker) { CB.textC(ctx, hk.kicker, y, CB.font(B.label, B.labelW, 22), B.light, {sp: 4, shadow: 1}); y += 64; }
  const lines = hk.lines.map(l => B.upperHook ? l.toUpperCase() : l);
  let hs = hk.size || (B.upperHook ? 56 : 68);
  ctx.font = CB.font(B.dispFam, B.dispW, hs);
  while (hs > 34 && Math.max(...lines.map(l => ctx.measureText(l).width)) > 620) { hs -= 2; ctx.font = CB.font(B.dispFam, B.dispW, hs); }
  lines.forEach((l, i) => {
    const w = CB.textC(ctx, l, y, CB.font(B.dispFam, B.dispW, hs), '#FFFFFF', {shadow: 1});
    if (B.dot && i === lines.length - 1 && !/[.?!]$/.test(l)) { ctx.fillStyle = B.box; ctx.fillText('.', (CB.W + w) / 2 + 2, y); }
    y += hs * 1.12;
  });
  ctx.globalAlpha = 1;
};
CB.caps = (ctx, t, c, B, y) => {
  const pg = c.pages.find(p => p.t0 <= t && t < p.t1); if (!pg) return;
  const f = CB.font(B.cap, B.capW, B.capSize); ctx.font = f; const gap = 14;
  const ws = pg.words.map(w => ctx.measureText(w.d).width);
  let x = (CB.W - (ws.reduce((a, b) => a + b, 0) + gap * (ws.length - 1))) / 2;
  const asc = B.capSize * 0.72;
  pg.words.forEach((w, i) => {
    const act = w.t0 <= t && t < w.e;
    if (act) {
      ctx.fillStyle = B.box; ctx.beginPath(); ctx.roundRect(x - 10, y - asc - 12, ws[i] + 20, asc + 24, 8); ctx.fill();
      ctx.fillStyle = B.boxText; ctx.fillText(w.d, x, y);
    } else {
      ctx.lineJoin = 'round'; ctx.lineWidth = 6; ctx.strokeStyle = '#000'; ctx.strokeText(w.d, x, y);
      ctx.fillStyle = '#FFF'; ctx.fillText(w.d, x, y);
    }
    x += ws[i] + gap;
  });
};
CB.bg = (ctx, src, B, blur, dim) => {
  ctx.save(); ctx.filter = `blur(${blur}px) brightness(${dim})`; ctx.drawImage(src, -40, -40, CB.W + 80, CB.H + 80); ctx.restore();
  if (false) { ctx.strokeStyle = 'rgba(255,255,255,0.04)'; ctx.lineWidth = 1; for (let g = 0; g < CB.W; g += 60) { ctx.beginPath(); ctx.moveTo(g, 0); ctx.lineTo(g, CB.H); ctx.stroke(); } for (let g = 0; g < CB.H; g += 60) { ctx.beginPath(); ctx.moveTo(0, g); ctx.lineTo(CB.W, g); ctx.stroke(); } }
};
CB.card = (ctx, cd, t, B, src) => {
  const lt = t - cd.t, a = CB.ease(lt / 0.22);
  ctx.fillStyle = B.dark; ctx.fillRect(0, 0, CB.W, CB.H);
  ctx.globalAlpha = 0.35; CB.bg(ctx, src, B, 26, 0.5); ctx.globalAlpha = 1;
  ctx.fillStyle = B.dark; ctx.globalAlpha = 0.55; ctx.fillRect(0, 0, CB.W, CB.H); ctx.globalAlpha = 1;
  if (B.grid) { ctx.strokeStyle = 'rgba(255,255,255,0.05)'; ctx.lineWidth = 1; for (let g = 0; g < CB.W; g += 60) { ctx.beginPath(); ctx.moveTo(g, 0); ctx.lineTo(g, CB.H); ctx.stroke(); } for (let g = 0; g < CB.H; g += 60) { ctx.beginPath(); ctx.moveTo(0, g); ctx.lineTo(CB.W, g); ctx.stroke(); } }
  ctx.globalAlpha = a;
  const lines = cd.big.split('\n'); let sz = cd.size || 96;
  const big = B.upperHook ? lines.map(l => l.toUpperCase()) : lines;
  ctx.font = CB.font(B.dispFam, B.dispW, sz);
  while (sz > 40 && Math.max(...big.map(l => ctx.measureText(l).width)) > 620) { sz -= 4; ctx.font = CB.font(B.dispFam, B.dispW, sz); }
  let y = (cd.y || 560) - (big.length - 1) * sz * 0.6 + (1 - a) * 24;
  if (cd.kicker) CB.textC(ctx, cd.kicker, y - sz - 10, CB.font(B.label, B.labelW, 24), B.light, {sp: 4});
  big.forEach((l, i) => { const w = CB.textC(ctx, l, y, CB.font(B.dispFam, B.dispW, sz), '#FFFFFF');
    if (B.dot && i === big.length - 1 && !/[.?!%]$/.test(l)) { ctx.fillStyle = B.box; ctx.fillText('.', (CB.W + w) / 2 + 2, y); } y += sz * 1.15; });
  if (cd.small) { ctx.fillStyle = B.light; ctx.fillRect(CB.W / 2 - 30, y - sz * 0.45, 60, 3); CB.textC(ctx, cd.small, y + 10, CB.font(B.label, B.labelW, 28), B.light, {sp: 2}); }
  ctx.globalAlpha = 1;
};
CB.endcard = (ctx, last, t, c, B) => {
  const a = CB.ease(t / 0.25);
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, CB.W, CB.H);
  CB.bg(ctx, last, {grid: false}, 22, 0.35);
  ctx.globalAlpha = a; let y = 500 + (1 - a) * 20;
  CB.textC(ctx, 'COMMENT', y, CB.font(B.label, B.labelW, 34), '#FFFFFF', {sp: 4});
  const f = CB.font('CBArimo', 700, 88); ctx.font = f; const w = ctx.measureText('PODCAST').width;
  const by = y + 40; ctx.fillStyle = B.box; ctx.beginPath(); ctx.roundRect((CB.W - w) / 2 - 30, by, w + 60, 110, 14); ctx.fill();
  ctx.fillStyle = B.boxText; ctx.fillText('PODCAST', (CB.W - w) / 2, by + 86);
  CB.textC(ctx, c.endLine || 'FOR THE FULL EPISODE', by + 170, CB.font(B.label, B.labelW, 26), '#FFFFFF', {sp: 3});
  if (c.brand === 'bmp') CB.textC(ctx, 'THE BREAKTHROUGH MOMENT PODCAST', 1090, CB.font(B.label, B.labelW, 18), B.light, {sp: 4});
  ctx.globalAlpha = 1;
};
CB.loudGain = async (blob, end, target) => {
  const ac = new AudioContext(); const buf = await ac.decodeAudioData(await blob.arrayBuffer()); ac.close();
  const sr = buf.sampleRate, n = Math.min(buf.length, Math.floor(end * sr));
  const off = new OfflineAudioContext(buf.numberOfChannels, n, sr); const s = off.createBufferSource(); s.buffer = buf;
  const hs = off.createBiquadFilter(); hs.type = 'highshelf'; hs.frequency.value = 1500; hs.gain.value = 4;
  const hp = off.createBiquadFilter(); hp.type = 'highpass'; hp.frequency.value = 38; hp.Q.value = 0.5;
  s.connect(hs); hs.connect(hp); hp.connect(off.destination); s.start(); const r = await off.startRendering();
  const blk = Math.floor(0.4 * sr), hop = Math.floor(0.1 * sr), ms = [];
  for (let i = 0; i + blk <= n; i += hop) { let z = 0; for (let ch = 0; ch < r.numberOfChannels; ch++) { const d = r.getChannelData(ch); for (let j = i; j < i + blk; j++) z += d[j] * d[j]; } ms.push(z / blk); }
  const L = m => -0.691 + 10 * Math.log10(m + 1e-12);
  let g = ms.filter(m => L(m) > -70); const rel = L(g.reduce((a, b) => a + b, 0) / g.length) - 10; g = g.filter(m => L(m) > rel);
  const lufs = L(g.reduce((a, b) => a + b, 0) / g.length);
  return {lufs, gain: Math.pow(10, (target - lufs) / 20)};
};
CB.render = async (blob, c) => {
  const B = CB.BR[c.brand]; const W = CB.W, H = CB.H;
  const lg = await CB.loudGain(blob, c.bodyEnd, -14);
  const vid = document.createElement('video'); vid.src = URL.createObjectURL(blob); vid.playsInline = true; vid.preload = 'auto'; vid.style.cssText = 'position:fixed;right:0;bottom:0;width:72px;height:128px;opacity:0.02;z-index:99998'; document.body.appendChild(vid);
  await new Promise(r => vid.onloadeddata = r); vid.currentTime = 0; await new Promise(r => vid.onseeked = r);
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H; const ctx = cv.getContext('2d');
  cv.style.cssText = 'position:fixed;left:0;top:0;height:90vh;z-index:99999;background:#000'; document.body.appendChild(cv);
  const last = document.createElement('canvas'); last.width = W; last.height = H; const lctx = last.getContext('2d');
  const snapC = document.createElement('canvas'); snapC.width = 270; snapC.height = 480;
  const ac = new AudioContext(); const srcN = ac.createMediaElementSource(vid); const gn = ac.createGain(); gn.gain.value = lg.gain;
  const lim = ac.createDynamicsCompressor(); lim.threshold.value = -5; lim.knee.value = 0; lim.ratio.value = 20; lim.attack.value = 0.002; lim.release.value = 0.08;
  const dest = ac.createMediaStreamDestination(); srcN.connect(gn); gn.connect(lim); lim.connect(dest);
  const vs = cv.captureStream(30); const ms = new MediaStream([...vs.getVideoTracks(), ...dest.stream.getAudioTracks()]);
  const mime = 'video/mp4;codecs=avc1.42E01F,mp4a.40.2';
  const rec = new MediaRecorder(ms, {mimeType: mime, videoBitsPerSecond: 8e6, audioBitsPerSecond: 192000}); const chunks = [];
  rec.ondataavailable = e => e.data.size && chunks.push(e.data);
  const snaps = {}; const want = [...(c.snaps || [])];
  const paint = (t) => {
    const cd = (c.cards || []).find(k => k.t <= t && t < k.t + k.dur);
    if (cd) { lctx.drawImage(vid, 0, 0, W, H); CB.card(ctx, cd, t, B, last); }
    else { CB.drawFrame(ctx, vid, t, c); lctx.drawImage(cv, 0, 0); CB.hook(ctx, t, c, B); }
    CB.caps(ctx, t, c, B, cd ? (c.capYCard || 1060) : (c.hook && t < c.hook.until ? (c.capYHook || 1190) : (c.capY || 1000)));
    while (want.length && t >= want[0]) { const k = want.shift(); snapC.getContext('2d').drawImage(cv, 0, 0, 270, 480); snaps[k.toFixed(1)] = snapC.toDataURL('image/jpeg', 0.7); }
  };
  let phase = 'body';
  const onVis = async () => { if (document.hidden) { if (rec.state === 'recording') rec.pause(); if (phase === 'body') vid.pause(); CB.stats && CB.stats.pauses++; }
    else { if (phase === 'body') { await vid.play(); } if (rec.state === 'paused') rec.resume(); } };
  document.addEventListener('visibilitychange', onVis);
  paint(0); rec.start(1000); await ac.resume(); await vid.play();
  await new Promise(res => {
    let done = false; CB.stats = {frames: 0, hidden: 0, pauses: 0, errs: []};
    const tick = () => { if (done) return; const t = vid.currentTime; if (document.hidden) CB.stats.hidden++;
      if (t >= c.bodyEnd || vid.ended) { done = true; clearInterval(iv); res(); return; }
      if (t >= c.bodyEnd - 0.08) gn.gain.setTargetAtTime(0, ac.currentTime, 0.02);
      try { paint(t); CB.stats.frames++; } catch (e) { CB.stats.errs.push(String(e)); } };
    const step = () => { tick(); if (!done) vid.requestVideoFrameCallback(step); };
    vid.requestVideoFrameCallback(step);
    const iv = setInterval(tick, 33);
  });
  vid.pause(); gn.gain.value = 0;
  phase = 'end'; let et = 0, prev = performance.now();
  await new Promise(res => { const iv2 = setInterval(() => { const now = performance.now(); if (!document.hidden) et += (now - prev) / 1000; prev = now;
      if (et >= 2.8) { clearInterval(iv2); res(); return; } CB.endcard(ctx, last, et, c, B);
      if (want.length && want[0] >= c.bodyEnd) { const k = want.shift(); snapC.getContext('2d').drawImage(cv, 0, 0, 270, 480); snaps[k.toFixed(1)] = snapC.toDataURL('image/jpeg', 0.7); } }, 33); });
  document.removeEventListener('visibilitychange', onVis);
  rec.stop(); await new Promise(r => rec.onstop = r);
  const out = new Blob(chunks, {type: 'video/mp4'}); cv.remove(); vid.remove(); ac.close();
  CB.out = CB.out || {}; CB.out[c.name] = out; CB.snaps = CB.snaps || {}; CB.snaps[c.name] = snaps;
  return {name: c.name, stats: CB.stats, size: out.size, lufs: lg.lufs, gain: lg.gain, snaps: Object.keys(snaps)};
};
CB.save = (name) => { const a = document.createElement('a'); a.href = URL.createObjectURL(CB.out[name]); a.download = name + '.mp4'; document.body.appendChild(a); a.click(); a.remove(); return name; };
'CB ready';
