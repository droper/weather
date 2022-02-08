"""Tests"""
from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from weather.settings import API_SOURCE
from .weather_api import OpenWeatherApi
from .client import weather_retrieve
from .factory import ConcreteWeatherApiFactory


class Weather(APITestCase):

    def test_get(self):
        response = self.client.get('http://127.0.0.1:8000/api',
                                   {'country': 'pe', 'city': 'Lima'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['location_name'], 'Lima, PE')

        response = self.client.get('http://127.0.0.1:8000/api',
                                   {'country': 'mx', 'city': 'Tamaulipas'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['location_name'], 'Tamaulipas, MX')

    def test_weather_retrieve(self):
        bogota = weather_retrieve(ConcreteWeatherApiFactory(), 'co', 'Bogota')
        lima = weather_retrieve(ConcreteWeatherApiFactory(), 'pe', 'Lima')
        assert (bogota['location_name'] == 'Bogota, CO')
        assert (bogota['geo_coordinates'] == [4.6097, -74.0817])
        assert (lima['location_name'] == 'Lima, PE')
        assert (lima['geo_coordinates'] == [-12.0432, -77.0282])

    def test_create_weather_api(self):
        obj = ConcreteWeatherApiFactory()
        self.assertEqual(type(obj.create_weather_api(API_SOURCE)), OpenWeatherApi)

    def test_timestamp_to_strtime(self):
        date_time_orig_obj = datetime.strptime('05:00', '%H:%M')
        timestamp = datetime.timestamp(date_time_orig_obj)

        date_time_end_obj = datetime.strptime('04:00', '%H:%M')

        timezone_offset = timedelta(hours=-1)
        self.assertEqual(OpenWeatherApi.timestamp_to_strtime(timestamp, timezone_offset),
                         date_time_end_obj.strftime('%H:%M'))
