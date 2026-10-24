"""Whether a low-price period is currently active."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import PriceInsightsRuntimeData
from .entity import PriceInsightsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PriceInsightsRuntimeData],
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(FavorableNowBinarySensor(coordinator, home) for home in coordinator.home_keys)


class FavorableNowBinarySensor(PriceInsightsEntity, BinarySensorEntity):
    _attr_translation_key = "favorable_now"
    _attr_icon = "mdi:cash-check"

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_favorable_now"
        self.entity_id = f"binary_sensor.epi_{self._home_slug}_favorable_now"

    @property
    def available(self):
        return bool(self.coordinator.slots(self.home)) and (
            self.coordinator.evaluation_mode(self.home) == "window"
            or self.coordinator.current_price(self.home) is not None
        )

    @property
    def is_on(self):
        return self.coordinator.is_favorable(self.home)
