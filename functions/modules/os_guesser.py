# Import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
import datetime
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path, db

def os_guesser():
    from functions.utils.prompt import prompt
    prompt_input = input(f'{yellow("netsploit", "underlined")} => {blue("(os-guesser)", "bold")} {green(">")} ')  # noqa
    prompt_input = prompt_input.lower()

    if prompt_input == 'show options':
        value = '(not set)' if db.get(
                'TARGET') is False else db.get('TARGET')
        # Table for displaying options and other info
        table = [['OPTIONS', 'VALUE', 'OPTIONAL?'], ['TARGET', value, 'no']]  # noqa
        # Print the table
        print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
        os_guesser()

    elif prompt_input.startswith('target =>') or prompt_input.startswith('set target'):  # noqa
        # split prompt_input from string to array
        optionArgs = prompt_input.split()
        # option is the second index (3rd string) in array
        option = optionArgs[2]
        # Set IP range to given option
        db.set('TARGET', option)
        # Display success message like this: "IP_RANGE set to 192.168.0.1"
        success_message(f'TARGET set to "{db.get("TARGET")}"')
        os_guesser()

    elif prompt_input == 'run':
        # If the command is "run":

        # retrive TARGET value from database
        TARGET = db.get('TARGET')
        # If the value of `TARGET` is not set by the user:
        if TARGET is False:
            # Print an error message
            error_message(
                'Cannot run scan(s) without TARGET being specified. Please specify the TARGET and try again')  # noqa
            os_guesser()
        else:
            # Or, if the value of `TARGET` is set:

            info_message(f'Running OS Guesser scan on {TARGET}, this may take up to two minutes')  # noqa
            info_message('Running a OS Guesser scan properly requires the command to be run using sudo')  # noqa
            print()
            # For logging
            date = datetime.datetime.now()
            formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
            filename = f'os-guesser_log_{formatted_time}.txt'
            # Run the scan
            os.system(f'sudo nmap -O --osscan-guess {TARGET} -Pn  -oN "{logs_folder_path}/os-guesser/{filename}"')  # noqa
            # os.system(f'sudo nmap -O --osscan-guess {TARGET} -Pn')
            print()
            # Print a success message
            success_message(f'Finished scanning {TARGET}')
            print()
            # Ask the user if they want to save the scan results to a log file.
            # print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                success_message(f'Saved results to log file: "{logs_folder_path}os-guesser/{filename}"')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}os-guesser/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}network-scanner/{filename}" -f')  # Delete the log file  # noqa
                os_guesser()
            os_guesser()
        os_guesser()

    elif prompt_input == 'exit':
        # Exit the program
        exit()

    elif prompt_input == 'back':
        # Go back to initial prompt
        prompt()

    elif prompt_input == '':
        # If user didn't enter anything and pressed enter, show os_guesser prompt again.  # noqa
        os_guesser()

    elif prompt_input == 'clear':
        # Clear the terminal using the shell command `clear`
        os.system('clear')
        os_guesser()

    elif prompt_input == 'help':
        # Help message
        print()
        print(f'{cyan("Help for os-guesser:", ["bold", "underlined"])}')
        print()
        print(f'[{yellow("Optional", "italic")}] See options that you can set using {yellow("show options", "bold")}')  # noqa
        print(f'1. Set the target using {yellow("set TARGET 123.456.789", "bold")} or {yellow("TARGET => 123.456.789", "bold")} (make sure to replace 123.456.789 with the IP of your target!)')  # noqa
        print(f'2. Run your scan using {yellow("run", "bold")}')
        print()
        os_guesser()

    else:

        # If the user types a command that is not any of the above.

        # The invalid command is index 0 of array
        invalidCommand = prompt_input.split()[0]
        error_message(f'Invalid command "{invalidCommand}". Please enter a valid command')  # noqa
        os_guesser()