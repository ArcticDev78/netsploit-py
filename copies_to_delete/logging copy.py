""" Logging Function in Modules
- During execution of the `run` command or the module itself, each module will
  create a log file, after which, through this (logging) utility, the user will be
  able to decide whether to keep the log file or not.
"""

# Import required modules and libraries

import os

from simple_colors import cyan, green

from utils.config import Config
from utils.font_styles import error_message, success_message


def log_prompt(module_fullname, log_filename):
    """Log Prompt function with:
    `module_fullname` providing the module's full name to be printed in the prompt,
    `log_filename` providing the path to the log file upon which the action will be performed
    """
    from utils.prompt import prompt

    # Check if logging is enabled (`config['logs']['enabled']` is True):
    # if config["logs"]["enabled"] is True:
    if Config.LOGS_ENABLED is True:
        # Ask the user whether they want to save the log file or not
        log_choice = input(
            f'[{green(">", "bold")}] {cyan(f"Do you want to save the {module_fullname} results to a log file? (y/n): ", "bold")}'
        ).lower()

        # If the users agrees, i.e. types "y":
        if log_choice in ("y", "yes"):
            print()
            # The log file is already created by the module's `run` command execution
            # Now, let the user know that the log file is "saved" along with the full path
            success_message(
                f"Saved results to log file: {config['logs']['folder_path']}{log_filename}"
            )
            print()

        # Else if the user disagrees, i.e. types "n":
        elif log_choice in ("n", "no"):
            try:
                # Delete the log file
                os.remove(log_filename)
                print()
                # Let the user know that the log file was not saved.
                # (The already existing log file was deleted by the above code)
                success_message("Did not save log file.")
                print()
                prompt()
            except OSError as e:
                # In case of any error, let the user know that the log file was not deleted
                # and display the error thrown
                error_message(f"Error: {log_filename} could not be deleted.\n{e}")
                prompt()

        else:
            # If the user types anything other than "y" or "n" in the prompt:
            print()
            error_message(
                'Invalid option entered. Enter either "y" for YES or "n" for NO.'
            )
            print()
            prompt()
            # Since the user provided an invalid option, the already created log file
            # will be deleted.
            try:
                # Delete the log file
                os.remove(log_filename)
                print()
                # Let the user know that the log file was not saved (it was deleted)
                success_message("Did not save log file.")
                print()
                prompt()
            except OSError as e:
                # In case of any error, let the user know that the log file was not deleted
                # and display the error thrown
                error_message(f"Error: {log_filename} could not be deleted.\n{e}")
                prompt()
    else:
        # Else if logging is disabled (`config["logs"]["enabled"] is False`), then do nothing (pass)
        pass
