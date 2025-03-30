from .base_fetcher import AircraftDataFetcher
import requests

class Dump1090Fetcher(AircraftDataFetcher):
    def __init__(self, host="localhost", port=8080):
        self.base_url = f"http://{host}:{port}"

    def fetch_aircraft_data(self):
        """Fetch JSON data from dump1090's aircraft endpoint."""
        response = requests.get(f"{self.base_url}/data/aircraft.json")
        response.raise_for_status()  # Raise error if request fails
        return response.json()

    @staticmethod
    def normalize_data(raw_data):
        """Convert dump1090 format to standard format."""
        return [
            {
                "icao": aircraft.get("hex"),
                "callsign": aircraft.get("flight"),
                "latitude": aircraft.get("lat"),
                "longitude": aircraft.get("lon"),
                "altitude": aircraft.get("altitude"),
                "speed": aircraft.get("speed"),
                "heading": aircraft.get("track"),
                "source": "dump1090",  # Identify data source
            }
            for aircraft in raw_data.get("aircraft", [])
            if aircraft.get("lat") and aircraft.get("lon")  # Only return aircraft with positions
        ]
