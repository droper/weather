"""'Client"""
from weather.settings import API_SOURCE

from rest_framework.exceptions import NotFound


def weather_retrieve(api_factory, country, city):
    """Retrieve the data from the weather api"""

    weather_data = api_factory.create_weather_api(API_SOURCE)

    if weather_data:
        return weather_data.weather_data(country, city)
    raise NotFound("Incorrect API source")
