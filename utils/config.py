"""
Configuration Module

This module defines the Config class, which stores settings and variables
to be accessed by other modules in the project.

Usage:
    from utils.config import Config

    # Accessing configuration values
    if Config.LOGS_ENABLED:
        log_path = Config.LOGS_FOLDER_PATH
        # ... logging logic ...

    oui_file = Config.OUI_FILE_PATH
    # ... OUI lookup logic ...

The configuration can be modified by changing the class attributes directly
in this file or by subclassing Config in other modules if needed.
"""

# Import required library for configuring paths
from pathlib import Path


# Config class to store and access all NetSploit program configuration options
class Config:
    # 1) Logging Configuration

    # a) Enable/Disable Logs
    LOGS_ENABLED: bool = True
    """
    Flag to enable or disable logging throughout the application.
    If False, no log files will be created regardless of module behavior.
    """

    # b) Logging Mode (PROMPT, AUTOMATIC, or DISABLED)
    # - PROMPT: Ask user to save/delete log after each module run
    # - AUTOMATIC: Always save logs without prompting
    # - DISABLED: Never create logs (overrides LOGS_ENABLED if False)
    LOGS_MODE: str = "PROMPT"
    """
    Controls logging behavior:
    - "PROMPT": Ask user whether to save log after module execution
    - "AUTOMATIC": Automatically save all logs without prompting
    - "DISABLED": Disable all logging (same as LOGS_ENABLED=False)
    """

    # c) Path to Logs Folder
    LOGS_FOLDER_PATH: Path = Path.cwd() / "logs"
    """
    Path to the folder where log files will be stored.
    Defaults to a 'logs' subdirectory in the current working directory.
    """

    # 2) OUI (Organizationally Unique Identifier) Configuration

    # a) OUI Filename
    OUI_FILENAME: str = "oui.txt"
    """Filename of the OUI database file."""

    # b) Path to OUI File
    OUI_FILE_PATH: Path = Path.cwd() / "resources" / OUI_FILENAME
    """
    Full path to the OUI database file.
    Defaults to a file named 'oui.txt' in the 'resources' subdirectory of the project root.
    """
