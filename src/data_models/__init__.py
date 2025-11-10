"""Data models package for JobHunter application."""

from .job_data import JobData
from .search_request import SearchRequest
from .run_summary import RunSummary
from .message_data import MessageData
from .relevance_status import RelevanceStatus
from .segmented_message import SegmentedMessage

__all__ = ['JobData', 'SearchRequest', 'RunSummary', 'MessageData', 'RelevanceStatus', 'SegmentedMessage']
