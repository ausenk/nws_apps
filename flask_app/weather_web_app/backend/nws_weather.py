import json
import requests


class NwsWeather:
    def __init__(self, office, coordinates):
        self.coordinates = coordinates
        self.office = office

    def __ApiCall(self, url, headers):
        response = requests.get(url, headers = headers)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    def __GetNwsPoints(self):
        lat = self.coordinates["lat"]
        lon = self.coordinates["long"]

        url = f"https://api.weather.gov/points/{lat},{lon}"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        return self.__ApiCall(url, headers)

    def GetNwsOfficeUsingCoords(self):
        points = self.__GetNwsPoints()
        return points

    def GetNwsWeather(self):
        if self.office == None:
            points = self.__GetNwsPoints()
            points = points["properties"]
        else:
            points = self.office
        
        office = points["gridId"]
        gridX = points["gridX"]
        gridY = points["gridY"]

        url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

        headers = {
            "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
        }

        nws_weather = self.__ApiCall(url, headers) 
        return self._ParseNwsWeather(nws_weather)

    def _ParseNwsWeather(self, nws_weather):
        periods = nws_weather["properties"]["periods"]
        if not periods[0]["isDaytime"]:
            periods = [periods[0]] + periods
            
        return periods
