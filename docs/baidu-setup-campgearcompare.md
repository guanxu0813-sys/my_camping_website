# 百度搜索资源平台 — campgearcompare.com

> 与 [Google GSC](./gsc-setup-campgearcompare.md) 并行；百度需单独注册、验证、提交。  
> 主域：`https://www.campgearcompare.com`  
> Sitemap：`https://www.campgearcompare.com/sitemap.xml`

---

## 0. 代码库已就绪项

| 项 | 状态 |
|----|------|
| `robots.txt` / `sitemap.xml` | 已有，允许抓取并声明 sitemap |
| `script.js` 自动推送 | 已接入百度 `push.js`（验证通过后，用户访问即通知百度） |
| `scripts/submit_baidu_urls.py` | API 批量推送（需 `BAIDU_PUSH_TOKEN`） |
| GitHub Action | `.github/workflows/submit-baidu-urls.yml`（配置密钥后自动推送） |

**仍需你在百度后台手动完成：** 注册账号 → 添加站点 → 验证所有权 → 提交 sitemap → 复制 API token。

---

## 1. 注册并添加站点

1. 打开 [百度搜索资源平台](https://ziyuan.baidu.com/)
2. 登录百度账号
3. **用户中心 → 站点管理 → 添加网站**
4. 站点 URL 填：`https://www.campgearcompare.com`（与 `data/seo.json` 的 `siteUrl` 一致）
5. 站点类型选「其他」或「工具」即可

---

## 2. 验证网站所有权（任选其一）

### 方式 A：HTML 文件（推荐，与 Google 相同流程）

1. 验证页选择 **文件验证**
2. 下载 `baidu_verify_xxxx.html`
3. 放到项目**根目录**（与 `index.html` 同级）
4. 提交并部署：

```bash
git add baidu_verify_xxxx.html
git commit -m "Add Baidu site verification file"
git push
```

5. 浏览器确认：`https://www.campgearcompare.com/baidu_verify_xxxx.html` 返回 200
6. 百度后台点 **完成验证**

### 方式 B：HTML 标签

1. 复制百度提供的 meta，例如：

```html
<meta name="baidu-site-verification" content="你的验证码" />
```

2. 加入各可索引页面的 `<head>`（至少 `index.html`），部署后点验证

### 方式 C：DNS

在域名 DNS 添加百度提供的 **CNAME** 或 **TXT** 记录，等待生效后验证。

---

## 3. 提交站点地图

验证通过后：

1. 左侧 **普通收录 → 资源提交 → Sitemap**
2. 提交：`https://www.campgearcompare.com/sitemap.xml`
3. 在「链接提交」里可再手动粘贴 6 个核心 URL（每日有配额）

---

## 4. API 主动推送（加速收录）

### 4.1 获取 token

1. **普通收录 → 资源提交 → API 提交**
2. 复制页面上的 **准入密钥**（16 位 token）
3. `site` 参数须为纯域名：`www.campgearcompare.com`（已在 `data/seo.json` 的 `baiduSite` 配置）

### 4.2 本地推送

```bash
export BAIDU_PUSH_TOKEN='你的token'
python3 scripts/submit_baidu_urls.py
```

预览（不调 API）：

```bash
python3 scripts/submit_baidu_urls.py --dry-run
```

### 4.3 GitHub Actions 自动推送

1. 仓库 **Settings → Secrets and variables → Actions**
2. 新建 **Repository secret**：`BAIDU_PUSH_TOKEN`
3. `main` 分支 push（SEO 相关文件变更）或手动 **Run workflow**

未配置密钥时 workflow 仅 dry-run，不会失败。

---

## 5. 自动推送（已写入前端）

`script.js` 在正式域（非 localhost / `file://`）加载百度 `push.js`：用户访问页面时自动将当前 URL 推送给百度。  
**前提：** 站点已在百度完成验证。

---

## 6. 部署后自检

```bash
bash scripts/gsc_post_verify.sh
python3 scripts/submit_baidu_urls.py --dry-run
bash scripts/check_site_seo.sh https://www.campgearcompare.com
```

在百度后台查看：**数据统计 → 索引量**、**抓取诊断**。

---

## 7. 预期与限制

| 项目 | 说明 |
|------|------|
| 语言 | 站点为英文；百度以中文搜索为主，收录速度与排名通常弱于 Google |
| 服务器 | Vercel 海外节点；百度抓取可能较慢，属正常现象 |
| ICP 备案 | 未备案也可提交，国内访问体验与权重可能受影响 |
| API 配额 | 普通收录每日有上限（常见为万级）；脚本单次最多 2000 URL |
| 常见报错 | `site init fail` → 检查 `site` 是否为纯域名，勿带 `https://` |

---

## 8. 相关文件

| 文件 | 用途 |
|------|------|
| [`data/seo.json`](../data/seo.json) | `siteUrl`、`baiduSite`、可索引页面列表 |
| [`scripts/submit_baidu_urls.py`](../scripts/submit_baidu_urls.py) | API 批量推送 |
| [`scripts/gsc_post_verify.sh`](../scripts/gsc_post_verify.sh) | 部署后 Google + 百度检查清单 |
| [`.github/workflows/submit-baidu-urls.yml`](../.github/workflows/submit-baidu-urls.yml) | CI 自动推送 |
