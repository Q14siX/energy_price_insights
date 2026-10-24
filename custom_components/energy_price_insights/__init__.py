"""Energy Price Insights Home Assistant integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change
from homeassistant.helpers import device_registry as dr
from homeassistant.util import slugify

from .const import PLATFORMS, SOURCE_TIBBER, DOMAIN, CONF_AREA_ID
from .coordinator import PriceInsightsCoordinator, PriceInsightsRuntimeData
from .dashboard import async_register_dashboard_card
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry[PriceInsightsRuntimeData]) -> bool:
    coordinator = PriceInsightsCoordinator(hass, entry)
    await coordinator.async_initialize()
    await coordinator.async_refresh()

    if coordinator.provider == SOURCE_TIBBER and not coordinator.home_keys:
        raise ConfigEntryNotReady("Tibber provided no homes or cached price data")

    entry.runtime_data = PriceInsightsRuntimeData(coordinator)

    @callback
    def clock_tick(now):
        # A freely chosen minute window can begin/end away from 15-minute boundaries.
        # Refresh state every minute, but request new provider data only each quarter hour.
        coordinator.async_update_listeners()
        if now.minute % 15 == 0:
            hass.async_create_task(coordinator.async_refresh())

    entry.async_on_unload(async_track_time_change(
        hass, clock_tick, minute=list(range(60)), second=0,
    ))

    watched = coordinator.source_entity_ids()
    if watched:
        @callback
        def source_updated(_event):
            hass.async_create_task(coordinator.async_refresh())
        entry.async_on_unload(async_track_state_change_event(hass, watched, source_updated))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    try:
        await async_register_dashboard_card(hass)
    except (RuntimeError, ValueError, OSError) as exc:
        # Price evaluation must still work if the dashboard is not available.
        _LOGGER.warning("Could not register dashboard card resource: %s", exc)
    _apply_device_area(hass, entry, coordinator)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry[PriceInsightsRuntimeData]) -> bool:
    success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if success:
        entry.async_unload()
    return success


@callback
def _apply_device_area(hass: HomeAssistant, entry: ConfigEntry, coordinator: PriceInsightsCoordinator) -> None:
    """Assign Home Assistant area to each virtual price device, not source devices."""
    if CONF_AREA_ID not in coordinator.config:
        return  # Keep existing room assignments of legacy installations.
    area = coordinator.config.get(CONF_AREA_ID) or None
    registry = dr.async_get(hass)
    for home in coordinator.home_keys:
        identifier = (f"{entry.entry_id}_{slugify(home)}"
                      if coordinator.provider == SOURCE_TIBBER else entry.entry_id)
        device = registry.async_get_device_by_identifier(
            (DOMAIN, identifier), entry.entry_id
        )
        if device is not None and device.area_id != area:
            registry.async_update_device(device.id, area_id=area)
