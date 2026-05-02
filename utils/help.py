"""Help Messages Module

This module provides functionality to display help messages for the NetSploit program,
both at the prompt level and within modules.

Classes:
    Help: Contains methods for displaying help messages.
"""

from tabulate import tabulate

# Use safe color wrappers from utils.colors to avoid hard dependency on simple-colors
from utils.colors import blue as color_blue
from utils.colors import cyan as color_cyan
from utils.colors import green as color_green
from utils.colors import yellow as color_yellow


class Help:
    """
    Help class for displaying formatted help messages.

    Methods:
        prompt_help_msg: Display the help message at the prompt level.
    """

    @staticmethod
    def prompt_help_msg() -> None:
        """
        Display the help message for the main prompt level.

        This method prints a formatted table of available commands and their descriptions.
        """
        print(f"{color_cyan('Commands', ['bold', 'underlined'])}:")

        help_table: list[tuple[str, str]] = [
            (
                color_blue("Command", "underlined"),
                color_blue("Description", "underlined"),
            ),
            (
                color_yellow("help", "bold"),
                color_green("Print this help message", "italic"),
            ),
            (
                f"{color_yellow('use', 'bold')} <module>",
                color_green("Select a module to use", "italic"),
            ),
            (
                color_yellow("auto", "bold"),
                color_green("Automate modules on a target device", "italic"),
            ),
            (
                color_yellow("modules", "bold"),
                color_green("Show available modules to use", "italic"),
            ),
            (
                color_yellow("shell", "bold"),
                color_green("Run a shell command", "italic"),
            ),
            (
                color_yellow("clear", "bold"),
                color_green("Clear the [terminal] screen", "italic"),
            ),
            (color_yellow("exit", "bold"), color_green("Exit the program", "italic")),
        ]

        print(
            tabulate(
                help_table, stralign="center", tablefmt="fancy_grid", headers="firstrow"
            )
        )
        print()


if __name__ == "__main__":
    # This allows for testing the help message display directly if needed
    Help.prompt_help_msg()
