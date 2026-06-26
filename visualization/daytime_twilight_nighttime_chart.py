"""Annual daytime, twilight, and nighttime duration chart."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.figure import Figure

from astronomy.data_models import GeoLocation


class DaytimeTwilightNighttimeChart:
    """Renders annual chart of daytime, twilight, and nighttime durations."""

    # Color scheme
    _COL_DAYTIME = "#FFD700"      # Gold/yellow
    _COL_TWILIGHT = "#FFA500"     # Orange
    _COL_NIGHTTIME = "#1a1a2e"    # Dark blue/night
    _COL_GRID = "#CCCCCC"
    _COL_BG = "#F7F7F7"

    def __init__(self) -> None:
        self._figure: Optional[Figure] = None
        self._location: Optional[GeoLocation] = None
        self._year: Optional[int] = None

    def _hours_to_hhmm(self, hours: float) -> str:
        """Convert decimal hours to HH:MM format."""
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h:02d}:{m:02d}"

    def _create_hhmm_formatter(self):
        """Create a formatter for time in Hours:Minutes."""
        def format_func(x, p=None):
            return self._hours_to_hhmm(x)
        return ticker.FuncFormatter(format_func)

    def generate(
        self,
        location: GeoLocation,
        year: int,
        daytime_hours: list[float],
        nighttime_hours: list[float],
        twilight_hours: list[float],
    ) -> Figure:
        """Generate the chart for the given location and data."""
        self._location = location
        self._year = year

        # Create figure
        fig = plt.figure(figsize=(14, 8))
        fig.patch.set_facecolor("#FFFFFF")
        ax = fig.add_subplot(111)

        # Generate x-axis data (dates)
        dates = []
        current = date(year, 1, 1)
        end = date(year, 12, 31)
        while current <= end:
            dates.append(datetime(current.year, current.month, current.day))
            current += timedelta(days=1)

        x_data = mdates.date2num(dates)

        # Plot the three curves
        ax.plot(
            x_data,
            daytime_hours,
            color=self._COL_DAYTIME,
            linewidth=2.5,
            label="Daytime (Sun > 0°)",
            zorder=5,
        )
        ax.plot(
            x_data,
            twilight_hours,
            color=self._COL_TWILIGHT,
            linewidth=2.5,
            label="Twilight (0° to -18°)",
            zorder=5,
        )
        ax.plot(
            x_data,
            nighttime_hours,
            color=self._COL_NIGHTTIME,
            linewidth=2.5,
            label="Nighttime (Sun < -18°)",
            zorder=5,
        )

        # Configure axes
        ax.set_facecolor(self._COL_BG)
        ax.set_xlim(x_data[0], x_data[-1])
        ax.set_ylim(0, 24)

        # Format Y-axis as HH:MM
        ax.yaxis.set_major_formatter(self._create_hhmm_formatter())
        ax.set_yticks(range(0, 25, 2))
        ax.set_ylabel("Duration (Hours:Minutes)", fontsize=11, fontweight="bold")

        # Format X-axis as dates
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.tick_params(axis="x", labelsize=9)
        ax.set_xlabel("Date", fontsize=11, fontweight="bold")

        # Grid
        ax.grid(True, color=self._COL_GRID, linewidth=0.5, alpha=0.6)
        ax.set_axisbelow(True)

        # Title
        polar_tag = "  [Polar Region]" if abs(location.latitude) >= 66.5 else ""
        ax.set_title(
            f"{location.name}, {location.region}, {location.country}\n"
            f"Annual Day / Twilight / Night Duration — {year}{polar_tag}",
            fontsize=13,
            fontweight="bold",
            pad=15,
        )

        # Legend
        ax.legend(
            loc="best",
            fontsize=10,
            frameon=True,
            framealpha=0.95,
            edgecolor="#cccccc",
        )

        plt.tight_layout()
        return fig

    def save(
        self,
        figure: Figure,
        output_path: str | Path,
    ) -> None:
        """Save the figure to a PNG file."""
        output_path = Path(output_path)
        figure.savefig(
            output_path,
            dpi=150,
            bbox_inches="tight",
            facecolor=figure.get_facecolor(),
        )
        plt.close(figure)
