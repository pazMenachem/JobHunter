"""Metadata manager for scheduler configuration and validation."""

import json
import os
from typing import Dict


CONFIG_FILE = "scheduler_config.json"


class MetadataManager:
    """Manages project metadata, validation, and configuration loading."""
    
    def __init__(self) -> None:
        """Initialize metadata manager."""
        self._project_root = None
        self._scheduler_dir = None
    
    def get_project_root(self) -> str:
        """Get the project root directory.
        
        Returns:
            String path to the project root
        """
        if self._project_root is None:
            scheduler_dir = self.get_scheduler_dir()
            self._project_root = os.path.dirname(scheduler_dir)
        return self._project_root
    
    def get_scheduler_dir(self) -> str:
        """Get the scheduler directory.
        
        Returns:
            String path to the scheduler directory
        """
        if self._scheduler_dir is None:
            self._scheduler_dir = os.path.dirname(os.path.abspath(__file__))
        return self._scheduler_dir
    
    def validate_project_root(self) -> None:
        """Validate that project root exists and contains required files.
        
        Raises:
            FileNotFoundError: If project root or required files don't exist
        """
        project_root = self.get_project_root()
        
        if not os.path.exists(project_root):
            raise FileNotFoundError(f"Project root not found: {project_root}")
        
        main_py = os.path.join(project_root, "main.py")
        if not os.path.exists(main_py):
            raise FileNotFoundError(
                f"main.py not found in project root: {project_root}"
            )
    
    def load_config(self) -> Dict:
        """Load scheduler configuration from JSON file.
        
        Returns:
            Dictionary with 'times' and 'mode' keys
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
            ValueError: If config structure is invalid
        """
        scheduler_dir = self.get_scheduler_dir()
        config_path = os.path.join(scheduler_dir, CONFIG_FILE)
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found: {config_path}\n"
                f"Please create {CONFIG_FILE} with 'times' and 'mode' fields."
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.validate_config(config)
        return config
    
    def validate_config(self, config: Dict) -> None:
        """Validate configuration structure.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If config structure is invalid
        """
        if 'times' not in config or 'mode' not in config:
            raise ValueError(
                f"Invalid config file. Must contain 'times' and 'mode' fields.\n"
                f"Example: {{\"times\": [\"09:00\", \"18:00\"], \"mode\": \"native\"}}"
            )
    
    def validate_time(self, time_str: str) -> bool:
        """Validate time format (HH:MM, 24-hour).
        
        Args:
            time_str: Time string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            hour = int(parts[0])
            minute = int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except (ValueError, AttributeError):
            return False

