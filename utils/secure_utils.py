"""Security utilities for safe command execution.

This module provides helpers for validating network inputs and running
commands in a safer way.

- `safe_clear_screen` uses `os.name` and falls back gracefully.
- `validate_ip_range` has an explicit `restrict_to_private` parameter.
- `validate_hostname` accepts trailing dots and optional IDN (via IDNA encoding),
  and can optionally allow underscores.
- `run_user_command` favors `shell=False`, uses `shlex.split`,
  sets a timeout and captures output by default.
"""

import os
import shutil
import shlex
import subprocess
import ipaddress
import re
from typing import Union, List


def safe_clear_screen() -> None:
    """Safely clear the terminal screen.

    Uses the platform to determine the right command. This is best-effort and
    will not raise on failure.
    """
    try:
        if os.name == "nt":
            # If detected operating system is Windows
            subprocess.run("cls", shell=True, check=False)
        else:
            if shutil.which("clear"):
                # Else, if detected operating system is Linux/MacOS
                subprocess.run(["clear"], check=False)
            else:
                # fallback: attempt /usr/bin/clear
                subprocess.run(["/usr/bin/clear"], check=False)
    except Exception as e:
        # Log the exception to the console for debugging purposes
        print(f"[netsploit] Warning: Failed to clear screen: {e}")


def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address format.

    Args:
        ip (str): IP address to validate

    Returns:
        bool: True if valid IP address, False otherwise
    """
    try:
        _ = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_ip_range(ip_range: str, restrict_to_private: bool = True) -> bool:
    """
    Validate IP range or CIDR notation.

    Args:
        ip_range (str): IP range or CIDR notation (e.g., '192.168.1.0/24' or
            '192.168.1.1-192.168.1.254')
        restrict_to_private (bool): If True, only accept private networks/ranges
            (keeps previous behaviour). If False, allow public ranges as well.

    Returns:
        bool: True if valid IP range, False otherwise
    """
    try:
        if '/' in ip_range:  # CIDR notation
            network = ipaddress.ip_network(ip_range, strict=False)
            if restrict_to_private:
                return network.is_private
            return True
        elif '-' in ip_range:  # IP range
            start_ip, end_ip = ip_range.split('-', 1)
            start = ipaddress.ip_address(start_ip.strip())
            end = ipaddress.ip_address(end_ip.strip())
            if start >= end:
                return False
            if restrict_to_private:
                return start.is_private and end.is_private
            return True
        return False
    except ValueError:
        return False


def validate_port(port: Union[str, int], allow_privileged: bool = False) -> bool:
    """
    Validate if a port number is valid.

    Args:
        port (Union[str, int]): Port number to validate
        allow_privileged (bool): Whether to allow privileged ports (1-1023).
            Default False to avoid accidental use of privileged ports.

    Returns:
        bool: True if valid port number, False otherwise
    """
    try:
        port_num = int(port)
        if not allow_privileged:
            return 1024 <= port_num <= 65535
        return 1 <= port_num <= 65535
    except (ValueError, TypeError):
        return False


def validate_hostname(
    hostname: str,
    allow_trailing_dot: bool = True,
    allow_idn: bool = True,
    allow_underscores: bool = False,
) -> bool:
    """
    Validate hostname format.

    This function validates hostnames per common rules:
    - total length <= 255
    - each label 1-63 characters
    - labels may contain letters, digits and hyphens (optionally underscores)
    - labels must not start or end with a hyphen

    Options:
        allow_trailing_dot: accept and strip a trailing dot (FQDN)
        allow_idn: attempt IDNA encoding for Unicode hostnames (returns False if encoding fails)
        allow_underscores: permit underscore character in labels (non-RFC but sometimes used)

    Returns:
        bool: True if valid hostname, False otherwise
    """
    if not hostname:
        return False

    # Accept and strip trailing dot if present (fully qualified domain name)
    if allow_trailing_dot and hostname.endswith('.'):
        hostname = hostname[:-1]

    if len(hostname) > 255:
        return False

    # Convert Unicode hostnames to ASCII using IDNA if requested
    if allow_idn:
        try:
            hostname = hostname.encode('idna').decode('ascii')
        except Exception as e:
            from utils.font_styles import error_message
            error_message(f"Warning: Failed to encode hostname '{hostname}' with IDNA: {e}")
            return False

    # Build label regex
    if allow_underscores:
        label_re = r"(?!-)[A-Z0-9_-]{1,63}(?<!-)$"
    else:
        label_re = r"(?!-)[A-Z0-9-]{1,63}(?<!-)$"

    allowed = re.compile(label_re, re.IGNORECASE)

    labels = hostname.split('.')
    if any(len(l) == 0 for l in labels):
        return False

    return all(allowed.match(label) for label in labels)


def run_user_command(
    cmd: Union[str, List[str]],
    timeout: int = 30,
    use_shell: bool = False,
    capture_output: bool = True,
) -> subprocess.CompletedProcess:
    """
    Run a user-provided command in a safer way.

    - `cmd` may be a string or a list of strings. If a list is provided it is used
      directly as argv for `subprocess.run` (recommended when arguments are already
      separated).
    - Prefer `use_shell=False`. If False and `cmd` is a string, it is split using
      `shlex.split`.
    - A timeout is applied to avoid hanging processes.
    - Output is captured by default and returned as strings (text mode).

    Note: This helper reduces some risks (no shell expansion by default, timeout),
    but does NOT sandbox the command. For untrusted commands consider running in
    a container or a dedicated restricted user.
    """
    # If caller passed a list of args, use that directly. This avoids shlex.
    if isinstance(cmd, list):
        if use_shell:
            raise ValueError("use_shell=True with a list cmd is not supported; pass a string when use_shell=True")
        args = [str(x) for x in cmd]
        return subprocess.run(
            args,
            shell=False,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
        )

    # At this point cmd is expected to be a string
    if use_shell:
        # shell=True is dangerous; caller must explicitly opt-in
        return subprocess.run(
            cmd,
            shell=True,
            timeout=timeout,
            capture_output=capture_output,
            text=True,
        )

    args: List[str] = []
    try:
        args = shlex.split(cmd)
    except ValueError:
        # fallback: treat the whole string as a single argument
        args = [cmd]

    return subprocess.run(
        args,
        shell=False,
        timeout=timeout,
        capture_output=capture_output,
        text=True,
    )
