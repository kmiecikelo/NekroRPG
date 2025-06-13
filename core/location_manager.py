import os
import sys
import json

def resource_path(relative_path):
    """Zwraca poprawną ścieżkę do pliku po spakowaniu przez PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class LocationManager:
    def __init__(self, data_folder="data/locations"):
        self.data_folder = resource_path(data_folder)
        self.locations = {}
        self.load_locations()

    def load_locations(self):
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(self.data_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.locations.update(data)

    def get_location(self, loc_id):
        return self.locations.get(loc_id)

    def get_npcs(self, loc_id):
        location = self.get_location(loc_id)
        return location.get("npcs", []) if location else []

    def to_dict(self):
        return self.locations

    def from_dict(self, data):
        self.locations = data