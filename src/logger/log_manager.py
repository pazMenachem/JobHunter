"""Logger setup for centralized logging."""

import logging
import os
import sys
from datetime import datetime


def _setup_logging() -> None:
    """Set up logging configuration."""
    
    main_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(main_dir))
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"job_hunter_{timestamp}.log")
    
    # Create handlers with UTF-8 encoding
    handlers = []
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1))
    handlers.append(console_handler)
    
    # Only add file handler if the log file can be created
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        handlers.append(file_handler)
    except (OSError, IOError) as e:
        print(f"Could not create log file {log_file}: {e}")
    
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        handlers=handlers
    )
    
    # Disable verbose logging from external libraries
    logging.getLogger('WDM').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    print(f"Logging to file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific component.
    
    Args:
        name: Name of the component (e.g., 'job_crawler', 'app_manager')
        
    Returns:
        Logger instance for the component
    """
    return logging.getLogger(name)


# Set up logging when module is imported
_setup_logging()