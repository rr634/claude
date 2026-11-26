// County-adapter registry.
//
// A county adapter implements ONE function:
//   async fetchRecordings({ address, parcelId, ownerName, county, state })
//     -> Promise<Array<{ id, recordedAt, type, grantor, grantee, bookPage, raw }>>
//
// `id` must be stable per recording (e.g. the county's instrument/clerk number) so the
// diff engine can tell new filings from ones it has already seen.
//
// Start with `mock` (deterministic, runs anywhere). Add real adapters per county and
// register them below. Select the active adapter with the COUNTY_ADAPTER env var, or map
// per-property by its `county` field once multiple real adapters exist.

const mock = require('./mock');

const adapters = {
  mock,
  // 'fl-broward': require('./fl-broward'),
  // 'fl-miami-dade': require('./fl-miami-dade'),
  // 'fl-palm-beach': require('./fl-palm-beach'),
};

function getAdapter(county) {
  // Explicit override wins (useful while only the mock exists).
  const forced = process.env.COUNTY_ADAPTER;
  if (forced && adapters[forced]) return adapters[forced];

  // Otherwise map a property's county to its adapter.
  if (county) {
    const key = 'fl-' + String(county).toLowerCase().replace(/\s+county$/, '').replace(/\s+/g, '-');
    if (adapters[key]) return adapters[key];
  }
  return mock;
}

module.exports = { getAdapter, adapters };
