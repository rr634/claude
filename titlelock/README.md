# DeedGuard — home title-fraud protection site

A self-contained, responsive marketing site for **DeedGuard**, an attorney-backed
deed & title monitoring service (home title theft / equity-fraud protection).

## What's here

| File | Purpose |
|---|---|
| `site/index.html` | The full landing page — hero, the threat, how it works, protection features, free property-check form, pricing, testimonials, FAQ, CTA, footer. |
| `site/assets/site.css` | The DeedGuard design system (deep slate + signal emerald). No frameworks, no build step. |
| `site/assets/favicon.svg` | Shield-and-lock mark. |
| `site/robots.txt` | Crawler allow. |

## Business model reflected in the site

The site is built around a **membership + embedded-insurance** model (placeholders, illustrative):

- **Phase 1 — piggyback.** An annual **membership** ($249 / $399 / $499) that *includes* a
  title-fraud **insurance endorsement** ($25K / $100K / $250K). The site deliberately splits the
  two: the insurance **premium is passed through at cost**, and the membership fee is a **separate
  charge** for monitoring + attorney-backed restoration (the cleaner premium-vs-fee structure).
- **Phase 2 — own paper.** Higher limits / DeedGuard's own program (fronting carrier + captive)
  to capture underwriting profit, not just the service spread.
- **Phase 3 — vertical.** In-house attorneys litigate the *fraud* (client-aligned quiet-title work);
  coverage-determination is firewalled to an independent administrator to avoid the conflict.

> ⚠️ **Before launch:** selling insurance needs a licensed carrier/producer; coverage limits,
> carriers, and state availability must be real; and the Phase-3 conflict/ownership structure
> (Rule 4-1.7 / 4-5.4; ABS domicile) must be cleared by a professional-responsibility specialist.
> Every dollar figure on the site is marked illustrative for this reason.

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
`breakwater/site/`. GitHub Pages serves **one** site per repository, so to publish DeedGuard
instead, point that workflow's `path:` at `titlelock/site` (and update its trigger `paths:`).
Alternatively, drop `titlelock/site/` onto Netlify, Vercel, Cloudflare Pages, or any static host.

---

*Demonstration site. DeedGuard is presented as monitoring **plus** an insurance policy underwritten by
a licensed carrier; all carriers, coverage limits, and figures shown are illustrative placeholders and
subject to the actual policy issued and state availability. Nothing here creates an attorney-client
relationship. Replace the placeholder coverage amounts with real, carrier-approved terms before launch.*
