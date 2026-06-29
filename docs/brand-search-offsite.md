# 品牌搜索 — 站外引用指南

站内代码已配置 `brand.sameAs`（见 [`data/seo.json`](../data/seo.json)）。完成以下站外动作后，将新 URL 追加到 `sameAs` 并运行 `python3 scripts/build_sitemap.py`。

## GitHub（必做）

1. 打开 https://github.com/guanxu0813-sys/my_camping_website/settings  
2. **General → Website** 填：`https://www.campgearcompare.com`  
3. **Description** 示例：`CampGear Compare — side-by-side camping gear spec comparisons (campgearcompare.com)`  
4. 根目录 [README.md](../README.md) 已含品牌名与正式链接（提交后生效）

`sameAs` 已包含本仓库 URL。

## 可选渠道（择 1–2 个即可）

| 渠道 | 建议动作 | 回填 sameAs |
|------|----------|-------------|
| Product Hunt / Indie Hackers | 发布工具介绍帖 | 帖子 URL |
| Reddit / 露营论坛 | 在相关讨论中自然提及（非 spam） | — |
| Twitter/X | 简介放 campgearcompare.com | 主页 URL |
| 小红书 / YouTube | 30 秒对比表演示 | 主页 URL |

## 原则

- 锚文本混合：`CampGear Compare`、`campgearcompare.com`、裸 URL  
- 优先 1–3 个高质量引用，避免购买外链或群发  
- 每新增一个 `sameAs` URL，重新运行 SEO 构建并部署

## 部署后

按 [brand-search-indexing-checklist.md](./brand-search-indexing-checklist.md) 触发 Google / Baidu Indexing workflow。
