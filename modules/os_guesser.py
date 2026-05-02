"""OS Guesser Module
- Module to find/guess the operating system running on the target device
"""

# Import required modules and libraries
from utils.config import Config
from utils.font_styles import error_message, info_message, success_message
from utils.logging import LogManager
from utils.secure_utils import (
    get_privilege_prefix,
    run_user_command,
    validate_hostname,
    validate_ip_address,
)

from .base import BaseModule


class OSGuesser(BaseModule):
    """OSGuesser module for identifying the operating system of a target device."""

    def __init__(self):
        self.name = "os-guesser"
        self.full_name = "OS Guesser"
        self.description = "Guess the operating system running on a device"
        self.options = "TARGET"
        self.requires_target = True
        self.target = None

    def run(self, target=None):
        """Execute OS guessing scan on target."""
        if target is None:
            error_message("Target required for OS Guesser")
            return

        self.target = target

        if not self._validate_target():
            return

        log_path = self._execute_core_logic()
        self._handle_results(log_path)

    def main(self):
        """Interactive prompt mode."""
        self._show_module_header()
        self.target = self._get_input("Target IP or hostname")

        if not self._validate_target():
            self._prompt_continue()
            return

        log_path = self._execute_core_logic()
        self._handle_results(log_path)
        self._prompt_continue()

    def _validate_target(self, target=None):
        """Validate target IP or hostname."""
        target = target or self.target
        if not target or not (
            validate_ip_address(str(target)) or validate_hostname(str(target))
        ):
            error_message(f'Invalid target "{target}"')
            return False
        return True

    def _execute_core_logic(self):
        """Execute the OS guessing nmap scan."""
        info_message(f"Running OS Guesser scan on {self.target}")
        info_message(
            "Running a OS Guesser scan properly requires the command to be run using sudo"
        )
        print()

        # Get log path only if logging is enabled
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )

        cmd_args = get_privilege_prefix() + [
            "nmap",
            "-O",
            "--osscan-guess",
            "-sV",
            "-T4",
            "-p",
            "1-1024",
            "-Pn",
            str(self.target),
        ]
        if log_path:
            cmd_args.extend(["-oN", str(log_path)])

        try:
            run_user_command(
                cmd_args, timeout=300, use_shell=False, capture_output=False
            )
        except Exception as e:
            error_message(f"OS Guesser scan failed: {e}")
            return None

        print()
        success_message(f"Finished scanning {self.target}")
        return log_path
