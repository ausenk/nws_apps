import googlemaps
from api_key import API_KEY
from datetime import datetime
from weather_getter import GetNwsWeatherTime

gm = googlemaps.Client(key=API_KEY)

routes = gm.directions(
    "Boston, MA", "Concord, MA", waypoints=["Charlestown, MA", "Lexington, MA"]
)

location = routes[0]["legs"][0]["steps"][0]["end_location"]
time = datetime(2022, 11, 13, 15, 0, 0)

weather = GetNwsWeatherTime(location, time)
print(weather)