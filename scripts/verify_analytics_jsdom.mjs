#!/usr/bin/env node
/**
 * Headless analytics smoke test (no browser download required).
 * Loads tent.html + catalog.js + script.js in jsdom and simulates modal/outbound clicks.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { JSDOM } from "jsdom";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const port = process.argv[2] || "8765";
const base = `http://127.0.0.1:${port}`;

const analyticsLogs = [];

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

async function main() {
  const tentHtml = await fetchText(`${base}/tent.html`);
  const dom = new JSDOM(tentHtml, {
    url: `${base}/tent.html`,
    runScripts: "outside-only",
    resources: "usable",
    pretendToBeVisual: true,
  });

  const { window } = dom;

  if (!window.fetch) {
    window.fetch = (...args) => fetch(...args);
  }

  window.console.info = (...args) => {
    const text = args.map(String).join(" ");
    if (text.includes("[CampGear analytics]")) analyticsLogs.push(text);
  };

  // Stub fetch for data files used by script.js
  const origFetch = window.fetch.bind(window);
  window.fetch = async (input) => {
    const url = String(input);
    if (url.includes("data/analytics.json")) {
      return origFetch(`${base}/data/analytics.json`);
    }
    if (url.includes("/api/consent-region")) {
      return {
        ok: true,
        json: async () => ({ country: "DE", requiresConsent: true }),
      };
    }
    if (url.includes("data/brands.json")) {
      return origFetch(`${base}/data/brands.json`);
    }
    if (url.includes("data/official/index.json")) {
      return origFetch(`${base}/data/official/index.json`);
    }
    if (url.includes("data/official/") && url.endsWith("/products.json")) {
      return origFetch(url.replace(/^https?:\/\/[^/]+/, base));
    }
    if (url.includes("data/site.json")) {
      return origFetch(`${base}/data/site.json`);
    }
    return origFetch(input);
  };

  // Load catalog bundle then app script (same order as tent.html)
  const catalogJs = await fetchText(`${base}/data/catalog.js`);
  window.eval(catalogJs);
  const scriptJs = await fetchText(`${base}/script.js`);
  window.eval(scriptJs);

  let consentBanner = null;
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 50));
    consentBanner = window.document.querySelector(".cookie-consent");
    if (consentBanner) break;
  }
  if (!consentBanner) {
    throw new Error("European analytics consent banner not shown");
  }
  if (typeof window.gtag === "function") {
    throw new Error("GA4 initialized before analytics consent");
  }
  consentBanner
    .querySelector('[data-analytics-consent="granted"]')
    .dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  if (window.localStorage.getItem("campgear_analytics_consent") !== "granted") {
    throw new Error("Analytics consent choice not persisted");
  }

  let thumb = null;
  for (let i = 0; i < 40; i++) {
    await new Promise((r) => setTimeout(r, 250));
    thumb = window.document.querySelector(".compare-table__thumb-btn");
    if (thumb) break;
  }

  if (!thumb) {
    throw new Error("Compare table thumb button not rendered");
  }

  thumb.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 100));

  const modal = window.document.getElementById("product-modal");
  if (!modal || modal.hidden) {
    throw new Error("Product modal did not open");
  }

  const modalOpen = analyticsLogs.some((l) => l.includes("Product Modal Open"));
  if (!modalOpen) {
    throw new Error("Missing Product Modal Open event");
  }

  const outboundLink = window.document.querySelector(
    "#product-modal-source a.outbound-link, #product-modal-source a.purchase-link"
  );
  if (!outboundLink || !outboundLink.href || outboundLink.href === "#") {
    throw new Error("Modal outbound link not set");
  }

  outboundLink.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));

  const outbound = analyticsLogs.some((l) => l.includes("Outbound Click"));
  if (!outbound) {
    throw new Error("Missing Outbound Click event");
  }

  const searchInput = window.document.getElementById("catalog-search-input");
  searchInput.value = "naturehike";
  searchInput.dispatchEvent(new window.Event("input", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 900));
  if (!analyticsLogs.some((l) => l.includes("Catalog Search"))) {
    throw new Error("Missing Catalog Search event");
  }

  const brandChip = window.document.querySelector(
    '[data-brand-filter]:not([data-brand-filter="all"])'
  );
  brandChip.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  if (!analyticsLogs.some((l) => l.includes("Brand Filter"))) {
    throw new Error("Missing Brand Filter event");
  }

  const sortButton = window.document.querySelector(".compare-table__sort-btn");
  sortButton.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  if (!analyticsLogs.some((l) => l.includes("Table Sort"))) {
    throw new Error("Missing Table Sort event");
  }

  const ga4Events = (window.dataLayer || [])
    .map((entry) => Array.from(entry))
    .filter((entry) => entry[0] === "event")
    .map((entry) => entry[1]);
  for (const expected of [
    "product_modal_open",
    "outbound_click",
    "catalog_search",
    "brand_filter",
    "table_sort",
  ]) {
    if (!ga4Events.includes(expected)) {
      throw new Error(`Missing GA4 event: ${expected}`);
    }
  }

  console.log("Analytics verification passed (jsdom smoke test).");
  analyticsLogs.forEach((l) => console.log(" ", l));
}

main().catch((err) => {
  console.error("Analytics verification failed:", err.message);
  if (analyticsLogs.length) {
    console.error("Captured logs:");
    analyticsLogs.forEach((l) => console.error(" ", l));
  }
  process.exit(1);
});
