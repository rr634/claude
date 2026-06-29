# TitleLock — home title-fraud protection site

A self-contained, responsive marketing site for **TitleLock**, an attorney-backed
deed & title monitoring service (home title theft / equity-fraud protection).

## What's here

| File | Purpose |
|---|---|
| `site/index.html` | The full landing page — hero, the threat, how it works, protection features, free property-check form, pricing, testimonials, FAQ, CTA, footer. |
| `site/assets/site.css` | The TitleLock design system (deep slate + signal emerald). No frameworks, no build step. |
| `site/assets/favicon.svg` | Shield-and-lock mark. |
| `site/robots.txt` | Crawler allow. |

## Design

- **Brand:** deep slate-blue (`#0E2A47`) for trust, signal emerald (`#10B981`) for "protected,"
  alert red (`#E0533D`) for the threat framing.
- **Fully self-contained:** all visuals are CSS gradients + inline SVG, so it works on any static
  host with zero external requests.
- Responsive (mobile nav, fluid type), accessible (semantic landmarks, `aria-live` form status,
  reduced-motion support), and animated with on-scroll reveals.

## Run it locally

```bash
cd titlelock/site
python3 -m http.server 8000
# open http://localhost:8000
```

Or just open `site/index.html` in a browser.

## The free-check form

The "Run Free Check" form is wired up client-side only — it validates input and shows a confirmation.
To go live, point the form `submit` handler at your backend, CRM, or an email/Forms endpoint
(e.g. Formspree, a Lambda, or your intake system). Search for `checkForm` in `index.html`.

## Deploying

The repo's existing GitHub Pages workflow (`.github/workflows/pages.yml`) publishes
`breakwater/site/`. GitHub Pages serves **one** site per repository, so to publish TitleLock
instead, point that workflow's `path:` at `titlelock/site` (and update its trigger `paths:`).
Alternatively, drop `titlelock/site/` onto Netlify, Vercel, Cloudflare Pages, or any static host.

---

*Demonstration site. TitleLock is a records-monitoring concept, not title insurance. Figures shown
are illustrative. Nothing here creates an attorney-client relationship.*
