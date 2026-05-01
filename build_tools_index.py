#!/usr/bin/env python3
"""
Generate TOOLS_INDEX.md — a comprehensive, AI-friendly index of all tools.

Combines:
  - Browser tools (from tools.json)
  - Python CLI scripts (parsed from python/README.md)

Output is a single Markdown file structured for quick LLM scanning:
  - Category headers
  - Per-tool: name, one-line purpose, filename, usage hint
"""

from __future__ import annotations

import json
import re
from pathlib import Path


TOOLS_JSON = Path("tools.json")
PYTHON_README = Path("python/README.md")
OUTPUT = Path("TOOLS_INDEX.md")


def load_browser_tools() -> list[dict]:
    """Load browser tools from tools.json."""
    if not TOOLS_JSON.exists():
        return []
    with TOOLS_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_tool_name(description: str, html_file: str, slug: str) -> str:
    """Extract a clean tool name from the title or description."""
    return slug


def parse_python_readme() -> list[dict]:
    """Parse python/README.md into tool entries.

    Each tool section starts with '## name.py' and contains
    descriptive text before the next section or a code block.
    """
    if not PYTHON_README.exists():
        return []

    text = PYTHON_README.read_text("utf-8")
    tools = []

    # Match sections like '## name.py' or '## name.md'
    pattern = re.compile(
        r"^## (.+\.py)\s*$([\s\S]+?)(?=^## |\Z)",
        re.MULTILINE,
    )

    for match in pattern.finditer(text):
        filename = match.group(1).strip()
        body = match.group(2).strip()

        # Extract first sentence as description (before code block or next section)
        desc_lines = []
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                break
            if stripped and not stripped.startswith("#"):
                desc_lines.append(stripped)

        description = " ".join(desc_lines).strip()
        # Clean up: remove extra spaces
        description = re.sub(r"\s+", " ", description).strip()
        # Remove markdown formatting for clean plain-text description
        description = description.replace("**", "")
        description = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", description)

        # Extract the first bash code block as usage example
        usage_match = re.search(
            r"```bash\n(.+?)\n```", body, re.DOTALL
        )
        usage = usage_match.group(1).strip() if usage_match else ""

        tools.append({
            "filename": filename,
            "description": description,
            "usage": usage,
        })

    return tools


def slug_to_tool_type(slug: str) -> str:
    """Categorize a tool based on its slug/description."""
    # Simple heuristic-based categorization
    image_keywords = ["image", "svg", "png", "jpg", "jpeg", "gif", "photo",
                      "thumbnail", "icon", "avatar", "crop", "resize", "mask",
                      "visualizer", "bbox", "ocr", "pdf", "tiff"]
    text_keywords = ["markdown", "json", "yaml", "xml", "html", "rtf",
                     "transcript", "clipboard", "word", "counter", "text",
                     "diff", "indentation", "escape", "pretty"]
    data_keywords = ["date", "time", "timestamp", "timezone", "token",
                     "csv", "map", "calculator", "transfer", "convert"]
    code_keywords = ["github", "git", "sql", "python", "quickjs", "wasm",
                     "pipfile", "schema", "debug", "graphiql"]
    social_keywords = ["bluesky", "hacker", "lobsters", "passkeys", "broadcast"]
    llm_keywords = ["claude", "gemini", "openai", "llm", "prompt", "haiku",
                    "token", "gpt", "chat"]
    dev_keywords = ["codex", "claude-code", "git", "github", "deploy",
                    "side-panel", "dialog", "iframe", "keyboard", "webc"]

    s = slug.lower()
    for kw_list, category in [
        (image_keywords, "Image & Media"),
        (text_keywords, "Text & Document"),
        (data_keywords, "Data & Time"),
        (code_keywords, "Development"),
        (social_keywords, "Social"),
        (llm_keywords, "LLM & AI"),
        (dev_keywords, "Development"),
    ]:
        if any(kw in s for kw in kw_list):
            return category
    return "Miscellaneous"


def generate_index() -> str:
    lines = []
    lines.append("# Tools Index")
    lines.append("")
    lines.append(
        "Comprehensive index of all tools in this repository, "
        "structured for quick AI agent scanning. "
        "Updated: auto-generated from `tools.json` and `python/README.md`."
    )
    lines.append("")

    # ── Browser tools ──────────────────────────────────────────
    browser_tools = load_browser_tools()
    if browser_tools:
        lines.append("## Browser Tools")
        lines.append("")
        lines.append(
            "Single-file HTML pages in the repository root. "
            "Open directly in a browser. "
            "Each has a companion `{slug}.docs.md` with detailed documentation."
        )
        lines.append("")

        # Group by category
        categories: dict[str, list[dict]] = {}
        for tool in browser_tools:
            cat = slug_to_tool_type(tool.get("slug", ""))
            categories.setdefault(cat, []).append(tool)

        for cat_name in sorted(categories.keys()):
            lines.append(f"### {cat_name}")
            lines.append("")
            for tool in sorted(categories[cat_name],
                               key=lambda t: t.get("slug", "")):
                slug = tool.get("slug", "")
                title = tool.get("title", slug)
                desc = tool.get("description", "")
                url = tool.get("url", f"/{slug}")

                # Truncate description to first sentence for compactness
                first_sent = desc.split(".")[0].strip()
                if first_sent:
                    first_sent += "."

                lines.append(f"- **{title}**")
                lines.append(f"  - File: `{slug}.html`")
                lines.append(f"  - Purpose: {first_sent if first_sent else desc}")
                lines.append("")

        lines.append("---")
        lines.append("")

    # ── Python CLI Tools ───────────────────────────────────────
    python_tools = parse_python_readme()
    if python_tools:
        lines.append("## Python CLI Scripts")
        lines.append("")
        lines.append(
            "Standalone Python scripts for CLI use. "
            "Run with `uv run` — dependencies are fetched automatically "
            "via PEP 723 inline metadata."
        )
        lines.append("")

        for tool in sorted(python_tools, key=lambda t: t["filename"]):
            filename = tool["filename"]
            desc = tool["description"]
            usage = tool["usage"]

            # Compact single-line entry: bold filename → description
            desc_clean = desc.split(".")[0].strip()
            if desc_clean:
                desc_clean += "."
            lines.append(f"- **`{filename}`** — {desc_clean}")
            if usage:
                lines.append(f"  - Run: `{usage}`")
            lines.append("")

        lines.append("---")
        lines.append("")

    # ── How to use this index ──────────────────────────────────
    lines.append("## For AI Agents")
    lines.append("")
    lines.append(
        "This index is designed for quick lookup. "
        "To find a tool for a specific task:"
    )
    lines.append("")
    lines.append(
        "1. Scan the category headers in **Browser Tools** "
        "or **Python CLI Scripts**."
    )
    lines.append(
        "2. Read the **Purpose** line to see if the tool matches."
    )
    lines.append(
        "3. Open `{slug}.html` for browser tools or "
        "`python/{filename}` for CLI scripts to see implementation."
    )
    lines.append(
        "4. Browser tools also have `{slug}.docs.md` with detailed docs."
    )
    lines.append("")
    lines.append(
        "When adding a new tool, update this index by running:\n"
        "```bash\n"
        "python build_tools_index.py\n"
        "```"
    )

    return "\n".join(lines)


if __name__ == "__main__":
    index_content = generate_index()
    OUTPUT.write_text(index_content, "utf-8")
    print(f"TOOLS_INDEX.md generated ({len(index_content)} chars)")
