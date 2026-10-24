"""Stable entity ID prefixes chosen only during initial setup."""
from __future__ import annotations

from homeassistant.util import slugify
from .const import SOURCE_TIBBER


def entity_slug(entry, provider: str, home: str, homes: list[str]) -> str:
    """Base entity IDs on the initial name, never rename existing registry entries.

    Existing installations without a user-selected name retain their old IDs.
    """
    initial_name = entry.data.get("display_name")
    if initial_name:
        base = slugify(initial_name)
        if provider == SOURCE_TIBBER and len(homes) > 1:
            return f"{base}_{slugify(home)}"
        return base
    if provider == SOURCE_TIBBER:
        return slugify(home)
    return f"{slugify(entry.title)}_{entry.entry_id[:6]}"
