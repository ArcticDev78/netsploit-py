""" Custom Nmap Command Runner """

# Import required modules and libraries

import os

from simple_colors import blue, cyan, green, yellow

from modules.shell import Shell
from utils.font_styles import error_message, success_message


def custom():
    """Function to receive input of the custom nmap command to run"""
    from utils.prompt import prompt

    print(f'{yellow("netsploit", "underlined")} => {blue("(custom)", "bold")}\n')
    custom_nmap_cmd = input(
        f'[{green(">", "bold")}] {cyan("Enter custom nmap command to run: ", "bold")}'
    )
    if custom_nmap_cmd.startswith("nmap"):
        print()
        success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
        print()
        os.system(custom_nmap_cmd)
        print()
        prompt()

    elif custom_nmap_cmd.startswith("sudo"):
        cmd = custom_nmap_cmd.split()
        if cmd[1] == "nmap":
            print()
            success_message(f'Running custom nmap command "{custom_nmap_cmd}"')
            print()
            os.system(
                custom_nmap_cmd
            )  # In this context, `custom_nmap_cmd` is the actual shell command the user tried to run
            print()
            prompt()

        else:
            print()
            error_message(
                f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.'
            )
            print()
            choice = input(
                f'[{green(">", "bold")}] {cyan("Did you mean to run a shell commmand? [y/n]: ", "bold")}'
            )
            if choice == "y":
                print()
                Shell().run(custom_nmap_cmd)
            elif choice == "n":
                print()
                prompt()
            else:
                error_message(f'Invalid option "{choice}"')
                prompt()

    else:
        print()
        error_message(
            f'Your command must be an nmap command! To run any other shell command, use the {yellow("shell", "bold")} (netsploit) command.'
        )
        print()
        choice = input(
            f'[{green(">", "bold")}] {cyan("Did you mean to run a shell commmand? [y/n]: ", "bold")}'
        )
        if choice == "y":
            print()
            shell()
        elif choice == "n":
            print()
            prompt()
        else:
            error_message(f'Invalid option "{choice}"')
            prompt()
