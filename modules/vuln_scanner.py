"""
Vulnerability Scanner Module

This module provides functionality to scan targets for potential vulnerabilities that can be exploited.
It uses nmap with the nmap-vulners script to perform the scan.
"""

from utils.config import Config
from utils.font_styles import error_message, info_message, success_message
from utils.logging import LogManager
from utils.secure_utils import run_user_command, validate_hostname, validate_ip_address

from .base import BaseModule


class VulnerabilityScanner(BaseModule):
    """VulnerabilityScanner module for scanning targets for potential vulnerabilities."""

    def __init__(self):
        self.name = "vuln-scanner"
        self.full_name = "Vulnerability Scanner"
        self.description = "Scan target for potential vulnerabilities"
        self.options = "TARGET"
        self.requires_target = True
        self.target = None

    def run(self, target=None):
        """Execute vulnerability scan on target."""
        if target is None:
            error_message("Target required for Vulnerability Scanner")
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
        if target is None:
            error_message("No target specified")
            return False
        if not (validate_ip_address(str(target)) or validate_hostname(str(target))):
            error_message(f'Invalid target "{target}"')
            return False
        return True

    def _execute_core_logic(self):
        """Execute the vulnerability scanner nmap scan."""
        info_message(f"Running Vulnerability scan on {self.target}")
        print()

        # Get log path only if logging is enabled
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )

        cmd_args = [
            "nmap",
            "--script",
            "nmap-vulners/",
            "-sV",
            self.target,
            "-Pn",
        ]
        if log_path:
            cmd_args.extend(["-oN", str(log_path)])

        try:
            run_user_command(
                cmd_args, timeout=300, use_shell=False, capture_output=False
            )
        except Exception as e:
            error_message(f"Vulnerability scan failed: {e}")
            return None

        print()
        success_message(f"Finished scanning {self.target}")
        return log_path
