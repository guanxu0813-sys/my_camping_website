# Day 8：Naturehike 集群内部链接

- 日期：2026-10-26
- 状态：`COMPLETED`
- 范围：现有 Naturehike 指南、品牌页、分类品牌页和相关产品页

## 做了什么

把 5 篇已有 Naturehike 指南纳入同一套可维护的链接关系：

1. Cloud Up 系列对比
2. Giling Pro 1 vs Mongar Pro 1
3. Mongar Base 2 vs Base 3
4. Snowbird SP700 vs SP550
5. TuYe R5.8 vs R6.5 vs R8.8

每篇指南都增加了返回 Naturehike 品牌主页的自然入口。Naturehike 品牌主页列出全部 5 篇指南；帐篷、睡袋和睡垫品牌分类页分别只列出与本品类相关的 3、1、1 篇指南，避免把睡垫内容硬塞进帐篷页面。

同时把这种关系写进生成器：以后重新生成页面时，会按 `brand_id + category` 自动选择相关指南，不再依赖只针对 Naturehike 帐篷页的特例。

## 链接闭环

- 指南 -> 品牌主页：5/5。
- 品牌主页 -> 指南：5 条且无重复。
- 分类品牌页 -> 相关指南：帐篷 3 条、睡袋 1 条、睡垫 1 条。
- 指南 -> 产品详情：沿用每篇指南的完整规格链接。
- 产品详情 -> 指南：27/27 个相关主产品和同系列产品已有反向链接。

这样用户可以从产品进入对比指南，也可以从指南回到品牌或完整品类继续研究，不需要依赖浏览器后退。搜索引擎也能更清楚地识别 Naturehike 品牌、品类和对比内容之间的主题关系。

## 边界

- 没有新增指南、产品或 sitemap URL。
- 没有修改价格、重量、标题实验或联盟链接。
- 没有向 Day 4 的配件问题记录导流。
- 没有把无关指南加入分类品牌页。

## 验证

- `npm test`：分析事件与比较漏斗通过，14 条指南深链覆盖 4 个品类。
- `python3 scripts/test_growth_tools.py`：16/16 通过，新增 Naturehike 品牌与品类链接映射回归测试。
- `python3 scripts/validate_generated_site.py`：900 个 HTML、863 个唯一 sitemap URL，RSS 和内部链接有效。
- `python3 scripts/audit_structured_data.py`：10/10 通过。
- `git diff --check`：通过。

## 下一步

Day 9 对 Big Agnes 集群执行同样的品类相关性规则，并检查品牌页、Copper Spur / Tiger Wall 指南和移动端比较入口。最新 GA4/GSC 28 天数据仍需用户登录后台或提供导出。
