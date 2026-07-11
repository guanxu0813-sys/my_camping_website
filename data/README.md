# 产品数据维护说明

本站使用 JSON 作为产品「数据库」，由 [`script.js`](../script.js) 在浏览器中加载并渲染对比表与详情卡。

**展示数据源：`data/official/{brandId}/products.json`**（品牌目录见 `data/official/index.json`；`data/brands.json` 仅用于品牌名称）。

- [`index.html`](../index.html) — 首页（按品类导航）
- [`tent.html`](../tent.html)、[`tarp.html`](../tarp.html) — 品类页（参数对比 + 产品介绍）
- [`furniture.html`](../furniture.html) 等 — 筹备中品类占位页

`data/products.json` 为**旧版遗留库**，页面不再读取；仅当需要导出到外部格式时可选用 [`merge_official.py`](../scripts/scrape/merge_official.py)。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`brands.json`](brands.json) | 品牌列表，`id` 供产品引用 |
| [`products.json`](products.json) | 遗留手工库（页面不读） |
| [`site.json`](site.json) | 首页头图文案与配图 URL |
| [`analytics.json`](analytics.json) | Plausible 分析配置（`enabled` + `plausibleDomain`） |
| [`seo.json`](seo.json) | 站点 URL（`siteUrl`），用于 sitemap / canonical；换正式域名后更新并运行 `scripts/build_sitemap.py` |
| [`catalog.js`](catalog.js) | 由 `scripts/build_catalog.py` 自动生成，供 `file://` 双击预览 |
| [`official/`](official/) | 官网抓取库（按品牌分子目录） |
| [`products.schema.json`](products.schema.json) | 官网产品 JSON 字段说明（JSON Schema） |

修改 official JSON 后请运行：

```bash
python3 scripts/build_catalog.py
python3 scripts/build_sitemap.py
```

其中 `build_sitemap.py` 会同步 `robots.txt`、`sitemap.xml`、HTML SEO 区块，并重建 `products/` 与 `brands/` 下的静态长尾 SEO 页面。

## 官网抓取工作流

品牌官网（Shopify 商城）通过脚本抓取产品图、型号、价格与介绍，写入 `data/official/{brandId}/products.json`，**即站点展示源**。

**合规提示：** 产品图与文案通常受版权保护。站点用于参数对比与联盟导流（见 [`legal.html`](../legal.html)），保留 `sourceUrl` 溯源。**默认仅外链展示品牌 CDN 图片**（`imageUrl`）；本地 `imageLocal` 仅在 `imageLicense: "brand-approved"` 时使用。抓取脚本限速运行，**不会**在 CI 中自动执行。

### 图片策略（商业化）

| 策略 | 说明 |
|------|------|
| 默认 | 前端优先 `imageUrl`（品牌 CDN 外链），不复制到 GitHub Pages |
| 本地图 | 仅当产品有 `imageLicense: "brand-approved"` 时使用 `imageLocal` |
| 批量下载 | `download_images.py` 需品牌书面授权后再运行；无授权时不要本地化图片 |
| 展示 | 对比表缩略图与 Modal 显示 `© Brand · Image from official site` 标注 |

### 分析埋点

配置 [`analytics.json`](analytics.json)：

```json
{
  "provider": "plausible",
  "enabled": true,
  "plausibleDomain": "your-domain.com"
}
```

本地开发时（`localhost`）事件会输出到浏览器控制台 `[CampGear analytics]`。上线前将 `enabled` 设为 `true` 并填入 Plausible 域名。

### SEO（软启动）

- 站点 URL 与 sitemap 页面列表：[`seo.json`](seo.json)
- 生成 `robots.txt` / `sitemap.xml`：

```bash
python3 scripts/build_sitemap.py
```

换正式域名时：更新 `seo.json` 的 `siteUrl`，运行：

```bash
python3 scripts/sync_site_url.py
```

（同步各 HTML canonical、`sitemap.xml`、`robots.txt` 及 docs 中的站点链接。）完整 Vercel / DNS 步骤见 [`docs/custom-domain-setup.md`](../docs/custom-domain-setup.md)。

百度搜索收录（与 Google 独立）：[`docs/baidu-setup-campgearcompare.md`](../docs/baidu-setup-campgearcompare.md)。验证通过后配置 `BAIDU_PUSH_TOKEN` 可自动 API 推送。

### 品牌赞助位

活动配置 [`sponsors.json`](sponsors.json)（不必改 554 条产品 JSON）：

```json
{
  "campaigns": [
    {
      "productId": "snow-peak-amenity-dome-m-ivory",
      "active": true,
      "tier": "table-featured",
      "label": "Sponsored",
      "expiresAt": "2026-12-31",
      "campaignId": "snow-peak-q3-tent"
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `productId` | 对应 official 产品 `id` |
| `active` | `true` 时生效 |
| `tier` | `table-featured`（对比表置顶 + Modal 标注）或 `modal-featured` |
| `expiresAt` | `YYYY-MM-DD`，过期自动失效 |
| `campaignId` | 活动 ID，便于对账 |

校验：

```bash
python3 scripts/validate_sponsors.py
```

也可在产品 JSON 内嵌 `sponsor` 对象（见 `products.schema.json`）；`sponsors.json` 会覆盖同 `productId` 的配置。

### 依赖

```bash
pip install -r requirements-scrape.txt
```

核心依赖：`PyYAML`（读取 [`scripts/scrape/config.yaml`](../scripts/scrape/config.yaml)）、`certifi`（macOS SSL 证书）、`beautifulsoup4`（HTML 解析）；`Pillow` 用于图片转 WebP。

### 环境与网络

在 macOS 或代理环境下抓取若出现 SSL / 连接错误，可尝试：

```bash
# 取消代理后抓取
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
  python3 scripts/scrape/scrape_brand.py naturehike

