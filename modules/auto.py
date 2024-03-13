""" Netsploit Automation Assistant """

# Import required modules and libraries
# import os

from modules.custom import custom
from modules.device_info import DeviceInfo
from modules.dos import DoS
from modules.network_scanner import NetworkScanner
from modules.os_guesser import OSGuesser
# from modules.oui_lookup import OuiLookup
from modules.ping import Ping
from modules.port_scanner import PortScanner
# from modules.shell import Shell
from modules.vuln_scanner import VulnerabilityScanner
from simple_colors import cyan, green, yellow
# from utils.config import DB, LOGS_FOLDER_PATH
from utils.font_styles import error_message, info_message, success_message

# import time


# from modules import DeviceInfo, DoS, NetworkScanner


class Auto:
    """Auto class with:
    __init__() method providing module metadata,
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "auto"
        self.description = "Automation of NetSploit modules on a target device"
        self.options = "TARGET"

    def main(self):
        """Auto function to automate the usage of NetSploit"""
        from utils.prompt import prompt

        print()
        success_message("NetSploit is now running in auto mode")
        # 1) Scan network for devices on which the module of choice can be executed
        NetworkScanner().run()
        # 2) Prompt the user for the device on which a module of choice is to be executed
        target_device = input(
            f'[{green(">", "bold")}] {cyan("Enter target device IP: ", "bold")}'
        )
        # If the target device was selected by the user, then continue module execution
        if target_device:
            print()
            # 3) List the available modules
            print(f'{yellow("Available scans/attacks:", ["underlined", "bold"])}\n\n')
            print(
                "  1 - Device Info\n  2 - OS Guesser\n  3 - Port Scanner\n  4 - DoS Attack\n  5 - Ping\n  6 - Vulnerability Scan\n  7 - Custom nmap command"
            )

            print()

            # 4) Prompt the user for the module of choice to be executed against the target device
            choice = str(
                input(
                    f'[{green(">", "bold")}] {cyan("Enter scan/attack to run on", "bold")} {yellow(target_device, "bold")}: '
                )
            )

            # 5) Execute the module of choice:

            if choice == "1":
                print()
                info_message(f'Selected {green("device-info", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                         Device Info                             │
        │                                                                 │
        │      Use a series of scans to gather information about          │
        │                      the target device                          │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(f'Running device scan on {target_device}, this may take up to two minutes')
                # info_message('Running a device scan properly requires the command to be run using sudo')
                # print()
                # os.system(f'sudo nmap -v -A -T4 {target_device} -Pn')
                # print()
                # success_message(f'Finished scanning {target_device}')
                # print()
                DeviceInfo().run(target_device)
                info_message("Exited auto mode")
                print()
                prompt()

            elif choice == "2":
                print()
                info_message(f'Selected {green("os-guesser", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                          OS Guesser                             │
        │                                                                 │
        │      Use a series of scans to gather information such as        │
        │      the operating system the target is running, the version    │
        │                of the operating system, etc.                    │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(
                #     f"Running OS Guesser scan on {target_device}, this may take up to two minutes"
                # )
                # info_message(
                #     "Running a OS Guesser scan properly requires the command to be run using sudo"
                # )
                # print()
                # os.system(f"sudo nmap -T4 -O --osscan-guess {target_device} -Pn")
                # print()
                # success_message(f"Finished scanning {target_device}")
                # print()
                OSGuesser().run(target_device)
                info_message("Exited auto mode")
                print()
                prompt()

            elif choice == "3":
                print()
                info_message(f'Selected {green("port-scanner", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                          Port Scanner                           │
        │                                                                 │
        │             Scan the target device for open ports               │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(
                #     f"Running port scan on {target_device}, this may take up to two minutes"
                # )
                # print()
                # os.system(f"nmap -T4 -sV {target_device} -Pn")
                # print()
                # success_message(f"Finished scanning {target_device}")
                # print()
                PortScanner().run(target_device)
                info_message("Exited auto mode")
                print()
                prompt()

            elif choice == "4":
                print()
                info_message(f'Selected {green("dos", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                           DoS Attack                            │
        │     Send a succession of SYN requests to the target system      │
        │     to make the system unresponsive to legitimate traffic       │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(
                #     f"Running DoS attack on {target_device}, this may take up to two minutes"
                # )
                # info_message(
                #     "Running a DoS attack properly requires the command to be run using sudo"
                # )
                # print()
                # os.system(
                #     f"sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {target_device}"
                # )
                # print()
                # success_message(f"Finished attacking {target_device}")
                # print()
                DoS().run(target_device)
                info_message("Exited auto mode")
                print()
                prompt()

            elif choice == "5":
                print()
                info_message(f'Selected {green("ping", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                              Ping                               │
        │                                                                 │
        │                Check the accessibility of devices               │
        │      and show how long it takes for packets to reach host       │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(f"Pinging {target_device} (5 times)...\n")
                # os.system(f"ping -c 5 {target_device}")
                # print()
                # success_message(f"Finished pinging {target_device}\n")
                # print()
                Ping().main()
                info_message("Exited auto mode.")
                print()
                prompt()

            elif choice == "6":
                print()
                info_message(f'Selected {green("vuln-scannner", "bold")} module')
                print(
                    """ \033[1;36m
        ╒═════════════════════════════════════════════════════════════════╕
        │                                                                 │
        │                      Vulnerability Scanner                      │
        │                                                                 │
        │          Scan the target for potential vulnerabilities          │
        │                     that can be exploited                       │
        ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                )
                print()
                # info_message(
                #     f"Running Vulnerability scan on {target_device}, this may take up to two minutes"
                # )
                # print()
                # os.system(f"nmap --script nmap-vulners/ -sV -T4 {target_device}")
                # print()
                # success_message(f"Finished scanning {target_device}")
                # print()
                VulnerabilityScanner().run(target_device)
                info_message("Exited auto mode.")
                print()
                prompt()

            elif choice == "7":
                print()
                info_message(f'Selected {green("custom", "bold")} module')
                print()
                # custom_nmap_cmd = input(
                #     f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}'
                # )
                # if custom_nmap_cmd.startswith("nmap"):
                #     print()
                #     success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
                #     print()
                #     os.system(custom_nmap_cmd)
                #     print()
                #     info_message("Exited auto mode.")
                #     print()
                #     prompt()
                # else:
                #     print()
                #     error_message(
                #         f'Your command must be an nmap command!\n \
                #         To run any other shell command, use the {yellow("shell", "bold")} module.'
                #     )
                #     print()
                custom()
                info_message("Exited auto mode.")
                print()
                prompt()
            else:
                error_message("Error: you did not provide a valid scan / attack.")

        else:
            error_message("Error: you did not provide a target device IP.")
            prompt()
