# County adapters — the real monitoring source

Each adapter turns a property into a list of **public recordings** (deeds, mortgages, liens,
judgments) pulled from that county's Official Records, in a normalized shape the diff engine
understands:

```js
// async fetchRecordings({ address, parcelId, ownerName, county, state })
[
  { id: 'INSTRUMENT-NO', recordedAt: '2025-11-01', type: 'deed',
    grantor: '...', grantee: '...', bookPage: '12345/678', raw: {/* original */} }
]
```

`id` must be the county's **stable instrument / clerk number** so re-scans can tell new filings
from already-seen ones.

## Florida reality (how to build real ones)

Florida has 67 counties and **no single API**. Each clerk publishes Official Records differently:

- **Miami-Dade** — Clerk of Courts Official Records search (web + some data endpoints).
- **Broward** — County Records, Taxes & Treasury Official Records search.
- **Palm Beach** — Clerk & Comptroller Official Records.
- Many mid/smaller counties run common vendor portals (e.g. the same "Official Records Search"
  software), so **one adapter can often cover several counties** with a different base URL.

### Recommended build order (biggest markets first)
1. `fl-miami-dade`, `fl-broward`, `fl-palm-beach` (South FL — highest fraud + population).
2. Tampa Bay (`fl-hillsborough`, `fl-pinellas`), `fl-orange` (Orlando), `fl-lee` (Ft. Myers/Naples).
3. A generic vendor-portal adapter parameterized by county to sweep up the rest.

### Each adapter should
- Search by **owner name** and/or **parcel/legal description** (store both on the property).
- Return only recordings at/after the baseline date on incremental scans (cheaper).
- Be polite: cache, throttle, respect robots/terms; prefer official **data downloads / APIs**
  over HTML scraping where a county offers them. Several FL clerks offer bulk/subscription data —
  that's the durable path at scale.
- Normalize document types to: `deed | mortgage | lien | judgment | other`.

### Alternative: a data vendor
Commercial property-data APIs can cover many counties at once (faster to launch, ongoing cost).
Wrap one behind this same `fetchRecordings` interface and the rest of the pipeline is unchanged.

Until a real adapter lands, `COUNTY_ADAPTER=mock` keeps the full signup → scan → alert flow working.
