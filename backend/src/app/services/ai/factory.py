# AI Optimized by Skills Agent: Provider factory centralizes AI_PROVIDER selection for business services.
from app.core.config import Settings, settings
from app.services.ai.base import AIProvider
from app.services.ai.mock_provider import MockAIProvider


class UnsupportedAIProviderError(ValueError):
    """Raised when AI_PROVIDER names an adapter that is not available yet."""


# AI Optimized by Skills Agent: Keeps vendor SDK choices out of route and service modules.
def get_ai_provider(config: Settings = settings) -> AIProvider:
    provider_name = config.ai_provider.strip().lower()

    if provider_name == "mock":
        return MockAIProvider()

    supported = "mock"
    raise UnsupportedAIProviderError(
        f"Unsupported AI provider '{config.ai_provider}'. Supported providers: {supported}."
    )
