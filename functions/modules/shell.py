# import required modules and libraries
import os
from simple_colors import yellow, blue, green, red, cyan
from functions.utils.font_styles import *

def shell():
    from functions.utils.prompt import prompt
    print(f'{yellow("netsploit", "underlined")} => {blue("(shell)", "bold")}\n')  # noqa
    custom_cmd = input(f'[{green(">", "bold")}] {cyan("Enter shell command to run: ", "bold")}')  # noqa
    print()
    success_message(f'Running shell command "{custom_cmd}"')
    print()
    # pwd = os.popen('pwd').read()
    # os.system('cd ~')
    os.system(f'cd ~ && {custom_cmd}')
    # os.system(f'cd "{pwd}"')
    print()
    prompt()