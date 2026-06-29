# 品牌 SEO — 补全收录操作清单

部署品牌信号相关代码后，按顺序完成以下步骤（约 30 分钟）。

## Google Search Console

资源 URL 必须为 **`https://www.campgearcompare.com`**（带 www）。

1. **网址检查** → 对以下 URL 逐个 **测试实际 URL** → **请求编入索引**（若显示尚未编入索引）：
   - `https://www.campgearcompare.com/tarp.html`
   - `https://www.campgearcompare.com/sleeping-bag.html`
   - `https://www.campgearcompare.com/furniture.html`

2. **不必**重复提交 sitemap（已提交且状态正常即可）。

3. GitHub → **Actions** → **Submit URLs to Google Indexing API** → **Run workflow**  
   日志应出现 6 行 `OK https://www.campgearcompare.com/...`

4. 验收：`site:www.campgearcompare.com` 结果数从 3 增至 **6**。

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
