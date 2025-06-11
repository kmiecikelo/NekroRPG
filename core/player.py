from utils.clean_screen import clear
from colorama import init, Fore, Style
init(autoreset=True)

class Player:
    def __init__(self, name, max_hp=50, strength=5, defence=5, dexterity=5, level=1, exp=0, exptonextlvl=100):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp

        self.strength = strength  # siła – wpływa na dmg
        self.defence = defence  # obrona – np. wpływa na otrzymywane dmg
        self.dexterity = dexterity  # obrona – np. wpływa na otrzymywane dmg

        self.level = level
        self.exp = exp
        self.exptonextlvl = exptonextlvl

    def status(self):
        clear()
        print("\n" + Fore.CYAN + "=" * 20 + " INFORMACJE " + "=" * 20)
        print(f"{Fore.YELLOW}Imię: {Style.BRIGHT}{self.name}")
        print(f"{Fore.YELLOW}Zdrowie: {Fore.GREEN}{self.hp}/{self.max_hp}")
        print(f"{Fore.YELLOW}Poziom: {Fore.MAGENTA}{self.level}  "
              f"{Fore.YELLOW}Doświadczenie: {Fore.BLUE}{self.exp}/{self.exp_to_next_level()}")

        print("\n" + Fore.CYAN + "=" * 20 + " STATYSTYKI " + "=" * 20)
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
            self.defence += 1
            self.dexterity += 1
            print(f"\n🎉 {self.name} awansował na poziom {self.level}!")

    def gain_exp(self, amount):
        print(f"Otrzymałeś: \n+{amount} punktów doświadczenia")
        self.exp += amount
        self.check_level_up()