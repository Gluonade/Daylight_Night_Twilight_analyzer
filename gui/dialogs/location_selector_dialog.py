"""Location selector dialog with continent/country/locality hierarchy."""
from __future__ import annotations

from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import (
    QCompleter,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from astronomy.data_models import GeoLocation
from config.world_locations import WorldLocationCatalog


class LocationSelectorDialog(QDialog):
    """Dedicated sub-GUI to select a location by continent, country, and locality."""

    def __init__(self, parent=None, initial_location: GeoLocation | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Select Observation Location")
        self.resize(520, 260)

        self._selected_location: GeoLocation | None = None
        self._location_lookup: dict[str, GeoLocation] = {}
        self._search_lookup: dict[str, tuple[str, str, GeoLocation]] = {}

        root_layout = QVBoxLayout()
        form_layout = QFormLayout()

        search_row = QHBoxLayout()
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Type city or country (e.g., Tromso, Ushuaia, Tokyo)")
        self._search_button = QPushButton("Find")
        search_row.addWidget(self._search_input, stretch=1)
        search_row.addWidget(self._search_button)

        root_layout.addLayout(search_row)

        self._continent_combo = QComboBox()
        self._country_combo = QComboBox()
        self._locality_combo = QComboBox()

        self._details_label = QLabel("")
        self._details_label.setWordWrap(True)
        self._details_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        form_layout.addRow("Continent:", self._continent_combo)
        form_layout.addRow("Country:", self._country_combo)
        form_layout.addRow("Locality:", self._locality_combo)

        root_layout.addLayout(form_layout)
        root_layout.addWidget(self._details_label)

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self._button_box.accepted.connect(self._on_accept)
        self._button_box.rejected.connect(self.reject)
        root_layout.addWidget(self._button_box)

        self.setLayout(root_layout)

        self._continent_combo.currentTextChanged.connect(self._on_continent_changed)
        self._country_combo.currentTextChanged.connect(self._on_country_changed)
        self._locality_combo.currentTextChanged.connect(self._on_locality_changed)
        self._search_button.clicked.connect(self._apply_search_query)
        self._search_input.returnPressed.connect(self._apply_search_query)

        self._build_search_lookup()
        completer_model = QStringListModel(sorted(self._search_lookup.keys()))
        completer = QCompleter(completer_model, self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.activated.connect(self._apply_search_display)
        self._search_input.setCompleter(completer)

        self._populate_continents(initial_location)

    @property
    def selected_location(self) -> GeoLocation | None:
        return self._selected_location

    def _build_search_lookup(self) -> None:
        lookup: dict[str, tuple[str, str, GeoLocation]] = {}
        for continent in WorldLocationCatalog.continents():
            for country in WorldLocationCatalog.countries(continent):
                for location in WorldLocationCatalog.localities(continent, country):
                    label = f"{location.name}, {country} ({continent})"
                    if label in lookup:
                        label = f"{location.name}, {location.region}, {country} ({continent})"
                    lookup[label] = (continent, country, location)
        self._search_lookup = lookup

    def _select_location(self, continent: str, country: str, location: GeoLocation) -> None:
        self._continent_combo.setCurrentText(continent)
        self._country_combo.setCurrentText(country)

        for key, candidate in self._location_lookup.items():
            if (
                candidate.name == location.name
                and candidate.region == location.region
                and candidate.country == location.country
                and candidate.timezone == location.timezone
            ):
                self._locality_combo.setCurrentText(key)
                self._selected_location = candidate
                self._update_details(candidate)
                return

    def _apply_search_display(self, display_text: str) -> None:
        item = self._search_lookup.get(display_text)
        if item is None:
            return
        continent, country, location = item
        self._select_location(continent, country, location)

    def _apply_search_query(self) -> None:
        query = self._search_input.text().strip().lower()
        if not query:
            return

        exact = None
        ranked_matches: list[tuple[int, str, str, GeoLocation]] = []

        for display, (continent, country, location) in self._search_lookup.items():
            display_l = display.lower()
            locality_l = location.name.lower()
            country_l = country.lower()

            if query == display_l or query == locality_l:
                exact = (continent, country, location)
                break

            score = None
            if locality_l.startswith(query):
                score = 1
            elif query in locality_l:
                score = 2
            elif country_l.startswith(query):
                score = 3
            elif query in country_l:
                score = 4
            elif query in display_l:
                score = 5

            if score is not None:
                ranked_matches.append((score, continent, country, location))

        if exact is not None:
            continent, country, location = exact
            self._select_location(continent, country, location)
            return

        if not ranked_matches:
            self._details_label.setText(
                "No search result found. Try another city or country name."
            )
            return

        ranked_matches.sort(key=lambda item: (item[0], item[3].name, item[2]))
        _, continent, country, location = ranked_matches[0]
        self._select_location(continent, country, location)

    def _populate_continents(self, initial_location: GeoLocation | None) -> None:
        continents = WorldLocationCatalog.continents()
        self._continent_combo.blockSignals(True)
        self._continent_combo.clear()
        self._continent_combo.addItems(continents)
        self._continent_combo.blockSignals(False)

        if initial_location is not None:
            for continent in continents:
                countries = WorldLocationCatalog.countries(continent)
                for country in countries:
                    for location in WorldLocationCatalog.localities(continent, country):
                        if (
                            location.name == initial_location.name
                            and location.country == initial_location.country
                            and location.timezone == initial_location.timezone
                        ):
                            self._continent_combo.setCurrentText(continent)
                            self._populate_countries(continent, initial_location)
                            return

        if continents:
            self._continent_combo.setCurrentText(continents[0])
            self._populate_countries(continents[0], initial_location)

    def _populate_countries(self, continent: str, initial_location: GeoLocation | None) -> None:
        countries = WorldLocationCatalog.countries(continent)
        self._country_combo.blockSignals(True)
        self._country_combo.clear()
        self._country_combo.addItems(countries)
        self._country_combo.blockSignals(False)

        if initial_location is not None and initial_location.country in countries:
            self._country_combo.setCurrentText(initial_location.country)
            self._populate_localities(continent, initial_location.country, initial_location)
            return

        if countries:
            country = countries[0]
            self._country_combo.setCurrentText(country)
            self._populate_localities(continent, country, initial_location)

    def _populate_localities(
        self,
        continent: str,
        country: str,
        initial_location: GeoLocation | None,
    ) -> None:
        localities = WorldLocationCatalog.localities(continent, country)

        self._location_lookup = {
            f"{location.name} ({location.region})": location
            for location in localities
        }

        self._locality_combo.blockSignals(True)
        self._locality_combo.clear()
        self._locality_combo.addItems(list(self._location_lookup.keys()))
        self._locality_combo.blockSignals(False)

        if not self._location_lookup:
            self._selected_location = None
            self._details_label.setText("No localities available for this country.")
            return

        if initial_location is not None:
            for key, location in self._location_lookup.items():
                if (
                    location.name == initial_location.name
                    and location.country == initial_location.country
                    and location.timezone == initial_location.timezone
                ):
                    self._locality_combo.setCurrentText(key)
                    self._selected_location = location
                    self._update_details(location)
                    return

        first_key = next(iter(self._location_lookup.keys()))
        self._locality_combo.setCurrentText(first_key)
        self._selected_location = self._location_lookup[first_key]
        self._update_details(self._selected_location)

    def _on_continent_changed(self, continent: str) -> None:
        self._populate_countries(continent, None)

    def _on_country_changed(self, country: str) -> None:
        continent = self._continent_combo.currentText()
        self._populate_localities(continent, country, None)

    def _on_locality_changed(self, locality_key: str) -> None:
        location = self._location_lookup.get(locality_key)
        self._selected_location = location
        if location is not None:
            self._update_details(location)

    def _update_details(self, location: GeoLocation) -> None:
        self._details_label.setText(
            f"Selected: {location.name}, {location.region}, {location.country}\n"
            f"Coordinates: {location.latitude:.4f}, {location.longitude:.4f}\n"
            f"Timezone: {location.timezone}"
        )

    def _on_accept(self) -> None:
        if self._selected_location is None:
            self.reject()
            return
        self.accept()
