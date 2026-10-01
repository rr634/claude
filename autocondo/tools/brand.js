// Generates the 8 AT RIO logo files (monoline, no font dependency).
// The "8" is the building section: a 14′ garage loop below, an 8′ mezzanine loop above,
// and the mezzanine slab between them drawn in Glow. 14 + 8 = the 22′ building height.
// Run: node autocondo/tools/brand.js   → writes autocondo/site/assets/brand/*.svg
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, '..', 'site', 'assets', 'brand');

const C = { bone: '#EFEBE4', ink: '#121211', glow: '#D3A462', black: '#0C0C0B' };
const f = n => +n.toFixed(2);

// Rounded-rect path (open stroke)
const rr = (x, y, w, h, r) => `M${f(x+r)} ${f(y)}H${f(x+w-r)}A${r} ${r} 0 0 1 ${f(x+w)} ${f(y+r)}V${f(y+h-r)}A${r} ${r} 0 0 1 ${f(x+w-r)} ${f(y+h)}H${f(x+r)}A${r} ${r} 0 0 1 ${f(x)} ${f(y+h-r)}V${f(y+r)}A${r} ${r} 0 0 1 ${f(x+r)} ${f(y)}Z`;

// The 8 glyph. Returns {d (loops), slab (line), w, h}
function eight(H, sw) {
  const up = H * 8 / 22, lo = H * 14 / 22;
  const lw = H * 0.58, uw = H * 0.48;
  const x0 = 0, ux = (lw - uw) / 2;
  const d = rr(ux + sw/2, sw/2, uw - sw, up, Math.min(up/2, uw*0.36)) + ' ' + rr(x0 + sw/2, up + sw/2, lw - sw, lo - sw, Math.min(lo*0.38, lw*0.38));
  const slab = `M${f(ux + sw/2)} ${f(up + sw/2)}H${f(ux + uw - sw/2)}`;
  return { d, slab, w: lw, h: H };
}

// Monoline capitals on a cap height H, starting at x, baseline y. Returns {d, adv}
function glyph(ch, x, y, H) {
  const t = y - H;
  switch (ch) {
    case 'A': { const w = H * 1.02; return { d: `M${f(x)} ${f(y)}L${f(x+w/2)} ${f(t)}L${f(x+w)} ${f(y)}M${f(x+w*0.2)} ${f(y-H*0.38)}H${f(x+w*0.8)}`, adv: w }; }
    case 'T': { const w = H * 0.92; return { d: `M${f(x)} ${f(t)}H${f(x+w)}M${f(x+w/2)} ${f(t)}V${f(y)}`, adv: w }; }
    case 'R': { const w = H * 0.86, b = H * 0.52, r = b / 2;
      return { d: `M${f(x)} ${f(y)}V${f(t)}H${f(x+w-r)}A${f(r)} ${f(r)} 0 0 1 ${f(x+w-r)} ${f(t+b)}H${f(x)}M${f(x+w*0.55)} ${f(t+b)}L${f(x+w)} ${f(y)}`, adv: w }; }
    case 'I': return { d: `M${f(x)} ${f(t)}V${f(y)}`, adv: 0 };
    case 'O': { const w = H * 1.22; return { d: rr(x, t, w, H, H * 0.42), adv: w }; }
    case ' ': return { d: '', adv: H * 0.55 };
  }
}
function word(str, x, y, H, track) {
  let d = '', cx = x;
  for (const ch of str) { const g = glyph(ch, cx, y, H); d += g.d + ' '; cx += g.adv + (ch === ' ' ? 0 : track); }
  return { d: d.trim(), w: cx - track - x };
}

function svg(w, h, body, label) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${f(w)} ${f(h)}" width="${f(w)}" height="${f(h)}" role="img" aria-label="${label}">\n${body}\n</svg>\n`;
}
const strokeAttrs = (c, sw) => `fill="none" stroke="${c}" stroke-width="${sw}" stroke-linecap="square" stroke-linejoin="miter"`;

// ---------- Horizontal lockup: [8] AT RIO
function horizontal(color, glow) {
  const sw = 2.6, H8 = 72, cap = 34, pad = 2;
  const e = eight(H8, sw);
  const gap = 26, track = 15;
  const wd = word('AT RIO', e.w + gap, H8 - sw/2, cap, track);
  const W = e.w + gap + wd.w + pad * 2 + sw;
  const body = `<g transform="translate(${pad} ${pad})" ${strokeAttrs(color, sw)}>
  <path d="${e.d}"/>
  <path d="${e.slab}" stroke="${glow}"/>
  <path d="${wd.d}"/>
</g>`;
  return svg(W, H8 + pad * 2, body, '8 AT RIO');
}
// ---------- Stacked lockup
function stacked(color, glow) {
  const sw = 2.6, H8 = 110, cap = 26, track = 13;
  const e = eight(H8, sw);
  const wd = word('AT RIO', 0, 0, cap, track);
  const W = Math.max(e.w, wd.w) + 8;
  const ex = (W - e.w) / 2, wx = (W - wd.w) / 2, wy = H8 + 26 + cap;
  const wd2 = word('AT RIO', wx, wy, cap, track);
  const body = `<g ${strokeAttrs(color, sw)}>
  <g transform="translate(${f(ex)} 2)"><path d="${e.d}"/><path d="${e.slab}" stroke="${glow}"/></g>
  <path d="${wd2.d}"/>
</g>`;
  return svg(W, wy + 4, body, '8 AT RIO');
}
// ---------- Monogram (8 alone)
function monogram(color, glow, bg) {
  const sw = 3, H8 = 88, P = 20;
  const e = eight(H8, sw);
  const S = H8 + P * 2;
  const body = `${bg ? `<rect width="${S}" height="${S}" fill="${bg}"/>` : ''}
<g transform="translate(${f((S - e.w) / 2)} ${P})" ${strokeAttrs(color, sw)}><path d="${e.d}"/><path d="${e.slab}" stroke="${glow}"/></g>`;
  return svg(S, S, body, '8 AT RIO monogram');
}
// ---------- Favicon (heavier stroke for small sizes)
function favicon() {
  const sw = 3.4, H8 = 24, S = 32;
  const e = eight(H8, sw);
  return svg(S, S, `<rect width="32" height="32" rx="6" fill="${C.black}"/>
<g transform="translate(${f((S - e.w) / 2)} 4)" ${strokeAttrs(C.bone, sw)}><path d="${e.d}"/><path d="${e.slab}" stroke="${C.glow}"/></g>`, '8 AT RIO');
}

const files = {
  'logo-horizontal-light.svg': horizontal(C.bone, C.glow),
  'logo-horizontal-dark.svg': horizontal(C.ink, C.glow),
  'logo-stacked-light.svg': stacked(C.bone, C.glow),
  'logo-stacked-dark.svg': stacked(C.ink, C.glow),
  'monogram-light.svg': monogram(C.bone, C.glow),
  'monogram-dark.svg': monogram(C.ink, C.glow),
  'monogram-tile.svg': monogram(C.bone, C.glow, C.black),
};
fs.mkdirSync(OUT, { recursive: true });
for (const [n, s] of Object.entries(files)) fs.writeFileSync(path.join(OUT, n), s);
fs.writeFileSync(path.join(OUT, '..', 'favicon.svg'), favicon());
// Exported for inlining into pages
if (require.main !== module) module.exports = { files, horizontal, stacked, monogram, C };
console.log('wrote', Object.keys(files).length + 1, 'files');
