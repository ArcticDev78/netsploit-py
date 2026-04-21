"""
Database utility module for netsploit-py.

This module sets up and manages the in-memory database using PickleDB.
It provides functionality for storing and retrieving the user-specified TARGET across modules.

Note: The current implementation requires this setup to be present.
"""

import pickledb
from typing import Any

def initialize_db(db_name: str = "netsploit.db", auto_dump: bool = False) -> pickledb.PickleDB:
    """
    Initialize and return a PickleDB database instance.

    Args:
        db_name (str): Name of the database file. Defaults to "netsploit.db".
        auto_dump (bool): Whether to automatically dump changes to disk. Defaults to False.

    Returns:
        pickledb.PickleDB: Initialized database object.

    Raises:
        Exception: If there's an issue creating or accessing the database file.
    """
    try:
        db = pickledb.load(db_name, auto_dump)
        return db
    except Exception as e:
        raise Exception(f"Failed to initialize database: {e}")

# Setup PickleDB (`DB` variable) with error handling
try:
    DB = initialize_db()
except Exception as e:
    print(f"Error: {e}")
    print("Falling back to in-memory database.")
    DB = pickledb.PickleDB(":memory:", False, sig=None)

def get_target() -> Any:
    """
    Retrieve the current TARGET from the database.

    Returns:
        Any: The current TARGET value, or None if not set.
    """
    return DB.get('TARGET')

def set_target(target: Any) -> bool:
    """
    Set the TARGET in the database.

    Args:
        target (Any): The target value to be stored.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    return DB.set('TARGET', target)

# Example usage:
# current_target = get_target()
# set_target("192.168.1.1")

# INFO: `DB` is used to 'set' and 'get' the TARGET option specified by the user across modules
