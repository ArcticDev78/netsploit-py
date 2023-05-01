# Import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path

# Network scanner function
def network_scanner():
    from functions.utils.prompt import prompt
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(network-scanner)", "bold")} {green(">")} ')  # noqa
    # if prompt_input == 'show options':
    #     # if there is no set value for IP_RANGE, display as "(not set)"
    #     # or if there is an existing value, set the variable to the value
    # value = '(not set)' if db.get(
    #         'IP_RANGE') is False else db.get('IP_RANGE')
    # # Table for displaying options and other info
    # table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['IP_RANGE', value, 'no']]  # noqa
    # # Print the table (on to the console, of course)
    # print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    # network_scanner()

    # elif prompt_input == 'subnet':
    #     # net = ipaddress.ip_network('192.168.0.0/255.255.255.0', strict=False) or ipaddress.ip_network('10.0.0.0/255.255.255.0', strict=False)  # noqa
    #     # print(net)
    #     net = str(os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read())  # noqa
    #     net = net.replace("\n", "")
    #     net2 = net[:-1]
    #     net3 = net2 + "0"
    #     info_message(f'Subnet is "{net3}/24"')
    #     network_scanner()

    # elif prompt_input.startswith('IP_RANGE =>'):
    #     # split prompt_input from string to array
    #     optionArgs = prompt_input.split()
    #     # option is the second index (3rd string) in array
    #     option = optionArgs[2]
    #     # Set IP range to given option
    #     db.set('IP_RANGE', option)
    #     # Display success message like this: "IP_RANGE set to 192.168.0.1"
    #     info_message(f'IP_RANGE set to {db.get("IP_RANGE")}')
    #     network_scanner()

    if prompt_input == 'run':
        net = str(os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read())  # noqa // Get LAN ip address. eg:  192.168.0.2\n
        net = net.replace("\n", "")  # Remove newline from `net`. eg: 192.168.0.2  # noqa
        net2 = net[:-1]  # Remove last character from `net`. eg: 192.168.0.
        net3 = net2 + "0"  # Add zero (0) to the end of the `net2`. eg: 192.168.0.  # noqa
        net4 = net3 + "/24"  # Add /24 to the end of `net3`. eg: 192.168.0.0/24
        IP_RANGE = net4
        # if IP_RANGE is False:  # If IP_RANGE is False, AKA, not set:
        #     error_message('Cannot start scan without IP_RANGE. Set the IP_RANGE using:', 'IP_RANGE => Your-IP-range-here')  # noqa
        #     network_scanner()  # Show the network scanner prompt
        info_message(f'Running network scan with IP range {IP_RANGE}, this may take up to two minutes')  # noqa
        info_message('Running a network scan properly requires the command to be run using sudo')  # noqa
        print()
        # For logging
        date = datetime.datetime.now()
        formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
        filename = f'network-scanner_log_{formatted_time}.txt'
        # Finally, run the scan
        os.system(f'sudo nmap -sn -T4 {IP_RANGE} -oN "{logs_folder_path}network-scanner/{filename}"')  # noqa
        # os.system(f'sudo nmap -sn -T4 {IP_RANGE}')
        print()
        success_message('Finished scanning network')
        print()
        # Ask the user if they want to save the scan results to a log file.
        # print()
        choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
        if choice == 'y':  # If the users agrees, i.e. types "y":
            # pwd = os.popen('pwd').read()  # For printing to success message
            print()
            # Print a success message stating the log has been saved.
            success_message(f'Saved results to log file: {logs_folder_path}network-scanner/{filename}')  # noqa
            print()
        elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
            os.system(f'rm "{logs_folder_path}network-scanner/{filename}" -f')  # Delete the log file  # noqa
            print()
            success_message('Did not save log file.')
            print()
        else:
            # If the user types anything other than "y" or "n":
            print()
            error_message('Invalid option. Enter either y - YES or n - NO')
            print()
            os.system(f'rm "{logs_folder_path}network-scanner/{filename}" -f')  # Delete the log file  # noqa
            network_scanner()
        network_scanner()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == '':
        network_scanner()

    elif prompt_input == 'clear':
        # Clear the terminal using `clear` shell command
        os.system('clear')
        network_scanner()

    elif prompt_input == 'help':
        # Help message
        print()
        print(f'{cyan("Help for network-scanner:", ["bold", "underlined"])}')
        print()
        print(f'To run a network scan, use {yellow("run", "bold")} command.')
        print()
        network_scanner()

    else:
        # If the user types a command that is not any of the above.

        # The invalid command is index 0 of array `prompt_input`
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        network_scanner()