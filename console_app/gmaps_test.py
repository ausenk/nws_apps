import googlemaps
from api_key import API_KEY

gmaps = googlemaps.Client(API_KEY)

routes = gmaps.directions(
"Adelaide, SA",
"Adelaide, SA",
waypoints=[
    "Barossa Valley, SA",
    "Clare, SA",
    "Connawarra, SA",
    "McLaren Vale, SA",
],
optimize_waypoints=True,
)

print(routes)
