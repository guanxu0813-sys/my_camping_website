# Google Indexing API 自动提交配置说明

> 适用站点：**CampGear Compare** · `https://www.campgearcompare.com`  
> 用途：部署或内容更新后，自动通知 Google 抓取/更新 URL（替代手动「请求编入索引」）。  
> 前置：已完成 [GSC 验证](./gsc-setup-campgearcompare.md)。

---

## 1. 能力边界（必读）

| 项目 | 说明 |
|------|------|
| **官方定位** | [Indexing API](https://developers.google.com/search/docs/crawling-indexing/indexing-api) 主要面向含 **JobPosting / BroadcastEvent** 结构化数据的页面 |
| **实际用法** | 许多站长对自有站点任意 URL 调用 `URL_UPDATED`；Google **不保证**一定收录，且可能忽略非合规页面 |
| **不能替代** | Sitemap 仍是基础；API 是**加速通知**，不是排名保证 |
| **配额** | 默认约 **200 次/天**（可在 Google Cloud Console 申请提高） |
| **与 GSC 手动请求** | 效果类似「请求编入索引」，但可脚本化、接入 CI |

**推荐策略**

1. 日常：依赖 **sitemap.xml** + `robots.txt`（已有）
2. 每次 **push 部署后**：对 `data/seo.json` 中的主要页面调用 Indexing API（本说明）
3. 监控：GSC「网页编制索引」+「站点地图」状态

---

## 2. 架构概览

```
部署 (Vercel) ──→ GitHub Action / 本地脚本
                        │
                        ├─ python3 scripts/build_sitemap.py   （已有）
                        └─ python3 scripts/submit_indexing_api.py
                                │
                                ├─ 读取 data/seo.json 页面列表
                                ├─ 服务账号 JWT → Access Token
                                └─ POST indexing.googleapis.com/v3/urlNotifications:publish
                                        │
                                        ▼
                                   Google 抓取队列
```

---

## 3. Google Cloud 一次性配置

### 3.1 创建项目并启用 API

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)
2. 新建项目（例如 `campgear-indexing`）
3. **API 和服务 → 库** → 搜索 **Web Search Indexing API** → **启用**  
   （旧称 Indexing API，API 名：`indexing.googleapis.com`）

### 3.2 创建服务账号

1. **IAM 和管理 → 服务账号 → 创建服务账号**
2. 名称：`campgear-gsc-indexing`
3. 角色：无需额外项目角色（GSC 侧授权即可）
4. **密钥 → 添加密钥 → JSON** → 下载，例如 `campgear-indexing-sa.json`

**安全**

- JSON **不要**提交 Git（已在 `.gitignore` 忽略 `*.credentials.json` 模式，见 §6）
- 丢失密钥可在 Cloud Console 轮换

### 3.3 在 Search Console 授权服务账号

