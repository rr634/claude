# 8 AT RIO — website

Single-page marketing site for **8 AT RIO**, a project of eight private garage residences on SE 12th Street
in Rio Vista, Fort Lauderdale (Richard N. Rosa, P.A.). The look follows the dark, editorial, members-club
style of revaultsociety.com. Content comes from the DRC schematics and renderings.

- `site/index.html` — the whole site (HTML + CSS + JS inline, no build step)
- `site/assets/` — images cropped and compressed from the concept package and drone photography

Open `site/index.html` in a browser to preview.

## Source of the content

| Site section | Source |
|---|---|
| Hero + "Entry Court" | Entry rendering (top band of the DRC sheet) → `entry-rendering.jpg` |
| Typical section | DRC sheet "Typical Section" → `typical-section.jpg` |
| Site plan + project data + setbacks | Site plan sheet → `site-plan.jpg` |
| Rio Vista aerial | Drone photo looking north → `aerial-skyline.jpg` |
| The site today | Overhead drone photo → `site-today.jpg` |

## Still to confirm before launch

- Drive times in the Rio Vista section (approximate)
- Unit status (all shown as "Pre-release")
- Ownership language in the FAQ (planned as condominium units)
- Florida §718.503 disclaimer in the footer (have counsel confirm the final text)

## Swapping in new images

To add a photo, drop the image into `site/assets/` and reference it from `index.html`. The Grounds tiles
02–05 (`.t-a` … `.t-d` in the CSS) are styled placeholders made ready for pool, promenade, cabana and
night-lighting renderings: set `background: url("assets/<file>.jpg") center/cover` on the tile's `::before`.
