# 产品数据维护说明

本站使用 JSON 作为产品「数据库」，由 [`script.js`](../script.js) 在浏览器中加载并渲染对比表与详情卡。

## 文件说明

| 文件 | 用途 |
|------|------|
| [`brands.json`](brands.json) | 品牌列表，`id` 供产品引用 |
| [`products.json`](products.json) | 全部产品参数与展示配置 |

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
npx serve .
```

然后打开 `http://localhost:3000`（端口以终端输出为准）。不要用 `file://` 直接打开 `index.html`，否则 `fetch` 会失败。

## 可选：表格同步

若团队用 Google 表格维护，可增加 GitHub Action 将表格导出为 `brands.json` / `products.json`。参见 [`.github/workflows/validate-catalog.yml`](../.github/workflows/validate-catalog.yml) 中的 JSON 校验步骤；完整表格同步需自行配置表格 API 与导出脚本。
