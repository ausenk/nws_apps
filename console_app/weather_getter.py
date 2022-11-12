import json
import requests
from datetime import datetime

def __ApiCall(url, headers):
    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def __GetNwsPoints(location):
    lat = location["lat"]
    lon = location["lng"]

    url = f"https://api.weather.gov/points/{lat},{lon}"

    headers = {
        "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
    }

    return __ApiCall(url, headers)

def GetDailyNwsWeather(location):
    points = __GetNwsPoints(location)

    office = points["properties"]["gridId"]
    gridX = points["properties"]["gridX"]
    gridY = points["properties"]["gridY"]

    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"

    headers = {
        "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
    }

    return __ApiCall(url, headers) 

def GetHourlyNwsWeather(location):
    points = __GetNwsPoints(location)

    office = points["properties"]["gridId"]
    gridX = points["properties"]["gridX"]
    gridY = points["properties"]["gridY"]

    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast/hourly"

    headers = {
        "User-Agent": "(weather_getter, ausenkyle@gmail.com)"
    }

    return __ApiCall(url, headers) 

def GetNwsWeatherTime(location, time):
    weather = GetHourlyNwsWeather(location)
    periods = weather["properties"]["periods"]

    for period in periods:
        start_time = period["startTime"]
        start_time_strs = start_time.split('T')
        d = start_time_strs[0].split('-')
        t = start_time_strs[1].split('-')
        t = t[0].split(':')
        if time == datetime(int(d[0]), int(d[1]), int(d[2]), int(t[0]), int(t[1])):
            return period

    return "Invalid Time."

