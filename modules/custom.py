"""Custom Nmap Command Runner"""

import shlex

from utils.colors import blue, cyan, green, yellow
from utils.font_styles import error_message, success_message
from utils.secure_utils import run_user_command


def custom():
    """Prompt for a custom nmap command and run it safely without a shell."""
    print(f"{yellow('netsploit', 'underlined')} => {blue('(custom)', 'bold')}\n")
    custom_nmap_cmd = input(
        f"[{green('>', 'bold')}] {cyan('Enter custom nmap command to run: ', 'bold')}"
    ).strip()

    if not custom_nmap_cmd:
        error_message("No command entered.")
        return

    # Parse the command safely — shlex splits on shell quoting rules without
    # actually invoking a shell, so there is no injection risk.
    try:
        parts = shlex.split(custom_nmap_cmd)
    except ValueError as e:
        error_message(f"Invalid command syntax: {e}")
        return

    # Validate: the command must be a plain nmap invocation, with an optional
    # leading 'sudo'.  We check the parsed list (not the raw string) so that
    # tricks like "nmapper" or "nmap;evil" are rejected cleanly.
    if parts[0] == "sudo":
        if len(parts) < 2 or parts[1] != "nmap":
            error_message(
                f"Your command must be an nmap command. "
                f"To run other shell commands, use the {yellow('shell', 'bold')} command."
            )
            return
    elif parts[0] != "nmap":
        error_message(
            f"Your command must be an nmap command. "
            f"To run other shell commands, use the {yellow('shell', 'bold')} command."
        )
        return

    print()
    success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
    print()
    # Pass the pre-parsed list — no shell involved, no injection risk.
    run_user_command(parts, use_shell=False, timeout=300, capture_output=False)
    print()
