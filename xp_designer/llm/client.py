from __future__ import annotations

import json
from pathlib import Path

from openai import OpenAI

from xp_designer.core.metrics_lib import load_metrics_spec
from xp_designer.core.spec import ExperimentSpec
from xp_designer.llm.config import get_api_key

_DEFAULT_METRICS_PATH = Path(__file__).resolve().parents[2] / "specs" / "metrics.yaml"

_PROMPT_TEMPLATE = """你是一个实验设计专家。根据用户提供的实验背景/需求描述，填写一份完整的实验设计规范（ExperimentSpec）。

## 可用指标库（必须从中选择填入 xp_primary_metrics、xp_secondary_metrics、xp_guardrail_metrics）

{metrics_list}

核心指标(xp_primary_metrics)：与实验目标最直接相关的1-3个指标。
次级指标(xp_secondary_metrics)：辅助观察的指标。
护栏指标(xp_guardrail_metrics)：需监控以防负向影响的指标（如收入、留存等）。

## 输出格式

请以 JSON 格式返回，字段如下（所有字符串字段均使用中文）：
- objective: 实验目标（一句话）
- xp_background: 实验背景与现状说明
- causal_reasoning: 因果假设与推理链路
- xp_primary_metrics: 一到两个核心指标，每行一个，格式为 "- 指标中文名（定义）"，必须从上述指标库选择
- xp_secondary_metrics: 次级指标，数量不限，同上格式
- xp_guardrail_metrics: 护栏指标，数量不限，同上格式
- xp_user_segmentation: 用户分流说明（实验组/对照组、分流比例、人群定义等）
- xp_duration: 实验时长建议
- xp_rollback_standard: 回滚标准（SRM异常、核心指标显著负向时回滚等）
- xp_analysis_drilldown_dimensions: 分析下钻维度（如渠道、设备、地域等）

只返回 JSON，不要其他文字。"""


def _format_metrics_for_prompt(metrics: dict) -> str:
    """Format metrics YAML data as a readable list for the prompt."""
    lines = []
    by_group = {}
    for key, m in metrics.items():
        if not isinstance(m, dict):
            continue
        group = m.get("group", "其他")
        subgroup = m.get("subgroup", "")
        display = m.get("display_name_zh", key)
        definition = m.get("definition", "")
        by_group.setdefault((group, subgroup), []).append((display, definition))

    for (group, subgroup), items in sorted(by_group.items()):
        header = f"{group} / {subgroup}" if subgroup else group
        lines.append(f"【{header}】")
        for display, definition in sorted(items, key=lambda x: x[0]):
            lines.append(f"- {display}：{definition}")
        lines.append("")

    return "\n".join(lines).strip()


def _build_system_prompt(metrics_path: Path | str | None = None) -> str:
    path = Path(metrics_path) if metrics_path else _DEFAULT_METRICS_PATH
    metrics = load_metrics_spec(str(path)) if path.exists() else {}
    metrics_list = _format_metrics_for_prompt(metrics) if metrics else "（无预设指标库，请根据实验上下文填写）"
    return _PROMPT_TEMPLATE.format(metrics_list=metrics_list)


def fill_spec(
    context: str,
    model: str = "gpt-4o",
    metrics_path: str | Path | None = None,
) -> ExperimentSpec:
    """Fill an ExperimentSpec from natural language context using the GPT API."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Set OPENAI_API_KEY or add your key to xp_designer/llm/.api_key"
        )

    system_prompt = _build_system_prompt(metrics_path)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context.strip() or "请帮我设计一个实验。"},
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from GPT API")

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GPT response as JSON: {e}") from e

    return ExperimentSpec(**parsed)
