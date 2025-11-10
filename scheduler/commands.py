"""Command handlers for scheduler operations."""

import sys

from .metadata_manager import MetadataManager
from .tasks_manager import TasksManager

MENU = """
JobHunter - Automated Job Search Application

Usage:
  python main.py <command> [options]

Commands:
  run             Run the JobHunter application
  create          Create scheduled task(s) from scheduler_config.json
  delete          Delete existing scheduled task(s)
  list            List existing scheduled task(s)
  help            Show this help message (default)

Configuration:
  Edit scheduler_config.json to set:
  - times: List of times in HH:MM format (e.g., ["09:00", "18:00"])
  - mode: "native" or "docker"

Examples:
  python main.py                  # Show this help message
  python main.py help             # Show this help message
  python main.py run              # Run the application
  python main.py create           # Create scheduled tasks
  python main.py delete           # Delete scheduled tasks
  python main.py list             # List scheduled tasks

For Linux users:
  Use native scheduler (cron/systemd) - see docs/LINUX_SCHEDULER.md
"""

class Commands:
    """Handles command execution."""
    
    def __init__(self) -> None:
        """Initialize commands handler."""
        self.metadata = MetadataManager()
        self.tasks_manager = TasksManager(self.metadata)
    
    def handle_run(self) -> None:
        """Handle run command - execute JobHunter application."""
        from src.app_manager import JobHunterOrchestrator
        
        JobHunterOrchestrator().run()
    
    def handle_help(self) -> None:
        """Handle help command."""
        self.show_help()
    
    def show_help(self) -> None:
        """Display help menu."""
        help_text = MENU
        print(help_text)
    
    def handle_create(self) -> None:
        """Handle create command."""
        try:
            self.metadata.validate_project_root()
            
            config = self.metadata.load_config()
            times = config["times"]
            mode = config["mode"]
            
            if not times:
                raise ValueError("No times specified in config file")
            
            if mode not in ["native", "docker"]:
                raise ValueError(
                    f"Invalid mode: {mode}. Must be 'native' or 'docker'"
                )
            
            self.tasks_manager.create_tasks(times, mode)
            
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def handle_delete(self) -> None:
        """Handle delete command."""
        self.tasks_manager.delete_tasks()
    
    def handle_list(self) -> None:
        """Handle list command."""
        self.tasks_manager.list_tasks()

