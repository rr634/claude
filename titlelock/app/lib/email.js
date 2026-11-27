// Transactional email via Resend. No-ops safely (logs) when RESEND_API_KEY is absent,
// so local/dev and preview deploys don't crash.
const { Resend } = require('resend');

async function sendEmail({ to, subject, html }) {
  const key = process.env.RESEND_API_KEY;
  const from = process.env.ALERT_FROM || 'DeedGuard USA <alerts@deedguard.us>';
  if (!key) {
    console.log('[email] RESEND_API_KEY missing — would send:', { to, subject });
    return { skipped: true };
  }
  const resend = new Resend(key);
  return resend.emails.send({ from, to, subject, html });
}

function escapeHtml(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

module.exports = { sendEmail, escapeHtml };
