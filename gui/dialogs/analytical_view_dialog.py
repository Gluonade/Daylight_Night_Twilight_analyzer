"""Dialog for analytical view of solar data with duration and rate-of-change analysis."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QTabWidget,
)

from astronomy.data_models import GeoLocation
from gui.widgets.chart_widget import MatplotlibChartWidget
from visualization.analytical_chart import AnalyticalChart


class AnalyticalViewDialog(QDialog):
    """Dialog displaying analytical views of solar data with two tabs."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Analytical Solar Data View")
        self.resize(1400, 900)

        layout = QVBoxLayout()

        # Tab widget
        self._tabs = QTabWidget()

        # Duration Analysis tab
        self._duration_widget = MatplotlibChartWidget(self)
        self._duration_chart = AnalyticalChart()
        self._duration_chart.attach_figure(self._duration_widget.figure)
        self._tabs.addTab(self._duration_widget, "Duration Analysis")

        # Rate of Change Analysis tab
        self._rate_widget = MatplotlibChartWidget(self)
        self._rate_chart = AnalyticalChart()
        self._rate_chart.attach_figure(self._rate_widget.figure)
        self._tabs.addTab(self._rate_widget, "Rate of Change Analysis")

        layout.addWidget(self._tabs)

        # Save PNG button
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Current Tab as PNG…")
        save_button.clicked.connect(self._save_current_tab_as_png)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self._location: GeoLocation | None = None
        self._year: int | None = None

    def _save_current_tab_as_png(self) -> None:
        """Ask the user for a folder and save the current tab's chart as PNG."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select folder to save PNG",
            str(Path.home()),
        )
        if not folder:
            return

        tab_index = self._tabs.currentIndex()
        if tab_index == 0:
            widget = self._duration_widget
            tab_name = "duration_analysis"
        else:
            widget = self._rate_widget
            tab_name = "rate_of_change_analysis"

        loc_slug = ""
        if self._location is not None:
            loc_slug = self._location.name.replace(" ", "_").replace(",", "").lower() + "_"
        year_slug = f"{self._year}_" if self._year is not None else ""
        filename = f"{loc_slug}{year_slug}{tab_name}.png"
        output_path = Path(folder) / filename

        try:
            widget.figure.savefig(
                output_path,
                dpi=150,
                bbox_inches="tight",
                facecolor=widget.figure.get_facecolor(),
            )
            QMessageBox.information(self, "Saved", f"Chart saved to:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", f"Could not save PNG:\n{e}")

    def update_data(
        self,
        df: pd.DataFrame,
        year: int,
        phase_grid: np.ndarray,
        location: GeoLocation,
    ) -> None:
        """Update the dialog with annual data derived from the phase grid."""
        self._year = year
        self._location = location

        # Count minutes per phase for each day.
        # Phase codes: 0=daylight, 1=civil, 2=nautical, 3=astronomical twilight, 4=night
        n_days = phase_grid.shape[1]
        daytime_hours: list[float] = []
        twilight_hours: list[float] = []
        nighttime_hours: list[float] = []

        for day_idx in range(n_days):
            col = phase_grid[:, day_idx]
            daytime_hours.append(int(np.sum(col == 0)) / 60.0)
            twilight_hours.append(int(np.sum((col >= 1) & (col <= 3))) / 60.0)
            nighttime_hours.append(int(np.sum(col == 4)) / 60.0)

        # Build date-based x-axis matching DaytimeTwilightNighttimeChart
        import matplotlib.dates as mdates
        dates = [
            datetime(year, 1, 1) + timedelta(days=i)
            for i in range(n_days)
        ]
        x_dates = mdates.date2num(dates)

        polar_tag = "  [Polar Region]" if abs(location.latitude) >= 66.5 else ""
        duration_title = (
            f"{location.name}, {location.region}, {location.country}\n"
            f"Annual Day / Twilight / Night Duration — {year}{polar_tag}"
        )

        # Update Duration Analysis tab
        self._duration_chart.update_data(
            x_dates,
            [daytime_hours, twilight_hours, nighttime_hours],
            ["Daytime (Sun > 0°)", "Twilight (0° to \u221218°)", "Nighttime (Sun < \u221218°)"],
            ["#FFD700", "#FFA500", "#1a1a2e"],
            duration_title,
            "Date",
            "Duration (Hours:Minutes)",
            use_hhmm_y=True,
            use_date_x=True,
            year=year,
        )
        self._duration_widget.redraw()

        # Rate of change: smooth derivative via Savitzky-Golay, expressed in minutes/day.
        # window=15 days, poly=3 — preserves peak shape while eliminating 1-min quantization noise.
        # deriv=1, delta=1 gives d(hours)/d(day); multiply by 60 → minutes/day.
        _sg = lambda a: savgol_filter(a, window_length=15, polyorder=3, deriv=1, delta=1.0) * 60.0
        day_arr = np.array(daytime_hours)
        twi_arr = np.array(twilight_hours)
        ngt_arr = np.array(nighttime_hours)
        day_diff = _sg(day_arr)
        twi_diff = _sg(twi_arr)
        ngt_diff = _sg(ngt_arr)

        rate_title = (
            f"{location.name}, {location.region}, {location.country}\n"
            f"Rate of Change of Durations — {year}{polar_tag}"
        )

        # Update Rate of Change Analysis tab
        self._rate_chart.update_data(
            x_dates,
            [day_diff.tolist(), twi_diff.tolist(), ngt_diff.tolist()],
            ["Change in Daytime", "Change in Twilight", "Change in Nighttime"],
            ["#FFD700", "#FFA500", "#1a1a2e"],
            rate_title,
            "Date",
            "Rate of Change (minutes/day)",
            use_hhmm_y=False,
            use_date_x=True,
            year=year,
        )
        self._rate_widget.redraw()
