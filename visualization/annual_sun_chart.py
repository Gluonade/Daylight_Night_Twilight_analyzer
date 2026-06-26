"""Annual solar and twilight chart rendering."""
from __future__ import annotations

from datetime import date, datetime

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from visualization.chart_renderer import ChartRenderer
from visualization.display_settings import ChartDisplaySettings


class AnnualSunChart:
    """Renders annual daylight and twilight progression."""

    def __init__(self) -> None:
        self._renderer = ChartRenderer()
        self._figure: Figure | None = None
        self._axes: Axes | None = None
        self._legend: Legend | None = None
        self._seasonal_marker_artists: list = []
        self._today_marker_artists: list = []
        self._extremes_marker_artists: list = []

    def attach_figure(self, figure: Figure) -> None:
        self._figure = figure
        self._figure.clear()
        self._axes = self._figure.add_subplot(111)

    @staticmethod
    def _wrap_series(series: pd.Series) -> pd.Series:
        wrapped = series.copy()
        valid = wrapped.notna()
        wrapped.loc[valid] = wrapped.loc[valid] % 24.0
        return wrapped

    @staticmethod
    def _split_discontinuities(series: pd.Series, jump_threshold_hours: float = 8.0) -> pd.Series:
        result = series.copy()
        previous: float | None = None
        for idx, value in result.items():
            if not pd.notna(value):
                previous = None
                continue
            current = float(value)
            if previous is not None and abs(current - previous) > jump_threshold_hours:
                result.at[idx] = np.nan
            previous = current
        return result

    def _background_legend_handles(self) -> list[Patch]:
        return [
            Patch(facecolor="#b9e5ff", edgecolor="none", label="Daylight", alpha=0.8),
            Patch(facecolor="#8ecae6", edgecolor="none", label="Civil Twilight", alpha=0.65),
            Patch(facecolor="#5d84a6", edgecolor="none", label="Nautical Twilight", alpha=0.6),
            Patch(facecolor="#274c77", edgecolor="none", label="Astronomical Twilight", alpha=0.7),
            Patch(facecolor="#0b1f3a", edgecolor="none", label="Astronomical Night", alpha=0.75),
        ]

    @staticmethod
    def _marker_legend_handle() -> Line2D:
        return Line2D([0], [0], color="#1f2937", linestyle=":", linewidth=1.4, label="Equinox/Solstice")

    @staticmethod
    def _seasonal_markers(year: int) -> list[tuple[date, str]]:
        return [
            (date(year, 3, 20), "Mar Equinox"),
            (date(year, 6, 21), "Jun Solstice"),
            (date(year, 9, 22), "Sep Equinox"),
            (date(year, 12, 21), "Dec Solstice"),
        ]

    def _clear_seasonal_markers(self) -> None:
        # Existing artists are discarded on axes clear during full redraw.
        self._seasonal_marker_artists = []

    def _clear_today_marker(self) -> None:
        self._today_marker_artists = []

    def _draw_seasonal_markers(self, ax: Axes, year: int) -> None:
        self._clear_seasonal_markers()
        for marker_date, label in self._seasonal_markers(year):
            x_value = pd.Timestamp(marker_date)
            line = ax.axvline(x=x_value, color="#1f2937", linestyle=":", linewidth=1.4, alpha=0.7, zorder=4)
            text = ax.text(
                x_value,
                23.8,
                label,
                rotation=90,
                va="top",
                ha="center",
                fontsize=7,
                color="#1f2937",
                alpha=0.85,
                zorder=5,
            )
            self._seasonal_marker_artists.extend([line, text])

    def set_seasonal_markers_visible(self, visible: bool) -> None:
        for artist in self._seasonal_marker_artists:
            artist.set_visible(visible)

    def _draw_selected_date_marker(self, ax: Axes, year: int, selected_date: date) -> None:
        self._clear_today_marker()
        if selected_date.year != year:
            return

        x_value = pd.Timestamp(selected_date)
        line = ax.axvline(x=x_value, color="#dc2626", linestyle="-", linewidth=1.8, alpha=0.9, zorder=7)
        label_text = "Today" if selected_date == datetime.now().date() else "Selected"
        text = ax.text(
            x_value,
            0.3,
            label_text,
            rotation=90,
            va="bottom",
            ha="center",
            fontsize=8,
            color="#dc2626",
            alpha=0.9,
            zorder=8,
        )
        self._today_marker_artists.extend([line, text])

    def _draw_today_marker_if_current_year(self, ax: Axes, year: int) -> None:
        """Legacy method for backward compatibility. Use _draw_selected_date_marker instead."""
        self._draw_selected_date_marker(ax, year, datetime.now().date())

    def _clear_extremes_markers(self) -> None:
        self._extremes_marker_artists = []

    def _draw_extremes_markers(self, ax: Axes, year: int, extremes: dict) -> None:
        """Draw vertical lines for sunrise/sunset extremes with season-based coloring."""
        self._clear_extremes_markers()
        
        # Map extremes to display info: (key, label, season_color_map)
        extremes_list = [
            ('earliest_sunrise', "Earliest Sunrise"),
            ('latest_sunrise', "Latest Sunrise"),
            ('earliest_sunset', "Earliest Sunset"),
            ('latest_sunset', "Latest Sunset"),
        ]
        
        for key, label in extremes_list:
            info = extremes.get(key)
            if info is None or not isinstance(info, dict):
                continue
            
            marker_date = info.get('date')
            season = info.get('season', 'winter')
            
            if marker_date is None or marker_date.year != year:
                continue
            
            # Color by season: red for summer, blue for winter
            color = "#dc2626" if season == 'summer' else "#2563eb"
            
            x_value = pd.Timestamp(marker_date)
            line = ax.axvline(x=x_value, color=color, linestyle="--", linewidth=1.3, alpha=0.7, zorder=3)
            text = ax.text(
                x_value,
                -8.0,
                label,
                rotation=90,
                va="top",
                ha="center",
                fontsize=6.5,
                color=color,
                alpha=0.8,
                zorder=4,
            )
            self._extremes_marker_artists.extend([line, text])

    def set_extremes_markers_visible(self, visible: bool) -> None:
        for artist in self._extremes_marker_artists:
            artist.set_visible(visible)

    def _plot_background_phases(
        self,
        ax: Axes,
        df: pd.DataFrame,
        settings: ChartDisplaySettings,
        phase_grid: np.ndarray,
    ) -> None:
        background_grid = phase_grid.copy()
        if not settings.show_twilight_areas:
            # Collapse twilight to night while preserving daylight.
            twilight_mask = (background_grid == 1) | (background_grid == 2) | (background_grid == 3)
            background_grid[twilight_mask] = 4

        colormap = ListedColormap(["#b9e5ff", "#8ecae6", "#5d84a6", "#274c77", "#0b1f3a"])
        day_numbers = mdates.date2num(df["date"])
        x_edges = np.append(day_numbers, day_numbers[-1] + 1.0)
        y_edges = np.linspace(0.0, 24.0, background_grid.shape[0] + 1)
        ax.pcolormesh(
            x_edges,
            y_edges,
            background_grid,
            cmap=colormap,
            shading="flat",
            alpha=0.78,
            zorder=0,
            antialiased=False,
            rasterized=True,
        )

    @staticmethod
    def _plot_wrapped_curve(
        ax: Axes,
        dates: pd.Series,
        raw_series: pd.Series,
        *,
        color: str,
        linewidth: float,
        label: str,
        linestyle: str = "-",
    ) -> None:
        wrapped = AnnualSunChart._wrap_series(raw_series)
        wrapped = AnnualSunChart._split_discontinuities(wrapped)
        ax.plot(dates, wrapped, color=color, linewidth=linewidth, linestyle=linestyle, label=label, zorder=6)

    @staticmethod
    def _plot_event_curves(ax: Axes, df: pd.DataFrame) -> None:
        date = df["date"]
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["solar_noon"],
            color="red",
            linewidth=1.6,
            label="Solar Noon",
        )
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["sunrise"],
            color="#ffcf33",
            linewidth=1.6,
            label="Sunrise",
        )
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["sunset"],
            color="#ffcf33",
            linewidth=1.6,
            linestyle="--",
            label="Sunset",
        )

        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["civil_dawn"],
            color="#f97316",
            linewidth=1.2,
            label="Civil Dawn",
        )
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["civil_dusk"],
            color="#f97316",
            linewidth=1.2,
            linestyle="--",
            label="Civil Dusk",
        )

        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["nautical_dawn"],
            color="#8b5cf6",
            linewidth=1.2,
            label="Nautical Dawn",
        )
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["nautical_dusk"],
            color="#8b5cf6",
            linewidth=1.2,
            linestyle="--",
            label="Nautical Dusk",
        )

        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["astronomical_dawn"],
            color="#1d4ed8",
            linewidth=1.2,
            label="Astronomical Dawn",
        )
        AnnualSunChart._plot_wrapped_curve(
            ax,
            date,
            df["astronomical_dusk"],
            color="#1d4ed8",
            linewidth=1.2,
            linestyle="--",
            label="Astronomical Dusk",
        )

    def update_data(
        self,
        df: pd.DataFrame,
        title: str,
        settings: ChartDisplaySettings,
        phase_grid: np.ndarray,
        selected_date: date | None = None,
        extremes: dict | None = None,
    ) -> Figure:
        if self._figure is None or self._axes is None:
            self.attach_figure(self._renderer.create_figure())

        assert self._figure is not None
        assert self._axes is not None

        ax = self._axes
        ax.clear()

        self._plot_background_phases(ax, df, settings, phase_grid)
        self._plot_event_curves(ax, df)

        year = int(df["date"].dt.year.iloc[0])
        self._draw_seasonal_markers(ax, year)
        if extremes is not None:
            self._draw_extremes_markers(ax, year, extremes)
        if selected_date is not None:
            self._draw_selected_date_marker(ax, year, selected_date)
        else:
            self._draw_today_marker_if_current_year(ax, year)
        self.set_seasonal_markers_visible(settings.show_equinox_solstice_markers)

        self._renderer.configure_date_axis(ax)
        self._renderer.configure_time_axis(ax)
        self._renderer.apply_common_style(ax, settings.show_grid)

        ax.set_title(title)
        background_handles = self._background_legend_handles()
        marker_handle = self._marker_legend_handle()
        line_handles, line_labels = ax.get_legend_handles_labels()
        all_handles = background_handles + [marker_handle] + line_handles
        all_labels = [handle.get_label() for handle in background_handles] + [marker_handle.get_label()] + line_labels
        self._legend = ax.legend(all_handles, all_labels, loc="upper left", fontsize=8, ncol=2)
        self.set_legend_visible(settings.show_legend)

        return self._figure

    def set_legend_visible(self, visible: bool) -> None:
        if self._legend is not None:
            self._legend.set_visible(visible)
