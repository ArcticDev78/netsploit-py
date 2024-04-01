""" Main Prompt  """

# Import required libraries and modules
import os

from simple_colors import blue, cyan, green, yellow
from tabulate import tabulate

from modules.auto import Auto
from modules.custom import custom
from modules.device_info import DeviceInfo
from modules.dos import DoS
from modules.network_scanner import NetworkScanner
from modules.os_guesser import OSGuesser
from modules.oui_lookup import OuiLookup
from modules.ping import Ping
from modules.port_scanner import PortScanner
from modules.shell import Shell
from modules.vuln_scanner import VulnerabilityScanner

from .exit_program import exit_program
from .font_styles import error_message, info_message
from .help import Help


def prompt():
    """Function to handle the prompts in which the user can enter other modules"""
    try:
        # The main (base) prompt of NetSploit:
        prompt_input = input(yellow("netsploit", "underlined") + " " + green(">") + " ")

        # Variables to handle the `prompt_input`
        args = prompt_input.split()  # Split `args` into an array
        args_length = len(args)  # Variable to store length of the array
        command = args[
            0
        ]  # args[0] is the top-level prompt command (eg: help, modules, etc.)

        # If nothing was entered (empty string was returned), run prompt again
        if args_length == 0:
            # error_message('Please enter a valid command.')
            prompt()
        # Otherwise, if the user indeed entered an input:
        else:
            if command == "use":
                try:
                    if args[1] == "network-scanner":
                        print()
                        info_message(
                            f'Selected {green("network-scanner", "bold")} module.'
                        )
                        print(
                            """ \033[1;36m
    ╒═════════════════════════════════════════════════════════════════╕
    │                                                                 │
    │                         Network Scanner                         │
    │                                                                 │
    │      Find devices connected to the network and retrieve         │
    │                basic information about them                     │
    ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                        )
                        print()
                        NetworkScanner().main()

                    elif args[1] == "device-info":
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
                        DeviceInfo().main()

                    elif args[1] == "os-guesser":
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
                        OSGuesser().main()

                    elif args[1] == "oui-lookup":
                        print()
                        info_message(f'Selected {green("oui-lookup", "bold")} module')
                        print(
                            """ \033[1;36m
    ╒═════════════════════════════════════════════════════════════════╕
    │                                                                 │
    │                          OUI Lookup                             │
    │                                                                 │
    │      Find the manufacturer of the target device using its       │
    │                          MAC Address.                           │
    ╘═════════════════════════════════════════════════════════════════╛     \033[1;m"""
                        )
                        print()
                        OuiLookup().main()

                    elif args[1] == "port-scanner":
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
                        PortScanner().main()

                    elif args[1] == "dos":
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
                        DoS().main()

                    elif args[1] == "ping":
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
                        Ping().main()

                    elif args[1] == "vuln-scanner":
                        print()
                        info_message(
                            f'Selected {green("vuln-scannner", "bold")} module'
                        )
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
                        VulnerabilityScanner().main()

                    elif args[1] == "custom":
                        print()
                        info_message(f'Selected {green("custom", "bold")} module')
                        print()
                        custom()

                    else:
                        error_message(
                            "Please enter a valid module name. Example:",
                            "use network-scanner",
                        )
                        prompt()
                except IndexError:
                    error_message(
                        "Please enter a valid module name. Example:",
                        "use network-scanner",
                    )
                    prompt()

            elif command == "exit":
                exit_program()

            elif command == "clear":
                os.system("clear")
                prompt()

            elif command == "":
                prompt()

            elif command == "modules":
                print()
                print(f'{yellow("Modules:", ["bold", "underlined"])}')
                modules_table = [
                    ["", "Module", "Information", "Options"],
                    [
                        "1",
                        NetworkScanner().name,
                        NetworkScanner().description,
                        NetworkScanner().options,
                    ],
                    [
                        "2",
                        DeviceInfo().name,
                        DeviceInfo().description,
                        DeviceInfo().options,
                    ],
                    [
                        "3",
                        OuiLookup().name,
                        OuiLookup().description,
                        OuiLookup().options,
                    ],
                    [
                        "4",
                        OSGuesser().name,
                        OSGuesser().description,
                        OSGuesser().options,
                    ],
                    [
                        "5",
                        PortScanner().name,
                        PortScanner().description,
                        PortScanner().options,
                    ],
                    [
                        "6",
                        DoS().name,
                        DoS().description,
                        DoS().options,
                    ],
                    [
                        "7",
                        Ping().name,
                        Ping().description,
                        Ping().options,
                    ],
                    [
                        "8",
                        "vuln-scanner",
                        "Scan the target for vulnerabilities",
                        "TARGET",
                    ],
                ]
                # Display the modules in the format of a table:
                print(
                    tabulate(
                        modules_table,
                        stralign="left",
                        tablefmt="fancy_grid",
                        headers="firstrow",
                    )
                )
                print()
                info_message('"TARGET" option is the IP Address of the target device.')
                info_message(
                    '"OUI" option is the first 3 parts of the MAC Address of the target device.'
                )
                info_message(
                    'Run "use <module>" to use a module (<module> is the name of the module to use)'
                )

                print()
                prompt()

            elif command == "help":
                print()
                Help().prompt_msg()
                prompt()

            elif command == "shell":
                Shell().main()

            elif command == "auto":
                Auto().main()

            else:
                error_message(
                    f'Invalid command: "{command}". Please enter a valid command.'
                )
                prompt()
    except IndexError:
        prompt()


# The prompts used inside the modules.
# Example: `netsploit => (MODULE NAME) > `
def custom_prompt(module_name):
    """Function that acts as a template for the prompts in each module"""
    custom_prompt_input = input(
        f'{yellow("netsploit", "underlined")} => {blue(f"({module_name})", "bold")} {green(">")} '
    )
    custom_prompt_input = custom_prompt_input.lower()

    return custom_prompt_input
