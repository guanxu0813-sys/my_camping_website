# Day 1 网站优化基线与访问阻塞

日期：2026-10-19  
计划：`website-optimization-sop-30d.md` Day 1  
状态：`NEEDS_USER`

## 可确认的本地基线

| 项目 | 当前值 | 数据日期 / 说明 |
|---|---:|---|
| 最近一条增长指标 | 2026-09-07 | 已过期，不能代表当前 28 天表现 |
| 最近完整周总访问 | 42 sessions | 2026-08-26 至 2026-09-01 |
| 最近完整周自然访问 | 23 sessions | 2026-08-26 至 2026-09-01 |
| 最近完整周 GSC 点击 | 22 | 2026-08-26 至 2026-09-01 |
| 最近完整周 GSC 展示 | 1,521 | 2026-08-26 至 2026-09-01 |
| 最近完整周 GSC CTR | 1.45% | 2026-08-26 至 2026-09-01 |
| 最近完整周平均排名 | 19.3 | 2026-08-26 至 2026-09-01 |
| 最近完整 M1 自然访问 | 93 sessions | 2026-08-05 至 2026-09-01 |
| 最近完整 M1 GSC 点击 / 展示 | 105 / 5,693 | 2026-08-05 至 2026-09-01 |
| 已知引用域名 | 2 | 最近确认于 2026-09-07 |
| Sitemap URL | 865 | core 29、brands 66、products 770 |
| 指南 HTML | 18 | 包含指南索引页 |
| 重量价格数据记录 | 541 | 当前可下载报告 |
| Amazon 联盟 | 未启用 | approval not confirmed |
| AliExpress 联盟 | 未启用 | appeal pending，没有批准证据 |

## 当前判断

- 当前线上表现没有可验证的新 28 天数据，因此不能判断 M2 是否达到进入 M3 的数据门槛，也不能把旧数据描述为当前增长。
- 最后确认的策略仍为 `FOCUS`：优先处理数据质量、查询意图、CTR、比较使用率和相关引用，不扩大第三个主题集群。
- Naturehike 与 Big Agnes 是最后确认通过点击门槛的两个集群；在新数据出现前保持这两个集群，不凭感觉扩展。
- 联盟账号均没有批准证据，继续保持关闭。
- 工作区存在未提交的推广资产和日志；它们不属于 Day 1，本次没有修改或暂存。

## 数据访问阻塞

Google Analytics 当前需要账号登录，项目中也没有 2026-09-07 之后的 GA4 或 GSC 导出。因此 Day 1 不能安全填写最新流量、自然访问、比较事件、GSC 查询、页面和引用域名。

需要用户完成以下任一方式：

1. 在当前 Google 页面完成登录，并保持 GA4 与 Search Console 会话可用；或
2. 提供同一固定窗口的 GA4 与 GSC CSV 导出。

建议固定窗口：2026-09-18 至 2026-10-15，共 28 个完整自然日。

## 需要补齐的字段

GA4：

- Sessions、Organic Search sessions
- Engaged sessions、Organic engaged sessions
- `compare_selected`
- `product_modal_open`
- `outbound_click`
- 按 landing page 的自然访问和参与情况
- Pinterest、YouTube 和社区 UTM 会话与有效事件

GSC：

- Clicks、impressions、CTR、average position
- 查询和页面两个维度的完整导出
- Naturehike 与 Big Agnes 集群点击、展示和查询数
- Indexed pages / not indexed pages
- External links 与 top linking sites

## 下一步

登录或导出完成后，先补齐本基线和 `growth-metrics.csv`，再运行 Day 5 的高展示低 CTR 队列。Day 2 的本地技术健康检查不依赖 Google 登录，可以按计划继续执行。
