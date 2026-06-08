(function () {
  var header = document.querySelector(".site-header");
  var navHeight = header ? header.offsetHeight : 68;
  var filter = "all";
  var brands = [];
  var products = [];
  var brandMap = {};

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

  function formatPrice(min, max) {
    if (min == null && max == null) return "—";
    if (min != null && max != null) {
      return min.toLocaleString("zh-CN") + "–" + max.toLocaleString("zh-CN") + " 元";
    }
    return (min != null ? min : max).toLocaleString("zh-CN") + " 元";
  }

  function formatWeight(product) {
    if (product.weightDisplay) return product.weightDisplay;
    if (product.weightRange) return product.weightRange;
    if (product.weightKg != null) return "约 " + product.weightKg + " kg";
    return "—";
  }

  function formatScenarios(scenarios) {
    if (!scenarios || !scenarios.length) return "—";
    return scenarios.join("、");
  }

  function brandName(brandId) {
    var b = brandMap[brandId];
    return b ? b.name : brandId;
  }

  function fullModelName(product) {
    return brandName(product.brandId) + " " + product.model;
  }

  function applyFilter() {
    document.querySelectorAll("[data-compare-group]").forEach(function (el) {
      var group = el.getAttribute("data-compare-group");
      var show = filter === "all" || filter === group;
      el.classList.toggle("is-hidden", !show);
    });
  }

  document.querySelectorAll(".filter-chip").forEach(function (btn) {
    btn.addEventListener("click", function () {
      filter = btn.getAttribute("data-filter") || "all";
      document.querySelectorAll(".filter-chip").forEach(function (b) {
        b.classList.toggle("is-active", b === btn);
      });
      applyFilter();
    });
  });

  function renderTentTable(rows) {
    var body = rows
      .map(function (p) {
        return (
          "<tr>" +
          "<td>" + escapeHtml(brandName(p.brandId)) + "</td>" +
          "<td>" + escapeHtml(p.model) + "</td>" +
          "<td>" + escapeHtml(p.structure || "—") + "</td>" +
          "<td>" + escapeHtml(formatWeight(p)) + "</td>" +
          "<td>" + escapeHtml(p.capacity || "—") + "</td>" +
          "<td>" + escapeHtml(p.fabric || "—") + "</td>" +
          "<td>" + escapeHtml(formatPrice(p.priceMin, p.priceMax)) + "</td>" +
          "<td>" + escapeHtml(formatScenarios(p.scenarios)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div id="tables" class="compare-block" data-compare-group="tent">' +
      '<h2 class="compare-block__title">帐篷参数总表</h2>' +
      '<div class="table-wrap"><table class="compare-table">' +
      "<thead><tr>" +
      "<th scope=\"col\">品牌</th><th scope=\"col\">型号</th><th scope=\"col\">结构</th>" +
      "<th scope=\"col\">重量</th><th scope=\"col\">人数</th><th scope=\"col\">面料 / 防水</th>" +
      "<th scope=\"col\">参考价</th><th scope=\"col\">适用场景</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderTarpTable(rows) {
    var body = rows
      .map(function (p) {
        return (
          "<tr>" +
          "<td>" + escapeHtml(brandName(p.brandId)) + "</td>" +
          "<td>" + escapeHtml(p.model) + "</td>" +
          "<td>" + escapeHtml(p.tarpType || "—") + "</td>" +
          "<td>" + escapeHtml(formatWeight(p)) + "</td>" +
          "<td>" + escapeHtml(p.size || "—") + "</td>" +
          "<td>" + escapeHtml(formatPrice(p.priceMin, p.priceMax)) + "</td>" +
          "<td>" + escapeHtml(formatScenarios(p.scenarios)) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="tarp">' +
      '<h2 class="compare-block__title">天幕参数总表</h2>' +
      '<div class="table-wrap"><table class="compare-table">' +
      "<thead><tr>" +
      "<th scope=\"col\">品牌</th><th scope=\"col\">型号</th><th scope=\"col\">类型</th>" +
      "<th scope=\"col\">重量</th><th scope=\"col\">尺寸</th><th scope=\"col\">参考价</th><th scope=\"col\">适用场景</th>" +
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
          "<tr>" +
          "<td>" + escapeHtml(fullModelName(p)) + "</td>" +
          "<td>" + escapeHtml(formatPrice(p.priceMin, p.priceMax)) + "</td>" +
          "<td>" + escapeHtml(p.pros) + "</td>" +
          "<td>" + escapeHtml(p.cons) + "</td>" +
          "</tr>"
        );
      })
      .join("");

    return (
      '<div class="compare-block" data-compare-group="tent">' +
      '<h2 class="compare-block__title">同价位徒步帐 · 优缺点对比</h2>' +
      '<div class="table-wrap"><table class="compare-table compare-table--pros">' +
      "<thead><tr>" +
      "<th scope=\"col\">品牌型号</th><th scope=\"col\">参考价格</th>" +
      "<th scope=\"col\">核心优势</th><th scope=\"col\">相对短板</th>" +
      "</tr></thead><tbody>" +
      body +
      "</tbody></table></div></div>"
    );
  }

  function renderProductCard(product) {
    var specs = [];
    if (product.category === "tent") {
      specs.push({ label: "结构", value: product.detailStructure || product.structure || "—" });
      specs.push({ label: "重量", value: formatWeight(product) });
    } else {
      specs.push({ label: "类型", value: product.detailStructure || product.tarpType || "—" });
      specs.push({ label: "重量", value: formatWeight(product) });
    }
    specs.push({ label: "参考价", value: formatPrice(product.priceMin, product.priceMax) });
    specs.push({
      label: "特点",
      value: (product.highlights && product.highlights[0]) || "—",
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

    return (
      '<article class="product-card">' +
      '<div class="product-card__media">' + img + "</div>" +
      '<div class="product-card__body">' +
      '<span class="product-card__brand">' + escapeHtml(brandName(product.brandId)) + "</span>" +
      "<h3 class=\"product-card__model\">" + escapeHtml(product.model) + "</h3>" +
      '<dl class="product-spec">' + specHtml + "</dl>" +
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

  function renderCatalog() {
    var tents = products.filter(function (p) {
      return p.category === "tent" && p.inSummaryTable !== false;
    });
    var tarps = products.filter(function (p) {
      return p.category === "tarp" && p.inSummaryTable !== false;
    });
    var prosRows = products.filter(function (p) {
      return p.pros && p.cons;
    });

    var root = document.getElementById("compare-root");
    if (!root) return;

    root.innerHTML =
      renderTentTable(tents) +
      renderTarpTable(tarps) +
      renderProsTable(prosRows) +
      renderDetailSection("tent", "tents", "帐篷 · 型号详情", "配图来自 Wikimedia Commons；部分为同结构类型示意。") +
      renderDetailSection("tarp", "tarps", "天幕 · 型号详情", "天幕侧重遮阳、防雨与营地客厅功能，常与帐篷组合使用。");

    root.hidden = false;
    applyFilter();
  }

  function setStatus(message, isError) {
    var el = document.getElementById("catalog-status");
    if (!el) return;
    el.textContent = message;
    el.classList.toggle("catalog-status--error", !!isError);
  }

  function loadCatalog() {
    return Promise.all([
      fetch("data/brands.json").then(function (r) {
        if (!r.ok) throw new Error("无法加载 brands.json");
        return r.json();
      }),
      fetch("data/products.json").then(function (r) {
        if (!r.ok) throw new Error("无法加载 products.json");
        return r.json();
      }),
    ])
      .then(function (results) {
        brands = results[0];
        products = results[1];
        brandMap = {};
        brands.forEach(function (b) {
          brandMap[b.id] = b;
        });
        renderCatalog();
        setStatus("");
        var statusEl = document.getElementById("catalog-status");
        if (statusEl) statusEl.hidden = true;
      })
      .catch(function (err) {
        setStatus(
          "加载失败：" + err.message + "。请通过本地服务器访问（如 npx serve），勿直接用 file:// 打开。",
          true
        );
      });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  loadCatalog();
})();
