from .base_fetcher import AircraftDataFetcher
import requests

class OpenSkyFetcher(AircraftDataFetcher):
    def __init__(self, username=None, password=None, bounds=None):
        """
        Args:
            username (str): OpenSky API username (optional for public endpoint).
            password (str): OpenSky API password (optional for public endpoint).
            bounds (tuple): (min_lat, min_lon, max_lat, max_lon) for area filtering.
        """
        self.auth = (username, password) if username and password else None
        self.bounds = bounds
        self.base_url = "https://opensky-network.org/api/states/all"

    def fetch_aircraft_data(self):
        """Fetch raw data from OpenSky's States API."""
        params = {}
        if self.bounds:
            params.update({
                "lamin": self.bounds[0],
                "lomin": self.bounds[1],
                "lamax": self.bounds[2],
                "lomax": self.bounds[3],
            })

        response = requests.get(
            self.base_url,
            params=params,
            auth=self.auth,
            timeout=10  # Avoid hanging
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def normalize_data(raw_data):
        """
        Convert OpenSky's "states" array to standard format.
        OpenSky's response fields: https://opensky-network.org/apidoc/rest.html
        """
        return [
            {
                "icao": state[0],           # Transponder address
                "callsign": state[1].strip() if state[1] else None,
                "latitude": state[6],       # Degrees
                "longitude": state[5],      # Degrees
                "altitude": state[7],       # Meters
                "speed": state[9],          # m/s → convert to km/h if needed
                "heading": state[10],       # Degrees
                "source": "opensky",
            }
            for state in raw_data.get("states", [])
            if state[6] and state[5]  # Only include aircraft with positions
        ]
