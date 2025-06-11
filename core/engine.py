from colorama import init, Fore, Style
from scenes.intro import create_player
from core.player import Player
init(autoreset=True, convert=True)

def game_loop(player):
    print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
    print("Co chcesz zrobić?")
    print("stat / statystyki / info – pokaż status gracza")
    print("stat / statystyki / info – pokaż status gracza")
    print("\n" * 2 + Fore.CYAN + "=" * 23 + " KODY " + "=" * 23)
    print("exp100 – dodaj 100 expa")
    print("exp1000 – dodaj 1000 expa")

    wybor = input(f"\nWpisz komendę: ").lower().strip()

    if wybor in ["stat", "statystyki", "info", "informacje"]:
        player.status()
    elif wybor == "exp100":
        player.gain_exp(100)
    elif wybor == "exp1000":
        player.gain_exp(1000)
    elif wybor in ["zapisz", "save"]:
        player.save()
        print(Fore.GREEN + "Gra zapisana!")
    else:
        print(Fore.RED + "Nieprawidłowa komenda.")