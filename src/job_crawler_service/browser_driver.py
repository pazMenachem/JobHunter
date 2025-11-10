"""Browser driver for automation using Playwright."""

import logging
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from src.config import browser_settings


class BrowserDriver:
    """Browser driver for automation.
    
    Creates and configures Playwright browser instances for Firefox and Chromium.
    """
    
    def __init__(
        self, 
        browser: str = browser_settings.browser_type, 
        headless: bool = browser_settings.headless_mode
        ) -> None:
        """Initialize the browser driver.
        
        Args:
            browser: Type of browser to use ('firefox', 'chrome'/'chromium').
            headless: Whether to run browser in headless mode.
        """
        self.browser = browser.lower()
        self.headless = headless
        self.playwright = None
        self.browser_instance: Browser | None = None
        self.context: BrowserContext | None = None
        self.logger = logging.getLogger(__name__)
    
    def __enter__(self) -> Page:
        """Context manager entry.
        
        Returns:
            Configured Playwright Page instance.
        """
        self.playwright = sync_playwright().start()
        
        # Launch appropriate browser
        match self.browser:
            case "chrome" | "chromium":
                self.browser_instance = self.playwright.chromium.launch(headless=self.headless)
            case "firefox":
                self.browser_instance = self.playwright.firefox.launch(headless=self.headless)
            case _:
                raise ValueError(f"Unsupported browser: {self.browser}. Use 'firefox' or 'chrome'")
        
        # Create context with settings
        self.context = self.browser_instance.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Create and configure page
        page = self.context.new_page()
        page.set_default_timeout(browser_settings.page_load_timeout * 1000)  # Convert to ms
        
        self.logger.info(f"Playwright {self.browser} browser launched")
        return page
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit.
        
        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        if self.context:
            self.context.close()
        if self.browser_instance:
            self.browser_instance.close()
        if self.playwright:
            self.playwright.stop()
        
        self.logger.info("Playwright browser closed")
