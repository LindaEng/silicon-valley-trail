import json

import requests
import time
import random

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

def build_query(category_pairs, lat, lon):
    nodes = "\n".join(
        f'node["{key}"="{value}"](around:2000,{lat},{lon});'
        for key, value in category_pairs
    )

    return f"""
    [out:json];
    (
        {nodes}
    );
    out 5;
    """


def generate_fallback_places():
    fake_places = [
        {"tags": {"name": "Local Spot"}},
        {"tags": {"name": "Hidden Gem"}},
        {"tags": {"name": "Secret Garden"}},
        {"tags": {"name": "Underground Networking club"}},
    ]
    return {"elements": random.sample(fake_places, k=2)}


def get_nearby(category_pairs, lat, lon):
    query = build_query(category_pairs, lat, lon)
    
    for attempt in range(3):
        try:
            response = requests.get(
                OVERPASS_URL,
                params={"data": query},
                timeout=30
            )
            response.raise_for_status()
            
            try:
                data = response.json()
                if isinstance(data, dict) and "elements" in data:
                    if data["elements"]:
                        print(f"Found {len(data['elements'])} spots!")
                    else:
                        print("No spots found nearby.")
                    return data
                elif isinstance(data, list):
                    if data:
                        print(f"Found {len(data)} spots!")
                    else:
                        print("No spots found nearby.")
                    return {"elements": data}
                else:
                    print("Checking local recommendations...")
                    return generate_fallback_places()
                    
            except json.JSONDecodeError:
                print("Checking local recommendations...")
                return generate_fallback_places()
                
        except requests.exceptions.ReadTimeout:
            print("Network slow, checking local recommendations...")
            return generate_fallback_places()
            
        except requests.exceptions.RequestException as e:
            print(f"Using local knowledge...")
            if attempt == 2:
                return generate_fallback_places()
            
        time.sleep(2)
    
    print("Asking locals for recommendations...")
    return generate_fallback_places()