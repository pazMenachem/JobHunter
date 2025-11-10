"""SegmentedMessage data class for handling long notification messages."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class SegmentedMessage:
    """Container for segmented notification message.
    
    This class holds a message that has been intelligently split into
    multiple parts to respect provider length limits (e.g., Telegram's 4096 chars).
    
    Attributes:
        header: Optional header sent first (e.g., summary statistics)
        message_parts: List of message segments (each < max_length)
    """
    header: str = ""
    message_parts: List[str] = field(default_factory=list)
