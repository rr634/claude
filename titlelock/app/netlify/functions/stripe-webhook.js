// POST /.netlify/functions/stripe-webhook  — syncs Stripe -> subscribers table.
// Configure this URL in Stripe (Developers -> Webhooks) and set STRIPE_WEBHOOK_SECRET.
// Requires the RAW body for signature verification (Netlify provides it as event.body).
const Stripe = require('stripe');
const { db } = require('../../lib/db');
const { resp } = require('../../lib/http');

exports.handler = async (event) => {
  const key = process.env.STRIPE_SECRET_KEY;
  const whsec = process.env.STRIPE_WEBHOOK_SECRET;
  if (!key || !whsec) return resp(500, { error: 'Stripe not configured' });
  const stripe = Stripe(key);

  let evt;
  try {
    const sig = event.headers['stripe-signature'];
    const raw = event.isBase64Encoded ? Buffer.from(event.body, 'base64') : event.body;
    evt = stripe.webhooks.constructEvent(raw, sig, whsec);
  } catch (e) {
    return resp(400, `Webhook signature verification failed: ${e.message}`);
  }

  try {
    if (evt.type === 'checkout.session.completed') {
      const s = evt.data.object;
      await db().from('subscribers').upsert(
        {
          email: s.customer_details?.email || s.customer_email,
          stripe_customer_id: s.customer,
          stripe_subscription_id: s.subscription,
          plan: s.metadata?.plan || null,
          status: 'active',
        },
        { onConflict: 'email' }
      );

      // Founding-rate step-up: if this plan has intro pricing, convert the subscription into a
      // schedule — phase 1 at the intro price for intro_months, then the standard price forever.
      if (s.subscription && s.metadata?.standard_price && s.metadata?.intro_price) {
        try {
          const schedule = await stripe.subscriptionSchedules.create({ from_subscription: s.subscription });
          const introMonths = parseInt(s.metadata.intro_months || '12', 10);
          await stripe.subscriptionSchedules.update(schedule.id, {
            end_behavior: 'release',
            phases: [
              { items: [{ price: s.metadata.intro_price, quantity: 1 }], iterations: introMonths },
              { items: [{ price: s.metadata.standard_price, quantity: 1 }] },
            ],
          });
        } catch (e) {
          console.error('[stripe-webhook] intro->standard schedule setup failed:', e.message);
        }
      }

      // NOTE: create the property row(s) here once the signup collects the address
      // (e.g. from a Checkout custom field or a short post-purchase onboarding form).
    } else if (evt.type === 'customer.subscription.updated' || evt.type === 'customer.subscription.deleted') {
      const sub = evt.data.object;
      await db().from('subscribers').update({ status: sub.status }).eq('stripe_subscription_id', sub.id);
    }
  } catch (e) {
    console.error('[stripe-webhook] handler error:', e.message);
    // Return 200 so Stripe doesn't retry forever on a transient DB issue; we log for replay.
  }

  return resp(200, { received: true });
};
