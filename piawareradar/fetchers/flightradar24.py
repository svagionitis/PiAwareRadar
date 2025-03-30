from .base_fetcher import AircraftDataFetcher
import requests

class FlightRadar24Fetcher(AircraftDataFetcher):
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.flightradar24.com/common/v1/flight/list"

    def fetch_aircraft_data(self):
        """Fetch data from FlightRadar24's API."""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        params = {
            "bounds": "51.0,-0.1,51.5,0.2",  # Example: London area
            "faa": "1",
            "satellite": "0",
        }
        response = requests.get(self.base_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def normalize_data(raw_data):
        """Convert FlightRadar24 format to standard format."""
        return [
            {
                "icao": aircraft.get("identification", {}).get("icao"),
                "callsign": aircraft.get("identification", {}).get("callsign"),
                "latitude": aircraft.get("trail", [{}])[0].get("lat"),  # Latest position
                "longitude": aircraft.get("trail", [{}])[0].get("lon"),
                "altitude": aircraft.get("altitude", {}).get("meters"),
                "speed": aircraft.get("speed", {}).get("kmh"),
                "heading": aircraft.get("heading"),
                "source": "flightradar24",
            }
            for aircraft in raw_data.get("data", [])
            if aircraft.get("trail")  # Only return aircraft with positions
        ]
