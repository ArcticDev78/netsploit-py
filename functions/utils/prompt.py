# import required modules and libraries
from simple_colors import yellow, blue, green, red, cyan
from functions.utils.font_styles import *
import os
from tabulate import tabulate

# Import required modules
from functions.utils.exit_program import exit
from functions.utils.font_styles import *
from functions.modules.network_scanner import network_scanner
from functions.modules.device_info import device_info
from functions.modules.os_guesser import os_guesser
from functions.modules.oui_lookup import oui_lookup
from functions.modules.port_scanner import port_scanner
from functions.modules.dos import dos
from functions.modules.ping import ping
from functions.modules.vuln_scanner import vuln_scanner
from functions.modules.custom import custom
from functions.modules.shell import shell
from functions.modules.auto import auto
# from functions.utils.prompt import prompt

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
                        ['7', 'ping', 'Ping the target to see if they are online', '<prompt>: TARGET'],  # noqa
                        ['8', 'vuln-scanner', 'Scan the target for vulnerabilities', 'TARGET']]  # noqa

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
            auto()

        else:
            error_message(
                f'Invalid command: "{args[0]}". Please enter a valid command.')
            prompt()