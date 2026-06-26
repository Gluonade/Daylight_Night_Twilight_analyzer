"""Shared astronomy data models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class GeoLocation:
    """Reusable geographic location model."""

    name: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str


@dataclass(frozen=True)
class DailySolarEvents:
    """All relevant solar/twilight event times for one day."""

    day: date
    solar_noon: Optional[float]
    sunrise: Optional[float]
    sunset: Optional[float]
    civil_dawn: Optional[float]
    civil_dusk: Optional[float]
    nautical_dawn: Optional[float]
    nautical_dusk: Optional[float]
    astronomical_dawn: Optional[float]
    astronomical_dusk: Optional[float]
