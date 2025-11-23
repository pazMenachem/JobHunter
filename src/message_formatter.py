"""Prompt formatter for creating LLM prompts from job data."""

from typing import List
from src.data_models import JobData, RunSummary, SegmentedMessage
from src.config import llm_settings

PADDING_LENGTH = 200

class MessageFormatterService:
    """Message formatter service for creating messages from job data."""

    @staticmethod
    def validate_base_prompt(prompt: str) -> str:
        """Validate base prompt length against character limit.
        
        Args:
            prompt: Base LLM prompt to validate
            
        Returns:
            warning_message: Warning message if prompt is too long
        """
        limit = llm_settings.base_prompt_char_limit
        if len(prompt) > limit:
            warning = f"Base prompt is {len(prompt)} characters (recommended: {limit})"
            return warning
        return ""

    @staticmethod
    def format_llm_prompt(
        jobs: List[JobData], 
        base_prompt: str = llm_settings.base_llm_prompt
        ) -> str:
        """Format jobs into a LLM prompt for analysis.
        
        Args:
            jobs: List of JobData objects to analyze
            base_prompt: Base prompt template (default is BASE_LLM_PROMPT from config)

        Returns:
            Formatted message string for LLM analysis
        """
        # Format jobs for the message
        jobs_text = "\n".join([
            f"\nid: {i}:\n"
            f"  Title: {job.title}\n"
            f"  Company: {job.company}\n"
            f"  URL: {job.url}\n"
            for i, job in enumerate(jobs)
        ])

        message_result = f"""{base_prompt}\nJobs to analyze:\n\n{jobs_text}"""

        return message_result

    @staticmethod
    def format_summary(
        run_summary: RunSummary,
        message_max_length: int,
    ) -> SegmentedMessage:
        """Format a readable summary of the filtered jobs for notifications.
        
        Args:
            run_summary: RunSummary object containing the filtered jobs
            message_max_length: Maximum message length per segment

        Returns:
            SegmentedMessage with header and message_parts for user notifications
        """
        header = MessageFormatterService._create_header(run_summary)
        message_parts = MessageFormatterService._create_body(
            run_summary, message_max_length
        )

        return SegmentedMessage(
            header=header,
            message_parts=message_parts
        )

    @staticmethod
    def _create_header(run_summary: RunSummary) -> str:
        """Create header message for job summary.
        
        Args:
            run_summary: RunSummary object containing the filtered jobs
            
        Returns:
            Header string for the summary message
        """
        header = (
            f"JobHunter Results Summary\n"
            f"Total jobs found: {run_summary.total_found}\n"
            f"Relevant jobs: {run_summary.filtered_count}\n"
            f"Filtered out: {run_summary.total_found - run_summary.filtered_count}\n"
            f"{run_summary.notes}\n"
            f"Job Matches:\n"
        )
        return header

    @staticmethod
    def _create_body(
        run_summary: RunSummary,
        message_max_length: int,
    ) -> List[str]:
        """Create message body parts from job list.
        
        Args:
            run_summary: RunSummary object containing the filtered jobs
            message_max_length: Maximum message length per segment
            
        Returns:
            List of message body parts
        """
        message_parts = []
        current_part = ""

        for i, job in enumerate(run_summary.relevant_jobs, 1):
            job_text = (
                f"\n{i}. {job.title} at {job.company}\n"
                f"relevant: {job.relevant.name}\n"
                f"reason: {job.reason}\n"
                f"url: {job.url}\n"
            )
            
            # Check if adding this job would exceed effective limit
            if len(current_part) + len(job_text) + PADDING_LENGTH > message_max_length:
                message_parts.append(current_part.rstrip())
                current_part = job_text
            else:
                current_part += job_text
        
        if current_part:
            message_parts.append(current_part.rstrip())
        
        message_parts[-1] += f"\n\nGenerated: {run_summary.filter_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message_parts
