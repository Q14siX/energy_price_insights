"""Register a self-hosted Lovelace card exactly once across integration entries.

Storage dashboards get one JS module resource. YAML-resource dashboards cannot be
written through Home Assistant's resource collection and receive a frontend
module injection instead. Both paths check for an existing resource first.
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from urllib.parse import urlsplit

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)
CARD_URL = "/energy_price_insights/energy-price-insights-card.js"
_CARD_FILENAME = "energy-price-insights-card.js"
_REGISTRY_KEY = "energy_price_insights_lovelace_card"


def _is_same_card(url: str) -> bool:
    """Compare stable physical paths, ignoring old query-string cache busters."""
    return urlsplit(url).path.rstrip("/").endswith("/" + _CARD_FILENAME)


async def async_register_dashboard_card(hass: HomeAssistant) -> None:
    """Serve bundled JS and register the module with at-most-one resource entry."""
    state = hass.data.setdefault(_REGISTRY_KEY, {"static": False, "registered": False, "lock": asyncio.Lock()})
    async with state["lock"]:
        if state["registered"]:
            return
        if not state["static"]:
            js_path = Path(__file__).parent / "frontend" / _CARD_FILENAME
            await hass.http.async_register_static_paths(
                [StaticPathConfig(CARD_URL, str(js_path), False)]
            )
            state["static"] = True

        from homeassistant.components.lovelace import LOVELACE_DATA, MODE_STORAGE
        lovelace = hass.data.get(LOVELACE_DATA)
        if lovelace is None:
            # Never create arbitrary .storage files: Lovelace may still be starting.
            # Retry when the remaining startup integrations are ready. The static
            # path is already registered, so it must not be registered again.
            from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
            from homeassistant.core import callback
            if not state.get("retry_on_start"):
                state["retry_on_start"] = True
                @callback
                def _retry(_event):
                    hass.async_create_task(async_register_dashboard_card(hass))
                hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _retry)
            return

        collection = lovelace.resources
        if lovelace.resource_mode == MODE_STORAGE:
            # async_get_info ensures the storage collection has been loaded first.
            await collection.async_get_info()
            existing = collection.async_items() or []
            if any(_is_same_card(str(item.get("url", ""))) for item in existing):
                state["registered"] = True
                return
            await collection.async_create_item({"url": CARD_URL, "res_type": "module"})
            state["registered"] = True
            _LOGGER.info("Added Energy Price Insights dashboard module resource")
            return

        # Lovelace YAML mode: resources are read-only from Home Assistant's API.
        if any(_is_same_card(str(item.get("url", ""))) for item in collection.async_items() or []):
            state["registered"] = True
            return
        from homeassistant.components.frontend import add_extra_js_url
        add_extra_js_url(hass, CARD_URL)
        state["registered"] = True
        _LOGGER.info("Loaded Energy Price Insights dashboard module for YAML dashboards")
