""" Device Info Module
- Module to lookup/retrieve various information about the TARGET device
"""

# Import required modules and libraries
import datetime
import os

from simple_colors import cyan, green, yellow
from tabulate import tabulate

from utils.config import DB, LOGS_FOLDER_PATH
from utils.exit_program import exit_program
from utils.font_styles import error_message, info_message, success_message


class DeviceInfo:
    """DeviceInfo class with:
    __init__() method providing module metadata,
    run() method to be called in the Auto module, and
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "device-info"
        self.description = "Get info about the target device"
        self.options = "TARGET"

    def run(self, target=None):
        """
        `target` parameter is the IP address of the target device for which the scan will be run on
        """
        # If the value of `TARGET` is not set by the user:
        if target is False:
            # Print an error message
            error_message(
                "Cannot run scan(s) without TARGET being specified.\nPlease specify the TARGET and try again"
            )
        else:
            # Or, if the value of `TARGET` IS set:
            info_message(
                f"Running Device Info scan on {target}, this may take up to two minutes"
            )
            info_message(
                "Running a Device Info scan properly requires the command to be run using sudo"
            )
            print()
            # For logging:
            date = datetime.datetime.now()
            formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
            filename = f"device-info_log_{formatted_time}.txt"
            # Finally, run the Device Info scan on the target
            os.system(
                f'sudo nmap -v -A -T4 {target} -Pn -oN "{LOGS_FOLDER_PATH}/device-info/{filename}" -f'
            )
            # os.system(f'sudo nmap -v -A -T4 {TARGET} -Pn')
            print()
            # Print a success message
            success_message(f"Finished scanning {target}")
            # Ask the user if they want to save the scan results to a log file.
            print()
            choice = input(
                f'[{green(">", "bold")}] {cyan("Do you want to save the Device Info results to a log file? (y/n): ", "bold")}'
            )
            if choice == "y":  # If the user agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message
                print()
                # Print a success message stating the log has been saved.
                success_message(
                    f"Saved results to log file: {LOGS_FOLDER_PATH}/device-info/{filename}"
                )
                print()
            elif choice == "n":  # Else if the user disagrees, i.e. types "n":
                os.system(
                    f'rm "{LOGS_FOLDER_PATH}device-info/{filename}" -f'
                )  # Delete the log file
                print()
                success_message("Did not save log file.")
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message("Invalid option. Enter either y - YES or n - NO")
                print()
                os.system(
                    f'rm "{LOGS_FOLDER_PATH}device-info/{filename}" -f'
                )  # Delete the log file
                # self.run()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import custom_prompt, prompt

        prompt_input = custom_prompt("device-info")

        if prompt_input == "show options":
            # If the value is NOT set (default is False), set `value` to "(not set)".
            # If the value IS set, then `value` is set to the value from user input
            value = "(not set)" if DB.get("TARGET") is False else DB.get("TARGET")
            # Table for displaying options and other info
            table = [
                ["OPTIONS", "VALUE", "OPTIONAL?"],
                ["TARGET", value, "no"],
            ]
            # Print the options table
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
            self.main()

        elif prompt_input.startswith("target =>") or prompt_input.startswith(
            "set target"
        ):
            # Split `prompt_input` from string to array
            option_args = prompt_input.split()
            # `option` is the second index (3rd string) in array
            option = option_args[2]
            # Set IP range to given option
            DB.set("TARGET", option)
            # Display success message to confirm that the IP_RANGE was set.
            success_message(f'TARGET set to "{DB.get("TARGET")}"')
            self.main()

        elif prompt_input == "run":
            # If the command is "run":
            # Retrive TARGET value from database
            TARGET = DB.get("TARGET")
            # If the value of `TARGET` is not set by the user:
            if TARGET is False:
                # Print an error message
                error_message(
                    "Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again"
                )
                self.main()
            else:
                # Or, if the value of `TARGET` is set:

                self.run(TARGET)
            self.main()

        elif prompt_input == "exit":
            # Exit the program
            exit_program()

        elif prompt_input == "back":
            # Go back to initial prompt
            prompt()

        elif prompt_input == "":
            # If user didn't enter anything and pressed enter, show DeviceInfo prompt again
            self.main()

        elif prompt_input == "help":
            # Help message
            print()
            print(f'{cyan(f"Help for {self.name}:", ["bold", "underlined"])}')
            print()
            print(
                f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}'
            )
            print(
                f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)'
            )
            print(f'2. Run your scan using {yellow("run", "bold")}')
            print()
            self.main()

        elif prompt_input == "clear":
            # Clear the terminal using the shell command `clear`
            os.system("clear")
            self.main()

        else:
            # If the user types a command that is not any of the above.
            # The invalid command is index 0 of array `prompt_input`
            invalid_command = prompt_input.split()[0]
            error_message(
                f'Invalid command "{invalid_command}". Please enter a valid command'
            )
            self.main()
