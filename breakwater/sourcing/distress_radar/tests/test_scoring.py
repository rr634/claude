"""Scoring + classification over the synthetic mock data set."""
import unittest
from datetime import date

from .. import config
from ..adapters import MockCountyAdapter
from ..scoring import score_all


def _all_mock_signals():
    docs = []
    for c in ("broward", "miami_dade", "palm_beach"):
        docs += list(MockCountyAdapter(c).fetch(date(2000, 1, 1),
                                                [config.CLAIM_OF_LIEN, config.LIS_PENDENS,
                                                 config.NOTICE_OF_COMMENCEMENT, config.FINAL_JUDGMENT,
                                                 config.TAX_LIEN, config.RELEASE]))
    return {s.address: s for s in score_all(docs)}, score_all(docs)


class TestScoring(unittest.TestCase):
    def setUp(self):
        self.by_addr, self.ordered = _all_mock_signals()

    def test_rio_vista_is_hot_and_triggered(self):
        s = self.by_addr["812 Rio Vista Blvd"]
        self.assertEqual(s.label, "HOT")
        self.assertTrue(s.triggered)
        self.assertEqual(s.max_lien, 420000.0)
        self.assertTrue(any("stalled project" in r for r in s.reasons))
        self.assertTrue(any("stacking" in r for r in s.reasons))

    def test_below_threshold_lien_not_triggered(self):
        s = self.by_addr["511 Coconut Isle Dr"]   # $95K claim
        self.assertFalse(s.triggered)
        self.assertEqual(s.label, "WATCH")

    def test_released_lien_suppressed(self):
        s = self.by_addr["200 Royal Palm Way"]     # claim + satisfaction
        self.assertEqual(s.label, "IGNORE")

    def test_out_of_footprint_no_fit(self):
        s = self.by_addr["3300 NW 9th Ave"]         # Pompano, $240K
        self.assertTrue(s.triggered)
        self.assertEqual(s.label, "WATCH")          # triggered but no fit, low score
        self.assertFalse(any("Target submarket" in r for r in s.reasons))

    def test_hot_sorts_first(self):
        labels = [s.label for s in self.ordered]
        self.assertEqual(labels.count("HOT"), 4)
        # all HOT precede the first non-HOT
        first_non_hot = next(i for i, l in enumerate(labels) if l != "HOT")
        self.assertTrue(all(l == "HOT" for l in labels[:first_non_hot]))


if __name__ == "__main__":
    unittest.main()
