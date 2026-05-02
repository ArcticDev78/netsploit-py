"""
Tests for utils/target.py

Covers:
  - Default value of _current_target is False
  - get_target() / set_target() round-trip
  - Resetting the target to False
  - Various valid string targets
"""

import pytest

import utils.target as target_module
from utils.target import get_target, set_target


@pytest.fixture(autouse=True)
def reset_target():
    """Ensure _current_target is reset to False before *and* after every test."""
    set_target(False)
    yield
    set_target(False)


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------


def test_initial_value_is_false():
    """After a reset the target must be exactly False (not just falsy)."""
    assert get_target() is False


# ---------------------------------------------------------------------------
# set_target / get_target round-trip
# ---------------------------------------------------------------------------


def test_set_and_get_ip_address():
    set_target("192.168.1.1")
    assert get_target() == "192.168.1.1"


def test_set_false_resets_target():
    set_target("10.0.0.1")
    assert get_target() == "10.0.0.1"
    set_target(False)
    assert get_target() is False


@pytest.mark.parametrize(
    "target_value",
    [
        "10.0.0.1",
        "hostname.local",
        "example.com",
    ],
)
def test_set_various_valid_strings(target_value):
    set_target(target_value)
    assert get_target() == target_value


# ---------------------------------------------------------------------------
# Module-level variable is updated in-place
# ---------------------------------------------------------------------------


def test_module_level_variable_reflects_set():
    """Accessing _current_target on the module directly should match get_target()."""
    set_target("scanner.local")
    assert target_module._current_target == "scanner.local"
    assert target_module._current_target == get_target()


def test_module_level_variable_reset_to_false():
    set_target("scanner.local")
    set_target(False)
    assert target_module._current_target is False


# ---------------------------------------------------------------------------
# Successive calls overwrite previous value
# ---------------------------------------------------------------------------


def test_successive_set_overwrites():
    set_target("first.host")
    set_target("second.host")
    assert get_target() == "second.host"


def test_set_empty_string():
    """An empty string is a falsy but valid string value — must be stored as-is."""
    set_target("")
    assert get_target() == ""
