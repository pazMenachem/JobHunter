GENERAL_EXCEPTION_MESSAGE = "Unknown General Exception"
JOB_CRAWLER_EXCEPTION_MESSAGE = "Error during Job Crawler phase"
LLM_EXCEPTION_MESSAGE = "Error during LLM phase"
NOTIFIER_EXCEPTION_MESSAGE = "Error during Notifier phase"
NO_NEW_JOBS_EXCEPTION_MESSAGE = "No new jobs found"

class JobHunterException(Exception):
    """Base exception for JobHunter."""
    def __init__(self, message: str = GENERAL_EXCEPTION_MESSAGE) -> None:
        super().__init__(message)

class JobCrawlerException(JobHunterException):
    """Exception for job crawling."""
    def __init__(self) -> None:
        super().__init__(JOB_CRAWLER_EXCEPTION_MESSAGE)

class LLMException(JobHunterException):
    """Exception for LLM."""
    def __init__(self) -> None:
        super().__init__(LLM_EXCEPTION_MESSAGE)

class NotifierException(JobHunterException):
    """Exception for notifier."""
    def __init__(self) -> None:
        super().__init__(NOTIFIER_EXCEPTION_MESSAGE)

class NoNewJobsException(JobHunterException):
    """Exception for no new jobs."""
    def __init__(self) -> None:
        super().__init__(NO_NEW_JOBS_EXCEPTION_MESSAGE)