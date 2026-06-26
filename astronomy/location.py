"""Location adapter for astronomy libraries."""
from __future__ import annotations

from astral import Observer

from astronomy.data_models import GeoLocation


class ObserverFactory:
    """Factory creating Astral observers from domain locations."""

    @staticmethod
    def create(location: GeoLocation) -> Observer:
        return Observer(latitude=location.latitude, longitude=location.longitude)
