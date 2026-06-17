# 正式域名部署指南 — campgearcompare.com

> **主域名（canonical）：** `https://campgearcompare.com`  
> **测试域（保留）：** `https://my-camping-website.vercel.app`  
> **最后更新：** 2026-06

代码库已切换 canonical / sitemap / robots 至正式域名。按下列步骤在 Vercel 与 DNS 侧完成绑定。

---

## 1. 代码侧（已完成 / 部署前确认）

| 文件 | 状态 |
|------|------|
| `data/seo.json` | `siteUrl` → `https://campgearcompare.com` |
| 各 HTML `<link rel="canonical">` | 由 `scripts/sync_site_url.py` 同步 |
| `sitemap.xml` / `robots.txt` | 由 `scripts/build_sitemap.py` 生成 |
| `data/analytics.json` | `plausibleDomain` → `campgearcompare.com`（`enabled` 仍为 `false`，Plausible 就绪后再开） |
| `vercel.json` | `www` → 根域 301 重定向 |

**换域名后一键同步：**

```bash
# 1. 修改 data/seo.json 的 siteUrl
# 2. 运行
python3 scripts/sync_site_url.py
git add -A && git commit -m "chore: switch site URL to campgearcompare.com"
git push
```

---

## 2. Vercel 添加自定义域名

1. 打开 [Vercel Dashboard](https://vercel.com) → 项目 **my-camping-website**
2. **Settings → Domains**
3. 添加：
   - `campgearcompare.com`
   - `www.campgearcompare.com`
4. Vercel 会显示需要配置的 **DNS 记录**（按 registrar 实际界面操作）

### 典型 DNS 配置（域名在 Cloudflare / Namecheap / GoDaddy 等）

| 类型 | 名称 | 值 | 说明 |
|------|------|-----|------|
| **A** | `@` | `76.76.21.21` | Vercel 根域（以 Vercel 面板显示为准） |
| **CNAME** | `www` | `cname.vercel-dns.com` | www 子域 |

> DNS 生效通常 5 分钟–48 小时。Vercel Domains 页出现 **Valid Configuration** 即表示成功。

### 主域策略

- **Canonical：** `https://campgearcompare.com`（无 www）
- **www：** 自动 301 到根域（见 `vercel.json`）
- 测试域 `my-camping-website.vercel.app` 可继续访问，但 SEO 以正式域为准

---

## 3. 部署后验证清单

在浏览器或终端逐项确认：

```bash
# 根域可访问
curl -sI https://campgearcompare.com | head -3

# www 重定向到根域
curl -sI https://www.campgearcompare.com | grep -i location

# sitemap / robots
curl -s https://campgearcompare.com/sitemap.xml | head -5
curl -s https://campgearcompare.com/robots.txt

# canonical 示例
curl -s https://campgearcompare.com/tent.html | grep canonical
```

- [ ] 首页与各品类页正常加载
- [ ] `sitemap.xml` 中 URL 均为 `campgearcompare.com`
- [ ] 对比表、Modal、赞助位（若 `active: true`）正常

---

## 4. Google Search Console（新资源）

测试域上的 GSC 验证 **不会** 自动迁移到正式域，需新建资源：

1. [Google Search Console](https://search.google.com/search-console) → **添加资源**
2. 选 **网址前缀**：`https://campgearcompare.com`
3. 验证方式（任选其一）：
   - **HTML 文件**：下载验证文件 → 放到项目根目录 → push 部署
   - **DNS TXT 记录**：在域名 DNS 添加 Google 提供的 TXT
4. 提交 sitemap：`https://campgearcompare.com/sitemap.xml`
5. 对 `tent.html`、`tarp.html` 等主要页面 **请求编入索引**

旧资源 `my-camping-website.vercel.app` 可保留观察，但排名以正式域为准。

详细步骤见 [`gsc-setup-campgearcompare.md`](./gsc-setup-campgearcompare.md)。

---

## 5. Plausible Analytics（正式域上线后）

1. 在 [Plausible](https://plausible.io) 添加站点 `campgearcompare.com`
2. 修改 `data/analytics.json`：

```json
{
  "provider": "plausible",
  "enabled": true,
  "plausibleDomain": "campgearcompare.com",
  "contactEmail": "guanxu0813@gmail.com"
}
```

3. Push 部署 → 打开站点 → 控制台应无 `[CampGear analytics]` 本地日志（生产环境走 Plausible）
4. 积累 30 天后，更新 `docs/sponsor/media-kit-one-pager.md` 中的流量指标表

---

## 6. 赞助 demo 与对外材料

- 对外链接统一改为 `https://campgearcompare.com`
- 媒体 kit 已随 `sync_site_url.py` 更新；PDF 导出前再核对一遍
- 签约前将 `data/sponsors.json` 的 `active` 改回 `false`（除非已有付费客户）

---

## 7. 常见问题

**Q：Vercel 显示 Invalid Configuration？**  
检查 DNS 是否指向 Vercel 提供的 A/CNAME，勿与其他主机冲突。

**Q：根域和 www 都能打开，没有跳转？**  
确认 `vercel.json` 已部署；在 Vercel Domains 里两个域名都添加。

**Q：正式域上线后测试域还要吗？**  
可保留作 staging；SEO 与 outreach 只用正式域 URL。

**Q：邮箱 legal@campgearcompare.com？**  
在域名 DNS 配置 MX / 邮件转发至 `guanxu0813@gmail.com`（与站点部署独立，在域名注册商或 Google Workspace 设置）。

---

## 相关脚本

| 脚本 | 用途 |
|------|------|
| `scripts/sync_site_url.py` | 从 `seo.json` 同步 canonical + docs + sitemap |
| `scripts/build_sitemap.py` | 仅生成 sitemap / robots |
