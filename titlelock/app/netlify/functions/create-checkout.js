// POST /.netlify/functions/create-checkout  — starts a Stripe subscription Checkout.
// Body: { plan: "essential" | "defend" | "premier" }  -> { url } to redirect the buyer to.
const Stripe = require('stripe');
const { resp, preflight } = require('../../lib/http');

exports.handler = async (event) => {
  const pf = preflight(event);
  if (pf) return pf;
  if (event.httpMethod !== 'POST') return resp(405, { error: 'Method not allowed' });

  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return resp(500, { error: 'Payments are not configured yet.' });
  const stripe = Stripe(key);

  let body;
  try { body = JSON.parse(event.body || '{}'); } catch { return resp(400, { error: 'Bad JSON' }); }
  const plan = String(body.plan || '').toLowerCase();

  const priceByPlan = {
    essential: process.env.STRIPE_PRICE_ESSENTIAL,
    defend: process.env.STRIPE_PRICE_DEFEND,
    premier: process.env.STRIPE_PRICE_PREMIER,
  };
  const price = priceByPlan[plan];
  if (!price) return resp(400, { error: 'Unknown plan' });

  const site = process.env.SITE_URL || `https://${event.headers.host || 'deedguardusa.com'}`;

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price, quantity: 1 }],
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
      success_url: `${site}/?welcome=1`,
      cancel_url: `${site}/#pricing`,
      metadata: { plan },
      subscription_data: { metadata: { plan } },
    });
    return resp(200, { url: session.url });
  } catch (e) {
    console.error('[create-checkout] failed:', e.message);
    return resp(500, { error: 'Could not start checkout.' });
  }
};
