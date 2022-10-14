import requests
import json

API_KEY = "1dff4948d848be45c241c8c47820f70d"

def GeoCoder(address):
    url = f"http://api.positionstack.com/v1/forward?access_key={API_KEY}&query={address}"
    url = url.replace(" ", "%20")

    response = requests.get(url)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))
        coordinates = {
            "lat" : response["data"][0]["latitude"],
            "long" : response["data"][0]["longitude"]
        }
        return coordinates
    else:
        return None

def ReverseGeoCoder(coordinates):
    url = f"http://api.positionstack.com/v1/reverse?access_key={API_KEY}&query={coordinates['lat']},{coordinates['long']}"
    url = url.replace(" ", "%20")

    response = requests.get(url)
    if response.status_code == 200:
        response = json.loads(response.content.decode('utf-8'))
        return response["data"][0]["label"]
    else:
        return None