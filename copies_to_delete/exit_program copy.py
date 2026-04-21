""" Exit (Program) Function """

# Import required libraries
import sys

from .font_styles import success_message


def exit_program():
    """Message to be printed when using exit command or Ctrl-C inputted"""
    sys.exit(success_message("Shutting down NetSploit ... Bye! ( ^_^)/"))
