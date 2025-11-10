"""Application orchestrator for coordinating all components."""

from src.logger import get_logger
from src.config import scraping_settings, llm_settings, NOTIFIER_PROVIDER_NAMES
from src.job_crawler_service.job_crawler_service import JobCrawlerService
from src.job_storage.job_storage_service import JobStorageService
from src.llm_service.factory import LLMProviderFactory
from src.llm_service.llm_service import LLMService
from src.job_filter.job_filter import JobFilter
from src.notification_service.notifier_service import NotifierService
from src.data_models import JobData, RunSummary, RelevanceStatus, SegmentedMessage
from src.message_formatter import MessageFormatterService
from src.exceptions.exceptions import JobCrawlerException, LLMException, NotifierException, NoNewJobsException
from typing import List

TEST_DATA = [
    JobData(
        id="1",
        title="Data Engineer",
        company="Copyleaks",
        url="https://copyleaks.com/careers/data-engineer",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.YES,
        reason="Data Engineer"
    ),
    JobData(
        id="2",
        title="QA AUTOMATION ENGINEER",
        company="Copyleaks",
        url="https://copyleaks.com/careers/qa-automation-engineer",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.MAYBE,
        reason="QA Automation Engineer"
    ),
    JobData(
        id="3",
        title="Bookkeeper",
        company="Copyleaks",
        url="https://copyleaks.com/careers/bookkeeper",
        source_url="https://copyleaks.com/careers",
        relevant=RelevanceStatus.NO,
        reason="Bookkeeper"
    ),
]

TEST_DATA_TWO = [ JobData(
        id=f"{i}",
        title=f"Data Engineer {i}",
        company=f"Company {i}",
        url=f"https://company{i}.com/careers/data-engineer",
        source_url=f"https://company{i}.com/careers",
        relevant=RelevanceStatus.YES,
        reason="Unknown"
    ) for i in range(1, 171) ]


