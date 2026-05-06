# AI Optimized by Skills Agent: Initial optimization schema module for autonomous CV rewrite contracts.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Captures autonomous before/after changes for trace UI.
class OptimizationDiffItem(BaseModel):
    section: str
    before: str
    after: str
