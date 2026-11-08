# Day 20：低风险清理执行判断

计划日期：2026-11-07
复核日期：2026-11-08
状态：`NEEDS_USER`
URL 清理数量：0
数据修正数量：0

## 结论

Day 19 没有批准任何 URL 合并、noindex、重定向或删除，因此 Day 20 不执行 URL 级清理。两项来源明确的数据修正也暂未落地，因为当前工作区正在并行修改生成链路：

- `data/catalog.js`
- `scripts/build_guides.py`
- `scripts/build_sitemap.py`
- `script.js`
- `package.json`

官方产品 JSON 本身没有未提交改动，但只修改源文件而不重建目录和静态页会造成数据不一致；直接重建又会把上述并行改动带入大量生成文件。按照 SOP 的权限边界，本次选择停下，不覆盖或混入用户工作。

## 已确认但未执行的修正

### Montbell Seamless Burrow Bag #5 Long

- 当前错误：`fillType` 为羽绒。
- 已核验事实：EXCELOFT 合成保温；产品重 912 g，含收纳袋 940 g；舒适温度 7°C，下限 3°C。
- 预定动作：把填充类型改为合成材料，并增加有明确标签的产品重量、打包重量和温标字段。

### AEGISMAX Wind Hard Tiny quilt

- 当前错误：0.29 kg 被当作产品重量。
- 已核验事实：290 g 是填充重量，440 g 是睡袋重量，不含压缩袋和收纳袋。
- 预定动作：把产品重量改为 0.44 kg，仅把 0.29 kg 保留为明确标注的填充重量。

## 未来执行与回滚清单

工作区生成链路干净后，单独执行以下小批次：

1. 修改 `data/official/montbell/products.json` 和 `data/official/aegismax/products.json` 中两个准确 ID。
2. 运行 `python3 scripts/build_catalog.py` 和 `python3 scripts/build_sitemap.py`。
3. 只保留由这两项数据修正产生的必要生成差异，排除无意义时间戳与无关页面。
4. 运行 `npm test`、增长测试、生成站点校验、结构化数据审计和 `git diff --check`。
5. 记录变更前字段、变更后字段、官方来源和受影响页面。
6. 如出现生成、索引入口或显示回归，使用该独立提交的反向提交恢复源数据和全部生成文件。

## 安全状态

- Day 19 的 7 个候选页均未修改。
- sitemap、robots、canonical、重定向和 noindex 均未改变。
- 最新 GSC 页面数据和外链证据到位前，URL 清理继续冻结。

## 用户操作

请先完成或提交当前目录/联盟生成链路改动，之后才能把这两项修正隔离为独立提交。GA4、GSC 查询/网页和引用域名导出仍是 M3/M4 闸门的另一项独立阻塞。
