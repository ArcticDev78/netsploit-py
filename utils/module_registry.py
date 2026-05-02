"""
Module registry and dynamic importer for NetSploit modules.

Purpose
-------
This module centralizes the mapping between CLI module names (as used by the
prompt) and the actual Python module paths / attributes. It provides helper
functions to import module attributes dynamically, instantiate module classes,
inspect module metadata (name/description/options), and run modules.

Benefits
--------
- Breaks circular imports by avoiding large top-level imports of `modules.*`
  inside the prompt or other utilities.
- Centralizes module metadata and import paths (easy to update in one place).
- Caches imports so each module is imported only once.

Usage
-----
from utils.module_registry import (
    list_modules,
    get_module_metadata,
    run_module,
    load_module_attr,
)

name_list = list_modules()
meta = get_module_metadata("network-scanner")
success = run_module("network-scanner")
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any, Callable, Dict, Optional, Tuple

# Mapping of CLI-name -> (python_module_path, attribute_name)
# attribute_name is either the class name (e.g. "NetworkScanner") or a callable
# function name (e.g. "custom").
# Keep this mapping in one place so other code can import it and load modules
# lazily via importlib.
MODULE_MAP: Dict[str, Tuple[str, str]] = {
    "network-scanner": ("modules.network_scanner", "NetworkScanner"),
    "device-info": ("modules.device_info", "DeviceInfo"),
    "os-guesser": ("modules.os_guesser", "OSGuesser"),
    "oui-lookup": ("modules.oui_lookup", "OuiLookup"),
    "port-scanner": ("modules.port_scanner", "PortScanner"),
    "dos": ("modules.dos", "DoS"),
    "ping": ("modules.ping", "Ping"),
    "vuln-scanner": ("modules.vuln_scanner", "VulnerabilityScanner"),
    "custom": ("modules.custom", "custom"),
    "auto": ("modules.auto", "Auto"),
}

# Internal caches to avoid repeated imports/instantiation
_LOADED_MODULES: Dict[str, ModuleType] = {}
_LOADED_ATTRS: Dict[str, Any] = {}
_INSTANCE_CACHE: Dict[str, Any] = {}


class ModuleRegistryError(RuntimeError):
    """Raised for registry-related errors."""


def list_modules() -> list[str]:
    """Return the list of available CLI module names (in insertion order)."""
    return list(MODULE_MAP.keys())


def _import_module(module_path: str) -> ModuleType:
    """Import a module by path and cache it."""
    if module_path in _LOADED_MODULES:
        return _LOADED_MODULES[module_path]

    try:
        mod = importlib.import_module(module_path)
    except Exception as e:
        raise ModuleRegistryError(
            f"Failed to import module '{module_path}': {e}"
        ) from e

    _LOADED_MODULES[module_path] = mod
    return mod


def load_module_attr(name: str) -> Any:
    """
    Load and return the attribute (class or function) for the given CLI module name.

    The attribute is cached so subsequent calls are fast.

    Raises:
        ModuleRegistryError: if the name is unknown or import fails.
    """
    if name in _LOADED_ATTRS:
        return _LOADED_ATTRS[name]

    if name not in MODULE_MAP:
        raise ModuleRegistryError(f"Unknown module name: {name!r}")

    module_path, attr_name = MODULE_MAP[name]
    mod = _import_module(module_path)

    try:
        attr = getattr(mod, attr_name)
    except AttributeError as e:
        raise ModuleRegistryError(
            f"Module '{module_path}' does not expose attribute '{attr_name}': {e}"
        ) from e

    _LOADED_ATTRS[name] = attr
    return attr


def get_module_instance(name: str, use_cache: bool = True) -> Any:
    """
    Instantiate and return the module class instance for `name`.

    If the registry attribute is a function (callable), the callable is returned
    directly (not invoked). If it is a class, an instance is created and cached.

    Args:
        name: CLI module name as defined in MODULE_MAP.
        use_cache: If True, reuse a previously created instance.

    Raises:
        ModuleRegistryError: if attribute isn't importable or isn't a class/function.
    """
    if use_cache and name in _INSTANCE_CACHE:
        return _INSTANCE_CACHE[name]

    attr = load_module_attr(name)

    # If attribute is a class, instantiate it
    if isinstance(attr, type):
        try:
            instance = attr()
        except Exception as e:
            raise ModuleRegistryError(
                f"Failed to instantiate module class for '{name}': {e}"
            ) from e

        if use_cache:
            _INSTANCE_CACHE[name] = instance
        return instance

    # If attribute is a callable function (like custom), return it
    if callable(attr):
        return attr

    # Unknown attribute type
    raise ModuleRegistryError(f"Loaded attribute for '{name}' is not class/function")


def get_module_metadata(name: str) -> Dict[str, Any]:
    """
    Return metadata for a module: full_name, description, options.

    This function imports the module (lazily) and attempts to read attributes
    from the class instance (or from the module if the attribute is a function).

    Returns a dict with keys: 'full_name', 'description', 'options'.
    If metadata cannot be discovered, sensible defaults are returned.
    """
    meta = {
        "full_name": name,
        "description": "No description available.",
        "options": "",
    }

    try:
        attr = load_module_attr(name)
    except ModuleRegistryError:
        return meta

    if isinstance(attr, type):
        # It's a class - create a temporary instance (don't cache here)
        try:
            inst = attr()
            meta["full_name"] = getattr(inst, "full_name", getattr(inst, "name", name))
            meta["description"] = getattr(inst, "description", meta["description"])
            meta["options"] = getattr(inst, "options", meta["options"])
            return meta
        except Exception as e:
            # Log the exception for debugging if instantiation fails
            print(f"[netsploit] Warning: Failed to instantiate module '{name}': {e}")
            # Fall back to module-level metadata if instantiation fails
            pass

    # If it's a function or class instantiation failed, try reading module-level vars
    module_path, _ = MODULE_MAP[name]
    try:
        mod = _import_module(module_path)
        meta["full_name"] = getattr(mod, "FULL_NAME", meta["full_name"])
        meta["description"] = (
            getattr(mod, "__doc__", meta["description"]) or meta["description"]
        )
        meta["options"] = getattr(mod, "OPTIONS", meta["options"])
    except ModuleRegistryError:
        pass

    return meta


def run_module(name: str, *, call_main: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Run the specified module.

    Behavior:
      - If the registry attribute is a class, instantiate it (or reuse cached instance)
        and then call `main()` if present; otherwise call `run()` if present.
      - If the attribute is a function (callable), call it directly.

    Returns:
      (success: bool, error_message: Optional[str])
    """
    try:
        attr = load_module_attr(name)
    except ModuleRegistryError as e:
        return False, str(e)

    # If it's a class, get/create instance
    if isinstance(attr, type):
        try:
            inst = get_module_instance(name)
        except ModuleRegistryError as e:
            return False, str(e)

        # Prefer main, then run
        if hasattr(inst, "main") and callable(getattr(inst, "main")):
            try:
                inst.main()
                return True, None
            except Exception as e:
                return False, f"Error while running main() of '{name}': {e}"
        if hasattr(inst, "run") and callable(getattr(inst, "run")):
            try:
                inst.run()
                return True, None
            except Exception as e:
                return False, f"Error while running run() of '{name}': {e}"

        return False, f"Module '{name}' has no callable main() or run()"

    # If it's a callable function (like custom)
    if callable(attr):
        try:
            attr()
            return True, None
        except Exception as e:
            return False, f"Error while executing function for '{name}': {e}"

    return False, f"Attribute for '{name}' is not runnable"


def clear_caches() -> None:
    """Clear internal caches (imports, attrs, instances). Useful for testing or reloads."""
    _LOADED_MODULES.clear()
    _LOADED_ATTRS.clear()
    _INSTANCE_CACHE.clear()
