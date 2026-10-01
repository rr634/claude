# The Paddock — Fort Lauderdale car condo site

Single-page marketing site for a private car-condo / collector-garage community in
Fort Lauderdale. Modeled on the dark, editorial, members-club style of Revault Society
(revaultsociety.com) and fully original.

- `site/index.html` — the whole site (HTML + CSS + JS inline, no build step)
- `site/assets/favicon.svg`

Open `site/index.html` in a browser to preview.

## Things to customize

| What | Where |
|---|---|
| Brand name "The Paddock" | search/replace in `site/index.html` |
| Colors / fonts | `:root` tokens at the top of the `<style>` block |
| Studio sizes and specs | `#studios` section (three tabs) |
| Unit inventory and status | `#availability` table (rows marked `s-open`, `s-hold`, `s-sold`) |
| Drive times and map | `#location` section |
| Inquiry email | `TO` constant in the inquiry script (sends via FormSubmit, falls back to mailto) |

Placeholder content (unit count, square footage, inventory, events, drive times) is
illustrative and should be replaced with real project data before launch. The footer
includes the Florida §718.503 developer disclaimer; have counsel confirm the final text.
