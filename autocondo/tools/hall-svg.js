// Generates the one-point-perspective "Hall" illustration used in the hero.
// Run: node autocondo/tools/hall-svg.js > /tmp/hall.svg
const VX = 800, VY = 400;
const s  = t => 1 / (1 + 4 * t);           // depth scale (t: 0 = entry, 1 = far wall)
const wallL = t => VX - 900 * s(t);
const wallR = t => VX + 900 * s(t);
const floorY = t => VY + 520 * s(t);
const ceilY  = t => VY - 480 * s(t);
const yAt = (t, h) => floorY(t) - h * 1000 * s(t);   // h: fraction of 22' hall height
const f = n => n.toFixed(1);
const out = [];
const P = pts => pts.map(p => f(p[0]) + ',' + f(p[1])).join(' ');

out.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Illustration of the covered hall: a polished drive aisle between eight lit glass garage doors, a skylight overhead and a car on a turntable at the far end">
<defs>
  <linearGradient id="hFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1a18"/><stop offset="1" stop-color="#0a0a09"/></linearGradient>
  <linearGradient id="hCeil" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#191816"/><stop offset="1" stop-color="#0c0c0b"/></linearGradient>
  <linearGradient id="hWall" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#121211"/><stop offset="1" stop-color="#1f1e1b"/></linearGradient>
  <linearGradient id="hWallR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#121211"/><stop offset="1" stop-color="#1f1e1b"/></linearGradient>
  <linearGradient id="hGlass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d39c" stop-opacity=".55"/><stop offset=".7" stop-color="#d3a462" stop-opacity=".85"/><stop offset="1" stop-color="#8a6431" stop-opacity=".9"/></linearGradient>
  <linearGradient id="hMezz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3a462" stop-opacity=".18"/><stop offset="1" stop-color="#d3a462" stop-opacity=".38"/></linearGradient>
  <linearGradient id="hRefl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d3a462" stop-opacity=".30"/><stop offset="1" stop-color="#d3a462" stop-opacity="0"/></linearGradient>
  <linearGradient id="hSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fc4d4" stop-opacity=".40"/><stop offset="1" stop-color="#9fc4d4" stop-opacity=".12"/></linearGradient>
  <linearGradient id="hEnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3a46"/><stop offset=".62" stop-color="#7d6a55"/><stop offset=".63" stop-color="#3f7f91"/><stop offset="1" stop-color="#1d3d47"/></linearGradient>
  <radialGradient id="hSpot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#f3d39c" stop-opacity=".45"/><stop offset="1" stop-color="#f3d39c" stop-opacity="0"/></radialGradient>
  <filter id="hBlur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="1600" height="900" fill="#0c0c0b"/>`);

const T0 = -0.04, T1 = 1;
// Planes
out.push(`<polygon points="${P([[wallL(T0),floorY(T0)],[wallR(T0),floorY(T0)],[wallR(T1),floorY(T1)],[wallL(T1),floorY(T1)]])}" fill="url(#hFloor)"/>`);
out.push(`<polygon points="${P([[wallL(T0),ceilY(T0)],[wallR(T0),ceilY(T0)],[wallR(T1),ceilY(T1)],[wallL(T1),ceilY(T1)]])}" fill="url(#hCeil)"/>`);
out.push(`<polygon points="${P([[wallL(T0),ceilY(T0)],[wallL(T1),ceilY(T1)],[wallL(T1),floorY(T1)],[wallL(T0),floorY(T0)]])}" fill="url(#hWall)"/>`);
out.push(`<polygon points="${P([[wallR(T0),ceilY(T0)],[wallR(T1),ceilY(T1)],[wallR(T1),floorY(T1)],[wallR(T0),floorY(T0)]])}" fill="url(#hWallR)"/>`);

