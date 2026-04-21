""" Shell (CLI) Command Runner """

# Import required modules and libraries
from .base import BaseModule
from utils.secure_utils import run_user_command
from utils.colors import green, cyan
from utils.font_styles import success_message


class Shell(BaseModule):
    """Shell module for running arbitrary shell commands."""

    def __init__(self):
        self.name = "shell"
        self.full_name = "Shell"
        self.description = "Run a shell (CLI) command"
        self.options = "<prompt>: <command>"
        self.requires_target = False
        self.command = None

    def run(self, command=None):
        """Execute shell command."""
        if command is None:
            from utils.font_styles import error_message
            error_message("Command required")
            return

        self.command = command
        self._execute_core_logic()

    def main(self):
        """Interactive prompt mode."""
        self._show_module_header()
        self.command = self._get_input("Shell command to run")
        self._execute_core_logic()
        self._prompt_continue()

    def _execute_core_logic(self):
        """Execute the shell command."""
        success_message(f'Running shell command "{self.command}"')
        print()

        working_dir = "~"
        cmd = f"cd {working_dir} && {self.command}"

        try:
            run_user_command(cmd, use_shell=True, timeout=120, capture_output=False)
        except Exception as e:
            from utils.font_styles import error_message
            error_message(f"Command failed: {e}")

        print()
        return None
