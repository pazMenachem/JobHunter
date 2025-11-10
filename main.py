"""Main application entry point for JobHunter."""

import argparse
import sys

MENU = """
JobHunter - Automated Job Search Application

Usage:
  jh <command> [options]
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
  
Docker:
  Build: docker build -t jobhunter .
  Run: docker-compose up

Examples:
  jh                              # Show this help message
  jh help                         # Show this help message
  jh run                          # Run the application
  jh create                       # Create scheduled tasks
  jh delete                       # Delete scheduled tasks
  jh list                         # List scheduled tasks

Installation:
  pip install -e .                # Install as 'jh' command (recommended)
  See INSTALL.md for details

For Linux users:
  Use native scheduler (cron/systemd) - see docs/LINUX_SCHEDULER.md
"""


def handle_run() -> None:
    """Handle run command - execute JobHunter application."""
    from src.app_manager import JobHunterOrchestrator
    
    orchestrator = JobHunterOrchestrator()
    orchestrator.run()


def handle_help() -> None:
    """Handle help command."""
    print(MENU)


def handle_create() -> None:
    """Handle create command."""
    from scheduler.metadata_manager import MetadataManager
    from scheduler.tasks_manager import TasksManager
    
    try:
        metadata = MetadataManager()
        metadata.validate_project_root()
        
        config = metadata.load_config()
        times = config["times"]
        mode = config["mode"]
        
        if not times:
            raise ValueError("No times specified in config file")
        
        if mode not in ["native", "docker"]:
            raise ValueError(
                f"Invalid mode: {mode}. Must be 'native' or 'docker'"
            )
        
        tasks_manager = TasksManager(metadata)
        tasks_manager.create_tasks(times, mode)
        
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_delete() -> None:
    """Handle delete command."""
    from scheduler.metadata_manager import MetadataManager
    from scheduler.tasks_manager import TasksManager
    
    metadata = MetadataManager()
    tasks_manager = TasksManager(metadata)
    tasks_manager.delete_tasks()


def handle_list() -> None:
    """Handle list command."""
    from scheduler.metadata_manager import MetadataManager
    from scheduler.tasks_manager import TasksManager
    
    metadata = MetadataManager()
    tasks_manager = TasksManager(metadata)
    tasks_manager.list_tasks()


def run_cli() -> None:
    """Parse arguments and route to appropriate command handler."""
    parser = argparse.ArgumentParser(
        description="JobHunter - Automated Job Search Application",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["run", "create", "delete", "list", "help"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    command = args.command if args.command else "help"
    
    match command:
        case "run":
            handle_run()
        case "help":
            handle_help()
        case "create":
            handle_create()
        case "delete":
            handle_delete()
        case "list":
            handle_list()
        case _:
            handle_help()


def main() -> None:
    """Main entry point."""
    run_cli()


if __name__ == "__main__":
    main()
