"""Analytical chart rendering for duration and rate-of-change analysis."""
from __future__ import annotations

from datetime import date, datetime

import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from visualization.chart_renderer import ChartRenderer


class AnalyticalChart:
    """Renders analytical charts for solar data."""

    _COL_GRID = "#CCCCCC"
    _COL_BG = "#F7F7F7"

    def __init__(self) -> None:
        self._renderer = ChartRenderer()
        self._figure: Figure | None = None
        self._axes: Axes | None = None

    def attach_figure(self, figure: Figure) -> None:
        self._figure = figure
        self._figure.clear()
        self._axes = self._figure.add_subplot(111)

    @staticmethod
    def _hhmm_formatter():
        def _fmt(x, p=None):
            h = int(x)
            m = int(round((x - h) * 60))
            return f"{h:02d}:{m:02d}"
        return ticker.FuncFormatter(_fmt)

    @staticmethod
    def _get_solstice_equinox_dates(year: int) -> dict[str, datetime]:
        """Get approximate dates for solstices and equinoxes for a given year."""
        return {
            "Spring Equinox": datetime(year, 3, 20),
            "Summer Solstice": datetime(year, 6, 21),
            "Autumn Equinox": datetime(year, 9, 22),
            "Winter Solstice": datetime(year, 12, 21),
        }

    def update_data(
        self,
        x_data: np.ndarray,
        data_series: list[list[float]],
        labels: list[str],
        colors: list[str],
        title: str,
        x_label: str,
        y_label: str,
        use_hhmm_y: bool = False,
        use_date_x: bool = False,
        year: int | None = None,
    ) -> Figure:
        """Update the chart with new data."""
        if self._figure is None or self._axes is None:
            self.attach_figure(self._renderer.create_figure())

        assert self._figure is not None
        assert self._axes is not None

        ax = self._axes
        ax.clear()

        for series, label, color in zip(data_series, labels, colors):
            ax.plot(x_data, series, color=color, linewidth=2.5, label=label, zorder=5)

        ax.set_facecolor(self._COL_BG)
        ax.set_xlabel(x_label, fontsize=11, fontweight="bold")
        ax.set_ylabel(y_label, fontsize=11, fontweight="bold")
        ax.set_title(title, fontsize=13, fontweight="bold", pad=15)
        ax.grid(True, color=self._COL_GRID, linewidth=0.5, alpha=0.6)
        ax.set_axisbelow(True)

        if use_date_x:
            ax.set_xlim(x_data[0], x_data[-1])
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
            ax.tick_params(axis="x", labelsize=9)
            
            # Add vertical lines for solstices and equinoxes
            if year is not None:
                solstice_equinox_dates = self._get_solstice_equinox_dates(year)
                line_colors = {
                    "Spring Equinox": "#2ecc71",
                    "Summer Solstice": "#e74c3c",
                    "Autumn Equinox": "#f39c12",
                    "Winter Solstice": "#3498db",
                }
                for event_name, event_date in solstice_equinox_dates.items():
                    event_x = mdates.date2num(event_date)
                    ax.axvline(x=event_x, color=line_colors[event_name], linestyle="--", 
                              linewidth=1.5, alpha=0.7, zorder=3)

        else:
            ax.set_xlim(0, 365)
            month_days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
            month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", ""]
            ax.set_xticks(month_days)
            ax.set_xticklabels(month_labels, fontsize=8)

        if use_hhmm_y:
            ax.set_ylim(0, 24)
            ax.set_yticks(range(0, 25, 2))
            ax.yaxis.set_major_formatter(self._hhmm_formatter())

        # Build legend with data series and optional solstice/equinox markers
        from matplotlib.lines import Line2D
        handles = [Line2D([0], [0], color=color, linewidth=2.5, label=label)
                   for label, color in zip(labels, colors)]
        
        if use_date_x and year is not None:
            solstice_equinox_dates = self._get_solstice_equinox_dates(year)
            line_colors = {
                "Spring Equinox": "#2ecc71",
                "Summer Solstice": "#e74c3c",
                "Autumn Equinox": "#f39c12",
                "Winter Solstice": "#3498db",
            }
            for event_name, event_color in line_colors.items():
                handles.append(Line2D([0], [0], color=event_color, linestyle="--", 
                                    linewidth=1.5, label=event_name))
        
        ax.legend(handles=handles, loc="best", fontsize=9, frameon=True, 
                 framealpha=0.95, edgecolor="#cccccc")


        self._figure.tight_layout()
        return self._figure
