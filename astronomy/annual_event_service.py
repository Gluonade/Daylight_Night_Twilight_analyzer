"""Builds annual solar/twilight datasets."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from astral.sun import elevation

from astronomy.data_models import DailySolarEvents, GeoLocation
from astronomy.location import ObserverFactory
from astronomy.solar_calculator import SolarCalculator
from astronomy.twilight_calculator import TwilightCalculator


class AnnualSolarEventService:
    """Creates one data point per day for a full year."""

    def __init__(self, location: GeoLocation) -> None:
        self._location = location
        self._observer = ObserverFactory.create(location)
        self._timezone = ZoneInfo(location.timezone)
        self._solar = SolarCalculator(location)
        self._twilight = TwilightCalculator(location)
        self._phase_cache: dict[tuple[int, bool], np.ndarray] = {}

    @staticmethod
    def _safe(callable_fn) -> Optional[float]:
        try:
            return float(callable_fn())
        except (ValueError, OverflowError):
            return None

    @staticmethod
    def _standard_offset_for_year(timezone_name: str, year: int) -> timedelta:
        tz = ZoneInfo(timezone_name)
        monthly_offsets = []
        for month in range(1, 13):
            offset = datetime(year, month, 1, 12, 0, tzinfo=tz).utcoffset()
            if offset is not None:
                monthly_offsets.append(offset)

        if not monthly_offsets:
            raise ValueError(f"Could not determine standard offset for timezone: {timezone_name}")

        return min(monthly_offsets)

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

    def _build_daily_events(
        self,
        day: date,
        use_daylight_saving_time: bool,
        standard_offset: Optional[timedelta],
    ) -> DailySolarEvents:
        return DailySolarEvents(
            day=day,
            solar_noon=self._safe(
                lambda: self._solar.solar_noon(day, use_daylight_saving_time, standard_offset)
            ),
            sunrise=self._safe(
                lambda: self._solar.sunrise(day, use_daylight_saving_time, standard_offset)
            ),
            sunset=self._safe(
                lambda: self._solar.sunset(day, use_daylight_saving_time, standard_offset)
            ),
            civil_dawn=self._safe(
                lambda: self._twilight.civil_dawn(day, use_daylight_saving_time, standard_offset)
            ),
            civil_dusk=self._safe(
                lambda: self._twilight.civil_dusk(day, use_daylight_saving_time, standard_offset)
            ),
            nautical_dawn=self._safe(
                lambda: self._twilight.nautical_dawn(day, use_daylight_saving_time, standard_offset)
            ),
            nautical_dusk=self._safe(
                lambda: self._twilight.nautical_dusk(day, use_daylight_saving_time, standard_offset)
            ),
            astronomical_dawn=self._safe(
                lambda: self._twilight.astronomical_dawn(day, use_daylight_saving_time, standard_offset)
            ),
            astronomical_dusk=self._safe(
                lambda: self._twilight.astronomical_dusk(day, use_daylight_saving_time, standard_offset)
            ),
        )

    def annual_dataframe(self, year: int, use_daylight_saving_time: bool = True) -> pd.DataFrame:
        start = date(year, 1, 1)
        end = date(year, 12, 31)

        standard_offset: Optional[timedelta] = None
        if not use_daylight_saving_time:
            standard_offset = self._standard_offset_for_year(self._location.timezone, year)

        days = []
        current = start
        while current <= end:
            days.append(
                self._build_daily_events(current, use_daylight_saving_time, standard_offset)
            )
            current += timedelta(days=1)

        data = [
            {
                "date": d.day,
                "day_of_year": d.day.timetuple().tm_yday,
                "solar_noon": d.solar_noon,
                "sunrise": d.sunrise,
                "sunset": d.sunset,
                "civil_dawn": d.civil_dawn,
                "civil_dusk": d.civil_dusk,
                "nautical_dawn": d.nautical_dawn,
                "nautical_dusk": d.nautical_dusk,
                "astronomical_dawn": d.astronomical_dawn,
                "astronomical_dusk": d.astronomical_dusk,
            }
            for d in days
        ]

        frame = pd.DataFrame(data)
        frame["date"] = pd.to_datetime(frame["date"])
        return frame

    def annual_phase_grid(self, year: int, use_daylight_saving_time: bool = True) -> np.ndarray:
        cache_key = (year, use_daylight_saving_time)
        if cache_key in self._phase_cache:
            return self._phase_cache[cache_key].copy()

        start = date(year, 1, 1)
        end = date(year, 12, 31)
        total_days = (end - start).days + 1
        phase_grid = np.full((1440, total_days), 4, dtype=np.uint8)

        standard_offset: Optional[timedelta] = None
        if not use_daylight_saving_time:
            standard_offset = self._standard_offset_for_year(self._location.timezone, year)

        for day_index in range(total_days):
            current_day = start + timedelta(days=day_index)
            for minute in range(1440):
                dt = self._display_datetime(
                    current_day,
                    minute,
                    use_daylight_saving_time,
                    standard_offset,
                )
                phase_grid[minute, day_index] = self._phase_code_for_elevation(
                    elevation(self._observer, dt)
                )

        self._phase_cache[cache_key] = phase_grid
        return phase_grid.copy()

    def sunrise_sunset_extremes(self, year: int, use_daylight_saving_time: bool = True) -> dict[str, dict | None]:
        """Find the dates and seasons of earliest/latest sunrise and earliest/latest sunset.
        
        Returns dict with keys for each extreme, each containing:
        - 'date': the date of the extreme
        - 'season': 'summer' or 'winter' (based on proximity to solstices)
        """
        frame = self.annual_dataframe(year, use_daylight_saving_time)
        
        # Filter out None/NaN values
        sunrise_valid = frame[frame['sunrise'].notna()].copy()
        sunset_valid = frame[frame['sunset'].notna()].copy()
        
        extremes = {
            'earliest_sunrise': None,
            'latest_sunrise': None,
            'earliest_sunset': None,
            'latest_sunset': None,
        }
        
        # Find extremes
        if not sunrise_valid.empty:
            # Wrap sunrise times and find extremes (accounting for year boundary)
            sunrise_wrapped = sunrise_valid['sunrise'].apply(lambda x: x % 24.0)
            earliest_idx = sunrise_wrapped.idxmin()
            latest_idx = sunrise_wrapped.idxmax()
            
            earliest_date = sunrise_valid.loc[earliest_idx, 'date'].date()
            latest_date = sunrise_valid.loc[latest_idx, 'date'].date()
            
            extremes['earliest_sunrise'] = {
                'date': earliest_date,
                'season': self._determine_season(earliest_date, year)
            }
            extremes['latest_sunrise'] = {
                'date': latest_date,
                'season': self._determine_season(latest_date, year)
            }
        
        if not sunset_valid.empty:
            # Wrap sunset times and find extremes (accounting for year boundary)
            sunset_wrapped = sunset_valid['sunset'].apply(lambda x: x % 24.0)
            earliest_idx = sunset_wrapped.idxmin()
            latest_idx = sunset_wrapped.idxmax()
            
            earliest_date = sunset_valid.loc[earliest_idx, 'date'].date()
            latest_date = sunset_valid.loc[latest_idx, 'date'].date()
            
            extremes['earliest_sunset'] = {
                'date': earliest_date,
                'season': self._determine_season(earliest_date, year)
            }
            extremes['latest_sunset'] = {
                'date': latest_date,
                'season': self._determine_season(latest_date, year)
            }
        
        return extremes

    @staticmethod
    def _determine_season(day: date, year: int) -> str:
        """Determine if a date is closer to summer or winter solstice.
        
        Summer solstice (northern hemisphere): ~June 21 (day 172)
        Winter solstice (northern hemisphere): ~December 21 (day 355)
        """
        day_of_year = day.timetuple().tm_yday
        
        # Distance to summer solstice
        summer_day = 172
        dist_to_summer = min(abs(day_of_year - summer_day), 365 - abs(day_of_year - summer_day))
        
        # Distance to winter solstice
        winter_day = 355
        dist_to_winter = min(abs(day_of_year - winter_day), 365 - abs(day_of_year - winter_day))
        
        return 'summer' if dist_to_summer < dist_to_winter else 'winter'
