"""Set up electricity price sources with focused, mode-dependent option forms."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.util import slugify
from homeassistant.helpers.selector import (
    EntitySelector, EntitySelectorConfig,
    NumberSelector, NumberSelectorConfig, NumberSelectorMode,
    SelectSelector, SelectSelectorConfig, SelectSelectorMode,
    TextSelector, TextSelectorConfig, AreaSelector, AreaSelectorConfig,
)

from .const import (
    CONF_DATA_ATTRIBUTE, CONF_END_FIELD, CONF_PRICE_FIELD, CONF_PRICE_UNIT,
    CONF_PROVIDER, CONF_SOURCE_ENTITY, CONF_START_FIELD, CONF_THRESHOLD,
    CONF_THRESHOLDS, CONF_TOMORROW_ENTITY, DEFAULT_THRESHOLD, DOMAIN,
    PRICE_UNITS, PROVIDERS, PROVIDER_NAMES, SOURCE_EPEX, SOURCE_GENERIC,
    SOURCE_OCTOPUS, SOURCE_TIBBER,
    CONF_MODE, CONF_WINDOW_MINUTES, DEFAULT_MODE, DEFAULT_WINDOW_MINUTES,
    MODE_THRESHOLD, MODE_WINDOW, MIN_WINDOW_MINUTES, MAX_WINDOW_MINUTES,
    CONF_WINDOW_SCOPE, WINDOW_SCOPES, DEFAULT_WINDOW_SCOPE,
    CONF_DISPLAY_NAME, CONF_AREA_ID,
)


def identity_schema(defaults: dict[str, Any], fallback_name: str) -> vol.Schema:
    """Provide an initial name and optional area; the name never changes later."""
    fields: dict[Any, Any] = {
        vol.Required(CONF_DISPLAY_NAME, default=defaults.get(CONF_DISPLAY_NAME) or fallback_name):
            TextSelector(TextSelectorConfig()),
    }
    chosen_area = defaults.get(CONF_AREA_ID)
    if chosen_area:
        fields[vol.Optional(CONF_AREA_ID, description={"suggested_value": chosen_area})] = AreaSelector(AreaSelectorConfig())
    else:
        fields[vol.Optional(CONF_AREA_ID)] = AreaSelector(AreaSelectorConfig())
    return vol.Schema(fields)


def area_schema(defaults: dict[str, Any]) -> vol.Schema:
    """In the options flow only the room can be changed."""
    selected = defaults.get(CONF_AREA_ID)
    if selected:
        return vol.Schema({vol.Optional(CONF_AREA_ID, description={"suggested_value": selected}): AreaSelector(AreaSelectorConfig())})
    return vol.Schema({vol.Optional(CONF_AREA_ID): AreaSelector(AreaSelectorConfig())})


def valid_display_name(value: Any) -> bool:
    return isinstance(value, str) and 0 < len(value.strip()) <= 80 and bool(slugify(value.strip()))


def threshold_selector():
    return NumberSelector(NumberSelectorConfig(
        min=0, max=100, step=0.01,
        mode=NumberSelectorMode.BOX, unit_of_measurement="%",
    ))


def mode_selector():
    return SelectSelector(SelectSelectorConfig(
        options=[MODE_THRESHOLD, MODE_WINDOW],
        translation_key="evaluation_mode",
        mode=SelectSelectorMode.DROPDOWN,
    ))


def duration_selector():
    return NumberSelector(NumberSelectorConfig(
        min=MIN_WINDOW_MINUTES, max=MAX_WINDOW_MINUTES, step=1,
        mode=NumberSelectorMode.BOX, unit_of_measurement="min",
    ))


def scope_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema({
        vol.Required(CONF_WINDOW_SCOPE, default=defaults.get(CONF_WINDOW_SCOPE, DEFAULT_WINDOW_SCOPE)):
            SelectSelector(SelectSelectorConfig(
                options=list(WINDOW_SCOPES), translation_key="window_search_scope",
                mode=SelectSelectorMode.DROPDOWN,
            )),
    })


def provider_schema():
    return vol.Schema({
        vol.Required(CONF_PROVIDER, default=SOURCE_TIBBER): SelectSelector(
            SelectSelectorConfig(
                options=list(PROVIDERS),
                translation_key="price_provider",
                mode=SelectSelectorMode.DROPDOWN,
            )
        )
    })


def price_unit_selector():
    return SelectSelector(SelectSelectorConfig(
        options=list(PRICE_UNITS),
        translation_key="price_unit",
        mode=SelectSelectorMode.DROPDOWN,
    ))


def source_schema(provider: str, defaults: dict[str, Any]) -> vol.Schema:
    """Only show the entity/unit fields for non-Tibber price sources."""
    schema: dict[Any, Any] = {}
    if provider != SOURCE_TIBBER:
        domains = ["event"] if provider == SOURCE_OCTOPUS else ["sensor", "event"]
        entity = EntitySelector(EntitySelectorConfig(domain=domains))
        current = defaults.get(CONF_SOURCE_ENTITY)
        schema[vol.Required(CONF_SOURCE_ENTITY, default=current) if current else vol.Required(CONF_SOURCE_ENTITY)] = entity
        tomorrow = defaults.get(CONF_TOMORROW_ENTITY)
        schema[vol.Optional(CONF_TOMORROW_ENTITY, description={"suggested_value": tomorrow}) if tomorrow else vol.Optional(CONF_TOMORROW_ENTITY)] = entity
        if provider in (SOURCE_EPEX, SOURCE_GENERIC):
            schema[vol.Required(CONF_PRICE_UNIT, default=defaults.get(CONF_PRICE_UNIT, "auto"))] = price_unit_selector()
    return vol.Schema(schema)


def evaluation_schema(defaults: dict[str, Any]) -> vol.Schema:
    """First ask which evaluation should be used."""
    return vol.Schema({
        vol.Required(CONF_MODE, default=defaults.get(CONF_MODE, DEFAULT_MODE)): mode_selector(),
    })


def setting_schema(mode: str, defaults: dict[str, Any]) -> vol.Schema:
    """Show exactly one applicable parameter, never both."""
    if mode == MODE_WINDOW:
        return vol.Schema({
            vol.Required(CONF_WINDOW_MINUTES, default=int(defaults.get(CONF_WINDOW_MINUTES, DEFAULT_WINDOW_MINUTES))): duration_selector(),
        })
    return vol.Schema({
        vol.Required(CONF_THRESHOLD, default=round(float(defaults.get(CONF_THRESHOLD, DEFAULT_THRESHOLD)), 2)): threshold_selector(),
    })


def advanced_schema(defaults: dict[str, Any]) -> vol.Schema:
    return vol.Schema({
        vol.Required(key, default=defaults.get(key, "auto")): str
        for key in (CONF_DATA_ATTRIBUTE, CONF_START_FIELD, CONF_END_FIELD, CONF_PRICE_FIELD)
    })


def inherited_tibber_threshold(hass) -> tuple[float, dict[str, Any]]:
    originals = hass.config_entries.async_entries("energy_storage_control")
    original = originals[0] if originals else None
    if not original:
        return DEFAULT_THRESHOLD, {}
    value = original.options.get(CONF_THRESHOLD, original.data.get(CONF_THRESHOLD, DEFAULT_THRESHOLD))
    per_home = original.options.get(CONF_THRESHOLDS, {})
    try:
        amount = float(value)
    except (TypeError, ValueError):
        amount = DEFAULT_THRESHOLD
    return amount, dict(per_home) if isinstance(per_home, dict) else {}


def _valid_setting(value: Any, mode: str) -> float | int | None:
    """Validate even when called outside a normal HA selector form."""
    try:
        number = float(value)
        if mode == MODE_WINDOW:
            if not number.is_integer() or not MIN_WINDOW_MINUTES <= number <= MAX_WINDOW_MINUTES:
                return None
            return int(number)
        if not 0 <= number <= 100:
            return None
        return round(number, 2)
    except (TypeError, ValueError, OverflowError):
        return None


class PriceInsightsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Each price source gets its own config entry and evaluation settings."""

    VERSION = 1

    def __init__(self):
        self._data: dict[str, Any] = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=provider_schema())
        self._data[CONF_PROVIDER] = user_input[CONF_PROVIDER]
        return await self.async_step_identity()

    async def async_step_identity(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            provider = self._data[CONF_PROVIDER]
            return self.async_show_form(
                step_id="identity", data_schema=identity_schema(self._data, PROVIDER_NAMES[provider]),
            )
        if not valid_display_name(user_input.get(CONF_DISPLAY_NAME)):
            return self.async_show_form(
                step_id="identity",
                data_schema=identity_schema(self._data, PROVIDER_NAMES[self._data[CONF_PROVIDER]]),
                errors={CONF_DISPLAY_NAME: "invalid_display_name"},
            )
        self._data[CONF_DISPLAY_NAME] = user_input[CONF_DISPLAY_NAME].strip()
        self._data[CONF_AREA_ID] = user_input.get(CONF_AREA_ID, "")
        if self._data[CONF_PROVIDER] == SOURCE_TIBBER:
            threshold, per_home = inherited_tibber_threshold(self.hass)
            self._data[CONF_THRESHOLD] = threshold
            if per_home:
                self._data[CONF_THRESHOLDS] = per_home
            return await self.async_step_evaluation_method()
        return await self.async_step_source_settings()

    async def async_step_source_settings(self, user_input: dict[str, Any] | None = None):
        provider = self._data[CONF_PROVIDER]
        if user_input is None:
            return self.async_show_form(step_id="source_settings", data_schema=source_schema(provider, self._data))
        self._data.update(user_input)
        if self.hass.states.get(self._data[CONF_SOURCE_ENTITY]) is None:
            return self.async_show_form(
                step_id="source_settings", data_schema=source_schema(provider, self._data),
                errors={CONF_SOURCE_ENTITY: "invalid_source"},
            )
        return await self.async_step_evaluation_method()

    async def async_step_evaluation_method(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="evaluation_method", data_schema=evaluation_schema(self._data))
        self._data[CONF_MODE] = user_input[CONF_MODE]
        return await (self.async_step_window_settings() if self._data[CONF_MODE] == MODE_WINDOW
                      else self.async_step_threshold_settings())

    async def async_step_threshold_settings(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="threshold_settings", data_schema=setting_schema(MODE_THRESHOLD, self._data))
        threshold = _valid_setting(user_input.get(CONF_THRESHOLD), MODE_THRESHOLD)
        if threshold is None:
            return self.async_show_form(step_id="threshold_settings", data_schema=setting_schema(MODE_THRESHOLD, self._data), errors={CONF_THRESHOLD: "invalid_threshold"})
        self._data[CONF_THRESHOLD] = threshold
        return await self.async_step_window_scope()

    async def async_step_window_settings(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="window_settings", data_schema=setting_schema(MODE_WINDOW, self._data))
        minutes = _valid_setting(user_input.get(CONF_WINDOW_MINUTES), MODE_WINDOW)
        if minutes is None:
            return self.async_show_form(step_id="window_settings", data_schema=setting_schema(MODE_WINDOW, self._data), errors={CONF_WINDOW_MINUTES: "invalid_duration"})
        self._data[CONF_WINDOW_MINUTES] = minutes
        return await self.async_step_window_scope()

    async def async_step_window_scope(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="window_scope", data_schema=scope_schema(self._data))
        self._data[CONF_WINDOW_SCOPE] = user_input[CONF_WINDOW_SCOPE]
        return await self._finish_settings()

    async def _finish_settings(self):
        if self._data[CONF_PROVIDER] == SOURCE_GENERIC:
            return await self.async_step_field_mapping()
        return await self._finish()

    async def async_step_field_mapping(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="field_mapping", data_schema=advanced_schema(self._data))
        self._data.update(user_input)
        return await self._finish()

    async def _finish(self):
        provider = self._data[CONF_PROVIDER]
        if provider == SOURCE_TIBBER:
            if not self.hass.config_entries.async_entries("tibber"):
                return self.async_abort(reason="source_missing")
            if any(e.data.get(CONF_PROVIDER, SOURCE_TIBBER) == SOURCE_TIBBER
                   for e in self.hass.config_entries.async_entries(DOMAIN)):
                return self.async_abort(reason="already_configured")
            identifier = "tibber:all"
            title = "Tibber"
        else:
            entity_id = self._data[CONF_SOURCE_ENTITY]
            state = self.hass.states.get(entity_id)
            if state is None:
                return self.async_show_form(
                    step_id="source_settings", data_schema=source_schema(provider, self._data),
                    errors={CONF_SOURCE_ENTITY: "invalid_source"},
                )
            identifier = f"{provider}:{entity_id}"
            source_name = state.attributes.get("friendly_name", entity_id)
            title = (f"Energy Price Insights · {source_name}" if provider == SOURCE_GENERIC
                     else f"{PROVIDER_NAMES[provider]} · {source_name}")
        await self.async_set_unique_id(identifier)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=self._data.get(CONF_DISPLAY_NAME, title), data=self._data)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return PriceInsightsOptionsFlow()


