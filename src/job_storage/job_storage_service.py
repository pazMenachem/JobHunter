"""Job storage service for tracking sent job URLs with expiry."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from src.data_models import JobData
from src.logger import get_logger
from src.config import job_storage_settings


class JobStorageService:
    """Manages job URL tracking with JSON persistence.
    
    This service tracks sent job URLs with timestamps and automatically
    expires old entries based on configured expiry days.
    """
    
    def __init__(self) -> None:
        """Initialize the job storage service."""
        self.logger = get_logger("job_storage_service")
        self.sent_job_urls: Dict[str, str] = {}
        self.storage_file_path = self._get_storage_file_path()
        
        self.load_from_file()
        self.cleanup_expired_urls()
        
        self.logger.info("Job storage service initialized...")
    
    def _get_storage_file_path(self) -> Path:
        """Get the full path to the storage file.
        
        Returns:
            Path object pointing to the storage file
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        data_dir = Path(project_root) / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        return data_dir / job_storage_settings.storage_file_name
    
    def load_from_file(self) -> None:
        """Load sent job URLs from JSON file.
        
        Handles missing or corrupt files gracefully by creating new storage.
        """
        self.logger.info("Loading sent job URLs from storage file...")
        
        try:
            if not self.storage_file_path.exists():
                self.logger.info("Storage file not found, creating new storage")
                self.sent_job_urls = {}
                return
            
            with open(self.storage_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.sent_job_urls = data.get("sent_job_urls", {})
            
            self.logger.info(f"Loaded {len(self.sent_job_urls)} sent job URLs from storage")
            
        except json.JSONDecodeError as e:
            self.logger.warning(f"Corrupt JSON file detected: {e}. Creating new storage.")
            self.sent_job_urls = {}
        except Exception as e:
            self.logger.warning(f"Error loading storage file: {e}. Creating new storage.")
            self.sent_job_urls = {}
    
    def save_to_file(self) -> None:
        """Save sent job URLs to JSON file.
        
        Raises:
            Exception: If unable to write to storage file
        """
        self.logger.info(f"Saving {len(self.sent_job_urls)} sent job URLs to storage")
        
        try:
            data = {
                "sent_job_urls": self.sent_job_urls,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.storage_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(self.sent_job_urls)} sent job URLs to storage")
            
        except Exception as e:
            self.logger.error(f"Error saving storage file: {e}")
            raise
    
    def is_job_sent(self, url: str) -> bool:
        """Check if a job URL has already been sent.
        
        Args:
            url: Job URL to check
            
        Returns:
            True if URL exists in storage, False otherwise
        """
        return url in self.sent_job_urls
    
    def mark_jobs_as_sent(self, jobs: List[JobData]) -> None:
        """Mark job URLs as sent with current timestamp.
        
        Args:
            jobs: List of JobData objects to mark as sent
        """
        if not jobs:
            self.logger.warning("No jobs to mark as sent")
            return
        
        current_time = datetime.now().isoformat()
        
        for job in jobs:
            if job.url:
                self.sent_job_urls[job.url] = current_time
        
        self.logger.info(f"Marked {len(jobs)} jobs as sent")
        self.save_to_file()
    
    def cleanup_expired_urls(self) -> None:
        """Remove URLs older than the configured expiry days."""
        if not self.sent_job_urls:
            return
        self.logger.info(f"Cleaning up expired URLs from storage")
        
        expiry_date = datetime.now() - timedelta(days=job_storage_settings.job_url_expiry_days)
        initial_count = len(self.sent_job_urls)
        
        # Filter out expired URLs
        self.sent_job_urls = {
            url: timestamp
            for url, timestamp in self.sent_job_urls.items()
            if datetime.fromisoformat(timestamp) > expiry_date
        }
        
        removed_count = initial_count - len(self.sent_job_urls)
        
        if removed_count > 0:
            self.logger.info(f"Removed {removed_count} expired URLs (older than {job_storage_settings.job_url_expiry_days} days)")
            self.save_to_file()
    
    def get_unsent_jobs(self, jobs: List[JobData]) -> List[JobData]:
        """Filter out jobs that have already been sent.
        
        Args:
            jobs: List of JobData objects to filter
            
        Returns:
            List of JobData objects that haven't been sent yet
        """
        if not jobs:
            return []
        
        unsent_jobs = [job for job in jobs if not self.is_job_sent(job.url)]
        
        duplicate_count = len(jobs) - len(unsent_jobs)
        
        if duplicate_count > 0:
            self.logger.info(f"Filtered out {duplicate_count} duplicate jobs")
        
        self.logger.info(f"{len(unsent_jobs)} new jobs found")
        
        return unsent_jobs

