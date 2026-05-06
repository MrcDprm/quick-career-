# AI Optimized by Skills Agent: Initial metrics schema module for 50 percent reduction proof.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Captures manual-vs-automated effort comparison.
class EfficiencyMetricSummary(BaseModel):
    workflow_name: str
    manual_steps: int
    automated_steps: int
    reduction_percent: float
