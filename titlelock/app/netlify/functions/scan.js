// Scheduled scanner — the heart of the product.
// Runs daily, pulls each watched property's current public recordings, diffs against its
// baseline, records the scan, raises alerts, and emails the subscriber on any change.
const { schedule } = require('@netlify/functions');
const { db } = require('../../lib/db');
const { getAdapter } = require('../../lib/counties');
const { detectChanges } = require('../../lib/diff');
const { sendEmail, escapeHtml } = require('../../lib/email');

function alertHtml(prop, alerts) {
  const items = alerts
    .map((a) => `<li><b>${escapeHtml(a.severity.toUpperCase())}:</b> ${escapeHtml(a.summary)}</li>`)
    .join('');
  return `<h2>New activity on ${escapeHtml(prop.address)}</h2>
          <p>DeedGuard detected the following new filing(s) on your property:</p>
          <ul>${items}</ul>
          <p>If you did not authorize this, reply to this email — a Florida real estate attorney will help you review it.</p>
          <p style="color:#5B6B7C;font-size:12px">DeedGuard USA · Always Watching. Always Protected.</p>`;
}

const run = async () => {
  let properties = [];
  try {
    const { data, error } = await db().from('properties').select('*').limit(1000);
    if (error) throw error;
    properties = data || [];
  } catch (e) {
    console.error('[scan] could not read properties:', e.message);
    return { statusCode: 500, body: 'db read failed' };
  }

  let scanned = 0, changed = 0;
  for (const prop of properties) {
    try {
      const adapter = getAdapter(prop.county);
      const current = await adapter.fetchRecordings(prop);
      const result = detectChanges(prop.baseline, current);
      scanned++;

      await db().from('scans').insert({ property_id: prop.id, records: current, changed: result.changed });
      await db().from('properties').update({ last_scanned_at: new Date().toISOString() }).eq('id', prop.id);

      if (result.changed) {
        changed++;
        for (const a of result.alerts) {
          await db().from('alerts').insert({ property_id: prop.id, severity: a.severity, kind: a.kind, summary: a.summary, record: a.record, notified: true });
        }
        const sub = (await db().from('subscribers').select('email').eq('id', prop.subscriber_id).single()).data;
        if (sub?.email) {
          await sendEmail({ to: sub.email, subject: `⚠️ New filing on ${prop.address}`, html: alertHtml(prop, result.alerts) });
        }
      }
    } catch (e) {
      console.error('[scan] error on property', prop.id, e.message);
    }
  }
  console.log(`[scan] done — scanned ${scanned}, changed ${changed}`);
  return { statusCode: 200, body: `scanned ${scanned}, changed ${changed}` };
};

// Daily at 11:00 UTC. Tighten/loosen as needed (the product promises "every few days").
exports.handler = schedule('0 11 * * *', run);
