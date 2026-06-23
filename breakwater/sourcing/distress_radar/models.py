"""
Breakwater Distress Radar — data models and normalization.

A `RecordedDocument` is one row from a county Official Records index.
A `DistressSignal` is the per-parcel aggregation we actually act on.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from . import config


# ---------------------------------------------------------------------------
# Raw-label -> canonical doc type normalization.
# County portals use inconsistent labels; map them here. Adapters should call
# normalize_doc_type() so scoring sees a stable vocabulary.
# ---------------------------------------------------------------------------
_DOC_TYPE_PATTERNS = [
    (r"lis\s*pendens",                        config.LIS_PENDENS),
    (r"claim\s*of\s*lien|construction\s*lien|mechanic", config.CLAIM_OF_LIEN),
    (r"notice\s*of\s*commencement",           config.NOTICE_OF_COMMENCEMENT),
    (r"notice\s*of\s*default",                config.NOTICE_OF_DEFAULT),
    (r"final\s*judg",                         config.FINAL_JUDGMENT),
    (r"judg.*lien|lien.*judg",                config.JUDGMENT_LIEN),
    (r"tax\s*lien|federal\s*tax|irs\s*lien",  config.TAX_LIEN),
    (r"satisfaction|release|discharge",       config.RELEASE),
    (r"mortgage|deed\s*of\s*trust",           config.MORTGAGE),
]


def normalize_doc_type(raw_label: str) -> str:
    s = (raw_label or "").lower()
    for pattern, code in _DOC_TYPE_PATTERNS:
        if re.search(pattern, s):
            return code
    return config.OTHER


@dataclass
class RecordedDocument:
    county: str                       # e.g. "broward"
    record_id: str                    # clerk instrument / CFN number (dedup key)
    doc_type: str                     # canonical code (see config)
    record_date: date
    amount: Optional[float] = None    # lien/claim/judgment amount, if present
    parcel_id: Optional[str] = None   # folio / parcel control number
    address: Optional[str] = None
    submarket: Optional[str] = None   # city / neighborhood
    party_from: Optional[str] = None  # owner / developer (the distressed party)
    party_to: Optional[str] = None    # lienor / plaintiff (the claimant)
    book_page: Optional[str] = None
    source_url: Optional[str] = None
    raw: dict = field(default_factory=dict)

    @property
    def dedup_key(self) -> str:
        return f"{self.county}:{self.record_id}"


@dataclass
class DistressSignal:
    """Per-parcel (or per-owner-without-parcel) aggregation of documents."""
    key: str                          # parcel_id or normalized address
    county: str
    address: Optional[str] = None
    submarket: Optional[str] = None
    developer: Optional[str] = None
    est_value: Optional[float] = None
    docs: list = field(default_factory=list)

    # computed by scoring
    score: float = 0.0
    label: str = "IGNORE"             # HOT / WATCH / IGNORE
    triggered: bool = False           # qualifying lien >= LIEN_MIN_AMOUNT
    max_lien: float = 0.0
    reasons: list = field(default_factory=list)

    def latest_date(self) -> Optional[date]:
        return max((d.record_date for d in self.docs), default=None)
