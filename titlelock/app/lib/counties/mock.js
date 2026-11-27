// Deterministic mock county adapter — lets the whole pipeline run with zero external deps.
// Returns a stable baseline for any property, and injects a fake fraudulent deed when the
// address contains "FRAUD" (handy for demos and tests).

async function fetchRecordings({ address } = {}) {
  const records = [
    { id: 'D-1001', recordedAt: '2019-05-02', type: 'deed', grantor: 'ABC Builders LLC', grantee: 'Homeowner', bookPage: '12345/678' },
    { id: 'M-2001', recordedAt: '2019-05-02', type: 'mortgage', grantor: 'Homeowner', grantee: 'Big Bank NA', bookPage: '12345/690' },
  ];
  if (String(address || '').toUpperCase().includes('FRAUD')) {
    records.push({
      id: 'D-9999',
      recordedAt: new Date().toISOString().slice(0, 10),
      type: 'deed',
      grantor: 'Homeowner',
      grantee: 'Unknown Party LLC',
      bookPage: '99999/001',
    });
  }
  return records;
}

module.exports = { fetchRecordings };
