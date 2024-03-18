""" STARTUP """

# Import required libraries for startup messages
import os

from simple_colors import blue, green, yellow
from tabulate import tabulate

from .config import HEADER


def startup():
    """Function to display ASCII art (header) of NetSploit, and network configuration table"""
    # 1. Print ASCII art of "NetSploit"
    print(blue(HEADER, "bold"))

    # 2. Print init messages
    print(yellow(" => netsploit v0.8", "bold"))
    print(yellow(" => Powered by nmap, ping and hping3", "bold"))
    print(green(" => 9 modules ready to use", "bold"))
    print(blue(" => 5 Scanners, 3 Info, 1 Attack", "bold"))

    # 3. Set variables for printing network configuration table
    # Get the network gateway IP (router)
    n_gateway = (
        os.popen("ip route show | grep -i 'default via'| awk '{print $3 }'")
        .read()
        .replace("\n", "")
    )
    # gateway = gateway.replace("\n", "")

    # Get the current network interface being used
    n_interface = (
        os.popen("route | awk '/Iface/{getline; print $8}'").read().replace("\n", "")
    )
    # up_interface = up_interface.replace("\n", "")

    # Get wireless network name (Previously used; Works on Linux distros except for Fedora)
    # n_name = os.popen('iwgetid -r').read()

    # Get wireless network name (Work-around for Fedora Linux)
    # n_name = os.popen("nmcli -t -f NAME connection show --active").read()

    # Get network MAC address
    n_mac = os.popen(
        "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'"
    ).read()  # noqa
    n_ip = os.popen("hostname -I").read()  # Local IP address
    n_host = os.popen("hostname").read()  # hostname

    # 4. Print network configuration table
    print(
        """ \033[1;36m                                                                                                                                       
    ╒══════════════════════════════════════════════════════════════════════════╕
    │                        Your Network Configuration                        │
    ╘══════════════════════════════════════════════════════════════════════════╛     \033[1;m"""
    )  # noqa

    # Print network configuration, using tabulate as table.
    table = [
        ["IP Address", "MAC Address", "Gateway", "Iface", "Hostname"],
        ["", "", "", "", ""],
        [n_ip, n_mac.upper(), n_gateway, n_interface, n_host],
    ]
    print(tabulate(table, stralign="center", tablefmt="fancy_grid", headers="firstrow"))
    print()
    print(f'{green("[+] Please type help to view commands", "bold")}')
    # print()
    # print(f'{cyan("[TIP]", "bold")} You can use the {yellow("auto", "bold")} command to automate your process!')
    print()
