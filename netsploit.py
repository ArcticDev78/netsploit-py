""" This is the main file of the whole program """

# /// IMPORTS ///
from utils.exit_program import exit_program
from utils.prompt import prompt
from utils.startup import startup

# /// STARTUP SCREEN ///
# Display the startup screen
startup()


# /// MAIN PROMPT ///
# Display the initial prompt from which other modules can be used
try:
    prompt()
except KeyboardInterrupt:  # If Ctrl-C is pressed, exit
    print()
    exit_program()
