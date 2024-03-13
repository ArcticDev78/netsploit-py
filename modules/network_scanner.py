""" Network Scanner Module
- Module that uses nmap to scan and find devices connected to the network
"""

# Import required modules and libraries
import datetime
import os

from simple_colors import cyan, green, yellow

# from utils import (LOGS_FOLDER_PATH, error_message, exit_program, info_message,
#                    success_message)
from utils.config import LOGS_FOLDER_PATH
from utils.exit_program import exit_program
from utils.font_styles import error_message, info_message, success_message


# NetworkScanner Class
class NetworkScanner:
    """Network Scanner class that uses nmap to scan and find devices connected to the network"""

    def __init__(self):
        self.name = "network-scanner"
        self.description = "Find devices connected to the network"
        self.options = "(none)"

    def run(self):
        """Execute the Network Scanner module"""
        net = str(
            os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()
        )  # Get LAN IP address of this device running NetSploit
        net = net.replace("\n", "")  # Remove newline from `net`. eg: 192.168.0.2
        net2 = net[:-1]  # Remove last character from `net`. eg: 192.168.0.
        net3 = (
            net2 + "0"
        )  # Add zero (0) to the end of the `net2`. eg: 192.168.0.  # noqa
        net4 = net3 + "/24"  # Add /24 to the end of `net3`. eg: 192.168.0.0/24
        ip_range = net4
        # if IP_RANGE is False:  # If IP_RANGE is False, AKA, not set:
        #     error_message('Cannot start scan without IP_RANGE. Set the IP_RANGE using:', 'IP_RANGE => Your-IP-range-here')  # noqa
        #     self.run()  # Show the network scanner prompt
        info_message(
            f"Running network scan with IP range {ip_range}, this may take up to two minutes"
        )  # noqa
        info_message(
            "Running a network scan properly requires the command to be run using sudo"
        )  # noqa
        print()
        # For logging
        date = datetime.datetime.now()
        formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
        filename = f"network-scanner_log_{formatted_time}.txt"
        # Finally, run the scan
        os.system(
            f'sudo nmap -sn -T4 {ip_range} -oN "{LOGS_FOLDER_PATH}network-scanner/{filename}"'
        )  # noqa
        # os.system(f'sudo nmap -sn -T4 {IP_RANGE}')
        print()
        success_message("Finished scanning network")
        print()
        # Ask the user if they want to save the scan results to a log file.
        # print()
        choice = input(
            f'[{green(">", "bold")}] {cyan("Do you want to save the Network Scan results to a log file? (y/n): ", "bold")}'
        )  # noqa
        if choice == "y":  # If the user agrees, i.e. types "y":
            # pwd = os.popen('pwd').read()  # For printing to success message
            print()
            # Print a success message stating the log has been saved.
            success_message(
                f"Saved results to log file: {LOGS_FOLDER_PATH}network-scanner/{filename}"
            )  # noqa
            print()
        elif choice == "n":  # Else if the user disagrees, i.e. types "n":
            os.system(
                f'rm "{LOGS_FOLDER_PATH}network-scanner/{filename}" -f'
            )  # Delete the log file  # noqa
            print()
            success_message("Did not save log file.")
            print()
        else:
            # If the user types anything other than "y" or "n":
            print()
            error_message("Invalid option. Enter either y - YES or n - NO")
            print()
            os.system(
                f'rm "{LOGS_FOLDER_PATH}network-scanner/{filename}" -f'
            )  # Delete the log file  # noqa
            # self.run()
        # self.run()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import custom_prompt, prompt

        prompt_input = custom_prompt("network-scanner")
        # if prompt_input == 'show options':
        #     # if there is no set value for IP_RANGE, display as "(not set)"
        #     # or if there is an existing value, set the variable to the value
        # value = '(not set)' if db.get(
        #         'IP_RANGE') is False else db.get('IP_RANGE')
        # # Table for displaying options and other info
        # table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['IP_RANGE', value, 'no']]  # noqa
        # # Print the table (on to the console, of course)
        # print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        # self.run()

        # elif prompt_input == 'subnet':
        #     # net = ipaddress.ip_network('192.168.0.0/255.255.255.0', strict=False) or ipaddress.ip_network('10.0.0.0/255.255.255.0', strict=False)  # noqa
        #     # print(net)
        #     net = str(os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read())  # noqa
        #     net = net.replace("\n", "")
        #     net2 = net[:-1]
        #     net3 = net2 + "0"
        #     info_message(f'Subnet is "{net3}/24"')
        #     self.run()

        # elif prompt_input.startswith('IP_RANGE =>'):
        #     # split prompt_input from string to array
        #     optionArgs = prompt_input.split()
        #     # option is the second index (3rd string) in array
        #     option = optionArgs[2]
        #     # Set IP range to given option
        #     db.set('IP_RANGE', option)
        #     # Display success message like this: "IP_RANGE set to 192.168.0.1"
        #     info_message(f'IP_RANGE set to {db.get("IP_RANGE")}')
        #     self.run()

        if prompt_input == "run":
            # net = str(os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read())  # noqa // Get LAN ip address. eg:  192.168.0.2\n
            # net = net.replace("\n", "")  # Remove newline from `net`. eg: 192.168.0.2  # noqa
            # net2 = net[:-1]  # Remove last character from `net`. eg: 192.168.0.
            # net3 = net2 + "0"  # Add zero (0) to the end of the `net2`. eg: 192.168.0.  # noqa
            # net4 = net3 + "/24"  # Add /24 to the end of `net3`. eg: 192.168.0.0/24
            # IP_RANGE = net4
            # # if IP_RANGE is False:  # If IP_RANGE is False, AKA, not set:
            # #     error_message('Cannot start scan without IP_RANGE. Set the IP_RANGE using:', 'IP_RANGE => Your-IP-range-here')  # noqa
            # #     self.run()  # Show the network scanner prompt
            # info_message(f'Running network scan with IP range {IP_RANGE}, this may take up to two minutes')  # noqa
            # info_message('Running a network scan properly requires the command to be run using sudo')  # noqa
            # print()
            # # For logging
            # date = datetime.datetime.now()
            # formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            # filename = f'network-scanner_log_{formatted_time}.txt'
            # # Finally, run the scan
            # os.system(f'sudo nmap -sn -T4 {IP_RANGE} -oN "{LOGS_FOLDER_PATH}network-scanner/{filename}"')  # noqa
            # # os.system(f'sudo nmap -sn -T4 {IP_RANGE}')
            # print()
            # success_message('Finished scanning network')
            # print()
            # # Ask the user if they want to save the scan results to a log file.
            # # print()
            # choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            # if choice == 'y':  # If the users agrees, i.e. types "y":
            #     # pwd = os.popen('pwd').read()  # For printing to success message
            #     print()
            #     # Print a success message stating the log has been saved.
            #     success_message(f'Saved results to log file: {LOGS_FOLDER_PATH}network-scanner/{filename}')  # noqa
            #     print()
            # elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
            #     os.system(f'rm "{LOGS_FOLDER_PATH}network-scanner/{filename}" -f')  # Delete the log file  # noqa
            #     print()
            #     success_message('Did not save log file.')
            #     print()
            # else:
            #     # If the user types anything other than "y" or "n":
            #     print()
            #     error_message('Invalid option. Enter either y - YES or n - NO')
            #     print()
            #     os.system(f'rm "{LOGS_FOLDER_PATH}network-scanner/{filename}" -f')  # Delete the log file  # noqa
            #     self.run()
            # self.run()
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
            print(f'{cyan("Help for network-scanner:", ["bold", "underlined"])}')
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
            )  # noqa
            self.main()
