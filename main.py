from core.player import Player
from utils.clean_screen import clear
from utils.slow_print import slow_print
from colorama import init, Fore, Style
import time
init(autoreset=True)

game = False
createplayer = True

if createplayer:
    slow_print("...Ciemność.")
    time.sleep(1)
    slow_print("Cisza.")
    time.sleep(1)
    slow_print("Tylko wiatr niosący piach, który drażni twoją skórę.")
    time.sleep(1)
    slow_print("Otwierasz oczy. Oślepia cię słońce, a gardło masz suche jak popiół.")
    slow_print("Nie pamiętasz, kim jesteś. Ani skąd się tu wziąłeś.")
    time.sleep(1)
    slow_print("W oddali majaczy kształt... może obóz, może ruiny?")
    time.sleep(1)
    slow_print("Jedno wiesz na pewno: musisz przetrwać.")
    time.sleep(1)
    slow_print("Nie do końca pamiętasz jak się nazywasz.")
    time.sleep(1)
    slow_print("W Twoich myślach układa się coś na wzór:")
    while True:
        name = input(">: ").strip()
        if name:
            break
        print("Imię nie może być puste.")
    player = Player(name, 50,)

while game:
    print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
    print("Co chcesz zrobić?")
    print("stat / statystyki / info – pokaż status gracza")
    print("\n"*2 + Fore.CYAN + "=" * 23 + " KODY " + "=" * 23)
    print("exp100 – dodaj 100 expa")
    print("exp1000 – dodaj 1000 expa")

    wybor = input(f"\nWpisz komendę: ").lower().strip()

    if wybor in ["stat", "statystyki", "info", "informacje"]:
        player.status()
    elif wybor == "exp100":
        player.gain_exp(100)
    elif wybor == "exp1000":
        player.gain_exp(1000)
    else:
        print(Fore.RED + "Nieprawidłowa komenda.")