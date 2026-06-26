"""Configured observing locations."""
from __future__ import annotations

from astronomy.data_models import GeoLocation
from config.world_locations import WorldLocationCatalog


class LocationRegistry:
    """Central location registry for current and future expansion."""

    @staticmethod
    def ulm() -> GeoLocation:
        location = WorldLocationCatalog.find_location("Europe", "Germany", "Ulm")
        if location is None:
            raise ValueError("Ulm location not found in world catalog")
        return location
