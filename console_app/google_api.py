import googlemaps
from api_key import API_KEY
from datetime import datetime, timedelta
from weather_getter import GetNwsWeatherTime

gm = googlemaps.Client(key=API_KEY)

def GetRouteTimes(route, departure_time):
    steps = route[0]["legs"][0]["steps"]
    times = [None] * len(steps)
    locations = [None] * len(steps)

    for k in range(len(steps)):
        locations[k] = steps[k]["end_location"]
        duration = steps[k]["duration"]["text"]
        hours = 0
        minutes = 0
        if duration.find('hour') != -1:
            ind = duration.find('hour')
            hours = int(duration[0:ind-1])
            duration = duration[ind + 5 : -1]
        if duration.find('min') != -1:
            ind = duration.find('min')
            minutes = int(duration[0 : ind-1])

        if k == 0:
            times[k] = departure_time + timedelta(hours=hours, minutes=minutes)
        else:
            times[k] = times[k-1] + timedelta(hours=hours, minutes=minutes)
        
    return locations, times

route = gm.directions(
    "Logan, UT", "Concord, MA"
)

departure_time = datetime(2022, 11, 13, 15, 0, 0)
locations, times = GetRouteTimes(route, departure_time)
  
k = 0
weather = [None] * len(locations)
for location, time in locations, times:
    weather[k] = GetNwsWeatherTime(location, time)
    k = k + 1