"""
Breakwater Distress Radar — Florida county adapter stubs.

These are deliberately UNIMPLEMENTED. Florida Official Records are public
(Sunshine law), but each county clerk exposes them differently and most
portals carry Terms of Use and rate limits. Wire each adapter to its county's
official data channel and honor the responsible-use contract in base.py.

Per-county source notes below capture where to connect and what to prefer.
The general priority order for EVERY county:
    official bulk data  >  official API  >  public-records request  >
    polite portal access  >  licensed third-party aggregator
Never defeat access controls or evade blocks; use the official channel.

Document types to query (canonical codes in config):
    CLAIM_OF_LIEN, LIS_PENDENS, NOTICE_OF_COMMENCEMENT, FINAL_JUDGMENT,
    JUDGMENT_LIEN, TAX_LIEN, NOTICE_OF_DEFAULT, RELEASE
"""
from .base import BaseCountyAdapter


class BrowardAdapter(BaseCountyAdapter):
    county = "broward"
    source_kind = "portal"
    # Broward County Records, Taxes & Treasury — Official Records search.
    # Check for a bulk/subscription data feed before automating the portal.
    source_url = "https://officialrecords.broward.org/"
    notes = ("Operational core. Highest priority. Look for the County's records "
             "data subscription / bulk export; otherwise polite, rate-limited "
             "queries by recorded date + document type.")


class MiamiDadeAdapter(BaseCountyAdapter):
    county = "miami_dade"
    source_kind = "api"
    # Miami-Dade Clerk Official Records; County also publishes Open Data sets.
    source_url = "https://onlineservices.miamidadeclerk.gov/officialrecords/"
    notes = ("Check Miami-Dade Open Data portal for downloadable recordings and "
             "the Property Appraiser API for parcel/value joins.")


class PalmBeachAdapter(BaseCountyAdapter):
    county = "palm_beach"
    source_kind = "portal"
    source_url = "https://erec.mypalmbeachclerk.com/"   # Clerk & Comptroller e-Records
    notes = ("Palm Beach Clerk e-Records. Join to Property Appraiser (PAPA) for "
             "value and waterfront flags.")


class MartinAdapter(BaseCountyAdapter):
    county = "martin"
    source_kind = "portal"
    source_url = "https://www.martinclerk.com/official-records"
    notes = "Treasure Coast reach — Stuart, Sewall's Point, Jupiter Island."


class StLucieAdapter(BaseCountyAdapter):
    county = "st_lucie"
    source_kind = "portal"
    source_url = "https://www.stlucieclerk.com/official-records"
    notes = "Treasure Coast reach — Vero Beach corridor."


class MonroeAdapter(BaseCountyAdapter):
    county = "monroe"
    source_kind = "portal"
    source_url = "https://www.monroe-clerk.com/official-records"
    notes = "Keys reach — Islamorada, Key Largo."


# Registry consumed by the pipeline / CLI.
COUNTY_ADAPTERS = {
    "broward": BrowardAdapter,
    "miami_dade": MiamiDadeAdapter,
    "palm_beach": PalmBeachAdapter,
    "martin": MartinAdapter,
    "st_lucie": StLucieAdapter,
    "monroe": MonroeAdapter,
}
