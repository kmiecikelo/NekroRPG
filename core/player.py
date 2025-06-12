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

    def to_dict(self):
        return {
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
        }

    @staticmethod
    def from_dict(data):
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