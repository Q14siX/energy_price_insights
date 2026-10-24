"""Pure price calculations adapted from Energy Storage Control.

The threshold is daily minimum + percent * (daily maximum - minimum).
SPDX-License-Identifier: Apache-2.0
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, slots=True)
class PriceSlot:
    start: datetime
    price: float
    end: datetime | None = None


def interval_seconds(slots: list[PriceSlot]) -> float:
    """Deduce a slot duration for sources that omit end times."""
    changes = [b.start.timestamp() - a.start.timestamp() for a, b in zip(slots, slots[1:])]
    valid = [delta for delta in changes if 0 < delta <= 3600]
    return min(valid) if valid else 900


def slot_end(slots: list[PriceSlot], position: int) -> datetime:
    item = slots[position]
    if item.end is not None and item.end.timestamp() > item.start.timestamp():
        return item.end
    inferred = (item.start.astimezone(timezone.utc) + timedelta(seconds=interval_seconds(slots))).astimezone(item.start.tzinfo)
    if position + 1 < len(slots) and slots[position + 1].start.timestamp() < inferred.timestamp():
        return slots[position + 1].start
    return inferred


def current_slot(slots: list[PriceSlot], now: datetime) -> PriceSlot | None:
    for i, item in enumerate(slots):
        if item.start.timestamp() <= now.timestamp() < slot_end(slots, i).timestamp():
            return item
    return None


def threshold_price(slots: list[PriceSlot], percent: float) -> tuple[float | None, float | None]:
    if not slots:
        return None, None
    low = min(Decimal(str(x.price)) for x in slots)
    high = max(Decimal(str(x.price)) for x in slots)
    percentage = Decimal(str(max(0, min(100, percent))))
    return float(low), float(low + (high - low) * percentage / Decimal(100))


def daily_slots(slots: list[PriceSlot], day: date) -> list[PriceSlot]:
    return [s for s in slots if s.start.date() == day]


def favorable_blocks(slots: list[PriceSlot], day: date, percent: float) -> list[list[PriceSlot]]:
    """Find favorable phases within *one* local day, clipped at midnight.

    Kept for callers which explicitly need day-local groups; the coordinator
    uses continuous_favorable_blocks for cross-midnight phases.
    """
    return continuous_favorable_blocks(slots, day, day, percent)


def continuous_favorable_blocks(
    slots: list[PriceSlot], first_day: date, last_day: date, percent: float,
) -> list[list[PriceSlot]]:
    """Join physically contiguous favorable prices across local day boundaries.

    Each day's own min/max defines its threshold; a phase crosses midnight
    only if the intervals on *both* sides satisfy their respective limits.
    Boundaries are clipped in local time; timestamps check real continuity,
    including 23/25-hour daylight-saving days and partial source intervals.
    """
    if not slots or last_day < first_day:
        return []
    blocks: list[list[PriceSlot]] = []
    current: list[PriceSlot] = []
    day = first_day
    while day <= last_day:
        segments = day_segments(slots, day)
        _minimum, cutoff = threshold_price(segments, percent)
        if cutoff is not None:
            limit = Decimal(str(cutoff))
            for item in segments:
                if (current and current[-1].end is not None
                        and abs(current[-1].end.timestamp() - item.start.timestamp()) > .5):
                    blocks.append(current)
                    current = []
                if Decimal(str(item.price)) <= limit:
                    current.append(item)
                elif current:
                    blocks.append(current)
                    current = []
        elif current:
            blocks.append(current)
            current = []
        day += timedelta(days=1)
    if current:
        blocks.append(current)
    return blocks


def _local_price_date(slots: list[PriceSlot], now: datetime) -> date:
    """Determine calendar date in the price source's timezone, never in UTC."""
    return now.astimezone(slots[0].start.tzinfo).date() if slots else now.date()


def block_end(slots: list[PriceSlot], block: list[PriceSlot]) -> datetime | None:
    if not block:
        return None
    # A phase may contain pieces clipped at a local midnight. Respect their
    # explicit ending instead of extending to the uncut source interval.
    if block[-1].end is not None and block[-1].end.timestamp() > block[-1].start.timestamp():
        return block[-1].end
    for index, item in enumerate(slots):
        if item.start.timestamp() == block[-1].start.timestamp():
            return slot_end(slots, index)
    return block[-1].end or block[-1].start + timedelta(seconds=interval_seconds(slots))


