"""Dialog for selecting a date with a calendar widget."""
from __future__ import annotations

from datetime import date

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QCalendarWidget,
    QPushButton,
)


class DatePickerDialog(QDialog):
    """Modal dialog for selecting a date from a calendar."""

    def __init__(self, parent=None, initial_date: date | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setModal(True)
        self.resize(400, 350)

        layout = QVBoxLayout()

        self._calendar = QCalendarWidget()
        if initial_date:
            self._calendar.setSelectedDate(initial_date)
        else:
            self._calendar.setSelectedDate(date.today())

        layout.addWidget(self._calendar)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self._selected_date = initial_date or date.today()
        self._calendar.clicked.connect(self._on_date_clicked)

    def _on_date_clicked(self, qdate) -> None:
        """Update selected date when user clicks on calendar."""
        self._selected_date = qdate.toPyDate()

    def selected_date(self) -> date:
        """Return the selected date."""
        return self._selected_date