class PriceInsightsOptionsFlow(config_entries.OptionsFlowWithReload):
    """Edit source and evaluation settings while retaining the inactive value."""

    def __init__(self):
        self._pending: dict[str, Any] = {}

    def _values(self) -> dict[str, Any]:
        return {**self.config_entry.data, **self.config_entry.options, **self._pending}

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        self._pending = {}
        return await self.async_step_area()

    async def async_step_area(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="area", data_schema=area_schema(self._values()))
        # Explicitly keep only the area here. The initial integration name is immutable.
        self._pending[CONF_AREA_ID] = user_input.get(CONF_AREA_ID, "")
        if self._values().get(CONF_PROVIDER, SOURCE_TIBBER) != SOURCE_TIBBER:
            return await self.async_step_source_settings()
        return await self.async_step_evaluation_method()

    async def async_step_source_settings(self, user_input: dict[str, Any] | None = None):
        values = self._values()
        provider = values.get(CONF_PROVIDER, SOURCE_TIBBER)
        if user_input is None:
            return self.async_show_form(step_id="source_settings", data_schema=source_schema(provider, values))
        self._pending.update(user_input)
        if self.hass.states.get(self._pending[CONF_SOURCE_ENTITY]) is None:
            return self.async_show_form(step_id="source_settings", data_schema=source_schema(provider, self._values()), errors={CONF_SOURCE_ENTITY: "invalid_source"})
        if CONF_TOMORROW_ENTITY not in user_input:
            self._pending[CONF_TOMORROW_ENTITY] = ""
        return await self.async_step_evaluation_method()

    async def async_step_evaluation_method(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="evaluation_method", data_schema=evaluation_schema(self._values()))
        self._pending[CONF_MODE] = user_input[CONF_MODE]
        return await (self.async_step_window_settings() if self._pending[CONF_MODE] == MODE_WINDOW
                      else self.async_step_threshold_settings())

    async def async_step_threshold_settings(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="threshold_settings", data_schema=setting_schema(MODE_THRESHOLD, self._values()))
        threshold = _valid_setting(user_input.get(CONF_THRESHOLD), MODE_THRESHOLD)
        if threshold is None:
            return self.async_show_form(step_id="threshold_settings", data_schema=setting_schema(MODE_THRESHOLD, self._values()), errors={CONF_THRESHOLD: "invalid_threshold"})
        self._pending[CONF_THRESHOLD] = threshold
        return await self.async_step_window_scope()

    async def async_step_window_settings(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="window_settings", data_schema=setting_schema(MODE_WINDOW, self._values()))
        minutes = _valid_setting(user_input.get(CONF_WINDOW_MINUTES), MODE_WINDOW)
        if minutes is None:
            return self.async_show_form(step_id="window_settings", data_schema=setting_schema(MODE_WINDOW, self._values()), errors={CONF_WINDOW_MINUTES: "invalid_duration"})
        self._pending[CONF_WINDOW_MINUTES] = minutes
        return await self.async_step_window_scope()

    async def async_step_window_scope(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="window_scope", data_schema=scope_schema(self._values()))
        self._pending[CONF_WINDOW_SCOPE] = user_input[CONF_WINDOW_SCOPE]
        return await self._finish_settings()

    async def _finish_settings(self):
        if self._values().get(CONF_PROVIDER) == SOURCE_GENERIC:
            return await self.async_step_field_mapping()
        return self._finish()

    async def async_step_field_mapping(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(step_id="field_mapping", data_schema=advanced_schema(self._values()))
        self._pending.update(user_input)
        return self._finish()

    def _finish(self):
        updated = {**self.config_entry.options, **self._pending}
        # The options form configures the entire entry; its values must take
        # precedence over previous per-home changes made through entity controls.
        override_keys = {
            CONF_THRESHOLD: CONF_THRESHOLDS,
            CONF_WINDOW_MINUTES: "windows",
            CONF_MODE: "modes",
            CONF_WINDOW_SCOPE: "window_scopes",
        }
        for changed_key, overrides_key in override_keys.items():
            if changed_key in self._pending and self._values().get(changed_key) is not None:
                current_value = {**self.config_entry.data, **self.config_entry.options}.get(changed_key)
                if current_value != self._pending[changed_key]:
                    updated[overrides_key] = {}

        # The OptionsFlowWithReload applies all changed settings immediately.
        return self.async_create_entry(data=updated)
