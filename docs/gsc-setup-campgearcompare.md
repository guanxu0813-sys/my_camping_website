# Google Search Console — campgearcompare.com

> 正式域 SEO 配置清单。测试域 `my-camping-website.vercel.app` 的 GSC **不会**自动迁移。

**主域（canonical）：** `https://campgearcompare.com`  
**Sitemap：** `https://campgearcompare.com/sitemap.xml`

---

## 0. 部署前自检（代码 / 线上）

```bash
# 本地
grep siteUrl data/seo.json
head -5 sitemap.xml

# 线上（部署 push 后）
curl -sI https://campgearcompare.com/
curl -s https://campgearcompare.com/sitemap.xml | head -8
curl -s https://campgearcompare.com/tent.html | grep canonical
```

期望：
- `siteUrl` = `https://campgearcompare.com`
- sitemap 中 URL 均为 `campgearcompare.com`
- canonical 与 sitemap 一致

### Vercel 域名跳转（重要）

若 `campgearcompare.com` 308 跳到 `www.campgearcompare.com`，请在 Vercel **Domains** 中：

1. `campgearcompare.com` → **Production**（主域）
2. `www.campgearcompare.com` → **Redirect** 到 `campgearcompare.com`

与项目 `vercel.json` 一致，避免 canonical 与真实访问 URL 冲突。

---

## 1. 新建 GSC 资源

1. 打开 [Google Search Console](https://search.google.com/search-console)
2. 左上角 **添加资源**
3. 类型选 **网址前缀**
4. 输入：`https://campgearcompare.com`
5. **继续**

> 若你最终只用 `www` 作主域，资源 URL 改为 `https://www.campgearcompare.com`，并同步修改 `data/seo.json` + 运行 `python3 scripts/sync_site_url.py`。

---

## 2. 验证所有权（二选一）

### 方式 A：HTML 文件（推荐，与测试域相同流程）

1. GSC 验证页选 **HTML 文件**
2. 下载 `googleXXXXXXXX.html`
3. 放到项目**根目录**（与 `index.html` 同级）
4. `git add googleXXXXXXXX.html && git commit && git push`
5. 浏览器访问 `https://campgearcompare.com/googleXXXXXXXX.html` 确认 200
6. GSC 点 **验证**

### 方式 B：DNS TXT（不改代码）

1. GSC 选 **域名提供商** → **TXT 记录**
2. 复制 Google 提供的 `google-site-verification=...`
3. 阿里云 → 域名 → **解析设置** → 添加记录：
   - 类型：**TXT**
   - 主机记录：**@**
   - 记录值：粘贴 Google 整段验证字符串
4. 等 5–30 分钟 → GSC **验证**

---

## 3. 提交站点地图

1. GSC 左侧 **站点地图**
2. **添加新的站点地图**，只填：

```
sitemap.xml
```

3. **提交**

| ✅ 正确 | ❌ 错误 |
|--------|--------|
| `sitemap.xml` | `/`（首页不是 sitemap） |
| | `https://campgearcompare.com/` |

成功标志：状态非「无法抓取」，**已发现的网页** 约 **6** 条。

---

## 4. 请求编入索引

顶部 **网址检查**，逐个输入 → **测试实际 URL** → **请求编入索引**：

| 页面 | URL |
|------|-----|
| 首页 | `https://campgearcompare.com/` |
| 帐篷 | `https://campgearcompare.com/tent.html` |
| 天幕 | `https://campgearcompare.com/tarp.html` |
| 睡袋 | `https://campgearcompare.com/sleeping-bag.html` |
| 家具 | `https://campgearcompare.com/furniture.html` |
| 法律 | `https://campgearcompare.com/legal.html` |

`other.html`、`etc.html` 为 `noindex`，**不必**提交。

---

## 5. 旧资源处理

| 资源 | 建议 |
|------|------|
| `my-camping-website.vercel.app` | 可保留，不再维护 |
| 根目录 `google552523522ea8ca31.html` | 仅服务测试域，正式域需**新**验证文件 |

---

## 6. 验证完成后（可选）

- 启用 Plausible：见 [`custom-domain-setup.md`](./custom-domain-setup.md) §5
- 30 天后填媒体 kit 流量表：[`sponsor/media-kit-one-pager-zh.md`](./sponsor/media-kit-one-pager-zh.md)

---

## 快速复制

```
GSC 资源：https://campgearcompare.com
Sitemap：sitemap.xml
Robots：https://campgearcompare.com/robots.txt
```
