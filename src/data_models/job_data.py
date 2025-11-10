"""JobData data class for representing job information."""

from dataclasses import dataclass
from datetime import datetime
from .relevance_status import RelevanceStatus
from src.logger import get_logger

@dataclass
class JobData:
    """Data class representing a job listing.
    
    Attributes:
        id: Unique identifier for the job
        title: Job title
        company: Company name
        url: Job URL
        found_date: Date when job was found (auto-generated if None)
        source_url: URL of the page where job was found
        relevant: LLM analysis result (RelevanceStatus enum)
        reason: LLM explanation for the relevance decision
    """
    id: str = ""
    title: str = ""
    company: str = "Unknown"
    url: str = None
    found_date: datetime = datetime.now()
    source_url: str = ""
    relevant: RelevanceStatus = RelevanceStatus.UNKNOWN
    reason: str = "Unknown"
    
    def __post_init__(self):
        """Set found_date to current time if not provided."""
        if self.found_date is None:
            self.found_date = datetime.now()

    def __str__(self):
        return f"""
        Job #{self.id}:
        \nTitle: {self.title}
        \nCompany: {self.company}
        \nURL: {self.url}
        \nSource URL: {self.source_url}
        \nRelevant: {self.relevant.name}
        \nReason: {self.reason}
        """

def log_job_data(jobs: list[JobData]):
    for job in jobs:
        get_logger("job_data").info(job)