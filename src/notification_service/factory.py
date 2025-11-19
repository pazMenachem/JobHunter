"""Factory for creating notification providers."""

from src.notification_service.notifier_interface import NotifierInterface
from src.notification_service.telegram_provider import TelegramProvider
from src.notification_service.gmail_provider import MailProvider
from src.config import telegram_settings, mail_settings

class NotifierFactory:
    """Factory class for creating notifier providers based on configuration."""
    
    @staticmethod
    def create_provider(provider_type: str) -> NotifierInterface:
        """
        Create and return the appropriate notifier provider based on configuration.
        """
        match provider_type.lower():
            case "mail":
                return NotifierFactory._create_mail_provider()
            case "telegram":
                return NotifierFactory._create_telegram_provider()
            case _:
                raise ValueError(f"Unsupported notifier provider: {provider_type}")
    
    @staticmethod
    def _create_telegram_provider() -> TelegramProvider:
        """Create a Telegram provider instance."""
        if telegram_settings.enabled:
            return TelegramProvider(
                bot_token=telegram_settings.bot_token,
                chat_id=telegram_settings.chat_id,
                max_message_length=telegram_settings.max_message_length
                )
        raise ValueError("Telegram notifications are not enabled")
    
    @staticmethod
    def _create_mail_provider() -> MailProvider:
        """Create a mail provider instance."""
        if mail_settings.enabled:
            return MailProvider(
                sender_email=mail_settings.sender_email,
                sender_password=mail_settings.sender_password,
                recipient_email=mail_settings.recipient_email,
                smtp_server=mail_settings.smtp_server,
                smtp_port=mail_settings.smtp_port,
                max_message_length=mail_settings.max_message_length
            )
        raise ValueError("Mail notifications are not enabled - check .env configuration")