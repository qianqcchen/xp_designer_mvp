from __future__ import annotations
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def _metrics_to_rows(metrics_str: str) -> list[tuple[str, str]]:
    """Parse bullet-list metrics string into (name, definition) rows for table display.
    Accepts: "- name（definition）" or "- name：definition" or "- name"
    """
    if not metrics_str or not metrics_str.strip():
        return []
    rows = []
    for line in metrics_str.strip().split("\n"):
        line = line.strip()
        if not line or not line.startswith("-"):
            continue
        text = line.lstrip("- ").strip()
        # Match "name（definition）"
        m = re.match(r"^(.+?)（(.+)）$", text)
        if m:
            rows.append((m.group(1).strip(), m.group(2).strip()))
        # Match "name：definition"
        elif "：" in text:
            name, _, defn = text.partition("：")
            rows.append((name.strip(), defn.strip()))
        else:
            rows.append((text, ""))
    return rows


def render_markdown(spec, template_name: str = "default.md.j2") -> str:
    templates_dir = Path(__file__).resolve().parents[1] / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["metrics_to_rows"] = _metrics_to_rows
    tmpl = env.get_template(template_name)
    return tmpl.render(spec=spec)