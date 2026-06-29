# DeedGuard USA — home title-fraud protection site

A self-contained, responsive marketing site for **DeedGuard USA** (deedguardusa.com), an
insurance-backed, attorney-led deed & title monitoring service (home title theft / equity-fraud
protection).

## What's here

| File | Purpose |
|---|---|
| `site/index.html` | The full landing page — hero, the threat, how it works, protection features, free property-check form, pricing, testimonials, FAQ, CTA, footer. |
| `site/assets/site.css` | The DeedGuard design system (deep slate + signal emerald). No frameworks, no build step. |
| `site/assets/favicon.svg` | Shield-and-lock mark. |
| `site/robots.txt` | Crawler allow. |

## Business model reflected in the site

The site presents a **four-layer stack** — **Prevent → Detect → Insure → Restore** — sold as an
annual **membership** ($249 / $399 / $499), where every layer is a real product:

- **Prevent** — a recorded protection notice placed in the county chain of title (deterrent; adds
  scrutiny, does not by itself block a filing).
- **Detect** — 24/7 monitoring of public land records + instant alerts.
- **Insure** — the **ALTA 49 / 49.1** post-closing forgery endorsement, **issued through Old Republic
  Title** (the operator is an Old Republic agent). Coverage ties to the owner's policy amount (home
  value). Eligibility: 1–4 family residential owned by a **natural person or estate-planning entity**
  — **LLC-held property is excluded** (a Phase-2 own-paper opportunity).
- **Restore** — attorney-led quiet-title / fraud restoration, with the policy covering the cost.

**Pricing structure (deliberate, for compliance):** the insurance **premium is passed through at
cost**; the **membership fee is a separate charge** for the recorded notice, monitoring, and
restoration services (premium-vs-fee split, not a marked-up premium).

- **Phase 1 — piggyback.** Add ALTA 49.1 to clients' existing owner's policies (or write a new
  policy + ALTA 49) and wrap it in the membership service layer.
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

## Deploying — domain: `deedguardusa.com`

The site is **deploy-ready**: `site/CNAME`, `site/sitemap.xml`, `site/robots.txt`, canonical/OG URLs,
and `netlify.toml` all point at **deedguardusa.com**. Pick a host and connect this repo — no build step.

**Recommended (doesn't touch the Breakwater site):** any static host pointed at **`titlelock/site`**.
- **Netlify:** New site from Git → this repo → set **Base directory = `titlelock`** (reads `netlify.toml`,
  publishes `site`). Add `deedguardusa.com` as a custom domain.
- **Cloudflare Pages / Vercel:** framework preset **None/Other**, **output dir = `titlelock/site`**.

**DNS at your registrar** for `deedguardusa.com`: follow the host's instructions — typically an
apex `A`/`ALIAS` (or `CNAME` for `www`) pointing at the host. The `CNAME` file in `site/` also makes
this repo's folder GitHub-Pages-ready if you ever move to a dedicated repo.

> GitHub Pages serves **one** site per repository and this repo already publishes `breakwater/site/`,
> so use a separate host (above) rather than this repo's Pages — or move DeedGuard to its own repo.

---

*Demonstration site. DeedGuard is presented as monitoring **plus** an insurance policy underwritten by
a licensed carrier; all carriers, coverage limits, and figures shown are illustrative placeholders and
subject to the actual policy issued and state availability. Nothing here creates an attorney-client
relationship. Replace the placeholder coverage amounts with real, carrier-approved terms before launch.*
