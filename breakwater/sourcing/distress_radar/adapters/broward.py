"""
Breakwater Distress Radar — Broward County adapter (operational core).

Broward's Official Records portal runs on the Harris "Acclaim" platform
(AcclaimWeb) — the same platform several Florida clerks use, so this adapter is
a template for those counties too.

WHAT IS REAL AND TESTED HERE
  * The full fetch loop: per-doc-type queries, monthly date chunking,
    pagination, polite HTTP via PoliteClient, and parsing → RecordedDocument.
  * `parse_records()` — the response parser — is unit-tested against a fixture
    (fixtures/broward_sample.json) and runs offline.

WHAT YOU MUST VERIFY AGAINST THE LIVE SITE BEFORE LIVE USE
  * The exact endpoint path, query-parameter names, doc-type query codes, and
    response field names are isolated in `BrowardWire` and marked VERIFY. They
    are representative of the Acclaim platform, not captured from production.
  * Set `BrowardWire.verified = True` only after confirming them (and after
    confirming the portal's Terms of Use permit automated access — otherwise
    use Broward's official bulk-data channel). Live fetch refuses to run until
    then, by design, so we never hammer the wrong endpoint.

USAGE
  Offline / test:  BrowardAdapter(fixture_path="fixtures/broward_sample.json")
  Live:            BrowardAdapter(client=PoliteClient(), wire=BrowardWire(verified=True))
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

from .. import config
from ..models import RecordedDocument, normalize_doc_type
from .base import BaseCountyAdapter


# ---------------------------------------------------------------------------
# Wire contract — the ONLY county-specific unknowns, isolated for verification.
# ---------------------------------------------------------------------------
@dataclass
class BrowardWire:
    verified: bool = False                       # operator flips True post-verification
    base_url: str = "https://officialrecords.broward.org"
    search_path: str = "/AcclaimWeb/search/SearchTypeDocType"   # VERIFY
    # request param names (VERIFY)
    p_date_from: str = "RecordDateFrom"
    p_date_to: str = "RecordDateTo"
    p_doctype: str = "DocTypes"
    p_page: str = "page"
    p_page_size: str = "pageSize"
    page_size: int = 50
    # response field names (VERIFY)
    f_results: str = "results"
    f_total: str = "total"
    f_instrument: str = "instrumentNumber"
    f_doctype: str = "documentType"
    f_date: str = "recordDate"
    f_amount: str = "consideration"
    f_parcel: str = "parcelId"
    f_address: str = "address"
    f_city: str = "city"
    f_party_from: str = "directName"     # grantor / owner-developer
    f_party_to: str = "indirectName"     # grantee / claimant
    f_book: str = "book"
    f_page_no: str = "pageNumber"
    f_url: str = "documentUrl"
    # canonical doc type -> county query code(s) (VERIFY against Acclaim list)
    doctype_query_codes: dict = field(default_factory=lambda: {
        config.CLAIM_OF_LIEN:          ["LIE", "CLN", "LIEN"],
        config.LIS_PENDENS:            ["LIS"],
        config.NOTICE_OF_COMMENCEMENT: ["NOC"],
        config.FINAL_JUDGMENT:         ["JUD", "FJ"],
        config.JUDGMENT_LIEN:          ["JLN"],
        config.TAX_LIEN:               ["FTL", "TAX"],
        config.NOTICE_OF_DEFAULT:      ["NOD"],
        config.RELEASE:                ["SAT", "REL"],
    })


def _parse_amount(raw) -> float | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    s = re.sub(r"[^\d.]", "", str(raw))
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(raw) -> date | None:
    if not raw:
        return None
    s = str(raw).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            from datetime import datetime
            return datetime.strptime(s[:len(fmt) + 2], fmt).date() if "T" not in fmt \
                else datetime.fromisoformat(s).date()
        except ValueError:
            continue
    try:
        from datetime import datetime
        return datetime.fromisoformat(s).date()
    except ValueError:
        return None


def parse_records(payload: dict, wire: BrowardWire) -> list[RecordedDocument]:
    """Map a raw Acclaim-style response into normalized RecordedDocuments.

    Pure, offline, and unit-tested. Skips rows missing an instrument number or
    a parseable record date.
    """
    out: list[RecordedDocument] = []
    for r in payload.get(wire.f_results, []) or []:
        rid = r.get(wire.f_instrument)
        rdate = _parse_date(r.get(wire.f_date))
        if not rid or rdate is None:
            continue
        book = r.get(wire.f_book)
        pageno = r.get(wire.f_page_no)
        out.append(RecordedDocument(
            county="broward",
            record_id=str(rid),
            doc_type=normalize_doc_type(r.get(wire.f_doctype, "")),
            record_date=rdate,
            amount=_parse_amount(r.get(wire.f_amount)),
            parcel_id=r.get(wire.f_parcel),
            address=r.get(wire.f_address),
            submarket=r.get(wire.f_city),
            party_from=r.get(wire.f_party_from),
            party_to=r.get(wire.f_party_to),
            book_page=(f"{book}/{pageno}" if book and pageno else None),
            source_url=r.get(wire.f_url),
            raw={"raw_label": r.get(wire.f_doctype, ""), **r},
        ))
    return out


def _month_windows(since: date, until: date):
    """Yield (from, to) month-sized windows to keep result pages bounded."""
    from calendar import monthrange
    cur = date(since.year, since.month, 1)
    while cur <= until:
        last = date(cur.year, cur.month, monthrange(cur.year, cur.month)[1])
        yield (max(cur, since), min(last, until))
        cur = date(cur.year + (cur.month // 12), (cur.month % 12) + 1, 1)


class BrowardAdapter(BaseCountyAdapter):
    county = "broward"
    source_kind = "portal"
    source_url = "https://officialrecords.broward.org"

    def __init__(self, client=None, wire: BrowardWire | None = None,
                 fixture_path: str | None = None):
        self.client = client
        self.wire = wire or BrowardWire()
        self.fixture_path = fixture_path

    # -- offline mode ------------------------------------------------------
    def _from_fixture(self, since, doc_types):
        payload = json.loads(Path(self.fixture_path).read_text())
        wanted = set(doc_types) if doc_types else None
        for d in parse_records(payload, self.wire):
            if d.record_date < since:
                continue
            if wanted and d.doc_type not in wanted:
                continue
            yield d

    # -- live mode ---------------------------------------------------------
    def _from_live(self, since, doc_types):
        if not self.wire.verified:
            raise RuntimeError(
                "BrowardWire.verified is False. Confirm the live endpoint, "
                "parameter names, doc-type codes, response fields, AND the "
                "portal's Terms of Use, then set wire.verified=True (or prefer "
                "Broward's official bulk-data channel). Refusing to query."
            )
        if self.client is None:
            raise RuntimeError("Live mode requires a PoliteClient (client=...).")
        url = self.wire.base_url + self.wire.search_path
        until = date.today()
        seen: set[str] = set()
        for dtype in (doc_types or list(self.wire.doctype_query_codes)):
            codes = self.wire.doctype_query_codes.get(dtype)
            if not codes:
                continue
            for win_from, win_to in _month_windows(since, until):
                page = 1
                while True:
                    payload = self.client.get_json(url, {
                        self.wire.p_date_from: win_from.isoformat(),
                        self.wire.p_date_to:   win_to.isoformat(),
                        self.wire.p_doctype:   ",".join(codes),
                        self.wire.p_page:      page,
                        self.wire.p_page_size: self.wire.page_size,
                    })
                    recs = parse_records(payload, self.wire)
                    if not recs:
                        break
                    for d in recs:
                        if d.dedup_key in seen:
                            continue
                        seen.add(d.dedup_key)
                        yield d
                    if len(recs) < self.wire.page_size:
                        break
                    page += 1

    def fetch(self, since: date, doc_types: list[str]) -> Iterable[RecordedDocument]:
        if self.fixture_path:
            yield from self._from_fixture(since, doc_types)
        else:
            yield from self._from_live(since, doc_types)
