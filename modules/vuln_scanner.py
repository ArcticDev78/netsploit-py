""" Vulnerability Scanner Module                                                    
- Scan the target for potential vulnerabilities that can be exploited
"""

# Import required modules and libraries
import datetime
import os

from simple_colors import blue, cyan, green, yellow
from tabulate import tabulate

from utils.config import DB, LOGS_FOLDER_PATH
from utils.exit_program import exit_program
from utils.font_styles import error_message, info_message, success_message


class VulnerabilityScanner:
    """OS Guesser class with:
    __init__() method providing module metadata,
    run() method to be called in the Auto module, and
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "os-guesser"
        self.description = "Guess the operating system running on a device"
        self.options = "TARGET"

    def run(self, target_param=None):
        """
        `target` parameter is the IP address of the target device for which the scan will be run on
        """

        if target_param is False:
            error_message(
                "Cannot run Vulnerability Scanner without TARGET being specified. Please specify the TARGET and try again"
            )
            # self.main()
        else:
            info_message(
                f"Running Vulnerability scan on {target_param}, this may take up to two minutes"
            )
            # For logging
            date = datetime.datetime.now()
            formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
            filename = f"vuln-scanner_log_{formatted_time}.txt"
            print()
            # os.system(f'nmap --script nmap-vulners/ -sV {TARGET}')
            os.system(
                f'nmap --script nmap-vulners/ -sV {target_param} -oN "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -Pn'
            )
            print()
            # Ask the user if they want to save the scan results to a log file.
            # print()
            choice = input(
                f'[{green(">", "bold")}] {cyan("Do you want to save the Vulnerability Scanner results to a log file? (y/n): ", "bold")}'
            )
            if choice == "y":  # If the user agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message
                print()
                # Print a success message stating the log has been saved.
                success_message(
                    f"Saved results to log file: {LOGS_FOLDER_PATH}vuln-scanner/{filename}"
                )
                print()
            elif choice == "n":  # Else if the user disagrees, i.e. types "n":
                os.system(
                    f'rm "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -f'
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
                    f'rm "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -f'
                )  # Delete the log file
                # self.main()
            success_message(f"Finished scanning {target_param}")
            print()
            # self.main()
        # self.main()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import prompt

        prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(vuln-scanner)", "bold")} {green(">")} '
        )
        prompt_input = prompt_input.lower()

        if prompt_input == "show options":
            value = "(not set)" if DB.get("TARGET") is False else DB.get("TARGET")
            # Table for displaying options and other info
            table = [["OPTIONS", "VALUE", "OPTIONAL?"], ["TARGET", value, "no"]]
            # Print the table (on to the console, of course)
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
            self.main()

        elif prompt_input.startswith("target =>") or prompt_input.startswith(
            "set target"
        ):
            # split prompt_input from string to array
            option_args = prompt_input.split()
            # option is the second index (3rd string) in array
            option = option_args[2]
            # Set IP range to given option
            DB.set("TARGET", option)
            # Display success message like this: "IP_RANGE set to 192.168.0.1"
            success_message(f'TARGET set to "{DB.get("TARGET")}"')
            self.main()

        elif prompt_input == "run":
            TARGET = DB.get("TARGET")
            if TARGET is False:
                error_message(
                    "Cannot run Vulnerability Scanner without TARGET being specified. Please specify the TARGET and try again"
                )
                self.main()
            else:
                #     info_message(
                #         f"Running Vulnerability scan on {TARGET}, this may take up to two minutes"
                #     )
                #     # For logging
                #     date = datetime.datetime.now()
                #     formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
                #     filename = f"vuln-scanner_log_{formatted_time}.txt"
                #     print()
                #     # os.system(f'nmap --script nmap-vulners/ -sV {TARGET}')
                #     os.system(
                #         f'nmap --script nmap-vulners/ -sV {TARGET} -oN "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -Pn'
                #     )
                #     print()
                #     # Ask the user if they want to save the scan results to a log file.
                #     # print()
                #     choice = input(
                #         f'[{green(">", "bold")}] {cyan("Do you want to save the Vulnerability Scanner results to a log file? (y/n): ", "bold")}'
                #     )
                #     if choice == "y":  # If the users agrees, i.e. types "y":
                #         # pwd = os.popen('pwd').read()  # For printing to success message
                #         print()
                #         # Print a success message stating the log has been saved.
                #         success_message(
                #             f"Saved results to log file: {LOGS_FOLDER_PATH}vuln-scanner/{filename}"
                #         )
                #         print()
                #     elif choice == "n":  # Else if the user disagrees, i.e. types "n":
                #         os.system(
                #             f'rm "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -f'
                #         )  # Delete the log file
                #         print()
                #         success_message("Did not save log file.")
                #         print()
                #     else:
                #         # If the user types anything other than "y" or "n":
                #         print()
                #         error_message("Invalid option. Enter either y - YES or n - NO")
                #         print()
                #         os.system(
                #             f'rm "{LOGS_FOLDER_PATH}vuln-scanner/{filename}" -f'
                #         )  # Delete the log file
                #         self.main()
                #     success_message(f"Finished scanning {TARGET}")
                #     print()
                #     self.main()
                # self.main()
                self.run(TARGET)
                self.main()

        elif prompt_input == "exit":
            exit_program()

        elif prompt_input == "back":
            prompt()

        elif prompt_input == "":
            self.main()

        elif prompt_input == "help":
            print()
            print(f'{cyan("Help for vuln-scanner:", ["bold", "underlined"])}')
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
            os.system("clear")
            self.main()

        else:
            invalid_command = prompt_input.split()[0]
            error_message(
                f'Invalid command "{invalid_command}". Please enter a valid command'
            )
            self.main()
