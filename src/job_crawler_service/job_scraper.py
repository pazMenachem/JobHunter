"""Job scraper for finding keywords in job listings using Playwright."""

from typing import List
from playwright.sync_api import Page, Locator
from src.config import scraping_settings
from src.logger import get_logger
from src.data_models.job_data import JobData

# Constants for scrollable containers
SCROLLABLE_CONTAINERS = [
    ".jobs-search-results-list",  # LinkedIn
    "[role='main']",             # Generic main content
    ".job-list",                 # Common class
    ".results-list"              # Common class
]

MAX_SCROLL_ATTEMPTS = 10

# Job title selectors - focus on URL patterns (href-based matching)
JOB_TITLE_SELECTORS = [
    # Primary: Links with job-related keywords in URL
    "a[href*='position']",  # Links containing 'position' in href
    "a[href*='career']",  # Links containing 'career' in href
    "a[href*='job']",  # Links containing 'job' in href
    "a[href*='opening']",  # Links containing 'opening' in href
    "a[href*='vacancy']",  # Links containing 'vacancy' in href
    "a[href*='opportunity']",  # Links containing 'opportunity' in href
    "a[href*='role']",  # Links containing 'role' in href
]


class JobScraper:
    """Scrapes job listings for specific keywords using Playwright."""
    
    def __init__(self, page: Page) -> None:
        """Initialize the job scraper.
        
        Args:
            page: Playwright Page instance.
        """
        self.page = page
        self.logger = get_logger("job_scraper")
        self.jobs_counter = 1
    
    def scrape_jobs(self) -> List[JobData]:
        """
        Find job listings that contain any of the specified keywords.
        
        Returns:
            List of JobData objects for jobs that match the keywords.
        """
        self.logger.info(f"Searching for jobs..")
        result: List[JobData] = []

        try:
            # Wait for page to be ready
            self.page.wait_for_load_state("networkidle")
            
            # Smart scroll - detects and scrolls correct container
            self._scroll_page()
            
            # Find and filter elements
            job_elements = self._find_job_elements()
            filtered_job_elements = self._filter_job_elements(job_elements)
            
            for element in filtered_job_elements:
                result.append(self._extract_job_data(element, self.jobs_counter))
                self.jobs_counter += 1

        except Exception as e:
            self.logger.error(f"Error finding jobs: {e}")
        
        return result

    def _scroll_page(self) -> None:
        """Smart scroll - handles both full page and container scrolling."""
        # Try to find common scrollable containers first
        scrolled = False
        for selector in SCROLLABLE_CONTAINERS:
            container = self.page.locator(selector).first
            if container.count() > 0:
                self._scroll_container(container)
                scrolled = True
                break
        
        # Fallback: scroll entire page
        if not scrolled:
            self._scroll_full_page()

    def _scroll_container(self, container: Locator) -> None:
        """Scroll a specific container element."""
        last_height = 0
        attempts = 0
        
        while attempts < MAX_SCROLL_ATTEMPTS:
            current_height = container.evaluate("el => el.scrollHeight")
            if current_height == last_height:
                break
            
            container.evaluate("el => el.scrollTo(0, el.scrollHeight)")
            self.page.wait_for_timeout(scraping_settings.scroll_pause_time * 1000)
            last_height = current_height
            attempts += 1

    def _scroll_full_page(self) -> None:
        """Scroll the entire page."""
        last_height = 0
        attempts = 0
        
        while attempts < MAX_SCROLL_ATTEMPTS:
            current_height = self.page.evaluate("document.body.scrollHeight")
            if current_height == last_height:
                break
            
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(scraping_settings.scroll_pause_time * 1000)
            last_height = current_height
            attempts += 1

    def _find_job_elements(self) -> List[Locator]:
        """Find job elements using Playwright locators."""
        self.logger.info(f"Searching job elements on {self.page.url}")
        
        job_elements = []

        for selector in JOB_TITLE_SELECTORS:
            try:
                elements = self.page.locator(selector).all()
                if elements:
                    self.logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    job_elements.extend(elements)
                else:
                    self.logger.debug(f"No elements found with selector: {selector}")
            except Exception as e:
                self.logger.debug(f"Error with selector {selector}: {e}")
                continue
        
        self.logger.info(f"Total elements found before deduplication: {len(job_elements)}")
        
        # Remove duplicates by href
        seen_urls = set()
        unique_elements = []
        for element in job_elements:
            try:
                href = element.evaluate("el => el.href")
                if href and href not in seen_urls:
                    seen_urls.add(href)
                    unique_elements.append(element)
                    self.logger.info(f"Added element: {element.inner_text()}")
                elif href:
                    self.logger.debug(f"Duplicate URL found: {href}")
            except Exception as e:
                self.logger.debug(f"Error getting href from element: {e}")
                continue
        
        self.logger.info(f"Found {len(unique_elements)} unique job elements")
        return unique_elements

    def _filter_job_elements(self, job_elements: List[Locator]) -> List[Locator]:
        """
        Filter job elements to only include those that match the keywords.
        
        Args:
            job_elements: List of Locators to filter.
            
        Returns:
            List of Locators that match the keywords.
        """
        self.logger.info(f"Filtering job elements..")
        filtered = []
        for element in job_elements:
            try:
                text = element.inner_text()
                if self._matches_keywords(text, scraping_settings.keywords) and not self._matches_keywords(text, scraping_settings.excluded_keywords):
                    filtered.append(element)
            except Exception:
                continue
        self.logger.info(f"{len(filtered)} / {len(job_elements)} jobs titles are relevant")
        return filtered

    def _extract_job_data(self, element: Locator, index: int) -> JobData:
        """
        Extract job data from Playwright element.
        
        Args:
            element: Locator to extract job data from.
            index: Job index for unique ID.
            
        Returns:
            JobData object.
        """
        return JobData(
            id=f"{index}",
            title=element.inner_text(),
            url=element.evaluate("el => el.href"),
            company=self._extract_company_name(self.page.url),
            source_url=self.page.url
        )
    
    def _extract_company_name(self, url: str) -> str:
        """
        Extract company name from URL.
        
        Args:
            url: URL to extract company name from.
            
        Returns:
            Company name extracted from URL.
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Extract company name (first part before first dot)
            company = domain.split('.')[0]
            
            return company.title()
            
        except Exception:
            return "Unknown"
    
    def _matches_keywords(self, job_title: str, keywords: List[str]) -> bool:
        """
        Check if job title matches any keywords.
        
        Args:
            job_title: Job title to check.
            keywords: List of keywords to check against.
            
        Returns:
            True if job title matches any keywords, False otherwise.
        """
        title_lower = job_title.lower()
        keywords_lower = [keyword.lower() for keyword in keywords]

        return any(keyword in title_lower for keyword in keywords_lower)