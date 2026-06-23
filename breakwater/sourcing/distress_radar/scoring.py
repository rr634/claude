"""
Breakwater Distress Radar — distress scoring engine.

Aggregates recorded documents into per-parcel DistressSignals and scores them
against the Breakwater thesis. The output is a ranked hot list that feeds the
Acquisition Screening Box (artifact 03).
"""
from __future__ import annotations

import re
from typing import Iterable

from . import config
from .models import DistressSignal, RecordedDocument


def _parcel_key(doc: RecordedDocument) -> str:
    if doc.parcel_id:
        return f"{doc.county}:{doc.parcel_id}"
    # fall back to a normalized address when no parcel id is present
    addr = re.sub(r"\s+", " ", (doc.address or "UNKNOWN").strip().upper())
    return f"{doc.county}:{addr}"


def aggregate(docs: Iterable[RecordedDocument]) -> list[DistressSignal]:
    signals: dict[str, DistressSignal] = {}
    for d in docs:
        k = _parcel_key(d)
        sig = signals.get(k)
        if sig is None:
            sig = DistressSignal(key=k, county=d.county, address=d.address,
                                 submarket=d.submarket, developer=d.party_from)
            signals[k] = sig
        sig.docs.append(d)
        # backfill descriptive fields as documents arrive
        sig.address = sig.address or d.address
        sig.submarket = sig.submarket or d.submarket
        sig.developer = sig.developer or d.party_from
        ev = (d.raw or {}).get("est_value")
        if ev and not sig.est_value:
            sig.est_value = ev
    return list(signals.values())


def _amount_band_points(amount: float) -> int:
    for floor, pts in config.AMOUNT_BANDS:
        if amount >= floor:
            return pts
    return 0


def _submarket_is_target(submarket: str | None) -> bool:
    if not submarket:
        return False
    s = submarket.lower()
    return any(t.lower() in s for t in config.all_submarkets())


def score_signal(sig: DistressSignal) -> DistressSignal:
    score = 0.0
    reasons: list[str] = []
    types = {d.doc_type for d in sig.docs}

    # 1. Document-type signals
    for t, w in config.DOC_WEIGHTS.items():
        if t in types:
            score += w
            reasons.append(f"{t.replace('_',' ').title()} on record (+{w})")

    # 2. Lien amount band (largest qualifying lien on the parcel)
    liens = [d.amount for d in sig.docs
             if d.doc_type in config.LIEN_DOC_TYPES and d.amount]
    sig.max_lien = max(liens) if liens else 0.0
    if sig.max_lien:
        band = _amount_band_points(sig.max_lien)
        if band:
            score += band
            reasons.append(f"Largest lien ${sig.max_lien:,.0f} (+{band})")

    # 3. Hard trigger — the founder's $100K rule
    sig.triggered = sig.max_lien >= config.LIEN_MIN_AMOUNT
    if sig.triggered:
        reasons.append(f"TRIGGER: lien ≥ ${config.LIEN_MIN_AMOUNT:,.0f}")

    # 4. Stalled-construction premium (active project + lien = our target)
    if config.NOTICE_OF_COMMENCEMENT in types and (types & config.LIEN_DOC_TYPES):
        score += config.PREMIUM_STALLED_CONSTRUCTION
        reasons.append(f"Active construction + lien = stalled project "
                       f"(+{config.PREMIUM_STALLED_CONSTRUCTION})")

    # 5. Stacking — multiple liens compound the distress
    if len(liens) >= 2:
        add = config.STACK_PER_EXTRA_LIEN * (len(liens) - 1)
        score += add
        reasons.append(f"{len(liens)} liens stacking (+{add})")

    # 6. Release/satisfaction recorded — problem may be cured, de-prioritize
    if config.RELEASE in types:
        score -= config.RELEASE_PENALTY
        reasons.append(f"Release/satisfaction on record (-{config.RELEASE_PENALTY})")

    # 7. Fit boosts
    if _submarket_is_target(sig.submarket):
        score += config.FIT_SUBMARKET
        reasons.append(f"Target submarket (+{config.FIT_SUBMARKET})")
    if sig.est_value and config.EXIT_VALUE_BOX[0] <= sig.est_value <= config.EXIT_VALUE_BOX[1]:
        score += config.FIT_VALUE_BOX
        reasons.append(f"Est. value in acquisition box (+{config.FIT_VALUE_BOX})")

    sig.score = round(max(score, 0.0), 1)
    sig.reasons = reasons
    sig.label = _classify(sig)
    return sig


def _classify(sig: DistressSignal) -> str:
    if sig.triggered and sig.score >= config.SCORE_THRESHOLD_HOT:
        return "HOT"
    if sig.score >= config.SCORE_THRESHOLD_WATCH:
        return "WATCH"
    return "IGNORE"


def score_all(docs: Iterable[RecordedDocument]) -> list[DistressSignal]:
    signals = [score_signal(s) for s in aggregate(docs)]
    # Sort: HOT first, then by score desc, then by recency.
    order = {"HOT": 0, "WATCH": 1, "IGNORE": 2}
    signals.sort(key=lambda s: (order[s.label], -s.score,
                                -(s.latest_date().toordinal() if s.latest_date() else 0)))
    return signals
