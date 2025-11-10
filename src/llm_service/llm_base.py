"""Abstract interface for LLM providers."""

from abc import ABC, abstractmethod
from src.logger import get_logger

class LLMInterface(ABC):
    """Abstract base class for LLM providers.
    
    This interface allows easy switching between different LLM providers
    (Ollama, OpenAI, Gemini, etc.) without changing the rest of the code.
    """
    def __init__(self) -> None:
        """Initialize the LLM interface."""
        self.logger = get_logger("LLM_Service")

    def send_to_llm(self, message: str) -> str:
        """Send a message to the LLM and get the raw response.
        
        Args:
            message: The message to send to the LLM
            
        Returns:
            Raw response from the LLM (JSON string for LLM processing)
        """
        self.logger.info(f"Sending message to LLM: {message}")
        response = self._send_to_llm(message)
        self.logger.info(f"Received response from LLM: {response}")
        return response

    @abstractmethod
    def _setup(self) -> None:
        """Setup the LLM provider."""
        pass

    @abstractmethod
    def _send_to_llm(self, prompt: str) -> str:
        """Send a prompt to the LLM and get the raw response."""
        pass
    