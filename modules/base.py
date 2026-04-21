"""
Base Module Class

Provides a standardized base class for all Netsploit modules.
Subclasses should implement at least `run()` / `main()` and `_execute_core_logic()`.
This file centralizes prompt helpers, input validation helpers and logging handling.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

# Prefer the project's color helpers if available
try:
    from simple_colors import blue, cyan, green, yellow  # type: ignore
except Exception:  # pragma: no cover - fallback when simple_colors not installed
    blue = cyan = green = yellow = lambda text, *args, **kwargs: text

from utils.font_styles import error_message
from utils.logging import LogManager


class BaseModule(ABC):
    """Abstract base class for all Netsploit modules.

    Attributes common to modules:
      - name: internal (hyphenated) module name
      - full_name: human readable name
      - description: short description
      - options: description of options
      - requires_target: whether module requires a target
      - target: current target value (if applicable)
    """

    def __init__(self) -> None:
        self.name: str = "base"
        self.full_name: str = "Base Module"
        self.description: str = "Base module"
        self.options: str = "(none)"
        self.requires_target: bool = False
        self.target: Optional[str] = None

    @abstractmethod
    def run(self, *args, **kwargs) -> None:
        """Entry point used by the Auto mode or programmatic callers.

        Implementations should validate inputs, call the core logic and then
        invoke `_handle_results()` with the returned log path (if any).
        """
        raise NotImplementedError

    @abstractmethod
    def main(self) -> None:
        """Interactive prompt entry point.

        Should display headers, prompt for input using `_get_input()` and then
        run the module logic.
        """
        raise NotImplementedError

    def _show_module_header(self) -> None:
        """Print a simple, consistent module header."""
        print()
        print(f"{yellow('netsploit', 'underlined')} => {blue(f'({self.name})', 'bold')}\n")

    def _validate_target(self, target: Optional[str] = None) -> bool:
        """Default target validation: ensure the target is provided when required.

        Override this method in subclasses to add IP/hostname validation.
        """
        target_to_validate = target or self.target
        if self.requires_target and target_to_validate is None:
            error_message(f"Target is required for {self.full_name}")
            return False
        return True

    def _validate_input(self) -> bool:
        """General input validation hook. Subclasses may override.

        Default implementation only checks `_validate_target()`.
        """
        return self._validate_target()

    @abstractmethod
    def _execute_core_logic(self) -> Optional[Path]:
        """Execute the module's primary work.

        Return:
            Path to the log file created (if any), or None.
        """
        raise NotImplementedError

    def _handle_results(self, log_path: Optional[Path]) -> None:
        """Handle results after `_execute_core_logic()` finishes.

        By default this delegates to LogManager.handle_log_prompt which respects
        the project's logging configuration.
        """
        if log_path:
            try:
                LogManager.handle_log_prompt(self.full_name, log_path)
            except Exception as e:  # don't let prompt-related issues crash the module
                error_message(f"Error handling log file: {e}")

    def _prompt_continue(self) -> None:
        """Return to the main prompt in a safe way."""
        try:
            from utils.prompt import prompt

            prompt()
        except Exception as e:
            from utils.font_styles import error_message
            error_message(f"Warning: Failed to return to main prompt: {e}")
            return

    def _get_bool_input(self, prompt_text: str) -> bool:
        """Ask user a yes/no question and return True for 'y', False for 'n'."""
        response = input(f"[{green('>', 'bold')}] {cyan(prompt_text, 'bold')} [y/n]: ").lower().strip()
        if response == 'y':
            return True
        if response == 'n':
            return False
        error_message(f'Invalid option "{response}". Please enter y or n.')
        return self._get_bool_input(prompt_text)

    def _get_input(self, prompt_text: str, required: bool = True) -> str:
        """Prompt the user for input, optionally re-prompting until non-empty.

        Returns the entered string (may be empty if not required).
        """
        while True:
            user_input = input(f"[{green('>', 'bold')}] {cyan(prompt_text, 'bold')}: ").strip()
            if required and not user_input:
                error_message('Input is required. Please try again.')
                continue
            return user_input
