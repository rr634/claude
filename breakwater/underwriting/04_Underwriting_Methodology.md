# Breakwater Capital Partners
## Underwriting Methodology

*Companion to `models/Breakwater_Underwriting_Model.xlsx`. This explains the logic, the assumptions, and the discipline behind the numbers — so a capital partner understands not just the output, but the rigor.*

---

## 1. Underwriting philosophy

1. **Engineer returns from basis and execution, not appreciation.** The base case assumes the market does *not* move in our favor. Appreciation is upside, never the thesis.
2. **Underwrite the all-in basis, not the purchase price.** The number that matters is acquisition + completion + carry + closing + disposition — everything required to turn the asset into cash.
3. **Lead with cost-to-complete honesty.** Distressed completion budgets are where deals die. We build conservative budgets, verify them independently, and carry contingency.
4. **Solve for the spread, then for the entry price.** We start from finished value, subtract every honest cost and a required margin, and *back into* the maximum price we can pay. We do not start from the asking price.
5. **Sensitize before committing.** Every deal is stress-tested on the two variables that matter most: finished value (exit) and cost to complete.

---

## 2. The core equation

```
Finished (Exit) Value
  – Selling / Disposition Costs
  – Cost to Complete (hard + soft + contingency)
  – Carry Costs (debt service + taxes + insurance + admin, over hold)
  – Acquisition & Closing Costs
  ─────────────────────────────────────────────
  = Maximum Supportable Basis  (the most we can pay and still hit target margin)

Completion Spread $  =  Finished Value – All-In Basis
Completion Spread %  =  Completion Spread $ / All-In Basis
```

We require a **minimum 20% completion spread at base case** (target 25%+) to advance, and we re-test that the spread survives the downside sensitivity.

---

## 3. Inputs (model tab: `Inputs`)

| Input | Definition | Sourcing discipline |
|---|---|---|
| **Finished value** | Projected gross sale price, as-completed. | Min. 3 finished comps in-submarket; haircut for time-to-sale. In-house brokerage validates. |
| **Acquisition cost** | Price to gain control (note face/discount, equity, or fee price). | Driven by the screen + this model's max-basis solve, not the ask. |
| **Cost to complete** | Hard costs + soft costs to reach CO. | Independent estimate; scope-verified; never the seller's number alone. |
| **Contingency %** | Buffer on completion. | 10% baseline; 15% for complex/finish-heavy or stale budgets. |
| **Hold period (months)** | Acquisition close → sale close. | Construction duration + listing/closing lag; honest, not optimistic. |
| **Disposition cost %** | Commission + closing + concessions. | Modeled even where brokerage is in-house (opportunity cost / co-broke). |
| **Carry costs** | Property taxes, insurance, utilities, security, admin. | Monthly run-rate × hold. |
| **Debt terms** | Loan amount, rate, fees on acquisition/completion financing. | Per actual or indicative term sheet. |
| **Capital structure** | Equity vs. debt; pref rate; promote/waterfall. | Per deal; feeds the partner-return tab. |

---

## 4. Outputs (model tabs: `Underwriting`, `Returns`, `Sensitivity`)

- **All-in basis** — total capital required to reach a sale.
- **Completion spread ($ and %)** — the headline margin; the go/no-go number.
- **Project profit** — finished value − all-in basis − financing cost.
- **Project gross IRR & equity multiple** — annualized and absolute return on equity, given hold.
- **Partner-level returns** — split of profit through the waterfall (preferred return to capital, then promote to GP).
- **Sensitivity grid** — IRR / profit across a matrix of finished value (−10% to +10%) and cost-to-complete (−10% to +20%). This is the slide capital partners actually study.

---

## 5. The capital waterfall (model tab: `Returns`)

Standard deal-by-deal structure (adjustable per investment):

```
1. Return OF capital            → 100% to capital partners until invested capital returned
2. Preferred return             → 100% to capital partners until pref hurdle met (e.g., 8–10%)
3. GP catch-up (optional)       → to GP until promote ratio achieved
4. Residual split (promote)     → e.g., 80% capital / 20% GP   (or 70/30 above a second hurdle)
```

**Alignment:** GP co-invests on every deal and earns the promote only after partner capital has received its return *of* capital and *preferred return*. Downside is shared; upside is shared.

---

## 6. Decision thresholds (must all hold to proceed)

| Metric | Minimum to proceed | Target |
|---|---|---|
| Completion spread % (base case) | ≥ 20% | ≥ 25% |
| Completion spread % (downside sensitivity) | > 0% (no loss of capital) | ≥ 10% |
| Project gross IRR (base case) | ≥ 20% | 25–40%+ |
| Equity multiple (gross) | ≥ 1.35x | 1.4x–1.8x |
| Contingency carried | ≥ 10% | 10–15% |
| DSCR / leverage | conservative; refi optionality preserved | — |

If the base case clears but the **downside** case loses capital, the deal is repriced (lower basis), restructured (move up the stack to a secured/pref position), or passed.

---

## 7. From model to memorandum

A deal that clears the screen and underwrites above threshold becomes an **Acquisition Memorandum** containing: situation overview, capital stack & distress trigger, control strategy, completion plan & budget, exit plan & comps, the underwriting output and sensitivity grid, risk register with mitigants, and the proposed partner structure and returns. That memo is the document a capital partner says "yes" to.

---

*Illustrative methodology and targets only; not investment advice and not a guarantee of results. Any investment is made solely pursuant to definitive offering documents.*
