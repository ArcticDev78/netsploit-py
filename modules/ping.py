"""Ping Module
- Ping the target device to check its accessibility and the time taken to send the
  packets back and forth.
"""

import platform

from utils.colors import blue, cyan, green, yellow
from utils.config import Config
from utils.font_styles import error_message, info_message, success_message
from utils.logging import LogManager
from utils.secure_utils import run_user_command, validate_hostname, validate_ip_address

from .base import BaseModule


class Ping(BaseModule):
    """Ping module for checking target accessibility and latency."""

    def __init__(self):
        self.name = "ping"
        self.full_name = "Ping"
        self.description = (
            "Check the accessibility and latency in reaching the target device"
        )
        self.options = "<prompt>: TARGET"
        self.requires_target = True
        self.target = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self, target=None):
        """Execute ping on target (non-interactive)."""
        if target is not None:
            self.target = target
        if not self._validate_target():
            return
        log_path = self._execute_core_logic()
        self._handle_results(log_path)

    def main(self):
        """Interactive prompt mode."""
        print(f"{yellow('netsploit', 'underlined')} => {blue('(ping)', 'bold')}\n")
        print(
            f"{yellow('Ping modes:', ['bold', 'underlined'])}\n"
            f"1. {cyan('ping', 'bold')} [Basic - OS-Provided]\n"
            f"2. {cyan('nping', 'bold')} [Advanced - Nmap-provided]\n"
        )
        while True:
            pingmode = input(
                f"[{green('>', 'bold')}] {cyan('Enter ping mode to use: ', 'bold')}"
            ).lower()

            if pingmode in ("ping", "1"):
                self._ping_interactive()
                return
            elif pingmode in ("nping", "2"):
                self._nping_interactive()
                return
            else:
                print()
                error_message(
                    f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n'
                )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_ping_args(target: str, count: int = 5) -> list:
        """Build platform-appropriate ping arguments.

        Linux/macOS use ``-c`` for packet count; Windows uses ``-n``.
        """
        if platform.system() == "Windows":
            return ["ping", "-n", str(count), str(target)]
        else:
            return ["ping", "-c", str(count), str(target)]

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
        """Execute the ping command (non-interactive)."""
        info_message(f"Pinging {self.target} (5 times)...\n")
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )
        try:
            if log_path:
                # Capture output for logging
                result = run_user_command(
                    Ping._build_ping_args(str(self.target)),
                    timeout=20,
                    use_shell=False,
                    capture_output=True,
                )
                with open(log_path, "w") as f:
                    f.write(result.stdout or "")
                print(result.stdout or "")
            else:
                # Stream without capturing
                run_user_command(
                    Ping._build_ping_args(str(self.target)),
                    timeout=20,
                    use_shell=False,
                    capture_output=False,
                )
        except Exception as e:
            error_message(f"Ping failed: {e}")
            return None

        print()
        success_message(f"Finished pinging {self.target}\n")
        return log_path

    def _nping_interactive(self):
        """Interactive nping logic."""
        target = input(f"[{green('>', 'bold')}] {cyan('IP of device to nping:')} ")
        if not (validate_ip_address(target) or validate_hostname(target)):
            error_message(f'Invalid target "{target}"')
            return
        print()
        info_message(f"Pinging {target} (5 times)...")
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )
        try:
            if log_path:
                result = run_user_command(
                    ["nping", "-c", "5", str(target)],
                    timeout=20,
                    use_shell=False,
                    capture_output=True,
                )
                with open(log_path, "w") as f:
                    f.write(result.stdout or "")
                print(result.stdout or "")
            else:
                run_user_command(
                    ["nping", "-c", "5", str(target)],
                    timeout=20,
                    use_shell=False,
                    capture_output=False,
                )
        except Exception:
            error_message(f"Nping command failed or timed out for {target}")
            return

        print()
        success_message(f"Finished pinging {target}\n")
        if log_path:
            LogManager.handle_log_prompt("Ping", log_path)

    def _ping_interactive(self):
        """Interactive ping logic."""
        target = input(f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} ")
        if not (validate_ip_address(target) or validate_hostname(target)):
            error_message(f'Invalid target "{target}"')
            return
        print()
        info_message(f"Pinging {target} (5 times)...")
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )
        try:
            if log_path:
                result = run_user_command(
                    Ping._build_ping_args(str(target)),
                    timeout=20,
                    use_shell=False,
                    capture_output=True,
                )
                with open(log_path, "w") as f:
                    f.write(result.stdout or "")
                print(result.stdout or "")
            else:
                run_user_command(
                    Ping._build_ping_args(str(target)),
                    timeout=20,
                    use_shell=False,
                    capture_output=False,
                )
        except Exception:
            error_message(f"Ping command failed or timed out for {target}")
            return

        print()
        success_message(f"Finished pinging {target}\n")
        if log_path:
            LogManager.handle_log_prompt("Ping", log_path)
