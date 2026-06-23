# Breakwater Distress Radar

**The top of the acquisition funnel.** A public-records distress-detection engine
that continuously surfaces the recorded signals of developer distress — **claims
of lien over $100,000**, lis pendens, judgments, and tax liens — across South
Florida counties, scores them against the Breakwater thesis, and emits a ranked
**hot list** that flows straight into the Acquisition Screening Box.

> **Why this comes first.** Outreach presumes you know who to call. The radar is
> what tells you — early, from the public record, before the asset is marketed.
> You become the first call *because you called first.*

```
DISTRESS RADAR ─▶ SCREEN (03) ─▶ MODEL ─▶ MEMO (05) ─▶ DD (07) ─▶ CLOSE
 detect signal     go / no-go                                ▲
       │                                                     │
       └────────── outreach engages a FLAGGED target ────────┘
```

---

## The distress signal — what we hunt and why

Florida construction and foreclosure distress leaves a public paper trail in each
county's **Official Records** (public under FL Sunshine law). The radar reads that
trail:

| Signal (FL recording) | What it means | Weight |
|---|---|---|
| **Lis Pendens** | A lawsuit — usually foreclosure — is pending. | Highest |
| **Claim of Lien** (Ch. 713) | A contractor/sub is unpaid — the classic stall. | High |
| **Notice of Default** | Borrower in default. | High |
| **Final Judgment / Judgment Lien** | Money judgment against owner/developer. | Medium |
| **Tax Lien** | Federal/state/county taxes unpaid. | Medium |
| **Notice of Commencement** (Ch. 713) | Construction *started* — not distress alone… | Context |
| **Release / Satisfaction** | The problem may be **cured** — de-prioritize. | Negative |

**The premium signal (our exact target):** a **Notice of Commencement** (active
project) *plus* a **Claim of Lien** on the same parcel = a live luxury build that
has stalled into nonpayment. That is the 50–90%-complete distressed spec home the
whole platform is built to acquire. The scorer pays a premium for that combination.

