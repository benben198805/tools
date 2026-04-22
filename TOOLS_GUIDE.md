# qlyan-tools：新增工具指南

本仓库由 [simonw/tools](https://github.com/simonw/tools) 复制而来，主体是**根目录下的静态 HTML/JS 小工具**，辅以 **`python/` 目录下的可执行脚本**（配合 `uv run`）。下面说明仓库如何组织，以及**如何根据你已有的一段代码**落地成「可被站点收录 / 可被他人复用」的工具。

---

## 1. 先选工具形态

| 形态 | 放哪里 | 适用场景 | 站点元数据（`tools.json`） |
|------|--------|----------|---------------------------|
| **浏览器工具** | 仓库根目录 `your-slug.html` | 纯前端、WASM、调用浏览器 API、少量 CDN | **会**：`gather_links.py` 只扫描根目录 `*.html` |
| **Python 脚本** | `python/your_script.py` | CLI、需要本机环境/密钥、批处理 | **不会**自动进 `tools.json`；需在 `python/README.md` 写说明与 `uv run` 示例 |
| **个人脚本** | 例如 `self/` | 仅自用、不对外展示 | 不参与 `gather_links` / 首页列表 |

**重要约束**：`gather_links.py` 使用 `Path.cwd().glob("*.html")`，**子目录里的 HTML 不会被写入 `tools.json`**。若要做「正式工具页」，请把 `*.html` 放在仓库根目录（与 `README.md` 同级）。

---

## 2. 浏览器工具：文件与命名

对 slug 为 `my-tool` 的页面，通常需要：

1. **`my-tool.html`** — 单文件或可配合根目录已有 `*.js`（如 `footer.js` 由构建注入）。
2. **`my-tool.docs.md`** — 一段简短说明；`gather_links.py` 会取**第一个非空段落**作为 `tools.json` 里的 `description`（遇到 `<!--` 会截断，因此可把 HTML 注释放在第一段之后）。
3. **（可选）** 在 **`README.md`** 的合适分类下增加一行链接，格式与现有一致，例如：  
   `- [My tool](https://你的域名/my-tool) 一句话说明`  
   首页/索引由 `build_index.py` 等脚本基于 `README.md` 与 `tools.json` 生成，**分类列表主要靠你维护 README**。

**命名建议**：slug 使用小写、连字符（与现有工具一致），`<title>` 与 `h1` 使用人类可读标题；`gather_links.py` 用 `<title>` 作为工具标题。

**`*.docs.md` 示例**（第一段 = 摘要；第二行起可放生成注释）：

```markdown
用一句话说明用户能做什么、输入输出是什么。

<!-- Generated from commit: abcdef1234567890abcdef1234567890abcdef12 -->
```

若设置环境变量 `GENERATE_LLM_DOCS=1` 并运行 `build.sh`，`write_docs.py` 可根据 HTML 用 `llm` 辅助生成/更新文档（需本机已配置相应 CLI）。

---

## 3. 浏览器工具：HTML/JS 实现要点（对齐本仓库风格）

参考任意现有根目录工具，常见约定包括：

- **单页自包含**：`<!DOCTYPE html>`、`charset`、`viewport`、内联或页内 `<style>` / `<script>`。
- **布局**：`* { box-sizing: border-box; }`，`body` 上 `max-width` + `margin: 0 auto` + `padding`，小屏用 `@media (max-width: 600px)` 等收紧间距。
- **交互**：输入用 `input`/`change`，实时反馈；错误信息单独区域；复制按钮优先 `navigator.clipboard.writeText`，必要时 `execCommand('copy')` 兜底。
- **外链库**：从 jsDelivr、cdnjs 等引入，**尽量固定版本**，避免静默升级破坏行为。

无需为单个工具单独跑打包；发布侧通过 **`build.sh`** 做聚合步骤（见下文）。

---

## 4. 从「你提供的一段代码」生成新工具的推荐流程

下面假设你有一段**可运行的逻辑**（Python/JS/伪代码均可），希望变成**根目录浏览器工具**（最常见）。

### 4.1 澄清需求（人机都可做）

- 输入是什么（粘贴、文件、URL、摄像头）？
- 输出是什么（文本、下载文件、画布、表格）？
- 是否必须联网或 API Key？若需要 Key，优先 **用户在本页粘贴** 或环境说明放在 `*.docs.md`，避免把密钥写进仓库。

### 4.2 选择实现栈

- 纯字符串/结构化数据：原生 JS 即可。
- 图像/PDF：仓库内已有大量用法可参考（如 PDF.js、Canvas、剪贴板）。
- Python 算法且不想重写：考虑 **`python/` + uv** 或 Pyodide 类页面（工作量和体积更大）。

### 4.3 落地文件

1. 在仓库根目录新增 **`{slug}.html`**，保证 `<title>` 正确。
2. 新增 **`{slug}.docs.md`**，写好第一段描述。
3. 在 **`README.md`** 增加列表项（若希望出现在主页介绍里）。
4. 若逻辑复杂或易回归，在 **`tests/test_*.py`** 里用 Playwright 做 1～2 个冒烟用例（见 `tests/conftest.py` 与现有测试）。

### 4.4 本地验证

```bash
python -m http.server 8123 --directory .
# 浏览器打开 http://127.0.0.1:8123/your-slug.html
```

安装测试依赖后：`pip install -e . && playwright install && pytest`。

### 4.5 构建与元数据（合并前）

在仓库根执行 **`./build.sh`**（或其中你需要的步骤），典型包括：

- `python gather_links.py` → 更新 `gathered_links.json`、`tools.json`
- `build_colophon.py`、`build_dates.py`、`build_index.py`、`build_by_month.py` 等
- 向已跟踪的根目录 `*.html`（除 `index.html`）注入带版本 query 的 **`footer.js`** 引用

合并前确认 **`tools.json`** 中出现你的 slug，且 **`*.docs.md`** 第一段符合预期。

---

## 5. `python/` 脚本工具（与浏览器工具分离）

- 脚本放在 **`python/`**，在 **`python/README.md`** 中为每个脚本增加一节：**用途说明、`uv run` 完整示例、依赖说明**。
- 许多脚本使用 **PEP 723** 内联元数据（`# /// script` / `requires-python` 等），便于 `uv run https://.../script.py` 拉取依赖。
- 这些脚本**不会**被 `gather_links.py` 扫描进 `tools.json`；发现与分发主要靠 **`python/README.md`** 与你自己仓库的链接。

若你提供的代码是 **PyMuPDF 批处理** 这类 CLI（例如 `self/pdf_to_jpg.py`），要进入「官方脚本」路径：把脚本移到 `python/`、补 CLI（`argparse`/`click`）、写清依赖与示例，并更新 `python/README.md`。

---

## 6. 测试与依赖

- **`pyproject.toml`**：当前声明了 `pytest-playwright`、`pytest-unused-port` 等，用于浏览器页冒烟测试。
- 新增测试时，保持与现有测试一致：本地起静态服务、`page.goto` 到对应 `*.html`，用 `expect` 断言关键 UI。

---

## 7. 关键脚本速查

| 脚本 | 作用 |
|------|------|
| `gather_links.py` | 扫描根目录 `*.html`，结合 git 历史与 `*.docs.md` 生成 **`tools.json`** |
| `build_index.py` | 由 `README.md` 等生成 **`index.html`** |
| `build.sh` | 串联元数据、索引、footer 注入等 |
| `write_docs.py` | 可选：基于 HTML 生成/更新 `*.docs.md`（需 `GENERATE_LLM_DOCS=1` 与 `llm`） |

---

## 8. 检查清单（浏览器新工具）

- [ ] `slug.html` 在**仓库根目录**，`<title>` 已填。
- [ ] `slug.docs.md` 首段为面向用户的说明（无标题、2～4 句为宜）。
- [ ] 已跑 `gather_links.py` 或完整 `./build.sh`，`tools.json` 含新条目。
- [ ] 若需要曝光：已更新 **`README.md`** 对应分类。
- [ ] 关键路径已 **`pytest`** 或至少手动测过移动窄屏。
- [ ] 无提交密钥；第三方 Key 由用户输入或环境变量提供。

---

## 9. 给后续 LLM 的简短系统提示（可粘贴）

> 你在为 qlyan-tools 添加浏览器工具。请在仓库**根目录**创建 `{slug}.html` 与 `{slug}.docs.md`（docs 第一段为摘要）。HTML 需含 viewport，样式与现有工具一致（max-width 居中、box-sizing）。不要依赖构建步骤才能打开单文件。若需要收录与描述，说明运行 `gather_links.py` / `./build.sh` 更新 `tools.json`。需要首页展示时在 `README.md` 增加列表项。

按上述步骤，就可以把「我提供的一段代码」稳定地变成与本仓库一致的新工具。
