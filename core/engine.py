import random
import time

from colorama import init, Fore, Style
from utils.clean_screen import clear


def game_loop(player):
    clear()
    while True:
        loc = player.lm.get_location(player.location)
        if loc:
            print(Fore.YELLOW + f"\n== {loc['name']} ==")
            print(loc['description'])

            exits = loc.get("exits", {})
            exits_desc = []
            for direction, dest_id in exits.items():
                dest_loc = player.lm.get_location(dest_id)
                dest_name = dest_loc['name'] if dest_loc else "Nieznana lokacja"
                exits_desc.append(f"{direction} ({dest_name})")

            print("Dostępne wyjścia: " + ", ".join(exits_desc))

            print(Fore.YELLOW + f"== {loc['name']} ==")
        else:
            print(Fore.RED + "\nNieznana lokacja.")

        print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
        print("stat / statystyki / info – pokaż status gracza")
        print("zapisz / save - zapisz stan gry")
        print("north / south / east / west – porusz się w danym kierunku")

        wybor = input(
            f"\n<hp{player.hp}/{player.max_hp}> <g{player.gold}> <exp{player.exp}/{player.exp_to_next_level()}> >> "
        ).lower().strip()

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
        elif wybor in ["north", "south", "east", "west", "up", "down"]:
            player.move(wybor)
            time.sleep(0.5)
            clear()
        else:
            print(Fore.RED + random.choice([
                "Nie rozumiem.",
                "Hm?????",
                "Co to ma znaczyć?",
                "Spróbuj jeszcze raz.",
                "Nie mam pojęcia o co chodzi."
            ]))
            time.sleep(0.8)
            clear()