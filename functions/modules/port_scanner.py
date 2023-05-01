# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path, db

def port_scanner():
    from functions.utils.prompt import prompt
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(port-scanner)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        port_scanner()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        port_scanner()

    elif prompt_input == 'run':
        TARGET = db.get('TARGET')
        if TARGET is False:
            error_message(
                'Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again')  # noqa
            port_scanner()
        else:
            info_message(f'Running port scan on {TARGET}, this may take up to two minutes')  # noqa
            print()
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'port-scanner_log_{formatted_time}.txt'
            os.system(
            f'nmap -T4 {TARGET} -sV -Pn -oN "{logs_folder_path}port-scanner/{filename}"')  # noqa
            # os.system(f'nmap -T4 {TARGET} -sV -Pn')
            print()
            success_message(f'Finished scanning {TARGET}')
            print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':
                # pwd = os.popen('pwd').read()
                print()
                success_message(f'Saved results to log file: {logs_folder_path}port-scanner/{filename}')  # noqa
                print()
            elif choice == 'n':
                os.system(f'rm "{logs_folder_path}port-scanner/{filename}" -f')
                print()
                success_message('Did not save log file.')
                print()
            else:
                error_message('Invalid option. Enter either y - YES or n - NO')  # noqa
            port_scanner()
        port_scanner()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == '':
        port_scanner()

    elif prompt_input == 'clear':
        os.system('clear')
        port_scanner()

    elif prompt_input == 'help':
        print()
        print(f'{cyan("Help for port-scanner:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        port_scanner()

    else:
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        port_scanner()