"""Main application window."""
from __future__ import annotations

from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from astronomy.annual_event_service import AnnualSolarEventService
from astronomy.daily_elevation_service import DailyElevationService
from config.locations import LocationRegistry
from gui.dialogs.analytical_view_dialog import AnalyticalViewDialog
from gui.dialogs.daily_altitude_dialog import DailyAltitudeDialog
from gui.dialogs.date_picker_dialog import DatePickerDialog
from gui.dialogs.location_selector_dialog import LocationSelectorDialog
from gui.widgets.chart_widget import MatplotlibChartWidget
from visualization.annual_sun_chart import AnnualSunChart
from visualization.display_settings import ChartDisplaySettings


class MainWindow(QMainWindow):
    """Main GUI for annual solar/twilight visualization."""

    def __init__(self) -> None:
        super().__init__()
        self._location = LocationRegistry.ulm()
        self._event_service = AnnualSolarEventService(self._location)
        self._daily_service = DailyElevationService(self._location)
        self._chart = AnnualSunChart()
        self._display_settings = ChartDisplaySettings(
            show_legend=True,
            use_daylight_saving_time=True,
            show_equinox_solstice_markers=True,
            show_grid=True,
            show_twilight_areas=True,
        )
        self._selected_date = date.today()

        self.setWindowTitle("Astronomy Planner - Annual Solar and Twilight Diagram")
        self.resize(1300, 850)

        root = QWidget(self)
        root_layout = QVBoxLayout()

        controls_layout = QHBoxLayout()
        self._location_label = QLabel("")
        self._location_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._update_location_label()

        select_location_button = QPushButton("Choose Location")
        select_location_button.clicked.connect(self._open_location_selector)

        year_label = QLabel("Year:")
        self._year_spin = QSpinBox()
        self._year_spin.setRange(1900, 2200)
        self._year_spin.setValue(date.today().year)
        self._year_spin.valueChanged.connect(self._refresh_chart)

        date_label = QLabel("Date:")
        self._date_edit = QDateEdit()
        self._date_edit.setDate(self._selected_date)
        self._date_edit.dateChanged.connect(self._on_date_changed)

        select_date_button = QPushButton("Select Date (Calendar)")
        select_date_button.clicked.connect(self._open_date_picker)

        now_button = QPushButton("Now")
        now_button.clicked.connect(self._reset_to_today)

        daily_altitude_button = QPushButton("Daily Altitude")
        daily_altitude_button.clicked.connect(self._open_daily_altitude_dialog)

        analytical_view_button = QPushButton("Analytical View")
        analytical_view_button.clicked.connect(self._open_analytical_view_dialog)

        self._legend_checkbox = QCheckBox("Show Legend")
        self._legend_checkbox.setChecked(self._display_settings.show_legend)
        self._legend_checkbox.toggled.connect(self._on_legend_toggled)

        self._dst_checkbox = QCheckBox("Use DST")
        self._dst_checkbox.setChecked(self._display_settings.use_daylight_saving_time)
        self._dst_checkbox.toggled.connect(self._on_dst_toggled)

        self._seasonal_markers_checkbox = QCheckBox("Show Equinox/Solstice")
        self._seasonal_markers_checkbox.setChecked(self._display_settings.show_equinox_solstice_markers)
        self._seasonal_markers_checkbox.toggled.connect(self._on_seasonal_markers_toggled)

        refresh_button = QPushButton("Generate Chart")
        refresh_button.clicked.connect(self._refresh_chart)

        controls_layout.addWidget(self._location_label, stretch=1)
        controls_layout.addWidget(select_location_button)
        controls_layout.addWidget(year_label)
        controls_layout.addWidget(self._year_spin)
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self._date_edit)
        controls_layout.addWidget(select_date_button)
        controls_layout.addWidget(now_button)
        controls_layout.addWidget(daily_altitude_button)
        controls_layout.addWidget(analytical_view_button)
        controls_layout.addWidget(self._legend_checkbox)
        controls_layout.addWidget(self._dst_checkbox)
        controls_layout.addWidget(self._seasonal_markers_checkbox)
        controls_layout.addWidget(refresh_button)

        self._chart_widget = MatplotlibChartWidget(self)
        self._chart.attach_figure(self._chart_widget.figure)

        root_layout.addLayout(controls_layout)
        root_layout.addWidget(self._chart_widget, stretch=1)

        root.setLayout(root_layout)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Time mode: Local civil time (DST enabled)")

        self._refresh_chart()

    def _update_location_label(self) -> None:
        self._location_label.setText(
            f"Location: {self._location.name}, {self._location.region}, {self._location.country}"
        )

    def _open_location_selector(self) -> None:
        dialog = LocationSelectorDialog(self, initial_location=self._location)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        selected_location = dialog.selected_location
        if selected_location is None:
            return

        self._location = selected_location
        self._event_service = AnnualSolarEventService(self._location)
        self._daily_service = DailyElevationService(self._location)
        self._update_location_label()

        # Reset date to today when location changes
        self._selected_date = date.today()
        self._date_edit.blockSignals(True)
        self._date_edit.setDate(self._selected_date)
        self._date_edit.blockSignals(False)
        self._year_spin.blockSignals(True)
        self._year_spin.setValue(self._selected_date.year)
        self._year_spin.blockSignals(False)

        self._refresh_chart()

    def _on_date_changed(self, new_date) -> None:
        self._selected_date = new_date.toPyDate()
        self._refresh_chart()

    def _reset_to_today(self) -> None:
        self._selected_date = date.today()
        self._date_edit.blockSignals(True)
        self._date_edit.setDate(self._selected_date)
        self._date_edit.blockSignals(False)
        self._year_spin.blockSignals(True)
        self._year_spin.setValue(self._selected_date.year)
        self._year_spin.blockSignals(False)
        self._refresh_chart()

    def _open_date_picker(self) -> None:
        """Open a calendar dialog for date selection."""
        dialog = DatePickerDialog(self, initial_date=self._selected_date)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        selected_date = dialog.selected_date()
        self._selected_date = selected_date

        # Block signals on both controls to prevent feedback loops
        self._date_edit.blockSignals(True)
        self._year_spin.blockSignals(True)

        # Update both controls while signals are blocked
        self._date_edit.setDate(self._selected_date)
        self._year_spin.setValue(self._selected_date.year)

        # Unblock signals after all updates are complete
        self._date_edit.blockSignals(False)
        self._year_spin.blockSignals(False)

        # Refresh chart explicitly after all controls are updated
        self._refresh_chart()

    def _open_daily_altitude_dialog(self) -> None:
        dialog = DailyAltitudeDialog(self)
        
        elevations = self._daily_service.elevation_for_day(
            self._selected_date,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        phase_grid = self._daily_service.phase_grid_for_day(
            self._selected_date,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        azimuths = self._daily_service.azimuth_for_day(
            self._selected_date,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        daily_events = self._daily_service.daily_events(
            self._selected_date,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        
        dialog.update_data(
            self._selected_date,
            elevations,
            phase_grid,
            daily_events,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
            azimuths=azimuths,
        )
        dialog.exec()

    def _open_analytical_view_dialog(self) -> None:
        dialog = AnalyticalViewDialog(self)
        
        year = self._year_spin.value()
        frame = self._event_service.annual_dataframe(
            year,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        phase_grid = self._event_service.annual_phase_grid(
            year,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        
        dialog.update_data(frame, year, phase_grid, self._location)
        dialog.exec()

    def _on_legend_toggled(self, checked: bool) -> None:
        self._display_settings = ChartDisplaySettings(
            show_legend=checked,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
            show_equinox_solstice_markers=self._display_settings.show_equinox_solstice_markers,
            show_grid=self._display_settings.show_grid,
            show_twilight_areas=self._display_settings.show_twilight_areas,
        )
        self._chart.set_legend_visible(checked)
        self._chart_widget.redraw()

    def _on_dst_toggled(self, checked: bool) -> None:
        self._display_settings = ChartDisplaySettings(
            show_legend=self._display_settings.show_legend,
            use_daylight_saving_time=checked,
            show_equinox_solstice_markers=self._display_settings.show_equinox_solstice_markers,
            show_grid=self._display_settings.show_grid,
            show_twilight_areas=self._display_settings.show_twilight_areas,
        )
        self._refresh_chart()

    def _on_seasonal_markers_toggled(self, checked: bool) -> None:
        self._display_settings = ChartDisplaySettings(
            show_legend=self._display_settings.show_legend,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
            show_equinox_solstice_markers=checked,
            show_grid=self._display_settings.show_grid,
            show_twilight_areas=self._display_settings.show_twilight_areas,
        )
        self._chart.set_seasonal_markers_visible(checked)
        self._chart_widget.redraw()

    def _refresh_chart(self) -> None:
        year = self._year_spin.value()
        frame = self._event_service.annual_dataframe(
            year,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        phase_grid = self._event_service.annual_phase_grid(
            year,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )
        extremes = self._event_service.sunrise_sunset_extremes(
            year,
            use_daylight_saving_time=self._display_settings.use_daylight_saving_time,
        )

        if self._display_settings.use_daylight_saving_time:
            mode_text = "Local civil time (DST enabled)"
        else:
            mode_text = "Standard time only (DST disabled)"

        title = (
            f"Annual Solar and Twilight Diagram - {self._location.name}, "
            f"{self._location.country} ({year}) [{mode_text}]"
        )
        self._chart.update_data(frame, title, self._display_settings, phase_grid, selected_date=self._selected_date, extremes=extremes)
        self._chart_widget.redraw()
        self.statusBar().showMessage(
            f"Time mode: {mode_text} | Location: {self._location.name}, {self._location.country}"
        )

