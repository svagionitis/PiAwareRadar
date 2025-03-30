from .dump1090 import Dump1090Fetcher
from .flightradar24 import FlightRadar24Fetcher
from .adsbexchange import ADSBExchangeFetcher
from .opensky import OpenSkyFetcher

class AircraftDataAggregator:
    def __init__(self, fetchers=None):
        self.fetchers = fetchers or [
            Dump1090Fetcher(),
            ADSBExchangeFetcher(),
            OpenSkyFetcher(),  # Add OpenSky (public endpoint)
            FlightRadar24Fetcher(api_key="API_KEY"),  # Enable if available
        ]

    def get_all_aircraft(self):
        """Fetch and merge data from all sources."""
        all_aircraft = []
        for fetcher in self.fetchers:
            try:
                all_aircraft.extend(fetcher.get_aircraft())
            except Exception as e:
                print(f"Error fetching from {fetcher.__class__.__name__}: {e}")
        return all_aircraft

# Export all fetchers for external use
__all__ = [
    "AircraftDataAggregator",
    "Dump1090Fetcher",
    "OpenSkyFetcher",
    "ADSBExchangeFetcher",
]
