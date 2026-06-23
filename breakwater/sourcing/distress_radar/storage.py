"""
Breakwater Distress Radar — persistence (stdlib sqlite3).

Stores every recorded document we have ever seen, de-duplicated by
(county, record_id). This lets the radar run incrementally: each run only
acts on genuinely new filings, and stacking signals accumulate over time.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path
from typing import Iterable

from .models import RecordedDocument

_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    dedup_key   TEXT PRIMARY KEY,
    county      TEXT NOT NULL,
    record_id   TEXT NOT NULL,
    doc_type    TEXT NOT NULL,
    record_date TEXT NOT NULL,
    amount      REAL,
    parcel_id   TEXT,
    address     TEXT,
    submarket   TEXT,
    party_from  TEXT,
    party_to    TEXT,
    book_page   TEXT,
    source_url  TEXT,
    raw         TEXT,
    first_seen  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_parcel ON documents(parcel_id);
CREATE INDEX IF NOT EXISTS idx_county ON documents(county);
"""


class Store:
    def __init__(self, path: str = "exports/distress_radar.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    def upsert(self, docs: Iterable[RecordedDocument]) -> int:
        """Insert new documents; ignore ones already seen. Returns # new."""
        new = 0
        today = date.today().isoformat()
        for d in docs:
            cur = self.conn.execute(
                """INSERT OR IGNORE INTO documents
                   (dedup_key, county, record_id, doc_type, record_date, amount,
                    parcel_id, address, submarket, party_from, party_to,
                    book_page, source_url, raw, first_seen)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (d.dedup_key, d.county, d.record_id, d.doc_type,
                 d.record_date.isoformat(), d.amount, d.parcel_id, d.address,
                 d.submarket, d.party_from, d.party_to, d.book_page,
                 d.source_url, json.dumps(d.raw or {}), today),
            )
            new += cur.rowcount
        self.conn.commit()
        return new

    def all_documents(self) -> list[RecordedDocument]:
        rows = self.conn.execute("SELECT * FROM documents").fetchall()
        cols = [c[0] for c in self.conn.execute("SELECT * FROM documents LIMIT 0").description]
        out = []
        for row in rows:
            r = dict(zip(cols, row))
            out.append(RecordedDocument(
                county=r["county"], record_id=r["record_id"], doc_type=r["doc_type"],
                record_date=date.fromisoformat(r["record_date"]), amount=r["amount"],
                parcel_id=r["parcel_id"], address=r["address"], submarket=r["submarket"],
                party_from=r["party_from"], party_to=r["party_to"], book_page=r["book_page"],
                source_url=r["source_url"], raw=json.loads(r["raw"] or "{}"),
            ))
        return out

    def close(self):
        self.conn.close()
