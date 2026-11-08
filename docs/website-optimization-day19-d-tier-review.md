# Day 19：D 层页面小样本复核

日期：2026-11-06
状态：`COMPLETED`
复核范围：7 个旧提案中的条件候选

## 结论

本次逐页检查了 `docs/growth-day38-d-tier-cleanup-proposal.md` 中全部 7 个条件候选。7/7 当前仍可索引且位于产品 sitemap；内部入口数为 2 至 15。没有页面具备立即合并、noindex 或删除的充分证据，因此本次批准的 URL 清理数量为 **0**。

这次复核没有用过期的 GSC 数据推断页面无需求。最新页面级搜索与外链证据仍缺失，Day 17 的 M3 数据闸门继续保持 `NEEDS_USER`。

逐页结果见 `docs/website-optimization-day19-d-tier-review.csv`。

## 分组结果

### 保留并修正：3 页

1. **Montbell Seamless Burrow Bag #5 Long**：当前官方页明确为 EXCELOFT 合成保温，产品重 912 g、含收纳袋 940 g，舒适温度 7°C、下限 3°C；本地 `fillType` 仍误写为羽绒。
2. **AEGISMAX Wind Hard Tiny quilt**：当前来源把 290 g 标为填充重量、440 g 标为睡袋重量；本地错误地把 0.29 kg 当作产品重量。
3. **Naturehike Morning View King**：旧 URL 已跳转为 Horizon 多变体气垫，King 版重量随 25/38/45 cm 厚度变化；本地单一 5.8 kg 和 1 人容量无法对应当前具体变体。

前两项是来源明确的低风险数据修正候选。Naturehike 页面必须先选择明确变体，不能把多个尺寸拼成一个产品事实。

### 保留并补充：1 页

**NEMO Pulse quilt** 的官方页现有完整重量、温标、填充与尺寸信息，本地页却没有重量和温标。该页有 9 个内部入口且产品身份独特，应该补充清晰变体，而不是 noindex。

### 暂缓处理：3 页

- **NANGA Level 8 -20**：官方集合仍列出该独特型号，但直接产品页抓取不稳定，当前不能安全重写重量。
- **NANGA Minimarhythm Zero**：官方商品仍存在，但可读取页面没有暴露足够技术字段；先刷新来源记录。
- **Asta Gear Shanju Cuben**：本地描述为空，但有 15 个内部入口；官方来源当前无法访问，而且另有 20D Shanju 页面。材料变体未核实前不得合并。

## Day 20 安全边界

- 可以准备 Montbell 与 AEGISMAX 两项来源明确的数据修正，但必须避开用户正在修改的生成文件；若无法隔离变更则继续暂缓。
- Naturehike、NEMO 与两项 NANGA 页面需要先刷新并绑定明确变体或字段。
- Asta Gear 页面需要先证明 Cuben 与 20D 是否为同一搜索意图和同一产品记录。
- 在获得当前 GSC 页面数据与外链证据前，任何 URL 的 noindex、合并、重定向或删除均不获批准。
- 后续若真执行清理，每批仍不得超过 10 个 URL，并必须保存原 URL、目标 URL、原因、验证和回滚动作。

## 验证

- 样本数量：7，未超过 SOP 的 10 页上限。
- 7/7 页面文件存在、可索引并出现在 `sitemap-products.xml`。
- 当前内部入口重新计数完成。
- 官方来源仅用于事实复核；未发送请求、提交表单或修改第三方账号。
- 未修改页面、目录数据、sitemap、robots、canonical 或重定向。

## 下一步

Day 20 只执行来源明确且能与用户工作区改动隔离的低风险修正。最新 GA4、GSC 查询/网页导出与引用域名数据仍需用户提供；在此之前，URL 级清理继续冻结。
