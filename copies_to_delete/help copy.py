""" Help Messages (In-Prompt & In-Module) """

# Import required libraries
from simple_colors import blue, cyan, green, yellow
from tabulate import tabulate


class Help:
    """Help class with:
    prompt_msg() method to be called in `prompt.py`, and
    module_help() method which is the whole module with all its functions"""

    def prompt_help_msg(self):
        """Display the help message (prompt-level)"""
        print(f'{cyan("Commands", ["bold", "underlined"])}:')
        # Initialise the data to be tabulated
        help_table = [
            [
                f'{blue("Command", "underlined")}',
                f'{blue("Description", "underlined")}',
            ],
            [
                f'{yellow("help", "bold")}',
                f'{green("Print this help message", "italic")}',
            ],
            [
                f'{yellow("use", "bold")} <module>',
                f'{green("Select a module to use", "italic")}',
            ],
            [
                f'{yellow("modules", "bold")}',
                f'{green("Show available modules to use", "italic")}',
            ],
            [f'{yellow("shell", "bold")}', f'{green("Run a shell command", "italic")}'],
            [
                f'{yellow("clear", "bold")}',
                f'{green("Clear the [terminal] screen", "italic")}',
            ],
            [f'{yellow("exit", "bold")}', f'{green("Exit the program", "italic")}'],
        ]
        # Print the Help table
        print(
            tabulate(
                help_table, stralign="center", tablefmt="fancy_grid", headers="firstrow"
            )
        )

        print()
