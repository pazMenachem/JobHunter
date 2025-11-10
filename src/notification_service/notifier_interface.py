"""Abstract base class for notification providers."""

from abc import ABC, abstractmethod
from src.logger import get_logger

class NotifierInterface(ABC):
    """Abstract base class for all notifiers providers.
    
    This class defines the interface that all notifiers providers must implement.
    It provides a common structure for sending job notifications via different channels.
    """
    def __init__(self, *, max_message_length: int) -> None:
        """Initialize the notifier interface.
        
        Args:
            max_message_length: The maximum message length for the notifier
        """
        self.logger = get_logger("notifier_service")
        self.max_message_length: int = max_message_length

    def send_notification(self, *, message: str) -> None:
        """Send a notification message.
        
        Args:
            message: The message string to send
            
        Raises:
            Exception: If notification fails
        """
        
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        try:
            self.logger.info(f"Sending message to user")
            self._send_notification(message)
            self.logger.info("Message sent successfully")
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise RuntimeError(f"Error sending message: {e}")
    
    @abstractmethod
    def _send_notification(self, message: str) -> None:
        """Send a notification message (concrete implementation).
        
        Args:
            message: The message string to send
            
        Raises:
            Exception: If notification fails
        """
        pass
