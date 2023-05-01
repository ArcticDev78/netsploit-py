# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from functions.utils.font_styles import *

def custom():
    from functions.utils.prompt import prompt
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