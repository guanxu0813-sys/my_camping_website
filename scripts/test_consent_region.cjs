const assert = require("node:assert/strict");
const handler = require("../api/consent-region");

function request(country) {
  let statusCode = 0;
  let payload = null;
  const headers = {};
  const response = {
    setHeader(name, value) {
      headers[name.toLowerCase()] = value;
    },
    status(code) {
      statusCode = code;
      return this;
    },
    json(value) {
      payload = value;
      return this;
    },
  };

  handler(
    { headers: country ? { "x-vercel-ip-country": country } : {} },
    response
  );
  return { statusCode, payload, headers };
}

assert.equal(request("DE").payload.requiresConsent, true);
assert.equal(request("GB").payload.requiresConsent, true);
assert.equal(request("CH").payload.requiresConsent, true);
assert.equal(request("US").payload.requiresConsent, false);
assert.equal(request("CN").payload.requiresConsent, false);
assert.equal(request("").payload.requiresConsent, true);
assert.equal(request("US").statusCode, 200);
assert.equal(request("US").headers["cache-control"], "private, no-store, max-age=0");

console.log("Consent region verification passed.");
