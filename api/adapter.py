"""Adapters"""
from datetime import datetime, timedelta
import requests


def open_weather_retrieve(country, city):
    """Retrieve the data from Open Weather"""

    appid = "1508a9a4840a5574c822d70ca2132032"

    weather_data = OpenWeatherAdapter()

    # Weather data
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    try:
        weather_resp = requests.get(weather_url, {'q': ','.join([city, country]),
                                                  'appid': appid})
    except requests.exceptions.RequestException as e:
        raise e.response.text

    # Forecast data
    today_weather_data = weather_data.today_weather(weather_resp.json())
    if 'geo_coordinates' in today_weather_data:
        lat, lon = today_weather_data['geo_coordinates']
    else:
        return {"message": "No coordinates"}

    forecast_url = "http://api.openweathermap.org/data/2.5/onecall"
    try:
        forecast_resp = requests.get(forecast_url, {'lat': lat, 'lon': lon,
                                                    'appid': appid})
    except requests.exceptions.RequestException as e:
        raise e.response.text

    return weather_data.weather_data(weather_resp.json(), forecast_resp.json())


class OpenWeatherAdapter:
    """Adapter for the OpenWeatherMap api"""

    @staticmethod
    def timestamp_to_strtime(timestamp, timezone_delta):
        """Returns a strtime from a timestamp minus the timezone offset"""

        date = datetime.fromtimestamp(timestamp) + timezone_delta
        return date.strftime('%H:%M')

    def today_weather(self, today_data):
        """Generates data from the weather api data"""

        weather_data = {}

        if today_data['cod'] == 200:

            timezone_delta = timedelta(hours=today_data['timezone']/3600)

            city_time = datetime.now() + timezone_delta
            weather_data = {
                "location_name": today_data['name'] + ', ' + today_data['sys']['country'],
                "temperature": str(round(float(today_data['main']['temp']) - 273.15)) + ' ºC',
                "wind": str(today_data['wind']['speed']) + ' m/s',
                "cloudiness": today_data['weather'][0]['description'],
                "pressure": str(today_data['main']['pressure']) + ' hpa',
                "humidity": str(today_data['main']['humidity']) + '%',
                "sunrise": self.timestamp_to_strtime(int(today_data['sys']['sunrise']), timezone_delta),
                "sunset": self.timestamp_to_strtime(int(today_data['sys']['sunset']), timezone_delta),
                "geo_coordinates": [today_data["coord"]["lat"], today_data["coord"]["lon"]],
                "requested_time": city_time.strftime('%Y-%m-%d %H:%M:%S')
            }

        return weather_data

    def forecast_weather(self, forecasts_data):
        """Generates data from the forecast data"""

        data = {}
        if forecasts_data:
            timezone_delta = timedelta(hours=forecasts_data['timezone_offset']/3600)

            forecast_data = forecasts_data['daily'][0]
            data = {
                "temperature": str(round(float(forecast_data['temp']['day']) - 273.15)) + ' ºC',
                "wind": str(forecast_data['wind_speed']) + ' m/s',
                "cloudiness": forecast_data['weather'][0]['description'],
                "pressure": str(forecast_data['pressure']) + ' hpa',
                "humidity": str(forecast_data['humidity']) + '%',
                "sunrise": self.timestamp_to_strtime(int(forecast_data['sunrise']), timezone_delta),
                "sunset": self.timestamp_to_strtime(int(forecast_data['sunset']), timezone_delta)
            }

        return data

    def weather_data(self, today_data, forecast_data):
        """Returns the weather and forecasted data"""

        data = self.today_weather(today_data)
        data['forecast'] = self.forecast_weather(forecast_data)
        return data



