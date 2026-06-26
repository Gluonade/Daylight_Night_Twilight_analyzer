"""Calculates sun elevation for each minute of a day."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import numpy as np
from astral.sun import elevation, azimuth

from astronomy.data_models import DailySolarEvents, GeoLocation
from astronomy.location import ObserverFactory
from astronomy.solar_calculator import SolarCalculator
from astronomy.twilight_calculator import TwilightCalculator


class DailyElevationService:
    """Calculates sun elevation throughout a day."""

    def __init__(self, location: GeoLocation) -> None:
        self._location = location
        self._observer = ObserverFactory.create(location)
        self._timezone = ZoneInfo(location.timezone)
        self._solar = SolarCalculator(location)
        self._twilight = TwilightCalculator(location)

    @staticmethod
    def _phase_code_for_elevation(elevation_degrees: float) -> int:
        # 0=daylight, 1=civil, 2=nautical, 3=astronomical, 4=night
        if elevation_degrees >= 0.0:
            return 0
        if elevation_degrees >= -6.0:
            return 1
        if elevation_degrees >= -12.0:
            return 2
        if elevation_degrees >= -18.0:
            return 3
        return 4

    @staticmethod
    def _standard_offset_for_day(timezone_name: str, day: date) -> timedelta:
        tz = ZoneInfo(timezone_name)
        offset = datetime(day.year, day.month, day.day, 12, 0, tzinfo=tz).utcoffset()
        if offset is None:
            raise ValueError(f"Could not determine offset for timezone: {timezone_name}")
        return offset

    def _display_datetime(
        self,
        day: date,
        minute_of_day: int,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> datetime:
        display_dt = datetime.combine(day, time(0, 0)) + timedelta(minutes=minute_of_day)
        if use_daylight_saving_time:
            return display_dt.replace(tzinfo=self._timezone)
        if standard_offset is None:
            raise ValueError("standard_offset is required when DST is disabled")
        return display_dt.replace(tzinfo=timezone(standard_offset))

    def elevation_for_day(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
    ) -> np.ndarray:
        """Return elevation array for each minute of the day."""
        standard_offset: Optional[timedelta] = None
        if not use_daylight_saving_time:
            standard_offset = self._standard_offset_for_day(self._location.timezone, day)

        elevations = np.zeros(1440)
        for minute in range(1440):
            dt = self._display_datetime(day, minute, use_daylight_saving_time, standard_offset)
            elevations[minute] = elevation(self._observer, dt)
        return elevations

    def phase_grid_for_day(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
    ) -> np.ndarray:
        """Return phase code array for each minute of the day."""
        standard_offset: Optional[timedelta] = None
        if not use_daylight_saving_time:
            standard_offset = self._standard_offset_for_day(self._location.timezone, day)

        phase_grid = np.zeros(1440, dtype=np.uint8)
        for minute in range(1440):
            dt = self._display_datetime(day, minute, use_daylight_saving_time, standard_offset)
            phase_grid[minute] = self._phase_code_for_elevation(elevation(self._observer, dt))
        return phase_grid

    def azimuth_for_day(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
    ) -> np.ndarray:
        """Return azimuth array (degrees from North) for each minute of the day."""
        standard_offset: Optional[timedelta] = None
        if not use_daylight_saving_time:
            standard_offset = self._standard_offset_for_day(self._location.timezone, day)

        azimuths = np.zeros(1440)
        for minute in range(1440):
            dt = self._display_datetime(day, minute, use_daylight_saving_time, standard_offset)
            azimuths[minute] = azimuth(self._observer, dt)
        return azimuths

    def daily_events(
        self,
        day: date,
        use_daylight_saving_time: bool = True,
    ) -> DailySolarEvents:
        """Get all solar events for the day."""
        return DailySolarEvents(
            day=day,
            solar_noon=self._safe(lambda: self._solar.solar_noon(day, use_daylight_saving_time)),
            sunrise=self._safe(lambda: self._solar.sunrise(day, use_daylight_saving_time)),
            sunset=self._safe(lambda: self._solar.sunset(day, use_daylight_saving_time)),
            civil_dawn=self._safe(lambda: self._twilight.civil_dawn(day, use_daylight_saving_time)),
            civil_dusk=self._safe(lambda: self._twilight.civil_dusk(day, use_daylight_saving_time)),
            nautical_dawn=self._safe(lambda: self._twilight.nautical_dawn(day, use_daylight_saving_time)),
            nautical_dusk=self._safe(lambda: self._twilight.nautical_dusk(day, use_daylight_saving_time)),
            astronomical_dawn=self._safe(lambda: self._twilight.astronomical_dawn(day, use_daylight_saving_time)),
            astronomical_dusk=self._safe(lambda: self._twilight.astronomical_dusk(day, use_daylight_saving_time)),
        )

    @staticmethod
    def _safe(callable_fn) -> Optional[float]:
        try:
            return float(callable_fn())
        except (ValueError, OverflowError):
            return None
