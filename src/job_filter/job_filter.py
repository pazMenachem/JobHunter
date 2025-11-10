"""Job filtering logic based on relevance configuration."""

from typing import List
from src.data_models import JobData, RunSummary, RelevanceStatus
from src.logger import get_logger
from src.config import job_filter_settings, llm_settings


class JobFilter:
    """Handles job filtering based on relevance configuration.
    
    This class applies filtering logic to jobs based on their relevance status
    and the configured filter level (RelevanceStatus enum).
    """
    
    def __init__(self) -> None:
        """Initialize the job filter."""
        self.logger = get_logger("job_filter")
        self.logger.info("Job filter initialized...")
    
    def filter_jobs_by_relevance(
        self,
        jobs: List[JobData],
        filter_level: RelevanceStatus = job_filter_settings.default_job_filter_level,
        run_summary: RunSummary = None
        ) -> None:
        """Filter jobs based on relevance status and filter level.
        
        Args:
            jobs: List of JobData objects to filter
            filter_level: Filter level (RelevanceStatus enum) - default is ALL
            run_summary: RunSummary object to store the results
        """
        if not jobs or not run_summary:
            raise RuntimeError("No jobs provided for FILTERING")
        
        relevant_jobs = [job for job in jobs if self._should_include_job(job.relevant, filter_level)]

        run_summary.jobs = relevant_jobs
        run_summary.filtered_count = len(relevant_jobs)
    
    def _should_include_job(
        self, 
        job_relevant: RelevanceStatus,
        filter_level: RelevanceStatus
        ) -> bool:
        """Determine if a job should be included based on filter level.

        Args:
            job_relevant: Job relevance status (RelevanceStatus enum)
            filter_level: Filter level (RelevanceStatus enum)
        Returns:
            True if job should be included, False otherwise
        """
        return job_relevant.value <= filter_level.value
