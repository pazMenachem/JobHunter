"""Configuration settings for the job scraper application."""

import os
from dotenv import load_dotenv
from typing import List
from src.data_models import RelevanceStatus

DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_LLM_MODEL = "gemini-2.5-flash"

## USER SETTINGS FOR JOB SCRAPING - MODIFY THIS SECTION AS NEEDED

# Keywords to search for (modify this list as needed)
DEFAULT_KEYWORDS = [
    "engineer",
    "graduate",
    "junior",
    "software engineer",
]

EXCLUDED_KEYWORDS = [
    "senior",
    "marketing",
    "sales",
    "hr",
    "finance",
    "operations",
]

# URLs to scrape (add your target job sites here)
TARGET_URLS = [
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52bbe14cf9326c&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&workerSubType=0c40f6bd1d8f10adf6dae161b1844a15&workerSubType=ab40a98049581037a3ada55b087049b7&timeType=5509c0b5959810ac0029943377d47364",
    "https://copyleaks.com/careers",
]

NOTIFIER_PROVIDER_NAMES = ["telegram"]

DEFAULT_BASE_PROMPT = """
You are a job relevance analyzer for computer science graduates. Analyze each job posting(url, title, company, description) and determine relevance.

ANALYSIS CRITERIA:
Analyze the FULL job description content, not just the title. Look for:

1. TECHNICAL SKILLS & REQUIREMENTS:
   - Programming languages (Python, Java, C++, JavaScript, etc.)
   - Software development tools (Git, Docker, AWS, etc.)
   - Technical frameworks and technologies
   - Computer science concepts (algorithms, data structures, etc.)

2. ROLE RESPONSIBILITIES:
   - Software development, coding, programming
   - System design, architecture, engineering
   - Data analysis, machine learning, AI
   - Technical problem-solving, debugging
   - Code review, testing, quality assurance

3. EXPERIENCE LEVEL INDICATORS:
   - "0-1 years", "entry-level", "junior", "graduate", "trainee" = YES
   - "2+ years", "experienced" = MAYBE
   - "0 years", "no experience required" = YES

4. INDUSTRY & DOMAIN:
   - Technology companies, startups, software firms
   - IT departments, engineering teams
   - Data science, AI/ML companies
   - Non-tech companies with technical roles

RELEVANCE RULES:
- YES: Technical role + (junior/entry-level OR 0-1 years experience)
- MAYBE: Technical role + (2+ years experience)
- NO: Non-technical roles (sales, marketing, HR, finance, operations)

OUTPUT FORMAT:
Return JSON array with this exact structure:
[
  {"id": "1", "relevant": "yes", "reason": "Junior software engineer position"},
  {"id": "2", "relevant": "maybe", "reason": "Senior role but CS field"},
  {"id": "3", "relevant": "no", "reason": "Marketing position, not technical"}
]
"""

job_filter_default_level = RelevanceStatus.MAYBE

## END OF USER SETTINGS FOR JOB SCRAPING


class BrowserSettings:
    """Browser settings for the job scraper application."""

    def __init__(
        self, 
        browser_type: str = "firefox",
        headless_mode: bool = True, 
        page_load_timeout: int = 30
        ) -> None:
        """Initialize the browser settings.
        
        Args:
            browser_type: Type of browser to use ('chrome', 'firefox').
            headless_mode: Whether to run browser in headless mode.
            page_load_timeout: Maximum time to wait for page to load (seconds)
        """
        self.browser_type = browser_type
        self.headless_mode = headless_mode
        self.page_load_timeout = page_load_timeout

class ScrapingSettings:
    """Scraping settings for the job scraper application."""

    def __init__(
        self, 
        scroll_pause_time: int = 2, 
        max_pages_per_url: int = 3,
        urls: List[str] = TARGET_URLS,
        keywords: List[str] = DEFAULT_KEYWORDS,
        excluded_keywords: List[str] = EXCLUDED_KEYWORDS
        ) -> None:
        """
        Initialize the scraping settings.

        Args:
            page_load_timeout: Maximum time to wait for page to load
            scroll_pause_time: Time to pause between scrolls
            max_pages_per_url: Maximum pages to scrape per URL
            urls: URLs to scrape
            keywords: Keywords to search for
        """

        self.scroll_pause_time = scroll_pause_time
        self.max_pages_per_url = max_pages_per_url
        self.urls = urls
        self.keywords = keywords
        self.excluded_keywords = excluded_keywords

