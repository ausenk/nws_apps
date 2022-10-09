import requests
import json

def GeoCoder(address):
    API_KEY = "1dff4948d848be45c241c8c47820f70d"
    url = f"http://api.positionstack.com/v1/forward?access_key={API_KEY}&query={address}"
    url = url.replace(" ", "%20")

    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

    
