"""FilteredJobs data class for filtered job results."""

from dataclasses import dataclass
from typing import List
from datetime import datetime
from .job_data import JobData


@dataclass
class RunSummary:
    """Data class representing run summary.
    
    Attributes:
        jobs: List of JobData objects
        total_found: Total number of jobs found before filtering
        filtered_count: Number of jobs after filtering
        deferred_count: Number of jobs deferred to next run
        notes: Optional general notes (e.g., warnings, info messages)
    """
    jobs: List[JobData] = None
    total_found: int = 0
    filtered_count: int = 0
    deferred_count: int = 0
    notes: str = ""
    filter_timestamp: datetime = None
    
    def __post_init__(self):
        """Set filter_timestamp to current time if not provided."""
        if self.filter_timestamp is None:
            self.filter_timestamp = datetime.now()
