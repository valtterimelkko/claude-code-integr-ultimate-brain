"""User-local configuration for the Ultimate Brain Notion scripts."""

from __future__ import annotations

import os
from pathlib import Path

LEGACY_CONFIG_PATH = Path("/etc/keep-to-notion/env.conf")


def config_path() -> Path:
    """Return the configured user-local path, without reading credentials."""
    explicit = os.environ.get("NOTION_CONFIG_FILE")
    if explicit:
        return Path(explicit).expanduser()
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return config_home / "ultimate-brain-notion" / "env.conf"


def candidate_paths() -> list[Path]:
    """Return the new path followed by the legacy path for migration support."""
    paths = [config_path()]
    if LEGACY_CONFIG_PATH not in paths:
        paths.append(LEGACY_CONFIG_PATH)
    return paths


def existing_config_path() -> Path:
    """Return the active config path, including the legacy fallback."""
    return next((path for path in candidate_paths() if path.is_file()), config_path())


def load_config() -> dict[str, str]:
    """Read simple KEY=value configuration without executing shell code."""
    selected = existing_config_path()
    if not selected.is_file():
        return {}

    values: dict[str, str] = {}
    for raw_line in selected.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key:
            values[key] = value.strip()
    return values
