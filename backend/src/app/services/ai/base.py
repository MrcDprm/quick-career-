# AI Optimized by Skills Agent: Provider interface keeps AI vendors outside business services.
from typing import Protocol


# AI Optimized by Skills Agent: Structured AI generation contract for job, resume and optimization agents.
class AIProvider(Protocol):
    async def generate_json(
        self,
        *,
        task: str,
        system_prompt: str,
        user_payload: dict,
        schema_name: str,
    ) -> dict:
        ...
