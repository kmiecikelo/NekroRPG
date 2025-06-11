import random
import time

from colorama import init, Fore, Style
from utils.clean_screen import clear


def game_loop(player):
    clear()
    while True:
        loc = player.lm.get_location(player.location)
        if loc:
            print("\n" + Fore.CYAN + "=" * 20 + " LOKACJA " + "=" * 20)
            print(f"{Fore.YELLOW}Nazwa: {Style.BRIGHT}{loc['name']}")
            print(f"{Fore.YELLOW}Opis: {Style.RESET_ALL}{loc['description']}\n")

            items = loc.get("items")
            if items:
                print(f"{Fore.MAGENTA}Przedmioty w lokacji:")
                for item in items:
                    print(f"  - {item}")
                print()  # pusta linia dla czytelności

            exits = loc.get("exits", {})
            exits_desc = []
            for direction, dest_id in exits.items():
                dest_loc = player.lm.get_location(dest_id)
                dest_name = dest_loc['name'] if dest_loc else "Nieznana lokacja"
                exits_desc.append(f"{Fore.GREEN}{direction}{Style.RESET_ALL} ({dest_name})")

            print(f"{Fore.YELLOW}Dostępne wyjścia: " + ", ".join(exits_desc))
        else:
            print(Fore.RED + "\nNieznana lokacja.")

        print("\n" + Fore.CYAN + "=" * 23 + " MENU " + "=" * 23)
        print("stat / statystyki / info – pokaż status gracza")
        print("inv / eq / ekwipunek / inventory – pokaż ekwipunek gracza")
        print("pick / zbierz / weź – podnosi przedmiot")
        print("zapisz / save - zapisz stan gry")
        print("north / south / east / west – porusz się w danym kierunku")
        print("exit / koniec  – wyjdź z gry")

        wybor = input(
            f"\n<hp{player.hp}/{player.max_hp}> <g{player.gold}> <exp{player.exp}/{player.exp_to_next_level()}> >> "
        ).lower().strip()

        if wybor in ["stat", "statystyki", "info", "informacje", "stats"]:
            player.status()
        elif wybor in ["inv", "eq", "ekwipunek", "inventory"]:
            player.show_inventory()
        elif wybor.startswith(("pick ", "zbierz ", "weź ")):
            # wyciągamy nazwę przedmiotu po spacji
            # usuwamy pierwszy wyraz i pobieramy resztę jako nazwę przedmiotu
            parts = wybor.split(" ", 1)
            if len(parts) > 1:
                item_name = parts[1].strip()
                if item_name:
                    success = player.pick_item(item_name)
                    if not success:
                        print(Fore.RED + "Nie udało się podnieść przedmiotu.")
                else:
                    print(Fore.RED + "Podaj nazwę przedmiotu do podniesienia.")
            else:
                print(Fore.RED + "Podaj nazwę przedmiotu do podniesienia.")
            time.sleep(1)
            clear()
        elif wybor in ["exit", "koniec"]:
            exit()
        elif wybor == "exp100":
            player.gain_exp(100)
        elif wybor == "exp1000":
            player.gain_exp(1000)
        elif wybor == "addsword":
            player.add_item("sword_01", 1)
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