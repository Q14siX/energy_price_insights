"""Settings shared by Energy Price Insights and its source adapters."""

DOMAIN = "energy_price_insights"
NAME = "Energy Price Insights"
MANUFACTURER = "Q14siX"
PLATFORMS = ("sensor", "binary_sensor", "number", "select")

CONF_PROVIDER = "provider"
CONF_DISPLAY_NAME = "display_name"
CONF_AREA_ID = "area_id"
CONF_SOURCE_ENTITY = "source_entity"
CONF_TOMORROW_ENTITY = "tomorrow_entity"
CONF_DATA_ATTRIBUTE = "data_attribute"
CONF_START_FIELD = "start_field"
CONF_END_FIELD = "end_field"
CONF_PRICE_FIELD = "price_field"
CONF_PRICE_UNIT = "price_unit"
CONF_THRESHOLD = "default_threshold_percent"
CONF_THRESHOLDS = "thresholds"
CONF_MODE = "price_evaluation_mode"
CONF_WINDOW_MINUTES = "window_minutes"
CONF_MODES = "modes"
CONF_WINDOWS = "windows"
CONF_WINDOW_SCOPE = "window_search_scope"
CONF_WINDOW_SCOPES = "window_scopes"
SCOPE_FUTURE = "future"
SCOPE_ACTIVE = "active_future"
WINDOW_SCOPES = (SCOPE_FUTURE, SCOPE_ACTIVE)
DEFAULT_WINDOW_SCOPE = SCOPE_FUTURE
MODE_THRESHOLD = "threshold"
MODE_WINDOW = "window"
MODES = (MODE_THRESHOLD, MODE_WINDOW)
DEFAULT_MODE = MODE_THRESHOLD
DEFAULT_WINDOW_MINUTES = 60
MIN_WINDOW_MINUTES = 1
MAX_WINDOW_MINUTES = 1440

SOURCE_TIBBER = "tibber"
SOURCE_EPEX = "epex"
SOURCE_OCTOPUS = "octopus"
SOURCE_GENERIC = "generic"
PROVIDERS = (SOURCE_TIBBER, SOURCE_EPEX, SOURCE_OCTOPUS, SOURCE_GENERIC)
PROVIDER_NAMES = {
    SOURCE_TIBBER: "Tibber",
    SOURCE_EPEX: "EPEX Spot",
    SOURCE_OCTOPUS: "Octopus Energy",
    SOURCE_GENERIC: "Energy Price Insights",
}

PRICE_UNITS = (
    "auto", "eur_kwh", "cent_kwh", "eur_mwh",
    "gbp_kwh", "pence_kwh", "gbp_mwh",
    "sek_kwh", "ore_sek_kwh", "nok_kwh", "ore_nok_kwh",
    "dkk_kwh", "ore_dkk_kwh", "pln_kwh", "pln_mwh",
)

DEFAULT_THRESHOLD = 20.0
STORAGE_VERSION = 2
VERSION = "20261025.001622"
