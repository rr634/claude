# DeedGuard USA — Demand Validation Playbook

**Goal:** prove people *want* this (and will pay) **before** building the monitoring tech.
You already have everything you need to run the test: a strong landing page, ad creatives, lead
capture, and Stripe checkout. This is how to use them to get a clear yes/no on demand.

---

## 1. The principle
Don't build delivery to find out if there's demand. Put the offer in front of real Florida
homeowners, spend a little money driving traffic, and **measure what they do.** Build the pipeline
only once the signal is green.

## 2. Demand signals, weakest → strongest
| Signal | What it proves | How we capture it |
|---|---|---|
| Time on page / scroll | Message resonates | Analytics (Plausible/GA) |
| **Free-check lead** (email) | Interested enough to raise a hand | `lead_submit` event + leads table/inbox |
| **Checkout click** | Willing to consider paying | `checkout_click` event |
| **Completed payment** | *Real* demand — the only signal that fully counts | Stripe |

The first paying customer is worth more than 1,000 visitors. Optimize the test toward payment signal.

## 3. Two ways to run it (pick based on readiness)

### A. Waitlist / lead test (softest, start here)
Drive ads → free property check → capture email. Measure **cost per lead** and **lead rate**.
Cheap, zero delivery obligation. Good first week to validate the *message*.

### B. Pre-sale / smoke test (strongest — do this next)
Let visitors actually hit **Stripe Checkout**. A real card entry is the truth. Two honest ways to
handle it before the tech is built:
- **Founding-member pre-sale:** charge now at a founder discount; tell them onboarding starts within
  X days. Deliver the first cohort **manually** (see §6). Refund anyone promptly if you can't deliver.
- **$0 authorization / reserve:** use Checkout in "setup" mode to capture the card without charging
  ("reserve your spot") — strong intent signal, no money held.
> Ethics/compliance: if you take money, deliver the service or refund fast. Never imply the AI
> pipeline is running if it isn't. "Founding member — early access" is honest; "live now" isn't.

## 4. The funnel + rough benchmarks (interpretation, not promises)
```
Ad impressions
   │  CTR ~1–2%  (creative/message)
Landing visits
   │  5–15% → lead      (free-check email)
Leads
   │  5–15% → checkout click
Checkout clicks
   │  20–40% → paid
Paying customers
```
Healthy early target: **cost per lead < ~$15–25**, and at least a handful of **checkout clicks /
pre-sales** from the first few hundred visits. These move a lot by geo, season, and offer — read
*trends and relative* performance, not absolutes.

## 5. Budget & timeline (lean)
- **Spend:** $300–600 total over ~2 weeks ($20–40/day). One or two FL geos (e.g. Broward + Palm Beach).
- **Channels:** Meta (Angles A/B from the ad playbook) + a little Google Search on high-intent terms
  ("home title lock", "home title theft florida").
- **Cadence:** check daily, kill losers after ~$50 no-signal spend, shift budget to winners.

## 6. Deliver the first customers *manually* (concierge MVP)
If people pay, you don't need the pipeline yet. For the first 5–20 properties, **you** (or a VA)
manually check the county Official Records weekly and email them a "you're protected / here's what we
saw" note. This proves the delivery is valuable and teaches you exactly what to automate — *then*
build the county adapters. Paying customers + manual delivery = validated business.

## 7. Decision tree (after ~2 weeks)
- 🟢 **Green** — steady leads at reasonable cost *and* real checkout clicks / pre-sales →
  **build the monitoring pipeline** (start Miami-Dade/Broward/Palm Beach adapters) and scale ads.
- 🟡 **Yellow** — leads but no payment intent → the *message* works, the *offer/price* doesn't.
  Iterate: price, founder discount, guarantee, plan names, hero promise. Re-test.
- 🔴 **Red** — little engagement, expensive leads, no checkout clicks across multiple angles →
  demand is weak as framed. Change audience (e.g. realtors/estate attorneys as referrers), or pivot.

## 8. Go-live checklist to start the test
- [ ] Register `deedguardusa.com`, connect Netlify, deploy (see `../DEPLOY.md`).
- [ ] Set analytics IDs in `site/index.html` (`__DG_ANALYTICS__` block) — Plausible and/or Meta Pixel.
- [ ] Wire `OPERATOR_EMAIL` so free-check leads hit your inbox (or just use the client-side fallback
      + Netlify Forms for the very first test — even lighter).
- [ ] (For pre-sale) create Stripe Prices + set env vars; add a "Founding member" line to pricing.
- [ ] Launch 2 Meta ad sets + 1 Google ad; point all at `deedguardusa.com`.
- [ ] Watch `lead_submit` and `checkout_click` events daily.

**Bottom line:** spend two weeks and a few hundred dollars to learn whether Florida homeowners raise
their hand and reach for a card. If they do, we build the delivery tech with confidence. If they
don't, we've saved months.
