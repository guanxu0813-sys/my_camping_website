#!/usr/bin/env node
/**
 * Headless sponsor placement smoke test.
 * Loads tent.html + catalog.js + script.js in jsdom and checks badge + pin + modal.
 */
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const port = process.argv[2] || "8765";
const base = `http://127.0.0.1:${port}`;
const EXPECTED_PRODUCT_ID = "snow-peak-amenity-dome-m-ivory";

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.text();
}

async function waitFor(fn, { tries = 40, delayMs = 250, label = "condition" }) {
  for (let i = 0; i < tries; i++) {
    if (fn()) return;
    await new Promise((r) => setTimeout(r, delayMs));
  }
  throw new Error(`Timed out waiting for ${label}`);
}

async function main() {
  const sponsorsRaw = await fetchText(`${base}/data/sponsors.json`);
  const sponsors = JSON.parse(sponsorsRaw);
  const campaign = sponsors.campaigns?.find((c) => c.productId === EXPECTED_PRODUCT_ID);
  if (!campaign) {
    throw new Error(`Missing campaign for ${EXPECTED_PRODUCT_ID} in sponsors.json`);
  }
  if (campaign.active !== true) {
    throw new Error(`sponsors.json has active=${campaign.active}; expected true for demo verification`);
  }

  const tentHtml = await fetchText(`${base}/tent.html`);
  const dom = new JSDOM(tentHtml, {
    url: `${base}/tent.html`,
    runScripts: "outside-only",
    resources: "usable",
    pretendToBeVisual: true,
  });

  const { window } = dom;
  if (!window.fetch) window.fetch = (...args) => fetch(...args);

  const origFetch = window.fetch.bind(window);
  window.fetch = async (input) => {
    const url = String(input);
    if (url.includes("data/sponsors.json")) {
      return origFetch(`${base}/data/sponsors.json`);
    }
    if (url.includes("data/analytics.json")) {
      return origFetch(`${base}/data/analytics.json`);
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

  window.eval(await fetchText(`${base}/data/catalog.js`));
  window.eval(await fetchText(`${base}/script.js`));

  await waitFor(
    () => window.document.querySelector(".compare-table tbody tr.compare-table__row--sponsored"),
    { label: "sponsored table row" }
  );

  const firstRow = window.document.querySelector(".compare-table tbody tr");
  if (!firstRow?.classList.contains("compare-table__row--sponsored")) {
    throw new Error("Sponsored product is not pinned to the first compare-table row");
  }

  const badge = firstRow.querySelector(".sponsor-badge");
  if (!badge || !/sponsored/i.test(badge.textContent || "")) {
    throw new Error("First row missing .sponsor-badge with Sponsored label");
  }

  const modelCell = firstRow.querySelector(".compare-table__model");
  if (!modelCell || !/Amenity Dome Medium in Ivory/i.test(modelCell.textContent || "")) {
    throw new Error(`First row model mismatch: ${modelCell?.textContent || "(empty)"}`);
  }

  const thumbBtn = firstRow.querySelector(".compare-table__thumb-btn");
  if (!thumbBtn || thumbBtn.getAttribute("data-product-id") !== EXPECTED_PRODUCT_ID) {
    throw new Error("First row thumb button does not match sponsored product id");
  }

  thumbBtn.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
  await new Promise((r) => setTimeout(r, 150));

  const modal = window.document.getElementById("product-modal");
  if (!modal || modal.hidden) {
    throw new Error("Product modal did not open for sponsored product");
  }

  const modalSponsor = window.document.getElementById("product-modal-sponsor");
  if (!modalSponsor || modalSponsor.hidden) {
    throw new Error("Modal sponsor strip is hidden");
  }
  if (!modalSponsor.querySelector(".sponsor-badge")) {
    throw new Error("Modal sponsor strip missing badge");
  }
  if (!/Paid placement/i.test(modalSponsor.textContent || "")) {
    throw new Error("Modal sponsor strip missing disclosure note");
  }

  console.log("Sponsor verification passed (jsdom smoke test).");
  console.log("  sponsors.json active:", campaign.active);
  console.log("  pinned model:", modelCell.textContent.trim());
  console.log("  table badge:", badge.textContent.trim());
  console.log("  modal sponsor:", modalSponsor.textContent.replace(/\s+/g, " ").trim());
}

main().catch((err) => {
  console.error("Sponsor verification failed:", err.message);
  process.exit(1);
});
