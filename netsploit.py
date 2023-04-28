""" IMPORT MODULES AND LIBRARIES """

from functions.utils.prompt import prompt

# Import required libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import sys
from tabulate import tabulate
import pickledb
# import ipaddress
import time
import datetime


""" PICKLEDB SETUP """
# db = pickledb.load('netsploit.db', False)

""" CONFIG """
# NOTE: Change the paths to to absolute paths if needed
# UPDATE: using `functions/utils/config.py` for storing configs

# username = os.popen('whoami').read()
# username = username.replace("\n", "")

# oui_file_path = f'/home/{username}/path/to/netsploit-py/oui.txt'  # noqa
# oui_file_path = 'oui.txt'

# logs_folder_path = f'/home/{username}/path/to/netsploit-py/logs/'  # noqa
# logs_folder_path = 'logs/'

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


try:
    prompt()
except KeyboardInterrupt:
    print()
    exit()
