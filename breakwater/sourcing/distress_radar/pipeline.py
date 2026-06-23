"""
Breakwater Distress Radar — pipeline orchestration.

fetch (per adapter) -> store/dedup -> score ALL known docs -> export.

Scoring runs over the full stored history (not just this run's new docs) so a
lien recorded last month and a lis pendens recorded today aggregate into one
strengthening signal on the same parcel.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

from . import config
from .models import DistressSignal
from .scoring import score_all
from .storage import Store


def run(adapters, since: date, doc_types: list[str],
        store_path: str, out_dir: str) -> dict:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    store = Store(store_path)

    fetched = 0
    new = 0
    for adapter in adapters:
        docs = list(adapter.fetch(since, doc_types))
        fetched += len(docs)
        new += store.upsert(docs)

    signals = score_all(store.all_documents())
    hot = [s for s in signals if s.label == "HOT"]
    watch = [s for s in signals if s.label == "WATCH"]

    _write_csv(signals, Path(out_dir) / "hot_list.csv")
    _write_json(signals, Path(out_dir) / "signals.json")
    for s in hot:
        _write_intake(s, Path(out_dir))

    store.close()
    return {
        "fetched": fetched, "new": new,
        "parcels": len(signals), "hot": len(hot), "watch": len(watch),
        "out_dir": out_dir,
    }


def _write_csv(signals: list[DistressSignal], path: Path):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "label", "score", "triggered", "county", "submarket",
                    "address", "developer", "max_lien", "est_value",
                    "doc_count", "latest_date", "doc_types"])
        for i, s in enumerate(signals, 1):
            w.writerow([
                i, s.label, s.score, "YES" if s.triggered else "",
                s.county, s.submarket or "", s.address or "", s.developer or "",
                f"{s.max_lien:.0f}" if s.max_lien else "",
                f"{s.est_value:.0f}" if s.est_value else "",
                len(s.docs), s.latest_date().isoformat() if s.latest_date() else "",
                "|".join(sorted({d.doc_type for d in s.docs})),
            ])


def _write_json(signals: list[DistressSignal], path: Path):
    payload = []
    for s in signals:
        payload.append({
            "key": s.key, "label": s.label, "score": s.score,
            "triggered": s.triggered, "county": s.county, "submarket": s.submarket,
            "address": s.address, "developer": s.developer,
            "max_lien": s.max_lien, "est_value": s.est_value,
            "latest_date": s.latest_date().isoformat() if s.latest_date() else None,
            "reasons": s.reasons,
            "documents": [{
                "record_id": d.record_id, "doc_type": d.doc_type,
                "record_date": d.record_date.isoformat(), "amount": d.amount,
                "party_from": d.party_from, "party_to": d.party_to,
                "source_url": d.source_url,
            } for d in s.docs],
        })
    path.write_text(json.dumps(payload, indent=2))


def _write_intake(s: DistressSignal, out_dir: Path):
    """Pre-fill the Acquisition Screening Box intake sheet (artifact 03)."""
    safe = s.key.replace(":", "_").replace(" ", "_").replace("/", "_")
    lines = [
        f"# Distress Radar — Lead Intake",
        f"*Auto-generated {date.today().isoformat()} · feeds Screening Box (artifact 03)*",
        "",
        f"- **Signal label:** {s.label}  (score {s.score}; "
        f"{'TRIGGERED ≥ $100K' if s.triggered else 'not triggered'})",
        f"- **Lead source:** Distress Radar — county Official Records",
        f"- **Address / submarket:** {s.address or 'n/a'} — {s.submarket or 'n/a'} ({s.county})",
        f"- **Developer / owner:** {s.developer or 'n/a'}",
        f"- **Largest recorded lien:** ${s.max_lien:,.0f}" if s.max_lien else "- **Largest recorded lien:** n/a",
        f"- **Est. finished value:** ${s.est_value:,.0f}" if s.est_value else "- **Est. finished value:** n/a",
        "",
        "## Why it flagged",
    ]
    lines += [f"- {r}" for r in s.reasons]
    lines += [
        "",
        "## Recorded documents",
        "| Date | Type | Amount | Claimant | Instrument |",
        "|---|---|---|---|---|",
    ]
    for d in sorted(s.docs, key=lambda x: x.record_date):
        amt = f"${d.amount:,.0f}" if d.amount else "—"
        lines.append(f"| {d.record_date.isoformat()} | {d.doc_type.replace('_',' ').title()} "
                     f"| {amt} | {d.party_to or '—'} | {d.record_id} |")
    lines += [
        "",
        "## Next actions (verify before any outreach)",
        "- [ ] Confirm parcel, owner entity, and lien validity in Official Records",
        "- [ ] Pull title / mortgage to map the capital stack and distress trigger",
        "- [ ] Confirm construction status (% complete) and permit history",
        "- [ ] Run the Screening Box hard filters + score; if PURSUE, open the model",
        "- [ ] Identify control path (note / pref / JV / DIL / foreclosure / REO)",
        "",
        "> A claim of lien is an allegation, not proof of default. Verify independently.",
    ]
    (out_dir / f"intake_{safe}.md").write_text("\n".join(lines))
