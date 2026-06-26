# SkyProject: Annual Solar and Twilight Planner

A Python desktop astronomy application with a reusable OOP architecture.

## Features

- PyQt6 GUI with Matplotlib integration
- Location sub-GUI with hierarchical selection:
  - Continent -> Country -> Locality
  - Quick search field to jump directly to a city/country
  - Curated major localities across the world
  - Includes extreme-latitude sites (for polar-day/polar-night scenarios)
- Annual chart (one point per day) for:
  - Solar noon
  - Sunrise and sunset
  - Civil dawn and dusk
  - Nautical dawn and dusk
  - Astronomical dawn and dusk
- Background phase coloring for:
  - Daylight
  - Civil twilight
  - Nautical twilight
  - Astronomical twilight
  - Astronomical night
- Initial location configuration for Ulm, Germany
- Optional equinox/solstice marker lines
- Automatic red "Today" line when the displayed year equals the current year
- Separated layers for GUI, astronomy calculations, and visualization

## Project Structure

- `main.py`: application entrypoint
- `gui/`: windows and widgets
- `astronomy/`: reusable calculators and data services
- `visualization/`: plotting logic
- `config/`: location registry
- `scripts/run_gui.py`: launcher script

## Quick Start

### Setup (First Time)

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

- **Main GUI:**
  ```bash
  python main.py
  ```

- **Alternative launcher:**
  ```bash
  python scripts/run_gui.py
  ```

### Requirements

- Python 3.10 or higher
- See `requirements.txt` for Python package dependencies

## Extendability

The architecture is built for future additions:

- Multiple locations
- Moon rise/set and planet visibility modules
- Weather integrations
- Export to PNG/PDF
- Additional astronomical planning diagrams
