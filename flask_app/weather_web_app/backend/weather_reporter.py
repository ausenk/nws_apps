''' Calls into weather getter and reports back weather to user'''
from weather_web_app.backend.nws_weather import WeatherGetter
from weather_web_app.backend.geo_coder import GeoCoder

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


def WeatherReporter():
    welcome_string = f"""
        Weather Service
        ---------------
        Enter address to continue"""

    print(welcome_string)

    address = input("        ")

    response = GeoCoder(address)
    lat = response["data"][0]["latitude"]
    long = response["data"][0]["longitude"]

    location = {
        "lat": lat,
        "long": long,
    }

    weather_station = WeatherGetter(location)
    forecast = weather_station.GetNwsWeather()
    ParseNwsForcast(forecast)
    return
