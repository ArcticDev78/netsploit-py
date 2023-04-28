# import required modules and libraries
import os
from simple_colors import yellow, blue, green, cyan
import datetime
from functions.utils.font_styles import *
from functions.utils.config import logs_folder_path, oui_file_path


def oui_lookup():
    from functions.utils.prompt import prompt
    print(f'{yellow("netsploit", "underlined")} => {blue("(oui-lookup)", "bold")}\n')  # noqa
    oui = input(f'[{green(">", "bold")}] {cyan("Enter OUI to lookup: ", "bold")}')  # noqa
    # For logging
    date = datetime.datetime.now()
    formatted_time = date.strftime('%I-%M-%S_%p_%d-%b-%Y')
    filename = f'oui-lookup_log_{formatted_time}.txt'
    os.system(f'touch "{logs_folder_path}oui-lookup/{filename}"')
    with open(oui_file_path) as f:
        if oui in f.read():
            print()
            success_message(f'Found OUI {cyan(oui, "bold")} in database.')
            file = open(oui_file_path, "r")
            searchlines = file.readlines()
            file.close()
            for i, line in enumerate(searchlines):
                if oui in line:
                    for foundLine in searchlines[i:i+3]:
                        print()
                        print(f'\t{yellow(foundLine, "bold")}')
                        print()
            choice = input(f'[{green(">", "bold")}] {cyan("Do you want to save the results to a log file? (y/n): ", "bold")}')  # noqa
            if choice == 'y':  # If the users agrees, i.e. types "y":
                # pwd = os.popen('pwd').read()  # For printing to success message  # noqa
                print()
                # Print a success message stating the log has been saved.
                for i, line in enumerate(searchlines):
                    if oui in line:
                        for foundLine in searchlines[i:i+3]:
                            os.system(f'echo "{foundLine}" >> "{logs_folder_path}oui-lookup/{filename}"')  # noqa

                success_message(f'Saved results to log file: {logs_folder_path}oui-lookup/{filename}')  # noqa
                print()
            elif choice == 'n':  # Else if the user disagrees, i.e. types "n":
                os.system(f'rm "{logs_folder_path}oui-lookup/{filename}" -f')  # Delete the log file  # noqa
                print()
                success_message('Did not save log file.')
                print()
            else:
                # If the user types anything other than "y" or "n":
                print()
                error_message('Invalid option. Enter either y - YES or n - NO')
                print()
                os.system(f'rm "{logs_folder_path}oui-lookup/{filename}" -f')  # Delete the log file  # noqa
                ()

        else:
            print()
            error_message(f'Could not find OUI {cyan(oui, "bold")} in database.')  # noqa
            print()

    prompt()