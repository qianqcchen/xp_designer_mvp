from pydantic import BaseModel
from typing import List, Optional

class MetricSpec(BaseModel):
    name: str
    type: str  # core / secondary / guardrail
    definition: Optional[str] = None

class ExperimentSpec(BaseModel):
    objective: str
    population: str
    unit: str
    metrics: List[MetricSpec]