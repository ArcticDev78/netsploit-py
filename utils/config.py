""" CONFIG 
- Store settings and variables to be accessed by modules, in this file.
"""

# Import required library for keeping `TARGET` in program memory
import pickledb

# /// STARTUP SCREEN
# Header to be shown on startup - you can change this to whatever you want!
HEADER = """
     __     _   __       _       _ _
  /\\ \\ \\___| |_/ _\\_ __ | | ___ (_) |_
 /  \\/ / _ \\ __\\ \\| '_ \\| |/ _ \\| | __|
/ /\\  /  __/ |__\\ \\ |_) | | (_) | | |_
\\_\\ \\/ \\___|\\__\\__/ .__/|_|\\___/|_|\\__|
                  |_|                                                                                                                                     
"""

# /// DATABASE - PICKLEDB (DO NOT TOUCH!)
DB = pickledb.load("netsploit.db", False)  # Setup PickleDB - DO NOT TOUCH


# /// LOGGING (OPTIONAL)
# NOTE: Change the paths to to absolute paths if needed

# Enable or disable logs. Default value is `True`
LOGS_ENABLED = True

# Set logs folder path to be accessed by modules - required if logs are ENABLED
LOGS_FOLDER_PATH = "./logs/"

# /// OUI Database Location (REQUIRED)
# Set OUI (text) file path used by oui-lookup module
OUI_FILE_PATH = "resources/oui.txt"
