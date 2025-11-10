from src.config import llm_settings
from src.llm_service.llm_base import LLMInterface
from src.llm_service.gemini_provider import GeminiProvider


class LLMProviderFactory:
    """Factory class for creating LLM providers based on configuration."""
    
    @staticmethod
    def create_provider(provider_type: str = llm_settings.llm_provider) -> LLMInterface:
        """
        Create and return the appropriate LLM provider based on configuration.

        Args:
            provider_type: The type of LLM provider to create (default: gemini).
        
        Returns:
            LLMInterface: The configured LLM provider instance.
            
        Raises:
            ValueError: If the configured provider is not supported.
        """
        
        match provider_type.lower():
            case "gemini":
                return GeminiProvider()
            case _:
                raise ValueError(f"Unsupported LLM provider: {provider_type}")
