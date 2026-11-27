# DeedGuard USA — unit economics (assumptions & scenarios)

Companion to `tools/economics.html`. The **core business is a recurring AI-monitoring subscription** —
that's the engine. The insurance add-on and a future own-product are modeled as upside. All numbers
below are **illustrative placeholders**.

## Revenue streams

1. **Subscription (core)** — Essential $7.99/mo, Guardian $9.99/mo founding (renews $17.95/mo), Premier
   $24.99/mo — penetration-priced to undercut Home Title Lock (~$19.95/mo). AI monitoring + alerts + attorney
   access. SaaS-like gross margin; the whole thesis rests on this.
2. **Insurance add-on commission (optional)** — *only where the ALTA 49/49.1 endorsement is actually
   sold*, through a licensed title agent/underwriter. The premium is passed through; your income is
   the commission, billed separately. Treat as upside, not base case.
3. **New-policy title commission (optional)** — if a client needs a new owner's policy to attach the
   endorsement, that's a one-time title-premium event where you act as agent.

## Costs

- **Service / member / yr** — county-record data/ingestion, AI compute, alerting, support.
- **Onboarding (yr 1)** — baseline setup per property.
- **Attorney response** — a cost reserve for the hands-on help; low-frequency.

## Why the margin works

- Subscription revenue is **recurring**; any insurance commission is **one-time** upside.
- Monitoring is cheap per property at scale (data + compute); the differentiator (AI explanation +
  attorney) is what justifies pricing above a bare "title lock."

## Phase 2 — our own coverage (upside)

Instead of relying on third-party endorsements, stand up a **bespoke product via a specialty market
(e.g. Lloyd's of London / surplus lines)**. Toggle "Phase 2" in the calculator to model
`premium − expected losses − reinsurance/admin` as underwriting profit on top of the subscription
margin. Title fraud is low-frequency / high-severity, so expected loss is low — the basis for the play.

## Illustrative default scenario (calculator defaults)

| Input | Default |
|---|---|
| Members | 500 |
| Subscription price | $399/yr (calculator default; site tiers $199/$349/$599) |
| Service cost / member | $40/yr |
| Onboarding (yr 1) | $50 |
| Insurance add-on premium (pass-through) | $100 |
| Commission on add-on | 70% |
| Add-on attach rate (where available) | 40% |

> Numbers move entirely with your inputs — the point of the tool is to make the real ones obvious
> once you have your true per-property monitoring cost and (optionally) the add-on economics.
