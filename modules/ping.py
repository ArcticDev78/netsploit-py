""" Ping Module
- Ping the target device to check its accessibility and the time taken to send the 
  packets back and forth.
"""

# Import required modules and libraries
import os

from simple_colors import blue, cyan, green, red, yellow

from utils.config import DB
from utils.font_styles import error_message, info_message, success_message


class Ping:
    """Ping class with:
    __init__() method providing module metadata,
    __ping() method using the OS-builtin `ping` command
    __nping() method using the nmap-provided `nping` command
    run() method to be called in the Auto module, and
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "ping"
        self.description = (
            "Check the accessibility and latency in reaching the target device"
        )
        self.options = "<prompt>: TARGET"

    def __ping(self, target_param=None):
        """
        `target_param` is the method parameter to use as the target to ping.
        This parameter is handled in two ways:
        1) If `target_param` IS supplied when calling this method, that will be taken as the
           target to ping.
        2) If `target_param` is NOT supplied when calling this method, the `target` variable
           (through `input`) will be taken as the target to ping.
        """
        if target_param:
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target_param} (5 times)...\n")
            # Run the `ping` command on the target 5 times
            os.system(f"ping -c 5 {target_param}")
            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target_param}\n")
            # prompt()
        else:
            # Ask the user for the IP of the device to ping
            target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')
            print()
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target} (5 times)...\n")
            # Run the `ping` command on the target 5 times
            os.system(f"ping -c 5 {target}")
            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target}\n")
            # prompt()

    def __nping(self, target_param=None):
        """
        `target_param` is the method parameter to use as the target to ping.
        This parameter is handled in two ways:
        1) If `target_param` IS supplied when calling this method, that will be taken as the
           target to ping.
        2) If `target_param` is NOT supplied when calling this method, the `target` variable
           (through `input`) will be taken as the target to ping.
        """
        if target_param:
            # from utils.prompt import prompt

            # Ask the user for the IP of the device to ping
            # target = input("Enter IP of device to ping: ")
            print()
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target_param} (5 times)...")
            # Print a `success_message` to let the user know the `ping` command has finished running
            os.system(f"nping -c 5 {target_param}")
            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target_param}\n")
            # prompt()
        else:
            # Ask the user for the IP of the device to ping
            target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')
            print()
            # Print an `info_message` to indicate how many times (5) the `target` is being pinged
            info_message(f"Pinging {target} (5 times)...")
            # Print a `success_message` to let the user know the `ping` command has finished running
            os.system(f"nping -c 5 {target}")
            print()
            # Print a `success_message` to let the user know the `ping` command has finished running
            success_message(f"Finished pinging {target}\n")
            # prompt()

    def run(self, pingmode):
        """`run` method to access each ping mode"""
        from utils.prompt import prompt

        # If the user chooses to use the first option - ping
        if pingmode == ("ping", "1"):
            already_set_target = DB.get("TARGET")
            # If the user has NOT already provided a target before, then prompt the user for it
            # and use that in `self.__ping()`
            if already_set_target is False:
                target = input(
                    f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
                )
                print()
                self.__ping(target)
                prompt()
            # Else, check if the user HAS already provided a target before, and if it is so,
            # prompt the user if they want to use the same target.
            # If the user responds yes, pass the `already_set_target` in `self.__ping()`
            # Otherwise, prompt the user for their desired target
            else:
                # Prompt the user if they want to use the `already_set_target` or not
                userchoice = input(
                    (
                        f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {already_set_target}? [y/n]: ")}'
                    )
                )
                if userchoice == "y":
                    print()
                    self.__ping(already_set_target)
                    prompt()

                elif userchoice == "n":
                    print()
                    success_message(
                        f"OK, {red('not', 'bold')} using {already_set_target} as target."
                    )
                    print()
                    target = input(
                        f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
                    )
                    print()
                    self.__ping(target)
                    prompt()

        # Else, if the user chooses to use the second option - nping
        elif pingmode in ("nping", "2"):
            already_set_target = DB.get("TARGET")
            # If the user has NOT already provided a target before, then prompt the user for it
            # and use that in `self.__nping()`
            if already_set_target is False:
                # self.__nping()
                target = input(
                    f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
                )
                print()
                self.__nping(target)
                prompt()
            else:
                # Else, check if the user HAS already provided a target before, and if it is so,
                # prompt the user if they want to use the same target.
                # If the user responds yes, pass the `already_set_target` in `self._n_ping()`
                # Otherwise, prompt the user for their desired target

                # self.__nping(already_set_target)
                # prompt()
                # else:
                # Prompt the user if they want to use the `already_set_target` or not
                userchoice = input(
                    (
                        f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {already_set_target}? [y/n]: ")}'
                    )
                )
                if userchoice == "y":
                    print()
                    self.__nping(already_set_target)
                    prompt()

                elif userchoice == "n":
                    print()
                    success_message(
                        f"OK, {red('not', 'bold')} using {already_set_target} as target."
                    )
                    print()
                    target = input(
                        f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
                    )
                    print()
                    self.__nping(target)
                    prompt()

    def main(self):
        """Function which includes module prompt with all in-module commands"""
        from utils.prompt import prompt

        print(f'{yellow("netsploit", "underlined")} => {blue("(ping)", "bold")}\n')

        # Prompt the user if they want to use: 1) ping `self.__ping()` or 2) nping `self.__nping()`
        print(
            f'{yellow("Ping modes:", ["bold", "underlined"])}\n1. {cyan("ping", "bold")} [Basic - OS-Provided]\n2. {cyan("nping", "bold")} [Advanced, Nmap-provided]\n'
        )
        pingmode = input(
            f'[{green(">", "bold")}] {cyan("Enter ping mode to use: ", "bold")}'
        ).lower()

        # If the user chooses to use the first option - ping
        if pingmode == ("ping", "1"):
            # already_set_target = DB.get("TARGET")
            # # If the user has NOT already provided a target before, then prompt the user for it
            # # and use that in `self.__ping()`
            # if already_set_target is False:
            #     self.__ping()
            #     prompt()
            # # Else, check if the user HAS already provided a target before, and if it is so,
            # # prompt the user if they want to use the same target.
            # # If the user responds yes, pass the `already_set_target` in `self.__ping()`
            # # Otherwise, prompt the user for their desired target
            # else:
            #     # Prompt the user if they want to use the `already_set_target` or not
            #     userchoice = input(
            #         (
            #             f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {already_set_target}? [y/n]: ")}'
            #         )
            #     )
            #     if userchoice == "y":
            #         print()
            #         self.__ping(already_set_target)
            #         prompt()
            #
            #     elif userchoice == "n":
            #         print()
            #         success_message(
            #             f"OK, {red('not', 'bold')} using {already_set_target} as target."
            #         )
            #         print()
            #         target = input(
            #             f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
            #         )
            #         print()
            #         self.__ping(target)
            #         prompt()
            self.run("ping")
            prompt()

        # Else, if the user chooses to use the second option - nping
        elif pingmode in ("nping", "2"):
            # already_set_target = DB.get("TARGET")
            # # If the user has NOT already provided a target before, then prompt the user for it
            # # and use that in `self.__nping()`
            # if already_set_target is False:
            #     self.__nping()
            #     prompt()
            # # Else, check if the user HAS already provided a target before, and if it is so,
            # # prompt the user if they want to use the same target.
            # # If the user responds yes, pass the `already_set_target` in `self._n_ping()`
            # # Otherwise, prompt the user for their desired target
            # else:
            #     # self.__nping(already_set_target)
            #     # prompt()
            #     # else:
            #     # Prompt the user if they want to use the `already_set_target` or not
            #     userchoice = input(
            #         (
            #             f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {already_set_target}? [y/n]: ")}'
            #         )
            #     )
            #     if userchoice == "y":
            #         print()
            #         self.__nping(already_set_target)
            #         prompt()
            #
            #     elif userchoice == "n":
            #         print()
            #         success_message(
            #             f"OK, {red('not', 'bold')} using {already_set_target} as target."
            #         )
            #         print()
            #         target = input(
            #             f'[{green(">", "bold")}] {cyan("IP of device to ping:")} '
            #         )
            #         print()
            #         self.__nping(target)
            #         prompt()
            self.run("nping")
            prompt()

        else:
            print()
            error_message(
                f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n'
            )
            # ping()
            self.main()
        # else:
        #
        #     userchoice = input(
        #         (
        #             f'[{green(">", "bold")}] {cyan(f"Target has already been set. Do you want to ping {already_set_target}? [y/n]: ")}'
        #         )
        #     )
        #     if userchoice == "y":
        #         # target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')
        #         print()
        #         info_message(f"Pinging {already_set_target} (5 times)...\n")
        #         os.system(f"ping -c 5 {already_set_target}")
        #         print()
        #         success_message(f"Finished pinging {already_set_target}\n")
        #         prompt()
        #         # elif pingmode == 'nping' or '2':
        #         #     target = input('Enter IP of device to ping: ')
        #         #     print()
        #         #     info_message(f'Pinging {target} (5 times)...')
        #         #     os.system(f'nping -c 5 {target}')
        #         #     print()
        #         #     success_message(f'Finished pinging {target}\n')
        #         #     prompt()
        #         # else:
        #         #     print()
        #         #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')
        #         #     ping()
        #
        #     elif userchoice == "n":
        #         print()
        #         success_message(f"OK, not using {already_set_target} as target.")
        #         print()
        #         target = input(f'[{green(">", "bold")}] {cyan("IP of device to ping:")} ')
        #         print()
        #         info_message(f"Pinging {target} (5 times)...\n")
        #         os.system(f"ping -c 5 {target}")
        #         print()
        #         success_message(f"Finished pinging {target}\n")
        #         prompt()
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
        #     error_message(f'Invalid option: "{pingmode}", please enter either "ping" or "nping" as per your needs.\n')
        #     ping()
