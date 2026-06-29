(function () {
  var header = document.querySelector(".site-header");
  var navHeight = header ? header.offsetHeight : 68;
  var brandFilter = "all";
  var searchQuery = "";
  var catalogLoaded = false;
  var catalogLoadPromise = null;
  var navSearchBound = false;
  var categoryFiltersBound = false;
  var brands = [];
  var products = [];
  var brandMap = {};
  var CATEGORY_PAGES = {
    tent: "tent.html",
    tarp: "tarp.html",
    "sleeping-bag": "sleeping-bag.html",
    table: "furniture.html",
    chair: "furniture.html",
  };
  var tableSort = {
    tent: { key: null, dir: "asc" },
    tarp: { key: null, dir: "asc" },
    "sleeping-bag": { key: null, dir: "asc" },
  };
  var tableSortBound = false;
  var furnitureModalBound = false;
  var furnitureMatrixBound = false;
  var outboundTrackingBound = false;
  var lastModalFocus = null;
  var analyticsConfig = null;

  function isLocalDevHost() {
    var host = window.location.hostname;
    return host === "localhost" || host === "127.0.0.1";
  }

  function loadBaiduPush() {
    if (window.location.protocol === "file:" || isLocalDevHost()) {
      return;
    }
    var bp = document.createElement("script");
    bp.src =
      window.location.protocol === "https:"
        ? "https://zz.bdstatic.com/linksubmit/push.js"
        : "http://push.zhanzhang.baidu.com/push.js";
    var first = document.getElementsByTagName("script")[0];
    if (first && first.parentNode) {
      first.parentNode.insertBefore(bp, first);
    } else {
      document.head.appendChild(bp);
    }
  }

  function loadAnalytics() {
    if (window.location.protocol === "file:") {
      return Promise.resolve(null);
    }
    return fetch("data/analytics.json")
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .then(function (cfg) {
        analyticsConfig = cfg;
        if (cfg && cfg.enabled && cfg.plausibleDomain) {
          if (!document.querySelector('script[src="https://plausible.io/js/script.js"]')) {
            var s = document.createElement("script");
            s.defer = true;
            s.dataset.domain = cfg.plausibleDomain;
            s.src = "https://plausible.io/js/script.js";
            document.head.appendChild(s);
          }
        }
        return cfg;
      })
      .catch(function () {
        return null;
      });
  }

  function trackEvent(name, props) {
    var payload = props || {};
    if (typeof window.plausible === "function") {
      window.plausible(name, { props: payload });
    }
    if (
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1" ||
      !analyticsConfig ||
      !analyticsConfig.enabled
    ) {
      console.info("[CampGear analytics]", name, payload);
    }
  }

  function bindOutboundTracking() {
    if (outboundTrackingBound) return;
    outboundTrackingBound = true;
    document.addEventListener("click", function (e) {
      var link = e.target.closest(
        "a.purchase-link, a.sponsor-link, a.outbound-link, #product-modal-link"
      );
      if (!link || !link.href || link.href === "#" || link.href.indexOf("javascript:") === 0) {
        return;
      }
      trackEvent("Outbound Click", {
        productId: link.getAttribute("data-product-id") || "",
        platform: link.getAttribute("data-platform") || "official",
        href: link.href,
        page: document.body.getAttribute("data-page") || "unknown",
        category: document.body.getAttribute("data-category") || "",
      });
    });
  }

  function scrollToHash(hash) {
    if (!hash || hash === "#") return;
    var target = document.querySelector(hash);
    if (!target) return;
    var top = target.getBoundingClientRect().top + window.scrollY - navHeight - 8;
    window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
  }

  document.querySelectorAll('.nav__links a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var hash = link.getAttribute("href");
      if (hash && hash.length > 1 && document.querySelector(hash)) {
        e.preventDefault();
        scrollToHash(hash);
        history.pushState(null, "", hash);
      }
    });
  });

  function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatPrice(min, max, currency) {
    if (min == null && max == null) return "—";
    var suffix = currency === "USD" ? " USD" : currency === "JPY" ? " JPY" : " CNY";
    if (min != null && max != null) {
      return min.toLocaleString("en-US") + "–" + max.toLocaleString("en-US") + suffix;
    }
    return (min != null ? min : max).toLocaleString("en-US") + suffix;
  }

  function priceForProduct(p) {
    return formatPrice(p.priceMin, p.priceMax, p.currency);
  }

  var DISPLAY_TERM_MAP = [
    ["睡袋系统", "Sleeping bag system"],
    ["化纤棉", "Synthetic fill"],
    ["棉 / 化纤", "Cotton / synthetic"],
    ["羽绒", "Down"],
    ["信封式", "Envelope"],
    ["木乃伊", "Mummy"],
    ["双层帐", "Double-wall tent"],
    ["单层帐", "Single-wall tent"],
    ["双层", "Double-wall"],
    ["单层", "Single-wall"],
    ["四季", "4-season"],
    ["三季", "3-season"],
    ["露营地", "Campsite"],
    ["登山", "Mountaineering"],
    ["徒步", "Hiking"],
    ["自驾", "Car camping"],
    ["家庭", "Family"],
    ["天幕", "Tarp"],
    ["帐篷", "Tent"],
    ["睡袋", "Sleeping bag"],
  ];

  function localizeDisplayValue(value) {
    if (value == null) return value;
    var s = String(value);
    DISPLAY_TERM_MAP.forEach(function (pair) {
      s = s.split(pair[0]).join(pair[1]);
    });
    s = s.replace(/约\s+/g, "~");
    s = s.replace(/(\d[\d\-–~to]*)\s*人/g, function (_, n) {
      return n + " ppl";
    });
    s = s.replace(/人/g, "");
    s = s.replace(/元\b/g, "CNY");
    s = s.replace(/\s{2,}/g, " ").trim();
    return s;
  }

  function displayCell(value) {
    if (value == null || value === "") return "—";
    return localizeDisplayValue(value);
  }

  function formatWeight(product) {
    if (product.weightDisplay) return localizeDisplayValue(product.weightDisplay);
    if (product.weightRange) return localizeDisplayValue(product.weightRange);
    if (product.weightKg != null) return "~" + product.weightKg + " kg";
    return "—";
  }

  function formatScenarios(scenarios) {
    if (!scenarios || !scenarios.length) return "—";
    return scenarios.map(localizeDisplayValue).join(", ");
  }

  function brandName(brandId) {
    var b = brandMap[brandId];
    if (!b) return brandId;
    return b.nameEn || b.name || brandId;
  }

  function parseSponsorDate(value) {
    if (!value) return null;
    var d = new Date(value + "T23:59:59");
    return isNaN(d.getTime()) ? null : d;
  }

  function normalizeSponsor(raw) {
    if (!raw || typeof raw !== "object") return null;
    return {
      active: raw.active === true,
      tier: raw.tier || "table-featured",
      label: raw.label || "Sponsored",
      expiresAt: raw.expiresAt || null,
      campaignId: raw.campaignId || "",
    };
  }

  function isSponsorActive(sponsor) {
    if (!sponsor || !sponsor.active) return false;
    var expires = parseSponsorDate(sponsor.expiresAt);
    if (expires && expires < new Date()) return false;
    return true;
  }

  function hasTableSponsor(product) {
    if (!isSponsorActive(product.sponsor)) return false;
    var tier = product.sponsor.tier;
    return tier === "table-featured" || tier === "featured";
  }

  function hasModalSponsor(product) {
    if (!isSponsorActive(product.sponsor)) return false;
    var tier = product.sponsor.tier;
    return tier === "modal-featured" || tier === "table-featured" || tier === "featured";
  }

  function renderSponsorBadge(product) {
    if (!isSponsorActive(product.sponsor)) return "";
    return (
      '<span class="sponsor-badge">' +
      escapeHtml(product.sponsor.label || "Sponsored") +
      "</span>"
    );
  }

  function renderCompareModelCell(product) {
    return (
      '<td class="compare-table__model">' +
      renderSponsorBadge(product) +
      escapeHtml(product.model) +
      "</td>"
    );
  }

  function compareTableRowAttrs(product) {
    var attrs =
      ' data-product-id="' +
      escapeHtml(product.id) +
      '" data-brand-id="' +
      escapeHtml(product.brandId) +
      '"';
    if (hasTableSponsor(product)) attrs += ' class="compare-table__row--sponsored"';
    return attrs;
  }

  function prepareCompareRows(rows, category) {
    var sponsored = [];
    var regular = [];
    rows.forEach(function (p) {
      if (hasTableSponsor(p)) sponsored.push(p);
      else regular.push(p);
    });
    sponsored.sort(compareByBrandFameThenModel);
    return sponsored.concat(sortRows(regular, category));
  }

  function applySponsorCampaigns(campaigns) {
    if (!Array.isArray(campaigns) || !campaigns.length) return;
    var byId = {};
    campaigns.forEach(function (c) {
      if (!c || !c.productId) return;
      byId[c.productId] = normalizeSponsor(c);
    });
    products.forEach(function (p) {
      if (byId[p.id]) p.sponsor = byId[p.id];
    });
  }

  function loadSponsors() {
    if (window.location.protocol === "file:") {
      return Promise.resolve(
        window.CAMPGEAR_DATA && window.CAMPGEAR_DATA.sponsors
          ? window.CAMPGEAR_DATA.sponsors
          : null
      );
    }
    return fetch("data/sponsors.json")
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .catch(function () {
        return null;
      });
  }

  function brandRank(brandId) {
    var b = brandMap[brandId];
    if (b && b.rank != null && isFinite(b.rank)) return b.rank;
    return 9999;
  }

  function compareByBrandFameThenModel(a, b) {
    var ra = brandRank(a.brandId);
    var rb = brandRank(b.brandId);
    if (ra !== rb) return ra - rb;
    return (a.model || "").localeCompare(b.model || "", "en");
  }

  function sortBrandsByFame(list) {
    return list.slice().sort(function (a, b) {
      var ra = a.rank != null && isFinite(a.rank) ? a.rank : 9999;
      var rb = b.rank != null && isFinite(b.rank) ? b.rank : 9999;
      if (ra !== rb) return ra - rb;
      return (a.name || a.id || "").localeCompare(b.name || b.id || "", "en");
    });
  }

  function fullModelName(product) {
    return brandName(product.brandId) + " " + product.model;
  }

  function normalizeSearchText(text) {
    return String(text || "").trim().toLowerCase();
  }

  function productSearchHaystack(product) {
    var parts = [
      brandName(product.brandId),
      product.brandId,
      product.model,
      product.structure,
      product.fabric,
      product.capacity,
      product.tarpType,
      product.bagType,
      product.fillType,
      product.comfortTemp,
      product.subcategory,
      product.size,
      product.weightDisplay,
      product.weightRange,
    ];
    return parts.filter(Boolean).join(" ").toLowerCase();
  }

  function productMatchesSearch(product, query) {
    if (!query) return true;
    return productSearchHaystack(product).indexOf(query) !== -1;
  }

  function productMatchesBrandFilter(product, brandId) {
    if (!brandId || brandId === "all") return true;
    return product.brandId === brandId;
  }

  function productInCategories(product, categories) {
    return categories.indexOf(product.category) !== -1;
  }

  function currentPageCategories() {
    var page = document.body.getAttribute("data-page");
    if (page === "furniture") return ["table", "chair"];
    var category = document.body.getAttribute("data-category");
    return category ? [category] : [];
  }

  function syncSearchInputs(value, source) {
    searchQuery = value;
    var navInput = document.getElementById("nav-search-input");
    var pageInput = document.getElementById("catalog-search-input");
    if (navInput && navInput !== source) navInput.value = value;
    if (pageInput && pageInput !== source) pageInput.value = value;
    document.querySelectorAll(".nav-search__clear, .catalog-search__clear").forEach(function (btn) {
      btn.hidden = !value;
    });
  }

  function updateSearchUrl() {
    if (window.location.protocol === "file:") return;
    var page = document.body.getAttribute("data-page");
    if (page !== "category" && page !== "furniture") return;
    var url = new URL(window.location.href);
    if (searchQuery) {
      url.searchParams.set("q", searchQuery);
    } else {
      url.searchParams.delete("q");
    }
    history.replaceState(null, "", url.pathname + url.search + url.hash);
  }

  function readSearchFromUrl() {
    if (window.location.protocol === "file:") return;
    var q = new URL(window.location.href).searchParams.get("q");
    if (!q) return;
    syncSearchInputs(q);
  }

  function setBrandFilter(brandId) {
    brandFilter = brandId || "all";
    document.querySelectorAll("[data-brand-filter]").forEach(function (btn) {
      var active = (btn.getAttribute("data-brand-filter") || "all") === brandFilter;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function applyCatalogFilters() {
    var categories = currentPageCategories();
    if (!categories.length) return;

    var query = normalizeSearchText(searchQuery);
    var seenIds = {};
    var visibleIds = {};

    document.querySelectorAll("tr[data-product-id], .matrix-card[data-product-id]").forEach(function (el) {
      var id = el.getAttribute("data-product-id");
      var product = findProductById(id);
      if (!product || !productInCategories(product, categories)) return;
      seenIds[id] = true;
      var show =
        productMatchesBrandFilter(product, brandFilter) && productMatchesSearch(product, query);
      el.classList.toggle("is-filtered-out", !show);
      if (show) visibleIds[id] = true;
    });

    document.querySelectorAll(".compare-block").forEach(function (block) {
      var rows = block.querySelectorAll("tbody tr[data-product-id]");
      if (!rows.length) return;
      var anyVisible = false;
      rows.forEach(function (row) {
        if (!row.classList.contains("is-filtered-out")) anyVisible = true;
      });
      block.classList.toggle("is-filtered-empty", !anyVisible);
    });

    document.querySelectorAll(".product-matrix").forEach(function (matrix) {
      var cards = matrix.querySelectorAll(".matrix-card[data-product-id]");
      if (!cards.length) return;
      var anyVisible = false;
      cards.forEach(function (card) {
        if (!card.classList.contains("is-filtered-out")) anyVisible = true;
      });
      matrix.classList.toggle("is-filtered-empty", !anyVisible);
    });

    var totalCount = Object.keys(seenIds).length;
    var visibleCount = Object.keys(visibleIds).length;

    var statusEl = document.getElementById("catalog-filter-status");
    if (statusEl) {
      var filtering = query || (brandFilter && brandFilter !== "all");
      if (!filtering) {
        statusEl.hidden = true;
        statusEl.textContent = "";
      } else {
        statusEl.hidden = false;
        statusEl.textContent =
          visibleCount === totalCount
            ? "Showing all " + totalCount + " models"
            : "Showing " + visibleCount + " of " + totalCount + " models";
      }
    }

    updateSearchUrl();
    renderNavSearchResults();
  }

  function onSearchInput(value, source) {
    syncSearchInputs(value, source);
    applyCatalogFilters();
  }

  function onBrandFilterClick(brandId) {
    setBrandFilter(brandId);
    applyCatalogFilters();
  }

  function categoryBrandIds(category) {
    var categories = category === "furniture" ? ["table", "chair"] : [category];
    var seen = {};
    var ids = [];
    products.forEach(function (p) {
      if (categories.indexOf(p.category) === -1) return;
      if (p.inSummaryTable === false && category !== "furniture") return;
      if (!p.brandId || seen[p.brandId]) return;
      seen[p.brandId] = true;
      ids.push(p.brandId);
    });
    ids.sort(function (a, b) {
      return brandRank(a) - brandRank(b);
    });
    return ids;
  }

  function renderBrandFilterToolbar(category) {
    var toolbar = document.getElementById("brand-filter-toolbar");
    if (!toolbar) return;
    var ids = categoryBrandIds(category);
    var chips =
      '<button type="button" class="filter-chip is-active" data-brand-filter="all" aria-pressed="true">All brands</button>';
    ids.forEach(function (brandId) {
      chips +=
        '<button type="button" class="filter-chip" data-brand-filter="' +
        escapeHtml(brandId) +
        '" aria-pressed="false">' +
        escapeHtml(brandName(brandId)) +
        "</button>";
    });
    toolbar.innerHTML = chips;
    setBrandFilter(brandFilter);
  }

  function ensureCategoryFilters(category) {
    var page = document.body.getAttribute("data-page");
    if (page !== "category" && page !== "furniture") return;

    var mount =
      page === "furniture"
        ? document.getElementById("category-brands") || document.querySelector(".page__head")
        : document.getElementById("catalog-status") || document.querySelector(".page__head");
    if (!mount) return;

    var root = document.getElementById("catalog-filters");
    if (!root) {
      root = document.createElement("div");
      root.id = "catalog-filters";
      root.className = "catalog-filters";
      root.innerHTML =
        '<div class="catalog-search">' +
        '<label class="catalog-search__label" for="catalog-search-input">Search models</label>' +
        '<div class="catalog-search__field">' +
        '<input type="search" id="catalog-search-input" class="catalog-search__input" placeholder="Brand, model, or spec…" autocomplete="off" enterkeyhint="search" />' +
        '<button type="button" class="catalog-search__clear" hidden aria-label="Clear search">×</button>' +
        "</div></div>" +
        '<div class="filter-toolbar" id="brand-filter-toolbar" role="group" aria-label="Filter by brand"></div>' +
        '<p class="catalog-filters__status" id="catalog-filter-status" hidden></p>';
      mount.insertAdjacentElement("afterend", root);
    }

    renderBrandFilterToolbar(category);

    if (!categoryFiltersBound) {
      categoryFiltersBound = true;
      root.addEventListener("input", function (e) {
        if (e.target.id === "catalog-search-input") {
          onSearchInput(e.target.value, e.target);
        }
      });
      root.addEventListener("click", function (e) {
        var clearBtn = e.target.closest(".catalog-search__clear");
        if (clearBtn) {
          onSearchInput("", null);
          var input = document.getElementById("catalog-search-input");
          if (input) input.focus();
          return;
        }
        var chip = e.target.closest("[data-brand-filter]");
        if (chip) {
          onBrandFilterClick(chip.getAttribute("data-brand-filter") || "all");
        }
      });
    }

    syncSearchInputs(searchQuery);
  }

  function searchAllProducts(query, limit) {
    var normalized = normalizeSearchText(query);
    if (!normalized) return [];
    var max = limit || 8;
    var matches = [];
    for (var i = 0; i < products.length; i++) {
      var product = products[i];
      if (!productMatchesSearch(product, normalized)) continue;
      matches.push(product);
      if (matches.length >= max) break;
    }
    return matches;
  }

  function productResultHref(product) {
    var page = CATEGORY_PAGES[product.category] || "index.html";
    var href = page + "?q=" + encodeURIComponent(product.model || "");
    return href;
  }

  function renderNavSearchResults() {
    var panel = document.getElementById("nav-search-results");
    var input = document.getElementById("nav-search-input");
    if (!panel || !input) return;

    var page = document.body.getAttribute("data-page");
    if (page === "category" || page === "furniture") {
      panel.hidden = true;
      panel.innerHTML = "";
      return;
    }

    var query = normalizeSearchText(input.value);
    if (!query) {
      panel.hidden = true;
      panel.innerHTML = "";
      return;
    }

    if (!catalogLoaded) {
      panel.hidden = false;
      panel.innerHTML = '<p class="nav-search__hint">Loading product index…</p>';
      ensureCatalogForSearch().then(function () {
        renderNavSearchResults();
      });
      return;
    }

    var matches = searchAllProducts(query, 8);
    if (!matches.length) {
      panel.hidden = false;
      panel.innerHTML = '<p class="nav-search__empty">No matching models</p>';
      return;
    }

    panel.hidden = false;
    panel.innerHTML = matches
      .map(function (product) {
        var categoryLabel = CATEGORY_LABELS[product.category] || product.category;
        return (
          '<a class="nav-search__result" href="' +
          escapeHtml(productResultHref(product)) +
          '">' +
          '<span class="nav-search__result-name">' +
          escapeHtml(fullModelName(product)) +
          "</span>" +
          '<span class="nav-search__result-meta">' +
          escapeHtml(categoryLabel) +
          "</span></a>"
        );
      })
      .join("");
  }

  function bindNavSearch() {
    if (navSearchBound) return;
    var form = document.querySelector(".nav-search__form");
    var input = document.getElementById("nav-search-input");
    if (!form || !input) return;
    navSearchBound = true;

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var page = document.body.getAttribute("data-page");
      if (page === "category" || page === "furniture") {
        applyCatalogFilters();
        var compare = document.getElementById("compare") || document.getElementById("tables-section");
        if (compare) scrollToHash("#" + compare.id);
        return;
      }
      renderNavSearchResults();
      var first = document.querySelector(".nav-search__result");
      if (first) {
        window.location.href = first.getAttribute("href");
      }
    });

    input.addEventListener("input", function () {
      var page = document.body.getAttribute("data-page");
      if (page === "category" || page === "furniture") {
        onSearchInput(input.value, input);
      } else {
        renderNavSearchResults();
      }
    });

    input.addEventListener("focus", function () {
      if (document.body.getAttribute("data-page") === "home") {
        ensureCatalogForSearch();
      }
      renderNavSearchResults();
    });

    document.addEventListener("click", function (e) {
      var panel = document.getElementById("nav-search-results");
      if (!panel || panel.hidden) return;
      if (e.target.closest(".nav-search")) return;
      panel.hidden = true;
    });

    var clearBtn = document.querySelector(".nav-search__clear");
    if (clearBtn) {
      clearBtn.addEventListener("click", function () {
        onSearchInput("", null);
        input.focus();
        renderNavSearchResults();
      });
    }
  }

  function injectNavSearch() {
    var nav = document.querySelector(".site-header .nav");
    if (!nav || nav.querySelector(".nav-search")) return;

    var wrap = document.createElement("div");
    wrap.className = "nav-search";
    wrap.innerHTML =
      '<form class="nav-search__form" role="search">' +
      '<label class="visually-hidden" for="nav-search-input">Search camping gear</label>' +
      '<span class="nav-search__icon" aria-hidden="true">' +
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>' +
      "</span>" +
      '<input type="search" id="nav-search-input" class="nav-search__input" placeholder="Search models…" autocomplete="off" enterkeyhint="search" />' +
      '<button type="button" class="nav-search__clear" hidden aria-label="Clear search">×</button>' +
      "</form>" +
      '<div class="nav-search__results" id="nav-search-results" hidden></div>';
    var links = nav.querySelector(".nav__links");
    if (links) {
      nav.insertBefore(wrap, links);
    } else {
      nav.appendChild(wrap);
    }
    bindNavSearch();
  }

  function ensureCatalogForSearch() {
    if (catalogLoaded) return Promise.resolve();
    if (catalogLoadPromise) return catalogLoadPromise;
    catalogLoadPromise = Promise.resolve(loadCatalog()).then(function () {
      return catalogLoaded;
    });
    return catalogLoadPromise;
  }

  function parseFirstNumber(text) {
    if (text == null || text === "") return null;
    var match = String(text).match(/[\d.]+/);
    return match ? parseFloat(match[0]) : null;
  }

  function getSortValue(product, key) {
    if (key === "weight") {
      if (product.weightKg != null && isFinite(product.weightKg)) return product.weightKg;
      return parseFirstNumber(product.weightDisplay || product.weightRange);
    }
    if (key === "capacity") {
      return parseFirstNumber(product.capacity);
    }
    if (key === "price") {
      var price = product.priceMin != null ? product.priceMin : product.price;
      return price != null && isFinite(price) ? price : null;
    }
    if (key === "comfort") {
      return parseFirstNumber(product.comfortTemp);
    }
    return null;
  }

  function isSortValueMissing(value) {
    return value == null || !isFinite(value);
  }

  function sortRows(rows, tableId) {
    var sort = tableSort[tableId];
    if (!sort || !sort.key) {
      return rows.slice().sort(compareByBrandFameThenModel);
    }
    var dir = sort.dir === "desc" ? -1 : 1;
    return rows.slice().sort(function (a, b) {
      var va = getSortValue(a, sort.key);
      var vb = getSortValue(b, sort.key);
      var aMissing = isSortValueMissing(va);
      var bMissing = isSortValueMissing(vb);
      if (aMissing && bMissing) return compareByBrandFameThenModel(a, b);
      if (aMissing) return 1;
      if (bMissing) return -1;
      if (va === vb) return compareByBrandFameThenModel(a, b);
      return (va < vb ? -1 : 1) * dir;
    });
  }

  function renderSortableTh(label, key, tableId) {
    var sort = tableSort[tableId];
    var active = sort && sort.key === key;
    var indicator = active ? (sort.dir === "asc" ? "↑" : "↓") : "↕";
    var ariaSort = active ? (sort.dir === "asc" ? "ascending" : "descending") : "none";
    return (
      '<th scope="col" class="compare-table__sortable' +
      (active ? " is-sorted" : "") +
      '" data-sort-table="' +
      tableId +
      '" data-sort-key="' +
      key +
      '" tabindex="0" role="columnheader" aria-sort="' +
      ariaSort +
      '">' +
      '<button type="button" class="compare-table__sort-btn">' +
      escapeHtml(label) +
      '<span class="compare-table__sort-icon" aria-hidden="true">' +
      indicator +
      "</span></button></th>"
    );
  }

  function toggleTableSort(tableId, key) {
    ensureSortState(tableId);
    var sort = tableSort[tableId];
    if (sort.key === key) {
      sort.dir = sort.dir === "asc" ? "desc" : "asc";
    } else {
      sort.key = key;
      sort.dir = "asc";
    }
    var category = document.body.getAttribute("data-category") || tableId;
    ensureSortState(tableId);
    renderCategoryPage(category);
  }

  function highlightProductCard(el) {
    if (!el) return;
    el.classList.add("product-card--highlight");
    window.setTimeout(function () {
      el.classList.remove("product-card--highlight");
    }, 2200);
  }

  function bindThumbLinkHandlers() {
    var root = document.getElementById("compare-root");
    if (!root || root.dataset.thumbNavBound === "1") return;
    root.dataset.thumbNavBound = "1";
    root.addEventListener("click", function (e) {
      var btn = e.target.closest(".compare-table__thumb-btn[data-product-id]");
      if (!btn) return;
      e.preventDefault();
      openProductModal(btn.getAttribute("data-product-id"));
    });
  }

  function scrollToProductHashIfPresent() {
    var hash = window.location.hash;
    if (!hash || hash.indexOf("#product-") !== 0) return;
    var productId = hash.slice(9);
    if (!productId || !document.getElementById("product-modal")) return;
    window.setTimeout(function () {
      if (findProductById(productId)) {
        openProductModal(productId);
      }
    }, 80);
  }

  function bindTableSortHandlers() {
    if (tableSortBound) return;
    var root = document.getElementById("compare-root");
    if (!root) return;
    tableSortBound = true;

    root.addEventListener("click", function (e) {
      var btn = e.target.closest(".compare-table__sort-btn");
      if (!btn) return;
      var th = btn.closest("[data-sort-key]");
      if (!th) return;
      e.preventDefault();
      toggleTableSort(th.getAttribute("data-sort-table"), th.getAttribute("data-sort-key"));
    });

    root.addEventListener("keydown", function (e) {
      if (e.key !== "Enter" && e.key !== " ") return;
      var th = e.target.closest("[data-sort-key]");
      if (!th || !th.classList.contains("compare-table__sortable")) return;
      e.preventDefault();
      toggleTableSort(th.getAttribute("data-sort-table"), th.getAttribute("data-sort-key"));
    });
  }

  function productAnchorId(product) {
    return "product-" + product.id;
  }

  function imageCreditHtml(product, className) {
    if (!product.imageUrl) return "";
    var brand = brandName(product.brandId);
    var credit =
      "© " +
      brand +
      " · Image from official site";
    if (product.sourceUrl) {
      return (
        '<p class="' +
        escapeHtml(className) +
        '">© ' +
        escapeHtml(brand) +
        ' · <a href="' +
        escapeHtml(product.sourceUrl) +
        '" target="_blank" rel="noopener noreferrer">Image from official site</a></p>'
      );
    }
    return '<p class="' + escapeHtml(className) + '">' + escapeHtml(credit) + "</p>";
  }

  function renderTableThumb(product) {
    var alt = escapeHtml(product.imageAlt || product.model);
    var label = escapeHtml('View details for "' + (product.model || "") + '"');
    if (product.imageUrl) {
      var img =
        '<img src="' +
        escapeHtml(product.imageUrl) +
        '" alt="' +
        alt +
        '" width="112" height="112" loading="lazy" decoding="async" />';
      return (
        '<td class="compare-table__thumb">' +
        '<button type="button" class="compare-table__thumb-btn" data-product-id="' +
        escapeHtml(product.id) +
        '" aria-label="' +
        label +
        '">' +
        img +
        "</button>" +
        imageCreditHtml(product, "compare-table__thumb-credit") +
        "</td>"
      );
    }
    return '<td class="compare-table__thumb compare-table__thumb--empty"><span aria-hidden="true">—</span></td>';
  }

  function renderTentTable(rows, compact) {
    var body = rows
      .map(function (p) {
        return (
          "<tr" + compareTableRowAttrs(p) + ">" +
          "<td>" + escapeHtml(brandName(p.brandId)) + "</td>" +
          renderCompareModelCell(p) +
          renderTableThumb(p) +
          "<td>" + escapeHtml(displayCell(p.structure)) + "</td>" +
          "<td>" + escapeHtml(formatWeight(p)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.capacity)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.fabric)) + "</td>" +
          "<td>" + escapeHtml(priceForProduct(p)) + "</td>" +
          "<td>" + escapeHtml(formatScenarios(p.scenarios)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="tent">' +
      '<h2 class="compare-block__title">Tent Specs Overview</h2>' +
      TABLE_SCROLL_HINT +
      '<div class="table-wrap"><table class="compare-table">' +
      "<thead><tr>" +
      "<th scope=\"col\">Brand</th><th scope=\"col\">Model</th><th scope=\"col\" class=\"compare-table__thumb-col\">Thumb</th><th scope=\"col\">Structure</th>" +
      renderSortableTh("Weight", "weight", "tent") +
      renderSortableTh("Capacity", "capacity", "tent") +
      "<th scope=\"col\">Fabric / Waterproofing</th>" +
      renderSortableTh("Price", "price", "tent") +
      "<th scope=\"col\">Use Cases</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderTarpTable(rows) {
    var body = rows
      .map(function (p) {
        return (
          "<tr" + compareTableRowAttrs(p) + ">" +
          "<td>" + escapeHtml(brandName(p.brandId)) + "</td>" +
          renderCompareModelCell(p) +
          renderTableThumb(p) +
          "<td>" + escapeHtml(displayCell(p.tarpType)) + "</td>" +
          "<td>" + escapeHtml(formatWeight(p)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.capacity)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.size)) + "</td>" +
          "<td>" + escapeHtml(priceForProduct(p)) + "</td>" +
          "<td>" + escapeHtml(formatScenarios(p.scenarios)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="tarp">' +
      '<h2 class="compare-block__title">Tarp Specs Overview</h2>' +
      TABLE_SCROLL_HINT +
      '<div class="table-wrap"><table class="compare-table">' +
      "<thead><tr>" +
      "<th scope=\"col\">Brand</th><th scope=\"col\">Model</th><th scope=\"col\" class=\"compare-table__thumb-col\">Thumb</th><th scope=\"col\">Type</th>" +
      renderSortableTh("Weight", "weight", "tarp") +
      renderSortableTh("Capacity", "capacity", "tarp") +
      "<th scope=\"col\">Size</th>" +
      renderSortableTh("Price", "price", "tarp") +
      "<th scope=\"col\">Use Cases</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderSleepingBagTable(rows) {
    var body = rows
      .map(function (p) {
        return (
          "<tr" + compareTableRowAttrs(p) + ">" +
          "<td class=\"compare-table__brand\">" + escapeHtml(brandName(p.brandId)) + "</td>" +
          renderCompareModelCell(p) +
          renderTableThumb(p) +
          "<td>" + escapeHtml(displayCell(p.bagType || p.structure)) + "</td>" +
          "<td class=\"compare-table__num\">" + escapeHtml(formatWeight(p)) + "</td>" +
          "<td class=\"compare-table__num\">" + escapeHtml(displayCell(p.comfortTemp)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.fillType || p.fabric)) + "</td>" +
          "<td class=\"compare-table__price\">" + escapeHtml(priceForProduct(p)) + "</td>" +
          "<td class=\"compare-table__scenarios\">" + escapeHtml(formatScenarios(p.scenarios)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="sleeping-bag">' +
      '<h2 class="compare-block__title">Sleeping Bag Specs Overview</h2>' +
      TABLE_SCROLL_HINT +
      '<div class="table-wrap"><table class="compare-table compare-table--sleeping-bag">' +
      "<thead><tr>" +
      "<th scope=\"col\">Brand</th><th scope=\"col\">Model</th><th scope=\"col\" class=\"compare-table__thumb-col\">Thumb</th>" +
      "<th scope=\"col\">Type</th>" +
      renderSortableTh("Weight", "weight", "sleeping-bag") +
      renderSortableTh("Comfort Rating", "comfort", "sleeping-bag") +
      "<th scope=\"col\">Fill</th>" +
      renderSortableTh("Price", "price", "sleeping-bag") +
      "<th scope=\"col\">Use Cases</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderProsTable(rows) {
    if (!rows.length) return "";

    var body = rows
      .map(function (p) {
        return (
          "<tr" + compareTableRowAttrs(p) + ">" +
          "<td>" + escapeHtml(fullModelName(p)) + "</td>" +
          "<td>" + escapeHtml(priceForProduct(p)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.pros)) + "</td>" +
          "<td>" + escapeHtml(displayCell(p.cons)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="tent">' +
      '<h2 class="compare-block__title">Backpacking Tents at Similar Prices · Pros &amp; Cons</h2>' +
      TABLE_SCROLL_HINT +
      '<div class="table-wrap"><table class="compare-table compare-table--pros">' +
      "<thead><tr>" +
      "<th scope=\"col\">Brand &amp; Model</th><th scope=\"col\">Price</th>" +
      "<th scope=\"col\">Strengths</th><th scope=\"col\">Trade-offs</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderProductCard(product) {
    var specs = [];
    if (product.category === "tent") {
      specs.push({ label: "Structure", value: displayCell(product.detailStructure || product.structure) });
      specs.push({ label: "Weight", value: formatWeight(product) });
    } else if (product.category === "sleeping-bag") {
      specs.push({ label: "Type", value: displayCell(product.bagType || product.detailStructure) });
      specs.push({ label: "Weight", value: formatWeight(product) });
      specs.push({ label: "Comfort Rating", value: displayCell(product.comfortTemp) });
      specs.push({ label: "Fill", value: displayCell(product.fillType) });
    } else {
      specs.push({ label: "Type", value: displayCell(product.detailStructure || product.tarpType) });
      specs.push({ label: "Weight", value: formatWeight(product) });
      specs.push({ label: "Capacity", value: displayCell(product.capacity) });
    }
    specs.push({ label: "Price", value: priceForProduct(product) });
    specs.push({
      label: "Highlights",
      value: displayCell(product.highlights && product.highlights[0]),
    });

    var specHtml = specs
      .map(function (s) {
        return "<div><dt>" + escapeHtml(s.label) + "</dt><dd>" + escapeHtml(s.value) + "</dd></div>";
      })
      .join("");

    var img =
      product.imageUrl
        ? '<img src="' + escapeHtml(product.imageUrl) + '" alt="' + escapeHtml(product.imageAlt || product.model) + '" width="640" height="427" loading="lazy" />'
        : "";

    var desc =
      product.description
        ? '<p class="product-card__desc">' + escapeHtml(localizeDisplayValue(product.description).slice(0, 220)) + (product.description.length > 220 ? "…" : "") + "</p>"
        : "";

    var sourceLink = product.sourceUrl
      ? '<p class="product-card__source"><a href="' + escapeHtml(product.sourceUrl) + '" target="_blank" rel="noopener noreferrer">View official site</a></p>'
      : "";

    return (
      '<article class="product-card" id="' +
      escapeHtml(productAnchorId(product)) +
      '" tabindex="-1">' +
      '<div class="product-card__media">' + img + "</div>" +
      '<div class="product-card__body">' +
      '<span class="product-card__brand">' + escapeHtml(brandName(product.brandId)) + "</span>" +
      "<h3 class=\"product-card__model\">" + escapeHtml(product.model) + "</h3>" +
      desc +
      '<dl class="product-spec">' + specHtml + "</dl>" +
      sourceLink +
      "</div></article>"
    );
  }

  function renderDetailSection(category, id, title, lead) {
    var items = products.filter(function (p) {
      return p.category === category && p.inDetailCards !== false;
    });
    if (!items.length) return "";

    var cards = items.map(renderProductCard).join("");

    return (
      '<section id="' + id + '" class="detail-section" data-compare-group="' + category + '" aria-labelledby="' + id + '-heading">' +
      '<h2 id="' + id + '-heading" class="detail-section__title">' + escapeHtml(title) + "</h2>" +
      '<p class="detail-section__lead">' + escapeHtml(lead) + "</p>" +
      '<div class="product-grid">' + cards + "</div>" +
      "</section>"
    );
  }

  var CATEGORY_LABELS = {
    tent: "Tents",
    tarp: "Tarps",
    "sleeping-bag": "Sleeping Bags",
    stove: "Stoves",
    table: "Tables & Chairs",
    chair: "Tables & Chairs",
    other: "Other",
  };

  function ensureSortState(tableId) {
    if (!tableSort[tableId]) {
      tableSort[tableId] = { key: null, dir: "asc" };
    }
  }

  function categoryBrandNames(category) {
    var categories =
      category === "furniture" ? ["table", "chair"] : [category];
    var skipSummaryFilter = category === "furniture";
    var seen = {};
    var ids = [];
    products.forEach(function (p) {
      if (categories.indexOf(p.category) === -1) return;
      if (!skipSummaryFilter && p.inSummaryTable === false) return;
      if (!p.brandId || seen[p.brandId]) return;
      seen[p.brandId] = true;
      ids.push(p.brandId);
    });
    ids.sort(function (a, b) {
      return brandRank(a) - brandRank(b);
    });
    return ids.map(brandName);
  }

  function renderCategoryBrands(category) {
    var el = document.getElementById("category-brands");
    if (!el) return;
    var names = categoryBrandNames(category);
    el.textContent = names.length ? "Brands: " + names.join(" · ") : "";
    el.hidden = !names.length;
  }

  var CATEGORY_MODAL = { tent: true, tarp: true, "sleeping-bag": true };

  function renderCategoryPage(category) {
    ensureSortState(category);

    var rows = products.filter(function (p) {
      return p.category === category && p.inSummaryTable !== false;
    });
    rows = prepareCompareRows(rows, category);

    renderCategoryBrands(category);

    var compareHtml = "";
    if (category === "tent") {
      var prosRows = products
        .filter(function (p) {
          return p.category === "tent" && p.pros && p.cons;
        })
        .slice()
        .sort(compareByBrandFameThenModel);
      compareHtml = renderTentTable(rows) + renderProsTable(prosRows);
    } else if (category === "tarp") {
      compareHtml = renderTarpTable(rows);
    } else if (category === "sleeping-bag") {
      compareHtml = renderSleepingBagTable(rows);
    }

    var compareRoot = document.getElementById("compare-root");
    if (compareRoot) {
      compareRoot.innerHTML =
        compareHtml || '<p class="page__lead">No comparison data for this category yet.</p>';
      compareRoot.hidden = false;
    }

    var label = CATEGORY_LABELS[category] || category;
    var introRoot = document.getElementById("intro-root");
    if (introRoot && !CATEGORY_MODAL[category]) {
      var sectionHtml = renderDetailSection(
        category,
        category + "-detail",
        label + " · Model Guides",
        "Data and images are from brand official sites (data/official) and are for reference only."
      );
      introRoot.innerHTML =
        sectionHtml || '<p class="page__lead">No model guide data for this category yet.</p>';
      introRoot.hidden = false;
    }

    bindProductModalHandlers();
    bindThumbLinkHandlers();
    if (compareHtml) {
      bindTableSortHandlers();
    }
    ensureCategoryFilters(category);
    applyCatalogFilters();
    scrollToProductHashIfPresent();
  }

  function findProductById(id) {
    for (var i = 0; i < products.length; i++) {
      if (products[i].id === id) return products[i];
    }
    return null;
  }

  function sortFurnitureRows(rows) {
    return rows.slice().sort(compareByBrandFameThenModel);
  }

  function renderMatrixCard(product) {
    var img = product.imageUrl
      ? '<img src="' +
        escapeHtml(product.imageUrl) +
        '" alt="' +
        escapeHtml(product.imageAlt || product.model) +
        '" width="320" height="240" loading="lazy" />'
      : '<span class="matrix-card__no-img">No image</span>';
    return (
      '<article class="matrix-card" role="listitem" data-product-id="' +
      escapeHtml(product.id) +
      '" data-brand-id="' +
      escapeHtml(product.brandId) +
      '">' +
      '<button type="button" class="matrix-card__btn" data-product-id="' +
      escapeHtml(product.id) +
      '" aria-label="View ' +
      escapeHtml(fullModelName(product)) +
      ' details">' +
      '<span class="matrix-card__media">' +
      img +
      "</span>" +
      '<span class="matrix-card__brand">' +
      escapeHtml(brandName(product.brandId)) +
      "</span>" +
      '<span class="matrix-card__model">' +
      escapeHtml(product.model) +
      "</span>" +
      '<span class="matrix-card__price">' +
      escapeHtml(priceForProduct(product)) +
      "</span>" +
      "</button>" +
      imageCreditHtml(product, "matrix-card__credit") +
      "</article>"
    );
  }

  function renderFurnitureMatrix(containerId, category) {
    var root = document.getElementById(containerId);
    if (!root) return 0;
    var rows = sortFurnitureRows(
      products.filter(function (p) {
        return p.category === category;
      })
    );
    if (!rows.length) {
      root.innerHTML = '<p class="product-matrix__empty">No models in this category yet.</p>';
      return 0;
    }
    root.innerHTML = rows.map(renderMatrixCard).join("");
    return rows.length;
  }

  function modalHighlights(product) {
    var desc = (product.description || "").trim();
    var list = (product.highlights || []).filter(Boolean);
    if (!list.length) return [];
    list = list.filter(function (h) {
      var snippet = String(h).trim().slice(0, 72);
      if (!snippet) return false;
      if (desc && desc.indexOf(snippet) >= 0) return false;
      return true;
    });
    return list.slice(0, 3);
  }

  function productSpecRows(product) {
    var rows = [];
    var cat = product.category;
    if (cat === "tent") {
      rows.push({ label: "Structure", value: displayCell(product.structure || product.detailStructure) });
      rows.push({ label: "Weight", value: formatWeight(product) });
      rows.push({ label: "Capacity", value: displayCell(product.capacity) });
      rows.push({ label: "Fabric / Waterproofing", value: displayCell(product.fabric) });
    } else if (cat === "tarp") {
      rows.push({ label: "Type", value: displayCell(product.tarpType || product.detailStructure) });
      rows.push({ label: "Weight", value: formatWeight(product) });
      rows.push({ label: "Capacity", value: displayCell(product.capacity) });
      rows.push({ label: "Size", value: displayCell(product.size) });
    } else if (cat === "sleeping-bag") {
      rows.push({ label: "Type", value: displayCell(product.bagType || product.detailStructure) });
      rows.push({ label: "Weight", value: formatWeight(product) });
      rows.push({ label: "Comfort Rating", value: displayCell(product.comfortTemp) });
      rows.push({ label: "Fill", value: displayCell(product.fillType) });
    } else if (cat === "table" || cat === "chair") {
      rows.push({ label: "Weight", value: formatWeight(product) });
      if (product.seatHeight) rows.push({ label: "Seat Height", value: displayCell(product.seatHeight) });
      if (product.foldedSize) rows.push({ label: "Packed Size", value: displayCell(product.foldedSize) });
      if (product.subcategory) rows.push({ label: "Type", value: displayCell(product.subcategory) });
    }
    rows.push({ label: "Price", value: priceForProduct(product) });
    if (product.scenarios && product.scenarios.length) {
      rows.push({ label: "Use Cases", value: formatScenarios(product.scenarios) });
    }
    if (product.pros) rows.push({ label: "Strengths", value: displayCell(product.pros) });
    if (product.cons) rows.push({ label: "Trade-offs", value: displayCell(product.cons) });
    return rows;
  }

  function openProductModal(productId) {
    var product = findProductById(productId);
    var modal = document.getElementById("product-modal");
    if (!product || !modal) return;

    lastModalFocus = document.activeElement;

    var media = document.getElementById("product-modal-media");
    if (media) {
      media.innerHTML = product.imageUrl
        ? '<img src="' +
          escapeHtml(product.imageUrl) +
          '" alt="' +
          escapeHtml(product.imageAlt || product.model) +
          '" />' +
          imageCreditHtml(product, "product-modal__image-credit")
        : '<p class="product-modal__no-img">No product image</p>';
    }

    var brandEl = document.getElementById("product-modal-brand");
    if (brandEl) brandEl.textContent = brandName(product.brandId);

    var sponsorEl = document.getElementById("product-modal-sponsor");
    if (sponsorEl) {
      if (hasModalSponsor(product)) {
        sponsorEl.innerHTML =
          renderSponsorBadge(product) +
          '<span class="product-modal__sponsor-note">Paid placement — comparison specs are not altered.</span>';
        sponsorEl.hidden = false;
      } else {
        sponsorEl.innerHTML = "";
        sponsorEl.hidden = true;
      }
    }

    var titleEl = document.getElementById("product-modal-title");
    if (titleEl) titleEl.textContent = product.model || "";

    var specsEl = document.getElementById("product-modal-specs");
    if (specsEl) {
      specsEl.innerHTML = productSpecRows(product)
        .map(function (s) {
          return (
            "<div><dt>" +
            escapeHtml(s.label) +
            "</dt><dd>" +
            escapeHtml(s.value) +
            "</dd></div>"
          );
        })
        .join("");
    }

    var descEl = document.getElementById("product-modal-desc");
    if (descEl) {
      if (product.description) {
        descEl.textContent = localizeDisplayValue(product.description.trim());
        descEl.hidden = false;
      } else {
        descEl.textContent = "";
        descEl.hidden = true;
      }
    }

    var hiEl = document.getElementById("product-modal-highlights");
    if (hiEl) {
      var modalHi = modalHighlights(product);
      if (modalHi.length) {
        hiEl.innerHTML = modalHi
          .map(function (h) {
            return "<li>" + escapeHtml(displayCell(h)) + "</li>";
          })
          .join("");
        hiEl.hidden = false;
      } else {
        hiEl.innerHTML = "";
        hiEl.hidden = true;
      }
    }

    var linkEl = document.getElementById("product-modal-link");
    var sourceWrap = document.getElementById("product-modal-source");
    if (linkEl && sourceWrap) {
      if (product.sourceUrl) {
        linkEl.href = product.sourceUrl;
        linkEl.classList.add("outbound-link");
        linkEl.setAttribute("data-product-id", product.id);
        linkEl.setAttribute("data-platform", "official");
        linkEl.removeAttribute("hidden");
        sourceWrap.hidden = false;
      } else {
        linkEl.href = "#";
        linkEl.classList.remove("outbound-link");
        linkEl.removeAttribute("data-product-id");
        linkEl.removeAttribute("data-platform");
        sourceWrap.hidden = true;
      }
    }

    trackEvent("Product Modal Open", {
      productId: product.id,
      brandId: product.brandId,
      category: product.category,
      page: document.body.getAttribute("data-page") || "unknown",
      sponsored: hasModalSponsor(product) ? "yes" : "no",
    });

    modal.hidden = false;
    document.body.classList.add("modal-open");
    var closeBtn = modal.querySelector(".product-modal__close");
    if (closeBtn) closeBtn.focus();
  }

  function closeProductModal() {
    var modal = document.getElementById("product-modal");
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("modal-open");
    if (lastModalFocus && typeof lastModalFocus.focus === "function") {
      lastModalFocus.focus();
    }
    lastModalFocus = null;
  }

  function bindProductModalHandlers() {
    if (furnitureModalBound) return;
    furnitureModalBound = true;
    document.addEventListener("click", function (e) {
      var close = e.target.closest("[data-modal-close]");
      if (close) {
        e.preventDefault();
        closeProductModal();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeProductModal();
    });
  }

  function bindFurnitureMatrixHandlers() {
    if (furnitureMatrixBound) return;
    furnitureMatrixBound = true;
    document.addEventListener("click", function (e) {
      var btn = e.target.closest(".matrix-card__btn[data-product-id]");
      if (!btn) return;
      e.preventDefault();
      openProductModal(btn.getAttribute("data-product-id"));
    });
  }

  function renderFurniturePage() {
    renderCategoryBrands("furniture");

    var tableCount = renderFurnitureMatrix("tables-matrix", "table");
    var chairCount = renderFurnitureMatrix("chairs-matrix", "chair");

    bindProductModalHandlers();
    bindFurnitureMatrixHandlers();
    ensureCategoryFilters("furniture");
    applyCatalogFilters();
  }

  function setStatus(message, isError) {
    var el = document.getElementById("catalog-status");
    if (!el) return;
    el.textContent = message;
    el.classList.toggle("catalog-status--error", !!isError);
  }

  function applySiteConfig(site) {
    if (!site || !site.hero) return;
    var h = site.hero;
    var img = document.getElementById("hero-image");
    if (img && h.imageUrl) {
      img.src = h.imageUrl;
      if (h.imageAlt) img.alt = h.imageAlt;
    }
    var eyebrow = document.getElementById("hero-eyebrow");
    if (eyebrow && h.eyebrow) eyebrow.textContent = h.eyebrow;
    var title = document.getElementById("hero-title");
    if (title && h.title) title.textContent = h.title;
    var subtitle = document.getElementById("hero-subtitle");
    if (subtitle && h.subtitle) subtitle.textContent = h.subtitle;
  }

  var TABLE_SCROLL_HINT =
    '<p class="table-scroll__hint" aria-hidden="true">← Swipe to see more columns →</p>';

  function loadSite() {
    return fetch("data/site.json")
      .then(function (r) {
        if (!r.ok) return null;
        return r.json();
      })
      .then(function (site) {
        if (site) applySiteConfig(site);
      })
      .catch(function () {});
  }

  function officialToDisplay(raw) {
    var specs = raw.specs || {};
    var image = raw.imageUrl;
    if (!image && raw.imageLicense === "brand-approved" && raw.imageLocal) {
      image = raw.imageLocal;
      if (image.indexOf("http") !== 0 && image.indexOf("/") !== 0) {
        image = "/" + image;
      }
    }
    var display = {
      id: raw.id,
      brandId: raw.brandId,
      category: raw.category,
      model: raw.model,
      priceMin: raw.priceMin != null ? raw.priceMin : raw.price,
      priceMax: raw.priceMax != null ? raw.priceMax : raw.price,
      currency: raw.currency,
      highlights: raw.highlights || [],
      description: raw.description,
      sourceUrl: raw.sourceUrl,
      scrapedAt: raw.scrapedAt,
      status: raw.status,
      inSummaryTable: raw.inSummaryTable !== false,
      inDetailCards: raw.inDetailCards !== false,
      imageUrl: image,
      imageAlt: raw.imageAlt || raw.model,
      pros: raw.pros,
      cons: raw.cons,
      scenarios: raw.scenarios,
    };
    var fields = [
      "structure",
      "detailStructure",
      "weightKg",
      "weightDisplay",
      "weightRange",
      "capacity",
      "fabric",
      "tarpType",
      "size",
      "subcategory",
      "bagType",
      "fillType",
      "comfortTemp",
      "seatHeight",
      "foldedSize",
    ];
    fields.forEach(function (key) {
      if (raw[key] != null && raw[key] !== "") display[key] = raw[key];
      else if (specs[key] != null && specs[key] !== "") display[key] = specs[key];
    });
    if (display.category === "tent") {
      if (!display.structure && display.subcategory) display.structure = display.subcategory;
      if (!display.detailStructure) {
        display.detailStructure = display.structure || display.subcategory || "—";
      }
    }
    if (display.category === "tarp") {
      if (!display.tarpType && display.subcategory) display.tarpType = display.subcategory;
      if (!display.detailStructure) display.detailStructure = display.tarpType || display.subcategory;
    }
    if (display.category === "sleeping-bag") {
      if (!display.bagType && display.subcategory) display.bagType = display.subcategory;
      if (!display.detailStructure) display.detailStructure = display.bagType || display.subcategory;
    }
    if (raw.sponsor) display.sponsor = normalizeSponsor(raw.sponsor);
    return display;
  }

  /** Visible on site: verified/merged, published, or legacy draft before migration. */
  function isVisibleOnSite(p) {
    if (!p || typeof p !== "object") return false;
    if (p.status === "verified" || p.status === "merged") return true;
    if (p.published === true) return true;
    if (p.status === "draft" && p.published === undefined) return true;
    return false;
  }

  /** Display products from data/official only (not products.json). */
  function productsFromOfficial(productsData, brandsData) {
    if (!Array.isArray(productsData)) return [];
    var brandIds = {};
    if (Array.isArray(brandsData)) {
      brandsData.forEach(function (b) {
        if (b && b.id) brandIds[b.id] = true;
      });
    }
    var seen = {};
    var list = [];
    productsData.forEach(function (p) {
      if (!p || typeof p !== "object") return;
      if (!p.id || seen[p.id]) return;
      if (!p.brandId || !brandIds[p.brandId]) return;
      if (!isVisibleOnSite(p)) return;
      var allowed = {
        tent: true,
        tarp: true,
        "sleeping-bag": true,
        stove: true,
        table: true,
        chair: true,
        other: true,
      };
      if (!allowed[p.category]) return;
      seen[p.id] = true;
      list.push(officialToDisplay(p));
    });
    return list;
  }

  function loadOfficialBrandIds() {
    return fetch("data/official/index.json")
      .then(function (r) {
        if (!r.ok) throw new Error("Failed to load official/index.json");
        return r.json();
      })
      .then(function (data) {
        return data.brandIds || [];
      });
  }

  function loadOfficialProducts(brandIds) {
    if (!brandIds.length) return Promise.resolve([]);
    return Promise.all(
      brandIds.map(function (brandId) {
        return fetch("data/official/" + brandId + "/products.json").then(function (r) {
          if (!r.ok) throw new Error("Failed to load official/" + brandId + "/products.json");
          return r.json();
        });
      })
    ).then(function (lists) {
      return lists.reduce(function (acc, list) {
        return acc.concat(list);
      }, []);
    });
  }

  function hydrateCatalog(brandsData, productsData, siteData, sponsorsData) {
    brands = sortBrandsByFame(Array.isArray(brandsData) ? brandsData : []);
    brandMap = {};
    brands.forEach(function (b) {
      if (b && b.id) brandMap[b.id] = b;
    });
    products = productsFromOfficial(productsData, brands);
    catalogLoaded = true;
    if (sponsorsData && sponsorsData.campaigns) {
      applySponsorCampaigns(sponsorsData.campaigns);
    }
    var page = document.body.getAttribute("data-page");
    var statusEl = document.getElementById("catalog-status");

    if (!products.length) {
      setStatus("No products available to display in data/official.", true);
      if (statusEl) statusEl.hidden = false;
      var compareRoot = document.getElementById("compare-root");
      var introRoot = document.getElementById("intro-root");
      if (compareRoot) compareRoot.hidden = true;
      if (introRoot) introRoot.hidden = true;
      if (page === "furniture") renderFurniturePage();
      return;
    }

    if (page === "furniture") {
      var furnitureCount = products.filter(function (p) {
        return p.category === "table" || p.category === "chair";
      }).length;
      if (!furnitureCount) {
        setStatus("No table or chair data for furniture yet. Run the scrape script first.", true);
        if (statusEl) statusEl.hidden = false;
      } else {
        setStatus("");
        if (statusEl) statusEl.hidden = true;
      }
      renderFurniturePage();
      return;
    }

    if (page === "category") {
      var category = document.body.getAttribute("data-category");
      var inCategory = products.filter(function (p) {
        return p.category === category;
      });
      if (!inCategory.length) {
        setStatus("No product data for this category yet.", true);
        if (statusEl) statusEl.hidden = false;
        return;
      }
      renderCategoryPage(category);
    }

    setStatus("");
    if (statusEl) statusEl.hidden = true;
  }

  function loadCatalog() {
    if (window.location.protocol === "file:") {
      if (window.CAMPGEAR_DATA) {
        hydrateCatalog(
          window.CAMPGEAR_DATA.brands,
          window.CAMPGEAR_DATA.products,
          window.CAMPGEAR_DATA.site,
          window.CAMPGEAR_DATA.sponsors
        );
        return;
      }
      setStatus(
        "Cannot load JSON from file://. Run python3 -m http.server 8080 in this directory and open http://localhost:8080, or run python3 scripts/build_catalog.py to generate data/catalog.js.",
        true
      );
      return;
    }

    return Promise.all([
      loadSite(),
      fetch("data/brands.json").then(function (r) {
        if (!r.ok) throw new Error("Failed to load brands.json");
        return r.json();
      }),
      loadOfficialBrandIds().then(loadOfficialProducts),
      loadSponsors(),
    ])
      .then(function (results) {
        hydrateCatalog(results[1], results[2], null, results[3]);
      })
      .catch(function (err) {
        if (window.CAMPGEAR_DATA) {
          hydrateCatalog(
            window.CAMPGEAR_DATA.brands,
            window.CAMPGEAR_DATA.products,
            window.CAMPGEAR_DATA.site,
            window.CAMPGEAR_DATA.sponsors
          );
          return;
        }
        setStatus(
          "Load failed: " +
            err.message +
            ". Run python3 -m http.server 8080 and open http://localhost:8080.",
          true
        );
      });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  bindOutboundTracking();

  function boot() {
    injectNavSearch();
    readSearchFromUrl();
    var page = document.body.getAttribute("data-page") || "home";
    if (page === "home") {
      loadSite();
      ensureCatalogForSearch();
    } else if (page === "category" || page === "furniture") {
      loadCatalog();
    }
  }

  loadBaiduPush();
  loadAnalytics().then(boot);
})();
