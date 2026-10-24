"""Provider-agnostic price caching and low-price phase calculation.

Read-only: no grid measurement and no battery charging/discharging commands.
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

import json
import logging
import math
from datetime import datetime, timezone
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    CONF_DATA_ATTRIBUTE, CONF_END_FIELD, CONF_PRICE_FIELD, CONF_PRICE_UNIT,
    CONF_PROVIDER, CONF_SOURCE_ENTITY, CONF_START_FIELD, CONF_THRESHOLD,
    CONF_THRESHOLDS, CONF_TOMORROW_ENTITY, DEFAULT_THRESHOLD, DOMAIN,
    SOURCE_GENERIC, SOURCE_TIBBER, SOURCE_OCTOPUS, STORAGE_VERSION,
    CONF_MODE, CONF_WINDOW_MINUTES, CONF_MODES, CONF_WINDOWS,
    DEFAULT_MODE, DEFAULT_WINDOW_MINUTES, MIN_WINDOW_MINUTES, MAX_WINDOW_MINUTES,
    MODE_THRESHOLD, MODE_WINDOW, MODES,
    CONF_WINDOW_SCOPE, CONF_WINDOW_SCOPES, SCOPE_FUTURE, SCOPE_ACTIVE, CONF_DISPLAY_NAME,
    WINDOW_SCOPES, DEFAULT_WINDOW_SCOPE, MAX_WINDOW_MINUTES,
)
from .pricing import (
    PriceSlot, active_block, block_end, block_summary, current_slot, daily_slots,
    favorable_blocks, continuous_favorable_blocks, iso, selected_block, serialized_rows, statistics, threshold_price,
    day_segments, day_duration_minutes, priced_minutes,
    cheapest_window, cheapest_periods, FavorablePeriod, evaluate_window, slot_end, longest_complete_future_coverage,
)
from .sources import PriceSourceError, normalize_forecast, normalize_tibber, resolve_price_unit

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class PriceInsightsRuntimeData:
    coordinator: "PriceInsightsCoordinator"


class PriceInsightsCoordinator(DataUpdateCoordinator[dict[str, list[dict[str, Any]]]]):
    """Share the same price calculations across all supported source integrations."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name=f"{DOMAIN}_{entry.entry_id}")
        self.entry = entry
        self.data: dict[str, list[dict[str, Any]]] = {}
        self.currency: str = "EUR" if self.provider != SOURCE_OCTOPUS else "GBP"
        self._store = Store(hass, STORAGE_VERSION, f"{DOMAIN}_{entry.entry_id}")
        # Per-home planning cache: preserve an active window instead of shifting
        # its start on every minute tick. Never retain a finished window.
        self._window_plans: dict[str, tuple[int, Any]] = {}
        # This also preserves a future-only THRESHOLD block after its start,
        # allowing its binary sensor to turn on when the chosen period begins.
        self._threshold_plans: dict[str, tuple[float, str, datetime, datetime]] = {}
        self._threshold_plan_revision: dict[str, int] = {}
        self._window_plan_checked: dict[str, tuple[int, int, int]] = {}
        self._price_revision = 0
        self._last_source_update: datetime | None = None
        self._max_cache_age = timedelta(hours=24)
        self._availability_cache: dict[str, tuple[tuple, dict[str, Any]]] = {}
        self._period_cache: dict[str, tuple[tuple, list[FavorablePeriod]]] = {}

    @property
    def config(self) -> dict[str, Any]:
        return {**self.entry.data, **self.entry.options}

    @property
    def provider(self) -> str:
        return self.config.get(CONF_PROVIDER, SOURCE_TIBBER)

    @property
    def home_keys(self) -> list[str]:
        if self.provider == SOURCE_TIBBER:
            return sorted(self.data)
        return [self.entry.entry_id]

    def device_name(self, home: str) -> str:
        custom = self.entry.data.get(CONF_DISPLAY_NAME)
        if custom:
            if self.provider == SOURCE_TIBBER and len(self.home_keys) > 1:
                return f"{custom} · {home}"
            return custom
        return home if self.provider == SOURCE_TIBBER else self.entry.title

    def source_entity_ids(self) -> list[str]:
        if self.provider == SOURCE_TIBBER:
            return []
        source = self.config.get(CONF_SOURCE_ENTITY)
        other = self.config.get(CONF_TOMORROW_ENTITY)
        if self.provider == SOURCE_OCTOPUS and source and not other:
            derived = source.replace("_current_day_rates", "_next_day_rates")
            if derived != source:
                other = derived
        return list(dict.fromkeys(k for k in (source, other) if k))

    def _cache_signature(self) -> str:
        """Exclude stale cache when source, unit or field mapping changes."""
        return json.dumps({key: self.config.get(key) for key in (
            CONF_PROVIDER, CONF_SOURCE_ENTITY, CONF_TOMORROW_ENTITY,
            CONF_PRICE_UNIT, CONF_DATA_ATTRIBUTE, CONF_START_FIELD,
            CONF_END_FIELD, CONF_PRICE_FIELD,
        )}, sort_keys=True)

    def _usable_cache(self) -> bool:
        if self._last_source_update is None:
            return False
        seconds = (dt_util.now() - self._last_source_update).total_seconds()
        return -300 <= seconds <= self._max_cache_age.total_seconds()

    def _store_payload(self) -> dict[str, Any]:
        plans = {}
        now = dt_util.now().timestamp()
        for home, (duration, scope, window) in self._window_plans.items():
            if window.end.timestamp() > now:
                plans[home] = {
                    "minutes": duration, "scope": scope,
                    "start": iso(window.start), "end": iso(window.end),
                }
        threshold_plans = {}
        for home, (percent, scope, start, end) in self._threshold_plans.items():
            if end.timestamp() > now:
                threshold_plans[home] = {
                    "threshold": percent, "scope": scope,
                    "start": iso(start), "end": iso(end),
                }
        return {
            "signature": self._cache_signature(), "currency": self.currency,
            "fetched_at": iso(self._last_source_update),
            "homes": self.data, "window_plans": plans,
            "threshold_plans": threshold_plans,
        }

    def _schedule_store(self) -> None:
        self._store.async_delay_save(self._store_payload, 2)

    async def async_initialize(self) -> None:
        try:
            stored = await self._store.async_load()
        except (OSError, ValueError, TypeError) as exc:
            _LOGGER.warning("Could not load price cache: %s", exc)
            return
        if not isinstance(stored, dict) or not isinstance(stored.get("homes"), dict):
            return
        signature = stored.get("signature")
        current_signature = self._cache_signature()
        if signature is not None and signature != current_signature:
            return
        if signature is None and self.provider != SOURCE_TIBBER:
            return
        timestamp = dt_util.parse_datetime(str(stored.get("fetched_at"))) if stored.get("fetched_at") else None
        # Legacy pre-version cache lacked fetched_at. Accept it only if there
        # are still live/future price intervals, then immediately refresh.
        if timestamp is None:
            timestamp = dt_util.now()
        self._last_source_update = timestamp
        if not self._usable_cache():
            _LOGGER.info("Ignoring expired electricity price cache")
            self._last_source_update = None
            return
        candidate_data = {
            str(key): self._sanitize_cached_rows(rows)
            for key, rows in stored["homes"].items() if isinstance(rows, list)
        }
        self.data = candidate_data
        # A multi-day shutdown must not resurrect yesterday's window.
        has_current_or_future = any(
            slot_end(items, i).timestamp() > dt_util.now().timestamp()
            for home in candidate_data
            for items in [self.slots(home)]
            for i in range(len(items))
        )
        if not has_current_or_future:
            self.data = {}
            self._last_source_update = None
            return
        if stored.get("currency") in ("EUR", "GBP", "SEK", "NOK", "DKK", "PLN"):
            self.currency = stored["currency"]
        for home, info in stored.get("window_plans", {}).items():
            if not isinstance(info, dict):
                continue
            try:
                start = dt_util.parse_datetime(info["start"])
                end = dt_util.parse_datetime(info["end"])
                duration = int(info["minutes"])
                scope = info.get("scope", SCOPE_FUTURE)
            except (KeyError, TypeError, ValueError):
                continue
            if (start is None or end is None or duration != self.window_minutes(home)
                or scope != self.window_scope(home)
                or not start.timestamp() < dt_util.now().timestamp() < end.timestamp()):
                continue
            restored = evaluate_window(self.slots(home), dt_util.as_local(start), duration)
            if restored and abs(restored.end.timestamp() - end.timestamp()) < 1:
                self._window_plans[home] = (duration, scope, restored)

        for home, info in stored.get("threshold_plans", {}).items():
            if not isinstance(info, dict):
                continue
            try:
                start = dt_util.parse_datetime(info["start"])
                end = dt_util.parse_datetime(info["end"])
                threshold = float(info["threshold"])
                scope = info["scope"]
            except (TypeError, KeyError, ValueError):
                continue
            if (start is None or end is None or scope != self.window_scope(home)
                    or threshold != self.threshold(home)
                    or end.timestamp() <= dt_util.now().timestamp()):
                continue
            for block in continuous_favorable_blocks(
                self.slots(home), start.date(),
                dt_util.as_local(dt_util.now()).date() + timedelta(days=1), threshold,
            ):
                finish = block_end(self.slots(home), block)
                if (finish is not None and block[0].start.timestamp() == start.timestamp()
                        and finish.timestamp() == end.timestamp()):
                    self._threshold_plans[home] = (threshold, scope, start, end)
                    self._threshold_plan_revision[home] = self._price_revision
                    break

    async def _async_update_data(self) -> dict[str, list[dict[str, Any]]]:
        try:
            if self.provider == SOURCE_TIBBER:
                rows, currency = await self._fetch_tibber()
            else:
                rows, currency = self._read_entities()
            if not rows or not any(rows.values()):
                raise PriceSourceError("Price source has no timestamped price forecast")
        except (PriceSourceError, KeyError, TypeError, ValueError, RuntimeError) as exc:
            if self.data and self._usable_cache() and any(self.slots(h) for h in self.data):
                _LOGGER.warning("Price source temporarily unavailable (%s): %s", self.provider, exc)
                return self.data
            raise UpdateFailed(f"No usable prices from {self.provider}: {exc}") from exc
        except Exception as exc:
            if self.data and self._usable_cache() and any(self.slots(h) for h in self.data):
                _LOGGER.warning("Failed fetching price source: %s", exc)
                return self.data
            raise UpdateFailed(f"Failed fetching price source: {exc}") from exc
        self.currency = currency
        self._last_source_update = dt_util.now()
        self._price_revision += 1
        self._availability_cache.clear()
        self._period_cache.clear()
        self.data = rows
        # Remove plans not covered by the latest source data.
        for home, (duration, scope, plan) in list(self._window_plans.items()):
            if not evaluate_window(self.slots(home), plan.start, duration):
                self._window_plans.pop(home, None)
        try:
            await self._store.async_save(self._store_payload())
        except (OSError, ValueError, TypeError) as exc:
            _LOGGER.warning("Unable to persist price forecast: %s", exc)
        return rows

    async def _fetch_tibber(self) -> tuple[dict[str, list[dict[str, Any]]], str]:
        if not self.hass.services.has_service("tibber", "get_prices"):
            raise PriceSourceError("Tibber get_prices service not available")
        start = dt_util.start_of_local_day()
        end = start + timedelta(days=2)
        response = await self.hass.services.async_call(
            "tibber", "get_prices",
            {
                "start": dt_util.as_local(start).strftime("%Y-%m-%d %H:%M:%S"),
                "end": dt_util.as_local(end).strftime("%Y-%m-%d %H:%M:%S"),
            },
            blocking=True, return_response=True,
        )
        prices = response.get("prices") if isinstance(response, dict) else None
        if not isinstance(prices, dict) or not prices:
            raise PriceSourceError("Tibber provided no homes")
        zone = dt_util.now().tzinfo
        return {
            str(home): normalize_tibber(records, zone)
            for home, records in prices.items() if isinstance(records, list)
        }, "EUR"

    def _read_entities(self) -> tuple[dict[str, list[dict[str, Any]]], str]:
        sources = self.source_entity_ids()
        if not sources:
            raise PriceSourceError("No source entity configured")
        values: dict[str, dict[str, Any]] = {}
        zone = dt_util.now().tzinfo
        currency: str | None = None
        for entity_id in sources:
            state = self.hass.states.get(entity_id)
            if state is None or (state.state in ("unavailable", "unknown") and not state.attributes):
                continue
            settings = self.config
            data, detected_currency = normalize_forecast(
                dict(state.attributes), self.provider,
                str(state.attributes.get("unit_of_measurement") or ""), zone,
                config=settings, date_today=dt_util.as_local(dt_util.now()).date(),
            )
            if data:
                if currency is not None and detected_currency != currency:
                    raise PriceSourceError("Selected price entities have different currencies")
                currency = detected_currency
                for row in data:
                    values[row["start_time"]] = row
        if not values:
            raise PriceSourceError("Enable the selected entity and ensure it exposes price data")
        return {
            self.entry.entry_id: sorted(values.values(), key=lambda x: dt_util.parse_datetime(x["start_time"]).timestamp())
        }, (currency or self.currency)

    @staticmethod
    def _sanitize_cached_rows(records: list[Any]) -> list[dict[str, Any]]:
        """Use only JSON-safe, previously normalized price rows."""
        return [
            row for row in records
            if isinstance(row, dict) and "start_time" in row and "price_per_kwh" in row
        ]

    def slots(self, home: str) -> list[PriceSlot]:
        if not self._usable_cache():
            return []
        result = []
        for record in self.data.get(home, []):
            start = dt_util.parse_datetime(str(record.get("start_time")))
            if start is None:
                continue
            end_raw = record.get("end_time")
            end = dt_util.parse_datetime(str(end_raw)) if end_raw else None
            try:
                price = float(record["price_per_kwh"])
            except (ValueError, TypeError):
                continue
            if not math.isfinite(price):
                continue
            result.append(PriceSlot(dt_util.as_local(start), price, dt_util.as_local(end) if end else None))
        result.sort(key=lambda s: s.start.timestamp())
        # Avoid retaining expired past days across service or HA restarts.
        cutoff = dt_util.now().timestamp() - MAX_WINDOW_MINUTES * 60
        return [s for i, s in enumerate(result) if slot_end(result, i).timestamp() > cutoff]

    def threshold(self, home: str) -> float:
        settings = self.config
        thresholds = settings.get(CONF_THRESHOLDS, {})
        if not isinstance(thresholds, dict):
            thresholds = {}
        value = thresholds.get(home, settings.get(CONF_THRESHOLD, DEFAULT_THRESHOLD))
        try:
            return max(0.0, min(100.0, float(value)))
        except (TypeError, ValueError):
            return DEFAULT_THRESHOLD

    def _invalidate_price_plans(self, home: str | None = None) -> None:
        """Drop cached decisions so every calculation uses the new settings."""
        self._availability_cache.clear()
        self._period_cache.clear()
        targets = [home] if home is not None else list(self.home_keys)
        for key in targets:
            self._window_plans.pop(key, None)
            self._window_plan_checked.pop(key, None)
            self._threshold_plans.pop(key, None)
            self._threshold_plan_revision.pop(key, None)
        self._schedule_store()

    async def async_recalculate(self) -> None:
        """Immediately reevaluate all home sensors, without waiting for a timer.

        Cached, still-valid prices are sufficient; retrieve fresh prices only
        if there are no usable intervals for the configured source.
        """
        homes = self.home_keys
        if not homes or not any(self.slots(home) for home in homes):
            await self.async_refresh()
            homes = self.home_keys
        for home in homes:
            self.current_price(home)
            self.is_favorable(home)
            self.phase_attrs(home)
            self.price_attrs(home)
            self.threshold_attrs(home)
        self.async_update_listeners()

    async def async_set_threshold(self, home: str, value: float) -> None:
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError("Threshold must be between 0 and 100 percent")
        current = self.config.get(CONF_THRESHOLDS, {})
        new = dict(current) if isinstance(current, dict) else {}
        new[home] = round(value, 2)
        self.hass.config_entries.async_update_entry(self.entry, options={
            **self.entry.options, CONF_THRESHOLDS: new,
        })
        self._invalidate_price_plans(home)
        await self.async_recalculate()

    def evaluation_mode(self, home: str) -> str:
        modes = self.config.get(CONF_MODES, {})
        choice = modes.get(home) if isinstance(modes, dict) and home in modes else self.config.get(CONF_MODE, DEFAULT_MODE)
        return choice if choice in MODES else DEFAULT_MODE

    async def async_set_evaluation_mode(self, home: str, mode: str) -> None:
        if mode not in MODES:
            raise ValueError("Invalid price evaluation mode")
        current = self.config.get(CONF_MODES, {})
        updated = dict(current) if isinstance(current, dict) else {}
        updated[home] = mode
        self.hass.config_entries.async_update_entry(self.entry, options={
            **self.entry.options, CONF_MODES: updated,
        })
        self._invalidate_price_plans(home)
        await self.async_recalculate()

    def window_minutes(self, home: str) -> int:
        windows = self.config.get(CONF_WINDOWS, {})
        value = windows.get(home) if isinstance(windows, dict) and home in windows else self.config.get(CONF_WINDOW_MINUTES, DEFAULT_WINDOW_MINUTES)
        try:
            number = int(value)
        except (ValueError, TypeError, OverflowError):
            return DEFAULT_WINDOW_MINUTES
        return max(MIN_WINDOW_MINUTES, min(MAX_WINDOW_MINUTES, number))

    async def async_set_window_minutes(self, home: str, minutes: float) -> None:
        if not math.isfinite(minutes) or int(minutes) != minutes or not MIN_WINDOW_MINUTES <= minutes <= MAX_WINDOW_MINUTES:
            raise ValueError("Window duration must be a whole number of minutes from 1 to 1440")
        current = self.config.get(CONF_WINDOWS, {})
        updated = dict(current) if isinstance(current, dict) else {}
        updated[home] = int(minutes)
        self.hass.config_entries.async_update_entry(self.entry, options={
            **self.entry.options, CONF_WINDOWS: updated,
        })
        self._invalidate_price_plans(home)
        await self.async_recalculate()

    def window_scope(self, home: str) -> str:
        overrides = self.config.get(CONF_WINDOW_SCOPES, {})
        value = overrides.get(home) if isinstance(overrides, dict) and home in overrides else self.config.get(CONF_WINDOW_SCOPE, DEFAULT_WINDOW_SCOPE)
        return value if value in WINDOW_SCOPES else DEFAULT_WINDOW_SCOPE

    async def async_set_window_scope(self, home: str, scope: str) -> None:
        if scope not in WINDOW_SCOPES:
            raise ValueError("Invalid window search scope")
        previous = self.config.get(CONF_WINDOW_SCOPES, {})
        updated = dict(previous) if isinstance(previous, dict) else {}
        updated[home] = scope
        self.hass.config_entries.async_update_entry(self.entry, options={
            **self.entry.options, CONF_WINDOW_SCOPES: updated,
        })
        self._invalidate_price_plans(home)
        await self.async_recalculate()

    def chosen_window(self, home: str):
        """Pick the cheapest upcoming (optionally ongoing) complete price window."""
        now = dt_util.now()
        duration = self.window_minutes(home)
        scope = self.window_scope(home)
        previous = self._window_plans.get(home)
        if previous:
            old_duration, old_scope, old = previous
            if (old_duration == duration and old_scope == scope
                    and old.start.timestamp() <= now.timestamp() < old.end.timestamp()):
                verified = evaluate_window(self.slots(home), old.start, duration)
                if verified is not None:
                    return verified
                self._window_plans.pop(home, None)
        minute = int(now.timestamp() // 60)
        fingerprint = (duration, scope, minute, self._price_revision)
        if self._window_plan_checked.get(home) == fingerprint:
            return self._window_plans[home][2] if home in self._window_plans else None
        earliest = datetime.fromtimestamp(math.ceil(now.timestamp() / 60) * 60, now.tzinfo)
        window = cheapest_window(self.slots(home), earliest, duration, include_active=scope == SCOPE_ACTIVE)
        self._window_plan_checked[home] = fingerprint
        if window is not None:
            old_window = previous[2] if previous else None
            self._window_plans[home] = (duration, scope, window)
            if old_window is None or old_window.start != window.start or old_window.end != window.end:
                self._schedule_store()
        elif home in self._window_plans:
            self._window_plans.pop(home)
            self._schedule_store()
        return window

    def eligible_price_periods(self, home: str) -> list[FavorablePeriod]:
        """Equally cheap continuous phases of at least the configured duration."""
        now = dt_util.now()
        scope = self.window_scope(home)
        previous = self._window_plans.get(home)
        # A previously planned future-only period remains eligible once started.
        active_pinned = bool(previous and previous[0] == self.window_minutes(home)
                             and previous[1] == scope
                             and previous[2].start.timestamp() <= now.timestamp() < previous[2].end.timestamp())
        include_active = scope == SCOPE_ACTIVE or active_pinned
        fingerprint = (self._price_revision, int(now.timestamp() // 60),
                       self.window_minutes(home), scope, include_active)
        cached = self._period_cache.get(home)
        if cached and cached[0] == fingerprint:
            return cached[1]
        results = cheapest_periods(self.slots(home), now, self.window_minutes(home), include_active)
        self._period_cache[home] = (fingerprint, results)
        return results

    def selected_price_period(self, home: str) -> FavorablePeriod | None:
        """Select the active phase when permitted, else the earliest planned phase."""
        periods = self.eligible_price_periods(home)
        if not periods:
            return None
        now = dt_util.now().timestamp()
        if self.window_scope(home) == SCOPE_ACTIVE:
            for period in periods:
                if period.start.timestamp() <= now < period.end.timestamp():
                    return period
        planned = self.chosen_window(home)
        if planned is not None:
            for period in periods:
                if period.start.timestamp() <= planned.start.timestamp() + .001 \
                        and planned.end.timestamp() <= period.end.timestamp() + .001:
                    return period
        return periods[0]

    def _selected_threshold_block(self, home: str) -> list[PriceSlot]:
        """Apply the same window scope to the percentage-threshold method."""
        now = dt_util.now()
        slots = self.slots(home)
        if not slots:
            return []
        threshold = self.threshold(home)
        scope = self.window_scope(home)
        previous = self._threshold_plans.get(home)
        if previous:
            old_percent, old_scope, old_start, old_end = previous
            if (old_percent == threshold and old_scope == scope
                    and now.timestamp() < old_end.timestamp()):
                # A started period stays stable until its end, but only if its
                # price points still meet the selected percentage threshold.
                # Future plans are recalculated after a fresh provider update.
                if (old_start.timestamp() <= now.timestamp()
                        or self._threshold_plan_revision.get(home) == self._price_revision):
                    for block in continuous_favorable_blocks(
                        slots, old_start.date(), dt_util.as_local(now).date() + timedelta(days=1), threshold,
                    ):
                        end = block_end(slots, block)
                        if (end is not None and block[0].start.timestamp() == old_start.timestamp()
                                and end.timestamp() == old_end.timestamp()):
                            return block
        chosen = selected_block(slots, now, threshold, include_active=scope == SCOPE_ACTIVE)
        if chosen:
            end = block_end(slots, chosen)
            if end is not None:
                new_plan = (threshold, scope, chosen[0].start, end)
                if new_plan != previous:
                    self._threshold_plans[home] = new_plan
                    self._schedule_store()
                self._threshold_plan_revision[home] = self._price_revision
                return chosen
        if home in self._threshold_plans:
            self._threshold_plans.pop(home, None)
            self._threshold_plan_revision.pop(home, None)
            self._schedule_store()
        return []

    def current_price(self, home: str) -> float | None:
        slot = current_slot(self.slots(home), dt_util.now())
        return slot.price if slot else None

    def is_favorable(self, home: str) -> bool:
        if self.evaluation_mode(home) == MODE_WINDOW:
            period = self.selected_price_period(home)
            now = dt_util.now().timestamp()
            return bool(period and period.start.timestamp() <= now < period.end.timestamp())
        block = self._selected_threshold_block(home)
        now = dt_util.now().timestamp()
        finish = block_end(self.slots(home), block)
        return bool(block and finish is not None and block[0].start.timestamp() <= now < finish.timestamp())

    def phase_start(self, home: str):
        if self.evaluation_mode(home) == MODE_WINDOW:
            period = self.selected_price_period(home)
            return period.start if period else None
        block = self._selected_threshold_block(home)
        return block[0].start if block else None

    def phase_end(self, home: str):
        if self.evaluation_mode(home) == MODE_WINDOW:
            period = self.selected_price_period(home)
            return period.end if period else None
        slots = self.slots(home)
        return block_end(slots, self._selected_threshold_block(home))

    def availability_snapshot(self, home: str) -> dict[str, Any]:
        """Compute price diagnostics once per minute/revision and share both entity properties."""
        now = dt_util.now()
        marker = (self._price_revision, int(now.timestamp() // 60),
                  self.evaluation_mode(home), self.window_scope(home),
                  self.window_minutes(home), self.threshold(home),
                  self._usable_cache())
        cached = self._availability_cache.get(home)
        if cached is not None and cached[0] == marker:
            return cached[1]
        slots = self.slots(home)
        today = dt_util.as_local(now).date()
        tomorrow = today + timedelta(days=1)
        current = current_slot(slots, now)
        has_window = True
        if self.evaluation_mode(home) == MODE_WINDOW:
            has_window = self.chosen_window(home) is not None
        status = (
            "no_forecast" if not slots else
            "no_current_price" if current is None else
            "no_complete_window" if not has_window else "ready"
        )
        result = {
            "status": status,
            "price_source": self.provider,
            "current_price_available": current is not None,
            "today_available": bool(day_segments(slots, today)),
            "tomorrow_available": bool(day_segments(slots, tomorrow)),
            "longest_available_minutes": longest_complete_future_coverage(slots, now),
            "required_window_minutes": self.window_minutes(home),
            "window_search_scope": self.window_scope(home),
            "last_price_update": iso(self._last_source_update),
            "price_cache_valid": self._usable_cache(),
            "latest_price_end": iso(max((slot_end(slots, i) for i in range(len(slots))),
                                         default=None, key=lambda t: t.timestamp())),
        }
        self._availability_cache[home] = (marker, result)
        return result

    def threshold_attrs(self, home: str) -> dict[str, Any]:
        low, cutoff = threshold_price(day_segments(self.slots(home), dt_util.as_local(dt_util.now()).date()), self.threshold(home))
        return {"current_threshold_price": cutoff, "min_today_price": low}

    def price_attrs(self, home: str) -> dict[str, Any]:
        slots = self.slots(home)
        today = dt_util.as_local(dt_util.now()).date()
        attrs = {
            "provider": self.provider,
            "source_entity": self.config.get(CONF_SOURCE_ENTITY),
            "currency": self.currency,
            "evaluation_mode": self.evaluation_mode(home),
            "window_minutes": self.window_minutes(home),
            "window_search_scope": self.window_scope(home),
            **statistics(day_segments(slots, today), "today"),
            **statistics(day_segments(slots, today + timedelta(days=1)), "tomorrow"),
            **statistics(slots, "overall"),
        }
        raw = serialized_rows(slots)
        if len(json.dumps({**attrs, "data": raw}, ensure_ascii=False)) <= 14000:
            attrs["data"] = raw
        return attrs

    def day_attrs(self, home: str, offset: int) -> dict[str, Any]:
        today = dt_util.as_local(dt_util.now()).date() + timedelta(days=offset)
        slots = day_segments(self.slots(home), today)
        _low, cutoff = threshold_price(slots, self.threshold(home))
        attrs = {
            "date": today.isoformat(), "threshold_price": cutoff,
            "covered_minutes": round(priced_minutes(slots), 2),
            "day_duration_minutes": day_duration_minutes(slots, today),
            "full_day_coverage": bool(slots) and abs(priced_minutes(slots) - day_duration_minutes(slots, today)) < 0.01,
            "evaluation_mode": self.evaluation_mode(home),
            "window_minutes": self.window_minutes(home),
            "window_search_scope": self.window_scope(home),
            **statistics(slots, "day"),
        }
        rows = serialized_rows(slots)
        if len(json.dumps({**attrs, "data": rows}, ensure_ascii=False)) < 14000:
            attrs["data"] = rows
        return attrs

    def day_average(self, home: str, offset: int) -> float | None:
        day = dt_util.as_local(dt_util.now()).date() + timedelta(days=offset)
        return statistics(day_segments(self.slots(home), day), "day")["avg_day_price"]

    @staticmethod
    def _bounded_phase_attrs(attrs: dict[str, Any]) -> dict[str, Any]:
        """Keep Home Assistant Recorder attributes below its 16 KiB limit."""
        if len(json.dumps(attrs, ensure_ascii=False, default=str).encode("utf-8")) > 14000:
            for block in attrs.get("all_favorable_blocks", []):
                block.pop("data", None)
        if len(json.dumps(attrs, ensure_ascii=False, default=str).encode("utf-8")) > 14000:
            attrs.pop("data", None)
        return attrs

    def phase_attrs(self, home: str) -> dict[str, Any]:
        slots = self.slots(home)
        now = dt_util.now()
        mode = self.evaluation_mode(home)
        if mode == MODE_WINDOW:
            period = self.selected_price_period(home)
            periods = self.eligible_price_periods(home)
            block = list(period.segments) if period else []
            summaries = []
            for candidate in periods:
                item = block_summary(list(candidate.segments), list(candidate.segments))
                item["favorable_from"] = iso(candidate.start)
                item["favorable_until"] = iso(candidate.end)
                item["avg_price"] = candidate.average_price
                item["actual_window_minutes"] = int(round((candidate.end.timestamp() - candidate.start.timestamp()) / 60))
                # Price series is already available on daily-forecast entities.
                item.pop("data", None)
                summaries.append(item)
            attrs = {
                "evaluation_mode": mode,
                "window_minutes": self.window_minutes(home),
                "window_minimum_minutes": self.window_minutes(home),
                "window_search_scope": self.window_scope(home),
                "remaining_window_minutes": max(0, math.ceil((period.end.timestamp() - now.timestamp()) / 60)) if period else None,
                "window_active": bool(period and period.start.timestamp() <= now.timestamp() < period.end.timestamp()),
                "window_available": period is not None,
                "longest_available_minutes": longest_complete_future_coverage(slots, now),
                "favorable_from": iso(period.start) if period else None,
                "favorable_until": iso(period.end) if period else None,
                **statistics(block, "favorable_phase"),
                "all_favorable_blocks": summaries,
                "data": serialized_rows(block),
            }
            if period is not None:
                attrs["avg_favorable_phase_price"] = period.average_price
                attrs["actual_window_minutes"] = int(round((period.end.timestamp() - period.start.timestamp()) / 60))
            return self._bounded_phase_attrs(attrs)

        block = self._selected_threshold_block(home)
        target_day = block[0].start.date() if block else None
        all_blocks = []
        current_time = now.timestamp()
        local_day = dt_util.as_local(now).date()
        for item in continuous_favorable_blocks(
            slots, local_day - timedelta(days=1), local_day + timedelta(days=1),
            self.threshold(home),
        ):
            end = block_end(slots, item)
            if end is None or end.timestamp() <= current_time:
                continue
            # In future-only mode retain the chosen period after its start,
            # but do not add unrelated already-running periods.
            chosen = bool(block and item[0].start.timestamp() == block[0].start.timestamp())
            if self.window_scope(home) == SCOPE_FUTURE and item[0].start.timestamp() < current_time and not chosen:
                continue
            all_blocks.append(item)
        low, cutoff = threshold_price(day_segments(slots, target_day), self.threshold(home)) if target_day else (None, None)
        attrs = {
            "evaluation_mode": mode,
            "window_minutes": self.window_minutes(home),
            "window_search_scope": self.window_scope(home),
            "favorable_from": iso(block[0].start) if block else None,
            "favorable_until": iso(block_end(slots, block)),
            "threshold_min_price": low,
            "threshold_max_price": cutoff,
            **statistics(block, "favorable_phase"),
            "all_favorable_blocks": [block_summary(slots, group) for group in all_blocks],
            "data": serialized_rows([slot for group in all_blocks for slot in group]),
        }
        return self._bounded_phase_attrs(attrs)
