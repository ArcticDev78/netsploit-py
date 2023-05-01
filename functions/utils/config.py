# Import required library for database
import pickledb

""" Store variables to be accessed by modules in this file """

# Setup PickleDB
db = pickledb.load('netsploit.db', False)

# Set logs folder path to be accessed by modules
logs_folder_path = 'logs/'

# Set OUI (text) file path to be accessed by oui-lookup module 
oui_file_path = 'oui.txt'