from .base_fetcher import AircraftDataFetcher
import requests

class ADSBExchangeFetcher(AircraftDataFetcher):
    def __init__(self, latitude=51.5, longitude=-0.1, radius=100):
        self.base_url = "https://adsbexchange.com/api/aircraft/json/"
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius  # Search radius in km

    def fetch_aircraft_data(self):
        """Fetch data from ADSBexchange's API."""
        params = {
            "lat": self.latitude,
            "lng": self.longitude,
            "dist": self.radius,
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def normalize_data(raw_data):
        """Convert ADSBexchange format to standard format."""
        return [
            {
                "icao": aircraft.get("hex"),
                "callsign": aircraft.get("flight"),
                "latitude": aircraft.get("lat"),
                "longitude": aircraft.get("lon"),
                "altitude": aircraft.get("alt"),
                "speed": aircraft.get("spd"),
                "heading": aircraft.get("trak"),
                "source": "adsbexchange",
            }
            for aircraft in raw_data.get("ac", [])
            if aircraft.get("lat") and aircraft.get("lon")
        ]
