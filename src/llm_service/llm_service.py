"""Job filter manager using abstract LLM interface."""

import json
import time
from typing import List
from src.data_models import JobData, RelevanceStatus
from src.logger import get_logger
from src.llm_service.llm_base import LLMInterface
from src.exceptions.exceptions import LLMException
from src.config import llm_settings
from src.message_formatter import MessageFormatterService


class LLMService:
    """LLM Service - handles job data list and updates status.
    
    This class manages the job data list and communicates with LLM providers
    to update job status. 
    """
    
    def __init__(self, llm_provider: LLMInterface) -> None:
        """Initialize the LLM service.
        
        Args:
            llm_provider: LLM provider implementing LLMInterface
            jobs: List of JobData objects to analyze and update
        """
        self.llm_provider = llm_provider
        self.logger = get_logger("llm_service")
        
        self.logger.info("LLM service initialized...")
        
    def sends_jobs_to_llm(self, *, jobs: List[JobData]) -> None:
        """Update job status using batched LLM analysis.
        
        Args:
            jobs: List of JobData objects to analyze
        """
        self.logger.info(f"Analyzing {len(jobs)} jobs")
        batch_size = llm_settings.batch_size
        total_batches = (len(jobs) // batch_size) + 1

        try:
            # Process jobs in batches
            for jobs_analyzed in range(0, len(jobs), batch_size):
                batch = jobs[jobs_analyzed:jobs_analyzed + batch_size]
                batch_num = (jobs_analyzed // batch_size) + 1
                
                self.logger.info(f"Processing batch {batch_num} out of {total_batches} batches...")
                
                prompt = MessageFormatterService.format_llm_prompt(batch)
                response = self.llm_provider.send_to_llm(prompt)
                
                if not response:
                    self.logger.error(f"Empty response from LLM, skipping batch {batch_num}")
                    continue

                json_data = self._clean_json_response(response)
                self._parse_batch_response(json_data, batch)
                
                # Rate limiting delay between batches
                if jobs_analyzed + batch_size < len(jobs):
                    time.sleep(6)
            
            self.logger.info("LLM analysis complete")
            
        except Exception as e:
            self.logger.error(f"Error during LLM analysis: {e}")
            raise LLMException()

    def _parse_batch_response(self, json_response: list[dict], jobs: List[JobData]) -> None:
        """Parse the LLM response and update existing job list.
        
        Args:
            json_response: Raw JSON response from the LLM
        """
        try:

            for job_data in json_response:
                id = int(job_data.get("id"))
                reason = job_data.get("reason")
                relevant = RelevanceStatus.from_string(job_data.get("relevant"))
                
                jobs[id].relevant = relevant
                jobs[id].reason = reason

        except (json.JSONDecodeError) as e:
            self.logger.error(f"Failed to parse LLM response, try to check the prompt and the response format")
            raise e
        except (KeyError) as e:
            self.logger.error(f"KeyError: {e}, try to check the prompt and the response format")
            raise e
        except Exception as e:
            self.logger.error(f"General error: {e}")
            raise e

    def _clean_json_response(self, response: str) -> list:
        """Clean LLM response by removing markdown code blocks and extra text.
        
        Extracts JSON array from response, handling cases where LLM adds
        verbose analysis text before or after the JSON.
        
        Args:
            response: Raw LLM response that may contain markdown formatting
                     or verbose text before/after JSON
            
        Returns:
            Cleaned JSON list (array of dictionaries)
        """
        self.logger.info("Cleaning response and converting to JSON object...")

        # First, try to extract from markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.rfind("```")
            if end > start:
                response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.rfind("```")
            if end > start:
                response = response[start:end].strip()
        
        # Try to find JSON array in the response
        # Look for the first '[' that starts a JSON array
        json_start = response.find('[')
        if json_start == -1:
            self.logger.error("No JSON array found in response")
            raise ValueError("No JSON array found in LLM response")
        
        # Find the matching closing ']' by counting brackets
        bracket_count = 0
        json_end = -1
        for i in range(json_start, len(response)):
            if response[i] == '[':
                bracket_count += 1
            elif response[i] == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            self.logger.error("Could not find matching closing bracket for JSON array")
            raise ValueError("Invalid JSON array structure in LLM response")
        
        # Extract just the JSON array
        json_str = response[json_start:json_end].strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse extracted JSON: {e}")
            self.logger.error(f"Extracted JSON string: {json_str[:500]}...")  # Log first 500 chars
            raise