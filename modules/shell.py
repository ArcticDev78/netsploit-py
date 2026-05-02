"""Shell (CLI) Command Runner"""

# Import required modules and libraries
import subprocess
from pathlib import Path

from utils.font_styles import error_message, success_message

from .base import BaseModule


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
        """Execute the shell command in the user's home directory.

        Uses subprocess.run with cwd=Path.home() for cross-platform home
        directory resolution instead of 'cd ~' which is Unix-specific.
        """
        success_message(f'Running shell command "{self.command}"')
        print()

        try:
            subprocess.run(
                self.command or "",
                shell=True,
                cwd=Path.home(),
            )
        except Exception as e:
            error_message(f"Command failed: {e}")

        print()
        return None
