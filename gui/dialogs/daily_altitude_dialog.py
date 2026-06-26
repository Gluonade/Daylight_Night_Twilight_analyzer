"""Dialog for displaying daily sun altitude with astronomical times table."""
from __future__ import annotations

from datetime import date, datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)

from astronomy.data_models import DailySolarEvents
from gui.widgets.chart_widget import MatplotlibChartWidget
from visualization.daily_sun_chart import DailySunChart


class DailyAltitudeDialog(QDialog):
    """Dialog displaying sun altitude chart and astronomical times for a day."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Daily Sun Altitude")
        self.resize(1200, 900)

        layout = QVBoxLayout()

        # Chart widget
        self._chart_widget = MatplotlibChartWidget(self)
        self._chart = DailySunChart()
        self._chart.attach_figure(self._chart_widget.figure)
        layout.addWidget(self._chart_widget, stretch=2)

        # Astronomical times table
        self._times_table = QTableWidget()
        self._times_table.setColumnCount(2)
        self._times_table.setHorizontalHeaderLabels(["Event", "Time"])
        self._times_table.horizontalHeader().setStretchLastSection(True)
        self._times_table.setMaximumHeight(200)
        layout.addWidget(self._times_table, stretch=1)

        self.setLayout(layout)
        
        # Connect mouse move event for hover info display
        self._chart_widget.figure.canvas.mpl_connect('motion_notify_event', self._on_mouse_move)

    def update_data(
        self,
        day: date,
        elevations,
        phase_grid,
        daily_events: DailySolarEvents,
        use_daylight_saving_time: bool = True,
        azimuths = None,
    ) -> None:
        """Update the dialog with new data."""
        day_str = day.strftime("%Y-%m-%d (%A)")
        
        # Calculate current time in hours if the displayed day is today
        current_hours = None
        if day == datetime.now().date():
            now = datetime.now()
            current_hours = now.hour + now.minute / 60.0 + now.second / 3600.0
        
        self._chart.update_data(day_str, elevations, phase_grid, current_hours, azimuths)
        self._chart_widget.redraw()

        self._update_times_table(daily_events)

    def _on_mouse_move(self, event) -> None:
        """Handle mouse movement to update hover info."""
        if event.xdata is None:
            self._chart._update_hover_info(None)
        else:
            self._chart._update_hover_info(event.xdata)
        self._chart_widget.redraw()

    def _time_str(self, hours: float | None) -> str:
        """Format time value for display."""
        if hours is None:
            return "N/A"
        
        # Handle wrap-around times
        if hours < 0:
            hours += 24
        elif hours >= 24:
            hours -= 24
        
        total_minutes = int(round(hours * 60))
        h = total_minutes // 60
        m = total_minutes % 60
        return f"{h:02d}:{m:02d}"

    def _update_times_table(self, daily_events: DailySolarEvents) -> None:
        """Populate the astronomical times table."""
        rows = [
            ("Sunrise", daily_events.sunrise),
            ("Sunset", daily_events.sunset),
            ("Civil Dawn", daily_events.civil_dawn),
            ("Civil Dusk", daily_events.civil_dusk),
            ("Nautical Dawn", daily_events.nautical_dawn),
            ("Nautical Dusk", daily_events.nautical_dusk),
            ("Astronomical Dawn", daily_events.astronomical_dawn),
            ("Astronomical Dusk", daily_events.astronomical_dusk),
        ]

        self._times_table.setRowCount(len(rows))
        for row_idx, (event_name, time_value) in enumerate(rows):
            event_item = QTableWidgetItem(event_name)
            event_item.setFlags(event_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            time_item = QTableWidgetItem(self._time_str(time_value))
            time_item.setFlags(time_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self._times_table.setItem(row_idx, 0, event_item)
            self._times_table.setItem(row_idx, 1, time_item)