// Far wall: glass onto the pool terrace (the one bit of open air)
const ex0 = wallL(1), ex1 = wallR(1), ey0 = ceilY(1), ey1 = floorY(1);
out.push(`<rect x="${f(ex0)}" y="${f(ey0)}" width="${f(ex1-ex0)}" height="${f(ey1-ey0)}" fill="url(#hEnd)"/>`);
for (let i = 1; i < 6; i++) { const x = ex0 + (ex1-ex0)*i/6; out.push(`<line x1="${f(x)}" y1="${f(ey0)}" x2="${f(x)}" y2="${f(ey1)}" stroke="#0c0c0b" stroke-width="2"/>`); }
// palm silhouettes beyond the glass
[[0.18,1],[0.32,.8],[0.74,.95],[0.86,.75]].forEach(([px,k])=>{
  const x = ex0 + (ex1-ex0)*px, base = ey0 + (ey1-ey0)*.62, top = base - 120*k;
  out.push(`<path d="M${f(x)} ${f(base)} Q${f(x+4)} ${f((base+top)/2)} ${f(x+2)} ${f(top)}" stroke="#16201f" stroke-width="3" fill="none"/>`);
  out.push(`<path d="M${f(x+2)} ${f(top)} q-26 -4 -40 12 M${f(x+2)} ${f(top)} q26 -6 40 10 M${f(x+2)} ${f(top)} q-14 -18 -34 -16 M${f(x+2)} ${f(top)} q16 -18 34 -14" stroke="#16201f" stroke-width="4" fill="none" stroke-linecap="round"/>`);
});

// Skylight spine
const sk = 150;
out.push(`<polygon points="${P([[VX-sk*s(T0),ceilY(T0)],[VX+sk*s(T0),ceilY(T0)],[VX+sk*s(T1),ceilY(T1)],[VX-sk*s(T1),ceilY(T1)]])}" fill="url(#hSky)"/>`);
for (let t = 0; t <= 1.0001; t += 0.125) out.push(`<line x1="${f(VX-sk*s(t))}" y1="${f(ceilY(t))}" x2="${f(VX+sk*s(t))}" y2="${f(ceilY(t))}" stroke="#0c0c0b" stroke-width="${f(Math.max(1,6*s(t)))}"/>`);
// linear LEDs along the ceiling edges
[-560,560].forEach(o=>out.push(`<line x1="${f(VX+o*s(T0))}" y1="${f(ceilY(T0)+30*s(T0))}" x2="${f(VX+o*s(T1))}" y2="${f(ceilY(T1)+30*s(T1))}" stroke="#f6e8cf" stroke-width="3" opacity=".75"/>`));

