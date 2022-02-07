"""views"""
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from weather.settings import CACHE_TTL
from .factory import ConcreteWeatherApiFactory
from .client import weather_retrieve


class Weather(APIView):
    """Return the Weather"""

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        """
        GET endpoint, obtain country and city and returns
        the formatted weather response.
        """

        try:
            country = self.request.query_params['country']
            city = self.request.query_params['city']
        except KeyError as country_city_not_exist:
            raise NotFound("There is no city or country parameter") from country_city_not_exist

        return Response(weather_retrieve(ConcreteWeatherApiFactory(), country, city))