class JobHunterOrchestrator:
    """Orchestrates the complete JobHunter application workflow.
    
    This class coordinates all application components and manages
    the overall application flow from start to finish.
    """
    
    def __init__(self) -> None:
        """Initialize the orchestrator."""
        self.logger = get_logger("orchestrator")
        self.job_crawler_service = None
        self.job_storage_service = None
        self.job_filter = None
        self.llm_service = None
        self.notifier_service = None
        self.jobs: List[JobData] = []
        self.run_summary: RunSummary = None

        self._setup()
        self.logger.info("JobHunter orchestrator initialized")

    def _setup(self) -> None:
        """Setup the orchestrator."""
        self.job_crawler_service = JobCrawlerService()
        
        self.job_storage_service = JobStorageService()
        
        self.llm_service = LLMService(
            llm_provider=LLMProviderFactory.create_provider()
            )
        
        self.notifier_service = NotifierService(
            provider_names=NOTIFIER_PROVIDER_NAMES
            )

        self.job_filter = JobFilter()
        self.run_summary = RunSummary()
    
    def run(self) -> None:
        """Run the complete application workflow."""

        try:
            self.logger.info("\n\t\t********* Starting to run *********\n")
            
            # Step 1: Crawl jobs
            # self._crawl_jobs()
            
            self.jobs = TEST_DATA_TWO
            # Step 2: Filter duplicate jobs
            self._filter_duplicate_jobs()

            # Step 3: Update job status using LLM
            # self._update_job_status()
            # Step 4: Filter jobs based on relevance
            self._filter_jobs_by_relevance()
            
            # Step 5: Send summary to user
            self._send_summary(run_summary=self.run_summary)
            
            # Step 6: Mark jobs as sent
            self._mark_jobs_as_sent()
        
            self.logger.info("\n\t\t********* Application finished successfully *********\n")
            
        except NoNewJobsException as e:
            self.logger.info(f"""
                             \n\t\t********* Application finished successfully *********
                             \n\t\t\t********* No new jobs found *********
                             \n""")
            self._send_component_error(error=e)
            
        except (JobCrawlerException, LLMException, NotifierException) as e:
            self._send_component_error(error=e)

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")

        except Exception as e:
            self._send_unknown_error(error=e)
            
        finally:
            self.logger.info("\n\t\t********* Finished running *********\n")
        
    def _crawl_jobs(self) -> None:
        """Crawl jobs."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 1 - crawling jobs ***\n")
        self.jobs = self.job_crawler_service.crawl_jobs()
        
        self._check_jobs_count()

    def _filter_duplicate_jobs(self) -> None:
        """Filter out jobs that have already been sent."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 2 - filtering duplicate jobs ***\n")
        
        initial_count = len(self.jobs)
        self.jobs = self.job_storage_service.get_unsent_jobs(self.jobs)
        
        if not self.jobs:
            raise NoNewJobsException()
        
        self.logger.info(f"Filtered {initial_count - len(self.jobs)} duplicate jobs, {len(self.jobs)} new jobs remaining")
    
    def _update_job_status(self) -> None:
        """Update job status using LLM with batching."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 3 - updating job status using LLM ***\n")
        self.llm_service.update_job_status(jobs=self.jobs)
        
    def _filter_jobs_by_relevance(self) -> None:
        """Filter jobs based on relevance."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 4 - filtering jobs by relevance ***\n")
        self.job_filter.filter_jobs_by_relevance(
            jobs=self.jobs, 
            run_summary=self.run_summary
            )
    
    def _send_summary(self, *, run_summary: RunSummary) -> None:
        """Send summary to user with deferred jobs and notes."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 5 - sending summary to user ***\n")

        if not run_summary.jobs:
            raise NoNewJobsException()
        
        for provider in self.notifier_service.providers:
            summary = MessageFormatterService.format_summary(
                run_summary=run_summary,
                message_max_length=provider.max_message_length,
            )
            self.notifier_service.send_notification(
                provider=provider, 
                message=summary
                )
    
    def _mark_jobs_as_sent(self) -> None:
        """Mark jobs as sent in storage."""
        self.logger.info(f"\n\n\t\t *** Starting Phase 6 - marking jobs as sent ***\n")
        self.job_storage_service.mark_jobs_as_sent(self.run_summary.jobs)
    
    def _send_component_error(self, *, error: Exception) -> None:
        """Send component error to user."""
        self.logger.error(f"Error in {error.__class__.__name__}")
        
        message: SegmentedMessage = SegmentedMessage(
            message_parts=[str(error)]
        )
        self._send_message(message=message)
    
    def _send_unknown_error(self, *, error: Exception) -> None:
        """Send unknown error to user."""
        self.logger.error(f"Application failed: {error}")
        
        message: SegmentedMessage = SegmentedMessage(
            message_parts=["Unknown error occurred, Check the logs."]
        )
        self._send_message(message=message)
    
    def _send_message(self, *, message: SegmentedMessage) -> None:
        """Send message to user."""
        for provider in self.notifier_service.providers:
            self.logger.info(f"{provider.__class__.__name__} sending message...")

            self.notifier_service.send_notification(
                    provider=provider,
                    message=message
                )

    def _check_jobs_count(self) -> None:
        """Check if the number of jobs is greater than the maximum number of jobs per run."""
        self.run_summary.total_found = len(self.jobs)
        self.run_summary.deferred_count = max(0, len(self.jobs) - llm_settings.max_jobs_per_run)

        if len(self.jobs) > llm_settings.max_jobs_per_run:
            self.logger.info(f"Maximum number of jobs per run reached, reducing the number of jobs to {llm_settings.max_jobs_per_run}.")
            self.run_summary.notes += f"Maximum number of jobs per run reached, reducing the number of jobs to {llm_settings.max_jobs_per_run}\nnext run will analyze the remaining jobs."
            self.jobs = self.jobs[:llm_settings.max_jobs_per_run]