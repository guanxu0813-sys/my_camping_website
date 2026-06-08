# 产品数据维护说明

本站使用 JSON 作为产品「数据库」，由 [`script.js`](../script.js) 在浏览器中加载并渲染对比表与详情卡。

**前端只读取 `data/official/{brandId}/products.json` 作为展示列表**（品牌目录见 `data/official/index.json`；`data/brands.json` 仅用于品牌名称）。

- [`index.html`](../index.html) — 首页（按品类导航）
- [`tent.html`](../tent.html)、[`tarp.html`](../tarp.html) — 品类页（参数对比 + 产品介绍）
- [`furniture.html`](../furniture.html) 等 — 筹备中品类占位页

`data/products.json` 为旧版手工/合并展示库，页面不再使用；若需导出到展示库仍可用 `merge_official.py`。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`brands.json`](brands.json) | 品牌列表，`id` 供产品引用 |
| [`products.json`](products.json) | 全部产品参数与展示配置 |
| [`site.json`](site.json) | 首页头图文案与配图 URL（Wikimedia 等外链） |
| [`catalog.js`](catalog.js) | 由 `scripts/build_catalog.py` 自动生成，供 `file://` 双击预览 |
| [`official/`](official/) | 品牌官网抓取原始库（按品牌分子目录，默认 `status: draft`） |
| [`products.schema.json`](products.schema.json) | 官网产品 JSON 字段说明（JSON Schema） |

修改 JSON 后请运行：

```bash
python3 scripts/build_catalog.py
```

## 官网抓取与合并（挪客 / Snow Peak 等）

品牌官网（Shopify 商城）可通过脚本抓取产品图、型号、价格与介绍，写入 `data/official/{brandId}/products.json`。

**合规提示：** 产品图与文案通常受版权保护；请仅用于个人/非商用参数对比，保留 `sourceUrl` 溯源，合并前人工审核。抓取脚本限速运行，**不会**在 CI 中自动执行。

### 依赖（可选）

```bash
pip install -r requirements-scrape.txt
```

核心抓取仅依赖 Python 标准库 + `scripts/scrape/config.json`；`Pillow` 用于图片转 WebP。

### 1. 抓取官网目录

```bash
python3 scripts/scrape/scrape_brand.py naturehike
python3 scripts/scrape/scrape_brand.py snow-peak
```

配置见 [`scripts/scrape/config.json`](../scripts/scrape/config.json)（或 `config.yaml`）。

### 2. 人工审核

在 `data/official/{brandId}/products.json` 中将确认无误的条目改为：

```json
"status": "verified"
```

### 3. 下载主图到本地（可选）

```bash
python3 scripts/scrape/download_images.py naturehike --status verified
```

图片保存至 `assets/products/{brandId}/{id}.webp`，并写回 `imageLocal`。

### 4. 合并到对比站展示库

```bash
python3 scripts/scrape/merge_official.py naturehike \
  --ids naturehike-mongartm-pro-2-person-ultralight-backpacking-tent \
  --target-id naturehike-yunshang-pro

python3 scripts/build_catalog.py
```

`--target-id` 用于更新已有 `products.json` 条目；省略则按官方 `id` 新增。

### 5. 校验

```bash
python3 scripts/validate_official.py
```

### 官网产品字段

| 字段 | 说明 |
|------|------|
| `category` | `tent` / `tarp` 等 |
| `model` / `description` | 官网型号与介绍 |
| `priceMin` / `priceMax` / `currency` | 官网标价（美元等） |
| `imageUrl` / `imageLocal` | 外链主图 / 本地备份 |
| `sourceUrl` | 产品详情页 |
| `status` | `draft` → `verified` → `merged` |

定期更新：重新运行 `scrape_brand.py`，对比 `scrapedAt` 与价格变动后再审核合并。


本地预览（推荐）：

```bash
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 新增品牌

在 `brands.json` 末尾追加（`id` 全局唯一，建议小写英文连字符）：

```json
{
  "id": "decathlon",
  "name": "迪卡侬",
  "nameEn": "Decathlon",
  "country": "FR"
}
```

## 新增帐篷产品

在 `products.json` 追加一条记录，必填字段示例：

```json
{
  "id": "decathlon-quechua-2",
  "brandId": "decathlon",
  "category": "tent",
  "model": "Quechua 2 Seconds",
  "structure": "穹顶",
  "weightKg": 2.1,
  "capacity": "2",
  "fabric": "涤纶 · PU2000",
  "priceMin": 299,
  "priceMax": 499,
  "scenarios": ["公园露营", "入门"],
  "highlights": ["速开、性价比高"],
  "detailStructure": "穹顶 · 双人",
  "imageUrl": "https://…",
  "imageAlt": "帐篷实景说明",
  "inSummaryTable": true,
  "inDetailCards": true
}
```

## 新增天幕产品

`category` 设为 `"tarp"`，使用 `tarpType`、`weightRange`、`size` 代替帐篷字段：

```json
{
  "id": "example-hex-tarp",
  "brandId": "naturehike",
  "category": "tarp",
  "model": "六角天幕 4×4",
  "tarpType": "六角涂硅",
  "weightRange": "约 0.8 kg",
  "size": "4×4 m",
  "priceMin": 200,
  "priceMax": 350,
  "scenarios": ["精致露营"],
  "highlights": ["多挂点客厅模式"],
  "detailStructure": "六角涂硅",
  "imageUrl": "https://…",
  "imageAlt": "天幕实景",
  "inSummaryTable": true,
  "inDetailCards": true
}
```

## 仅出现在「优缺点对比表」

若产品只需参与同价位对比、不出现在总表与详情卡，设置：

```json
"inSummaryTable": false,
"inDetailCards": false,
"pros": "核心优势描述",
"cons": "相对短板描述",
"priceMin": 800,
"priceMax": 1200
```

## 字段速查

| 字段 | 说明 |
|------|------|
| `weightKg` | 数值重量（公斤），用于自动生成「约 X kg」 |
| `weightDisplay` | 覆盖重量展示，如 `约 8 kg+` |
| `weightRange` | 天幕重量区间文案 |
| `priceMin` / `priceMax` | 参考价区间（元，数字） |
| `pros` / `cons` | 同时填写则进入优缺点对比表 |
| `inSummaryTable` | 默认 `true`，是否出现在参数总表 |
| `inDetailCards` | 默认 `true`，是否出现在详情卡片 |

## 本地预览

JSON 需通过 HTTP 访问，推荐：

```bash
python3 -m http.server 5173
```

然后打开 `http://localhost:5173`。不要用 `file://` 直接打开 `index.html`，否则 `fetch` 会失败。

如果你确实想双击 `index.html` 用 `file://` 预览（无本地服务器），请先运行：

```bash
python3 scripts/build_catalog.py
```

这会生成 `data/catalog.js`，页面会自动回退使用它来渲染数据。

## 可选：表格同步

若团队用 Google 表格维护，可增加 GitHub Action 将表格导出为 `brands.json` / `products.json`。参见 [`.github/workflows/validate-catalog.yml`](../.github/workflows/validate-catalog.yml) 中的 JSON 校验步骤；完整表格同步需自行配置表格 API 与导出脚本。
