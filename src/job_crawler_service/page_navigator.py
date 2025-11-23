"""Page navigation for handling URLs and pagination using Playwright."""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator
from src.config import scraping_settings

# Next button keywords - focus on explicit "next" indicators
NEXT_KEYWORDS = ['next', 'forward']
ARROW_SYMBOLS = ['›', '→', '>']


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
            
            # Scroll to bottom to ensure pagination buttons are loaded
            self._scroll_to_bottom()
            
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
    
    def _scroll_to_bottom(self) -> None:
        """Scroll to bottom of page to ensure pagination elements are loaded."""
        try:
            # Scroll to bottom
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(1000)  # Wait for any lazy-loaded content
            
            # Try one more scroll in case content loaded
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.page.wait_for_timeout(500)
        except Exception as e:
            self.logger.debug(f"Error scrolling to bottom: {e}")
    
    def _find_next_page_element(self) -> Optional[Locator]:
        """Find next page button by checking for 'next' indicators in any attribute or text."""
        all_elements = self.page.locator("a, button").all()
        
        for element in all_elements:
            try:
                if not element.is_visible():
                    continue
                
                if self._is_next_button(element):
                    return element
                    
            except Exception:
                continue
        
        self.logger.warning("No next page element found")
        return None
    
    def _is_next_button(self, element: Locator) -> bool:
        """Check if element is a 'next' button by examining all attributes and text.
        
        Args:
            element: Locator to check
            
        Returns:
            True if element contains 'next' indicators, False otherwise
        """
        try:
            # Extract all relevant data
            class_attr = (element.get_attribute("class") or "").lower()
            title = (element.get_attribute("title") or "").lower()
            aria_label = (element.get_attribute("aria-label") or "").lower()
            href = (element.get_attribute("href") or "").lower()
            text = element.inner_text().lower()
            
            # Get all data-* attributes
            data_attrs = self._get_data_attributes(element)
            data_values = " ".join(data_attrs.values())
            
            # Combine all searchable content
            all_content = f"{class_attr} {title} {aria_label} {href} {text} {data_values}"
            
            # Check for NEXT_KEYWORDS or ARROW_SYMBOLS
            for keyword in NEXT_KEYWORDS + ARROW_SYMBOLS:
                if keyword in all_content:
                    self.logger.info(f"Found next button with keyword '{keyword}': text='{text[:30]}', href='{href[:50]}'")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.debug(f"Error checking element: {e}")
            return False
    
    def _get_data_attributes(self, element: Locator) -> dict:
        """Extract all data-* attributes from element.
        
        Args:
            element: Locator to extract data attributes from
            
        Returns:
            Dictionary of data-* attribute names and values
        """
        data_attrs = {}
        try:
            attrs = element.evaluate("el => Array.from(el.attributes).map(a => a.name)")
            for attr_name in attrs:
                if attr_name.startswith("data-"):
                    value = element.get_attribute(attr_name) or ""
                    data_attrs[attr_name] = value.lower()
        except Exception:
            pass
        return data_attrs
    