"""Editable, per-home favorable threshold as a Home Assistant number entity."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import MIN_WINDOW_MINUTES, MAX_WINDOW_MINUTES
from .coordinator import PriceInsightsRuntimeData
from .entity import PriceInsightsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PriceInsightsRuntimeData],
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        item for home in coordinator.home_keys for item in (
            FavorableThresholdNumber(coordinator, home),
            CheapestWindowMinutesNumber(coordinator, home),
        )
    )


class FavorableThresholdNumber(PriceInsightsEntity, NumberEntity):
    _attr_translation_key = "favorable_threshold"
    _attr_icon = "mdi:percent"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = 0.0
    _attr_native_max_value = 100.0
    _attr_native_step = 0.01
    _attr_native_unit_of_measurement = "%"
    _attr_suggested_display_precision = 2

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_threshold_v2"
        self.entity_id = f"number.epi_{self._home_slug}_favorable_threshold"

    @property
    def available(self):
        return True

    @property
    def native_value(self):
        return self.coordinator.threshold(self.home)

    @property
    def extra_state_attributes(self):
        return self.coordinator.threshold_attrs(self.home)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_threshold(self.home, value)


class CheapestWindowMinutesNumber(PriceInsightsEntity, NumberEntity):
    """Editable duration of the cheapest continuous electricity-price interval."""

    _attr_translation_key = "window_minutes"
    _attr_icon = "mdi:timer-outline"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_mode = NumberMode.BOX
    _attr_native_min_value = MIN_WINDOW_MINUTES
    _attr_native_max_value = MAX_WINDOW_MINUTES
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "min"
    _attr_suggested_display_precision = 0

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_window_minutes"
        self.entity_id = f"number.epi_{self._home_slug}_window_minutes"

    @property
    def available(self):
        return True

    @property
    def native_value(self):
        return self.coordinator.window_minutes(self.home)

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_window_minutes(self.home, value)
