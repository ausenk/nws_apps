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

    def GetNwsWeather(self):
        points = self.__GetNwsPoints()

        office = points["properties"]["gridId"]
        gridX = points["properties"]["gridX"]
        gridY = points["properties"]["gridY"]

        url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        return self.__ApiCall(url, headers) 


