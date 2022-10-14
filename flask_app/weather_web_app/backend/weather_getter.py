import json
import requests


class WeatherGetter:
    def __init__(self, location):
        self.location = location

    def __ApiCall(self, url, headers):
        response = requests.get(url, headers = headers)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    def __GetNwsPoints(self):
        lat = self.location["lat"]
        lon = self.location["long"]

        url = f"https://api.weather.gov/points/{lat},{lon}"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        return self.__ApiCall(url, headers)

    def GetNwsOfficeUsingCoords(self):
        points = self.__GetNwsPoints()
        return points

    def GetNwsWeatherUsingCoords(self):
        points = self.__GetNwsPoints()

        office = points["properties"]["gridId"]
        gridX = points["properties"]["gridX"]
        gridY = points["properties"]["gridY"]

        url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        return self.__ApiCall(url, headers) 

    def GetNwsWeatherUsingOffice(self):
        office = self.location["office"]
        gridX = self.location["gridx"]
        gridY = self.location["gridy"]

        url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        return self.__ApiCall(url, headers)


def ParseNwsForcast(forecast: dict):
    periods = forecast["properties"]["periods"]
    for period in periods:
        forecast_str = f"""
        {period["name"]} from {period["startTime"]} to {period["endTime"]}
        Forecast: {period["detailedForecast"]}
        Temperature: {period["temperature"]} {period["temperatureUnit"]}
        Wind Speed: {period["windSpeed"]}
        Wind Direction: {period["windDirection"]}"""

        return forecast_str