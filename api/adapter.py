"""Adapters"""
from datetime import datetime


class OpenWeatherAdapter:
    """Adapter for the OpenWeatherMap api"""

    def __init__(self, today_data, forecast_data):
        self.today_data = today_data
        self.forecast_data = forecast_data

    def timestamp_to_strtime(self, timestamp):
        """Returns a strtime from a timestamp"""

        date = datetime.fromtimestamp(timestamp)
        return date.strftime('%H:%M')

    def utc_to_strtime(self, utc_timestamp):
        """Unix Utc timestamp to """

    def today_weather(self):
        """Generates data from the weather api data"""

        sunset = datetime.fromtimestamp(int(self.today_data['sys']['sunset']))
        sunset_time = sunset.strftime('%H:%M')

        sunrise = datetime.fromtimestamp(int(self.today_data['sys']['sunrise']))
        sunrise_time = sunrise.strftime('%H:%M')

        timestamp = datetime.utcfromtimestamp(self.today_data['timestamp'])
        city_time = datetime.fromtimestamp(timestamp) - datetime.utcfromtimestamp(timestamp)

        weather_data = {
            "location_name": self.today_data['name'] + ', ' + self.today_data['country'],
            "temperature": str(float(self.today_data['main']['temp']) - 273.15) + ' ºC',
            "wind": str(self.today_data['speed']) + ' m/s',
            "cloudiness": self.today_data['weather'][0]['description'],
            "pressure": str(self.today_data['main']['pressure']) + ' hpa',
            "humidity": str(self.today_data['main']['humidity']) + '%',
            "sunrise": sunrise_time,
            "sunset": sunset_time,
            "geo_coordinates": [self.today_data["coord"]["lat"], self.today_data["coord"]["lon"]],
            "requested_time": city_time.strftime('%Y-%m-%d %H:%M:%S')
        }

        return weather_data

    def forecast_weather(self):
        """Generates data from the forecast data"""

        sunrise = datetime.fromtimestamp(int(self.forecast_data['sunrise']))
        sunrise_time = sunrise.strftime('%H:%M')

        sunset = datetime.fromtimestamp(int(self.forecast_data['sunset']))
        sunset_time = sunset.strftime('%H:%M')

        forecast_data = {
            "temperature": str(float(self.forecast_data['temp']['day']) - 273.15) + ' ºC',
            "wind": str(self.forecast_data['wind_speed']) + ' m/s',
            "cloudiness": self.forecast_data['weather'][0]['description'],
            "pressure": str(self.forecast_data['main']['pressure']) + ' hpa',
            "humidity": str(self.forecast_data['main']['humidity']) + '%',
            "sunrise": sunrise_time,
            "sunset": sunset_time
        }

        return forecast_data

    def weather_data(self):
        """Returns the weather and forecasted data"""

        data = self.today_data
        data.append(self.forecast_data)
        return data



