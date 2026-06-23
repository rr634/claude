"""
Breakwater Distress Radar — MOCK adapter.

Returns deterministic synthetic Official-Records data so the full pipeline
(fetch -> normalize -> score -> store -> export) runs end-to-end without any
network access. Use it to validate scoring and to demo the hot list. Real
county adapters replace this with live data behind the same interface.

The synthetic set deliberately includes:
  * a classic stalled-construction stack (NOC + multiple liens)  -> HOT
  * a foreclosure-in-progress (lis pendens + claim of lien)      -> HOT
  * a below-$100K claim                                          -> WATCH (untriggered)
  * an out-of-footprint lien                                     -> WATCH (no fit)
  * a cured lien (claim then release)                            -> IGNORE
  * plain-vanilla noise (a mortgage)                             -> IGNORE
"""
from __future__ import annotations

from datetime import date
from typing import Iterable

from ..models import RecordedDocument, normalize_doc_type
from .base import BaseCountyAdapter

# (county, record_id, raw_label, record_date, amount, parcel_id, address,
#  submarket, party_from(owner/developer), party_to(claimant), est_value)
_SYNTHETIC = [
    # --- Rio Vista stalled spec home: active project + stacked liens -> HOT ---
    ("broward", "CFN-2026-018221", "Notice of Commencement", date(2025, 6, 12), None,
     "5042-12-07-0310", "812 Rio Vista Blvd", "Rio Vista",
     "Rio Vista Estates LLC", "Self", 7_500_000),
    ("broward", "CFN-2026-041877", "Claim of Lien", date(2026, 5, 28), 420_000,
     "5042-12-07-0310", "812 Rio Vista Blvd", "Rio Vista",
     "Rio Vista Estates LLC", "Atlantic Custom Builders LLC", 7_500_000),
    ("broward", "CFN-2026-043990", "Construction Lien", date(2026, 6, 9), 180_000,
     "5042-12-07-0310", "812 Rio Vista Blvd", "Rio Vista",
     "Rio Vista Estates LLC", "Coastal MEP Subcontractors Inc", 7_500_000),

    # --- Coral Gables: foreclosure in progress + contractor lien -> HOT ---
    ("miami_dade", "CFN-2026-220145", "Lis Pendens", date(2026, 6, 2), None,
     "03-4108-019-0450", "1492 Cocoplum Rd", "Coral Gables",
     "Cocoplum Waterfront Partners LLC", "Regional Bank N.A.", 11_200_000),
    ("miami_dade", "CFN-2026-219980", "Claim of Lien", date(2026, 5, 19), 615_000,
     "03-4108-019-0450", "1492 Cocoplum Rd", "Coral Gables",
     "Cocoplum Waterfront Partners LLC", "Gables Structural Group", 11_200_000),

    # --- Miami Beach: active build + lien, mid-box value -> HOT ---
    ("miami_dade", "CFN-2026-221760", "Notice of Commencement", date(2025, 9, 3), None,
     "02-3211-006-0120", "230 Sunset Islands Dr", "Sunset Islands",
     "Sunset Isle Development LLC", "Self", 9_000_000),
    ("miami_dade", "CFN-2026-244015", "Claim of Lien", date(2026, 6, 14), 305_000,
     "02-3211-006-0120", "230 Sunset Islands Dr", "Sunset Islands",
     "Sunset Isle Development LLC", "Premier Concrete & Shell", 9_000_000),

    # --- Palm Beach: tax lien + final judgment, no construction signal -> WATCH ---
    ("palm_beach", "CFN-2026-090233", "Federal Tax Lien", date(2026, 4, 30), 260_000,
     "50-43-46-21-00-001", "1100 S Ocean Blvd", "Manalapan",
     "Ocean Vista Holdings LLC", "IRS", 6_800_000),
    ("palm_beach", "CFN-2026-091500", "Final Judgment", date(2026, 5, 22), 140_000,
     "50-43-46-21-00-001", "1100 S Ocean Blvd", "Manalapan",
     "Ocean Vista Holdings LLC", "Sun Trust Vendors LLC", 6_800_000),

    # --- Las Olas: claim below the $100K trigger -> WATCH (untriggered) ---
    ("broward", "CFN-2026-044120", "Claim of Lien", date(2026, 6, 1), 95_000,
     "5042-10-01-0150", "511 Coconut Isle Dr", "Las Olas",
     "Coconut Isle LLC", "Boutique Millwork Co", 5_400_000),

    # --- Out-of-footprint lien (inland Pompano) -> WATCH (no fit) ---
    ("broward", "CFN-2026-045700", "Claim of Lien", date(2026, 6, 5), 240_000,
     "4842-22-10-0990", "3300 NW 9th Ave", "Pompano Beach",
     "Inland Storage Partners LLC", "Tri-County Paving", 1_100_000),

    # --- Cured lien (claim then release) -> IGNORE ---
    ("palm_beach", "CFN-2026-088010", "Claim of Lien", date(2026, 3, 10), 350_000,
     "06-43-47-09-00-077", "200 Royal Palm Way", "Palm Beach",
     "Royal Palm Renovations LLC", "Apex Builders", 8_200_000),
    ("palm_beach", "CFN-2026-093441", "Satisfaction of Lien", date(2026, 5, 30), None,
     "06-43-47-09-00-077", "200 Royal Palm Way", "Palm Beach",
     "Royal Palm Renovations LLC", "Apex Builders", 8_200_000),

    # --- Pure noise (a mortgage) -> IGNORE ---
    ("broward", "CFN-2026-046001", "Mortgage", date(2026, 6, 10), 3_000_000,
     "5042-09-15-0220", "640 Solar Isle Dr", "Coral Ridge",
     "Solar Isle Owner LLC", "Community Lender FSB", 4_900_000),
]


class MockCountyAdapter(BaseCountyAdapter):
    source_kind = "mock"
    source_url = "synthetic://breakwater/distress_radar"

    def __init__(self, county: str):
        self.county = county

    def fetch(self, since: date, doc_types: list[str]) -> Iterable[RecordedDocument]:
        wanted = set(doc_types) if doc_types else None
        for row in _SYNTHETIC:
            (county, rid, label, rdate, amount, parcel, addr,
             submkt, pfrom, pto, est_value) = row
            if county != self.county:
                continue
            if rdate < since:
                continue
            dtype = normalize_doc_type(label)
            if wanted and dtype not in wanted:
                continue
            yield RecordedDocument(
                county=county, record_id=rid, doc_type=dtype, record_date=rdate,
                amount=amount, parcel_id=parcel, address=addr, submarket=submkt,
                party_from=pfrom, party_to=pto, source_url=self.source_url,
                raw={"raw_label": label, "est_value": est_value},
            )
