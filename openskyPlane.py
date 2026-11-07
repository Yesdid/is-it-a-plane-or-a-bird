import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("OPENSKY_CLIENT_ID")
CLIENT_SECRET = os.getenv("OPENSKY_CLIENT_SECRET")

auth_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

auth_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PlaneTracker/1.0"
}

auth_response = requests.post(auth_url, data=auth_data, headers=auth_headers)

if auth_response.status_code != 200:
    print(f"Login failed! Check your credentials. Error: {auth_response.text}")
    exit()

token = auth_response.json().get("access_token")

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PlaneTracker/1.0"
}

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io", timeout=10)
        response.raise_for_status()

        data = response.json()

        location = data.get("loc")

        if not location:
            print("Could not determine location.")
            return None

        latitude, longitude = map(float, location.split(","))

        print(f"City: {data.get('city')}, {data.get('region')}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")

        return latitude, longitude

    except Exception as e:
        print(f"Error fetching location: {e}")
        return None


location = get_current_location()

if location is None:
    exit()

latitude, longitude = location
#Roughly 5 miles
lat_range = 0.0725
long_range = 0.0916

places_url = "https://opensky-network.org/api/states/all"
params = {
    "lamin": latitude - lat_range,
    "lamax": latitude + lat_range,
    "lomin": longitude - long_range,
    "lomax": longitude + long_range
}

response = requests.get(places_url, headers=headers, params=params)

result = ""
if response.status_code == 200:
    data = response.json()
    states = data.get("states", [])
    
    print(f"\nFound {len(states)} active flights in this zone:\n")

    airborne = [flight for flight in states if flight[8] is False]

    print(f"Found {len(airborne)} airborne aircraft:\n")

    for flight in airborne[:5]:
        if flight[8] is True:
            continue
        # OpenSky array indices: 1 = Callsign, 2 = Country, 5 = Longitude, 6 = Latitude, 7 = Baro Altitude, 8 = on_ground, 9 = Velocity
        callsign = flight[1].strip() if flight[1] else "UNKNOWN"
        country = flight[2]
        lon, lat = flight[5], flight[6]
        alt = flight[7]
        speed = flight[9]*2.237
        
        print(f"Flight: {callsign} ({country})")
        print(f"   Coords: ({lat}, {lon}) | Altitude: {alt}m | Speed: {speed} mph\n")
        result += (f"Flight: {callsign} ({country})")
        result += (f"Coords: ({lat}, {lon}) | Altitude: {alt}m | Speed: {speed} mph\n")
else:
    print(f"Failed to fetch flight data. Status code: {response.status_code}")

print("result:", result)