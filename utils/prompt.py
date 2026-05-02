"""Main Prompt Module"""

import readline  # noqa: F401
import shutil
import textwrap
from typing import Any

from tabulate import tabulate

# from simple_colors import color  # Import the color function instead of individual colors
from utils.colors import blue, green, yellow  # type: ignore
from utils.secure_utils import safe_clear_screen

# Avoid importing module classes at top-level (prevents circular imports).
# Module classes will be loaded dynamically via `utils.module_registry` when needed.
from .exit_program import exit_program
from .font_styles import error_message, info_message
from .help import Help

# Define color functions using the color function from simple_colors
# blue = lambda text, style=None: color(text, 'blue', style)
# green = lambda text, style=None: color(text, 'green', style)
# yellow = lambda text, style=None: color(text, 'yellow', style)


def prompt():
    """Handle the main prompt and user input for module selection."""
    while True:
        try:
            prompt_input = input(f"{yellow('netsploit', 'underlined')} {green('>')} ")
            args = prompt_input.split()

            if not args:
                continue

            command = args[0].lower()

            if command == "use":
                handle_use_command(args)
            elif command == "exit":
                exit_program()
            elif command == "clear":
                safe_clear_screen()
            elif command == "modules":
                display_modules()
            elif command == "help":
                Help().prompt_help_msg()
            elif command == "shell":
                # Load and run the `shell` module via the module registry to avoid top-level imports
                try:
                    import utils.module_registry as registry  # local import to avoid cycle

                    success, err = registry.run_module("shell")
                    if not success:
                        error_message(err or "Failed to run module shell")
                except Exception as e:
                    error_message(f"Failed to run module shell: {e}")
            elif command == "auto":
                # Load and run the `auto` module via the module registry to avoid top-level imports
                try:
                    import utils.module_registry as registry  # local import to avoid cycle

                    success, err = registry.run_module("auto")
                    if not success:
                        error_message(err or "Failed to run module auto")
                except Exception as e:
                    error_message(f"Failed to run module auto: {e}")
            else:
                error_message(
                    f'Invalid command: "{command}". Please enter a valid command.'
                )

        except IndexError:
            continue


def handle_use_command(args: list[str]):
    """Handle the 'use' command to select and run modules using the module registry.

    This implementation uses `utils.module_registry` to dynamically import and
    instantiate modules at runtime, preventing circular imports that would
    occur if modules were imported at top-level.
    """
    import utils.module_registry as registry  # imported here to avoid top-level import cycle

    if len(args) < 2:
        error_message("Please enter a valid module name. Example: use network-scanner")
        return

    module_name = args[1]

    try:
        # Load the attribute (class or callable) for the requested module
        attr: Any = registry.load_module_attr(module_name)
    except Exception as e:
        error_message(f"Please enter a valid module name. {e}")
        return

    print()
    info_message(f"Selected {green(module_name, 'bold')} module.")

    # If attr is a class, get/create the instance and run it
    if isinstance(attr, type):
        try:
            instance: Any = registry.get_module_instance(module_name)
        except Exception as e:
            error_message(f"Failed to instantiate module {module_name}: {e}")
            return

        module_full_name = getattr(instance, "full_name", instance.__class__.__name__)
        module_description = getattr(
            instance, "description", "No description available."
        )

        print_module_header(module_full_name, module_description)

        if hasattr(instance, "main") and callable(getattr(instance, "main")):
            instance.main()
        elif hasattr(instance, "run") and callable(getattr(instance, "run")):
            instance.run()
        else:
            error_message(
                f'Module "{module_name}" does not have a runnable main() or run() method.'
            )

    else:
        # Attribute is a callable function (e.g., custom)
        try:
            attr()
        except Exception as e:
            error_message(f"Error running module {module_name}: {e}")


def print_module_header(module_name: str, module_description: str):
    """Print a formatted header for the selected module."""

    # Get terminal width, default to 80 if not available
    terminal_width = shutil.get_terminal_size((80, 20)).columns

    # Set box width (adjust as needed, but keep it odd for center alignment)
    box_width = min(terminal_width - 3, 65)  # -2 for some margin
    content_width = box_width - 4  # Subtract 4 for the border characters

    # ANSI escape codes for formatting
    bold_cyan = "\033[1;36m"
    bold_yellow = "\033[1;33m"
    underline = "\033[4m"
    italic = "\033[3m"
    reset = "\033[0m"

    # Prepare the title and description
    # title = module_name.center(content_width)
    # description_lines = textwrap.wrap(module_description, width=content_width - 6)  # -6 for extra padding
    # description_lines = textwrap.wrap(module_description, width=content_width - 4 )  # -6 for extra padding
    # Center the title and add underline only to the text
    title = module_name.strip()  # Remove any leading/trailing spaces
    left_padding = (content_width - len(title)) // 2
    right_padding = content_width - len(title) - left_padding
    title_line = f"{' ' * left_padding}{underline}{title}{reset}{bold_yellow}{' ' * right_padding}"

    description_lines = textwrap.wrap(module_description, width=content_width - 4)

    box = [
        f"{bold_cyan}╒{'═' * (box_width - 2)}╕{reset}",
        f"{bold_cyan}│{' ' * content_width}  │{reset}",
        f"{bold_cyan}│ {bold_yellow}{title_line}{reset}{bold_cyan} │{reset}",
        f"{bold_cyan}│{' ' * content_width}  │{reset}",
        # f"{bold_cyan}│{' ' * content_width}  │{reset}"
    ]

    for line in description_lines:
        padded_line = line.center(content_width)
        box.append(
            f"{bold_cyan}│{reset} {italic}{padded_line}{reset} {bold_cyan} │{reset}"
        )

    box.append(f"{bold_cyan}╘{'═' * (box_width - 2)}╛{reset}")

    print()
    print("\n".join(box))
    print()


def display_modules():
    """Display available modules in a formatted table using the module registry."""
    import utils.module_registry as registry  # local import to avoid cycles

    print()
    print(f"{yellow('Modules:', ['bold', 'underlined'])}")

    modules_table = [["", "Module", "Information", "Options"]]

    for i, name in enumerate(registry.list_modules(), 1):
        meta = registry.get_module_metadata(name)
        modules_table.append(
            [str(i), name, meta.get("description", ""), meta.get("options", "")]
        )

    print(
        tabulate(
            modules_table, headers="firstrow", tablefmt="fancy_grid", stralign="left"
        )
    )
    print()
    info_message('"TARGET" option is the IP Address of the target device.')
    info_message(
        '"OUI" option is the first 3 parts of the MAC Address of the target device.'
    )
    info_message(
        'Run "use <module>" to use a module (<module> is the name of the module to use)'
    )
    print()


def get_module_list() -> list[str]:
    """Return a list of module names (from the registry)."""
    import utils.module_registry as registry

    return registry.list_modules()


def create_module_row(index: int, module_name: str) -> list[str]:
    """Create a row for the modules table.

    Note: Kept for backwards compatibility with older code paths. Current
    display_modules uses the registry's metadata instead.
    """
    meta = __import__(
        "utils.module_registry", fromlist=["get_module_metadata"]
    ).get_module_metadata(module_name)
    return [
        str(index),
        meta.get("full_name", module_name),
        meta.get("description", ""),
        meta.get("options", ""),
    ]


def custom_prompt(module_name: str) -> str:
    """Generate a custom prompt for each module."""
    return input(
        f"{yellow('netsploit', 'underlined')} => {blue(f'({module_name})', 'bold')} {green('>')} "
    ).lower()


if __name__ == "__main__":
    prompt()
