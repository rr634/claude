"""
Breakwater Distress Radar — CLI entrypoint.

Examples
--------
# Demo end-to-end on synthetic data (no network), last ~90 days, all counties:
    python -m distress_radar.run --mock --since 2026-03-01

# Target specific counties and a higher trigger:
    python -m distress_radar.run --mock --counties broward,miami_dade --min-amount 250000

# Live mode (requires implemented county adapters):
    python -m distress_radar.run --counties broward --since 2026-06-01
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta

from . import config
from .adapters import COUNTY_ADAPTERS, MockCountyAdapter

# Default document types we hunt for (the distress vocabulary).
DEFAULT_DOC_TYPES = [
    config.CLAIM_OF_LIEN, config.LIS_PENDENS, config.NOTICE_OF_COMMENCEMENT,
    config.FINAL_JUDGMENT, config.JUDGMENT_LIEN, config.TAX_LIEN,
    config.NOTICE_OF_DEFAULT, config.RELEASE,
]


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description="Breakwater Distress Radar")
    p.add_argument("--counties", default=",".join(COUNTY_ADAPTERS),
                   help="comma-separated county keys (default: all)")
    p.add_argument("--since", default=None,
                   help="YYYY-MM-DD; default = 90 days ago")
    p.add_argument("--min-amount", type=float, default=config.LIEN_MIN_AMOUNT,
                   help=f"lien trigger amount (default {config.LIEN_MIN_AMOUNT:.0f})")
    p.add_argument("--mock", action="store_true",
                   help="use the synthetic mock adapter (no network) [default]")
    p.add_argument("--live", action="store_true",
                   help="use real county adapters over HTTP (requires verified wire config)")
    p.add_argument("--fixture", default=None,
                   help="path to a saved county response (offline real-parser demo; broward)")
    p.add_argument("--store", default="exports/distress_radar.db")
    p.add_argument("--out", default="exports")
    return p.parse_args(argv)


def _make_adapter(county, args):
    """Pick the adapter for a county given the run mode."""
    if args.fixture and county == "broward":
        from .adapters import BrowardAdapter
        return BrowardAdapter(fixture_path=args.fixture)
    if args.live:
        from .http_client import PoliteClient
        from .adapters import BrowardAdapter, BrowardWire
        if county == "broward":
            return BrowardAdapter(client=PoliteClient(), wire=BrowardWire())
        return COUNTY_ADAPTERS[county]()        # raises NotImplementedError on fetch
    return MockCountyAdapter(county)            # safe default


def main(argv=None):
    args = _parse_args(argv)
    config.LIEN_MIN_AMOUNT = args.min_amount  # allow runtime override
    since = (date.fromisoformat(args.since) if args.since
             else date.today() - timedelta(days=90))
    counties = [c.strip() for c in args.counties.split(",") if c.strip()]

    adapters = []
    for c in counties:
        if c not in COUNTY_ADAPTERS:
            print(f"  ! unknown county '{c}' — skipping")
            continue
        adapters.append(_make_adapter(c, args))

    mode = "FIXTURE" if args.fixture else ("LIVE" if args.live else "MOCK")
    from .pipeline import run
    print(f"Distress Radar — {mode} | "
          f"counties={counties} | since={since} | trigger=${args.min_amount:,.0f}")
    summary = run(adapters, since, DEFAULT_DOC_TYPES, args.store, args.out)
    print(f"  fetched={summary['fetched']} new={summary['new']} "
          f"parcels={summary['parcels']} HOT={summary['hot']} WATCH={summary['watch']}")
    print(f"  → {summary['out_dir']}/hot_list.csv, signals.json, intake_*.md")
    return summary


if __name__ == "__main__":
    main()
