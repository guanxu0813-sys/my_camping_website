# 品牌 SEO — 补全收录操作清单

部署品牌信号相关代码后，按顺序完成以下步骤（约 30 分钟）。

## Google Search Console

资源 URL 必须为 **`https://www.campgearcompare.com`**（带 www）。

1. **网址检查** → 对以下代表性 URL **测试实际 URL**；仅在排查重要页面时使用“请求编入索引”：
   - `https://www.campgearcompare.com/tarp.html`
   - `https://www.campgearcompare.com/sleeping-bag.html`
   - `https://www.campgearcompare.com/furniture.html`

2. 确认 `sitemap.xml` 已提交且状态正常，不必在每次发布后重复提交。
3. 不向 Google Indexing API 提交普通装备页；该 API 官方仅支持招聘和直播页面。
4. 验收以 GSC 的有效收录页与搜索点击为准，不使用 `site:` 结果数作为精确指标。

## Bing Webmaster Tools

1. 从 GSC 导入站点并提交 `sitemap.xml`。
2. Push 部署后检查 **Submit changed URLs to IndexNow** workflow。
3. 在 Bing 的 IndexNow 报告确认已接收 URL。

## 百度搜索资源平台

详见 [baidu-setup-campgearcompare.md](./baidu-setup-campgearcompare.md)。

1. 确认站点已验证（`baidu_verify_*.html` 可访问）。
2. 确认已提交 `sitemap.xml`。
3. GitHub → **Actions** → **Submit URLs to Baidu indexing API** → **Run workflow**（需 `BAIDU_PUSH_TOKEN`）。
4. 验收：平台「索引量」> 0，或 `site:campgearcompare.com` 有结果。

## 部署

```bash
git push origin main
```

Vercel 部署完成后，再执行上述 Indexing / Baidu workflow。
