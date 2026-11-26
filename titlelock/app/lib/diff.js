// Change detection — the core of the monitoring product.
// Compares a fresh pull of public recordings against a property's stored baseline
// and produces risk-scored alerts for anything new.

const SEVERITY_BY_TYPE = {
  deed: 'critical',       // a new deed = possible title transfer = highest risk
  mortgage: 'warning',    // new loan against the property
  lien: 'warning',
  judgment: 'warning',
};

function summarize(r) {
  const t = r.type || 'record';
  const label = {
    deed: 'A new deed',
    mortgage: 'A new mortgage',
    lien: 'A new lien',
    judgment: 'A new judgment',
  }[t] || 'A new recording';
  const who = r.grantee ? ` naming ${r.grantee}` : '';
  const when = r.recordedAt ? ` on ${r.recordedAt}` : '';
  return `${label}${who} was recorded against your property${when}.`;
}

// baseline / current: arrays of { id, recordedAt, type, grantor, grantee, bookPage, raw }
function detectChanges(baseline, current) {
  const baseIds = new Set((baseline || []).map((r) => r.id));
  const added = (current || []).filter((r) => r && r.id && !baseIds.has(r.id));
  const alerts = added.map((r) => ({
    severity: SEVERITY_BY_TYPE[r.type] || 'info',
    kind: r.type || 'other',
    summary: summarize(r),
    record: r,
  }));
  return { added, alerts, changed: added.length > 0 };
}

module.exports = { detectChanges, summarize };
