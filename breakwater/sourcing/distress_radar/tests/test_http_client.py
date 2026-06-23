"""PoliteClient: robots + backoff behavior (no network)."""
import unittest
import urllib.robotparser

from ..http_client import PoliteClient, RobotsDisallowed


def _robots(lines):
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(lines)
    return rp


class TestPoliteClient(unittest.TestCase):
    def _client_with_robots(self, lines):
        c = PoliteClient(min_delay_seconds=0)
        c._robots["https://officialrecords.broward.org"] = _robots(lines)
        return c

    def test_allows_when_permitted(self):
        c = self._client_with_robots(["User-agent: *", "Allow: /"])
        self.assertTrue(c._allowed("https://officialrecords.broward.org/AcclaimWeb/search"))

    def test_blocks_when_disallowed(self):
        c = self._client_with_robots(["User-agent: *", "Disallow: /AcclaimWeb"])
        self.assertFalse(c._allowed("https://officialrecords.broward.org/AcclaimWeb/search"))

    def test_get_raises_on_disallowed_before_any_network(self):
        c = self._client_with_robots(["User-agent: *", "Disallow: /"])
        with self.assertRaises(RobotsDisallowed):
            c.get("https://officialrecords.broward.org/AcclaimWeb/search")

    def test_respect_robots_false_bypasses(self):
        c = self._client_with_robots(["User-agent: *", "Disallow: /"])
        c.respect_robots = False
        self.assertTrue(c._allowed("https://officialrecords.broward.org/anything"))

    def test_backoff_monotonic_and_capped(self):
        self.assertLess(PoliteClient._backoff(1), PoliteClient._backoff(2))
        self.assertLessEqual(PoliteClient._backoff(10), 30.0)


if __name__ == "__main__":
    unittest.main()
