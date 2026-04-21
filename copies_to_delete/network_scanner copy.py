""" Network Scanner Module
- Module that uses nmap to scan and find devices connected to the network
"""

# Import required modules and libraries
import datetime
import os

from simple_colors import cyan, green, yellow

# from utils.config import LOGS_ENABLED, LOGS_FOLDER_PATH
from utils.config import Config
from utils.exit_program import exit_program
from utils.font_styles import error_message, info_message, success_message
from utils.logging import log_prompt


class NetworkScanner:
    """Network Scanner class that uses nmap to scan and find devices connected to the network"""

    def __init__(self):
        self.name = "network-scanner"
        self.full_name = "Network Scanner"
        self.description = "Find devices connected to the network"
        self.options = "(none)"

    def run(self):
        """Execute the Network Scanner module"""
        # Get LAN IP address of the user's device running NetSploit
        net = str(
            os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()
        )
        # Get the IP address range of the local network
        ip_range = net.replace("\n", "")[:-1] + "0" + "/24"
        info_message(
            f"Running {green("Network Scan", "bold")} with IP range {cyan(ip_range, "bold")}, this may take up to two minutes", False
        )
        info_message(
            "Running a Network Scan properly requires the command to be run using sudo",
            True,
        )
        print()
        # For logging
        date = datetime.datetime.now()
        formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
        filename = f"{Config.LOGS_FOLDER_PATH}{self.name}_log_{formatted_time}.txt"
        # Finally, run the scan
        os.system(f'sudo nmap -sn -T4 {ip_range} -oN "{filename}"')
        # os.system(f'sudo nmap -sn -T4 {IP_RANGE}')
        print()
        success_message("Finished scanning network")
        print()
        # Ask the user if they want to save the scan results to a log file.

        log_prompt(self.full_name, filename)

        # print()
        # choice = input(
        #     f'[{green(">", "bold")}] {cyan("Do you want to save the Network Scan results to a log file? (y/n): ", "bold")}'
        # )
        # if choice == "y":  # If the user agrees, i.e. types "y":
        #     print()
        #     success_message(
        #         f"Saved results to log file: {LOGS_FOLDER_PATH}{self.name}/{filename}"
        #     )
        #     print()
        # elif choice == "n":  # Else if the user disagrees, i.e. types "n":
        #     os.system(
        #         f'rm "{LOGS_FOLDER_PATH}{self.name}/{filename}" -f'
        #     )  # Delete the log file
        #     print()
        #     success_message("Did not save log file.")
        #     print()
        # else:
        #     # If the user types anything other than "y" or "n":
        #     print()
        #     error_message("Invalid option. Enter either y - YES or n - NO")
        #     print()
        #     os.system(
        #         f'rm "{LOGS_FOLDER_PATH}{self.name}/{filename}" -f'
        #     )  # Delete the log file

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import custom_prompt, prompt

        prompt_input = custom_prompt(self.name)

        if prompt_input == "run":
            self.run()
            self.main()

        elif prompt_input == "back":
            prompt()

        elif prompt_input == "exit":
            exit_program()

        elif prompt_input == "":
            self.main()

        elif prompt_input == "clear":
            # Clear the terminal using `clear` shell command
            os.system("clear")
            self.main()

        elif prompt_input == "help":
            # Help message
            print()
            print(f'{cyan(f"Help for {self.name}:", ["bold", "underlined"])}')
            print()
            print(f'To run a network scan, use {yellow("run", "bold")} command.')
            print()
            self.main()

        else:
            # If the user types a command that is not any of the above.

            # The invalid command is index 0 of array `prompt_input`
            invalid_command = prompt_input.split()[0]
            error_message(
                f'Invalid command "{invalid_command}". Please enter a valid command'
            )
            self.main()
