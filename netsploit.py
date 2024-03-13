""" This is the main file of the whole program (DO NOT DELETE THIS FILE!) """

# /// IMPORTS ///

from utils.exit_program import exit_program
# from src.utils.exit_program import exit_program
# from src.utils.prompt import prompt
# from src.utils.startup import startup
# from utils import exit_program, prompt, startup
from utils.prompt import prompt
from utils.startup import startup

# OLDER IMPORTS - THESE WILL BE REMOVED LATER
# import datetime
# import os
# import sys
# import time
# from simple_colors import blue, cyan, green, red, yellow
# from tabulate import tabulate


# /// STARTUP ///
# Display the startup screen
startup()


# /// MAIN PROMPT ///
# Display the initial prompt from which other modules can be used
try:
    prompt()
except KeyboardInterrupt:  # If Ctrl-C is pressed, exit
    print()
    exit_program()
