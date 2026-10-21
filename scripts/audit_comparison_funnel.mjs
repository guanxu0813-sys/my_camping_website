#!/usr/bin/env node
/** Validate every guide-to-comparison deep link against the generated catalog. */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const base = "https://www.campgearcompare.com";
const categoryPaths = {
  tent: "/tent.html",
  tarp: "/tarp.html",
  "sleeping-bag": "/sleeping-bag.html",
  "sleeping-pad": "/sleeping-pad.html",
  stove: "/stove.html",
};

function fail(message) {
  throw new Error(message);
}

const catalogDom = new JSDOM("", { runScripts: "outside-only" });
catalogDom.window.eval(
  fs.readFileSync(path.join(root, "data", "catalog.js"), "utf8")
);
const products = catalogDom.window.CAMPGEAR_DATA?.products || [];
const productById = new Map(products.map((product) => [product.id, product]));

const guideDir = path.join(root, "guides");
const guideFiles = fs
  .readdirSync(guideDir)
  .filter((name) => name.endsWith(".html") && name !== "index.html")
  .sort();

let auditedLinks = 0;
const categoryFiles = new Set();

for (const guideFile of guideFiles) {
  const html = fs.readFileSync(path.join(guideDir, guideFile), "utf8");
  const dom = new JSDOM(html, { url: `${base}/guides/${guideFile}` });
  const links = Array.from(
    dom.window.document.querySelectorAll("a.guide-compare-link")
  );

  for (const link of links) {
    auditedLinks += 1;
    const target = new URL(link.href, base);
    const ids = (target.searchParams.get("compare") || "")
      .split(",")
      .map((id) => id.trim())
      .filter(Boolean);
    const declaredCount = Number(link.dataset.compareCount);

    if (target.origin !== base) fail(`${guideFile}: comparison link is not internal`);
    if (target.searchParams.get("source") !== "guide") {
      fail(`${guideFile}: comparison link is missing source=guide`);
    }
    if (ids.length < 2 || ids.length > 16) {
      fail(`${guideFile}: comparison link has ${ids.length} products`);
    }
    if (new Set(ids).size !== ids.length) {
      fail(`${guideFile}: comparison link contains duplicate product IDs`);
    }
    if (declaredCount !== ids.length) {
      fail(`${guideFile}: data-compare-count does not match the URL`);
    }

    for (const id of ids) {
      const product = productById.get(id);
      if (!product) fail(`${guideFile}: unknown product ID ${id}`);
      if (categoryPaths[product.category] !== target.pathname) {
        fail(`${guideFile}: ${id} does not belong on ${target.pathname}`);
      }
    }
    categoryFiles.add(target.pathname.slice(1));
  }
}

if (!auditedLinks) fail("No guide comparison links found");

for (const categoryFile of categoryFiles) {
  const html = fs.readFileSync(path.join(root, categoryFile), "utf8");
  const dom = new JSDOM(html);
  const viewport = dom.window.document.querySelector('meta[name="viewport"]');
  if (!viewport?.content.includes("width=device-width")) {
    fail(`${categoryFile}: missing responsive viewport metadata`);
  }
  if (!dom.window.document.getElementById("compare-root")) {
    fail(`${categoryFile}: missing comparison root`);
  }
  if (!dom.window.document.getElementById("product-modal")) {
    fail(`${categoryFile}: missing product modal`);
  }
}

const css = fs.readFileSync(path.join(root, "style.css"), "utf8");
const mobileTrayRule = /@media\s*\(max-width:\s*720px\)[\s\S]*?\.compare-tray\s*\{[\s\S]*?bottom:\s*[^;]+;[\s\S]*?max-width:\s*calc\(100vw/;
const mobileModalRule = /@media\s*\(max-width:\s*720px\)[\s\S]*?\.product-modal__panel\s*\{[\s\S]*?grid-template-columns:\s*1fr/;
if (!mobileTrayRule.test(css)) fail("Missing mobile compare tray layout rule");
if (!mobileModalRule.test(css)) fail("Missing mobile product modal layout rule");

console.log(
  `Comparison funnel audit passed: ${auditedLinks} guide links across ${categoryFiles.size} category pages.`
);
