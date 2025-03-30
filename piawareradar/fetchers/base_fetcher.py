from abc import ABC, abstractmethod
import requests

class AircraftDataFetcher(ABC):
    """Abstract base class for all aircraft data fetchers."""

    @abstractmethod
    def fetch_aircraft_data(self):
        """Fetch raw aircraft data from the source."""
        pass

    @staticmethod
    def normalize_data(raw_data):
        """Convert raw API response into a standardized format."""
        pass

    def get_aircraft(self):
        """Public method: Fetch and normalize data."""
        raw_data = self.fetch_aircraft_data()
        return self.normalize_data(raw_data)
