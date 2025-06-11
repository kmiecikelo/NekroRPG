from utils.clean_screen import clear
from colorama import init, Fore, Style
from utils.slow_print import slow_print
from core.player import Player
import time
init(autoreset=True, convert=True)

def create_player():
    clear()
    slow_print("...Ciemność.")
    clear()
    slow_print("Cisza.")
    clear()
    slow_print("Tylko wiatr niosący piach, który drażni Twoją skórę.")
    clear()
    slow_print("Otwierasz oczy. Oślepia Cię słońce, a gardło masz suche jak popiół.")
    clear()
    slow_print("Nie pamiętasz, kim jesteś. Ani skąd się tu wziąłeś.")
    clear()
    slow_print("W oddali majaczy kształt... może obóz, może ruiny?")
    clear()
    slow_print("Jedno wiesz na pewno: musisz przetrwać.")
    clear()
    slow_print("Nie do końca pamiętasz jak się nazywasz.")
    clear()
    slow_print("W Twoich myślach układa się coś na wzór:")

    while True:
        name = input("> ").strip()
        if name:
            break
        clear()
        print("Imię nie może być puste.")

    while True:
        clear()
        slow_print(f"A więc {name}")
        slow_print("Ostatnie miejsce jakie pamiętasz to:")
        slow_print("1. Wioska i Twój ojciec")
        slow_print("2. Handlarz łapiący Cię za rękę")
        slow_print("3. Miejsce pełne tarcz, które służą do przechwytywania strzał")
        wybor = input("\nOstatnie co pamiętam to: ").lower().strip()
        clear()
        if wybor == "1":
            player = Player(name, 50)
            player.strength += 2
            player.klasa = "Wojownik"
            break
        elif wybor == "2":
            player = Player(name, 50)
            player.defence += 2
            player.klasa = "Łotr"
            break
        elif wybor == "3":
            player = Player(name, 50)
            player.dexterity += 2
            player.klasa = "Łucznik"
            break
        else:
            slow_print("To chyba nie tak...")
            time.sleep(2)
            clear()

    slow_print("Więc już powoli odzyskujesz pamięć....")
    slow_print("Dobrze....")
    slow_print("X: Całe szczęście, że Cię znalazłem....")
    slow_print("Jutro wyruszysz w nową podróż....")
    clear()
    return player