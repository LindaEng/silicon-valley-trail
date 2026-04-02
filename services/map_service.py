import requests
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_location(query):
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "silicon-trail-app"
    }
    response = requests.get(NOMINATIM_URL, params=params, headers=headers)
    data = response.json()
    if not data:
        return None
    result = data[0]
    return {
        "name": result["display_name"],
        "lat": result["lat"],
        "lon": result["lon"]
    }

def get_nearby(desc, lat, lon):
    pattern = "|".join(desc)
    query = f"""
    [out:json];
    node
      ["amenity"~"{pattern}"]
      (around:2000,{lat},{lon});
    out;
    """
    print("You wander and wander and look for interesting spots...")
    time.sleep(0.5)
    response = requests.get(
        OVERPASS_URL,
        params={"data": query},
        timeout = 10
    )

    if response.status_code != 200:
        print("You find nothing interesting... Try again or try somewhere else?")
        return []

    try:
        data = response.json()
    except Exception:
        print("FAILED TO PARSE JSON")
        print(response.text[:200])
        return []
    
    locations = []
    
    for el in data.get("elements", []):
        locations.append(el)
        if len(locations) >= 5:
            break
    
    return locations


