import os
import json

class LocationManager:
    def __init__(self, data_folder="data/locations"):
        self.data_folder = data_folder
        self.locations = {}
        self.load_locations()

    def load_locations(self):
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_folder, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.locations.update(data)

    def get_location(self, loc_id):
        return self.locations.get(loc_id)

