from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .adapter import open_weather_retrieve
from weather.settings import CACHE_TTL


class Weather(APIView):
    """Return the Weather"""

    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        """GET endpoint"""

        try:
            country = self.request.query_params['country']
            city = self.request.query_params['city']
        except KeyError:
            raise NotFound("There is no city or country parameter")

        return Response(open_weather_retrieve(country, city))
