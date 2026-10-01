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
| Hero | Entry rendering (top band of the DRC sheet) → `entry-rendering.jpg` |
| Motor Court · "The Gate" | Left crop of the entry rendering → `entry-gate.jpg` |
| Typical section | DRC sheet "Typical Section" → `typical-section.jpg` |
| Site plan diagram | Inline SVG redrawn from the DRC site plan, with the courtyard shown as an open motor court (no trees in the middle). `site-plan.jpg` is kept but not used |
| Project data + setbacks | DRC site plan sheet |
| Rio Vista aerial | Drone photo looking north → `aerial-skyline.jpg` |
| The site today | Overhead drone photo → `site-today.jpg` |

## Still to confirm before launch

- The hero rendering still shows palms down the middle of the courtyard; replace it when an updated motor-court rendering is available
- Drive times in the Rio Vista section (approximate)
- Unit status (all shown as "Planned"; the site says nothing is for sale yet)
- Ownership language in the FAQ (planned as condominium units)
- Footer disclosures (§718.503 statement, Chapter 718 no-offer language, square-footage note); have counsel confirm the final text
- Whether "Richard N. Rosa, P.A." is the developer entity to name, or whether a project entity should appear instead

## Swapping in new images

To add a photo, drop the image into `site/assets/` and reference it from `index.html`. The Motor Court
tiles 02–05 (`.t-court`, `.t-a`, `.t-c`, `.t-d` in the CSS) are styled placeholders made ready for renderings of the
court, pool, cabana and landscaped edges: set `background: url("assets/<file>.jpg") center/cover` on the tile's
`::before`.