def selected_block(slots: list[PriceSlot], now: datetime, percent: float,
                   include_active: bool = True) -> list[PriceSlot]:
    """Select a future or active threshold phase, spanning day boundaries.

    Previously selected future-only phases remain pinned in the coordinator
    after their start and are not discarded just because they turned active.
    """
    if not slots:
        return []
    today = _local_price_date(slots, now)
    blocks = continuous_favorable_blocks(slots, today - timedelta(days=1),
                                         today + timedelta(days=1), percent)
    timestamp = now.timestamp()
    if include_active:
        for block in blocks:
            end = block_end(slots, block)
            if end and block[0].start.timestamp() <= timestamp < end.timestamp():
                return block
    for block in blocks:
        if block[0].start.timestamp() >= timestamp:
            return block
    return []


def active_block(slots: list[PriceSlot], now: datetime, percent: float) -> list[PriceSlot]:
    if not slots:
        return []
    today = _local_price_date(slots, now)
    for block in continuous_favorable_blocks(slots, today - timedelta(days=1),
                                            today + timedelta(days=1), percent):
        end = block_end(slots, block)
        if end and block[0].start.timestamp() <= now.timestamp() < end.timestamp():
            return block
    return []


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat(timespec="seconds") if dt is not None else None


def serialized_rows(slots: list[PriceSlot]) -> list[dict[str, Any]]:
    return [
        {"start_time": iso(x.start), "end_time": iso(x.end) if x.end else None, "price_per_kwh": x.price}
        for x in slots
    ]


def block_summary(slots: list[PriceSlot], block: list[PriceSlot]) -> dict[str, Any]:
    costs = [x.price for x in block]
    return {
        "favorable_from": iso(block[0].start) if block else None,
        "favorable_until": iso(block_end(slots, block)),
        "slot_count": len(block),
        "min_price": min(costs) if costs else None,
        "avg_price": statistics(block, "block")["avg_block_price"] if costs else None,
        "max_price": max(costs) if costs else None,
        "data": serialized_rows(block),
    }


