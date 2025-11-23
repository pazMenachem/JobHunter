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
    "software",
    "fullstack",
    "full stack",
    "backend",
    "devops",
    "developer",
]

EXCLUDED_KEYWORDS = [
    "senior",
    "marketing",
    "sales",
    "hr",
    "finance",
    "operations",
    "lead",
    "manager",
    "director",
    "head",
    "chip",
    "electrical",
    "sr.",
]

# URLs to scrape (add your target job sites here)
TARGET_URLS = [
    "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52bbe14cf9326c&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78&workerSubType=0c40f6bd1d8f10adf6dae161b1844a15&workerSubType=ab40a98049581037a3ada55b087049b7&timeType=5509c0b5959810ac0029943377d47364",
    "https://copyleaks.com/careers",
    "https://redhat.wd5.myworkdayjobs.com/jobs/?a=084562884af243748dad7c84c304d89a&e=3afab13eadf301a2eaafadcc15425800",
    "https://careers.checkpoint.com/index.php?q=&module=cpcareers&a=search&fa%5B%5D=department_s%3AR%26D&fa%5B%5D=country_ss%3AIsrael&sort=date_published_display_s+desc",
    "https://monday.com/careers?department=rnd&location=telaviv",
    "https://www.playtika.com/careers/research-development",
    "https://autodesk.wd1.myworkdayjobs.com/en-US/Ext?locationCountry=084562884af243748dad7c84c304d89a&timeType=6d5ece62cf5a4f9f9e349b55f045b5e2&jobFamilyGroup=1f75c4299c9201c0f3b5f8e6fa01c5bf",
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
   - "entry-level", "junior", "graduate", "trainee" = YES
   - "0-2 years", "experienced" = MAYBE

4. INDUSTRY & DOMAIN:
   - Technology companies, startups, software firms
   - IT departments, engineering teams
   - Data science, AI/ML companies
   - Non-tech companies with technical roles

5. LOCATION:
   - Israel

RELEVANCE RULES:
- YES: Programmer/developer role with 0 - 1 years experience(junior/entry-level OR 0-1 years experience)
- MAYBE: Programmer/developer role with 1 - 2 years experience
- NO: Non-programmer roles or 2+ years experience(sales, marketing, HR, finance, etc.)

CRITICAL OUTPUT FORMAT REQUIREMENTS:
⚠️ MANDATORY: The output format below is ABSOLUTE and UNCHANGEABLE. Under NO circumstances can you modify this structure.

⚠️ FORMAT RULES:
- You MUST return a JSON array with EXACTLY the structure shown below
- Every job MUST have exactly three fields: "id", "relevant", and "reason"
- The "id" field MUST be a string matching the job's index (starting from "0")
- The "relevant" field MUST be exactly one of: "yes", "maybe", or "no" (lowercase)
- The "reason" field MUST be a string explaining your decision
- DO NOT add extra fields, comments, or modify the structure in any way
- DO NOT wrap the response in markdown code blocks or add explanatory text
- DO NOT skip jobs or change the order

⚠️ EDGE CASE HANDLING:
- If a job URL is unreachable or inaccessible, write this in the "reason" field (e.g., "URL unreachable - [reason]")
- If job description is missing or incomplete, analyze based on available information (title, company) and note this in the "reason" field
- If you cannot determine relevance, use your best judgment and explain in the "reason" field
- NEVER change the format structure, even for edge cases - always use the reason field to explain issues

OUTPUT FORMAT (MANDATORY - DO NOT MODIFY):
[
  {"id": "0", "relevant": "yes", "reason": "Junior software engineer position"},
  {"id": "1", "relevant": "maybe", "reason": "Senior role but CS field"},
  {"id": "2", "relevant": "no", "reason": "Marketing position, not technical"}
]

REMEMBER: The format is non-negotiable. Return ONLY the JSON array, nothing else.
"""

job_filter_default_level = RelevanceStatus.MAYBE

## END OF USER SETTINGS FOR JOB SCRAPING


class BrowserSettings:
    """Browser settings for the job scraper application."""

    def __init__(
        self, 
        browser_type: str = "firefox",
        headless_mode: bool = False, 
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

class MailSettings:
    """Mail notification settings for the job scraper application."""
    
    def __init__(
        self,
        sender_email: str = None,
        sender_password: str = None,
        recipient_email: str = None,
        smtp_server: str = None,
        smtp_port: int = 587,
        max_message_length: int = 1000000
    ) -> None:
        """Initialize the mail settings.
        
        Args:
            sender_email: Email address for sending
            sender_password: Email password or app password for authentication
            recipient_email: Email address to receive notifications
            smtp_server: SMTP server address (e.g., smtp.gmail.com)
            smtp_port: SMTP server port (default: 587 for TLS)
            max_message_length: Maximum message length (default: 1000000)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.max_message_length = max_message_length
        self.enabled = bool(
            self.sender_email and
            self.sender_password and
            self.recipient_email and
            self.smtp_server
        )

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

mail_settings = MailSettings(
    sender_email=os.getenv("MAIL_SENDER_EMAIL", None),
    sender_password=os.getenv("MAIL_APP_PASSWORD", None),
    recipient_email=os.getenv("MAIL_RECIPIENT_EMAIL", None),
    smtp_server=os.getenv("MAIL_SMTP_SERVER", None),
    smtp_port=int(os.getenv("MAIL_SMTP_PORT", "587"))
)

job_storage_settings = JobStorageSettings()