# 或批量抓取全部品牌
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
  python3 scripts/scrape/scrape_all.py --continue
```

- `CERTIFICATE_VERIFY_FAILED`：确认已安装 `certifi`（`pip install certifi`）
- 部分站点需浏览器 User-Agent，已在 `config.yaml` 中为对应品牌配置 `useBrowserUserAgent: true`

### 1. 抓取官网目录

单品牌：

```bash
python3 scripts/scrape/scrape_brand.py naturehike
python3 scripts/scrape/scrape_brand.py snow-peak
```

全部品牌（`--continue` 在某个品牌失败后继续）：

```bash
python3 scripts/scrape/scrape_all.py
python3 scripts/scrape/scrape_all.py --continue naturehike snow-peak
```

配置仅维护一份：[`scripts/scrape/config.yaml`](../scripts/scrape/config.yaml)。

**增量合并：** 重抓时按 `id` 合并，自动保留 `status`、`published`、`imageLocal`、人工编辑字段；某 collection 失败或 404 时保留该品类旧数据。

### 2. 审核与上架

新抓取条目默认为 `"status": "draft"`、`"published": false`，**不会出现在站点**。

上架方式（二选一）：

```json
"status": "verified"
```

或：

```json
"published": true
```

迁移前已存在的 draft 条目（无 `published` 字段）仍可见，直至你重新抓取该条目。

### 3. 下载主图到本地（可选）

```bash
python3 scripts/scrape/download_images.py naturehike --status verified
```

图片保存至 `assets/products/{brandId}/{id}.webp`，并写回 `imageLocal`（重抓时会保留）。

### 4. 生成预览包

```bash
python3 scripts/build_catalog.py
```

`catalog.js` 与线上一致，仅包含已上架产品（`verified` / `merged` / `published: true` / 迁移前 legacy draft）。

### 5. 校验

```bash
python3 scripts/validate_official.py
```

### 遗留：合并到 products.json

页面不读 `products.json`。仅当需要导出到旧格式时：

```bash
python3 scripts/scrape/merge_official.py naturehike --include-verified
```

### 官网产品字段

| 字段 | 说明 |
|------|------|
| `category` | `tent` / `tarp` 等 |
| `model` / `description` | 官网型号与介绍 |
| `priceMin` / `priceMax` / `currency` | 官网标价 |
| `imageUrl` / `imageLocal` | 外链主图 / 本地备份 |
| `sourceUrl` | 产品详情页 |
| `status` | `draft` → `verified`（审核通过） |
| `published` | `true` 时上架展示（无需改 status） |

定期更新：重新运行 `scrape_brand.py` 或 `scrape_all.py`，对比 `scrapedAt` 与价格变动后再审核。

## 新增品牌

在 `brands.json` 末尾追加（`id` 全局唯一，建议小写英文连字符），并在 `data/official/index.json` 的 `brandIds` 中登记：

```json
{
  "id": "decathlon",
  "name": "迪卡侬",
  "nameEn": "Decathlon",
  "country": "FR"
}
```

在 [`scripts/scrape/config.yaml`](../scripts/scrape/config.yaml) 添加抓取配置后运行 `scrape_brand.py`。

## 手工新增产品（official 库）

在 `data/official/{brandId}/products.json` 追加条目，必填字段示例：

```json
{
  "id": "naturehike-example-tent",
  "brandId": "naturehike",
  "category": "tent",
  "model": "示例帐篷",
  "sourceUrl": "https://…",
  "sourceSite": "naturehike.com",
  "scrapedAt": "2026-06-11T00:00:00Z",
  "status": "verified",
  "published": true,
  "inSummaryTable": true,
  "inDetailCards": true
}
```

## 仅出现在「优缺点对比表」

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
| `weightKg` | 数值重量（公斤） |
| `weightDisplay` | 覆盖重量展示，如 `约 8 kg+` |
| `weightRange` | 天幕重量区间文案 |
| `priceMin` / `priceMax` | 参考价区间 |
| `pros` / `cons` | 同时填写则进入优缺点对比表 |
| `inSummaryTable` | 默认 `true`，是否出现在参数总表 |
| `inDetailCards` | 默认 `true`，是否出现在详情卡片 |
| `published` | 新抓取默认 `false`；`true` 即上架 |

## 本地预览

推荐 HTTP 服务：

```bash
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080
```

若用 `file://` 双击打开，须先运行 `python3 scripts/build_catalog.py` 生成 `catalog.js`。

## 可选：表格同步

若团队用 Google 表格维护，可增加 GitHub Action 将表格导出为 JSON。参见 [`.github/workflows/validate-catalog.yml`](../.github/workflows/validate-catalog.yml)。
