"""Telegram notification provider implementation."""

import asyncio
from telegram import Bot
from src.notification_service.notifier_interface import NotifierInterface

class TelegramProvider(NotifierInterface):
    """Telegram notification provider using python-telegram-bot."""
    
    def __init__(self, bot_token: str, chat_id: str, max_message_length: int) -> None:
        """Initialize the Telegram provider.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
            max_message_length: The maximum message length for the notifier
        """
        super().__init__(max_message_length=max_message_length)
        self.bot_token = bot_token
        self.chat_id = chat_id
    
    def _send_notification(self, message: str) -> None:
        """Send a notification message to Telegram.
        
        Args:
            message: Message text to send
        """
        asyncio.run(self._send_message_async(message))
    
    async def _send_message_async(self, message: str) -> None:
        """Async method to send Telegram message.
        
        Args:
            message: Message text to send
        """
        bot = Bot(token=self.bot_token)
        await bot.send_message(
            chat_id=self.chat_id,
            text=message,
            disable_web_page_preview=True
        )

