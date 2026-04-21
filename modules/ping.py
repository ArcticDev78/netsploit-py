"""Ping Module
- Ping the target device to check its accessibility and the time taken to send the
  packets back and forth.
"""

# Import required modules and libraries
from .base import BaseModule
from utils.secure_utils import validate_ip_address, validate_hostname, run_user_command
from utils.logging import LogManager
from utils.colors import green, cyan
from utils.font_styles import error_message, info_message, success_message


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

    def run(self, target=None):
        """Execute ping on target."""
        if target is None:
            error_message("Target required for Ping")
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
        print()

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
        """Execute the ping command."""
        info_message(f"Pinging {self.target} (5 times)...\n")

        log_path = LogManager.get_log_file_path(self.name)

        try:
            if log_path:
                # Capture output for logging
                result = run_user_command(
                    ["ping", "-c", "5", self.target],
                    timeout=20,
                    use_shell=False,
                    capture_output=True
                )
                with open(log_path, "w") as f:
                    f.write(result.stdout or "")
            else:
                # Stream without capturing
                run_user_command(
                    ["ping", "-c", "5", self.target],
                    timeout=20,
                    use_shell=False,
                    capture_output=False
                )
        except Exception as e:
            error_message(f"Ping failed: {e}")
            return None

        print()
        success_message(f"Finished pinging {self.target}\n")
        return log_path

            # Handle log save/delete prompt
            LogManager.handle_log_prompt("Ping", log_path)

    def __nping(self, target_param=None):
        """
        `target_param` is the method parameter to use as the target to ping.
        This parameter is handled in two ways:
        1) If `target_param` IS supplied when calling this method, that will be taken as the
           target to ping.
        2) If `target_param` is NOT supplied when calling this method, the `target` variable
           (through `input`) will be taken as the target to ping.
        """
        from utils.logging import LogManager
        from utils.secure_utils import run_user_command

        if target_param:
            if not (validate_ip_address(target_param) or validate_hostname(target_param)):
                error_message(f'Invalid target "{target_param}"')
                return
            print()
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target_param} (5 times)...")

            # Get log path
            log_path = LogManager.get_log_file_path(self.name)

            try:
                if log_path:
                    # Capture output for logging
                    result = run_user_command(["nping", "-c", "5", target_param], timeout=20, use_shell=False, capture_output=True)
                    with open(log_path, "w") as f:
                        f.write(result.stdout or "")
                else:
                    # Stream without capturing
                    run_user_command(["nping", "-c", "5", target_param], timeout=20, use_shell=False, capture_output=False)
            except Exception:
                error_message(f"Nping command failed or timed out for {target_param}")
                return

            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target_param}\n")

            # Handle log save/delete prompt
            LogManager.handle_log_prompt("Ping", log_path)
        else:
            # Ask the user for the IP of the device to ping
            target = input(f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} ")
            print()
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target} (5 times)...")

            # Get log path
            log_path = LogManager.get_log_file_path(self.name)

            try:
                if log_path:
                    # Capture output for logging
                    result = run_user_command(["nping", "-c", "5", target], timeout=20, use_shell=False, capture_output=True)
                    with open(log_path, "w") as f:
                        f.write(result.stdout or "")
                else:
                    # Stream without capturing
                    run_user_command(["nping", "-c", "5", target], timeout=20, use_shell=False, capture_output=False)
            except Exception:
                error_message(f"Nping command failed or timed out for {target}")
                return

            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target}\n")

            # Handle log save/delete prompt
            LogManager.handle_log_prompt("Ping", log_path)

    def run(self, pingmode):
        """
        `pingmode` parameter is used to specify one of the following two modes to ping the target:
        1. `ping` -> This is the OS built-in ping command.
        2. `nping` -> This command comes along with your `nmap` install.
        """
        from utils.prompt import prompt

        # If the user chooses to use the first option - ping
        if pingmode == ("ping", "1"):
            already_set_target = get_target()
            # If the user has NOT already provided a target before, then prompt the user for it
            # and use that in `self.__ping()`
            if already_set_target is False:
                target = input(
                    f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} "
                )
                print()
                self.__ping(target)
                prompt()
            # Else, check if the user HAS already provided a target before, and if it is so,
            # prompt the user if they want to use the same target.
            # If the user responds yes, pass the `already_set_target` in `self.__ping()`
            # Otherwise, prompt the user for their desired target
            else:
                # Prompt the user if they want to use the `already_set_target` or not
                userchoice = input(
                    (
                        f"[{green('>', 'bold')}] {cyan(f'Target has already been set. Do you want to ping {already_set_target}? [y/n]: ')}"
                    )
                )
                if userchoice == "y":
                    print()
                    self.__ping(already_set_target)
                    prompt()

                elif userchoice == "n":
                    print()
                    success_message(
                        f"OK, {red('not', 'bold')} using {already_set_target} as target."
                    )
                    print()
                    target = input(
                        f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} "
                    )
                    print()
                    self.__ping(target)
                    prompt()

        # Else, if the user chooses to use the second option - nping
        elif pingmode in ("nping", "2"):
            already_set_target = get_target()
            # If the user has NOT already provided a target before, then prompt the user for it
            # and use that in `self.__nping()`
            if already_set_target is False:
                # self.__nping()
                target = input(
                    f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} "
                )
                print()
                self.__nping(target)
                prompt()
            else:
                # Else, check if the user HAS already provided a target before, and if it is so,
                # prompt the user if they want to use the same target.
                # If the user responds yes, pass the `already_set_target` in `self._n_ping()`
                # Otherwise, prompt the user for their desired target

                # Prompt the user if they want to use the `already_set_target` or not
                userchoice = input(
                    (
                        f"[{green('>', 'bold')}] {cyan(f'Target has already been set. Do you want to ping {already_set_target}? [y/n]: ')}"
                    )
                )
                if userchoice == "y":
                    print()
                    self.__nping(already_set_target)
                    prompt()

                elif userchoice == "n":
                    print()
                    success_message(
                        f"OK, {red('not', 'bold')} using {already_set_target} as target."
                    )
                    print()
                    target = input(
                        f"[{green('>', 'bold')}] {cyan('IP of device to ping:')} "
                    )
                    print()
                    self.__nping(target)
                    prompt()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import prompt

        print(f"{yellow('netsploit', 'underlined')} => {blue('(ping)', 'bold')}\n")

        # Prompt the user if they want to use: 1) ping `self.__ping()` or 2) nping `self.__nping()`
        print(
            f"{yellow('Ping modes:', ['bold', 'underlined'])}\n1. {cyan('ping', 'bold')} [Basic - OS-Provided]\n2. {cyan('nping', 'bold')} [Advanced - Nmap-provided]\n"
        )
        pingmode = input(
            f"[{green('>', 'bold')}] {cyan('Enter ping mode to use: ', 'bold')}"
        ).lower()

        # If the user chooses to use the first option - ping
        if pingmode == ("ping", "1"):
            self.run("ping")
            prompt()

        # Else, if the user chooses to use the second option - nping
        elif pingmode in ("nping", "2"):
            self.run("nping")
            prompt()

        else:
            print()
            error_message(
                f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n'
            )
            self.main()
