"""Network Scanner Module
This module uses nmap to scan and find devices connected to the network.
"""

from .base import BaseModule
from utils.secure_utils import run_user_command
from utils.colors import cyan, green, yellow
from utils.logging import LogManager
from utils.font_styles import error_message, info_message, success_message
from utils.config import Config


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
        ip_range = self._get_local_ip_range()
        if not ip_range:
            error_message(
                "Could not determine local IP range. Cannot proceed with network scan."
            )
            return

        self._run_network_scan(ip_range)

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
        """Get the IP address range of the local network."""
        try:
            cp = run_user_command("ip route show", timeout=5, use_shell=False, capture_output=True)
            stdout = cp.stdout or ""
            for line in stdout.splitlines():
                if line.startswith("default via"):
                    parts = line.split()
                    if len(parts) >= 3:
                        gateway = parts[2]
                        ip_parts = gateway.split(".")
                        if len(ip_parts) == 4:
                            network = ".".join(ip_parts[:3]) + ".0/24"
                            return network
        except Exception as e:
            error_message(f"Error parsing network information: {e}")
        return None

    def _run_network_scan(self, ip_range: str) -> None:
        """Run the nmap network scan and handle logging."""
        info_message(
            f"Running {green('Network Scan', 'bold')} with IP range {cyan(ip_range, 'bold')}, this may take up to two minutes",
            False,
        )
        info_message(
            "Running a Network Scan properly requires the command to be run using sudo",
            True,
        )
        print()

        log_path = LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None

        try:
            cmd_args = ["sudo", "nmap", "-sn", "-T4", ip_range]
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
            return

        self._handle_results(log_path)
        print(f"To run a network scan, use {yellow('run', 'bold')} command.")
        print("This module scans your local network to find connected devices.")
        print("Available commands:")
        print("  - run: Start the network scan")
        print("  - help: Show this help message")
        print("  - back: Return to main menu")
        print("  - clear: Clear the screen")
        print("  - exit: Exit the program")
        print()
