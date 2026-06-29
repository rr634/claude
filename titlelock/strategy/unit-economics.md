# DeedGuard USA — unit economics (assumptions & scenarios)

Companion to `tools/economics.html`. ALTA 49 / 49.1 is **available in Florida**; the remaining
unknowns are Old Republic's real **endorsement charge** and your **FL title-agency split** — drop
those in and the margins are real. All numbers below are **illustrative placeholders**.

## Revenue streams (Phase 1 — piggyback on ORT)

1. **Membership fee** — recurring annual (e.g. $249 / $399 / $499). The core engine; SaaS-like margin.
2. **Endorsement commission** — your title-agency split of the ALTA 49/49.1 premium (one-time at issuance).
   The premium itself is **passed through at cost** to the homeowner; your income is the commission, not a markup.
3. **New-policy title commission** — for clients without an eligible owner's policy, writing a new ORT
   owner's policy is a one-time title-premium event (your agency retains its FL split).

## Costs (Phase 1)

- **Service / member / yr** — monitoring data, recorded-notice upkeep, support concierge.
- **Onboarding (yr 1)** — county recording fee for the protection notice + prep.
- **Covered-claim legal defense** — borne by **Old Republic** on covered claims, so *not* a DeedGuard
  cost in Phase 1. (This is also why the in-house-litigation margin needs Phase 2.)

## Why the margin works

- Membership is **recurring**; the title commissions are **one-time** (year 1 boost).
- Title fraud is **low-frequency / high-severity**, so the insurance leg carries a low expected loss —
  which is the whole basis for Phase 2.

## Phase 2 — own paper (upside)

Replace pass-through with your own program (fronting carrier + captive): you keep
`premium − expected losses − reinsurance/admin` as **underwriting profit**, on top of the recurring
service margin. Toggle this in the calculator. This is also where the in-house litigation/defense
dollars become capturable — subject to the conflict/firewall structure (see project README).

## Illustrative default scenario (calculator defaults)

| Input | Default |
|---|---|
| Members | 500 |
| Membership price | $399/yr |
| Service cost / member | $40/yr |
| Onboarding (yr 1) | $50 |
| Endorsement premium (pass-through) | $100 |
| Your commission on endorsement | 70% |
| New-policy attach rate | 40% |
| Avg new-policy premium / your retention | $1,500 / 70% |

> Numbers move entirely with your inputs — the point of the tool is to make the real ones obvious
> once ORT gives you the endorsement cost and your split.
