"""Network Scanner Module
This module uses nmap to scan and find devices connected to the network.
"""

import netifaces  # type: ignore[import-untyped]

from utils.colors import yellow
from utils.config import Config
from utils.font_styles import error_message, info_message, success_message
from utils.logging import LogManager
from utils.secure_utils import get_privilege_prefix, run_user_command

from .base import BaseModule


class NetworkScanner(BaseModule):
    """NetworkScanner module that uses nmap to scan and find devices connected to the network."""

    def __init__(self) -> None:
        self.name: str = "network-scanner"
        self.full_name: str = "Network Scanner"
        self.description: str = (
            "Find devices connected to the network and retrieve information about them"
        )
        self.options: str = "(none)"
        self.requires_target = False

    def run(self, *args, **kwargs) -> None:
        """Execute network scan."""
        return self._execute_core_logic(interactive=False)

    def _execute_core_logic(self, interactive=False):
        """Execute the network scan logic (required by BaseModule)."""
        info_message("Running Network Scan on local network")
        info_message(
            "Running a Network Scan properly requires the command to be run using sudo"
        )
        print()
        ip_range = self._get_local_ip_range()
        if not ip_range:
            error_message(
                "Could not determine local IP range. Cannot proceed with network scan."
            )
            return None

        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )

        try:
            cmd_args = get_privilege_prefix() + ["nmap", "-sn", "-T4", ip_range]
            if log_path:
                cmd_args.extend(["-oN", str(log_path)])

            run_user_command(
                cmd_args,
                timeout=300,
                use_shell=False,
                capture_output=False,
            )
            print()
            success_message("Finished scanning network")
        except Exception as e:
            error_message(f"Failed to run nmap scan: {e}")
            return None

        self._handle_results(log_path)
        if interactive:
            print(f"To run a network scan, use {yellow('run', 'bold')} command.")
            print("This module scans your local network to find connected devices.")
            print("Available commands:")
            print("  - run: Start the network scan")
            print("  - help: Show this help message")
            print("  - back: Return to main menu")
            print("  - clear: Clear the screen")
            print("  - exit: Exit the program")
            print()
        return None

    def main(self) -> None:
        """Interactive prompt mode."""
        self._show_module_header()
        ip_range = self._get_local_ip_range()
        if not ip_range:
            error_message(
                "Could not determine local IP range. Cannot proceed with network scan."
            )
            self._prompt_continue()
            return

        self._run_network_scan(ip_range)
        self._prompt_continue()

    def _get_local_ip_range(self) -> str | None:
        """Get the IP address range of the local network using Python (cross-platform)."""
        try:
            gateways = netifaces.gateways()
            default_gw = gateways.get("default", {})
            if netifaces.AF_INET in default_gw:
                gateway_ip = default_gw[netifaces.AF_INET][0]
                parts = gateway_ip.split(".")
                if len(parts) == 4:
                    return ".".join(parts[:3]) + ".0/24"
        except Exception as e:
            error_message(f"Error determining network range: {e}")
        return None

    def _run_network_scan(self, ip_range: str) -> None:
        """Run the nmap network scan and handle logging."""
        self._execute_core_logic(interactive=True)
