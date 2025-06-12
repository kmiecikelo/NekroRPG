import hashlib
import os
import time

from core.item_manager import ItemManager
from core.location_manager import LocationManager
from utils.clean_screen import clear
from utils.load_game_version import CURRENT_GAME_VERSION
from colorama import init, Fore, Style
import marshal




class Player:
    def __init__(self, name, max_hp=50, strength=5, defence=5, dexterity=5, level=1, exp=0,
                 klasa="Wojownik", rasa="Człowiek", gold=0, lp=0):
        self.name = name
        self.max_hp = max(max_hp, 0)
        self.hp = self.max_hp
        self.strength = max(strength, 0)
        self.defence = max(defence, 0)
        self.dexterity = max(dexterity, 0)
        self.level = max(level, 1)
        self.exp = max(exp, 0)
        self.klasa = klasa
        self.rasa = rasa
        self.gold = max(gold, 0)
        self.lp = max(lp, 0)
        self.inventory = {}
        self.item_manager = ItemManager()
        self.location = "xyras_house"
        self.lm = LocationManager()
        self.equipment = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "gloves": None,
            "boots": None,
            "ring_1": None,
            "ring_2": None,
            "amulet": None
        }
        self.equipment_stats = {  # Suma statystyk z całego wyposażenia
            "strength": 0,
            "defence": 0,
            "dexterity": 0,
            "max_hp": 0
        }

    def status(self):
        clear()
        print("\n" + Fore.CYAN + "=" * 20 + " INFORMACJE " + "=" * 20)
        print(f"{Fore.YELLOW}Imię: {Style.BRIGHT}{self.name}")
        print(f"{Fore.YELLOW}Złoto: {Style.BRIGHT}{self.gold} sztuk")
        print(f"{Fore.YELLOW}Klasa: {Style.BRIGHT}{self.klasa}")
        print(f"{Fore.YELLOW}Rasa: {Style.BRIGHT}{self.rasa}")
        print(f"{Fore.YELLOW}Zdrowie: {Fore.GREEN}{self.hp}/{self.max_hp}")
        print(f"{Fore.YELLOW}Poziom: {Fore.MAGENTA}{self.level}  "
              f"{Fore.YELLOW}Doświadczenie: {Fore.BLUE}{self.exp}/{self.exp_to_next_level()}")

        print("\n" + Fore.CYAN + "=" * 20 + " STATYSTYKI " + "=" * 20)
        print(f"{Fore.YELLOW}Punkty Nauki: {Fore.RED}{self.lp}")
        print(f"{Fore.YELLOW}Siła: {Fore.RED}{self.strength}")
        print(f"{Fore.YELLOW}Obrona: {Fore.RED}{self.defence}")
        print(f"{Fore.YELLOW}Zręczność: {Fore.RED}{self.dexterity}")

    def exp_to_next_level(self):
        return int(100 * (1.1 ** (self.level - 1)))

    def check_level_up(self):
        while self.exp >= self.exp_to_next_level():
            required_exp = self.exp_to_next_level()
            self.exp -= required_exp
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.strength += 2
            self.lp += 5
            self.defence += 1
            self.dexterity += 1
            print(f"\nAwansowałeś na poziom {Fore.RED}{self.level}{Style.RESET_ALL}!")
            input(Fore.GREEN + "\nNaciśnij Enter aby przejść dalej..." + Style.RESET_ALL)
            clear()

    def gain_exp(self, amount):
        print(f"Otrzymałeś: \n+{amount} punktów doświadczenia")
        self.exp += amount
        self.check_level_up()

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"Przywrocono {amount} HP. Aktualne HP: {self.hp}/{self.max_hp}")

    def move(self, direction):
        loc = self.lm.get_location(self.location)
        if not loc:
            print("Błąd: nieznana lokalizacja.")
            return
        exits = loc.get("exits", {})
        if direction in exits:
            new_location_id = exits[direction]
            new_location = self.lm.get_location(new_location_id)
            if new_location:
                self.location = new_location_id
                print(Fore.GREEN + f"Przechodzisz {direction} do {new_location['name']}.")
                time.sleep(1)
            else:
                print(Fore.RED + "Błąd: docelowa lokacja nie istnieje.")
        else:
            print(Fore.RED + "Nie możesz tam pójść.")

    def add_item(self, item_id, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if not self.item_manager:
            raise RuntimeError("Item manager not set.")
        if item_id not in self.item_manager.items:
            raise ValueError(f"Item {item_id} does not exist.")
        item_name = self.item_manager.items[item_id]['name']
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity
        print(f"Dodano do ekwipunku: {item_name} x{quantity}")
        time.sleep(1.5)

    def remove_item(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]

    def pickitem(self, item_id, amount=1):
        loc = self.lm.get_location(self.location)
        if not loc:
            print("Nieznana lokacja.")
            return
        items = loc.get("items", {})
        if item_id not in items:
            print("Nie ma takiego przedmiotu w tej lokacji.")
            return
        available_amount = items[item_id]
        if available_amount < amount:
            print(f"Nie ma tyle przedmiotów do podniesienia. Dostępne: {available_amount}")
            return
        # Dodajemy przedmiot do ekwipunku gracza
        print(f"Podniosłeś {amount} x {self.item_manager.get_item(item_id)['name']}.")
        time.sleep(1)
        self.add_item(item_id, amount)
        # Odejmujemy z lokacji
        if available_amount == amount:
            del items[item_id]
        else:
            items[item_id] -= amount

    def show_inventory(self):
        clear()
        print("\n" + Fore.CYAN + "=" * 20 + " EKWIPUNEK " + "=" * 20)
        if not self.inventory:
            print(Fore.YELLOW + "Brak przedmiotów w ekwipunku.")
            return

        for item_id, qty in self.inventory.items():
            item = self.item_manager.get_item(item_id) if self.item_manager else None
            item_name = item["name"] if item and "name" in item else item_id
            item_description = item["description"] if item and "description" in item else ""
            print(Fore.YELLOW + f"{item_name}: {Style.BRIGHT}x{qty} - {item_description}")

    def can_equip(self, item):
        """Sprawdza czy gracz może założyć przedmiot"""
        if not item:
            return False

        # Sprawdź wymagany poziom
        if item.get("required_level", 0) > self.level:
            print(f"Wymagany poziom: {item['required_level']}!")
            return False

        # Sprawdź ograniczenia klasowe
        restrictions = item.get("class_restrictions", [])
        if restrictions and self.klasa not in restrictions:
            print(f"Twoja klasa ({self.klasa}) nie może użyć tego przedmiotu!")
            return False

        return True

    def equip(self, item_id):
        """Zakłada przedmiot z ekwipunku"""
        if item_id not in self.inventory or self.inventory[item_id] < 1:
            print(f"Nie posiadasz: {item_id}!")
            return False

        item = self.item_manager.get_item(item_id)
        if not item or not self.can_equip(item):
            return False

        slot = item.get("slot")
        if not slot or slot not in self.equipment:
            print("Ten przedmiot nie może być założony!")
            return False

        # Zdejmij obecny przedmiot jeśli slot zajęty
        if self.equipment[slot] is not None:
            self.unequip(slot)

        # Załóż nowy przedmiot
        self.equipment[slot] = item_id
        self.remove_item(item_id, 1)
        self.update_equipment_stats()

        print(f"Założono: {item['name']}!")
        return True

    def unequip(self, slot):
        """Zdejmuje przedmiot z danego slotu"""
        if slot not in self.equipment:
            return False

        item_id = self.equipment[slot]
        if item_id is None:
            return False

        item = self.item_manager.get_item(item_id)
        if not item:
            return False

        self.add_item(item_id, 1)
        self.equipment[slot] = None
        self.update_equipment_stats()

        print(f"Zdjęto: {item['name']}!")
        return True

    def update_equipment_stats(self):
        """Przelicza sumę statystyk z wyposażenia"""
        # Resetujemy statystyki
        self.equipment_stats = {k: 0 for k in self.equipment_stats}

        # Obliczamy sumę statystyk z wszystkich założonych przedmiotów
        for item_id in filter(None, self.equipment.values()):
            item = self.item_manager.get_item(item_id)
            if item and "stats" in item:
                for stat, value in item["stats"].items():
                    if stat in self.equipment_stats:
                        self.equipment_stats[stat] += value

        # Bazowe statystyki (bez ekwipunku)
        base_stats = {
            "max_hp": self.max_hp + (self.level - 1) * 10,
            "strength": self.strength + (self.level - 1) * 2,
            "defence": self.defence + (self.level - 1) * 1,
            "dexterity": self.dexterity + (self.level - 1) * 1
        }

        # Aktualizacja statystyk gracza (uwzględniając bonusy z ekwipunku)
        self.max_hp = base_stats["max_hp"] + self.equipment_stats.get("max_hp", 0)
        self.hp = min(self.hp, self.max_hp)
        self.strength = base_stats["strength"] + self.equipment_stats.get("strength", 0)
        self.defence = base_stats["defence"] + self.equipment_stats.get("defence", 0)
        self.dexterity = base_stats["dexterity"] + self.equipment_stats.get("dexterity", 0)

    def show_equipment(self):
        """Wyświetla ekran wyposażenia"""
        clear()
        print("\n" + Fore.CYAN + "=" * 20 + " WYPOSAŻENIE " + "=" * 20)

        # Wyświetl założone przedmioty
        for slot, item_id in self.equipment.items():
            item = self.item_manager.get_item(item_id) if item_id else None
            slot_name = slot.replace("_", " ").title()

            if item:
                stats_str = ", ".join(f"{stat}+{value}" for stat, value in item.get("stats", {}).items())
                print(f"{Fore.YELLOW}{slot_name}: {Fore.GREEN}{item['name']} {Fore.WHITE}({stats_str})")
            else:
                print(f"{Fore.YELLOW}{slot_name}: {Fore.RED}Puste")

        # Wyświetl statystyki z uwzględnieniem bonusów
        print("\n" + Fore.CYAN + "=" * 20 + " STATYSTYKI " + "=" * 20)
        stats_display = {
            "strength": "Siła",
            "defence": "Obrona",
            "dexterity": "Zręczność",
            "max_hp": "Maks. HP"
        }

        for stat_key, stat_name in stats_display.items():
            base_value = getattr(self, stat_key) if stat_key != "max_hp" else (50 + (self.level - 1) * 10)
            bonus = self.equipment_stats.get(stat_key, 0)

            if bonus != 0:
                print(f"{Fore.YELLOW}{stat_name}: {Fore.RED}{base_value} {Fore.GREEN}(+{bonus})")
            else:
                print(f"{Fore.YELLOW}{stat_name}: {Fore.RED}{base_value}")

    def to_dict(self):
        data = {
            "version": CURRENT_GAME_VERSION,
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "exp": self.exp,
            "level": self.level,
            "strength": self.strength,
            "defence": self.defence,
            "dexterity": self.dexterity,
            "klasa": self.klasa,
            "rasa": self.rasa,
            "gold": self.gold,
            "lp": self.lp,
            "location": self.location,
            "inventory": self.inventory,
            "locations": self.lm.to_dict(),
            "equipment": self.equipment,
            "equipment_stats": self.equipment_stats
        }
        return data

    @staticmethod
    def from_dict(data):
        """Rozszerzenie metody from_dict() o wyposażenie"""
        p = Player(data["name"])
        p.hp = data["hp"]
        p.max_hp = data["max_hp"]
        p.exp = data["exp"]
        p.level = data["level"]
        p.strength = data["strength"]
        p.defence = data["defence"]
        p.dexterity = data["dexterity"]
        p.klasa = data["klasa"]
        p.rasa = data["rasa"]
        p.gold = data["gold"]
        p.lp = data["lp"]
        p.location = data["location"]
        p.inventory = data.get("inventory", {})
        if "locations" in data:
            p.lm.from_dict(data["locations"])
        p.equipment = data.get("equipment", {
            "weapon": None, "armor": None, "helmet": None,
            "gloves": None, "boots": None, "ring_1": None,
            "ring_2": None, "amulet": None
        })
        p.equipment_stats = data.get("equipment_stats", {
            "strength": 0, "defence": 0, "dexterity": 0, "max_hp": 0
        })
        return p

    def save(self, filename="save.dat"):
        try:
            data = self.to_dict()

            # Dodajemy hash dla weryfikacji integralności
            data_str = str(sorted(data.items()))  # Sortowanie dla spójności
            data["_integrity"] = hashlib.sha256(data_str.encode()).hexdigest()

            # Zapis binarny z marshal
            with open(filename, "wb") as f:
                marshal.dump(data, f)
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load(filename="save.dat"):
        try:
            # Sprawdzenie czy plik istnieje
            if not os.path.exists(filename):
                return None

            # Odczyt danych
            with open(filename, "rb") as f:
                data = marshal.load(f)

            # Weryfikacja integralności
            integrity_check = data.pop("_integrity")
            data_str = str(sorted(data.items()))
            if hashlib.sha256(data_str.encode()).hexdigest() != integrity_check:
                print(Fore.RED + "Plik zapisu został zmodyfikowany!")
                return None

            # Weryfikacja wersji
            save_version = data.get("version", "0.0.0")
            if save_version != CURRENT_GAME_VERSION:
                print(Fore.RED + f"Nieprawidłowa wersja zapisu ({save_version}). Wersja gry ({CURRENT_GAME_VERSION})")
                return None

            return Player.from_dict(data)

        except Exception as e:
            print(Fore.RED + f"Błąd podczas wczytywania gry: {e}")
            return None