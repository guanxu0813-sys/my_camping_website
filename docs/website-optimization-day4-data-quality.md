# Day 4 数据质量抽查

- 日期：2026-10-22
- 状态：`COMPLETED`（2026-10-25 完成用户批准的低风险修复）
- 样本：20 条，覆盖 tent、tarp、sleeping bag、sleeping pad、stove，每类 4 条
- 明细：`docs/website-optimization-day4-data-sample.csv`

## 结论

本次采用风险导向抽样：每个核心品类同时检查正常记录和高风险提示，因此结果不能外推为全站错误率。20 条中有 7 条通过、11 条存在明确的字段或品类问题、2 条需要刷新来源链接。风险样本明确问题率为 55%，超过计划的 5% 停止门槛，所以本轮只记录证据和修复队列，不批量改产品数据。

这样做对流量的帮助很直接：错误的重量、零价格和把配件当主产品，会降低比较结果可信度，也可能让搜索引擎收录低价值页面；先修高风险记录比继续增加 URL 更有价值。

## 20 条抽查结果

| 品类 | 通过 | 明确问题 | 待刷新来源 |
|---|---:|---:|---:|
| Tent | 1 | 2 | 1 |
| Tarp | 1 | 3 | 0 |
| Sleeping bag | 1 | 3 | 0 |
| Sleeping pad | 1 | 3 | 0 |
| Stove | 3 | 0 | 1 |
| **合计** | **7** | **11** | **2** |

## 全量提示分层

`validate_official.py` 对 836 条产品给出 204 个提示，涉及 187 条产品。提示不是 204 个已确认事实错误：

- 113 个缺重量提示。
- 30 个配件候选，并伴随 30 个 indexability 复核提示。
- 24 个标准化名称重复提示，很多是颜色或人数变体，需要人工判断，不能自动合并。
- 22 个缺描述提示。
- 15 个非正价格提示。
- 14 个可疑重量提示，其中大型帐篷或整套火炉可能是真实值。

问题记录主要集中在 tent 68 条、sleeping bag 54 条、sleeping pad 23 条、chair 12 条、tarp 11 条。当前没有 JSON 结构错误。

## 优先修复队列

1. 配件误分类：Daisy Chain、Alto TR2 Inner Tent、Naturehike tent pole、Sleeping Bag Stuff Sack、Pad Coupler Kit Loops、Vortex Pump Sack。
2. 无效数值：Snow Peak Land Station 的 0 kg，以及 3 条 Flames Creed 记录的 0 价格。
3. 缺字段：Flames Creed sleeping bag、Aegismax AIR sleeping bag。
4. 来源刷新：Giling Pro、Daisy Chain、Naturehike tent pole、Fire Maple Hornet II 的请求落到品牌首页；Snow Peak 页面返回 403，需要普通浏览器人工核对。

## 权限边界

本轮没有把 0 自动猜成价格或重量，也没有仅凭名称批量改分类、删除页面或设置 noindex。请用户确认先执行一个不超过 10 条的低风险修复批次；来源仍不确定的记录继续保留为待验证，不伪造官方数据。

## 验证

- `python3 scripts/validate_official.py --quality-report ... --limit 836`：结构通过，836 条产品，204 个质量提示。
- 20 个官方 URL 只读检查：多数返回 200；1 个返回 403；4 个请求落到品牌首页，其中部分与明确品类问题重合。
- Day 4 未修改生成数据或页面。

## 下一步

Day 4 的低风险修复已经完成。剩余缺字段、重复名称和来源刷新项继续保留为人工核对队列，不根据名称或相邻产品猜值。Day 5 的 CTR 页面队列继续明确沿用 2026-09-07 的最后确认数据，除非用户先完成 GSC 登录或提供最新导出。

## 2026-10-25 修复收尾

用户批准后，按上限处理了正好 10 条记录：

- 6 个明确配件设置为不进入主比较表和详情卡；其独立页面保留但使用 `noindex,follow`，并从产品 sitemap 移除。
- Snow Peak Land Station 删除错误的 `0 kg`，在没有可靠来源值时显示为未提供重量。
- 3 个 Flames Creed 产品删除错误的 `0 USD`，在没有可靠来源值时显示为 `Price not listed`。
- 同步页面生成、前端过滤和质量审计的配件识别规则，并定向更新受影响的产品页、品牌页和 4 个分类页。

这批修复没有修改来源 URL、没有猜测缺失值、没有删除页面，也没有扩大到其余质量提示。质量报告仍会把“缺少价格/重量”和“配件候选”保留为提示，这是对未知事实和审核状态的诚实记录，不代表修复失败。
