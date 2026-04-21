"""
Safe ANSI color utilities for NetSploit.

This module provides simple, dependency-free helpers for coloring console
output using ANSI escape sequences. It intentionally does NOT require any
third-party package. If colored output is disabled (via the NO_COLOR env var
or via `set_enabled(False)`), these functions return the original text.

Supported color functions:
- blue(text, style=None)
- green(text, style=None)
- yellow(text, style=None)
- cyan(text, style=None)
- red(text, style=None)

The optional `style` parameter accepts a string or list of strings. Supported
style names (case-insensitive): "bold", "underline" (or "underlined"),
"italic", "invert".

Example usages:
    blue('hello', 'bold')
    yellow('warning', ['bold', 'underline'])

This file intentionally keeps the API simple and deterministic.
"""

from __future__ import annotations

import os
from typing import Any

# Default: enable colors unless NO_COLOR is set in the environment
_ENABLED: bool = "NO_COLOR" not in os.environ

# ANSI codes
_COLOR_CODES = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

_STYLE_CODES = {
    "reset": 0,
    "bold": 1,
    "dim": 2,
    "italic": 3,
    "underline": 4,
    "underlined": 4,
    "blink": 5,
    "invert": 7,
    "hidden": 8,
}


def set_enabled(enabled: bool) -> None:
    """Globally enable or disable colored output."""
    global _ENABLED
    _ENABLED = bool(enabled)


def is_enabled() -> bool:
    """Return whether colored output is currently enabled."""
    return _ENABLED


def _normalize_styles(style: Any) -> list[str]:
    """Turn the style argument into a list of normalized style names."""
    if not style:
        return []
    if isinstance(style, (list, tuple)):
        parts = []
        for s in style:
            if s is None:
                continue
            parts.append(str(s).lower())
        return parts
    return [str(style).lower()]


def _wrap(text: str, color: str | None = None, style: Any = None) -> str:
    """Wrap text with ANSI escape sequences for color and styles.

    If colors are disabled, returns `text` unchanged.
    """
    if not _ENABLED:
        return text

    codes: list[str] = []

    # styles first
    for s in _normalize_styles(style):
        code = _STYLE_CODES.get(s)
        if code is not None:
            codes.append(str(code))

    # then color
    if color:
        color_code = _COLOR_CODES.get(color.lower())
        if color_code is not None:
            codes.append(str(color_code))

    if not codes:
        return text

    prefix = "\033[" + ";".join(codes) + "m"
    suffix = "\033[0m"
    return f"{prefix}{text}{suffix}"


def blue(text: str, style: Any = None) -> str:
    """Return `text` colored blue (if enabled)."""
    return _wrap(text, "blue", style)


def green(text: str, style: Any = None) -> str:
    """Return `text` colored green (if enabled)."""
    return _wrap(text, "green", style)


def yellow(text: str, style: Any = None) -> str:
    """Return `text` colored yellow (if enabled)."""
    return _wrap(text, "yellow", style)


def cyan(text: str, style: Any = None) -> str:
    """Return `text` colored cyan (if enabled)."""
    return _wrap(text, "cyan", style)


def red(text: str, style: Any = None) -> str:
    """Return `text` colored red (if enabled)."""
    return _wrap(text, "red", style)


__all__ = [
    "blue",
    "green",
    "yellow",
    "cyan",
    "red",
    "set_enabled",
    "is_enabled",
]
