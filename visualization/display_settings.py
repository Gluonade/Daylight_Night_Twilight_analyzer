"""Display configuration for chart rendering."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChartDisplaySettings:
    """Centralized settings controlling chart appearance and time mode."""

    show_legend: bool = True
    use_daylight_saving_time: bool = True
    show_equinox_solstice_markers: bool = True
    show_grid: bool = True
    show_twilight_areas: bool = True
