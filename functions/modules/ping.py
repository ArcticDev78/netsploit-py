# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
from functions.utils.font_styles import *
from functions.utils.config import db

def ping():
    from functions.utils.prompt import prompt
    print(f'{yellow("netsploit", "underlined")} => {blue("(ping)", "bold")}\n')  # noqa
    # print(f'{yellow("Ping modes:", ["bold", "underlined"])}\n1. {cyan("ping", "bold")}\n2. {cyan("nping", "bold")}\n')  # noqa
    # pingmode = input(f'[{green(">", "bold")}] {cyan("Enter ping mode to use: ", "bold")}')  # noqa
    # if pingmode == 'ping' or '1':

    alreadySetTarget = db.get('TARGET')
    if alreadySetTarget is False:
        target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
        print()
        info_message(f'Pinging {target} (5 times)...\n')
        os.system(f'ping -c 5 {target}')
        print()
        success_message(f'Finished pinging {target}\n')
        prompt()
        # elif pingmode == 'nping' or '2':
        #     target = input('Enter IP of device to ping: ')
        #     print()
        #     info_message(f'Pinging {target} (5 times)...')
        #     os.system(f'nping -c 5 {target}')
        #     print()
        #     success_message(f'Finished pinging {target}\n')
        #     prompt()
        # else:
        #     print()
        #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
        #     ping()
    else:

        userchoice = input((f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {alreadySetTarget}? [y/n]: ")}'))  # noqa
        if userchoice == 'y':
            # target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
            print()
            info_message(f'Pinging {alreadySetTarget} (5 times)...\n')
            os.system(f'ping -c 5 {alreadySetTarget}')
            print()
            success_message(f'Finished pinging {alreadySetTarget}\n')
            prompt()
            # elif pingmode == 'nping' or '2':
            #     target = input('Enter IP of device to ping: ')
            #     print()
            #     info_message(f'Pinging {target} (5 times)...')
            #     os.system(f'nping -c 5 {target}')
            #     print()
            #     success_message(f'Finished pinging {target}\n')
            #     prompt()
            # else:
            #     print()
            #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
            #     ping()

        elif userchoice == 'n':
            print()
            success_message(f'Okay, not using {alreadySetTarget} as target.')
            print()
            target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')  # noqa
            print()
            info_message(f'Pinging {target} (5 times)...\n')
            os.system(f'ping -c 5 {target}')
            print()
            success_message(f'Finished pinging {target}\n')
            prompt()
            # elif pingmode == 'nping' or '2':
            #     target = input('Enter IP of device to ping: ')
            #     print()
            #     info_message(f'Pinging {target} (5 times)...')
            #     os.system(f'nping -c 5 {target}')
            #     print()
            #     success_message(f'Finished pinging {target}\n')
            #     prompt()
            # else:
            #     print()
            #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')  # noqa
            #     ping()