1. 打开 [Search Console](https://search.google.com/search-console) → 资源 **`https://www.campgearcompare.com`**
2. **设置 → 用户和权限 → 添加用户**
3. 填入服务账号邮箱（形如 `campgear-gsc-indexing@xxx.iam.gserviceaccount.com`）
4. 权限：**所有者** 或 **完整**（需能代表站点提交 URL）

> 未添加此步骤时，API 返回 `403 Permission denied`。

---

## 4. 本地环境变量

在项目根目录（勿提交）：

```bash
# .env.local（自行创建，已在 .gitignore）
export GOOGLE_APPLICATION_CREDENTIALS="/绝对路径/campgear-indexing-sa.json"
export INDEXING_SITE_URL="https://www.campgearcompare.com"
```

或在 shell 中：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/secrets/campgear-indexing-sa.json"
```

---

## 5. 使用项目脚本

仓库已提供模板脚本：[`scripts/submit_indexing_api.py`](../scripts/submit_indexing_api.py)

### 5.1 安装依赖

```bash
pip install google-auth google-auth-oauthlib requests
```

或写入 `requirements-dev.txt`（可选）。

### 5.2  dry-run（只打印 URL，不调用 API）

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sa.json"
python3 scripts/submit_indexing_api.py --dry-run
```

### 5.3 提交全部 SEO 页面

```bash
python3 scripts/submit_indexing_api.py
```

默认读取 `data/seo.json` 的 `pages`，跳过 `other.html` / `etc.html`（与 sitemap 一致）。

### 5.4 只提交指定 URL

```bash
python3 scripts/submit_indexing_api.py \
  --url https://www.campgearcompare.com/tent.html \
  --url https://www.campgearcompare.com/sleeping-bag.html
```

### 5.5 成功 / 失败

| HTTP | 含义 |
|------|------|
| **200** | 已接受通知 |
| **403** | 服务账号未加入 GSC，或 API 未启用 |
| **429** | 超出日配额，次日再试或申请提额 |

---

## 6. Git 与密钥忽略

在 `.gitignore` 中应包含（若尚未有）：

```gitignore
# Google Indexing API credentials
*-sa.json
*.credentials.json
.env.local
secrets/
```

---

## 7. 接入 CI（部署后自动提交）

### 已配置：GitHub Actions

仓库 workflow：[`.github/workflows/submit-indexing-api.yml`](../.github/workflows/submit-indexing-api.yml)

- **触发**：`main` 分支 push（SEO 相关文件变更）或手动 **Run workflow**
- **无密钥时**：只跑 `--dry-run`，不会失败
- **有密钥时**：自动对 `data/seo.json` 中 6 个 URL 调用 Indexing API

### 你需要做的一次性配置（约 15 分钟）

#### A. Google Cloud

1. [Google Cloud Console](https://console.cloud.google.com/) → 新建项目 `campgear-indexing`
2. **API 和服务 → 库** → 启用 **Web Search Indexing API**
3. **IAM → 服务账号 → 创建** `campgear-gsc-indexing`
4. **密钥 → 添加密钥 → JSON** → 下载 `campgear-indexing-sa.json`

#### B. Search Console 授权

1. [Search Console](https://search.google.com/search-console) → **`https://www.campgearcompare.com`**
2. **设置 → 用户和权限 → 添加用户**
3. 填入服务账号邮箱（JSON 内 `client_email`，形如 `xxx@xxx.iam.gserviceaccount.com`）
4. 权限：**所有者**

#### C. GitHub Secret

1. 打开 GitHub 仓库 → **Settings → Secrets and variables → Actions**
2. **New repository secret**
3. Name：`GSC_INDEXING_SA_JSON`
4. Value：粘贴 **整个** JSON 文件内容（从 `{` 到 `}`）
5. 保存

#### D. 验证

1. GitHub → **Actions** → **Submit URLs to Google Indexing API** → **Run workflow**
2. 日志中应出现 6 行 `OK https://www.campgearcompare.com/...`
3. 若 `403`：检查 GSC 是否已添加服务账号、API 是否已启用

### 本地手动运行（可选）

```bash
pip install -r requirements-dev.txt
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/campgear-indexing-sa.json"
python3 scripts/submit_indexing_api.py --dry-run
python3 scripts/submit_indexing_api.py
```

### 方案 B：Vercel Deploy Hook + 本地 cron

Vercel 无内置 Indexing API；可在本机或 GitHub Actions 监听部署成功 webhook 后跑脚本。

### 方案 C：仅 sitemap 重建（零密钥）

每次部署已生成 `sitemap.xml`；Google 会定期重新抓取 sitemap，**无需 API** 也能 slowly 收录。API 用于**加快**已知 URL 的更新通知。

---

## 8. 与 sitemap 工作流配合

| 时机 | 动作 |
|------|------|
| 改 `data/seo.json` 或换域名 | `python3 scripts/sync_site_url.py` |
| 任意 SEO 相关 push 前 | `python3 scripts/build_sitemap.py` |
| 部署成功后 | `python3 scripts/submit_indexing_api.py`（可选） |
| 每周抽查 | GSC → 站点地图 + 网页编制索引 |

---

## 9. 备选：Bing IndexNow（可选）

Google 无官方 IndexNow；Bing/Yandex 支持。若需覆盖 Bing：

1. 生成随机 key，根目录放置 `{key}.txt`
2. POST `https://api.indexnow.org/indexnow`  
   文档：[IndexNow](https://www.indexnow.org/documentation)

CampGear 主战场是 Google，**优先完成 Indexing API** 即可。

---

## 10. 故障排查

| 现象 | 处理 |
|------|------|
| `403 Forbidden` | 检查 GSC 是否已添加服务账号；API 是否已启用 |
| `Invalid JWT` | 检查 `GOOGLE_APPLICATION_CREDENTIALS` 路径与 JSON 有效性 |
| 提交成功但长期未收录 | 正常；继续优化内容、内链、sitemap；API 非收录保证 |
| 脚本找不到页面 | 确认 `data/seo.json` 的 `siteUrl` 为 `https://www.campgearcompare.com` |

---

## 11. 相关文件

| 文件 | 用途 |
|------|------|
| [`data/seo.json`](../data/seo.json) | 站点 URL + 可索引页面列表 |
| [`scripts/submit_indexing_api.py`](../scripts/submit_indexing_api.py) | Indexing API 提交脚本 |
| [`scripts/build_sitemap.py`](../scripts/build_sitemap.py) | 生成 sitemap / robots |
| [`scripts/gsc_post_verify.sh`](../scripts/gsc_post_verify.sh) | 验证后自检 + 打印待索引 URL |
| [`docs/gsc-setup-campgearcompare.md`](./gsc-setup-campgearcompare.md) | GSC 手动配置清单 |

---

## 12. 快速 Checklist

- [ ] Google Cloud 项目 + 启用 Web Search Indexing API
- [ ] 创建服务账号并下载 JSON 密钥
- [ ] GSC 资源 `https://www.campgearcompare.com` 添加服务账号为**所有者**
- [ ] 本地 `GOOGLE_APPLICATION_CREDENTIALS` 指向 JSON
- [ ] `python3 scripts/submit_indexing_api.py --dry-run` 输出 6 条 URL
- [ ] 正式运行脚本，返回 200
- [ ] （可选）GitHub Secret `GSC_INDEXING_SA_JSON` + Actions workflow 跑通
- [ ] GSC 几天后查看「网页编制索引」是否增加
