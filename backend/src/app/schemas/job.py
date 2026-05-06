# AI Optimized by Skills Agent: Initial job schema module reserved for JobPost and JobAnalysis contracts.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Minimal placeholder keeps future endpoint contracts typed from day one.
class JobAnalysisSummary(BaseModel):
    title: str
    required_skills: list[str]
    keywords: list[str]