def price_segments(
    slots: list[PriceSlot],
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[PriceSlot]:
    """Return non-overlapping, precisely bounded priced intervals.

    Using UTC timestamps for clipping avoids arithmetic across daylight-saving
    transitions; the displayed times retain the source's local timezone.
    """
    if not slots:
        return []
    zone = slots[0].start.tzinfo
    lower = start.timestamp() if start is not None else float("-inf")
    upper = end.timestamp() if end is not None else float("inf")
    segments = []
    for interval_start, interval_end, price in _priced_intervals(slots):
        a, b = max(interval_start, lower), min(interval_end, upper)
        if a < b:
            segments.append(PriceSlot(
                datetime.fromtimestamp(a, zone),
                price,
                datetime.fromtimestamp(b, zone),
            ))
    return segments


def day_segments(slots: list[PriceSlot], day: date) -> list[PriceSlot]:
    """Clip source prices at local midnight (including 23/25-hour days)."""
    if not slots:
        return []
    zone = slots[0].start.tzinfo
    start = datetime.combine(day, time.min, tzinfo=zone)
    end = datetime.combine(day + timedelta(days=1), time.min, tzinfo=zone)
    return price_segments(slots, start, end)


def day_duration_minutes(slots: list[PriceSlot], day: date) -> float:
    """Length of the actual local calendar day, not always 1,440 minutes."""
    if not slots:
        return 0
    zone = slots[0].start.tzinfo
    start = datetime.combine(day, time.min, tzinfo=zone)
    end = datetime.combine(day + timedelta(days=1), time.min, tzinfo=zone)
    return (end.timestamp() - start.timestamp()) / 60


def priced_minutes(slots: list[PriceSlot]) -> float:
    """Sum the priced duration, avoiding an unweighted point average."""
    return sum(
        max(0.0, (segment.end.timestamp() - segment.start.timestamp()))
        for segment in price_segments(slots) if segment.end is not None
    ) / 60


def statistics(slots: list[PriceSlot], name: str) -> dict[str, Any]:
    """Price min/max and elapsed-time weighted average of priced intervals.

    Missing time is excluded, never filled with synthetic prices. The time
    associated with the average denotes the interval closest to the average.
    """
    segments = price_segments(slots)
    if not segments:
        return {f"{key}_{name}_{suffix}": None for suffix in ("price", "time") for key in ("min", "avg", "max")}
    minimum = min(segments, key=lambda s: (s.price, s.start.timestamp()))
    maximum = max(segments, key=lambda s: (s.price, -s.start.timestamp()))
    seconds = [(segment.end.timestamp() - segment.start.timestamp()) for segment in segments]
    duration = sum(seconds)
    average = sum(segment.price * length for segment, length in zip(segments, seconds)) / duration
    average_at = min(segments, key=lambda s: (abs(s.price - average), s.start.timestamp()))
    return {
        f"min_{name}_price": minimum.price,
        f"avg_{name}_price": average,
        f"max_{name}_price": maximum.price,
        f"min_{name}_time": iso(minimum.start),
        f"avg_{name}_time": iso(average_at.start),
        f"max_{name}_time": iso(maximum.start),
    }


@dataclass(frozen=True, slots=True)
class CheapestWindow:
    """A complete contiguous duration with a duration-weighted average price."""

    start: datetime
    end: datetime
    average_price: float
    segments: tuple[PriceSlot, ...]


def _priced_intervals(slots: list[PriceSlot]) -> list[tuple[float, float, float]]:
    ordered = sorted(slots, key=lambda s: s.start.timestamp())
    intervals = []
    inferred = interval_seconds(ordered)
    for i, slot in enumerate(ordered):
        start = slot.start.timestamp()
        end = slot.end.timestamp() if slot.end and slot.end.timestamp() > start else start + inferred
        if i + 1 < len(ordered):
            end = min(end, ordered[i + 1].start.timestamp())
        if end > start:
            intervals.append((start, end, slot.price))
    return intervals


def _evaluate_window_intervals(intervals: list[tuple[float, float, float]],
                               start: datetime, duration_minutes: int) -> CheapestWindow | None:
    """Compute a candidate from pre-normalized intervals without rescanning the forecast."""
    if not 1 <= duration_minutes <= 1440:
        return None
    length = duration_minutes * 60.0
    from_time = start.timestamp()
    finish = from_time + length
    cursor = from_time
    cost = 0.0
    covered = []
    for a, b, price in intervals:
        if b <= cursor + .001:
            continue
        if a > cursor + .001:
            break
        stop = min(b, finish)
        if stop > cursor:
            covered.append(PriceSlot(datetime.fromtimestamp(cursor, start.tzinfo), price,
                                     datetime.fromtimestamp(stop, start.tzinfo)))
            cost += (stop - cursor) * price
            cursor = stop
        if cursor >= finish - .001:
            return CheapestWindow(start, datetime.fromtimestamp(finish, start.tzinfo),
                                  cost / length, tuple(covered))
    return None


def evaluate_window(slots: list[PriceSlot], start: datetime, duration_minutes: int) -> CheapestWindow | None:
    """Evaluate one exact window; reject all gaps."""
    return _evaluate_window_intervals(_priced_intervals(slots), start, duration_minutes)


def cheapest_window(
    slots: list[PriceSlot], now: datetime, duration_minutes: int,
    include_active: bool = False,
) -> CheapestWindow | None:
    """Find the lowest duration-weighted window, either future-only or also active.

    Active windows must have started in the past and finish after now.
    Completely elapsed windows are NEVER offered. All segments must be covered.
    """
    if not 1 <= duration_minutes <= 1440 or not slots:
        return None
    length = duration_minutes * 60.0
    intervals = _priced_intervals(slots)
    if not intervals:
        return None
    present = now.timestamp()
    earliest = present - length if include_active else present
    candidates = {present}
    for start, end, _ in intervals:
        candidates.update((start, end - length))
    # Piecewise-linear cost is extremal at a tariff boundary or a boundary
    # shifted by the window duration. For active-only choices, an end exactly
    # at now is not running and therefore excluded.
    best = None
    for candidate in sorted(candidates):
        if candidate < earliest - .001 or candidate < intervals[0][0] - .001:
            continue
        if candidate + length <= present + .001 or candidate + length > intervals[-1][1] + .001:
            continue
        start = datetime.fromtimestamp(candidate, now.tzinfo)
        item = _evaluate_window_intervals(intervals, start, duration_minutes)
        if item is None:
            continue
        if best is None or item.average_price < best.average_price - 1e-10:
            best = item
    return best



@dataclass(frozen=True, slots=True)
class FavorablePeriod:
    """Union of overlapping/touching equally optimal fixed-duration windows."""

    start: datetime
    end: datetime
    average_price: float
    segments: tuple[PriceSlot, ...]


def cheapest_periods(
    slots: list[PriceSlot], now: datetime, duration_minutes: int,
    include_active: bool = False,
) -> list[FavorablePeriod]:
    """Find every globally cheapest eligible window and merge continuous ties.

    The configured duration is a MINIMUM for each result, rather than a cap.
    Two equal-price 60-minute windows at separate times stay separate;
    overlapping/touching 60-minute windows with the same optimal cost become
    a single longer period. Disconnected data never becomes a fictitious span.
    """
    if not 1 <= duration_minutes <= 1440 or not slots:
        return []
    length = duration_minutes * 60.0
    intervals = _priced_intervals(slots)
    if not intervals:
        return []
    present = now.timestamp()
    earliest = present - length if include_active else present
    candidates = {present, earliest}
    for a, b, _ in intervals:
        candidates.add(a)
        candidates.add(b - length)
    valid = []
    for candidate in sorted(candidates):
        if candidate < earliest - .001 or candidate < intervals[0][0] - .001:
            continue
        if candidate + length <= present + .001 or candidate + length > intervals[-1][1] + .001:
            continue
        item = _evaluate_window_intervals(
            intervals, datetime.fromtimestamp(candidate, now.tzinfo), duration_minutes,
        )
        if item is not None:
            valid.append(item)
    if not valid:
        return []
    best_price = min(item.average_price for item in valid)
    tolerance = max(1e-10, abs(best_price) * 1e-9)
    cheapest = [item for item in valid if abs(item.average_price - best_price) <= tolerance]
    ranges = []
    previous_optimal_index = None
    for index, item in enumerate(valid):
        if abs(item.average_price - best_price) > tolerance:
            previous_optimal_index = None
            continue
        a, b = item.start.timestamp(), item.end.timestamp()
        # A flat-price plateau can be much longer than the requested minimum.
        # Its outer optimal windows do not overlap, but EVERY intermediate
        # start is equally cheap. Connect only when no other candidate lies
        # between them and the midpoint is fully priced at the same optimum.
        bridge = False
        if ranges and previous_optimal_index == index - 1 and a > ranges[-1][1] + .001:
            previous = valid[index - 1]
            middle = (previous.start.timestamp() + a) / 2
            midpoint = _evaluate_window_intervals(
                intervals, datetime.fromtimestamp(middle, now.tzinfo), duration_minutes,
            )
            bridge = midpoint is not None and abs(midpoint.average_price - best_price) <= tolerance
            if bridge:
                # Never merge across a hole in the provider forecast.
                cursor = ranges[-1][0]
                for start_t, end_t, _ in intervals:
                    if end_t <= cursor + .001:
                        continue
                    if start_t > cursor + .001:
                        break
                    cursor = max(cursor, end_t)
                    if cursor >= b - .001:
                        break
                bridge = cursor >= b - .001
        if ranges and (a <= ranges[-1][1] + .001 or bridge):
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], b))
        else:
            ranges.append((a, b))
        previous_optimal_index = index
    periods = []
    for a, b in ranges:
        # If a price plateau started long before the current time, its
        # full real beginning is still useful when showing an ACTIVE period.
        # Only extend over genuinely contiguous intervals at the same
        # optimal price; do not reinterpret historical, expired windows as
        # new standalone candidates.
        if include_active and a <= present < b:
            cursor = a
            for x, y, price in reversed(intervals):
                if x >= cursor - .001:
                    continue
                if y < cursor - .001 or abs(price - best_price) > tolerance:
                    break
                cursor = x
            a = cursor
        start = datetime.fromtimestamp(a, now.tzinfo)
        end = datetime.fromtimestamp(b, now.tzinfo)
        pieces = tuple(price_segments(slots, start, end))
        if not pieces:
            continue
        total = sum((x.end.timestamp() - x.start.timestamp()) for x in pieces)
        cost = sum(x.price * (x.end.timestamp() - x.start.timestamp()) for x in pieces)
        periods.append(FavorablePeriod(start, end, cost / total, pieces))
    return periods

def longest_complete_future_coverage(slots: list[PriceSlot], now: datetime) -> int:
    """Return the longest uninterrupted future forecast in whole minutes."""
    intervals = [
        (max(now.timestamp(), a), b)
        for a, b, _ in _priced_intervals(slots)
        if b > now.timestamp() and b > a
    ]
    longest = 0.0
    run_start = run_end = None
    for a, b in intervals:
        if run_end is None or a > run_end + 0.001:
            if run_end is not None:
                longest = max(longest, run_end - run_start)
            run_start, run_end = a, b
        else:
            run_end = max(run_end, b)
    if run_end is not None:
        longest = max(longest, run_end - run_start)
    return int(longest // 60)
