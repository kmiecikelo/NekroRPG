import os
import json

class ItemManager:
    def __init__(self, items_folder="data/items"):
        self.items_folder = items_folder
        self.items = {}  # id -> item dict
        self.load_items()

    def load_items(self):
        self.items = {}
        for filename in os.listdir(self.items_folder):
            if filename.endswith(".json"):
                path = os.path.join(self.items_folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        self.items[item["id"]] = item

    def get_item(self, item_id):
        return self.items.get(item_id)
