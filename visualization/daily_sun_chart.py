"""Daily sun altitude chart rendering."""
from __future__ import annotations

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from visualization.chart_renderer import ChartRenderer


class DailySunChart:
    """Renders sun altitude throughout a single day."""

    def __init__(self) -> None:
        self._renderer = ChartRenderer()
        self._figure: Figure | None = None
        self._axes: Axes | None = None
        self._current_time_artist: list = []
        self._elevations: np.ndarray | None = None
        self._azimuths: np.ndarray | None = None
        self._info_text_artist = None

    def attach_figure(self, figure: Figure) -> None:
        self._figure = figure
        self._figure.clear()
        self._axes = self._figure.add_subplot(111)

    @staticmethod
    def _background_legend_handles() -> list[Patch]:
        return [
            Patch(facecolor="#b9e5ff", edgecolor="none", label="Daylight", alpha=0.8),
            Patch(facecolor="#8ecae6", edgecolor="none", label="Civil Twilight", alpha=0.65),
            Patch(facecolor="#5d84a6", edgecolor="none", label="Nautical Twilight", alpha=0.6),
            Patch(facecolor="#274c77", edgecolor="none", label="Astronomical Twilight", alpha=0.7),
            Patch(facecolor="#0b1f3a", edgecolor="none", label="Astronomical Night", alpha=0.75),
        ]

    def _plot_background_phases(
        self,
        ax: Axes,
        phase_grid: np.ndarray,
    ) -> None:
        """Plot colored background for twilight phases."""
        colormap = ListedColormap(["#b9e5ff", "#8ecae6", "#5d84a6", "#274c77", "#0b1f3a"])
        
        times = np.arange(0, 1440)
        y_edges = np.linspace(-90, 90, 101)
        
        # Create 2D grid for pcolormesh
        phase_2d = np.tile(phase_grid[:, np.newaxis], (1, 100))
        time_edges = np.append(times, times[-1] + 1)
        
        ax.pcolormesh(
            time_edges / 60.0,  # Convert minutes to hours
            y_edges,
            phase_2d.T,
            cmap=colormap,
            shading="flat",
            alpha=0.78,
            zorder=0,
            antialiased=False,
            rasterized=True,
        )

    @staticmethod
    def _hours_from_minutes(minutes: float) -> float:
        """Convert minutes since midnight to hours."""
        return minutes / 60.0

    @staticmethod
    def _azimuth_to_compass(azimuth_degrees: float) -> str:
        """Convert azimuth angle to compass direction."""
        # Normalize to 0-360
        azimuth_degrees = azimuth_degrees % 360.0
        
        # 8-point compass: N, NE, E, SE, S, SW, W, NW
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        index = int((azimuth_degrees + 22.5) / 45.0)
        return directions[index]

    @staticmethod
    def _format_time(hours: float) -> str:
        """Format decimal hours to HH:MM format."""
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h:02d}:{m:02d}"

    def _get_hover_info(self, time_hours: float) -> str:
        """Get formatted info for the hover position."""
        if self._elevations is None or self._azimuths is None:
            return ""
        
        # Convert hours to minute index
        minute = int(time_hours * 60)
        if minute < 0 or minute >= len(self._elevations):
            return ""
        
        time_str = self._format_time(time_hours)
        altitude = self._elevations[minute]
        az = self._azimuths[minute]
        compass = self._azimuth_to_compass(az)
        
        info = f"Time: {time_str}\nAltitude: {altitude:.1f}°\nAzimuth: {compass} ({az:.0f}°)"
        return info

    def _update_hover_info(self, time_hours: float | None) -> None:
        """Update the hover information display."""
        if self._info_text_artist is not None:
            self._info_text_artist.remove()
            self._info_text_artist = None
        
        if time_hours is None or self._axes is None:
            return
        
        info = self._get_hover_info(time_hours)
        if not info:
            return
        
        self._info_text_artist = self._axes.text(
            0.98, 0.97, info,
            transform=self._axes.transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontsize=9,
            family='monospace',
            zorder=10,
        )

    def _plot_altitude_curve(
        self,
        ax: Axes,
        elevations: np.ndarray,
    ) -> None:
        """Plot the sun altitude curve."""
        times_hours = np.arange(1440) / 60.0
        ax.plot(times_hours, elevations, color="#FFD700", linewidth=2.5, label="Sun Altitude", zorder=6)

    def _draw_twilight_lines(self, ax: Axes) -> None:
        """Draw horizontal lines for twilight boundaries."""
        ax.axhline(y=-6, color="#f97316", linestyle="--", linewidth=1, alpha=0.7, zorder=5, label="Civil Twilight (-6°)")
        ax.axhline(y=-12, color="#8b5cf6", linestyle="--", linewidth=1, alpha=0.7, zorder=5, label="Nautical Twilight (-12°)")
        ax.axhline(y=-18, color="#1d4ed8", linestyle="--", linewidth=1, alpha=0.7, zorder=5, label="Astronomical Twilight (-18°)")
        ax.axhline(y=0, color="#333333", linestyle="-", linewidth=0.8, alpha=0.5, zorder=4)

    def _clear_current_time_marker(self) -> None:
        self._current_time_artist = []

    def _draw_current_time_marker(self, ax: Axes, current_hours: float | None) -> None:
        """Draw a vertical line at the current local time."""
        self._clear_current_time_marker()
        if current_hours is None:
            return
        
        # Normalize current_hours to 0-24 range
        current_hours = current_hours % 24.0
        
        line = ax.axvline(x=current_hours, color="#22c55e", linestyle="-", linewidth=1.5, alpha=0.8, zorder=5)
        text = ax.text(
            current_hours,
            85,
            "Now",
            rotation=90,
            va="bottom",
            ha="center",
            fontsize=8,
            color="#22c55e",
            alpha=0.9,
            zorder=6,
        )
        self._current_time_artist.extend([line, text])

    def update_data(
        self,
        day_str: str,
        elevations: np.ndarray,
        phase_grid: np.ndarray,
        current_hours: float | None = None,
        azimuths: np.ndarray | None = None,
    ) -> Figure:
        """Update the chart with new data."""
        if self._figure is None or self._axes is None:
            self.attach_figure(self._renderer.create_figure())

        assert self._figure is not None
        assert self._axes is not None

        ax = self._axes
        ax.clear()

        self._elevations = elevations
        self._azimuths = azimuths if azimuths is not None else np.zeros_like(elevations)
        self._info_text_artist = None

        self._plot_background_phases(ax, phase_grid)
        self._plot_altitude_curve(ax, elevations)
        self._draw_twilight_lines(ax)
        self._draw_current_time_marker(ax, current_hours)

        ax.set_xlim(0, 24)
        ax.set_ylim(-90, 90)
        ax.set_xlabel("Time of Day (hours)")
        ax.set_ylabel("Sun Altitude (degrees)")
        ax.set_xticks(range(0, 25, 2))
        ax.set_yticks(range(-90, 91, 10))
        ax.grid(True, linestyle="--", alpha=0.25)
        ax.set_axisbelow(True)

        ax.set_title(f"Sun Altitude During the Day - {day_str}")

        background_handles = self._background_legend_handles()
        line_handles, line_labels = ax.get_legend_handles_labels()
        all_handles = background_handles + line_handles
        all_labels = [h.get_label() for h in background_handles] + line_labels
        ax.legend(all_handles, all_labels, loc="upper left", fontsize=8, ncol=2)

        return self._figure
