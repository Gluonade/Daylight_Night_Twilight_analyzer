"""Matplotlib chart widget for Qt."""
from __future__ import annotations

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class MatplotlibChartWidget(QWidget):
    """Embeds a Matplotlib figure plus toolbar into Qt."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._canvas = FigureCanvasQTAgg(Figure(figsize=(12, 7)))
        self._toolbar = NavigationToolbar2QT(self._canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self._toolbar)
        layout.addWidget(self._canvas)
        self.setLayout(layout)

    @property
    def figure(self) -> Figure:
        return self._canvas.figure

    def redraw(self) -> None:
        self._toolbar.update()
        self._canvas.draw_idle()

    def set_figure(self, figure: Figure) -> None:
        figure.set_canvas(self._canvas)
        self._canvas.figure = figure
        self.redraw()
