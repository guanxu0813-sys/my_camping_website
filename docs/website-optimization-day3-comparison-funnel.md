# Day 3 比较漏斗端到端审计

- 日期：2026-10-21
- 状态：`COMPLETED`
- 路径：指南 -> 品类比较页 -> 选择/过滤 -> 产品 Modal -> 官方站链接

## 结论

比较漏斗的本地实现通过审计，没有发现阻塞用户完成比较或访问官方来源的功能问题。新增的自动审计覆盖 14 条指南比较深链、4 个品类页面，并已纳入 `npm test`，以后产品 ID、品类或链接参数不一致会直接导致测试失败。

## 覆盖结果

| 环节 | 验证结果 |
|---|---|
| 指南 CTA | 14 条 `.guide-compare-link` 均指向站内页面并携带 `source=guide` |
| 产品集合 | 每条链接包含 2–16 个唯一产品 ID，声明数量与 URL 一致 |
| 品类匹配 | 所有产品均存在，且与目标 tent、sleeping bag、sleeping pad 或 stove 页面匹配 |
| 深链选择 | 示例指南深链自动勾选 2 个产品，并仅显示指定产品 |
| 手动选择 | 选择两个产品后可进入比较状态，`compare_item_toggle` 和 `compare_selected` 正常触发 |
| 产品详情 | 表格缩略图可打开产品 Modal，`product_modal_open` 正常触发 |
| 站外点击 | Modal 的官方来源链接有效，点击触发 `outbound_click` |
| 移动端基础 | 4 个目标页均有响应式 viewport、比较根节点和 Modal；CSS 包含 720px 下的底部比较条与单列 Modal 规则 |

在 390 x 844 的本地 Chrome 视口中额外检查了双产品深链。选中行能够渲染，表格保持横向滚动容器，未发现文字或控件互相遮挡。截图仅用于本地视觉核验，未加入仓库。

## 新增保护

- 新增 `scripts/audit_comparison_funnel.mjs`，自动扫描全部指南，而不是只测一条示例链接。
- `npm test` 现在同时运行交互/分析测试和全指南漏斗审计。

## 验证

- `npm test`：通过；分析、深链和 14 条指南漏斗审计通过。
- `python3 scripts/validate_generated_site.py`：通过；900 个 HTML、865 个唯一 sitemap URL，RSS 与内部链接有效。
- `python3 scripts/audit_structured_data.py`：通过；抽查 10/10。
- `python3 scripts/test_growth_tools.py`：通过；14/14。
- `git diff --check`：通过。

## 边界与下一步

本次证明代码会生成并记录这些事件，但 GA4 后台是否持续收到真实访客事件仍需要账号登录后核对，不能用本地测试代替。Day 1 的 GA4/GSC 阻塞继续保留。

Day 4 按品类抽查至少 20 条重量、价格和官方来源，并重点处理 Day 2 记录的 204 条质量提示。
