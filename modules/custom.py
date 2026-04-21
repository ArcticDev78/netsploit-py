""" Custom Nmap Command Runner """

# Import required modules and libraries

from utils.secure_utils import run_user_command

from utils.colors import blue, cyan, green, yellow

from modules.shell import Shell
from utils.font_styles import error_message, success_message


def custom():
    """Function to receive input of the custom nmap command to run, with input validation"""
    from utils.prompt import prompt
    import shlex

    print(f'{yellow("netsploit", "underlined")} => {blue("(custom)", "bold")}\n')
    custom_nmap_cmd = input(
        f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}'
    ).strip()

    # Basic validation: must start with nmap or sudo nmap, and not contain dangerous shell metacharacters
    def is_safe_nmap_command(cmd: str) -> bool:
        # Only allow commands that start with 'nmap' or 'sudo nmap'
        allowed_prefixes = ["nmap", "sudo nmap"]
        if not any(cmd.startswith(prefix) for prefix in allowed_prefixes):
            return False
        # Disallow dangerous shell metacharacters
        dangerous = [';', '|', '&', '`', '$(', '>', '<', '&&', '||']
        if any(d in cmd for d in dangerous):
            return False
        # Try to parse with shlex to catch obvious syntax errors
        try:
            shlex.split(cmd)
        except Exception:
            return False
        return True

    if not is_safe_nmap_command(custom_nmap_cmd):
        error_message("Invalid or potentially unsafe nmap command. Please enter a valid nmap command without shell metacharacters.")
        print()
        prompt()
        return

    if custom_nmap_cmd.startswith("nmap"):
        print()
        success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
        print()
        run_user_command(custom_nmap_cmd, use_shell=True, timeout=300, capture_output=False)
        print()
        prompt()

    elif custom_nmap_cmd.startswith("sudo"):
        cmd = custom_nmap_cmd.split()
        if len(cmd) > 1 and cmd[1] == "nmap":
            print()
            success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
            print()
            run_user_command(custom_nmap_cmd, use_shell=True, timeout=300, capture_output=False)
            print()
            prompt()
        else:
            print()
            error_message(
                f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.'
            )
            print()
            choice = input(
                f'[{green(">", "bold")}] {cyan("Did you mean to run a shell command? [y/n]: ", "bold")}'
            )
            if choice == "y":
                print()
                Shell().run(custom_nmap_cmd)
            elif choice == "n":
                print()
                prompt()
            else:
                error_message(f'Invalid option "{choice}"')
                prompt()

    else:
        print()
        error_message(
            f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.'
        )
        print()
        choice = input(
            f'[{green(">", "bold")}] {cyan("Did you mean to run a shell command? [y/n]: ", "bold")}'
        )
        if choice == "y":
            print()
            Shell().run(custom_nmap_cmd)
        elif choice == "n":
            print()
            prompt()
        else:
            error_message(f'Invalid option "{choice}"')
            prompt()
