# Day 23 联盟链接准备度复核

> 复核日期：2026-08-12
> 结论：Amazon Associates 和 AliExpress Affiliate 均无批准证据，保持关闭；本轮不添加试点商品。

## 1. 账号与地区

| 平台 | 本地配置 | 邮箱证据 | 地区 | 决策 |
|---|---|---|---|---|
| Amazon Associates | `enabled: false`，Associate Tag 为空 | 过去一年未找到申请、批准或拒绝邮件 | 仅预设 `www.amazon.com`，不能视为已获美国站批准 | 不启用，不添加 ASIN |
| AliExpress Affiliate | `enabled: false`，Tracking ID 为空 | 过去一年未找到申请、批准或拒绝邮件 | 未配置 | 不启用，不添加推广链接 |

“未找到证据”不等同于断言从未申请，但在取得后台批准页面或批准邮件前，一律按未批准处理。

## 2. 当前网站检查

- `data/affiliate-links.json` 的商品映射为空。
- 商品页继续使用品牌官网 `sourceUrl`，没有 Amazon/AliExpress 购买按钮。
- 联盟按钮只有在平台启用、批准 ID 存在且商品链接通过校验后才会生成。
- 联盟按钮生成时固定包含 `rel="nofollow sponsored noopener noreferrer"` 和可见佣金披露。
- `legal.html#affiliate` 与 `about.html` 已说明潜在佣金关系，不影响排序和编辑判断。

## 3. 产品匹配门槛

启用任何单个商品前，必须同时满足：

1. 品牌、完整型号、容量/尺寸和关键变体与本站产品完全一致。
2. Amazon 使用人工核实的 10 位 ASIN，或配置市场内的 `/dp/`、`/gp/product/` 直达页。
3. AliExpress 使用批准账号在 Portals 生成的 `s.click.aliexpress.com/e/` 追踪链接。
4. 禁止使用搜索页、分类页、相似款、猜测 ASIN 或无法确认变体的链接。
5. 页面必须显示佣金披露；联盟关系不得改变规格、排序或编辑结论。

构建脚本现会自动拒绝 Amazon 搜索页、错误市场/错误 ASIN，以及非 Portals 追踪格式的 AliExpress URL。

## 4. 本轮结果与下一步

- 试点商品数：**0**。原因是两个平台均未确认批准，符合 Day 23 的保守规则。
- 当前佣金链接数：**0**；未披露佣金链接数：**0**。
- 获批后先保存批准平台、地区和账号 ID，再逐件人工核对 5–10 个商品；不能一次性批量映射。
