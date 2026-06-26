"""Shared Matplotlib rendering utilities."""
from __future__ import annotations

import matplotlib.dates as mdates
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class ChartRenderer:
    """Base renderer with consistent styling and axis formatting."""

    def create_figure(self) -> Figure:
        return Figure(figsize=(12, 7), constrained_layout=True)

    def configure_time_axis(self, ax: Axes) -> None:
        ax.set_ylim(0, 24)
        ax.set_yticks(range(0, 25, 2))
        ax.set_ylabel("Time of Day (hours)")

    def configure_date_axis(self, ax: Axes) -> None:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.set_xlabel("Date")

    def apply_common_style(self, ax: Axes, show_grid: bool) -> None:
        ax.grid(show_grid, linestyle="--", alpha=0.25)
        ax.set_axisbelow(True)
