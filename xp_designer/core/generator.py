from .spec import ExperimentSpec, MetricSpec


def _format_metrics_bullets(metrics: list[MetricSpec]) -> str:
    if not metrics:
        return ""
    return "\n".join(f"- {m.name}" + (f"（{m.definition}）" if m.definition else "") for m in metrics)


def generate_from_context(context: str) -> ExperimentSpec:
    # MVP: placeholder content derived from context; later replace with LLM.
    objective = context.strip() or "实验目标待填写"
    metrics = [
        MetricSpec(name="D1_retention", type="core"),
        MetricSpec(name="ARPDAU", type="guardrail"),
    ]
    primary = [m for m in metrics if m.type == "core"]
    secondary = [m for m in metrics if m.type == "secondary"]
    guardrail = [m for m in metrics if m.type == "guardrail"]

    return ExperimentSpec(
        objective=objective,
        xp_background="根据实验目标补充背景与现状说明。",
        causal_reasoning="根据实验目标补充因果假设与推理链路。",
        xp_primary_metrics=_format_metrics_bullets(primary) or "- （待填写）",
        xp_secondary_metrics=_format_metrics_bullets(secondary) or "- （待填写）",
        xp_guardrail_metrics=_format_metrics_bullets(guardrail) or "- （待填写）",
        xp_user_segmentation="实验组 / 对照组，按 user_id 随机分流；可在此补充具体人群与分流比例。",
        xp_duration="建议 2 周，可根据指标敏感度调整。",
        xp_rollback_standard="SRM 异常或核心指标显著负向时回滚；可在此补充具体阈值。",
        xp_analysis_drilldown_dimensions="渠道、设备、地域等（按需填写）。",
        population="all_users",
        unit="user_id",
        metrics=metrics,
    )
