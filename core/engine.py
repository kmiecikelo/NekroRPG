import time

from colorama import init, Fore, Style
from utils.clean_screen import clear


def game_loop(player):
    print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
    print("stat / statystyki / info – pokaż status gracza")
    print("zapisz / save - zapisz stan gry")
    print("\n" * 2 + Fore.CYAN + "=" * 23 + " KODY " + "=" * 23)
    print("exp100 – dodaj 100 expa")
    print("exp1000 – dodaj 1000 expa")

    wybor = input(f"\n<hp{player.hp}/{player.max_hp}> <g{player.gold}> <exp{player.exp}/{player.exp_to_next_level()}> >> ").lower().strip()

    if wybor in ["stat", "statystyki", "info", "informacje", "stats"]:
        player.status()
    elif wybor == "exp100":
        player.gain_exp(100)
    elif wybor == "exp1000":
        player.gain_exp(1000)
    elif wybor in ["zapisz", "save"]:
        player.save()
        print(Fore.GREEN + "Gra zapisana!")
        time.sleep(0.8)
        clear()
    else:
        print(Fore.RED + "Nieprawidłowa komenda.")
        time.sleep(0.8)
        clear()