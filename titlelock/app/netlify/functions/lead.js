// POST /.netlify/functions/lead  — free property-check lead capture.
// Stores the lead (best-effort) and emails the operator. Never blocks the user on infra errors.
const { db } = require('../../lib/db');
const { sendEmail, escapeHtml } = require('../../lib/email');
const { resp, preflight } = require('../../lib/http');

exports.handler = async (event) => {
  const pf = preflight(event);
  if (pf) return pf;
  if (event.httpMethod !== 'POST') return resp(405, { error: 'Method not allowed' });

  let body;
  try { body = JSON.parse(event.body || '{}'); } catch { return resp(400, { error: 'Bad JSON' }); }
  const email = String(body.email || '').trim();
  const address = String(body.address || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !address) {
    return resp(400, { error: 'A valid email and property address are required.' });
  }

  // Store the lead (don't fail the request if the DB isn't configured yet).
  try {
    await db().from('leads').insert({ email, address, source: 'free-check' });
  } catch (e) {
    console.error('[lead] insert failed:', e.message);
  }

  // Notify the operator.
  try {
    await sendEmail({
      to: process.env.OPERATOR_EMAIL || 'rr@richardrosalaw.com',
      subject: `New DeedGuard free-check: ${address}`,
      html: `<p>New free title-check request.</p>
             <p><b>Address:</b> ${escapeHtml(address)}<br>
                <b>Email:</b> ${escapeHtml(email)}</p>`,
    });
  } catch (e) {
    console.error('[lead] email failed:', e.message);
  }

  return resp(200, { ok: true });
};
