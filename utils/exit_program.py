"""Exit Program Function

This util allows the user to exit the NetSploit program.
It displays a farewell message and ensures proper program termination.
"""

import sys

from .font_styles import success_message


def exit_program():
    """
    Gracefully exit the NetSploit program.

    This function prints a farewell message using the success_message style
    and then terminates the program using sys.exit().

    Returns:
        None

    Note:
        This function does not return as it terminates the program.
    """
    farewell_message = "Shutting down NetSploit..."
    success_message(farewell_message)
    sys.exit(0)


if __name__ == "__main__":
    # This allows for testing the exit function directly if needed
    exit_program()
