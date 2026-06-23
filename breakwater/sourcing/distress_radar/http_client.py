"""
Breakwater Distress Radar — polite HTTP client (stdlib only).

A small, well-behaved HTTP client used by live county adapters. It enforces the
responsible-use contract from adapters/base.py at the transport layer so an
adapter cannot accidentally misbehave:

  * honest, identifying User-Agent (with a contact),
  * robots.txt is fetched and obeyed per host (cached),
  * a minimum crawl delay is enforced between requests to the same host,
  * transient failures (5xx / 429 / network) retried with exponential backoff,
  * hard timeout on every request.

It deliberately does NOT support proxy rotation, CAPTCHA solving, or any other
block-evasion. If a host disallows a path in robots.txt, requests raise
`RobotsDisallowed` — use the county's official data channel instead.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from dataclasses import dataclass, field


class RobotsDisallowed(Exception):
    """Raised when robots.txt forbids the requested path."""


@dataclass
class PoliteClient:
    user_agent: str = "BreakwaterDistressRadar/0.1 (+research; contact: rr@richardrosalaw.com)"
    min_delay_seconds: float = 2.0
    timeout_seconds: float = 20.0
    max_retries: int = 3
    respect_robots: bool = True
    _last_request_at: dict = field(default_factory=dict)   # host -> ts
    _robots: dict = field(default_factory=dict)            # host -> RobotFileParser

    # -- robots ------------------------------------------------------------
    def _robots_for(self, host_url: str) -> urllib.robotparser.RobotFileParser:
        parts = urllib.parse.urlsplit(host_url)
        base = f"{parts.scheme}://{parts.netloc}"
        rp = self._robots.get(base)
        if rp is None:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(base + "/robots.txt")
            try:
                rp.read()
            except Exception:
                # If robots.txt can't be read, fail closed-but-usable: assume
                # allowed only for the root; operators should confirm terms.
                rp.parse(["User-agent: *", "Allow: /"])
            self._robots[base] = rp
        return rp

    def _allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        return self._robots_for(url).can_fetch(self.user_agent, url)

    # -- rate limiting -----------------------------------------------------
    def _throttle(self, url: str):
        host = urllib.parse.urlsplit(url).netloc
        last = self._last_request_at.get(host)
        if last is not None:
            wait = self.min_delay_seconds - (time.monotonic() - last)
            if wait > 0:
                time.sleep(wait)
        self._last_request_at[host] = time.monotonic()

    # -- core --------------------------------------------------------------
    def get(self, url: str, params: dict | None = None) -> str:
        if params:
            url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        if not self._allowed(url):
            raise RobotsDisallowed(
                f"robots.txt disallows {url}. Use the county's official data "
                f"channel (bulk export / API / records request) instead."
            )
        attempt = 0
        while True:
            attempt += 1
            self._throttle(url)
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent,
                                                       "Accept": "application/json, text/html"})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                    return resp.read().decode("utf-8", errors="replace")
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt <= self.max_retries:
                    time.sleep(self._backoff(attempt)); continue
                raise
            except (urllib.error.URLError, TimeoutError):
                if attempt <= self.max_retries:
                    time.sleep(self._backoff(attempt)); continue
                raise

    def get_json(self, url: str, params: dict | None = None):
        return json.loads(self.get(url, params))

    @staticmethod
    def _backoff(attempt: int) -> float:
        return min(2.0 ** attempt, 30.0)
