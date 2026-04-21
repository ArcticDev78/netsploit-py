"""
Target management utility module for netsploit-py.

This module provides simple functions To get and set the current target,
making it accessible and modifiable across different modules.
"""

from typing import Union

# The current target is stored in-memory. Historically the codebase checks
# `get_target() is False` to detect "not set". Keep that contract by defaulting
# to False so existing modules don't break.
_current_target: Union[str, bool] = False


def get_target() -> Union[str, bool]:
    """Retrieve the current target.

    Returns:
        Union[str, bool]: The current target value, or False if not set.
    """
    return _current_target


def set_target(target: Union[str, bool]) -> None:
    """Set the current target.

    Args:
        target (Union[str, bool]): The target value to be stored (string or False to unset).
    """
    global _current_target
    _current_target = target
