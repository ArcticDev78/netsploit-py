""" Device Info Module
- Module to lookup/retrieve various information about the TARGET device
"""

# Import required modules and libraries
from .base import BaseModule
from utils.secure_utils import run_user_command, validate_ip_address, validate_hostname
from utils.logging import LogManager
from utils.config import Config
from utils.font_styles import error_message, info_message, success_message


class DeviceInfo(BaseModule):
    """DeviceInfo module for gathering comprehensive information about a target device."""

    def __init__(self):
        self.name = "device-info"
        self.full_name = "Device Info"
        self.description = "Get info about the target device"
        self.options = "TARGET"
        self.requires_target = True
        self.target = None

    def run(self, target=None):
        """Execute device info scan on target."""
        if target is None:
            error_message("Target required for Device Info")
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
        if not (validate_ip_address(target) or validate_hostname(target)):
            error_message(f'Invalid target "{target}"')
            return False
        return True

    def _execute_core_logic(self):
        """Execute the device info nmap scan."""
        info_message(f"Running Device Info scan on {self.target}")
        info_message("Running a Device Info scan properly requires the command to be run using sudo")
        print()

        # Get log path only if logging is enabled
        log_path = LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None

        cmd_args = [
            "sudo",
            "nmap",
            "-v",
            "-A",
            "-T4",
            self.target,
            "-Pn",
            "-f",
        ]
        if log_path:
            cmd_args.extend(["-oN", str(log_path)])

        try:
            run_user_command(cmd_args, timeout=300, use_shell=False, capture_output=False)
        except Exception as e:
            error_message(f"Device Info scan failed: {e}")
            return None

        print()
        success_message(f"Finished scanning {self.target}")
        return log_path