class OutputSettings:
    """Output settings for the job scraper application."""

    def __init__(self, output_file: str = "found_jobs.txt", log_level: str = "INFO") -> None:
        """Initialize the output settings.
        
        Args:
            output_file: File to save found job URLs
            log_level: Logging level: DEBUG, INFO, WARNING, ERROR
        """
        self.output_file = output_file
        self.log_level = log_level

class JobFilterSettings:
    """Job filtering settings for the job scraper application."""
    
    def __init__(self, default_job_filter_level: RelevanceStatus) -> None:
        """Initialize the job filtering settings.
        
        Args:
            default_job_filter_level: Default filtering level: "yes", "no", "maybe", "all"
        """
        self.default_job_filter_level = default_job_filter_level

class LLMSettings:
    """LLM settings for the job scraper application."""
    
    def __init__(
        self, 
        base_llm_prompt: str,
        llm_provider: str,
        llm_model: str,
        api_key: str
        ) -> None:
        """Initialize the LLM settings.
        
        Args:
            base_llm_prompt: Base LLM prompt
            llm_provider: LLM provider: "gemini", "openai"
            llm_model: LLM model: "gemini-2.5-flash", "gpt-4o"
            api_key: API key for the LLM provider
        """
        self.api_key = api_key
        self.base_llm_prompt = base_llm_prompt
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        
        # Batching configuration (based on Gemini 2.5 Flash API limitations)
        # Batch size limited by Gemini URL context tool (20 URLs max)
        # Using 15 URLs per batch for safety margin (output token limit)
        self.batch_size = 15  # Jobs per batch
        self.rpm = 10  # Requests per minute (Gemini 2.5 Flash)
        self.max_jobs_per_run = self.batch_size * self.rpm  # 150 jobs
        self.base_prompt_char_limit = 2000  # Warning threshold
        self.unlimited_mode = False  # For future local LLMs
        
        self.enabled = bool(self.api_key)

class TelegramSettings:
    """Telegram notification settings for the job scraper application."""
    
    def __init__(
        self,
        bot_token: str = None,
        chat_id: str = None,
        max_message_length: int = 4096
        ) -> None:
        """Initialize the Telegram settings.
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
            max_message_length: Maximum message length for Telegram (default: 4096)
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.max_message_length = max_message_length
        self.enabled = bool(
            self.bot_token and self.chat_id
            )

class GmailSettings:
    """Gmail notification settings for the job scraper application."""
    
    def __init__(self, max_message_length: int = 1000000) -> None:
        """Initialize the Gmail settings.
        
        Args:
            max_message_length: Maximum message length for Gmail (default: 1000000)
        """
        self.max_message_length = max_message_length
        self.enabled = False

class JobStorageSettings:
    """Job storage settings for the job scraper application."""
    
    def __init__(
        self,
        storage_file_name: str = "sent_jobs.json",
        job_url_expiry_days: int = 30
        ) -> None:
        """Initialize the job storage settings.
        
        Args:
            storage_file_name: Name of the JSON file to store sent job URLs
            job_url_expiry_days: Number of days to keep job URLs before expiry
        """
        self.storage_file_name = storage_file_name
        self.job_url_expiry_days = job_url_expiry_days

load_dotenv()

browser_settings = BrowserSettings()

scraping_settings = ScrapingSettings()

output_settings = OutputSettings()

job_filter_settings = JobFilterSettings(
    default_job_filter_level=job_filter_default_level
)

llm_settings = LLMSettings(
    base_llm_prompt=DEFAULT_BASE_PROMPT,
    llm_provider=DEFAULT_LLM_PROVIDER,
    llm_model=DEFAULT_LLM_MODEL,
    api_key=os.getenv("LLM_API_KEY", None)
    )

telegram_settings = TelegramSettings(
    bot_token=os.getenv("TELEGRAM_API_TOKEN", None),
    chat_id=os.getenv("TELEGRAM_API_CHAT_ID", None)
    )

gmail_settings = GmailSettings()

job_storage_settings = JobStorageSettings()
