"""Adapters"""
from abc import ABC, abstractmethod

from datetime import datetime, timedelta
import requests

from rest_framework.exceptions import NotFound

from weather.settings import APPID


class AbstractWeatherApi(ABC):
    """Abstract class for the Weather APIs"""

    @abstractmethod
    def retrieve_data(self, country: str, city: str):
        pass

    @abstractmethod
    def weather_data(self, country: str, city: str):
        pass


class OpenWeatherApi(AbstractWeatherApi):
    """Adapter for the OpenWeatherMap api"""

    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    forecast_url = "http://api.openweathermap.org/data/2.5/onecall"

    def retrieve_data(self, country, city):
        """Retrieve weather data from OpenWeatherMap"""

        # Retrieve today weather data
        try:
            weather_resp = requests.get(self.weather_url, {'q': ','.join([city, country]),
                                                           'appid': APPID})
        except requests.exceptions.RequestException as e:
            raise e.response.text

        # Retrieve forecast data
        today_weather_data = weather_resp.json()
        try:
            lon = today_weather_data['coord']['lon']
            lat = today_weather_data['coord']['lat']
        except KeyError as key_not_exist:
            raise NotFound("There are no coordinates in weather data") from key_not_exist

        try:
            forecast_resp = requests.get(self.forecast_url, {'lat': lat, 'lon': lon,
                                                             'appid': APPID})
        except requests.exceptions.RequestException as e:
            raise e.response.text

        return today_weather_data, forecast_resp.json()

    @staticmethod
    def timestamp_to_strtime(timestamp, timezone_delta):
        """Returns a strtime from a timestamp minus the timezone offset

        :param timestamp: the actual timestamp
        :param timezone_delta: timezone offset
        """

        date = datetime.fromtimestamp(timestamp) + timezone_delta
        return date.strftime('%H:%M')

    def today_weather(self, today_data):
        """Format data from today weather api"""

        weather_data = {}

        if today_data['cod'] == 200:
            timezone_delta = timedelta(hours=today_data['timezone'] / 3600)

            city_time = datetime.now() + timezone_delta
            weather_data = {
                "location_name": today_data['name'] + ', ' + today_data['sys']['country'],
                "temperature": str(round(float(today_data['main']['temp']) - 273.15)) + ' ºC',
                "wind": str(today_data['wind']['speed']) + ' m/s',
                "cloudiness": today_data['weather'][0]['description'],
                "pressure": str(today_data['main']['pressure']) + ' hpa',
                "humidity": str(today_data['main']['humidity']) + '%',
                "sunrise": self.timestamp_to_strtime(int(today_data['sys']['sunrise']),
                                                     timezone_delta),
                "sunset": self.timestamp_to_strtime(int(today_data['sys']['sunset']),
                                                    timezone_delta),
                "geo_coordinates": [today_data["coord"]["lat"], today_data["coord"]["lon"]],
                "requested_time": city_time.strftime('%Y-%m-%d %H:%M:%S')
            }

        return weather_data

    def forecast_weather(self, forecasts_data):
        """Formats data from the forecast weather"""

        data = {}
        if 'cod' not in forecasts_data:
            timezone_delta = timedelta(hours=forecasts_data['timezone_offset'] / 3600)

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

    def weather_data(self, country, city):
        """Returns the weather and forecasted data"""

        today_data, forecast_data = self.retrieve_data(country, city)
        data = self.today_weather(today_data)
        data['forecast'] = self.forecast_weather(forecast_data)
        return data
