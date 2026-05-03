"""STARTUP"""

# Import required libraries for startup messages
import platform
import socket

import netifaces  # type: ignore[import-untyped]
import psutil  # type: ignore[import-untyped]
from tabulate import tabulate

from utils.colors import blue, cyan, green, yellow
from utils.oui_updater import check_and_update_oui
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

    # 2a. Refresh the OUI database if it is stale (non-fatal on failure)
    check_and_update_oui()
    print(yellow(" => Powered by nmap, ping and hping3", "bold"))
    print(green(" => 9 modules ready to use", "bold"))
    print(blue(" => 5 Scanners, 3 Info and 1 Attack Module", "bold"))

    # 3. Set variables for printing network configuration table

    # 3.1 & 3.2 Get gateway and interface in a single netifaces call
    try:
        _gw_data = netifaces.gateways()
        _default_gw = _gw_data.get("default", {})
        if netifaces.AF_INET in _default_gw:
            network_gateway = _default_gw[netifaces.AF_INET][0]
            network_interface = _default_gw[netifaces.AF_INET][1]
        else:
            network_gateway = ""
            # Fallback: first non-loopback interface that is up
            network_interface = ""
            for iface, stats in psutil.net_if_stats().items():
                if (
                    stats.isup
                    and iface not in ("lo", "loopback")
                    and not iface.startswith("loop")
                ):
                    network_interface = iface
                    break
    except Exception:
        network_gateway = ""
        network_interface = ""

    # 3.3 Get wireless network name (SSID) — platform-specific, best-effort
    try:
        system = platform.system()
        if system == "Linux":
            cp = run_user_command(
                ["nmcli", "-t", "-f", "NAME", "connection", "show", "--active"],
                timeout=5,
                use_shell=False,
                capture_output=True,
            )
            stdout = (cp.stdout or "").strip()
            network_name = stdout.splitlines()[0] if stdout else ""
        elif system == "Darwin":
            try:
                # CoreWLAN is the modern API for Wi-Fi info on macOS (Monterey+).
                # Requires: pip install pyobjc-framework-CoreWLAN
                from CoreWLAN import CWWiFiClient  # type: ignore[import-untyped]

                client = CWWiFiClient.sharedWiFiClient()
                iface = client.interface()
                network_name = (iface.ssid() or "") if iface else ""
            except Exception:
                network_name = ""
        elif system == "Windows":
            cp = run_user_command(
                ["netsh", "wlan", "show", "interfaces"],
                timeout=5,
                use_shell=False,
                capture_output=True,
            )
            network_name = ""
            for line in (cp.stdout or "").splitlines():
                stripped = line.strip()
                if stripped.startswith("SSID") and "BSSID" not in stripped:
                    network_name = stripped.split(":", 1)[1].strip()
                    break
        else:
            network_name = ""
    except Exception:
        network_name = ""

    # 3.4 Get network MAC address — cross-platform via netifaces
    try:
        network_mac = ""
        if network_interface:
            addrs = netifaces.ifaddresses(network_interface)
            if netifaces.AF_LINK in addrs:
                network_mac = addrs[netifaces.AF_LINK][0].get("addr", "")
    except Exception:
        network_mac = ""

    # 3.5 Get IP address — cross-platform via netifaces with socket fallback
    try:
        network_ip = ""
        if network_interface:
            addrs = netifaces.ifaddresses(network_interface)
            if netifaces.AF_INET in addrs:
                network_ip = addrs[netifaces.AF_INET][0].get("addr", "")
        if not network_ip:
            # Fallback: connect outward to determine which local IP is in use
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(("8.8.8.8", 80))
                network_ip = s.getsockname()[0]
            finally:
                s.close()
    except Exception:
        network_ip = ""

    # 3.6 Get hostname — cross-platform via socket
    try:
        network_hostname = socket.gethostname()
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
