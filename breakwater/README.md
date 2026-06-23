# Breakwater Capital Partners
### Special Situations Development Platform — South Florida Luxury Residential

This package is the foundational spine of the platform: the **institutional narrative** (why this exists, why us) and the **underwriting discipline** (proof we won't lose a partner's money). Both are built with a capital-formation lens, because **capital is the current binding constraint** — these are the documents a capital partner says "yes" to.

> **Positioning:** A *special situations development platform*, not a "distress fund." Distress is how we source; completion is what we sell.

---

## What's here

| File | Purpose | Audience |
|---|---|---|
| **strategy/01_Platform_Thesis.md** | Full institutional thesis — opportunity, strategy, the completion-spread engine, the vertical-integration moat, target returns, risk, capital structure, roadmap to a fund. | Capital partners, internal north star |
| **strategy/02_Capital_Partner_Teaser.md** | One/two-page door-opener distilling the thesis. | First contact with capital |
| **underwriting/03_Acquisition_Screening_Box.md** | The go/no-go deal screen — hard filters + scored criteria + decision rule + intake sheet. | Internal sourcing/screening |
| **underwriting/04_Underwriting_Methodology.md** | The logic, assumptions, thresholds, and waterfall behind the model. | Internal + capital-partner diligence |
| **underwriting/07_Due_Diligence_Checklist.md** | Memo Appendix G — gated confirmatory checklist across 8 workstreams (incl. construction & design partners), with owners, gating items, and sign-off. | Internal deal execution |
| **models/Breakwater_Underwriting_Model.xlsx** | Working single-asset model: live formulas, partner waterfall, sensitivity grid. Loaded with an illustrative Rio Vista worked example. | Per-deal underwriting |
| **models/build_underwriting_model.py** | Reproducible builder for the model (re-run to regenerate). | Internal |
| **acquisitions/05_Acquisition_Memorandum_Template.md** | The per-deal "yes" document — reusable template with placeholders + drafting rules. | IC, then capital partner |
| **acquisitions/06_Acquisition_Memorandum_SAMPLE_RioVista.md** | Fully worked sample memo on the Rio Vista deal; ties number-for-number to the model. | Reference / training |
| **site/index.html** | Public landing page — self-contained, responsive, navy/gold brand. Thesis, value chain, totally-vertical edge, markets, box; return targets gated. | Public / marketing |
| **site/investors.html** | Gated investor page — accredited/institutional acknowledgment wall, then target economics, participation structures, waterfall, worked example, roadmap, full securities disclaimers. | Verified investors |
| **sourcing/distress_radar/** | Public-records distress-detection engine — flags recorded liens > $100K, lis pendens, judgments; scores them and emits a ranked hot list + pre-filled intake sheets. Runnable now on mock data; per-county adapter framework. | Internal sourcing (top of funnel) |

---

## The flow these create

```
DISTRESS RADAR ──▶ SCREEN (03) ──▶ MODEL (xlsx) ──▶ MEMO (05/06) ──▶ DD (07) ──▶ CLOSE
 detect signal      decide whether   decide price &    the "yes"       verify CPs
 (liens >$100K)     to underwrite     structure        document
                                                                  └─▶ CAPITAL (01/02 + site) funds it
```

1. The **Distress Radar** scans county Official Records and flags developer distress → ranked HOT leads with pre-filled intake.
2. Each flagged lead runs through the **Screening Box (03)** → pursue / pass in <30 min.
3. Survivors are priced and structured in the **Underwriting Model** → spread, equity, IRR, waterfall, sensitivity.
4. A passing deal becomes an **Acquisition Memorandum (05/06)** → the IC and capital-partner "yes."
5. **Due Diligence (07)** verifies the memo's conditions precedent across 8 workstreams → gate to close.
6. The **Thesis (01)** and **Teaser (02)** open and hold the capital relationship; the **site** is the public + gated-investor face.

## Worked example economics (illustrative, in the model)

| Metric | Value |
|---|---|
| Finished value | $7.5M |
| All-in basis | ~$5.9M |
| Completion spread | **27%** |
| Equity required | ~$1.65M |
| Project equity multiple | **1.41x** |
| Project gross IRR (~12 mo) | **~41%** |
| Downside corner (−10% value / +20% cost) | still profitable — capital preserved |

## Suggested next builds

- **Live county adapters** for the Distress Radar (Broward first) + Property Appraiser value joins
- **Acquisition funnel / CRM** — where flagged leads move through stages (radar → screen → memo → close)
- **Lender / receiver / estate-attorney outreach engine** — the action taken on a flagged signal
- **Construction completion playbook** and **lender workout playbook**
- **Construction & design partner agreement framework** (scope, pricing, conflict disclosure)

---

*All materials are informational and illustrative only. Nothing here is an offer to sell or a solicitation to buy any security, or investment/legal/tax advice. Targets are objectives, not guarantees. Any investment is made solely pursuant to definitive offering documents.*
