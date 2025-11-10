"""JobHunter - Automated Job Search and Filtering Application.

This package provides a comprehensive job hunting solution that:
- Crawls job listings from company career pages
- Filters jobs using LLM analysis with URL context
- Sends notifications via Telegram/Gmail
- Manages job data and configurations
"""

# Core data models
from .data_models.job_data import JobData, RelevanceStatus
from .data_models.search_request import SearchRequest
from .data_models.run_summary import RunSummary
from .data_models.message_data import MessageData

# Configuration
from .config import (
    browser_settings,
    scraping_settings,
    output_settings,
    job_filter_settings,
    llm_settings
)

# LLM Service
from .llm_service.factory import LLMProviderFactory
from .llm_service.llm_service import LLMService

# Notification Service
from .notification_service.factory import NotifierFactory

# Message Formatter
from .message_formatter import MessageFormatterService

# Logger
from .logger import get_logger

__version__ = "1.0.0"
__author__ = "JobHunter Team"

# Main exports for easy access
__all__ = [
    # Data Models
    "JobData",
    "RelevanceStatus", 
    "SearchRequest",
    "RunSummary",
    "MessageData",
    
    # Configuration
    "browser_settings",
    "scraping_settings", 
    "output_settings",
    "job_filter_settings",
    "llm_settings",
    
    # Services
    "LLMProviderFactory",
    "LLMService",
    "NotifierService",
    "MessageFormatterService",
    
    # Utilities
    "get_logger",
]
