"""
Logging Utility Module

This module provides unified logging functionality for all Netsploit modules.
It abstracts log file creation, directory management, and user prompts.

Key Features:
- Centralized control via Config.LOGS_ENABLED and Config.LOGS_MODE
- Three logging modes: PROMPT (ask user), AUTOMATIC (always save), DISABLED (no logs)
- Automatic log file naming and directory creation
- Consistent save/delete prompts across modules
- Works with nmap-based modules (receives -oN path) and custom loggers

Usage:
    from utils.logging import LogManager

    # Create log path for nmap (before running nmap with -oN)
    log_path = LogManager.get_log_file_path("device-info")
    # Pass log_path to nmap as: -oN "{log_path}"

    # After module execution, handle user prompt
    LogManager.handle_log_prompt("Device Info", log_path)

    # For custom logging (non-nmap), write to file then prompt
    log_path = LogManager.get_log_file_path("oui-lookup")
    with open(log_path, "w") as f:
        f.write(results)
    LogManager.handle_log_prompt("OUI Lookup", log_path)
"""

import datetime
import os
from pathlib import Path
from typing import Optional

from utils.colors import cyan, green
from utils.config import Config
from utils.font_styles import error_message, success_message


class LogManager:
    """Centralized logging manager for all Netsploit modules."""

    @staticmethod
    def _is_logging_enabled() -> bool:
        """Check if logging is enabled globally."""
        if not Config.LOGS_ENABLED:
            return False
        if Config.LOGS_MODE == "DISABLED":
            return False
        return True

    @staticmethod
    def _ensure_log_directory_exists(log_path: Path) -> bool:
        """
        Ensure the log file's parent directory exists.

        Args:
            log_path (Path): Full path to the log file

        Returns:
            bool: True if directory exists or was created, False on error
        """
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except OSError as e:
            error_message(f"Error creating log directory: {e}")
            return False

    @staticmethod
    def get_log_file_path(module_name: str) -> Optional[Path]:
        """
        Generate and return the log file path for a module.

        This method:
        1. Checks if logging is enabled
        2. Generates a timestamped filename
        3. Creates the module's log subdirectory if needed
        4. Returns the full path

        Args:
            module_name (str): The module name (e.g., "device-info", "oui-lookup")

        Returns:
            Path: Full path to the log file (may not exist yet)
            None: If logging is disabled

        Example:
            log_path = LogManager.get_log_file_path("port-scanner")
            # Returns: Path("logs/port-scanner/port-scanner_log_HH-MM-SS_PM_DD-Mon-YYYY.txt")
        """
        if not LogManager._is_logging_enabled():
            return None

        # Generate timestamped filename
        timestamp = datetime.datetime.now().strftime("%H-%M-%S-%f_%d-%b-%Y")
        filename = f"{module_name}_log_{timestamp}.txt"

        # Build full path
        log_path = Config.LOGS_FOLDER_PATH / module_name / filename

        # Ensure directory exists
        if not LogManager._ensure_log_directory_exists(log_path):
            return None

        return log_path

    @staticmethod
    def handle_log_prompt(module_fullname: str, log_path: Optional[Path]) -> None:
        """
        Handle the save/delete prompt based on Config.LOGS_MODE.

        Behavior depends on LOGS_MODE:
        - "PROMPT": Ask user to save or delete
        - "AUTOMATIC": Always keep the log (no prompt)
        - "DISABLED": Never create logs (log_path is None)

        Args:
            module_fullname (str): Full name of the module (e.g., "Device Info")
            log_path (Path or None): Path to the log file (from get_log_file_path)

        Example:
            log_path = LogManager.get_log_file_path("port-scanner")
            # ... run nmap with -oN {log_path} ...
            LogManager.handle_log_prompt("Port Scanner", log_path)
        """
        # If logging is disabled or log_path is None, do nothing
        if not log_path or not LogManager._is_logging_enabled():
            return

        # AUTOMATIC mode: always keep the log
        if Config.LOGS_MODE == "AUTOMATIC":
            print()
            success_message(f"Saved results to log file: {log_path}")
            print()
            return

        # PROMPT mode: ask user
        if Config.LOGS_MODE == "PROMPT":
            LogManager._prompt_save_or_delete(module_fullname, log_path)
            return

        # Unknown mode: warn and keep the file so data is not silently lost
        error_message(
            f'Unknown LOGS_MODE "{Config.LOGS_MODE}". '
            f'Expected "PROMPT", "AUTOMATIC", or "DISABLED". '
            f"Log file kept at: {log_path}"
        )

    @staticmethod
    def _prompt_save_or_delete(module_fullname: str, log_path: Path) -> None:
        """
        Prompt the user to save or delete the log file.

        Args:
            module_fullname (str): Full name of the module
            log_path (Path): Path to the log file
        """
        while True:
            log_choice = input(
                f"[{green('>', 'bold')}] {cyan(f'Do you want to save the {module_fullname} results to a log file? (y/n): ', 'bold')}"
            ).lower()

            if log_choice in ("y", "yes"):
                print()
                success_message(f"Saved results to log file: {log_path}")
                print()
                return
            elif log_choice in ("n", "no"):
                LogManager._delete_log(log_path)
                return
            else:
                print()
                error_message('Invalid option. Please enter "y" for YES or "n" for NO.')
                print()

    @staticmethod
    def _delete_log(log_path: Path) -> None:
        """
        Delete a log file and show confirmation message.

        Args:
            log_path (Path): Path to the log file to delete
        """
        try:
            os.remove(log_path)
            print()
            success_message("Log file deleted.")
            print()
        except OSError as e:
            error_message(f"Error: Could not delete log file: {e}")


# Legacy function for backward compatibility (used by existing code)
def log_prompt(module_fullname: str, log_filename: str) -> None:
    """
    Legacy wrapper for backward compatibility.

    DEPRECATED: Use LogManager.handle_log_prompt() instead.

    Args:
        module_fullname (str): The full name of the module
        log_filename (str): The log file path (as string)
    """
    log_path = Path(log_filename) if log_filename else None
    LogManager.handle_log_prompt(module_fullname, log_path)
