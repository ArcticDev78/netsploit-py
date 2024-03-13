""" OUI Lookup Module
- Search the database (oui.txt) for the device OUI (first three parts of the MAC
  Address, separated by colons (:) )
"""

# Import required modules and libraries
import datetime
import os

from simple_colors import blue, cyan, green, yellow

from utils.config import LOGS_FOLDER_PATH, OUI_FILE_PATH
from utils.font_styles import error_message, success_message


class OuiLookup:
    """OUI Lookup class with:
    __init__() method providing module metadata,
    run() method to be called in the Auto module"""

    def __init__(self):
        self.name = "oui-lookup"
        self.description = "Find the manufacturer of target with OUI"
        self.options = "<prompt>: OUI"

    def main(self):
        """Find the manufacturer of target with OUI"""
        from utils.prompt import prompt

        print(
            f'{yellow("netsploit", "underlined")} => {blue("(oui-lookup)", "bold")}\n'
        )
        query = input(f'[{green(">", "bold")}] {cyan("Enter OUI to lookup: ", "bold")}')
        # For logging
        date = datetime.datetime.now()
        formatted_time = date.strftime("%I-%M-%S_%p_%d-%b-%Y")
        filename = f"oui-lookup_log_{formatted_time}.txt"
        log_filename = f"{LOGS_FOLDER_PATH}oui-lookup/{filename}"

        # First, open the OUI file and check if the query string exists in it
        with open(OUI_FILE_PATH) as f:
            if query in f.read():
                print()
                success_message(f'Found OUI {cyan(query, "bold")} in database!')
                print()
                # Then, log (each) occurence of the query string existing in the file

                # Open the source text file in read mode
                with open(OUI_FILE_PATH, "r") as source_file:
                    # Open the destination text file in write mode
                    with open(log_filename, "w") as output_file:
                        # Read each line of the source text file
                        for line in source_file:
                            # Search for the desired string within the line
                            if query in line:
                                # DB.set("OUI_FOUND", True)
                                # success_message(f'Found OUI {cyan(query, "bold")} in database.')
                                # Print the line which was found
                                print(f'[{green("✓", "bold")}] {yellow(line, "bold")}')
                                # Write the line to the destination text file
                                output_file.write(line)
                            # else:
                            #     error_message(
                            #         f'Could not find OUI {cyan(query, "bold")} in database.'
                            #     )

                    # Close both the source and destination text files
                    source_file.close()
                    output_file.close()

                    # Search the OUI Database (`OUI_FILE_PATH`) for `query` (inputted string)
                    # with open(OUI_FILE_PATH, "r") as file:
                    #     lines = file.readlines()
                    #     file_data = file.read()
                    #     file.close()
                    #     # for line in lines:
                    #         if query in file_data:
                    #             DB.set("OUI_FOUND", True)
                    #             print()
                    #             success_message(f'Found OUI {cyan(query, "bold")} in database.')
                    #             print(f'\n\t{yellow(line, "bold")}\n')
                    #         # else:
                    #
                    #             DB.set(
                    #                 "OUI_FOUND", False
                    #             )  # Probably a bad practice but its there so that the value can get cleared
                    #             print()
                    #             error_message(
                    #                 f'Could not find OUI {cyan(query, "bold")} in database.'
                    #             )
                    #             print()
                    # oui_found = DB.get("OUI_FOUND")

                    # if oui_found is True:
                    log_choice = input(
                        f'[{green(">", "bold")}] {cyan("Do you want to save the OUI Lookup results to a log file? (y/n): ", "bold")}'
                    )
                    if log_choice == "y":  # If the users agrees, i.e. types "y":
                        print()
                        # Create and write the results to a log file
                        # with open(log_filename, "w") as log_file:
                        #     for line in lines:
                        #         for query in lines:
                        #             log_file.write(f"{query}\n")

                        # We are not creating any file and writing to it as it is already done above
                        success_message(f"Saved results to log file: {log_filename}")
                        print()
                    elif (
                        log_choice == "n"
                    ):  # Else if the user disagrees, i.e. types "n":

                        # Delete the log file
                        try:
                            os.remove(log_filename)
                            print()
                            success_message("Did not save log file.")
                            print()
                            prompt()
                        except OSError as e:
                            error_message(
                                f"Error: {log_filename} could not be deleted.\n{e}"
                            )
                            prompt()

                        # print()
                        # success_message("Did not save log file.")
                        # print()
                    else:
                        # If the user types anything other than "y" or "n":
                        print()
                        error_message("Invalid option. Enter either y - YES or n - NO")
                        print()
                        self.main()
                        # Delete the log file
                        try:
                            os.remove(log_filename)
                            print()
                            success_message("Did not save log file.")
                            print()
                            prompt()
                        except OSError as e:
                            error_message(
                                f"Error: {log_filename} could not be deleted.\n{e}"
                            )
                            prompt()

            else:
                # If the query was not found, clear the value in the DB for next module run
                print()
                error_message(f'Could not find OUI {cyan(query, "bold")} in database.')
                print()

        # Clear the value for the next module run
        try:
            # DB.rem("OUI_FOUND")
            prompt()
        except KeyError:
            prompt()

        # prompt()
