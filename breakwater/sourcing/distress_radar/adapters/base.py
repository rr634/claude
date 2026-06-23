"""
Breakwater Distress Radar — county adapter interface.

Each county exposes its Official Records differently. A county adapter's only
job is to fetch recently recorded documents and yield normalized
`RecordedDocument` objects. Scoring, storage, and export are county-agnostic.

RESPONSIBLE-USE CONTRACT (every real adapter must honor this):
  1. Prefer the county's OFFICIAL bulk-data export, public API, or public-records
     request feed over scraping an interactive portal.
  2. Respect robots.txt, published Terms of Use, and rate limits. Default to a
     conservative crawl delay; identify the client honestly via User-Agent.
  3. Do NOT defeat CAPTCHAs or other access controls, and do NOT use rotating
     proxies/credentials to evade blocks. If a source forbids automated access,
     use its official data channel or a licensed third-party aggregator instead.
  4. Recorded data is noisy and sometimes erroneous. A claim of lien is an
     allegation, not proof of default — every signal must be independently
     verified before any outreach or commitment.
"""
from __future__ import annotations

from datetime import date
from typing import Iterable

from ..models import RecordedDocument


class BaseCountyAdapter:
    county: str = "base"
    #: Polite default crawl delay (seconds) for real HTTP adapters.
    crawl_delay_seconds: float = 2.0
    #: Where the data comes from — documented per county for auditability.
    source_url: str = ""
    source_kind: str = "unimplemented"   # "bulk" | "api" | "portal" | "aggregator"

    def fetch(self, since: date, doc_types: list[str]) -> Iterable[RecordedDocument]:
        """Yield documents recorded on/after `since` matching `doc_types`.

        Implementations should:
          - query only the requested doc_types where the source allows it,
          - normalize raw labels via models.normalize_doc_type(),
          - set record_id to the clerk instrument/CFN (stable dedup key),
          - populate amount/parcel_id/address/submarket/parties where available.
        """
        raise NotImplementedError(
            f"Adapter for county '{self.county}' is not implemented. "
            f"See adapters/florida_counties.py for source notes."
        )