**The hard trigger (founder's rule):** any qualifying lien **≥ $100,000** flips a
parcel to `triggered`. A `HOT` lead requires *both* the trigger and a high
composite score.

### How scoring ranks a parcel
Documents are aggregated **per parcel**, then scored on: document-type severity,
lien-amount band, the stalled-construction premium, **lien stacking** (multiple
liens compound), a penalty if a release is recorded, and **fit boosts** for target
submarkets and in-box estimated value. Output label: `HOT` / `WATCH` / `IGNORE`.
All weights live in `config.py` — tune without touching code logic.

---

## What it produces

Every run writes to `exports/`:
- **`hot_list.csv`** — ranked parcels with label, score, trigger, lien size, value, doc types.
- **`signals.json`** — full structured detail incl. the scoring reasons and every document.
- **`intake_<parcel>.md`** — for each `HOT` lead, a **pre-filled Screening Box intake
  sheet** (artifact 03) with a verify-first action checklist — ready to hand to an analyst.

---

## Run it

Stdlib only — no install required. From `breakwater/sourcing/`:

```bash
# End-to-end demo on synthetic data (no network):
python3 -m distress_radar.run --mock --since 2025-01-01

# Specific counties / higher trigger:
python3 -m distress_radar.run --mock --counties broward,miami_dade --min-amount 250000

# Live mode (after implementing county adapters):
python3 -m distress_radar.run --counties broward --since 2026-06-01
```

The store de-duplicates by clerk instrument number, so the radar is **incremental
and safe to schedule** (e.g., a daily cron): each run only acts on genuinely new
filings, while signals accumulate on a parcel over time.

---

## Architecture

```
distress_radar/
  config.py        trigger, box, doc-type weights, target submarkets  ← tune here
  models.py        RecordedDocument + DistressSignal + label normalization
  scoring.py       aggregate-by-parcel → score → classify (HOT/WATCH/IGNORE)
  storage.py       SQLite dedup store (incremental runs)
  pipeline.py      fetch → store → score → export (csv/json/intake)
  http_client.py   PoliteClient — robots + rate-limit + retry (stdlib)
  run.py           CLI (--mock | --fixture | --live)
  adapters/
    base.py            BaseCountyAdapter + responsible-use contract
    mock_county.py     working synthetic adapter (demo + tests)
    broward.py         LIVE Broward adapter (Acclaim platform) — implemented
    florida_counties.py registry + remaining county stubs
  fixtures/        representative county responses (offline parser demo/tests)
  tests/           unit tests (parser, scoring, http client) — 16 tests
```

### Broward adapter (the operational core — implemented)

Broward's Official Records run on the Harris **Acclaim** platform, so this
adapter is also a template for other Acclaim counties. Three run modes:

```bash
# MOCK (default): synthetic data, exercises scoring/exports end-to-end
python3 -m distress_radar.run --mock --since 2025-01-01

# FIXTURE: runs the REAL Broward parser against a saved response (offline)
python3 -m distress_radar.run --counties broward \
    --fixture distress_radar/fixtures/broward_sample.json --since 2025-01-01

# LIVE: real HTTP (refuses until the wire config is verified — see below)
python3 -m distress_radar.run --counties broward --live --since 2026-06-01
```

**Going live — verification checklist (in `adapters/broward.py → BrowardWire`):**
The county-specific unknowns are isolated and marked `VERIFY`. Confirm against
the live portal, then set `wire.verified = True`:
- [ ] Endpoint path + query-parameter names (`p_date_from`, `p_doctype`, …)
- [ ] Doc-type query codes (`doctype_query_codes`) against the Acclaim doc-type list
- [ ] Response field names (`f_instrument`, `f_amount`, …)
- [ ] **The portal's Terms of Use permit automated access** — else use Broward's
      official bulk-data channel instead
The live path **refuses to run** while `verified` is `False`, by design, so we
never hammer the wrong endpoint.

> **Domain nuance — NOC lookback.** A Notice of Commencement is filed at project
> *start*, often 1–2 years before the distress. Query NOCs on a **longer
> lookback** than lien events (e.g., 24 months) — or rely on the dedup store
> accumulating them — so the stalled-construction premium can fire. A narrow
> recent-date window will miss the NOC and under-score an active stalled build.

### Tests
```bash
python3 -m unittest discover -t . -s distress_radar/tests -p 'test_*.py'
```

### Adding a live county adapter
Subclass `BaseCountyAdapter`, implement `fetch(since, doc_types)` to yield
normalized `RecordedDocument`s from that county's official channel, and register
it in `florida_counties.COUNTY_ADAPTERS`. Use `models.normalize_doc_type()` so the
scorer sees a stable vocabulary. **A high-value enhancement:** join each parcel to
the county Property Appraiser to fill `est_value` and a waterfront flag — that
sharpens the fit score and pre-qualifies the box.

---

## Responsible use — read before going live

This tool reads **public** records, which is lawful and standard practice. It is
built to stay on the right side of that line:

1. **Prefer official data channels** — bulk export, public API, or records request
   — over scraping an interactive portal.
2. **Respect robots.txt, Terms of Use, and rate limits.** Conservative crawl delay
   by default; identify the client honestly.
3. **No evasion.** Do not defeat CAPTCHAs/access controls or rotate
   proxies/credentials to dodge blocks. If a source forbids automation, use its
   official channel or a licensed aggregator.
4. **Verify before acting.** A claim of lien is an *allegation*, not proof of
   default. Recorded data is noisy and sometimes wrong. Every signal is confirmed
   independently before any outreach or commitment — enforced by the verify-first
   checklist on each intake sheet.

---

## Roadmap
- **Broward adapter: implemented** (verify wire config + ToS to go live). Remaining
  five counties follow the same pattern; Acclaim counties can reuse `BrowardWire`.
- **Property Appraiser joins** for `est_value` + waterfront pre-qualification — the
  highest-value next step (sharpens fit scoring and pre-qualifies the box). Without
  it, parcels score on distress alone and fit boosts are limited.
- NOC lookback handling (longer window for Notices of Commencement).
- Developer-level rollup (one sponsor, multiple troubled parcels = portfolio play).
- Scheduling + alerting (daily run → email/Slack the new HOT leads).
- Feed accepted leads directly into the funnel/CRM (the next build).

---

*Internal sourcing tool. Informational only; not legal advice. Confirm data-source
terms and all legal/regulatory steps with licensed counsel before live use.*
