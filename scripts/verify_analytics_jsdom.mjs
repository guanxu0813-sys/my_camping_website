#!/usr/bin/env node
/**
 * Headless analytics smoke test (no browser download required).
 * Loads tent.html + catalog.js + script.js in jsdom and simulates modal/outbound clicks.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const base = "http://127.0.0.1";

const analyticsLogs = [];

async function fetchText(url) {
  const pathname = new URL(url, base).pathname;
  return fs.readFileSync(path.join(root, pathname.replace(/^\//, "")), "utf8");
}

async function main() {
  const tentHtml = await fetchText(`${base}/tent.html`);
  const dom = new JSDOM(tentHtml, {
    url: `${base}/tent.html`,
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });

  const { window } = dom;
  window.CAMPGEAR_TEST_MODE = true;

  window.console.info = (...args) => {
    const text = args.map(String).join(" ");
    if (text.includes("[CampGear analytics]")) analyticsLogs.push(text);
  };

  // Resolve site data from disk so this smoke test does not require a network port.
  window.fetch = async (input) => {
    const url = String(input);
    if (url.includes("/api/consent-region")) {
      return {
        ok: true,
        json: async () => ({ country: "DE", requiresConsent: true }),
      };
    }
    try {
      const pathname = new URL(url, base).pathname;
      const filePath = path.join(root, pathname.replace(/^\//, ""));
      const body = fs.readFileSync(filePath, "utf8");
      return {
        ok: true,
        status: 200,
        json: async () => JSON.parse(body),
        text: async () => body,
      };
    } catch (error) {
      return {
        ok: false,
        status: 404,
        json: async () => ({}),
        text: async () => "",
      };
    }
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

  const compareInputs = window.document.querySelectorAll(".compare-select__input");
  if (compareInputs.length < 2) {
    throw new Error("Not enough compare inputs rendered");
  }
  for (const input of Array.from(compareInputs).slice(0, 2)) {
    input.checked = true;
    input.dispatchEvent(new window.Event("change", { bubbles: true }));
  }
  if (!analyticsLogs.some((l) => l.includes("Compare Item Toggle"))) {
    throw new Error("Missing Compare Item Toggle event");
  }
  const compareButton = window.document.getElementById("compare-tray-action");
  compareButton.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  if (!analyticsLogs.some((l) => l.includes("Compare Selected"))) {
    throw new Error("Missing Compare Selected event");
  }

  const newsletterForm = window.document.querySelector("[data-newsletter-form]");
  const newsletterEmail = window.document.getElementById("newsletter-email");
  if (!newsletterForm || !newsletterEmail) {
    throw new Error("Newsletter signup entry not rendered");
  }
  newsletterEmail.value = "reader@example.com";
  newsletterForm.dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));
  if (!analyticsLogs.some((l) => l.includes("Newsletter Signup Intent"))) {
    throw new Error("Missing Newsletter Signup Intent event");
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
    "compare_item_toggle",
    "compare_selected",
    "newsletter_signup_intent",
  ]) {
    if (!ga4Events.includes(expected)) {
      throw new Error(`Missing GA4 event: ${expected}`);
    }
  }

  console.log("Analytics verification passed (jsdom smoke test).");
  analyticsLogs.forEach((l) => console.log(" ", l));

  const firstTwoIds = [
    "big-agnes-tiger-wall-ul-two",
    "big-agnes-copper-spur-ul-two",
  ];
  const deepLinkDom = new JSDOM(tentHtml, {
    url: `${base}/tent.html?compare=${firstTwoIds.join(",")}&source=guide`,
    runScripts: "outside-only",
    pretendToBeVisual: true,
  });
  deepLinkDom.window.CAMPGEAR_TEST_MODE = true;
  deepLinkDom.window.localStorage.setItem("campgear_analytics_consent", "granted");
  deepLinkDom.window.fetch = window.fetch;
  deepLinkDom.window.HTMLElement.prototype.scrollIntoView = () => {};
  deepLinkDom.window.eval(catalogJs);
  deepLinkDom.window.eval(scriptJs);
  for (let i = 0; i < 40; i++) {
    await new Promise((r) => setTimeout(r, 100));
    const selected = deepLinkDom.window.document.querySelectorAll(
      ".compare-select__input:checked"
    );
    if (selected.length >= 2) break;
  }
  const deepLinkSelected = deepLinkDom.window.document.querySelectorAll(
    ".compare-select__input:checked"
  );
  if (deepLinkSelected.length !== 2) {
    throw new Error("Guide compare deep link did not select two products");
  }
  const visibleRows = Array.from(
    deepLinkDom.window.document.querySelectorAll("tr[data-product-id]")
  ).filter((row) => !row.classList.contains("is-filtered-out"));
  if (!visibleRows.length || visibleRows.some((row) => !firstTwoIds.includes(row.dataset.productId))) {
    throw new Error("Guide compare deep link did not filter to requested products");
  }
  console.log("Guide compare deep-link verification passed.");
}

main().catch((err) => {
  console.error("Analytics verification failed:", err.message);
  if (analyticsLogs.length) {
    console.error("Captured logs:");
    analyticsLogs.forEach((l) => console.error(" ", l));
  }
  process.exit(1);
});
