"""Broward adapter: parser + fixture-mode fetch (offline)."""
import json
import unittest
from datetime import date
from pathlib import Path

from .. import config
from ..adapters.broward import BrowardAdapter, BrowardWire, parse_records, _parse_amount, _parse_date

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "broward_sample.json"


class TestParsers(unittest.TestCase):
    def test_parse_amount(self):
        self.assertEqual(_parse_amount("$420,000.00"), 420000.0)
        self.assertEqual(_parse_amount("0.00"), 0.0)
        self.assertEqual(_parse_amount(95000), 95000.0)
        self.assertIsNone(_parse_amount(None))
        self.assertIsNone(_parse_amount(""))

    def test_parse_date(self):
        self.assertEqual(_parse_date("2026-05-28"), date(2026, 5, 28))
        self.assertEqual(_parse_date("05/28/2026"), date(2026, 5, 28))
        self.assertIsNone(_parse_date(""))

    def test_parse_records_maps_and_normalizes(self):
        payload = json.loads(FIXTURE.read_text())
        recs = parse_records(payload, BrowardWire())
        self.assertEqual(len(recs), 4)
        by_id = {r.record_id: r for r in recs}

        lien = by_id["117654321"]
        self.assertEqual(lien.doc_type, config.CLAIM_OF_LIEN)
        self.assertEqual(lien.amount, 420000.0)
        self.assertEqual(lien.submarket, "Rio Vista")
        self.assertEqual(lien.party_from, "RIO VISTA ESTATES LLC")
        self.assertEqual(lien.book_page, "59021/1187")
        self.assertEqual(lien.county, "broward")

        self.assertEqual(by_id["117654322"].doc_type, config.NOTICE_OF_COMMENCEMENT)
        self.assertIsNone(by_id["117654322"].amount)
        self.assertEqual(by_id["117660045"].doc_type, config.LIS_PENDENS)
        self.assertEqual(by_id["117661120"].doc_type, config.RELEASE)


class TestFixtureFetch(unittest.TestCase):
    def test_since_filter(self):
        a = BrowardAdapter(fixture_path=str(FIXTURE))
        recs = list(a.fetch(date(2026, 1, 1), []))
        # The 2025 Notice of Commencement is filtered out by `since`.
        self.assertTrue(all(r.record_date >= date(2026, 1, 1) for r in recs))
        self.assertEqual(len(recs), 3)

    def test_doctype_filter(self):
        a = BrowardAdapter(fixture_path=str(FIXTURE))
        recs = list(a.fetch(date(2000, 1, 1), [config.LIS_PENDENS]))
        self.assertEqual([r.doc_type for r in recs], [config.LIS_PENDENS])

    def test_live_refuses_until_verified(self):
        a = BrowardAdapter(client=object(), wire=BrowardWire(verified=False))
        with self.assertRaises(RuntimeError):
            list(a.fetch(date(2026, 1, 1), []))


if __name__ == "__main__":
    unittest.main()
