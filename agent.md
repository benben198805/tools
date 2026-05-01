# qlyan-tools — Agent Guide

> 本仓库 fork 自 [simonw/tools](https://github.com/simonw/tools)（Apache 2.0），是 Simon Willison 的 "tools.simonwillison.net" 站点的本地化版本。主体是大量**根目录下的单文件 HTML/JS 浏览器小工具**，辅以 **`python/` 目录下的 CLI 脚本**和少量**基础设施脚本**。站点的功能是为各种小型、实用的浏览器端工具提供托管，这些工具大多由 LLM 辅助生成。

---

## 目录结构总览

```
.
├── {slug}.html              # 浏览器工具（根目录，约 200+ 个）
├── {slug}.docs.md           # 同名工具的简要文档（首段 = 首页摘要）
├── python/
│   ├── {name}.py            # CLI 脚本，配合 uv run 使用
│   └── README.md            # 所有 Python 脚本的索引和用法文档
├── tests/
│   ├── conftest.py          # pytest fixtures（StaticServer、unused_port）
│   ├── test_quickjs.py      # Playwright 浏览器测试示例
│   ├── test_sloccount.py    # 另一个 Playwright 测试示例
│   └── cooking-timer.spec.js # Playwright JS 测试示例
├── bash/
│   └── *.sh                 # 辅助 shell 脚本
├── vercel/
│   └── anthropic-proxy/     # Vercel Serverless 代理（CORS 代理到 Anthropic API）
├── lib/
│   └── gifsicle/            # 子模块：gifsicle build
├── build*.py                # 构建/元数据脚本（见下方"基础设施脚本"）
├── gather_links.py          # 核心：扫描 *.html 生成 tools.json
├── build.sh                 # 完整构建入口
├── tools.json               # 自动生成的工具元数据（供首页/by-month 页使用）
├── _redirects.json          # URL 重定向映射
├── _config.yml              # Jekyll 配置（GitHub Pages 用）
├── CNAME                    # 自定义域名
├── README.md                # 首页内容源（markdown，被 build_index.py 转为 index.html）
├── llm-lib.js               # 共享库：统一浏览器 LLM API（支持 OpenAI/Anthropic/Gemini）
└── footer.js                # 所有工具页自动注入的 footer
```

---

## 两种工具形态

### 1. 浏览器工具（根目录 `{slug}.html`）

最常用的工具形态。纯前端 HTML+JS，放在仓库根目录。

**文件约定：**
- `{slug}.html` — 单文件自包含工具页
- `{slug}.docs.md` — 简短 Markdown 文档，**首段必须是面向用户的工具说明（2-4 句）**，用于 `tools.json` 的 `description` 字段

**技术特征：**
- 单页自包含，无构建步骤即可直接在浏览器打开
- `<!DOCTYPE html>`、`charset`、`viewport` 必须
- CSS：`box-sizing: border-box`、`max-width` 居中、`@media` 移动端适配
- 交互：实时反馈、错误信息单独区域、`navigator.clipboard.writeText` 优先
- 外链库：从 jsDelivr/CDNJS 引入，尽量固定版本号
- 可复用 `llm-lib.js`（需 LLM API 调用时）
- footer 在 build 时自动注入（`build.sh` 会在 `</body>` 前插入 `footer.js` 引用）

**哪些文件不参与 `tools.json` 索引：**
- 子目录中的 `.html` 不被 `gather_links.py` 扫描
- `index.html` 不被扫描
- 其他如 `python/`、`tests/`、`vercel/` 等子目录都不被扫描
- 新工具放在根目录才能被收录

### 2. Python CLI 脚本（`python/{name}.py`）

独立的命令行脚本，通常用 `uv run` 直接执行。

**文件约定：**
- `python/{name}.py` — 脚本本身
- 常见使用 **PEP 723 内联元数据**（`# /// script` 头），便于 `uv run URL` 自动安装依赖
- 在 `python/README.md` 中为每个脚本增加一节：用途 + `uv run` 示例
- **不进入** `tools.json`，发现与分发靠 `python/README.md`
- 示例：`python/mistral_ocr.py`、`python/gguf_inspect.py`

**Python 脚本与浏览器工具的区别：**
| 维度 | 浏览器工具 | Python CLI 脚本 |
|------|-----------|-----------------|
| 位置 | 根目录 `{slug}.html` | `python/{name}.py` |
| 元数据 | `gather_links.py` → `tools.json` | 不进入 `tools.json` |
| 文档 | `{slug}.docs.md` (首段) | `python/README.md` (整节) |
| 依赖管理 | CDN 固定版本 | PEP 723 `# /// script` / `uv run` |
| 运行环境 | 浏览器 | 本地 Python |

---

## 核心基础设施脚本（按构建顺序）

| 脚本 | 功能 | 在 `build.sh` 中的顺序 |
|------|------|----------------------|
| `gather_links.py` | 扫描根目录 `*.html`，从 git 历史提取创建/更新时间，从 `*.docs.md` 提取描述，生成 `tools.json` | 1 |
| `write_docs.py` | 可选：用 `llm` CLI 基于 HTML 生成/更新 `*.docs.md`（需环境变量 `GENERATE_LLM_DOCS=1`） | 2（条件执行） |
| `build_colophon.py` | 生成 colophon 页面，列出每个工具的 git 提交历史 | 3 |
| `build_dates.py` | 生成 `dates.json`，含每个工具的日期信息 | 4 |
| `build_index.py` | 将 `README.md` 转为 `index.html`，注入"最近添加"和"最近更新"部分 | 5 |
| `build_by_month.py` | 按月分组工具列表 → `by-month.html` | 6 |
| 注入 footer.js | 为每个根目录 `*.html`（不含 index.html）插入版本化 `footer.js` 引用 | 7 |
| `build_redirects.py` | 从 `_redirects.json` 生成静态重定向页面 | 8 |

`build.sh` 是完整构建入口，建议新增工具后运行 `python gather_links.py` 更新 `tools.json`。

---

## 测试体系

- **`tests/conftest.py`**：提供 `unused_port` fixture 和 `StaticServer` 类（启动 `python -m http.server` 做静态文件服务）
- **Playwright Python 测试**（如 `test_quickjs.py`、`test_sloccount.py`）：
  - 使用 `page` fixture + `unused_port_server` fixture
  - `unused_port_server.start(root)` 启动服务
  - `page.goto(...)`，然后用 `expect()` 断言
  - CDN 依赖测试可用 `pytest.mark.skipif` 条件跳过
- **Playwright JS 测试**（如 `cooking-timer.spec.js`）：
  - 独立 JS 测试文件，用 `@playwright/test` 框架
  - 需要自行配置服务器地址
- 运行测试：
  ```bash
  pip install -e . && playwright install && pytest
  ```

---

## 新增浏览器工具的标准流程

### 步骤 1：确认形态 → 浏览器工具

绝大多数新增需求都对应根目录浏览器工具。

### 步骤 2：创建文件

1. **`{slug}.html`** — 在仓库根目录创建
   - 设置正确的 `<title>`（用于 `tools.json` 里的工具名）
   - 包含 `viewport`
   - 样式对齐现有工具风格
   - 自包含，不需要构建步骤就能直接打开

2. **`{slug}.docs.md`** — 在仓库根目录创建
   - **首段必须是 2-4 句面向用户的工具说明**（无标题），用于 `tools.json` 的 description
   - 不要以"This tool is..." 开头，而应以 "Do X..." 或 "Convert/View/Analyze..." 开头
   - 第二段起可以放生成标记注释，如 `<!-- Generated from commit: ... -->`

3. **`README.md`** — 在合适分类下增加一行：`- [Tool name](https://tools.simonwillison.net/{slug}) 一句话说明`

### 步骤 3：运行构建

```bash
python gather_links.py         # 更新 tools.json
```

验证 `tools.json` 中包含了新增工具条目。

### 步骤 4：编写测试（可选但推荐）

在 `tests/` 下创建 `test_{slug}.py`，用 Playwright 做 1-2 个冒烟测试：
- 页面加载测试
- 核心交互测试
- 移动端适配检查

---

## 新增 Python CLI 脚本的标准流程

### 步骤 1：确认形态 → Python 脚本

适合需要本地环境、API Key、文件系统访问、批处理操作的场景。

### 步骤 2：创建文件

1. **`python/{name}.py`** — 在 `python/` 目录创建
   - **必须**包含 PEP 723 内联元数据头（`# /// script`），方便 `uv run URL` 执行
   - CLI 参数建议用 `argparse` 或 `click`
   - 支持 `--help`
   - 使用 `from __future__ import annotations`（项目约定）

2. **`python/README.md`** — 在对应分类增加一节，包含：
   - **用途说明**
   - **`uv run` 完整示例**
   - **依赖说明**（标准库还是第三方）
   - **输出示例**（可选）

### 步骤 3：验证

```bash
uv run python/{name}.py --help
```

---

## 关键约定与最佳实践

### 命名
- slug 用小写字母 + 连字符（kebab-case）
- `<title>` 和 `<h1>` 用可读性标题，大小写正常

### 样式
- `* { box-sizing: border-box; }`
- `body { max-width: 800px; margin: 0 auto; padding: 20px; }`
- `@media (max-width: 600px)` 收紧间距
- 参考 `word-counter.html`、`date-calculator.html` 等现有工具的风格

### 安全性
- 不将 API Key 硬编码在 HTML/Python 中
- 用户 API Key 由用户在本页粘贴输入或通过环境变量提供
- 第三方 Key 的获取方式在 `*.docs.md` 中说明

### Python 脚本
- PEP 723 内联元数据头（`# /// script`）优先
- `from __future__ import annotations`
- 不引入过多依赖，优先标准库
- 如果脚本需要 API Key，读环境变量（如 `MISTRAL_API_KEY`）
- `argparse` 支持友好的 `--help`

### git 提交
- 每次新增/更新工具后建议提交，因为 `gather_links.py` 依赖 git 时间戳
- 提交信息可用工具说明或 Claude 的对话链接

---

## 文件模板

### HTML 工具模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tool Name</title>
<style>
* { box-sizing: border-box; }
body {
  font-family: Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background: #f5f5f5;
}
.container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
h1 { color: #333; margin-bottom: 20px; }
textarea, input, button { font-size: 16px; }
@media (max-width: 600px) {
  body { padding: 10px; }
  .container { padding: 15px; }
}
</style>
</head>
<body>
<div class="container">
<h1>Tool Name</h1>
<!-- content -->
</div>
<script>
// logic
</script>
</body>
</html>
```

### `{slug}.docs.md` 模板

```markdown
首段：简明扼要说明工具的功能、输入和输出，2-4 句。以 "Do/Convert/View/Analyze..." 等动词开头，不用 "This tool is..."

<!-- Generated from commit: abc123... -->
```

### Python 脚本模板

```python
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

from __future__ import annotations

import argparse


def main():
    parser = argparse.ArgumentParser(description="...")
    # add arguments
    args = parser.parse_args()


if __name__ == "__main__":
    main()
```

---

## 常见问题

**Q: 新工具没有出现在首页怎么办？**
A: 检查两件事：(1) 确认运行了 `python gather_links.py` 且 `tools.json` 中出现了新条目；(2) 确认在 `README.md` 的分类列表中增加了链接行。`build_index.py` 同时依赖这两个来源。

**Q: 工具引用 CDN 资源没加载？**
A: 检查 CDN URL 是否可访问，建议固定版本号（如 `@3.0.0` 而非 `@3`）。部分浏览器安全策略可能需要 CORS 头。

**Q: Python 脚本如何在浏览器中展示结果？**
A: 考虑两种方案：(1) 保持为独立的 CLI 脚本，在 `python/README.md` 中说明；(2) 将核心逻辑用 Pyodide/WASM 移植为浏览器工具（更复杂，但可被首页索引）。
