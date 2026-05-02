"""STARTUP"""

# Import required libraries for startup messages
from tabulate import tabulate

from utils.colors import blue, cyan, green, yellow
from utils.secure_utils import run_user_command

__version__ = "1.0.0"

# ASCII Art of "NetSploit for header"
HEADER = """
     __     _   __       _       _ _
  /\\ \\ \\___| |_/ _\\_ __ | | ___ (_) |_
 /  \\/ / _ \\ __\\ \\| '_ \\| |/ _ \\| | __|
/ /\\  /  __/ |__\\ \\ |_) | | (_) | | |_
\\_\\ \\/ \\___|\\__\\__/ .__/|_|\\___/|_|\\__|
                  |_|
"""


def startup():
    """Function to display ASCII art (header) of NetSploit, and network configuration table"""
    # 1. Print ASCII art of "NetSploit"
    print(blue(HEADER, "bold"))

    # 2. Print init messages (version, dependencies and extra info)
    print(yellow(f" => netsploit v{__version__}", "bold"))
    print(yellow(" => Powered by nmap, ping and hping3", "bold"))
    print(green(" => 9 modules ready to use", "bold"))
    print(blue(" => 5 Scanners, 3 Info and 1 Attack Module", "bold"))

    # 3. Set variables for printing network configuration table
    # 3.1 Get the network gateway IP (router)
    try:
        cp = run_user_command(
            "ip route show", timeout=5, use_shell=False, capture_output=True
        )
        stdout = cp.stdout or ""
        network_gateway = ""
        for line in stdout.splitlines():
            if line.startswith("default via"):
                parts = line.split()
                if len(parts) >= 3:
                    network_gateway = parts[2]
                    break
    except Exception:
        network_gateway = ""

    # 3.2 Get the current network interface being used
    try:
        cp = run_user_command(
            ["ip", "-o", "link"], timeout=5, use_shell=False, capture_output=True
        )
        stdout = cp.stdout or ""
        network_interface = ""
        # pick first non-loopback interface name
        for line in stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and not parts[1].startswith("lo"):
                network_interface = parts[1].rstrip(":")
                break
    except Exception:
        network_interface = ""

    # 3.3 Get wireless network name

    # Previously used method to get SSID; Works on Linux distros except for Fedora
    # network_name = os.popen('iwgetid -r').read()

    # Work-around method for Fedora Linux  to get SSID
    try:
        cp = run_user_command(
            ["nmcli", "-t", "-f", "NAME", "connection", "show", "--active"],
            timeout=5,
            use_shell=False,
            capture_output=True,
        )
        network_name = (cp.stdout or "").strip()
    except Exception:
        network_name = ""

    # 3.4 Get network MAC address
    try:
        cp = run_user_command(
            ["ip", "addr"], timeout=5, use_shell=False, capture_output=True
        )
        stdout = cp.stdout or ""
        network_mac = ""
        for line in stdout.splitlines():
            if "link/ether" in line:
                # extract mac
                parts = line.split()
                try:
                    idx = parts.index("link/ether")
                    network_mac = parts[idx + 1]
                    break
                except ValueError:
                    continue
    except Exception:
        network_mac = ""

    try:
        cp = run_user_command(
            ["hostname", "-I"], timeout=3, use_shell=False, capture_output=True
        )
        network_ip = (cp.stdout or "").strip()
    except Exception:
        network_ip = ""
    try:
        cp = run_user_command(
            ["hostname"], timeout=3, use_shell=False, capture_output=True
        )
        network_hostname = (cp.stdout or "").strip()
    except Exception:
        network_hostname = ""

    # 4. Print network configuration table
    print(
        """ \033[1;36m
    ╒══════════════════════════════════════════════════════════════════════════╕
    │                        Your Network Configuration                        │
    ╘══════════════════════════════════════════════════════════════════════════╛     \033[1;m"""
    )

    # 4.1 Setup the network configuration table
    table = [
        ["IP Address", "MAC Address", "Gateway", "Iface", "Hostname", "SSID"],
        [
            network_ip,
            network_mac.upper() if network_mac else "",
            network_gateway,
            network_interface,
            network_hostname,
            network_name,
        ],
    ]

    # 4.2 Print the network configuration table (using tabulate as table)
    print(tabulate(table, stralign="center", tablefmt="fancy_grid", headers="firstrow"))
    print()
    # 4.3 (OPTIONAL) Print extra guidance and tips
    print(green("[+] Please type help to view commands", "bold"))
    print()
    print(
        cyan("[TIP] You can use the ", "bold")
        + yellow("auto", "bold")
        + cyan(" command to automate your workflow!", "bold")
    )
    print()
