"""Choose the price evaluation method without reconfiguring the price source."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import MODES, MODE_THRESHOLD, MODE_WINDOW, WINDOW_SCOPES
from .coordinator import PriceInsightsRuntimeData
from .entity import PriceInsightsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry[PriceInsightsRuntimeData],
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(item for home in coordinator.home_keys for item in (
        PriceEvaluationModeSelect(coordinator, home), WindowSearchScopeSelect(coordinator, home),
    ))


class PriceEvaluationModeSelect(PriceInsightsEntity, SelectEntity):
    _attr_translation_key = "price_evaluation_mode"
    _attr_icon = "mdi:chart-timeline-variant"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = list(MODES)

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_price_evaluation_mode"
        self.entity_id = f"select.epi_{self._home_slug}_price_evaluation_mode"

    @property
    def available(self):
        return True

    @property
    def current_option(self):
        return self.coordinator.evaluation_mode(self.home)

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_set_evaluation_mode(self.home, option)


class WindowSearchScopeSelect(PriceInsightsEntity, SelectEntity):
    _attr_translation_key = "window_search_scope"
    _attr_icon = "mdi:calendar-clock"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = list(WINDOW_SCOPES)

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_window_search_scope"
        self.entity_id = f"select.epi_{self._home_slug}_window_search_scope"

    @property
    def available(self):
        return True

    @property
    def current_option(self):
        return self.coordinator.window_scope(self.home)

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_set_window_scope(self.home, option)
