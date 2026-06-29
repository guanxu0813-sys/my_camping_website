# 品牌搜索监控 — 每周检查清单

约 10 分钟 / 周。记录日期与结果，便于观察趋势。

## Google

在 Google 搜索：

```
site:www.campgearcompare.com
campgearcompare.com
campgearcompare
"CampGear Compare"
```

| 查询 | 本周结果 | 备注 |
|------|----------|------|
| site: | ___ 条 | 目标 ≥ 6 |
| campgearcompare.com | 官网是否前 3 | |
| campgearcompare | 官网是否出现 | |
| "CampGear Compare" | 官网是否首位 | |

**GSC**（[Search Console](https://search.google.com/search-console)）

- **效果 → 搜索查询**：筛选含 `campgear` 的查询，记录展示 / 点击 / 平均排名
- **网址检查**：对仍未收录的品类页再查一次

## 百度

```
site:campgearcompare.com
campgearcompare
CampGear Compare
露营装备对比
```

| 查询 | 本周结果 | 备注 |
|------|----------|------|
| site: | ___ 条 | |
| campgearcompare | | |

**百度搜索资源平台**：索引量、抓取频次。

## Plausible

- 直接访问 `/` 的流量（品牌词 type-in）是否上升

## 预期里程碑

| 里程碑 | Google | 百度 |
|--------|--------|------|
| `campgearcompare.com` 搜到官网 | 1–3 周 | 2–6 站 |
| `campgearcompare` 进前 3 | 3–8 周 | 4–12 周 |
| `CampGear Compare` 首位 | 4–12 周 | 视中文内容 |

## 站外引用维护

新增社交 / 论坛主页后，把 URL 填入 [`data/seo.json`](../data/seo.json) → `brand.sameAs`，运行：

```bash
python3 scripts/build_sitemap.py
```

GitHub 仓库 About 字段应包含：**Website** = `https://www.campgearcompare.com`，**Description** 含 CampGear Compare。
