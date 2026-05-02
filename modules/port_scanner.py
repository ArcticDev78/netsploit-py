"""Port Scanner Module
- Scan the target device for open ports
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


class PortScanner(BaseModule):
    """PortScanner module for scanning open ports on a target device."""

    def __init__(self):
        self.name = "port-scanner"
        self.full_name = "Port Scanner"
        self.description = "Scan the target device for open ports"
        self.options = "TARGET"
        self.requires_target = True
        self.target = None

    def run(self, target=None):
        """Execute port scan on target."""
        if target is None:
            error_message("Target required for Port Scanner")
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
        """Execute the port scanner nmap scan."""
        info_message(f"Running port scan on {self.target}")
        print()

        # Get log path only if logging is enabled
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )

        cmd_args = get_privilege_prefix() + [
            "nmap",
            "-sS",
            "-sV",
            "-T4",
            "--top-ports",
            "5000",
            "--open",
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
            error_message(f"Port scan failed: {e}")
            return None

        print()
        success_message(f"Finished scanning {self.target}")
        return log_path
