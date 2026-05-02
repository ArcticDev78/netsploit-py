"""
Tests for utils/module_registry.py

Covers:
  - list_modules() returns all 10 expected names in consistent order
  - load_module_attr() raises ModuleRegistryError for unknown names
  - run_module() returns (False, non-empty str) for unknown names
  - get_module_metadata() returns graceful fallback for unknown names
  - clear_caches() runs without error
  - get_module_metadata() returns correct full_name for known modules

NOTE: Real modules (network-scanner, port-scanner, etc.) are NOT invoked
because they call nmap / network resources. Only metadata and error-paths
are exercised.
"""

import pytest

from utils.module_registry import (
    MODULE_MAP,
    ModuleRegistryError,
    clear_caches,
    get_module_metadata,
    list_modules,
    load_module_attr,
    run_module,
)

# ---------------------------------------------------------------------------
# Expected module names (order matters — same as MODULE_MAP insertion order)
# ---------------------------------------------------------------------------

EXPECTED_MODULES = [
    "network-scanner",
    "device-info",
    "os-guesser",
    "oui-lookup",
    "port-scanner",
    "dos",
    "ping",
    "vuln-scanner",
    "custom",
    "auto",
]


# ---------------------------------------------------------------------------
# Fixture: clear all caches before every test to prevent cross-test pollution
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def fresh_caches():
    """Clear registry caches before each test."""
    clear_caches()
    yield
    clear_caches()


# ---------------------------------------------------------------------------
# list_modules
# ---------------------------------------------------------------------------


def test_list_modules_contains_all_expected_names():
    modules = list_modules()
    for name in EXPECTED_MODULES:
        assert name in modules, f"Expected module '{name}' missing from list_modules()"


def test_list_modules_has_correct_count():
    assert len(list_modules()) == 10


def test_list_modules_order_is_consistent():
    """Calling list_modules() twice must return the same ordered list."""
    first = list_modules()
    second = list_modules()
    assert first == second


def test_list_modules_matches_expected_order():
    """The returned list must exactly match the insertion order of MODULE_MAP."""
    assert list_modules() == EXPECTED_MODULES


# ---------------------------------------------------------------------------
# load_module_attr — unknown name
# ---------------------------------------------------------------------------


def test_load_module_attr_unknown_raises_registry_error():
    with pytest.raises(ModuleRegistryError):
        load_module_attr("unknown-module")


def test_load_module_attr_error_message_contains_name():
    with pytest.raises(ModuleRegistryError, match="unknown-module"):
        load_module_attr("unknown-module")


# ---------------------------------------------------------------------------
# run_module — unknown name
# ---------------------------------------------------------------------------


def test_run_module_unknown_returns_false():
    success, error = run_module("unknown-module")
    assert success is False


def test_run_module_unknown_returns_nonempty_error_string():
    _, error = run_module("unknown-module")
    assert isinstance(error, str)
    assert len(error) > 0


def test_run_module_unknown_error_mentions_name():
    _, error = run_module("unknown-module")
    assert "unknown-module" in error


# ---------------------------------------------------------------------------
# get_module_metadata — unknown name (graceful fallback)
# ---------------------------------------------------------------------------


def test_get_module_metadata_unknown_returns_dict():
    meta = get_module_metadata("unknown-module")
    assert isinstance(meta, dict)


def test_get_module_metadata_unknown_has_required_keys():
    meta = get_module_metadata("unknown-module")
    assert "full_name" in meta
    assert "description" in meta
    assert "options" in meta


def test_get_module_metadata_unknown_full_name_is_string():
    meta = get_module_metadata("unknown-module")
    assert isinstance(meta["full_name"], str)


# ---------------------------------------------------------------------------
# clear_caches
# ---------------------------------------------------------------------------


def test_clear_caches_runs_without_error():
    """clear_caches() must complete without raising any exception."""
    clear_caches()  # already called by fixture; call again explicitly


def test_clear_caches_can_be_called_multiple_times():
    clear_caches()
    clear_caches()
    clear_caches()


# ---------------------------------------------------------------------------
# get_module_metadata — known modules (metadata correctness)
# ---------------------------------------------------------------------------


def test_get_module_metadata_port_scanner_full_name():
    meta = get_module_metadata("port-scanner")
    assert meta["full_name"] == "Port Scanner"


def test_get_module_metadata_os_guesser_full_name():
    meta = get_module_metadata("os-guesser")
    assert meta["full_name"] == "OS Guesser"


def test_get_module_metadata_known_module_has_all_keys():
    """Every known module's metadata dict must have the three standard keys."""
    for name in EXPECTED_MODULES:
        meta = get_module_metadata(name)
        assert "full_name" in meta, f"'full_name' missing for module '{name}'"
        assert "description" in meta, f"'description' missing for module '{name}'"
        assert "options" in meta, f"'options' missing for module '{name}'"
