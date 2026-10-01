# 8 AT RIO — website

Single-page marketing site for **8 AT RIO**, a project of eight private garage residences on SE 12th Street
in Rio Vista, Fort Lauderdale (Richard N. Rosa, P.A.). The look follows the dark, editorial, members-club
style of revaultsociety.com.

The site now presents the **covered-hall refinement**: eight identical bays off one enclosed, drive-in hall.
See `CONCEPT-hall.md` for the reasoning, the numbers and open code and zoning questions.

- `site/index.html` — the whole site (HTML + CSS + JS inline, no build step)
- `site/assets/` — images cropped and compressed from the concept package and drone photography
- `tools/hall-svg.js` — generates the hero's perspective drawing of the Hall (`node tools/hall-svg.js`);
  paste the output into the `.hero-art` block of `index.html` when you change it

Open `site/index.html` in a browser to preview.

## Source of the content

| Site section | Source |
|---|---|
| Hero | Drawn in code from `tools/hall-svg.js` (illustrative, until real hall renderings exist) |
| Typical section | DRC sheet "Typical Section" → `typical-section.jpg` |
| Plan | Inline SVG diagram of the covered-hall layout (built from the DRC site plan geometry) |
| Rio Vista aerial | Drone photo looking north → `aerial-skyline.jpg` |
| The site today | Overhead drone photo → `site-today.jpg` |

The original open-courtyard entry rendering and site plan were removed from the site because they no
longer match the concept. They remain in the git history.

## Still to confirm before launch

- Everything listed under "Questions" in `CONCEPT-hall.md`
- Garage spec items (lift, 240V, compressed air, etc.), which are labeled as planned
- Drive and track times in the Rio Vista section (approximate)
- Unit status (all shown as "Pre-release")
- Ownership language in the FAQ (planned as condominium units)
- Florida §718.503 disclaimer in the footer (have counsel confirm the final text)

## Swapping in new images

To add a photo, drop the image into `site/assets/` and reference it from `index.html`. The Hall tiles
(`.t-wide`, `.t-tall`, `.t-third` in the CSS) are styled placeholders made ready for renderings of the
hall, turntable, gate, detail bay and pool terrace: set `background: url("assets/<file>.jpg") center/cover`
on the tile's `::before`. When a real rendering of the Hall exists, it can replace the drawn hero.
