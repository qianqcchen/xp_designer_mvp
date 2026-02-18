from pydantic import BaseModel
from typing import List, Optional


class MetricSpec(BaseModel):
    name: str
    type: str  # core / secondary / guardrail
    definition: Optional[str] = None


class ExperimentSpec(BaseModel):
    objective: str
    xp_background: str = ""
    causal_reasoning: str = ""
    xp_primary_metrics: str = ""
    xp_secondary_metrics: str = ""
    xp_guardrail_metrics: str = ""
    xp_user_segmentation: str = ""
    xp_duration: str = ""
    xp_rollback_standard: str = ""
    xp_analysis_drilldown_dimensions: str = ""
    # Optional structured data for generator use
    population: Optional[str] = None
    unit: Optional[str] = None
    metrics: Optional[List[MetricSpec]] = None
