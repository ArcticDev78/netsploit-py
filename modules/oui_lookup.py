"""OUI Lookup Module
- Search the database (oui.txt) for the device OUI (first three parts of the MAC
  Address, separated by colons (:) )
"""

# Import required modules and libraries
from utils.colors import cyan, green, yellow
from utils.config import Config
from utils.font_styles import error_message, success_message
from utils.logging import LogManager

from .base import BaseModule


class OuiLookup(BaseModule):
    """OUI Lookup module for finding device manufacturers by OUI."""

    def __init__(self):
        self.name = "oui-lookup"
        self.full_name = "OUI Lookup"
        self.description = "Find the manufacturer of target with OUI"
        self.options = "<prompt>: OUI"
        self.requires_target = False
        self.query = None

    def run(self, query=None):
        """Execute OUI lookup with provided query."""
        if query is None:
            error_message("OUI query required")
            return

        self.query = query
        log_path = self._execute_core_logic()
        self._handle_results(log_path)

    def main(self):
        """Interactive prompt mode."""
        self._show_module_header()
        self.query = self._get_input("OUI to lookup")
        print()

        log_path = self._execute_core_logic()
        self._handle_results(log_path)
        self._prompt_continue()

    def _execute_core_logic(self):
        """Execute the OUI lookup in database."""
        if not self.query:
            error_message("No OUI query specified.")
            return None

        oui_file_path = Config.OUI_FILE_PATH
        # Get log path only if logging is enabled
        log_path = (
            LogManager.get_log_file_path(self.name) if Config.LOGS_ENABLED else None
        )

        # First check if OUI exists in file
        with open(oui_file_path) as f:
            if self.query not in f.read():
                error_message(
                    f"Could not find OUI {cyan(self.query, 'bold')} in database."
                )
                print()
                return None

        print()
        success_message(f"Found OUI {cyan(self.query, 'bold')} in database!")
        print()

        # Search and log results
        results = []
        with open(oui_file_path, "r") as source_file:
            for line in source_file:
                if self.query in line:
                    print(f"[{green('✓', 'bold')}] {yellow(line, 'bold')}")
                    results.append(line)

        # Write results to log if logging enabled
        if log_path:
            with open(log_path, "w") as output_file:
                output_file.writelines(results)

        return log_path
