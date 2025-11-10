"""Page navigation for handling URLs and pagination using Playwright."""

import logging
import re
from typing import Optional
from playwright.sync_api import Page, Locator
from src.config import scraping_settings

# Constants for button detection
QUICK_SELECTORS = [
    "a[aria-label='Next']",
    "a[aria-label='next']",
    ".next-page",
    ".pagination .next",
    "[data-testid='pagination-next']",
    "button[aria-label='Next']",
    ".pagination a:last-child"
]

TEXT_SELECTORS = [
    "button:has-text('next')",
    "a:has-text('next')",
    "button:has-text('›')",
    "a:has-text('›')",
    "[aria-label*='next' i]",
    "[aria-label*='Next' i]"
]


class PageNavigator:
    """Page navigation for job scraping using Playwright.
    
    Handles URL navigation and pagination with flexible button detection.
    """
    
    def __init__(self, page: Page) -> None:
        """Initialize the page navigator.
        
        Args:
            page: Playwright Page instance for browser automation.
        """
        self.page = page
        self.logger = logging.getLogger(__name__)
        self.current_page = 1
    
    def go_to_next_page(self) -> bool:
        """Navigate to the next page with smart button detection.
        
        Returns:
            True if successfully moved to next page, False if no next page available.
        """
        self.logger.info(f"Attempting to navigate to next page..")
        
        try:
            if not self._check_page_limit():
                return False
            
            next_button = self._find_next_page_element()
            if next_button is None:
                self.logger.info("No next page found")
                return False
            
            current_url = self.page.url
            
            # Playwright auto-waits for element to be clickable
            next_button.click()
            
            # Wait for navigation (if URL changes)
            try:
                self.page.wait_for_url(lambda url: url != current_url, timeout=5000)
            except:
                # URL might not change (AJAX pagination)
                self.page.wait_for_timeout(2000)

            self.current_page += 1
            return True

        except Exception as e:
            self.logger.warning(f"Error navigating to next page: {str(e)[:100]}")
            return False
    
    def _check_page_limit(self) -> bool:
        """Check if we've reached the maximum pages limit."""
        if self.current_page >= scraping_settings.max_pages_per_url:
            self.logger.info(f"Reached maximum pages limit ({scraping_settings.max_pages_per_url})")
            return False
        return True
    
    def _find_next_page_element(self) -> Optional[Locator]:
        """Find next page button with flexible text matching."""
        
        # Try different detection methods
        methods = [
            # Role-based (most reliable)
            lambda: self.page.get_by_role("button", name=re.compile("next|›|→", re.IGNORECASE)).first,
            lambda: self.page.get_by_role("link", name=re.compile("next|›|→", re.IGNORECASE)).first,
            # Text selectors
            *[lambda s=sel: self.page.locator(s).first for sel in TEXT_SELECTORS],
            # CSS selectors
            *[lambda s=sel: self.page.locator(s).first for sel in QUICK_SELECTORS]
        ]
        
        for method in methods:
            try:
                element = method()
                if element.count() > 0 and element.is_visible():
                    return element
            except:
                continue
        
        self.logger.warning("No next page element found")
        return None