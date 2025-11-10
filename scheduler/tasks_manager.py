"""Tasks manager for Windows Task Scheduler operations."""

import os
import subprocess
import sys
from typing import List

from .metadata_manager import MetadataManager


TASK_NAME = "JobHunter"


class TasksManager:
    """Manages Windows Task Scheduler operations."""
    
    def __init__(self, metadata: MetadataManager) -> None:
        """Initialize tasks manager.
        
        Args:
            metadata: MetadataManager instance
        """
        self.metadata = metadata
    
    def build_native_command(self, project_root: str) -> str:
        """Build command for native Python execution.
        
        Args:
            project_root: Path to project root directory
            
        Returns:
            Command string to execute
            
        Raises:
            FileNotFoundError: If venv not found
        """
        if sys.platform == "win32":
            venv_python = os.path.join(
                project_root, "venv", "Scripts", "python.exe"
            )
        else:
            venv_python = os.path.join(
                project_root, "venv", "bin", "python"
            )
        
        main_script = os.path.join(project_root, "main.py")
        
        if not os.path.exists(venv_python):
            raise FileNotFoundError(
                f"Virtual environment not found at {venv_python}\n"
                f"Please create venv first: python -m venv venv"
            )
        
        return f'"{venv_python}" "{main_script}" run'
    
    def build_docker_command(self, project_root: str) -> str:
        """Build command for Docker execution using docker-compose.
        
        Args:
            project_root: Path to project root directory
            
        Returns:
            Command string to execute
        """
        docker_compose_file = os.path.join(project_root, "docker-compose.yml")
        
        if not os.path.exists(docker_compose_file):
            raise FileNotFoundError(
                f"docker-compose.yml not found at {docker_compose_file}\n"
                f"Please ensure docker-compose.yml exists in project root"
            )
        
        # Use docker-compose to run the container
        docker_cmd = f'docker-compose -f "{docker_compose_file}" up --abort-on-container-exit'
        return docker_cmd
    
    def build_command(self, mode: str, project_root: str) -> str:
        """Build the command to execute based on mode.
        
        Args:
            mode: Execution mode ('native' or 'docker')
            project_root: Path to project root directory
            
        Returns:
            Command string to execute
            
        Raises:
            ValueError: If mode is invalid
        """
        match mode:
            case "native":
                return self.build_native_command(project_root)
            case "docker":
                return self.build_docker_command(project_root)
            case _:
                raise ValueError(f"Invalid mode: {mode}. Must be 'native' or 'docker'")
    
    def validate_times(self, times: List[str]) -> None:
        """Validate all times in the list.
        
        Args:
            times: List of time strings to validate
            
        Raises:
            ValueError: If any time is invalid
        """
        for time_str in times:
            if not self.metadata.validate_time(time_str):
                raise ValueError(
                    f"Invalid time format: {time_str}. Use HH:MM (24-hour)"
                )
    
    def create_single_task(
        self, task_name: str, time_str: str, command: str, working_dir: str
        ) -> None:
        """Create a single Windows Task Scheduler task.
        
        Args:
            task_name: Name of the task
            time_str: Time in HH:MM format
            command: Command to execute
            working_dir: Working directory for the task
            
        Raises:
            RuntimeError: If task creation fails
        """
        schtasks_cmd = [
            "schtasks", "/create",
            "/tn", task_name,
            "/tr", command,
            "/sc", "daily",
            "/st", time_str,
            "/f"
        ]
        
        try:
            subprocess.run(
                schtasks_cmd,
                cwd=working_dir,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Created task '{task_name}' scheduled for {time_str}")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else e.stdout
            raise RuntimeError(
                f"Failed to create task '{task_name}': {error_msg}\n"
                f"Command: {' '.join(schtasks_cmd)}"
            )
    
    def create_tasks(self, times: List[str], mode: str) -> None:
        """Create Windows Task Scheduler tasks.
        
        Args:
            times: List of times in HH:MM format
            mode: Execution mode ('native' or 'docker')
        """
        project_root = self.metadata.get_project_root()

        self.validate_times(times)

        command = self.build_command(mode, project_root)
        working_dir = project_root
        
        # Delete existing tasks first
        try:
            self.delete_tasks()
        except subprocess.CalledProcessError:
            pass
        
        # Create tasks for each time
        for i, time_str in enumerate(times):
            self.create_single_task(f"{TASK_NAME}_{i+1}", time_str, command, working_dir)
        
        print(f"\n✓ Successfully created {len(times)} scheduled task(s)")
        print(f"  Mode: {mode}")
        print(f"  Times: {', '.join(times)}")
    
    def delete_single_task(self, task_name: str) -> bool:
        """Delete a single Windows Task Scheduler task.
        
        Args:
            task_name: Name of the task to delete
            
        Returns:
            True if task was deleted, False otherwise
        """
        try:
            subprocess.run(
                ["schtasks", "/delete", "/tn", task_name, "/f"],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Deleted task '{task_name}'")
            return True
        except subprocess.CalledProcessError:
            return False
    
    def find_all_tasks(self) -> List[str]:
        """Find all JobHunter tasks by querying incrementally.
        
        Tasks are created sequentially (JobHunter_1, JobHunter_2, etc.),
        so we check until we find a gap, indicating no more tasks exist.
        
        Returns:
            List of task names that exist
        """
        found_tasks = []
        i = 1
        
        # Check tasks sequentially until we find a gap
        # Since tasks are always created sequentially, first gap = no more tasks
        task_name = f"{TASK_NAME}_{i}"
        while self.query_task(task_name):
            found_tasks.append(task_name)
            i += 1
            task_name = f"{TASK_NAME}_{i}"
        
        return found_tasks
    
    def delete_tasks(self) -> None:
        """Delete Windows Task Scheduler task(s)."""
        found_tasks = self.find_all_tasks()

        if not found_tasks:
            print("No tasks found to delete")
            return
        
        for task_name in found_tasks:
            self.delete_single_task(task_name)
        
        print(f"\n✓ Successfully deleted {len(found_tasks)} task(s)")
    
    def query_task(self, task_name: str) -> bool:
        """Query a Windows Task Scheduler task.
        
        Args:
            task_name: Name of the task to query
            
        Returns:
            True if task exists, False otherwise
        """
        result = subprocess.run(
            ["schtasks", "/query", "/tn", task_name, "/fo", "list", "/v"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def list_tasks(self) -> None:
        """List existing JobHunter tasks."""
        print(f"Checking for '{TASK_NAME}' tasks...\n")
        
        try:
            found_tasks = self.find_all_tasks()
            
            if not found_tasks:
                print("No JobHunter tasks found")
                return
            
            for task_name in found_tasks:
                result = subprocess.run(
                    ["schtasks", "/query", "/tn", task_name, "/fo", "list", "/v"],
                    capture_output=True,
                    text=True
                )
                print(f"Task: {task_name}\n{result.stdout}")

        except Exception as e:
            print(f"Error listing tasks: {e}")
