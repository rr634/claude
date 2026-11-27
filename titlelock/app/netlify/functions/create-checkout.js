// POST /.netlify/functions/create-checkout  — starts a Stripe subscription Checkout.
// Body: { plan: "essential" | "defend" | "premier" }  -> { url } to redirect the buyer to.
//
// "defend" (the Guardian plan) uses INTRO pricing: it checks out at the founding monthly price,
// and the webhook converts the new subscription into a schedule that steps up to the standard
// price after `introMonths`. Essential/Premier are flat.
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

  // Plan -> Stripe prices. "defend" (Guardian) carries an intro price + a standard renewal price.
  const PLANS = {
    essential: { price: process.env.STRIPE_PRICE_ESSENTIAL },
    defend: { price: process.env.STRIPE_PRICE_DEFEND_INTRO, standard: process.env.STRIPE_PRICE_DEFEND, introMonths: 12 },
    premier: { price: process.env.STRIPE_PRICE_PREMIER },
  };
  const cfg = PLANS[plan];
  if (!cfg || !cfg.price) return resp(400, { error: 'Unknown or unconfigured plan' });

  const site = process.env.SITE_URL || `https://${event.headers.host || 'deedguardusa.com'}`;

  // Pass intro details through metadata so the webhook can build the step-up schedule.
  const meta = { plan };
  if (cfg.standard) {
    meta.intro_price = cfg.price;
    meta.standard_price = cfg.standard;
    meta.intro_months = String(cfg.introMonths || 12);
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: cfg.price, quantity: 1 }],
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
      success_url: `${site}/?welcome=1`,
      cancel_url: `${site}/#pricing`,
      metadata: meta,
      subscription_data: { metadata: meta },
    });
    return resp(200, { url: session.url });
  } catch (e) {
    console.error('[create-checkout] failed:', e.message);
    return resp(500, { error: 'Could not start checkout.' });
  }
};
