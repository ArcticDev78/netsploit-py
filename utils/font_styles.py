"""
Font Styles Utility

This module provides functions for styled console output:
- error_message: for displaying error messages
- success_message: for displaying success messages
- info_message: for displaying informational messages

These functions can be used across other modules for consistent formatting.
"""

from utils.colors import green, red, yellow


def error_message(error_msg: str, solution: str = "") -> None:
    """
    Display an error message with an optional solution.

    Args:
        error_msg (str): The error message to display.
        solution (str, optional): A potential solution to the error. Defaults to "".
    """
    prefix = red("!", "bold")
    if solution:
        solution_text = green(solution, "bold")
        print(f'[{prefix}] {error_msg} {solution_text}')
    else:
        print(f'[{prefix}] {error_msg}')


def success_message(success_msg: str) -> None:
    """
    Display a success message.

    Args:
        success_msg (str): The success message to display.
    """
    prefix = green("+", "bold")
    print(f'[{prefix}] {success_msg}')


def info_message(info_msg: str, italics: bool = False) -> None:
    """
    Display an informational message, optionally in italics.

    Args:
        info_msg (str): The informational message to display.
        italics (bool, optional): Whether to display the message in italics. Defaults to False.
    """
    prefix = yellow("*", "bold")
    if italics:
        print(f'[{prefix}] \x1B[3m{info_msg}\x1B[0m')
    else:
        print(f'[{prefix}] {info_msg}')
