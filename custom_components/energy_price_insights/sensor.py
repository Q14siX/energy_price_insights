"""Current price, favorable period and daily forecast sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import PriceInsightsRuntimeData
from .entity import PriceInsightsEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry[PriceInsightsRuntimeData], async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        item for home in coordinator.home_keys for item in (
            CurrentPriceSensor(coordinator, home),
            FavorablePhaseSensor(coordinator, home),
            DailyForecastSensor(coordinator, home, 0),
            DailyForecastSensor(coordinator, home, 1),
            PriceAvailabilitySensor(coordinator, home),
        )
    )


class PriceValueSensor(PriceInsightsEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 4

    @property
    def native_unit_of_measurement(self):
        currency = self.coordinator.currency
        prefix = {"EUR": "€", "GBP": "£"}.get(currency, currency)
        return f"{prefix}/kWh"


class CurrentPriceSensor(PriceValueSensor):
    _attr_translation_key = "current_price"
    _attr_icon = "mdi:currency-eur"

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_current_price"
        self.entity_id = f"sensor.epi_{self._home_slug}_current_price"

    @property
    def available(self):
        # A forecast can exist before/after the active tariff is published.
        # In that case a missing current price is unknown, not unavailable.
        return bool(self.coordinator.slots(self.home))

    @property
    def native_value(self):
        return self.coordinator.current_price(self.home)

    @property
    def extra_state_attributes(self):
        return self.coordinator.price_attrs(self.home)


class FavorablePhaseSensor(PriceInsightsEntity, SensorEntity):
    _attr_translation_key = "favorable_phase"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:clock-check-outline"

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_next_favorable_start"
        self.entity_id = f"sensor.epi_{self._home_slug}_favorable_phase"

    @property
    def native_value(self):
        return self.coordinator.phase_start(self.home)

    @property
    def extra_state_attributes(self):
        return self.coordinator.phase_attrs(self.home)


class DailyForecastSensor(PriceValueSensor):
    _attr_icon = "mdi:chart-line"

    def __init__(self, coordinator, home, offset: int):
        super().__init__(coordinator, home)
        self.offset = offset
        suffix = "today" if offset == 0 else "tomorrow"
        self._attr_translation_key = f"forecast_{suffix}"
        self._attr_unique_id = f"{self._device_identifier}_forecast_{suffix}"
        self.entity_id = f"sensor.epi_{self._home_slug}_forecast_{suffix}"

    @property
    def available(self):
        # Tomorrow may not be published yet. Show unknown until it is,
        # rather than wrongly implying that the source integration failed.
        return bool(self.coordinator.slots(self.home))

    @property
    def native_value(self):
        return self.coordinator.day_average(self.home, self.offset)

    @property
    def extra_state_attributes(self):
        return self.coordinator.day_attrs(self.home, self.offset)


class PriceAvailabilitySensor(PriceInsightsEntity, SensorEntity):
    """Explain why a price entity or complete duration may not be available."""

    _attr_translation_key = "price_availability"
    _attr_icon = "mdi:information-outline"
    _attr_entity_category = None

    def __init__(self, coordinator, home):
        super().__init__(coordinator, home)
        self._attr_unique_id = f"{self._device_identifier}_price_availability"
        self.entity_id = f"sensor.epi_{self._home_slug}_price_availability"

    @property
    def available(self):
        return True

    @property
    def native_value(self):
        return self.coordinator.availability_snapshot(self.home)["status"]

    @property
    def extra_state_attributes(self):
        return {key: value for key, value in self.coordinator.availability_snapshot(self.home).items()
                if key != "status"}
