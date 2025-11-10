"""MessageData data class for notification messages."""

from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class MessageData:
    """Data class representing a notification message.
    
    Attributes:
        subject: Message subject line
        content: Message content/body
        job_count: Number of jobs in the message
        channels: List of notification channels (e.g., ['gmail', 'telegram'])
        created_at: Timestamp when message was created (auto-generated if None)
    """
    subject: str
    content: str
    job_count: int
    channels: List[str]
    created_at: datetime = None
    
    def __post_init__(self):
        """Set created_at to current time if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
