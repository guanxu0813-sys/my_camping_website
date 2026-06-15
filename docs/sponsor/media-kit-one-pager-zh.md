# CampGear Compare — 媒体 Kit（One-Pager）

**最后更新：** 2026 年 6 月  
**站点：** [https://campgear.com](https://campgear.com)  
**赞助联系：** [guanxu0813@gmail.com](mailto:guanxu0813@gmail.com)  
**英文版：** [`media-kit-one-pager.md`](./media-kit-one-pager.md)

---

## 我们是谁

**CampGear Compare** 是一个英文界面的露营装备 **参数对比** 站点。用户可在并排对比表中查阅帐篷、天幕、睡袋等产品的重量、容量、面料、价格——数据均来自 **品牌官网**，并可一键跳转至品牌官方商城购买。

我们帮助品牌在 **用户做购买决策的对比时刻** 获得曝光，且 **不修改任何客观产品数据**。

---

## 受众与使用场景

| | |
|---|---|
| **语言** | 英文 UI（面向美国及全球露营用户） |
| **使用场景** | 购前调研：重量、容量、面料、价格 |
| **主要转化路径** | 品类对比表 → 产品详情弹窗（Modal）→ 点击跳转品牌官网 |
| **流量阶段** | 软启动中（SEO 索引进行中；正式域名上线后启用分析统计） |

---

## 数据概览 *(目录快照 — 2026 年 6 月)*

| 指标 | 数值 |
|--------|------:|
| **已收录产品** | 554 |
| **数据库品牌数** | 11 |
| **帐篷** | 242 |
| **睡袋** | 162 |
| **天幕** | 58 |
| **桌椅** | 92 *（家具品类 — 持续扩充）* |
| **已上线对比页** | 帐篷 · 天幕 · 睡袋 · 家具 |

### 当前数据库中的品牌

Big Agnes · Blackdeer · DOD · Helinox · Mobi Garden · Montbell · NANGA · Naturehike · NEMO · Sea to Summit · Snow Peak

*若我们已抓取您的官方商城，您的型号已在库中。赞助位让 **您的产品** 出现在研究者眼前——而非竞争对手。*

---

## 赞助位库存

所有付费展示均 **明确标注「Sponsored」**，仅改变 **可见性**，绝不修改重量、容量、价格等规格字段。

| 赞助位 | 出现位置 | 形式 | 参考定价 |
|-----------|------------------|--------|----------------|
| **对比表置顶行** | 品类对比表首行（如帐篷页） | 行高亮 + 型号旁「Sponsored」徽章 | **$300–500 / 月 / 品类** |
| **Modal 推荐** | 用户打开您的产品详情弹窗时 | 徽章 + 说明：*Paid placement — comparison specs are not altered.* | **$150–300 / 月** |
| **品牌 Banner** | 首页或品类页头部区域 | Logo + 标题 + 跳转官网 | **$500–800 / 月** |
| **品类洞察报告** | 交付 PDF + 可选站内提及 | 单一品类的规格/价格格局汇总 | **$1,000+ / 次** |

**对比表置顶** 已包含该 SKU 在 Modal 内的赞助说明。  
完整定价、套餐与试点折扣见：[`pricing-sheet-zh.md`](./pricing-sheet-zh.md)

---

## 效果指标 *(每月从分析后台更新)*

分析工具：**Plausible**（隐私友好、无 Cookie）。已埋点的自定义事件：

| 事件 | 含义 |
|-------|---------|
| `Product Modal Open` | 用户打开产品详情弹窗（高意向行为） |
| `Outbound Click` | 用户点击跳转至品牌官网 |

### 汇报模板

正式域名启用 Plausible 后（建议 outreach 前至少积累 **30 天** 数据），填写下表：

| 页面 / 品类 | 月 PV | Modal 打开数 | Modal 率¹ | 出站点击数 | 出站 CTR² |
|-----------------|------------------:|------------:|------------:|----------------:|--------------:|
| `tent.html` | _待填_ | _待填_ | _待填_ | _待填_ | _待填_ |
| `tarp.html` | _待填_ | _待填_ | _待填_ | _待填_ | _待填_ |
| `sleeping-bag.html` | _待填_ | _待填_ | _待填_ | _待填_ | _待填_ |
| **全站合计** | _待填_ | _待填_ | _待填_ | _待填_ | _待填_ |

¹ **Modal 率** = Modal 打开数 ÷ 该品类页 PV  
² **出站 CTR** = 出站点击数 ÷ Modal 打开数 *（或以 PV 为分母看漏斗上层）*

**从 Plausible 导出步骤**

1. 在生产环境启用 `data/analytics.json`（`enabled: true`，填入正确域名）。
2. 在 Plausible → **Goals** 中确认 `Product Modal Open` 与 `Outbound Click` 事件。
3. 按页面 URL 与日期范围（近 30 天）筛选。
4. 发媒体 kit 给品牌前，将数字填入上表。

> **早期 outreach 提示：** 在流量基线建立前，主打 **目录深度**、**对比体验** 与 **编辑防火墙**（见下）。可提供 **创始合作伙伴** 试点价（见定价表）。

---

## 编辑诚信（品牌为何信任我们）

- 赞助行 **置顶并标注**——规格列保持客观事实。
- 赞助产品须已在官方目录中（优先 `status: verified`）。
- 活动通过 `expiresAt` **自动到期**——无「幽灵」赞助位。
- 公开政策：[Sponsor Policy](https://campgear.com/legal.html#sponsor)

---

## 赞助商获得什么

1. 高意向对比表中的 **首行曝光**（Table Featured 档位）。
2. 用户点开 SKU 时的 **Modal 展示**。
3. 合同 bundled 的 **书面素材授权**——品牌批准的图片/Logo 可在活动期内使用（见 [`sponsorship-agreement-template-zh.md`](./sponsorship-agreement-template-zh.md) §4）。
4. **Campaign ID** 便于内部对账；可按需提供汇总的点击/Modal 数据。

---

## 创始合作伙伴试点 *(名额有限)*

前 **3** 家品牌合作伙伴（目标：Naturehike、Snow Peak、Helinox、Big Agnes、Sea to Summit）：

- 前 **3 个月** 标价 **75 折**
- 预订 Table Featured 即 **免费** 加赠 Modal Featured
- 优先选择品牌目录内的赞助 SKU

---

## 下一步

1. 发邮件至 [guanxu0813@gmail.com](mailto:guanxu0813@gmail.com)，注明品牌名、目标品类、意向 SKU。
2. 我们确认资格（产品已在目录、无规格冲突）。
3. 签署 [`sponsorship-agreement-template-zh.md`](./sponsorship-agreement-template-zh.md)（或同等条款的纸质合同）。
4. 素材交付 + 付款后 **5 个工作日内** 上线活动。

---

*CampGear Compare · 露营装备对比 · 规格数据来自品牌官网*
