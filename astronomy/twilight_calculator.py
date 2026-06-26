"""Twilight calculations using Astral."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

from astral import Depression
from astral.sun import dawn, dusk

from astronomy.data_models import GeoLocation
from astronomy.location import ObserverFactory


class TwilightCalculator:
    """Calculates civil, nautical, and astronomical twilight events."""

    def __init__(self, location: GeoLocation) -> None:
        self._location = location
        self._observer = ObserverFactory.create(location)
        self._tz = ZoneInfo(location.timezone)

    @staticmethod
    def _adjusted_datetime(
        value: datetime,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> datetime:
        if not use_daylight_saving_time:
            if standard_offset is None:
                raise ValueError("standard_offset is required when DST is disabled")
            utc_value = value.astimezone(timezone.utc)
            return (utc_value + standard_offset).replace(tzinfo=None)

        return value.replace(tzinfo=None)

    @classmethod
    def _hours_since_reference_day(
        cls,
        value: datetime,
        reference_day: date,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> float:
        adjusted = cls._adjusted_datetime(value, use_daylight_saving_time, standard_offset)
        day_delta = (adjusted.date() - reference_day).days
        return (
            day_delta * 24.0
            + adjusted.hour
            + adjusted.minute / 60.0
            + adjusted.second / 3600.0
        )

    def _resolve_morning_event(
        self,
        value: datetime,
        day: date,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> float:
        hours = self._hours_since_reference_day(value, day, use_daylight_saving_time, standard_offset)
        if hours > 12.0:
            return hours - 24.0
        return hours

    def _resolve_evening_event(
        self,
        value: datetime,
        day: date,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> float:
        hours = self._hours_since_reference_day(value, day, use_daylight_saving_time, standard_offset)
        if hours < 12.0:
            return hours + 24.0
        return hours

    def civil_dawn(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dawn(self._observer, day, tzinfo=self._tz, depression=Depression.CIVIL)
        return self._resolve_morning_event(value, day, use_daylight_saving_time, standard_offset)

    def civil_dusk(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dusk(self._observer, day, tzinfo=self._tz, depression=Depression.CIVIL)
        return self._resolve_evening_event(value, day, use_daylight_saving_time, standard_offset)

    def nautical_dawn(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dawn(self._observer, day, tzinfo=self._tz, depression=Depression.NAUTICAL)
        return self._resolve_morning_event(value, day, use_daylight_saving_time, standard_offset)

    def nautical_dusk(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dusk(self._observer, day, tzinfo=self._tz, depression=Depression.NAUTICAL)
        return self._resolve_evening_event(value, day, use_daylight_saving_time, standard_offset)

    def astronomical_dawn(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dawn(self._observer, day, tzinfo=self._tz, depression=Depression.ASTRONOMICAL)
        return self._resolve_morning_event(value, day, use_daylight_saving_time, standard_offset)

    def astronomical_dusk(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
        standard_offset: Optional[timedelta] = None,
    ) -> float:
        value = dusk(self._observer, day, tzinfo=self._tz, depression=Depression.ASTRONOMICAL)
        return self._resolve_evening_event(value, day, use_daylight_saving_time, standard_offset)
