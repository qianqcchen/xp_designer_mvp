from .spec import ExperimentSpec, MetricSpec

def generate_from_context(context: str) -> ExperimentSpec:
    # MVP：placeholder
    return ExperimentSpec(
        objective=context,
        population="all_users",
        unit="user_id",
        metrics=[
            MetricSpec(name="D1_retention", type="core"),
            MetricSpec(name="ARPDAU", type="guardrail"),
        ],
    )