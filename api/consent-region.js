const CONSENT_COUNTRIES = new Set([
  "AT",
  "BE",
  "BG",
  "CH",
  "CY",
  "CZ",
  "DE",
  "DK",
  "EE",
  "ES",
  "FI",
  "FR",
  "GB",
  "GR",
  "HR",
  "HU",
  "IE",
  "IS",
  "IT",
  "LI",
  "LT",
  "LU",
  "LV",
  "MT",
  "NL",
  "NO",
  "PL",
  "PT",
  "RO",
  "SE",
  "SI",
  "SK",
]);

module.exports = function consentRegion(request, response) {
  const country = String(request.headers["x-vercel-ip-country"] || "").toUpperCase();

  response.setHeader("Cache-Control", "private, no-store, max-age=0");
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.status(200).json({
    country,
    requiresConsent: country ? CONSENT_COUNTRIES.has(country) : true,
  });
};

module.exports.CONSENT_COUNTRIES = CONSENT_COUNTRIES;
