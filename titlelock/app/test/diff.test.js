// Runs with: node --test app/test/
const test = require('node:test');
const assert = require('node:assert');
const { detectChanges } = require('../lib/diff');
const mock = require('../lib/counties/mock');

test('no change when current matches baseline', async () => {
  const baseline = await mock.fetchRecordings({ address: '123 Harbor View Dr' });
  const current = await mock.fetchRecordings({ address: '123 Harbor View Dr' });
  const r = detectChanges(baseline, current);
  assert.equal(r.changed, false);
  assert.equal(r.alerts.length, 0);
});

test('detects a new forged deed as critical', async () => {
  const baseline = await mock.fetchRecordings({ address: '123 Harbor View Dr' });
  const current = await mock.fetchRecordings({ address: '123 Harbor View Dr FRAUD' });
  const r = detectChanges(baseline, current);
  assert.equal(r.changed, true);
  assert.equal(r.alerts.length, 1);
  assert.equal(r.alerts[0].severity, 'critical');
  assert.equal(r.alerts[0].kind, 'deed');
  assert.match(r.alerts[0].summary, /new deed/i);
});

test('empty baseline flags everything as new', () => {
  const current = [{ id: 'X-1', type: 'mortgage', recordedAt: '2025-01-01', grantee: 'Bank' }];
  const r = detectChanges([], current);
  assert.equal(r.changed, true);
  assert.equal(r.alerts[0].severity, 'warning');
});
