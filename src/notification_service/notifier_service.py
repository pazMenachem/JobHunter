"""Notification service for managing different notification providers."""

from typing import List
from src.notification_service.notifier_interface import NotifierInterface
from src.notification_service.factory import NotifierFactory
from src.data_models import SegmentedMessage
from src.logger import get_logger
from src.exceptions.exceptions import NotifierException


class NotifierService:
    """Service for managing notification providers and sending messages."""
    
    def __init__(self, *, provider_names: List[str]) -> None:
        """Initialize the notifier service.
        
        Args:
            provider_names: The names of the providers to set
        """
        self.logger = get_logger("notifier_service")
        self.providers: List[NotifierInterface] = []
        self.set_providers(provider_names=provider_names)

        self.logger.info("Notifier service initialized...")
    
    def set_providers(self, *, provider_names: List[str]) -> None:
        """Set the notification providers.
        
        Args:
            provider_names: The names of the providers to set
        """
        if not provider_names:
            raise ValueError("Provider names cannot be empty")
        
        for provider_name in provider_names:
            provider = NotifierFactory.create_provider(provider_name)
            self.providers.append(provider)
            self.logger.info(f"Notification provider {provider_name} added")
    
    def send_notification(self, provider: NotifierInterface, message: SegmentedMessage) -> None:
        """Send segmented notification to a specific provider.
        
        Args:
            provider: The notification provider to send to
            message: SegmentedMessage object with header and message_parts
        """
        self.logger.info(f"Sending notification to {provider.__class__.__name__}")
            
        try:
            if message.header:
                provider.send_notification(message=message.header)
            
            total_parts = len(message.message_parts)
            for i, part in enumerate(message.message_parts):
                if total_parts > 1:
                    content = f"Part {i + 1}/{total_parts}\n\n{part}"
                else:
                    content = part
                
                provider.send_notification(message=content)

        except Exception as e:
            self.logger.error(f"Error sending notification to {type(provider).__name__}: {e}")
            raise NotifierException()

