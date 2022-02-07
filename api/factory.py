"""factories"""
from abc import ABC, abstractmethod

from .weather_api import AbstractWeatherApi, OpenWeatherApi


class AbstractWeatherApiFactory(ABC):
    """Abstract factory for Weather apis"""

    @abstractmethod
    def create_weather_api(self, api_source) -> AbstractWeatherApi:
        pass


class ConcreteWeatherApiFactory(AbstractWeatherApiFactory):
    """Constructor of Weather Api classes"""

    def create_weather_api(self, api_source) -> AbstractWeatherApi:
        if api_source == "OPEN_WEATHER":
            return OpenWeatherApi()
