"""Gemini Flash API provider for batch job filtering."""

from google import genai
from google.genai.types import GenerateContentConfig
from src.logger import get_logger
from src.llm_service.llm_base import LLMInterface
from src.config import llm_settings


class GeminiProvider(LLMInterface):
    """Gemini Flash API provider for batch job analysis.
    
    NOTE: Gemini flash module is limited to 20 urls in a single request.
    This provider uses Google's Gemini Flash API to analyze multiple jobs
    in a single batch request, providing efficient and cost-effective filtering.
    """
    
    def __init__(self) -> None:
        """Initialize the Gemini provider."""
        self.logger = get_logger("gemini_provider")
        self.model = None
        
        self._setup()
        self.logger.info("Gemini provider initialized...")
        
    def _setup(self) -> None:
        """Setup the Gemini provider."""
        if not llm_settings.enabled:
            raise ValueError("gemini provider is not enabled")

        self.client = genai.Client(api_key=llm_settings.api_key)
        self.model_id = llm_settings.llm_model

    def _send_to_llm(self, prompt: str) -> str:
        """Send a prompt to the Gemini API and get the raw response.

        Args:
            prompt: The prompt to send to the LLM

        Returns:
            Raw response from the LLM (JSON string for batch processing)
        """
        
        # Configure tools for URL context
        tools = [{"url_context": {}}]
        
        # Configure generation config for URL context
        config = GenerateContentConfig(
            tools=tools
        )
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=config
        )
        
        if not response.text:
            raise RuntimeError("Empty response from Gemini API")
        
        return response.text
