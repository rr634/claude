# DeedGuard USA — AI home title monitoring site

A self-contained, responsive marketing site for **DeedGuard USA** (deedguard.us), an
**AI-powered title-monitoring subscription** with a Florida real estate attorney on call, plus an
**optional** title-insurance add-on where available (home title theft / deed-fraud protection).
Tagline: **Always Watching. Always Protected.**

## What's here

| File | Purpose |
|---|---|
| `site/index.html` | The full landing page — hero, the threat, how it works, protection features, free property-check form, pricing, testimonials, FAQ, CTA, footer. |
| `site/assets/site.css` | The DeedGuard design system (deep slate + signal emerald). No frameworks, no build step. |
| `site/assets/favicon.svg` | Shield-and-lock mark. |
| `site/robots.txt` | Crawler allow. |

## Business model reflected in the site

The core is a **recurring AI-monitoring subscription** ($199 / $349 / $599 per year), differentiated
from basic "title locks" (Home Title Lock, etc.) by three things: an **AI** that re-scans the public
record every few days and explains each filing in plain English, a **real Florida attorney on call**,
and **honest, cancel-anytime pricing**. No carrier dependency, no regulatory gate — just software + a
lawyer + recurring revenue.

**Insurance is an *optional* add-on, not the product.** Where the **ALTA 49 / 49.1** forgery
endorsement is actually sold (through a licensed title agent/underwriter — *any* underwriter, not a
specific one), we can help a homeowner add it to their owner's policy, priced and billed separately.
The site never bundles it or claims it as DeedGuard's own insurance. (Earlier drafts framed it as an
"Old Republic" product; Old Republic doesn't sell a consumer product like this, so that framing was
removed.)

- **Phase 1 — the subscription.** Sell AI monitoring + attorney access as recurring revenue. Offer
  the insurance endorsement as a separate add-on only in states where it's genuinely available.
- **Phase 2 — our own coverage.** Evaluate a bespoke insurance product via a specialty market
  (e.g. **Lloyd's of London / surplus lines**) so coverage isn't dependent on third-party endorsements.
- **Phase 3 — vertical.** In-house attorneys handle restoration; if DeedGuard ever carries risk,
  firewall coverage-determination from the firm (Rule 4-1.7 / 4-5.4; ABS domicile) — clear with a
  professional-responsibility specialist.

> ⚠️ **Before launch:** the monitoring subscription is real and buildable today. Keep the insurance
> add-on marketed only where it's actually for sale. Dollar figures remain illustrative until real
> unit costs are dropped into `tools/economics.html`. Build the AI monitoring pipeline (county-record
> ingestion + change detection + alerting) to back the product claims.

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

## Deploying — domain: `deedguard.us`

The site is **deploy-ready**: `site/CNAME`, `site/sitemap.xml`, `site/robots.txt`, canonical/OG URLs,
and `netlify.toml` all point at **deedguard.us**. Pick a host and connect this repo — no build step.

**Recommended (doesn't touch the Breakwater site):** any static host pointed at **`titlelock/site`**.
- **Netlify:** New site from Git → this repo → set **Base directory = `titlelock`** (reads `netlify.toml`,
  publishes `site`). Add `deedguard.us` as a custom domain.
- **Cloudflare Pages / Vercel:** framework preset **None/Other**, **output dir = `titlelock/site`**.

**DNS at your registrar** for `deedguard.us`: follow the host's instructions — typically an
apex `A`/`ALIAS` (or `CNAME` for `www`) pointing at the host. The `CNAME` file in `site/` also makes
this repo's folder GitHub-Pages-ready if you ever move to a dedicated repo.

> GitHub Pages serves **one** site per repository and this repo already publishes `breakwater/site/`,
> so use a separate host (above) rather than this repo's Pages — or move DeedGuard to its own repo.

---

*Demonstration site. DeedGuard is presented as monitoring **plus** an insurance policy underwritten by
a licensed carrier; all carriers, coverage limits, and figures shown are illustrative placeholders and
subject to the actual policy issued and state availability. Nothing here creates an attorney-client
relationship. Replace the placeholder coverage amounts with real, carrier-approved terms before launch.*
