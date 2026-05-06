# AI Optimized by Skills Agent: Deterministic mock provider supports tests and reliable hackathon demos.
from app.services.ai.base import AIProvider


# AI Optimized by Skills Agent: Simple provider returns predictable payloads until real model adapters land.
class MockAIProvider(AIProvider):
    async def generate_json(
        self,
        *,
        task: str,
        system_prompt: str,
        user_payload: dict,
        schema_name: str,
    ) -> dict:
        return {
            "task": task,
            "schema_name": schema_name,
            "provider": "mock",
            "input_keys": sorted(user_payload.keys()),
            "summary": "Mock AI response generated for skeleton verification.",
        }
