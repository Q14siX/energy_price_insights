"""Preserve stable entity ID prefixes, including those from legacy setups."""
from __future__ import annotations

from homeassistant.util import slugify
from .const import SOURCE_TIBBER


def entity_slug(entry, provider: str, home: str, homes: list[str]) -> str:
    """Retain legacy name-based IDs; new setups use source-derived IDs.

    Home Assistant handles new device naming at the end of the setup flow.
    Existing entity registry entries are not renamed by this helper.
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
