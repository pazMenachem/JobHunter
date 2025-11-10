"""SearchRequest data class for search parameters."""

from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class SearchRequest:
    """Data class representing a search request.
    
    Attributes:
        urls: List of URLs to search
        keywords: List of keywords to search for
        max_pages: Maximum pages to scrape per URL (default: 5)
        delay_seconds: Delay between requests in seconds (default: 1.0)
        created_at: Timestamp when request was created (auto-generated if None)
    """
    urls: List[str]
    keywords: List[str]
    max_pages: int = 5
    delay_seconds: float = 1.0
    created_at: datetime = None
    
    def __post_init__(self):
        """Set created_at to current time if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
