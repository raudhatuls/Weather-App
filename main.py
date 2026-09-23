import argparse
import openmeteo_requests
import requests_cache
from retry_requests import retry
import datetime

weather_code = {
    0 : "Clear Sky",
    1 : "Mainly clear, partly cloudy, and overcast",
    2 : "Mainly clear, partly cloudy, and overcast",
    3 : "Mainly clear, partly cloudy, and overcast",
    45 : "Fog and depositing rime fog",
    48 : "Fog and depositing rime fog",
    51 : "Drizzle: Light, moderate, and dense intensity",
    53 : "Drizzle: Light, moderate, and dense intensity",
    55 : "Drizzle: Light, moderate, and dense intensity",
    56 : "Freezing Drizzle: Light and dense intensity",
    57 : "Freezing Drizzle: Light and dense intensity",
    61 : "Rain: Slight, moderate and heavy intensity",
    63 : "Rain: Slight, moderate and heavy intensity",
    65 : "Rain: Slight, moderate and heavy intensity",
    66 : "Freezing Rain: Light and heavy intensity",
    67 : "Freezing Rain: Light and heavy intensity",
    71 : "Snow fall: Slight, moderate, and heavy intensity",
    73 : "Snow fall: Slight, moderate, and heavy intensity",
    75 : "Snow fall: Slight, moderate, and heavy intensity",
    77 : "Snow grains",
    80 : "Rain showers: Slight, moderate, and violent",
    81 : "Rain showers: Slight, moderate, and violent",
    82 : "Rain showers: Slight, moderate, and violent",
    85 : "Snow showers slight and heavy",
    86 : "Snow showers slight and heavy",
    95 : "Thunderstorm: Slight or moderate",
    96 : "Thunderstorm with slight and heavy hail",
    99 : "Thunderstorm with slight and heavy hail"
}
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
    elif args.command == "city" :
        forecast_by_city(args)

def forecast_by_coordinates(args):
    latitude = args.latitude
    longitude = args.longitude
    openmeteo = setup_open_meteo_api()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "wind_speed_10m", "weather_code"],
	    "forecast_days": 1,
    }
    try:
        responses = openmeteo.weather_api(url, params = params)
        response = responses[0]
        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")


        # Process current data. The order of variables needs to be the same as requested.
        current = response.Current()
        current_time = datetime.datetime.fromtimestamp(int(current.Time())).strftime('%d-%m-%y %H:%M:%S')
        current_temperature_2m = round(current.Variables(0).Value(),1)
        current_relative_humidity_2m = round(current.Variables(1).Value())
        current_apparent_temperature = round(current.Variables(2).Value(),1)
        current_is_day = "Daylight" if current.Variables(3).Value()== 1 else "Current is Nighttime"
        current_wind_speed_10m = round(current.Variables(4).Value(),1)
        current_weather_code = weather_code[int(current.Variables(5).Value())]

        print(f"\nCurrent time: {current_time}")
        print(f"Current temperature_2m: {current_temperature_2m} C")
        print(f"Current relative_humidity_2m: {current_relative_humidity_2m} %")
        print(f"Current apparent_temperature: {current_apparent_temperature} C")
        print(f"Current is_day: {current_is_day}")
        print(f"Current wind_speed_10m: {current_wind_speed_10m} km/h")
        print(f"Current weather: {current_weather_code}")
    except Exception as e:
        print(f"Error fetching data: {e}")
    

def forecast_by_city(args):
    print("")

def setup_open_meteo_api():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    return openmeteo
    
if __name__ == "__main__":
    main()