# 搜索引擎收录提交说明

适用站点：CampGear Compare
最后更新：2026-07-28

## Google：使用 sitemap，不使用 Indexing API

Google 官方 Indexing API 仅支持包含 `JobPosting`，或嵌入
`VideoObject` 的 `BroadcastEvent` 页面。CampGear Compare 的装备、品牌和
指南页不属于支持范围，因此仓库不再向该 API 提交普通页面。

官方说明：
https://developers.google.com/search/apis/indexing-api/v3/using-api

Google 收录流程：

1. 部署后确认 `https://www.campgearcompare.com/sitemap.xml` 返回 200。
2. 在 Search Console 的“站点地图”提交一次 `sitemap.xml`。
3. 每周记录 `sitemap-core.xml`、`sitemap-brands.xml` 和
   `sitemap-products.xml` 的发现与收录数量。
4. URL Inspection 仅用于抽查重要新页面或诊断异常，不进行批量提交。
5. 新页面依靠 sitemap、主导航、hub 和正文内链被发现。

记录模板：[`gsc-indexing-log.csv`](./gsc-indexing-log.csv)

## Bing 和参与 IndexNow 的搜索引擎

仓库提供：

- 根目录验证文件：`indexnow-key.txt`
- 提交脚本：`scripts/submit_indexnow.py`
- GitHub Actions：`.github/workflows/submit-indexnow.yml`

Push 到 `main` 后，workflow 根据本次 Git 变更仅提交新增、更新或删除的
公开 HTML URL。不会把整个 872 URL 目录在每次部署时重复提交。

本地预览：

```bash
python3 scripts/submit_indexnow.py \
  --changed-file guides/naturehike-cloud-up-models-compared.html \
  --dry-run
```

首次接入或需要全量刷新时：

```bash
python3 scripts/submit_indexnow.py --all --dry-run
python3 scripts/submit_indexnow.py --all
```

`200` 或 `202` 仅表示搜索引擎接受通知，不代表保证收录。sitemap 始终是
全量发现的基础。

## 一次性人工配置

1. 登录 Google Search Console，确认 sitemap 状态为“成功”。
2. 登录 Bing Webmaster Tools，可从 GSC 导入站点。
3. 在 Bing 提交同一个 `sitemap.xml`。
4. 打开 Bing 的 IndexNow 报告，确认 workflow 部署后出现接收记录。

这些步骤需要站点所有者登录，代码无法代替账户授权。
