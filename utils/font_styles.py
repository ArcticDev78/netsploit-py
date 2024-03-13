""" Font Styles (Error, Success, Info) """

# Import required library for font styles
from simple_colors import green, red, yellow


def error_message(error_msg, solution=None):
    """Error Message font style"""
    if solution:  # If a solution is provided when the function is called
        print(f'[{red("!", "bold")}] {error_msg} {green(solution, "bold")}')  # noqa
    else:  # Else, if no solution is provided
        print(f'[{red("!", "bold")}] {error_msg}')


def success_message(success_msg):
    """Success Message font style"""
    print(f'[{green("+", "bold")}] {success_msg}')


def info_message(info_msg):
    """Info Message font style"""
    print(f'[{yellow("*", "bold")}] {info_msg}')
