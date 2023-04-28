# Import required library for font styles
from simple_colors import yellow, blue, green, red, cyan

# Error message font style
def error_message(error_msg, solution=None):
    if solution:
        print(f'[{red("!", "bold")}] {error_msg} {green(solution, "bold")}')  # noqa
    else:
        print(f'[{red("!", "bold")}] {error_msg}')


# Success message font style
def success_message(success_msg):
    print(f'[{green("+", "bold")}] {success_msg}')


# Info message font style
def info_message(info_msg):
    print(f'[{yellow("*", "bold")}] {info_msg}')
