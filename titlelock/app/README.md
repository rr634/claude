# DeedGuard USA — backend (recurring-revenue stack)

Serverless backend that turns the marketing site into a working business:
**free-check lead capture → Stripe subscription → stored customer → scheduled title scan → alert email.**

```
Visitor ──> site (static)
   │  free check  ──────────────> /functions/lead ──> Supabase(leads) + email operator
   │  pick a plan ──────────────> /functions/create-checkout ──> Stripe Checkout
   │                                                                   │ pays
   │                               Stripe ──webhook──> /functions/stripe-webhook ──> Supabase(subscribers)
   │
   └─ daily cron ─> /functions/scan ─> county adapter ─> diff vs baseline ─> Supabase(alerts) + email subscriber
```

## Stack (low-ops, fast to revenue)
- **Host + functions:** Netlify (static `site/` + Netlify Functions in `app/netlify/functions`).
- **Payments / recurring:** Stripe Checkout + Billing (subscriptions).
- **Database:** Supabase (Postgres). Schema in `app/db/schema.sql`.
- **Email:** Resend. **SMS (later):** add Twilio in `app/lib/`.
- **Monitoring:** scheduled function + pluggable county adapters (`app/lib/counties/`).

Everything is swappable — the functions are plain Node and the county adapters are a one-method interface.

## One-time setup
1. **Supabase:** create a project → run `app/db/schema.sql` in the SQL editor. Copy the URL + **service-role** key.
2. **Stripe:** create 3 Products with recurring Prices (Essential/Defend/Premier) → copy the `price_…` IDs.
   Add a webhook to `https://deedguardusa.com/.netlify/functions/stripe-webhook` (events:
   `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`) → copy the signing secret.
3. **Resend:** verify the sending domain → copy the API key.
4. **Netlify:** connect the repo (base `titlelock`), then add all env vars from `app/.env.example`
   under Site settings → Environment. Deploy.

The scheduled scanner runs automatically once deployed (daily; adjust the cron in `scan.js`).

## Local test (no external services needed)
```bash
cd titlelock && npm install
npm test            # exercises the change-detection engine against the mock county adapter
```

## What's real vs. stubbed
- **Real & runnable:** lead capture, Stripe checkout + webhook sync, the scan→diff→alert pipeline, schema.
- **Stubbed:** the county data source is the deterministic **mock** adapter. Shipping to paying customers
  means building real county adapters (`app/lib/counties/README.md` has the FL build order) **or** wrapping a
  property-data vendor behind the same `fetchRecordings` interface.
- **Next wiring:** capture each subscriber's property **address/parcel/county** at signup (Stripe Checkout
  custom field or a short post-purchase onboarding form) and insert a `properties` row so the scanner picks it up.

## Pricing (Stripe Prices → match the site)
Essential $199/yr · Defend $349/yr · Premier $599/yr (monthly options optional). Figures are illustrative
until unit costs are set — see `../strategy/unit-economics.md` and `../tools/economics.html`.
