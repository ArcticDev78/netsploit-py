""" Shell (CLI) Command Runner """

# Import required modules and libraries
import os

from simple_colors import blue, cyan, green, yellow

from utils.font_styles import success_message


class Shell:
    """DeviceInfo class with:
    __init__() method providing module metadata,
    run() method to be called in the Auto module, and
    main() method which is the whole module with all its functions"""

    def __init__(self):
        self.name = "shell"
        self.description = "Run a shell (CLI) command"
        self.options = "<prompt>: <command>"

    def run(self, command=None):
        """
        `command` parameter is the CLI command to be run
        """
        from utils.prompt import prompt

        print()
        success_message(f'Running shell command "{command}"')
        print()
        # Change working directory to `working_dir` to execute the command
        working_dir = "~"  # `~` is the $HOME directory
        os.system(f"cd {working_dir} && {command}")
        print()
        prompt()


    def main(self):
        """Function to execute custom shell commands"""
        # from utils.prompt import prompt

        print(f'{yellow("netsploit", "underlined")} => {blue("(shell)", "bold")}\n')  # noqa
        # Input function to get the command to be executed
        custom_cmd = input(
            f'[{green(">", "bold")}] {cyan("Enter shell command to run: ", "bold")}'
        )
        self.run(custom_cmd)
