import os
import sys
import json

def resource_path(relative_path):
    """Zwraca poprawną ścieżkę po spakowaniu przez PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ItemManager:
    def __init__(self, items_folder="data/items"):
        self.items_folder = resource_path(items_folder)
        self.items = {}  # id -> item dict
        self.load_items()

    def load_items(self):
        self.items = {}
        for filename in os.listdir(self.items_folder):
            if filename.endswith(".json"):
                path = os.path.join(self.items_folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        # Obsłuż oba przypadki - pojedynczy przedmiot lub lista
                        if isinstance(data, list):
                            for item in data:
                                self.items[item["id"]] = item
                        elif isinstance(data, dict):  # Pojedynczy przedmiot
                            self.items[data["id"]] = data
                    except json.JSONDecodeError as e:
                        print(f"Błąd w pliku {filename}: {str(e)}")
                    except KeyError as e:
                        print(f"Brak wymaganego pola w pliku {filename}: {str(e)}")

    def get_item(self, item_id):
        return self.items.get(item_id)
