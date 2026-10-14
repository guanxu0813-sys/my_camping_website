(function () {
  var dataNode = document.getElementById("data-explorer-data");
  var categoryInput = document.getElementById("data-explorer-category");
  var weightInput = document.getElementById("data-explorer-weight");
  var priceInput = document.getElementById("data-explorer-price");
  var queryInput = document.getElementById("data-explorer-query");
  var status = document.getElementById("data-explorer-status");
  var chart = document.getElementById("data-explorer-chart");
  var results = document.getElementById("data-explorer-results");
  if (!dataNode || !categoryInput || !weightInput || !priceInput || !queryInput || !status || !chart || !results) return;

  var records;
  try {
    records = JSON.parse(dataNode.textContent || "[]");
  } catch (error) {
    status.textContent = "The explorer data could not be loaded.";
    return;
  }

  var categoryLabels = {
    tent: "Tent",
    tarp: "Tarp",
    "sleeping-bag": "Sleeping bag",
    "sleeping-pad": "Sleeping pad",
    stove: "Stove",
  };
  var colors = {
    tent: "#28634d",
    tarp: "#c85c3f",
    "sleeping-bag": "#2f6f91",
    "sleeping-pad": "#8a6b2f",
    stove: "#7a4d78",
  };
  var tracked = false;

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function numericLimit(input) {
    var value = Number(input.value);
    return input.value !== "" && Number.isFinite(value) && value >= 0 ? value : null;
  }

  function filteredRecords() {
    var category = categoryInput.value;
    var maxWeight = numericLimit(weightInput);
    var maxPrice = numericLimit(priceInput);
    var query = queryInput.value.trim().toLowerCase();
    return records.filter(function (record) {
      if (category !== "all" && record.category !== category) return false;
      if (maxWeight !== null && record.weight > maxWeight) return false;
      if (maxPrice !== null && (record.usdPrice === null || record.usdPrice > maxPrice)) return false;
      if (query && (record.brand + " " + record.model).toLowerCase().indexOf(query) === -1) return false;
      return true;
    });
  }

  function renderChart(filtered) {
    var priced = filtered.filter(function (record) {
      return record.usdPrice !== null && record.weight > 0;
    });
    if (!priced.length) {
      chart.innerHTML = '<p class="data-explorer__empty">No USD-priced products match these filters.</p>';
      return;
    }

    var width = 900;
    var height = 360;
    var left = 62;
    var right = 20;
    var top = 20;
    var bottom = 48;
    var maxWeight = Math.max.apply(null, priced.map(function (record) { return record.weight; }));
    var maxPrice = Math.max.apply(null, priced.map(function (record) { return record.usdPrice; }));
    var weightCeiling = Math.max(1, Math.ceil(maxWeight));
    var priceCeiling = Math.max(100, Math.ceil(maxPrice / 100) * 100);
    var plotWidth = width - left - right;
    var plotHeight = height - top - bottom;

    var dots = priced.slice(0, 400).map(function (record) {
      var x = left + (record.weight / weightCeiling) * plotWidth;
      var y = top + plotHeight - (record.usdPrice / priceCeiling) * plotHeight;
      var label = record.brand + " " + record.model + ": " + record.weight.toFixed(2) + " kg, $" + record.usdPrice.toFixed(2);
      return '<a href="' + escapeHtml(record.url) + '" aria-label="' + escapeHtml(label) + '">' +
        '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="4" fill="' +
        (colors[record.category] || "#28634d") + '"><title>' + escapeHtml(label) + '</title></circle></a>';
    }).join("");

    chart.innerHTML = '<svg viewBox="0 0 ' + width + " " + height + '" aria-hidden="true" focusable="false">' +
      '<line class="data-explorer__axis" x1="' + left + '" y1="' + (top + plotHeight) + '" x2="' + (left + plotWidth) + '" y2="' + (top + plotHeight) + '" />' +
      '<line class="data-explorer__axis" x1="' + left + '" y1="' + top + '" x2="' + left + '" y2="' + (top + plotHeight) + '" />' +
      '<text x="' + (left + plotWidth / 2) + '" y="348" text-anchor="middle">Weight (kg)</text>' +
      '<text x="16" y="' + (top + plotHeight / 2) + '" text-anchor="middle" transform="rotate(-90 16 ' + (top + plotHeight / 2) + ')">USD price</text>' +
      '<text x="' + left + '" y="335">0</text>' +
      '<text x="' + (left + plotWidth) + '" y="335" text-anchor="end">' + weightCeiling + '</text>' +
      '<text x="52" y="' + (top + plotHeight) + '" text-anchor="end">$0</text>' +
      '<text x="52" y="' + (top + 5) + '" text-anchor="end">$' + priceCeiling + '</text>' + dots + '</svg>';
  }

  function renderTable(filtered) {
    var sorted = filtered.slice().sort(function (a, b) {
      if (a.weight !== b.weight) return a.weight - b.weight;
      return (a.usdPrice === null ? Infinity : a.usdPrice) - (b.usdPrice === null ? Infinity : b.usdPrice);
    });
    results.innerHTML = sorted.slice(0, 30).map(function (record) {
      return "<tr><td><a href=\"" + escapeHtml(record.url) + "\"><strong>" + escapeHtml(record.brand) + "</strong> " +
        escapeHtml(record.model) + "</a></td><td>" + escapeHtml(categoryLabels[record.category] || record.category) +
        "</td><td>" + record.weight.toFixed(2) + " kg</td><td>" +
        (record.usdPrice === null ? "Not USD-priced" : "$" + record.usdPrice.toFixed(2)) + "</td></tr>";
    }).join("");
    if (!sorted.length) {
      results.innerHTML = '<tr><td colspan="4">No products match these filters.</td></tr>';
    }
  }

  function render() {
    var filtered = filteredRecords();
    status.textContent = filtered.length + " of " + records.length + " products";
    renderChart(filtered);
    renderTable(filtered);
  }

  function onFilterChange() {
    render();
    if (!tracked && typeof window.gtag === "function") {
      tracked = true;
      window.gtag("event", "data_explorer_filter", {
        category: categoryInput.value,
      });
    }
  }

  [categoryInput, weightInput, priceInput, queryInput].forEach(function (input) {
    input.addEventListener(input.tagName === "SELECT" ? "change" : "input", onFilterChange);
  });
  render();
})();
