import requests

BASE_URL = "https://nominatim.openstreetmap.org/search"


def get_location(query):
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "silicon-trail-app"
    }

    response = requests.get(BASE_URL, params=params, headers=headers)

    data = response.json()

    if not data:
        return None

    result = data[0]

    return {
        "name": result["display_name"],
        "lat": result["lat"],
        "lon": result["lon"]
    }
