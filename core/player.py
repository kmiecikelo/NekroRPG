import time

from core.location_manager import LocationManager
from utils.clean_screen import clear
from colorama import init, Fore, Style
import json

class Player:
    def __init__(self, name, max_hp=50, strength=5, defence=5, dexterity=5, level=1, exp=0, exptonextlvl=100,
                 klasa="Wojownik", rasa="Człowiek", gold=0, lp=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp

        self.strength = strength  # siła – wpływa na dmg
        self.defence = defence  # obrona – np. wpływa na otrzymywane dmg
        self.dexterity = dexterity  # obrona – np. wpływa na otrzymywane dmg

        self.level = level
        self.exp = exp
        self.exptonextlvl = exptonextlvl
        self.klasa = klasa
        self.rasa = rasa
        self.gold = gold
        self.lp = lp

        self.location = "start"  # aktualna lokacja
        self.lm = LocationManager()  # menedżer lokacji

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

    def move(self, direction):
        loc = self.lm.get_location(self.location)
        if not loc:
            print("Błąd: nieznana lokalizacja.")
            return

        exits = loc.get("exits", {})
        if direction in exits:
            self.location = exits[direction]
            print(Fore.GREEN + f"Przechodzisz {direction} do {self.location}.")
            time.sleep(0.5)
        else:
            print(Fore.RED + "Nie możesz tam pójść.")


    def to_dict(self):
        return {
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
        return p

    def save(self, filename="save.json"):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @staticmethod
    def load(filename="save.json"):
        with open(filename, "r") as f:
            data = json.load(f)
            return Player.from_dict(data)