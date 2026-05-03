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

from pathlib import Path


class Config:
    # Resolve the project root relative to this file so that paths are correct
    # regardless of which directory the user runs netsploit.py from.
    # Layout: <project_root>/utils/config.py  →  parent.parent = project root
    _PROJECT_ROOT: Path = Path(__file__).parent.parent

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
    LOGS_FOLDER_PATH: Path = _PROJECT_ROOT / "logs"
    """
    Path to the folder where log files will be stored.
    Anchored to the project root so it works regardless of the working directory.
    """

    # 2) OUI (Organizationally Unique Identifier) Configuration

    # a) OUI Filename
    OUI_FILENAME: str = "oui.txt"
    """Filename of the OUI database file."""

    # b) Path to OUI File
    OUI_FILE_PATH: Path = _PROJECT_ROOT / "resources" / OUI_FILENAME
    """
    Full path to the OUI database file.
    Anchored to the project root so it works regardless of the working directory.
    """

    # c) Upstream URL for the OUI database
    OUI_SOURCE_URL: str = "https://www.wireshark.org/download/automated/data/manuf"
    """
    Canonical URL of the Wireshark-maintained OUI/manuf database.
    Used by the OUI updater to fetch the latest version.
    """

    # d) Maximum age (in days) before the local OUI file is refreshed
    OUI_MAX_AGE_DAYS: int = 7
    """
    How many days the local OUI database is considered fresh.
    When the file is older than this threshold netsploit will attempt to
    download a newer copy from OUI_SOURCE_URL at startup.
    The IEEE publishes OUI updates weekly (every Sunday) and Wireshark
    regenerates its manuf/oui.txt on the same cadence, so 7 days keeps
    you in sync without unnecessarily hammering the server.
    Set to 0 to always update, or a large number to effectively disable
    automatic updates.
    """
