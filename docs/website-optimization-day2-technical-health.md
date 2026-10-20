# Day 2 全站技术健康检查

- 日期：2026-10-20
- 状态：`COMPLETED`
- 范围：本地生成站点、内部链接、结构化数据、数据文件、分析埋点、线上基础 SEO

## 结论

网站核心技术检查通过。当前生成站点包含 900 个 HTML 文件和 865 个唯一 sitemap URL，RSS 与内部链接有效；结构化数据抽查 10/10 通过；首页及帐篷页线上访问返回 HTTP 200，canonical、Open Graph、JSON-LD、robots.txt 和 sitemap 均可读取。

## 本次修复

1. 更新重量价格报告回归测试：报告已主动排除 1 条误分类睡袋和 1 个睡垫连接配件，当前正确记录数为 541，其中 USD 495、GBP 28、JPY 18。测试同时明确断言这两条低价值记录不得重新进入报告。
2. 为线上 SEO 检查脚本增加 5 秒连接超时、20 秒总超时和 2 次重试，避免单个网络请求无限等待。

## 验证结果

| 检查 | 结果 |
|---|---|
| `npm test` | 通过，分析埋点和指南比较深链通过 |
| `python3 scripts/validate_generated_site.py` | 通过，900 个 HTML、865 个 sitemap URL，RSS 与内部链接有效 |
| `python3 scripts/audit_structured_data.py` | 通过，抽查 10/10 |
| `python3 scripts/validate_official.py` | 通过，836 条产品；保留 204 条质量提示供 Day 4 抽查 |
| `python3 scripts/validate_sponsors.py` | 通过，1 个活动配置且当前 0 个启用 |
| `python3 scripts/test_growth_tools.py` | 通过，14/14 |
| `node scripts/test_consent_region.cjs` | 通过 |
| `bash scripts/check_site_seo.sh` | 通过，线上首页 HTTP 200，关键 SEO 标签可读 |
| `git diff --check` | 通过 |

`verify_sponsors_jsdom.mjs` 是启用演示赞助活动时使用的专项测试；当前生产配置明确关闭赞助活动，因此本轮不将该演示前置条件作为失败。

## 问题清单

### P0 / P1

- 无阻塞发布、抓取或核心交互的问题。

### P2

- 官方数据校验产生 204 条质量提示。它们不是结构错误，但需要在 Day 4 按品类抽查时判断是否包含重量、价格、描述或来源质量问题。
- 部分历史推广文案仍写“543 products”，而当前清洗报告为 541 条。历史投递记录不应篡改；后续新文案必须使用 541 或自动读取当前报告数量。已发布平台内容若允许编辑，需要用户在对应平台修改。

### P3

- Day 1 的 GA4/GSC 登录阻塞仍未解除，但不影响本次本地和公开页面技术检查。

## 下一步

Day 3 执行比较漏斗端到端审计，重点验证指南深链、选择、比较、产品 Modal、站外点击和移动端路径。Day 1 的 GA4/GSC 数据补录继续单独保留，不用估算值代替。