// Bays: 4 per side, glass sectional doors + mezzanine glazing above
const bays = [0,.25,.5,.75,1];
for (let i = 0; i < 4; i++) {
  const a = bays[i] + 0.035, b = bays[i+1] - 0.035;
  for (const side of ['L','R']) {
    const X = side === 'L' ? wallL : wallR;
    const door = [[X(a),yAt(a,.52)],[X(b),yAt(b,.52)],[X(b),floorY(b)],[X(a),floorY(a)]];
    out.push(`<polygon points="${P(door)}" fill="url(#hGlass)"/>`);
    for (let k = 1; k < 5; k++) { const h = .52*k/5; out.push(`<line x1="${f(X(a))}" y1="${f(yAt(a,h))}" x2="${f(X(b))}" y2="${f(yAt(b,h))}" stroke="#2a1f12" stroke-width="${f(3*s(a))}" opacity=".7"/>`); }
    out.push(`<polygon points="${P(door)}" fill="none" stroke="#0c0c0b" stroke-width="${f(10*s(a))}"/>`);
    // car hint inside: a dark low band at the bottom of the glass
    const ca = a + (b-a)*.12, cb = b - (b-a)*.12;
    out.push(`<polygon points="${P([[X(ca),yAt(ca,.2)],[X(cb),yAt(cb,.2)],[X(cb),yAt(cb,.03)],[X(ca),yAt(ca,.03)]])}" fill="#1a130b" opacity=".32"/>`);
    // mezzanine window
    out.push(`<polygon points="${P([[X(a),yAt(a,.88)],[X(b),yAt(b,.88)],[X(b),yAt(b,.62)],[X(a),yAt(a,.62)]])}" fill="url(#hMezz)" stroke="#0c0c0b" stroke-width="${f(8*s(a))}"/>`);
    // floor reflection
    const ra = [[X(a),floorY(a)],[X(b),floorY(b)],[X(b)+(VX-X(b))*.18,floorY(b)+ (floorY(b)-VY)*.18],[X(a)+(VX-X(a))*.18,floorY(a)+(floorY(a)-VY)*.18]];
    out.push(`<polygon points="${P(ra)}" fill="url(#hRefl)" filter="url(#hBlur)"/>`);
    // bay number plate
    const nt = a + 0.012, ns = s(nt);
    out.push(`<text x="${f(X(nt) + (side==='L'? 6: -6)*ns)}" y="${f(yAt(nt,.565))}" font-family="Archivo, Inter, sans-serif" font-size="${f(34*ns)}" fill="#efebe4" opacity=".8" text-anchor="${side==='L'?'start':'end'}" letter-spacing="${f(4*ns)}">${String(side==='L'? i+1 : i+5).padStart(2,'0')}</text>`);
  }
}
// Turntable + car at the far end
const tt = 0.86, ts = s(tt), ty = floorY(tt);
out.push(`<ellipse cx="${VX}" cy="${f(ty)}" rx="${f(190*ts*2.3)}" ry="${f(40*ts*2.3)}" fill="url(#hSpot)"/>`);
out.push(`<ellipse cx="${VX}" cy="${f(ty)}" rx="${f(170*ts*2.3)}" ry="${f(26*ts*2.3)}" fill="#151412" stroke="#d3a462" stroke-opacity=".7" stroke-width="1.5"/>`);
out.push(`<ellipse cx="${VX}" cy="${f(ty)}" rx="${f(150*ts*2.3)}" ry="${f(22*ts*2.3)}" fill="none" stroke="#d3a462" stroke-opacity=".25"/>`);
{ const w = 300*ts*2.3, h = 120*ts*2.3, x = VX - w/2, y = ty - h*0.92;
  out.push(`<g transform="translate(${f(x)} ${f(y)}) scale(${f(w/300)})">
    <path d="M18 92 C14 70 24 58 52 52 L84 30 C100 18 200 18 216 30 L248 52 C276 58 286 70 282 92 L282 112 L18 112 Z" fill="#0b0b0a"/>
    <path d="M92 34 C104 26 196 26 208 34 L232 54 L68 54 Z" fill="#2c3740" opacity=".9"/>
    <path d="M30 74 L92 80" stroke="#f6f1e6" stroke-width="5" stroke-linecap="round"/>
    <path d="M270 74 L208 80" stroke="#f6f1e6" stroke-width="5" stroke-linecap="round"/>
    <rect x="118" y="84" width="64" height="14" rx="3" fill="#151515" stroke="#2b2b2b"/>
    <path d="M18 92 C14 70 24 58 52 52 L84 30 C100 18 200 18 216 30 L248 52 C276 58 286 70 282 92" fill="none" stroke="#efebe4" stroke-opacity=".35" stroke-width="1.5"/>
  </g>`); }
// Entry floor line + drive-lane joints
for (let t = 0.125; t < 1; t += 0.125) out.push(`<line x1="${f(wallL(t))}" y1="${f(floorY(t))}" x2="${f(wallR(t))}" y2="${f(floorY(t))}" stroke="#efebe4" stroke-opacity=".04"/>`);
out.push(`<line x1="${f(VX)}" y1="${f(floorY(T0))}" x2="${f(VX)}" y2="${f(floorY(.8))}" stroke="#efebe4" stroke-opacity=".05" stroke-width="2"/>`);
out.push(`</svg>`);
process.stdout.write(out.join('\n'));
