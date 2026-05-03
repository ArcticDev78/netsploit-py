"""OUI Database Updater

Downloads the latest Wireshark OUI/manuf database when the local copy is
stale (older than Config.OUI_MAX_AGE_DAYS days).

Called automatically during startup; failures are non-fatal — netsploit
continues with whatever copy is already on disk.
"""

import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from utils.colors import green, red, yellow
from utils.config import Config

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _file_age_days(path: Path) -> float:
    """Return how many days ago *path* was last modified (mtime)."""
    mtime = path.stat().st_mtime
    age_seconds = time.time() - mtime
    return age_seconds / 86_400  # 86 400 s per day


def _download(url: str, dest: Path, timeout: int = 30) -> None:
    """Stream *url* to *dest*, writing atomically via a temp file."""
    tmp = dest.with_suffix(".tmp")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Netsploit/1.0 (OUI updater)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            tmp.write_bytes(response.read())
        tmp.replace(dest)  # atomic on POSIX
    except Exception:
        tmp.unlink(missing_ok=True)  # clean up on failure
        raise


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def check_and_update_oui(*, verbose: bool = True, silent_if_fresh: bool = True) -> bool:
    """Check whether the local OUI database is stale and refresh if needed.

    Parameters
    ----------
    verbose:
        When *True* (default) print a one-line status message to stdout.
    silent_if_fresh:
        When *True* (default) suppress the "up to date" message so startup
        output stays clean.  Set to *False* (e.g. inside the oui-lookup
        module) to always show the current status.

    Returns
    -------
    bool
        *True* if the file was successfully refreshed, *False* if it was
        already fresh or if the update attempt failed.
    """
    dest: Path = Config.OUI_FILE_PATH
    url: str = Config.OUI_SOURCE_URL
    max_age: int = Config.OUI_MAX_AGE_DAYS

    # ── 1. Does the file exist at all? ──────────────────────────────────────
    if not dest.exists():
        if verbose:
            print(
                yellow(f" [OUI] Database not found, downloading from {url} …", "bold")
            )
    else:
        age = _file_age_days(dest)
        if age < max_age:
            # File is fresh — nothing to do.
            if verbose and not silent_if_fresh:
                last_updated = datetime.fromtimestamp(
                    dest.stat().st_mtime, tz=timezone.utc
                ).strftime("%Y-%m-%d")
                print(
                    green(
                        f" [OUI] Database is up to date "
                        f"(last updated {last_updated}, "
                        f"{age:.0f}d / {max_age}d max age).",
                        "bold",
                    )
                )
            return False
        else:
            if verbose:
                print(
                    yellow(
                        f" [OUI] Database is {age:.0f} days old "
                        f"(threshold: {max_age}d) — refreshing …",
                        "bold",
                    )
                )

    # ── 2. Attempt the download ──────────────────────────────────────────────
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        _download(url, dest)
    except urllib.error.URLError as exc:
        if verbose:
            print(
                red(
                    f" [OUI] Network error while updating database: {exc.reason}",
                    "bold",
                )
            )
        return False
    except OSError as exc:
        if verbose:
            print(red(f" [OUI] Could not write OUI database to {dest}: {exc}", "bold"))
        return False
    except Exception as exc:  # noqa: BLE001
        if verbose:
            print(red(f" [OUI] Unexpected error during OUI update: {exc}", "bold"))
        return False

    if verbose:
        print(green(" [OUI] Database updated successfully.", "bold"))
    return True
