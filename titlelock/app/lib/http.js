// Small HTTP helpers for Netlify Functions.
function resp(statusCode, body) {
  const isObj = body && typeof body === 'object';
  return {
    statusCode,
    headers: {
      'Content-Type': isObj ? 'application/json' : 'text/plain',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    },
    body: isObj ? JSON.stringify(body) : String(body),
  };
}
function preflight(event) {
  return event.httpMethod === 'OPTIONS' ? resp(204, '') : null;
}
module.exports = { resp, preflight };
