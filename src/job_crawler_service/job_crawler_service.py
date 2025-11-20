"""Job crawler manager for coordinating job scraping operations using Playwright."""

from typing import List
from .job_scraper import JobScraper
from .browser_driver import BrowserDriver
from .page_navigator import PageNavigator
from src.data_models import JobData
from src.config import scraping_settings
from src.logger import get_logger
from src.exceptions.exceptions import JobCrawlerException


class JobCrawlerService:

    """Manages job crawling operations.

    This class coordinates the job scraping process, including
    browser management, URL navigation, and job data extraction.
    """

    def __init__(self) -> None:
        """Initialize the job crawler manager."""
        self.logger = get_logger("job_crawler")
        self.job_scraper = None
        self.page_navigator = None
        
        self.logger.info("Job crawler manager initialized...")
    
    def crawl_jobs(self) -> List[JobData]:
        """Crawl jobs from specified URLs."""
        self.logger.info(f"Starting job crawl..")

        result: List[JobData] = []

        try:
            with BrowserDriver() as page:
                self.job_scraper = JobScraper(page)
                self.page_navigator = PageNavigator(page)

                for url in scraping_settings.urls:
                    page.goto(url, wait_until="domcontentloaded")
                    result.extend(self._process_url(url))

        except Exception as e:
            self.logger.error(f"Error during job crawling: {e}")
            raise JobCrawlerException()
        
        if not result:
            raise RuntimeError("No jobs found during crawling")

        self.logger.info(f"Found {len(result)} jobs total:")
        for i, job in enumerate(result, 1):
            self.logger.info(f"  {i}. {job.title} at {job.company}")
        return result
    
    def _process_url(self, url: str) -> List[JobData]:

        """
        Process all pages for current URL.
        
        Args:
            url: URL to process.
            
        Returns:
            List of JobData objects found on all pages.
        """        
        result: List[JobData] = []
        ongoing = True
        self.logger.info(f"Processing URL: {url}")
        # Process all pages for this URL
        while ongoing:
            # Find jobs on the current page
            result.extend(self.job_scraper.scrape_jobs())

            # Try to go to next page
            if not self.page_navigator.go_to_next_page():
                ongoing = False

        return result
