import argparse
import openmeteo_requests
import requests_cache
from retry_requests import retry
import json
from operator import itemgetter
from datetime import date

def main():
    parser = argparse.ArgumentParser(description='Weather Forecast.')
    subparsers = parser.add_subparsers(dest='command', required=True)
    parser_coordinates = subparsers.add_parser('coordinates', help='Weather forecast based on coordinate.')
    #parser coordinates
    parser_coordinates.add_argument('-latitude', '--latitude', required=True, type=float, help='Latitude.')
    parser_coordinates.add_argument('-longitude', '--longitude', required=True, type=float,  help='Longitude.')
    #parser city
    parser_city = subparsers.add_parser('city', help='Weather forecast based on city name.')
    parser_city.add_argument('-name', '--name', required=True, help='Name of the city.')
    args = parser.parse_args()
    if args.command == "coordinates" :
        forecast_by_coordinates(args)
    elif args.command == "list" :
        forecast_by_city(args)

def forecast_by_coordinates(args):
    latitude = args.latitude
    longitude = args.longitude
    openmeteo = setup_open_meteo_api()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
    }
    responses = openmeteo.weather_api(url, params = params)
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

def forecast_by_city():
    print("a")

def setup_open_meteo_api():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    return openmeteo
    
if __name__ == "__main__":
    main()