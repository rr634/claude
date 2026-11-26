// Supabase client (service role — server-side only, never ship this key to the browser).
const { createClient } = require('@supabase/supabase-js');

let client;
function db() {
  if (!client) {
    const url = process.env.SUPABASE_URL;
    const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
    if (!url || !key) throw new Error('Supabase env (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY) not configured');
    client = createClient(url, key, { auth: { persistSession: false } });
  }
  return client;
}
module.exports = { db };
