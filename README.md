# Weather CLI

A simple command-line tool to check current weather conditions by city name or coordinates, using the [Open-Meteo](https://open-meteo.com/) API.

## Features

- Get current weather by latitude/longitude
- Get current weather by city name (auto-converted to coordinates via geocoding)
- Displays temperature, apparent temperature, humidity, wind speed, and weather condition

## Installation

1. Clone this repository
    git clone https://github.com/raudhatuls/Weather-App.git
    cd weather-app

2. Create and activate a virtual environment
    python -m venv venv
    venv\Scripts\Activate.ps1 # Windows PowerShell
    
3. Install dependencies
    pip install -r requirements.txt
    
## Usage

**By coordinates:**
    python weather.py coordinates --latitude 3.5952 --longitude 98.6722
    
**By city name:**
    python weather.py city --name Medan
    
## Example Output
    Weather forecast for Medan
    Coordinates: 3.5952 98.6722
    Elevation: 25.0 m asl
    Timezone difference to GMT+0: 25200s

    Current time: 23-09-26 14:30:00
    Current temperature_2m: 29.5 C
    Current relative_humidity_2m: 78 %
    Current apparent_temperature: 32.1 C
    Current is_day: Daylight
    Current wind_speed_10m: 3.3 km/h
    Current weather: Clear Sky


## What I learned

- Making HTTP requests and handling API responses in Python
- Working with two different API response formats (JSON vs FlatBuffers) from the same provider
- Using `argparse` with subcommands
- Error handling for network requests
- Reusing logic between functions to avoid duplication (geocoding → coordinates lookup)

## Built with

- Python
- [openmeteo_requests](https://github.com/open-meteo/python-requests)
- [requests](https://requests.readthedocs.io/)
- requests-cache, retry-requests