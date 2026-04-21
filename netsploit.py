#!/usr/bin/env python3
"""
Netsploit: Network Security Testing Tool

This file serves as the main entry point for the Netsploit program.
It initializes the application, handles user interactions, and manages program flow.

The tool is designed to assist in network security testing and analysis.

It provides various modules for Different aspects of network security assessment.
Usage:
    $ python netsploit.py

Note: This tool should only be used on networks and systems you have permission to test.
"""

# IMPORTS
# Import required utils

from utils.exit_program import exit_program
from utils.prompt import prompt
from utils.startup import startup


def main():
    """
    Main function to run the Netsploit application.
    Handles the program flow and user interactions.
    """
    try:
        # Display the startup messages and initialize the application
        startup()

        # Enter the main prompt loop for user interactions
        prompt()

    except KeyboardInterrupt:
        exit_program()


if __name__ == "__main__":
    main()
