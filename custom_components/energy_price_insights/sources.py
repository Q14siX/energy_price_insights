"""Provider-independent conversion of Home Assistant price forecasts.

Supported out of the box: Tibber service, EPEX Spot sensors, Octopus Energy
rate events and other integrations exposing timestamped sensor/event arrays.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import math
import re
from typing import Any

from .const import (
    CONF_DATA_ATTRIBUTE, CONF_END_FIELD, CONF_PRICE_FIELD, CONF_PRICE_UNIT,
    CONF_START_FIELD, SOURCE_EPEX, SOURCE_OCTOPUS, SOURCE_TIBBER,
)

START_KEYS = ("start_time", "start", "startsAt", "starts_at", "from", "datetime", "timestamp", "time", "date")
END_KEYS = ("end_time", "end", "endsAt", "ends_at", "to", "until", "valid_until")
PRICE_KEYS = (
    "price_per_kwh", "value_inc_vat", "total", "price", "value",
    "market_price_per_kwh", "total_price", "value_with_tax", "electricity_price",
    "energy_price", "marketprice", "PriceWithVAT", "price_with_tax", "amount",
)
ARRAY_KEYS = (
    "data", "rates", "prices", "raw_today", "raw_tomorrow", "today", "tomorrow",
    "all_prices", "price_data", "forecast", "values", "prices_today", "prices_tomorrow",
    "today_prices", "tomorrow_prices", "price_forecast",
)
TODAY_KEYS = frozenset(("today", "raw_today", "prices_today", "today_prices"))
TOMORROW_KEYS = frozenset(("tomorrow", "raw_tomorrow", "prices_tomorrow", "tomorrow_prices"))

# Each multiplier normalizes to the major currency unit per kWh.
UNIT_TABLE = {
    "eur_kwh": ("EUR", 1), "cent_kwh": ("EUR", 0.01), "eur_mwh": ("EUR", 0.001),
    "gbp_kwh": ("GBP", 1), "pence_kwh": ("GBP", 0.01), "gbp_mwh": ("GBP", 0.001),
    "sek_kwh": ("SEK", 1), "ore_sek_kwh": ("SEK", 0.01),
    "nok_kwh": ("NOK", 1), "ore_nok_kwh": ("NOK", 0.01),
    "dkk_kwh": ("DKK", 1), "ore_dkk_kwh": ("DKK", 0.01),
    "pln_kwh": ("PLN", 1), "pln_mwh": ("PLN", 0.001),
}


class PriceSourceError(ValueError):
    """Input price series is unusable, missing or contains ambiguous units."""


def unit_from_text(raw: str | None) -> str | None:
    """Interpret common Home Assistant unit labels without guessing currencies."""
    if not raw:
        return None
    text = re.sub(r"\s+", "", str(raw)).lower().replace("€", "eur").replace("£", "gbp")
    text = text.replace("kwh", "kwh").replace("mwh", "mwh")
    for token, code in (("ct/", "cent"), ("c/", "cent"), ("cent/", "cent"),
                        ("p/", "pence"), ("pence/", "pence")):
        if text.startswith(token) and text.endswith("kwh"):
            return "cent_kwh" if code == "cent" else "pence_kwh"
    if text in ("öre/kwh", "ore/kwh"):
        return "ore_sek_kwh"  # use explicit currency for NOK/DKK if applicable
    if text in ("øre/kwh",):
        return "ore_nok_kwh"  # use explicit currency for DKK if applicable
    if text in ("eur/kwh", "eur/kwh", "eurkwh"):
        return "eur_kwh"
    if text in ("eur/mwh", "eurmwh"):
        return "eur_mwh"
    if text in ("gbp/kwh", "gbpkwh"):
        return "gbp_kwh"
    if text == "gbp/mwh":
        return "gbp_mwh"
    for currency in ("sek", "nok", "dkk", "pln"):
        if text == f"{currency}/kwh":
            return f"{currency}_kwh"
        if text == f"{currency}/mwh" and currency == "pln":
            return "pln_mwh"
    return None


def resolve_price_unit(provider: str, override: str, sensor_unit: str | None) -> tuple[str, float]:
    """Never mix prices in different currencies or per-MWh versus per-kWh."""
    key = override if override != "auto" else unit_from_text(sensor_unit)
    if not key:
        if provider == SOURCE_TIBBER:
            key = "eur_kwh"
        elif provider == SOURCE_OCTOPUS:
            key = "gbp_kwh"
        else:
            raise PriceSourceError("Unknown price unit: configure an explicit currency and unit")
    if key not in UNIT_TABLE:
        raise PriceSourceError(f"Unsupported price unit: {key}")
    return UNIT_TABLE[key]


def parse_time(value: Any, zone: Any) -> datetime | None:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (float, int)) and not isinstance(value, bool):
        try:
            number = float(value)
            if not math.isfinite(number):
                return None
            dt = datetime.fromtimestamp(number / 1000 if abs(number) > 10**11 else number, tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            return None
    elif isinstance(value, str):
        try:
            # ISO 8601, including a UTC Z suffix.
            dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=zone)
    return dt.astimezone(zone)


def first_field(mapping: dict[str, Any], configured: str, guesses: tuple[str, ...]):
    """Configured field takes precedence; fallback is an explicit known schema."""
    if configured and configured != "auto":
        return mapping.get(configured)
    for key in guesses:
        if key in mapping:
            return mapping[key]
    return None


def _walk_attribute(attrs: dict[str, Any], path: str) -> Any:
    result: Any = attrs
    for part in path.split("."):
        if not isinstance(result, dict) or not part in result:
            return None
        result = result[part]
    return result


def _array_sources(attrs: dict[str, Any], explicit: str = "auto") -> list[tuple[Any, str | None]]:
    if explicit and explicit != "auto":
        found = _walk_attribute(attrs, explicit)
        return [(found, None)] if found is not None else []
    arrays: list[tuple[Any, str | None]] = []
    for key in ARRAY_KEYS:
        value = attrs.get(key)
        if isinstance(value, (list, dict)):
            hint = "today" if key in TODAY_KEYS else "tomorrow" if key in TOMORROW_KEYS else None
            arrays.append((value, hint))
    # Some integrations nest the payload in 'attributes' or 'forecast'.
    if not arrays:
        for name in ("attributes", "price_data", "forecast"):
            value = attrs.get(name)
            if isinstance(value, dict):
                arrays.extend(_array_sources(value))
    return arrays


def _numeric_day_array(values: list[Any], day: date, zone: Any) -> list[dict[str, Any]]:
    """Parse bare today/tomorrow lists only if their shape matches the real day length."""
    start = datetime(day.year, day.month, day.day, tzinfo=zone)
    next_day = day + timedelta(days=1)
    end = datetime(next_day.year, next_day.month, next_day.day, tzinfo=zone)
    seconds = end.astimezone(timezone.utc).timestamp() - start.astimezone(timezone.utc).timestamp()
    n = len(values)
    if not n or seconds / n not in (900, 1800, 3600):
        return []
    result: list[dict[str, Any]] = []
    interval = seconds / n
    for index, value in enumerate(values):
        try:
            p = float(value)
        except (ValueError, TypeError, OverflowError):
            return []
        if not math.isfinite(p):
            return []
        t = (start.astimezone(timezone.utc) + timedelta(seconds=index * interval)).astimezone(zone)
        finish = (start.astimezone(timezone.utc) + timedelta(seconds=(index + 1) * interval)).astimezone(zone)
        result.append({"start_time": t.isoformat(), "end_time": finish.isoformat(), "price": p})
    return result


def normalize_forecast(
    attributes: dict[str, Any], provider: str, unit: str, zone: Any,
    *, config: dict[str, Any] | None = None, date_today: date | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """Convert timestamped prices to a uniform per-kWh forecast and currency.

    The adapter operates exclusively on read-only HA state attributes and never
    calls an external API. Invalid rows are rejected (never silently assigned
    a time or unit). The return shape is cache-safe and JSON-serializable.
    """
    config = config or {}
    currency, factor = resolve_price_unit(provider, config.get(CONF_PRICE_UNIT, "auto"), unit)
    date_today = date_today or datetime.now(zone).date()
    start_field = config.get(CONF_START_FIELD, "auto")
    end_field = config.get(CONF_END_FIELD, "auto")
    price_field = config.get(CONF_PRICE_FIELD, "auto")
    path = config.get(CONF_DATA_ATTRIBUTE, "auto")
    normalized: dict[float, dict[str, Any]] = {}

    for payload, hint in _array_sources(attributes, path):
        if isinstance(payload, dict):
            if any(k in payload for k in ARRAY_KEYS):
                for nested, nested_hint in _array_sources(payload):
                    if isinstance(nested, list):
                        payload = nested
                        hint = nested_hint or hint
                        break
            elif all(isinstance(k, str) for k in payload):
                # Time-keyed dictionary accepted as a universal fallback.
                payload = [{"start_time": k, "price": v} for k, v in payload.items()]
        if not isinstance(payload, list):
            continue
        if payload and all(isinstance(item, (float, int)) and not isinstance(item, bool) for item in payload):
            if hint in ("today", "tomorrow"):
                day = date_today if hint == "today" else date_today + timedelta(days=1)
                payload = _numeric_day_array(payload, day, zone)
            else:
                continue
        for row in payload:
            if isinstance(row, (list, tuple)) and len(row) >= 2:
                row = {"start_time": row[0], "price": row[1]}
            if not isinstance(row, dict):
                continue
            start = parse_time(first_field(row, start_field, START_KEYS), zone)
            if start is None:
                continue
            end = parse_time(first_field(row, end_field, END_KEYS), zone)
            if end is not None and end.timestamp() <= start.timestamp():
                continue
            raw = first_field(row, price_field, PRICE_KEYS)
            try:
                price = float(raw) * factor
            except (TypeError, ValueError, OverflowError):
                continue
            if not math.isfinite(price):
                continue
            item = {"start_time": start.isoformat(timespec="seconds"), "price_per_kwh": price}
            if end is not None:
                item["end_time"] = end.isoformat(timespec="seconds")
            normalized[start.timestamp()] = item
    return [normalized[t] for t in sorted(normalized)], currency


def normalize_tibber(rows: list[Any], zone: Any) -> list[dict[str, Any]]:
    result, _currency = normalize_forecast(
        {"data": rows}, SOURCE_TIBBER, "€/kWh", zone,
        config={CONF_PRICE_UNIT: "eur_kwh"},
    )
    return result
