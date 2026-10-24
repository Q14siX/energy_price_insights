"""Price-only virtual devices used for all providers."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN, MANUFACTURER, SOURCE_TIBBER
from .identity import entity_slug
from .coordinator import PriceInsightsCoordinator


class PriceInsightsEntity(CoordinatorEntity[PriceInsightsCoordinator]):
    _attr_has_entity_name = True

    def __init__(self, coordinator: PriceInsightsCoordinator, home: str) -> None:
        super().__init__(coordinator)
        self.home = home
        # Keep previous Tibber IDs stable when upgrading from 20261024.112249.
        self._home_slug = entity_slug(
            coordinator.entry, coordinator.provider, home, coordinator.home_keys,
        )
        # Hardware-independent stable identifiers survive changes to the name.
        if coordinator.provider == SOURCE_TIBBER:
            self._device_identifier = f"{coordinator.entry.entry_id}_{slugify(home)}"
        else:
            self._device_identifier = coordinator.entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_identifier)},
            "name": self.coordinator.device_name(self.home),
            "manufacturer": MANUFACTURER,
            "model": "Energy Price Insights",
        }

    @property
    def available(self) -> bool:
        # Cached forecasts remain readable during transient provider outages.
        # Config entities override this to remain editable even without forecasts.
        return bool(self.coordinator.slots(self.home))
