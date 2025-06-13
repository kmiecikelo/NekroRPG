import hashlib
import os
import time

from core.dialogue import NPC
from core.item_manager import ItemManager
from core.location_manager import LocationManager
from utils.clean_screen import clear
from utils.load_game_version import CURRENT_GAME_VERSION
from colorama import init, Fore, Style
import marshal


class Player:
    def __init__(self, name, max_hp=50, strength=5, defence=5, dexterity=5, level=1, exp=0,
                 klasa="Wojownik", rasa="Człowiek", gold=0, lp=0):
        # Inicjalizacja podstawowych atrybutów
        self.name = name
        self.level = max(level, 1)
        self.exp = max(exp, 0)
        self.klasa = klasa
        self.rasa = rasa
        self.gold = max(gold, 0)
        self.lp = max(lp, 0)
        self.inventory = {}
        self.location = "xyras_house"

        # Inicjalizacja menedżerów
        self.item_manager = ItemManager()
        self.lm = LocationManager()

        # Inicjalizacja statystyk ekwipunku
        self.equipment_stats = {
            "strength": 0,
            "defence": 0,
            "dexterity": 0,
            "max_hp": 0
        }

        # Inicjalizacja ekwipunku
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

        # Statystyki bazowe
        self.base_max_hp = max(max_hp, 0)
        self.base_strength = max(strength, 0)
        self.base_defence = max(defence, 0)
        self.base_dexterity = max(dexterity, 0)

        # Inicjalizacja HP przed update_stats()
        self.max_hp = self.calculate_max_hp()
        self.hp = self.max_hp  # Ustawiamy pełne HP na start

        # Inicjalizacja pozostałych statystyk
        self.update_stats()

    def calculate_max_hp(self):
        """Oblicza maksymalne HP na podstawie statystyki bazowej i poziomu"""
        return self.base_max_hp + (self.level - 1) * 10 + self.equipment_stats.get("max_hp", 0)

    def calculate_strength(self):
        """Oblicza siłę na podstawie statystyki bazowej i poziomu"""
        return self.base_strength + (self.level - 1) * 2 + self.equipment_stats.get("strength", 0)

    def calculate_defence(self):
        """Oblicza obronę na podstawie statystyki bazowej i poziomu"""
        return self.base_defence + (self.level - 1) * 1 + self.equipment_stats.get("defence", 0)

    def calculate_dexterity(self):
        """Oblicza zręczność na podstawie statystyki bazowej i poziomu"""
        return self.base_dexterity + (self.level - 1) * 1 + self.equipment_stats.get("dexterity", 0)

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
        print(f"{Fore.YELLOW}Punkty Nauki: {Fore.RED}{self.lp}")

        print("\n" + Fore.CYAN + "=" * 20 + " STATYSTYKI " + "=" * 20)
        stats_display = {
            "strength": "Siła",
            "defence": "Obrona",
            "dexterity": "Zręczność",
            "max_hp": "Maks. HP"
        }

        for stat_key, stat_name in stats_display.items():
            base_value = getattr(self, f"base_{stat_key}") if hasattr(self, f"base_{stat_key}") else 0
            level_bonus = (self.level - 1) * (10 if stat_key == "max_hp" else (2 if stat_key == "strength" else 1))
            bonus = self.equipment_stats.get(stat_key, 0)
            total = base_value + level_bonus + bonus

            print(f"{Fore.YELLOW}{stat_name}: {Fore.RED}{total} "
                  f"{Fore.WHITE}(bazowa: {base_value}, poziom: +{level_bonus}, ekwipunek: +{bonus})")

    def exp_to_next_level(self):
        if self.level <= 10:
            return 100 * self.level  # Wczesne poziomy: szybko
        else:
            return int(1000 + 500 * (self.level - 10))

    def check_level_up(self):
        while self.exp >= self.exp_to_next_level():
            required_exp = self.exp_to_next_level()
            self.exp -= required_exp
            self.level += 1
            self.lp += 5
            self.update_stats()
            self.hp = self.max_hp
            reward = self.level * 4  # Złoto
            self.gold += reward
            print(f"\nAwansowałeś na poziom {Fore.RED}{self.level}{Style.RESET_ALL}! Nagroda: {reward} złota")
            input(Fore.GREEN + "\nNaciśnij Enter aby przejść dalej..." + Style.RESET_ALL)
            clear()

    def update_stats(self):
        """Aktualizuje wszystkie statystyki po zmianach"""
        self.max_hp = self.calculate_max_hp()
        self.hp = min(self.hp, self.max_hp)
        self.strength = self.calculate_strength()
        self.defence = self.calculate_defence()
        self.dexterity = self.calculate_dexterity()

    def add_stats(self, strength=0, defence=0, dexterity=0, max_hp=0):
        """Dodaje punkty do statystyk bazowych"""
        self.base_strength += strength
        self.base_defence += defence
        self.base_dexterity += dexterity
        self.base_max_hp += max_hp
        self.update_stats()  # Aktualizuje wszystkie statystyki
        print(
            f"Otrzymałeś bonus do statystyk: +{strength} Siły, +{defence} Obrony, "
            f"+{dexterity} Zręczności, +{max_hp} Maks. HP")
        input(Fore.GREEN + "\nNaciśnij Enter aby przejść dalej..." + Style.RESET_ALL)

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
        print(f"Podniosłeś {amount} x {self.item_manager.get_item(item_id)['name']}.")
        time.sleep(1)
        self.add_item(item_id, amount)
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
        if not item:
            return False

        if item.get("required_level", 0) > self.level:
            print(f"Wymagany poziom: {item['required_level']}!")
            return False

        restrictions = item.get("class_restrictions", [])
        if restrictions and self.klasa not in restrictions:
            print(f"Twoja klasa ({self.klasa}) nie może użyć tego przedmiotu!")
            return False

        return True

    def equip(self, item_id):
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

        if self.equipment[slot] is not None:
            self.unequip(slot)

        self.equipment[slot] = item_id
        self.remove_item(item_id, 1)
        self.update_equipment_stats()

        print(f"Założono: {item['name']}!")
        return True

    def unequip(self, slot):
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
        self.equipment_stats = {k: 0 for k in self.equipment_stats}

        for item_id in filter(None, self.equipment.values()):
            item = self.item_manager.get_item(item_id)
            if item and "stats" in item:
                for stat, value in item["stats"].items():
                    if stat in self.equipment_stats:
                        self.equipment_stats[stat] += value

        self.update_stats()

    def show_equipment(self):
        clear()
        print("\n" + Fore.CYAN + "=" * 20 + " WYPOSAŻENIE " + "=" * 20)

        for slot, item_id in self.equipment.items():
            item = self.item_manager.get_item(item_id) if item_id else None
            slot_name = slot.replace("_", " ").title()

            if item:
                stats_str = ", ".join(f"{stat}+{value}" for stat, value in item.get("stats", {}).items())
                print(f"{Fore.YELLOW}{slot_name}: {Fore.GREEN}{item['name']} {Fore.WHITE}({stats_str})")
            else:
                print(f"{Fore.YELLOW}{slot_name}: {Fore.RED}Puste")

        print("\n" + Fore.CYAN + "=" * 20 + " STATYSTYKI " + "=" * 20)
        stats_display = {
            "strength": "Siła",
            "defence": "Obrona",
            "dexterity": "Zręczność",
            "max_hp": "Maks. HP"
        }

        for stat_key, stat_name in stats_display.items():
            base_value = getattr(self, f"base_{stat_key}") if hasattr(self, f"base_{stat_key}") else 0
            level_bonus = (self.level - 1) * (2 if stat_key == "strength" else 1)
            bonus = self.equipment_stats.get(stat_key, 0)
            total = base_value + level_bonus + bonus

            print(f"{Fore.YELLOW}{stat_name}: {Fore.RED}{total} "
                  f"{Fore.WHITE}(bazowa: {base_value}, poziom: +{level_bonus}, ekwipunek: +{bonus})")

    def talk_to_npc(self, npc_name):
        loc = self.lm.get_location(self.location)
        npcs = loc.get("npcs", [])

        for npc_data in npcs:
            if npc_data["name"].lower() == npc_name.lower():
                if "dialogues" in npc_data:
                    npc = NPC(
                        name=npc_data["name"],
                        description=npc_data["description"],
                        dialogues=npc_data["dialogues"]
                    )

                    while True:
                        available_options = npc.start_dialogue(self)

                        # Jeśli nie ma dostępnych opcji, zakończ dialog
                        if available_options is None:

                            return True

                        try:
                            choice = input(f"\n{Fore.CYAN}>> {Style.RESET_ALL}").strip()
                            if choice == "0":
                                break

                            choice_index = int(choice)
                            if not npc.process_choice(choice_index, available_options, self):
                                break

                        except (ValueError, IndexError):
                            print(Fore.RED + "Nieprawidłowy wybór!")
                            continue


                    return True

        print(Fore.RED + f"Nie ma NPC o nazwie '{npc_name}' z którym możesz rozmawiać.")
        return False

    def check_condition(self, condition):
        """Sprawdza warunek dialogu"""
        if condition is None:
            return True
        elif isinstance(condition, str):
            try:
                return eval(condition, {"p": self})
            except:
                return False
        elif callable(condition):
            return condition(self)
        return False

    def to_dict(self):
        data = {
            "version": CURRENT_GAME_VERSION,
            "name": self.name,
            "base_max_hp": self.base_max_hp,
            "base_strength": self.base_strength,
            "base_defence": self.base_defence,
            "base_dexterity": self.base_dexterity,
            "hp": self.hp,
            "exp": self.exp,
            "level": self.level,
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
        p = Player(data["name"],
                   max_hp=data.get("base_max_hp", 50),
                   strength=data.get("base_strength", 5),
                   defence=data.get("base_defence", 5),
                   dexterity=data.get("base_dexterity", 5),
                   level=data.get("level", 1),
                   exp=data.get("exp", 0),
                   klasa=data.get("klasa", "Wojownik"),
                   rasa=data.get("rasa", "Człowiek"),
                   gold=data.get("gold", 0),
                   lp=data.get("lp", 0))

        p.hp = data.get("hp", p.max_hp)
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
        p.update_stats()
        return p

    def save(self, filename="save.dat"):
        try:
            data = self.to_dict()
            data_str = str(sorted(data.items()))
            data["_integrity"] = hashlib.sha256(data_str.encode()).hexdigest()

            with open(filename, "wb") as f:
                marshal.dump(data, f)
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load(filename="save.dat"):
        try:
            if not os.path.exists(filename):
                return None

            with open(filename, "rb") as f:
                data = marshal.load(f)

            integrity_check = data.pop("_integrity")
            data_str = str(sorted(data.items()))
            if hashlib.sha256(data_str.encode()).hexdigest() != integrity_check:
                print(Fore.RED + "Plik zapisu został zmodyfikowany!")
                return None

            save_version = data.get("version", "0.0.0")
            if save_version != CURRENT_GAME_VERSION:
                print(Fore.RED + f"Nieprawidłowa wersja zapisu ({save_version}). Wersja gry ({CURRENT_GAME_VERSION})")
                return None

            return Player.from_dict(data)

        except Exception as e:
            print(Fore.RED + f"Błąd podczas wczytywania gry: {e}")
            return None